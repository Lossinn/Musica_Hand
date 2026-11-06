"""Construye el artículo sobre la plantilla oficial de la Revista UIS Ingenierías.

- Estilos, márgenes y numeración salen de revista/plantilla_UIS.docx (no se modifican).
- Las cifras se leen de analisis/resultados_vision.json (nada escrito a mano).
- Las ecuaciones son OMML reales (LaTeX -> pandoc -> Word).
- Las referencias salen de analisis/refs_crossref.json (metadatos de Crossref/DataCite).
Uso: python -X utf8 construir_articulo.py
"""
from __future__ import annotations

import copy
import html
import json
import re
import tempfile
import zipfile
from pathlib import Path

import docx
import pypandoc
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from lxml import etree

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
PLANTILLA = BASE / "revista" / "plantilla_UIS.docx"
FIG = BASE / "articulo" / "fig"
R = json.loads((BASE / "analisis" / "resultados_vision.json").read_text(encoding="utf-8"))
REFS = {r["doi"]: r for r in json.loads((BASE / "analisis" / "refs_crossref.json").read_text(encoding="utf-8"))}
LOG = []
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def f(x: float, d: int = 1) -> str:
    return f"{x:.{d}f}".replace(".", ",")


# ------------------------------------------------------------------ referencias
CLAVES = {
    "yi": "10.1007/s10462-023-10637-7", "mediapipe": "10.48550/arXiv.2006.10214",
    "li_hong": "10.1007/s40745-026-00689-1", "li_peerj": "10.7717/peerj-cs.3464",
    "li_disc": "10.1007/s44163-026-01115-4", "deng_sci": "10.1038/s41598-026-53749-0",
    "shi": "10.1007/s44163-026-01858-0", "deng_piano": "10.5216/mh.v26.85176",
    "chulu": "10.1007/s11042-026-21667-y", "tang": "10.1007/s10791-026-10022-2",
    "wang": "10.1007/s44163-026-00832-0", "ramoneda": "10.1016/j.eswa.2026.132088",
    "apay": "10.31681/jetol.1243501", "barroso": "10.6018/red.602301",
    "leon": "10.17811/rifie.20620", "cepeda": "10.1037/0033-2909.132.3.354",
    "corbett": "10.1007/BF01099821", "wilson85": "10.1038/s41467-019-12552-4",
    "wilsonci": "10.1080/01621459.1927.10502953", "wozniak": "10.55782/ane-1994-1003",
}
ORDEN: list[str] = []


def num(clave: str) -> int:
    assert clave in CLAVES or clave == 'dane', clave
    if clave not in ORDEN:
        ORDEN.append(clave)
    return ORDEN.index(clave) + 1


def cita(claves: str) -> str:
    ns = sorted(num(c.strip()) for c in claves.split(","))
    grupos, ini = [], ns[0]
    for a, b in zip(ns, ns[1:] + [None]):
        if b != a + 1:
            grupos.append((ini, a)); ini = b
    return ", ".join(f"[{a}]" if a == b else (f"[{a}], [{b}]" if b == a + 1 else f"[{a}]–[{b}]")
                     for a, b in grupos)


