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
PLANTILLA = AQUI.parent / "8.clorificadordeAgua (2)" / "8.clorificadordeAgua" / "entrega_corte3" / "revista" / "plantilla_UIS.docx"
FIG = AQUI / "fig"
R = json.loads((AQUI / "resultados_estudio.json").read_text(encoding="utf-8"))
C = json.loads((AQUI / "resultados_complemento.json").read_text(encoding="utf-8"))
PR = json.loads((AQUI / "prisma_cifras.json").read_text(encoding="utf-8"))
REFS = {r["doi"]: r for r in json.loads((AQUI / "refs_crossref.json").read_text(encoding="utf-8")) if r["estado"] == "VERIFICADO"}
LOG = []   # texto plano del artículo (para el ESCRITO FINAL)
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def f(x: float, d: int = 1) -> str:
    return f"{x:.{d}f}".replace(".", ",")


# ------------------------------------------------------------------ referencias
CLAVES = {
    "uganda": "10.3362/1756-3488.20-00014", "nepal": "10.1021/acs.est.2c03133", "venturi": "10.1038/s41545-020-00091-1",
    "dhaka": "10.1021/acs.est.1c01308", "mercado": "10.1021/acs.estlett.2c00781", "aquatabs": "10.1061/(asce)ee.1943-7870.0001883",
    "ghana": "10.1371/journal.pwat.0000295", "usvi": "10.1061/(asce)ee.1943-7870.0002063", "honduras": "10.1021/acsestwater.3c00425",
    "kmu": "10.2166/washdev.2024.407", "guatemala": "10.1371/journal.pwat.0000255", "odisha": "10.1371/journal.pwat.0000440",
    "etiopia": "10.1371/journal.pwat.0000575", "amrose": "10.1146/annurev-environ-031411-091819", "arnold": "10.4269/ajtmh.2007.76.354",
    "wolf": "10.1016/S0140-6736(23)00458-0", "clasen": "10.1002/14651858.CD004794.pub3", "powell": "10.1016/S0043-1354(99)00097-4",
    "wilson": "10.1080/01621459.1927.10502953", "pickering": "10.1016/S2214-109X(19)30315-8", "prisma": "10.1136/bmj.n71",
}
NORMAS = {
    "res2115": "Ministerio de la Protección Social y Ministerio de Ambiente, Vivienda y Desarrollo Territorial, “Resolución 2115 de 2007, por "
               "medio de la cual se señalan características, instrumentos básicos y frecuencias del sistema de control y vigilancia para la calidad "
               "del agua para consumo humano,” Bogotá, Colombia, 2007. [Online]. Available: https://normograma.invima.gov.co/normograma/"
               "compilacion/docs/resolucion_minproteccion_2115_2007.htm. Accessed: Nov. 6, 2026.",
    "oms": "World Health Organization, Guidelines for Drinking-water Quality: Fourth Edition Incorporating the First and Second Addenda. Geneva, "
           "Switzerland: WHO, 2022. [Online]. Available: https://www.who.int/publications/i/item/9789240045064. Accessed: Nov. 6, 2026.",
}
ORDEN: list[str] = []


def num(clave: str) -> int:
    assert clave in CLAVES or clave in NORMAS, clave
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
    if clave in NORMAS:
        return NORMAS[clave]
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




# ================================================================== utilidades de cierre y encabezado
def m(x) -> str:
    """Entero con punto de miles."""
    return f"{int(round(x)):,}".replace(",", ".")


AUTORES_ALL = {
    "Muñoz": ("Roxana Elena Muñoz-Rodiño", "roxana.munoz@upb.edu.co", "000525435"),
    "Alvarez": ("Camilo Esteban Alvarez-Durán", "camilo.alvarezd@upb.edu.co", "000503488"),
    "Guzmán": ("Andrea Guzmán-Gómez", "andrea.guzmang@upb.edu.co", "000511622"),
}
DOCENTE = ("M.Sc. Cristian Javier Cano Mogollón", "cristian.cano@upb.edu.co")


def cita_autor(nombre: str) -> str:
    partes = nombre.split()
    return " ".join(x[0] + "." for x in partes[:-1]) + " " + partes[-1]