def limpiar(t: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def iniciales(nombre: str) -> str:
    return " ".join(p[0] + "." for p in re.split(r"[ \-]+", nombre.strip()) if p)


def ref_ieee(clave: str) -> str:
    r = REFS[CLAVES[clave]]
    autores = []
    for a in r["autores"].split("; "):
        ap, _, nom = a.partition(", ")
        autores.append(f"{iniciales(nom)} {ap.title() if ap.isupper() else ap}")
    au = autores[0] if len(autores) == 1 else (", ".join(autores[:-1]) + (", and " if len(autores) > 2 else " and ")
                                              + autores[-1])
    if len(autores) > 6:
        au = autores[0] + " et al."
    t = limpiar(r["titulo"])
    s = f"{au}, “{t},” "
    if r["revista"] == "arXiv":
        return s + f"arXiv:2006.10214, {r['anio']}, doi: {r['doi']}."
    s += f"{limpiar(r['revista'])}"
    if r["volumen"]:
        s += f", vol. {r['volumen']}"
    if r["numero"]:
        s += f", no. {r['numero']}"
    if r["paginas"]:
        s += f", {'art. ' if not '-' in str(r['paginas']) else 'pp. '}{r['paginas']}"
    return s + f", {r['anio']}, doi: {r['doi']}."


# ------------------------------------------------------------------ OMML
_cache: dict[tuple[str, bool], etree._Element] = {}


def omml(latex: str, display: bool = False):
    clave = (latex, display)
    if clave not in _cache:
        md = f"$${latex}$$" if display else f"${latex}$"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "m.docx"
            pypandoc.convert_text(md, "docx", format="markdown", outputfile=str(out))
            xml = zipfile.ZipFile(out).read("word/document.xml")
        raiz = etree.fromstring(xml)
        ns = {"m": M_NS}
        el = raiz.find(".//m:oMathPara", ns) if display else raiz.find(".//m:oMath", ns)
        if el is None:
            el = raiz.find(".//m:oMath", ns)
        _cache[clave] = el
    return copy.deepcopy(_cache[clave])


# ------------------------------------------------------------------ documento
doc = docx.Document(str(PLANTILLA))
TBL_EQ = copy.deepcopy(doc.tables[1]._tbl)
cuerpo = doc.element.body
sect_final = cuerpo[-1]
for el in list(cuerpo):
    if el is not sect_final:
        cuerpo.remove(el)

TOK = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\$.+?\$|\{c:[^}]+\}|\^\{[^}]+\})")


def runs(p, texto: str, size: float | None = None, bold: bool | None = None):
    for parte in TOK.split(texto):
        if not parte:
            continue
        if parte.startswith("$"):
            p._p.append(omml(parte[1:-1]))
            continue
        if parte.startswith("{c:"):
            parte = cita(parte[3:-1])
        parte = parte.replace("`", "")
        r_kw = {}
        if parte.startswith("**"):
            parte, r_kw = parte[2:-2], {"bold": True}
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            parte, r_kw = parte[1:-1], {"italic": True}
        sup = parte.startswith("^{")
        if sup:
            parte = parte[2:-1]
        run = p.add_run(parte)
        if r_kw.get("bold") or bold:
            run.bold = True
        if r_kw.get("italic"):
            run.italic = True
        if sup:
            run.font.superscript = True
        if size:
            run.font.size = Pt(size)
    return p


def par(texto: str, estilo: str = "Normal", align=None, size: float | None = None, bold=None):
    LOG.append((estilo, texto))
    p = doc.add_paragraph(style=estilo)
    runs(p, texto, size, bold)
    if estilo.startswith("Heading") or estilo == "Subtitulos":
        p.paragraph_format.keep_with_next = True
    if align is not None:
        p.alignment = align
    return p


def sin_num(p):
    pPr = p._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl"); ilvl.set(qn("w:val"), "0")
    nid = OxmlElement("w:numId"); nid.set(qn("w:val"), "0")
    numPr.append(ilvl); numPr.append(nid); pPr.append(numPr)
    return p


def H1(t): return par(t, "Heading 1")
def H2(t): return par(t, "Heading 2")
def H3(t): return sin_num(par(t, "Heading 3"))
def T(t): return par(t, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)


EQ_N = [0]
EQ_MAP: dict[str, int] = {}


def ecuacion(clave: str, latex: str) -> None:
    EQ_N[0] += 1
    EQ_MAP[clave] = EQ_N[0]
    tbl = copy.deepcopy(TBL_EQ)
    doc.element.body.insert(doc.element.body.index(sect_final), tbl)
    t = docx.table.Table(tbl, doc)
    c0, c1 = t.rows[0].cells
    for c in (c0, c1):
        for extra in c.paragraphs[1:]:
            extra._p.getparent().remove(extra._p)
        for r in list(c.paragraphs[0]._p):
            if r.tag != qn("w:pPr"):
                c.paragraphs[0]._p.remove(r)
    c0.paragraphs[0]._p.append(omml(latex, display=True))
    c1.paragraphs[0].add_run(f"({EQ_N[0]})")
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT


def e(clave: str) -> str:
    return f"({EQ_MAP[clave]})"


def borde_tabla(tbl) -> None:
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "bottom"):
        x = OxmlElement(f"w:{lado}")
        x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "8"); x.set(qn("w:color"), "000000")
        b.append(x)
    ih = OxmlElement("w:insideH")
    ih.set(qn("w:val"), "single"); ih.set(qn("w:sz"), "2"); ih.set(qn("w:color"), "BBBBBB")
    b.append(ih)
    tblPr.append(b)


def tabla(titulo: str, cab: list[str], filas: list[list[str]], fuente: str, anchos: list[float]) -> None:
    par(titulo, "Tabla Título", WD_ALIGN_PARAGRAPH.CENTER).paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(cab))
    t.alignment = 1
    t.autofit = False
    borde_tabla(t)
    for i, c in enumerate(cab):
        cel = t.rows[0].cells[i]
        cel.paragraphs[0].text = ""
        runs(cel.paragraphs[0], c, 8, True)
    for fila in filas:
        cs = t.add_row().cells
        for i, v in enumerate(fila):
            runs(cs[i].paragraphs[0], v, 8)
    for row in t.rows:
        for i, w in enumerate(anchos):
            row.cells[i].width = Cm(w)
            for p in row.cells[i].paragraphs:
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
    for row in t.rows:
        for c in row.cells:
            for pp in c.paragraphs:
                pp.paragraph_format.keep_with_next = True
    par(fuente, "Tabla Título", WD_ALIGN_PARAGRAPH.CENTER)


def figura(archivos: list[str], ancho: float, pie: str) -> None:
    if len(archivos) == 1:
        p = doc.add_paragraph(style="Normal"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(FIG / archivos[0]), width=Cm(ancho))
        p.paragraph_format.keep_with_next = True
    else:
        t = doc.add_table(rows=1, cols=len(archivos)); t.alignment = 1
        for i, a in enumerate(archivos):
            pc = t.rows[0].cells[i].paragraphs[0]; pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pc.add_run().add_picture(str(FIG / a), width=Cm(ancho))
            pc.paragraph_format.keep_with_next = True
    par(pie, "Figura Título", WD_ALIGN_PARAGRAPH.CENTER)




# ================================================================== utilidades de encabezado, declaraciones y cierre
import sys as _sys


def m(x) -> str:
    return f"{int(round(x)):,}".replace(",", ".")


EQUIPO = {  # clave: (nombre en el artículo, correo, ID)
    "Vitola": ("Antolin De Jesús Vitola-Montes", "antolin.vitola@upb.edu.co", "000523062"),
    "Petro": ("Isaías José Petro-Rodríguez", "isaias.petro@upb.edu.co", "000522944"),
    "Negrete": ("Andrés Julián Negrete-Pacheco", "andresj.negretep@upb.edu.co", "000506474"),
    "Carrascal": ("Juliana Esther Carrascal-Hernández", "juliana.carrascal@upb.edu.co", "000518109"),
    "Quintana": ("Angel Quintana-Jiménez", "angel.quintana@upb.edu.co", "000454040"),
    "Pemberty": ("Alejandro Pemberty-Vergara", "alejandro.pemberty@upb.edu.co", "000362954"),
    "Guerra": ("Juan Diego Guerra-Gómez", "juan.guerra@upb.edu.co", "000520912"),
}
DOCENTE = ("M.Sc. Cristian Javier Cano Mogollón", "cristian.cano@upb.edu.co")
DANE_REF = ("DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” "
            "Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/"
            "Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.")