def encabezado(primero: str, titulo_es: str, titulo_en: str, res_es: str, res_en: str, kw_es: str, kw_en: str):
    orden = [primero] + [k for k in AUTORES_ALL if k != primero]
    autores = [AUTORES_ALL[k] for k in orden]
    corresp = autores[0][0]
    par(titulo_es, "Título art"); par(titulo_en, "Título art")
    doc.add_paragraph(style="Normal")
    nombres = ", ".join(f"{n}^{{{i + 1}}}" + ("^{*}" if n == corresp else "") for i, (n, _, _) in enumerate(autores))
    par(nombres + f", Cristian Javier Cano-Mogollón^{{{len(autores) + 1}}}", "Nombre autores")
    doc.add_paragraph(style="Normal")
    for i, (n, mail, _) in enumerate(autores, 1):
        par(f"^{{{i}}} Autor {i}: {n} - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. "
            f"ORCID: pendiente. Correo electrónico: {mail}", "Normal", size=8)
    par(f"^{{{len(autores) + 1}}} Co-Autor / Co-Investigador: {DOCENTE[0]}. Filiación: Docente Titular, Facultad de Ingeniería "
        "Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), "
        f"Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: {DOCENTE[1]}", "Normal", size=8)
    par(f"^{{*}} Autor de correspondencia: {corresp} ({autores[0][1]}).", "Normal", size=8)
    doc.add_paragraph(style="Normal")
    par("Resumen:", "Subtitulos"); par(res_es, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    par("Palabras clave:", "Subtitulos"); par(kw_es, "Normal")
    par("Abstract:", "Subtitulos"); par(res_en, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    par("Keywords:", "Subtitulos"); par(kw_en, "Normal")
    return autores


def declaraciones(extra_datos: str = ""):
    sin_num(par("Contribución de los autores", "Heading 2"))
    T("Contribución de los autores (taxonomía CRediT; por confirmar por el equipo antes del envío): los estudiantes autores participaron en "
      "conceptualización, metodología, investigación, análisis formal y redacción del borrador original; Cristian Javier Cano-Mogollón "
      "realizó la supervisión y la revisión y edición del manuscrito. Los autores leyeron y aprobaron la versión final.")
    sin_num(par("Declaraciones finales", "Heading 2"))
    H3("Financiación")
    T("Según el presupuesto del proyecto, los insumos de laboratorio previstos (160.000 COP) están a cargo del semillero SILOGE de la UPB. "
      "[Por confirmar por el equipo.]")
    H3("Conflicto de intereses")
    T("Los autores declaran que no existen conflictos de intereses relacionados con la presente publicación. [Por confirmar por el equipo.]")
    H3("Consentimiento informado")
    T("No aplica. No se recolectaron datos de personas; el estudio es un análisis de diseño, modelación y simulación.")
    H3("Declaración de la Junta de Revisión Institucional")
    T("No aplica, dado que no hubo participantes humanos. La encuesta comunitaria prevista en el proyecto requerirá consentimiento informado.")
    H3("Disponibilidad de datos, código y materiales de investigación")
    T("Los scripts de simulación, la búsqueda bibliográfica, la verificación de referencias y las salidas numéricas están en la carpeta "
      "de evidencia compartida del proyecto (estudio_clorificador.py, complemento.py, busqueda_prisma.py, resultados_estudio.json, "
      "prisma_cifras.json, verificacion_referencias.csv). El repositorio público está por definir. " + extra_datos)
    H3("Uso de herramientas de inteligencia artificial")
    T("Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para ejecutar y documentar los análisis, verificar las "
      "referencias y redactar borradores. Los autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.")
    par("Author Contributions", "Subtitulos")
    T("CRediT roles (to be confirmed by the team before submission): the student authors contributed to conceptualization, methodology, "
      "investigation, formal analysis and writing of the original draft; C. J. Cano-Mogollón contributed supervision and review and editing.")
    par("Funding and Acknowledgments", "Subtitulos"); T("Laboratory supplies are budgeted by the SILOGE research seed group. [To be confirmed by the team.]")
    par("Conflicts of Interest", "Subtitulos"); T("The authors declare that there is no conflict of interests. [To be confirmed by the team.]")
    par("Informed Consent Statement", "Subtitulos"); T("Not applicable.")
    par("Institutional Review Board Statement", "Subtitulos"); T("Not applicable.")
    par("Data, Code, and Research Materials Availability", "Subtitulos")
    T("Simulation scripts, search logs, reference verification and numerical outputs are in the shared evidence folder of the project.")


def cierre(autores, titulo_es: str, titulo_corto: str, salida: Path, esperadas: int = 23):
    sin_num(par("References", "Heading 1"))
    for p in doc.paragraphs:
        for r in p.runs:
            for k, v in EQ_MAP.items():
                if "{E_" + k.upper() + "}" in r.text:
                    r.text = r.text.replace("{E_" + k.upper() + "}", f"({v})")
    ORDEN_FIN = list(ORDEN)
    for i, k in enumerate(ORDEN_FIN, 1):
        par(f"[{i}] {ref_ieee(k)}", "Normal", size=8)

    def reemplazar(parte, viejo, nuevo):
        for t in parte._element.iter(qn("w:t")):
            if viejo in (t.text or ""):
                t.text = t.text.replace(viejo, nuevo)
    sec = doc.sections[0]
    reemplazar(sec.header, "Apellido, A. Apellido", autores[0][0].split("-")[0].split()[-1] + " et al.")
    reemplazar(sec.even_page_header, "Título del artículo", titulo_corto)
    reemplazar(sec.first_page_footer, "Autores (A. Apellido).,", ", ".join(cita_autor(a[0]) for a in autores) + " y C. J. Cano-Mogollón,")
    reemplazar(sec.first_page_footer, "Título en el idioma en que se presenta el artículo,", titulo_es + ",")
    salida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(salida))
    print("guardado", salida, "| refs citadas:", len(ORDEN_FIN), "(esperadas", esperadas, ") | ecuaciones:", EQ_N[0])
    assert len(ORDEN_FIN) == esperadas, ORDEN_FIN