def encabezado(primero: str, titulo_es: str, titulo_en: str, res_es: str, res_en: str, kw_es: str, kw_en: str, corresp_clave: str | None = None):
    orden = [primero] + [k for k in EQUIPO if k != primero]
    autores = [EQUIPO[k] for k in orden]
    corresp = EQUIPO[corresp_clave][0] if corresp_clave else autores[0][0]
    par(titulo_es, "Título art"); par(titulo_en, "Título art")
    doc.add_paragraph(style="Normal")
    nombres = ", ".join(f"{n}^{{{i + 1}}}" + ("^{*}" if n == corresp else "") for i, (n, _, _) in enumerate(autores))
    par(nombres + f", Cristian Javier Cano-Mogollón^{{{len(autores) + 1}}}", "Nombre autores")
    doc.add_paragraph(style="Normal")
    v = list(EQUIPO).index(primero)
    plantillas = [
        "Autor {i}: {n} - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: {m}",
        "{n}. Universidad Pontificia Bolivariana, Seccional Montería (Córdoba, Colombia). Correo: {m}. ORCID: pendiente.",
        "Autor {i} — {n} — {m} — UPB Seccional Montería, Córdoba, Colombia — ORCID: pendiente",
        "{n} (autor {i}), Universidad Pontificia Bolivariana, Seccional Montería, Colombia; correo electrónico {m}; ORCID pendiente.",
        "Afiliación del autor {i}: Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. {n}, {m}. ORCID: pendiente.",
        "{i}. {n}, Universidad Pontificia Bolivariana (Seccional Montería, Colombia). Contacto: {m}. ORCID: pendiente.",
        "Autor {i}: {n}. Filiación: Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. {m}. ORCID: pendiente.",
    ]
    docentes = [
        "Co-Autor / Co-Investigador: {d}. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: {c}",
        "Co-Autor / Co-Investigador: {d}, Docente Titular de la Facultad de Ingeniería Industrial; SILOGE (Grupo de Investigación en Simulación, Logística y Gestión de Operaciones) y HIS (Hub Industrial Solution), UPB Seccional Montería, Colombia. {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d} ({c}; ORCID pendiente). Filiación: Hub Industrial Solution (HIS) y grupo SILOGE, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia; Docente Titular.",
        "Co-Autor / Co-Investigador: {d}. Docente Titular, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia, y miembro del Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE) y del Hub Industrial Solution (HIS). Correo: {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d} — Filiación: Facultad de Ingeniería Industrial (Docente Titular), Grupo SILOGE de Simulación, Logística y Gestión de Operaciones, Hub Industrial Solution (HIS); UPB Seccional Montería, Colombia — {c} — ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d}, UPB Seccional Montería, Colombia. Docente Titular de la Facultad de Ingeniería Industrial; Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE); Hub Industrial Solution (HIS). Correo electrónico: {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d}. Filiación: Hub Industrial Solution (HIS); Grupo de Investigación SILOGE (Simulación, Logística y Gestión de Operaciones); Docente Titular, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia. Contacto: {c}. ORCID: pendiente.",
    ]
    for i, (n, mail, _) in enumerate(autores, 1):
        par("^{" + str(i) + "} " + plantillas[v].format(i=i, n=n, m=mail), "Normal", size=8)
    par("^{" + str(len(autores) + 1) + "} " + docentes[v].format(d=DOCENTE[0], c=DOCENTE[1]), "Normal", size=8)
    par(f"^{{*}} Autor de correspondencia: {corresp} ({dict((x[0], x[1]) for x in autores)[corresp]}).", "Normal", size=8)
    doc.add_paragraph(style="Normal")
    par("Resumen:", "Subtitulos"); par(res_es, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    par("Palabras clave:", "Subtitulos"); par(kw_es, "Normal")
    par("Abstract:", "Subtitulos"); par(res_en, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    par("Keywords:", "Subtitulos"); par(kw_en, "Normal")
    return autores


def resto(frase_intro: str) -> None:
    """Cita, en una frase, las referencias aún no usadas (cada artículo debe citar las 21 fuentes del equipo)."""
    faltan = [k for k in list(CLAVES) + ["dane"] if k not in ORDEN]
    if faltan:
        T(frase_intro + " {c:" + ",".join(faltan) + "}.")


def declaraciones(d: dict) -> None:
    sin_num(par("Contribución de los autores", "Heading 2")); T(d["cred"])
    sin_num(par("Declaraciones finales", "Heading 2"))
    H3("Financiación"); T(d["fin"])
    H3("Conflicto de intereses"); T(d["conf"])
    H3("Consentimiento informado"); T(d["cons"])
    H3("Declaración de la Junta de Revisión Institucional"); T(d["irb"])
    H3("Disponibilidad de datos, código y materiales de investigación"); T(d["datos"])
    H3("Uso de herramientas de inteligencia artificial"); T(d["ia"])
    par("Declarations (English)", "Subtitulos"); T(d["en"])


def cierre(autores, titulo_es: str, titulo_corto: str, salida: Path, esperadas: int = 21):
    sin_num(par("References", "Heading 1"))
    import re as _re

    def limpio(t):
        t = _re.sub(r"\{c:([^}]+)\}", lambda mm: cita(mm.group(1)), t)
        t = t.replace("{E_ACEPT}", e("acepta") if "acepta" in EQ_MAP else "")
        for k, v in EQ_MAP.items():
            t = t.replace("{E_" + k.upper() + "}", f"({v})")
        return t
    for p in doc.paragraphs:
        for r in p.runs:
            if "{E_" in r.text:
                r.text = limpio(r.text)
    ORDEN_FIN = list(ORDEN)
    for i, k in enumerate(ORDEN_FIN, 1):
        par(f"[{i}] " + (DANE_REF if k == "dane" else ref_ieee(k)), "Normal", size=8)

    def reemplazar(parte, viejo, nuevo):
        for t in parte._element.iter(qn("w:t")):
            if viejo in (t.text or ""):
                t.text = t.text.replace(viejo, nuevo)
    sec = doc.sections[0]
    reemplazar(sec.header, "Apellido, A. Apellido", autores[0][0].split("-")[0].split()[-1] + " et al.")
    reemplazar(sec.even_page_header, "Título del artículo", titulo_corto)
    reemplazar(sec.first_page_footer, "Autores (A. Apellido).,", ", ".join(cita_autor(a[0].replace("-", " ")) for a in autores) + " y C. J. Cano-Mogollón,")
    reemplazar(sec.first_page_footer, "Título en el idioma en que se presenta el artículo,", titulo_es + ",")
    # texto plano para el ESCRITO FINAL
    visto = []
    for est, t in LOG:
        t = _re.sub(r"\{c:([^}]+)\}", lambda mm: cita(mm.group(1)), t)
        for k, v in EQ_MAP.items():
            t = t.replace("{E_" + k.upper() + "}", f"({v})")
        t = t.replace("{E_ACEPT}", e("acepta") if "acepta" in EQ_MAP else "")
        for lat, uni in (("\\alpha", "α"), ("\\approx", "≈"), ("\\mathcal{M}", "M"), ("\\bar\\mu", "μ"), ("\\", ""), ("$", ""), ("{,}", ","), ("_{", "_"), ("^{", "^")):
            t = t.replace(lat, uni)
        visto.append((est, t))
    salida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(salida))
    salida.with_suffix(".txt").write_text("\n\n".join(f"[{a}] {b}" for a, b in visto), encoding="utf-8")
    print("guardado", salida.name, "| refs:", len(ORDEN_FIN), "| ecuaciones:", EQ_N[0])
    assert len(ORDEN_FIN) == esperadas, [k for k in list(CLAVES) + ["dane"] if k not in ORDEN_FIN]


def bloque(nombre: str) -> None:
    """Ejecuta un bloque de la redacción técnica original del equipo (extraído de construir_articulo.py)."""
    import json as _json
    exec(compile(_json.loads((AQUI / "bloques.json").read_text(encoding="utf-8"))[nombre], f"<bloque {nombre}>", "exec"), globals())


def cita_autor(nombre: str) -> str:
    partes = nombre.split()
    return " ".join(x[0] + "." for x in partes[:-1]) + " " + partes[-1]
