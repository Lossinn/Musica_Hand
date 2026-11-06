"""Constructor del «escrito final» con formato de artículo de proyecto (dos columnas, carta, serif), inspirado en el ejemplo CVRP.
API: Escrito(...).titulo_bloque(...), .sec(), .sub(), .P(), .B(), .eq(), .tabla(), .figura(), .guardar().
Etiquetas en el texto: {cite:a,b} (parentético), {citet:a} (narrativo), {tab:k}, {fig:k}, {eq:k}; **negrita**, *cursiva*, $latex$.
El contenido se ejecuta dos veces (primera pasada: numeración; segunda: documento)."""
from __future__ import annotations

import copy, json, re, tempfile, zipfile
from pathlib import Path

import docx
import pypandoc
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu
from lxml import etree

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
FIG = BASE / "articulo" / "fig"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
AZUL = RGBColor(0x1F, 0x38, 0x64)
FUENTE = "Times New Roman"

# ---------------------------------------------------------------- referencias (autor-año)
REFS = {r["doi"]: r for r in json.loads((BASE / "analisis" / "refs_crossref.json").read_text(encoding="utf-8"))}
CLAVES = {
    "yi": "10.1007/s10462-023-10637-7", "mediapipe": "10.48550/arXiv.2006.10214", "li_hong": "10.1007/s40745-026-00689-1",
    "li_peerj": "10.7717/peerj-cs.3464", "li_disc": "10.1007/s44163-026-01115-4", "deng_sci": "10.1038/s41598-026-53749-0",
    "shi": "10.1007/s44163-026-01858-0", "deng_piano": "10.5216/mh.v26.85176", "chulu": "10.1007/s11042-026-21667-y",
    "tang": "10.1007/s10791-026-10022-2", "wang": "10.1007/s44163-026-00832-0", "ramoneda": "10.1016/j.eswa.2026.132088",
    "apay": "10.31681/jetol.1243501", "barroso": "10.6018/red.602301", "leon": "10.17811/rifie.20620",
    "cepeda": "10.1037/0033-2909.132.3.354", "corbett": "10.1007/BF01099821", "wilson85": "10.1038/s41467-019-12552-4",
    "wilsonci": "10.1080/01621459.1927.10502953", "wozniak": "10.55782/ane-1994-1003",
}
DANE = ("DANE (2026). Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026). Bogotá, Colombia. "
        "Disponible en https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx (consultado el 5 de noviembre de 2026).")
CURWEN = None


def _limpiar(t: str) -> str:
    import html
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def _ap(nombre: str) -> str:
    return nombre.title() if nombre.isupper() else nombre


def _inic(nombre: str) -> str:
    return " ".join(p[0] + "." for p in re.split(r"[ \-]+", nombre.strip()) if p)


def _autores(r):
    out = []
    for a in r["autores"].split("; "):
        ap, _, nom = a.partition(", ")
        out.append((_ap(ap), _inic(nom)))
    return out


def cita_corta(clave: str, narrativa: bool = False) -> str:
    if clave == "dane":
        return "DANE (2026)" if narrativa else "DANE, 2026"
    r = REFS[CLAVES[clave]]; a = _autores(r); y = r["anio"]
    if len(a) == 1:
        n = a[0][0]
    elif len(a) == 2:
        n = f"{a[0][0]} y {a[1][0]}"
    else:
        n = f"{a[0][0]} et al."
    return f"{n} ({y})" if narrativa else f"{n}, {y}"


def ref_larga(clave: str) -> str:
    if clave == "dane":
        return DANE
    r = REFS[CLAVES[clave]]; a = _autores(r)
    fa = [f"{ap}, {ini}" for ap, ini in a]
    if len(fa) == 1:
        au = fa[0]
    elif len(fa) <= 6:
        au = ", ".join(fa[:-1]) + ", y " + fa[-1]
    else:
        au = ", ".join(fa[:6]) + ", et al."
    t = _limpiar(r["titulo"]).rstrip(".")
    rev = _limpiar(r["revista"])
    if rev == "arXiv":
        return f"{au} ({r['anio']}). {t}. *arXiv:2006.10214*. https://doi.org/{r['doi']}"
    s = f"{au} ({r['anio']}). {t}. *{rev}*"
    if r["volumen"]:
        s += f", {r['volumen']}"
        if r["numero"]:
            s += f"({r['numero']})"
    if r["paginas"]:
        s += f":{r['paginas']}"
    return s + f". https://doi.org/{r['doi']}"


def _orden_alfa(clave: str) -> str:
    if clave == "dane":
        return "dane"
    return _autores(REFS[CLAVES[clave]])[0][0].lower()


# ---------------------------------------------------------------- OMML
_cache: dict = {}


def omml(latex: str, display: bool = False):
    k = (latex, display)
    if k not in _cache:
        md = f"$${latex}$$" if display else f"${latex}$"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "m.docx"
            pypandoc.convert_text(md, "docx", format="markdown", outputfile=str(out))
            xml = zipfile.ZipFile(out).read("word/document.xml")
        raiz = etree.fromstring(xml); ns = {"m": M_NS}
        el = raiz.find(".//m:oMathPara", ns) if display else raiz.find(".//m:oMath", ns)
        if el is None:
            el = raiz.find(".//m:oMath", ns)
        _cache[k] = el
    return copy.deepcopy(_cache[k])


def _fuente(run, size=None, bold=None, italic=None, color=None):
    run.font.name = FUENTE
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FUENTE)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color


class Escrito:
    TOK = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|\$[^$]+\$|\{(?:cite|citet|tab|fig|eq|sec):[^}]+\})")

    def __init__(self, etiquetas=None, plantilla_pasada=False):
        self.d = docx.Document()
        self.etiq = etiquetas or {}
        self.nuevas: dict[str, str] = {}
        self.n_sec = 0; self.n_sub = 0; self.n_tab = 0; self.n_fig = 0; self.n_eq = 0
        self.citadas: list[str] = []
        self._config()

    # ---- configuración de página, estilos, encabezado y pie
    def _config(self):
        d = self.d
        st = d.styles["Normal"]; st.font.name = FUENTE; st.font.size = Pt(10)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
        pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(0); pf.line_spacing = 1.12
        s = d.sections[0]
        s.page_width = Cm(21.59); s.page_height = Cm(27.94)
        s.left_margin = s.right_margin = Cm(1.9); s.top_margin = Cm(2.4); s.bottom_margin = Cm(2.2)
        s.header_distance = Cm(1.1); s.footer_distance = Cm(1.1)
        # encabezado: texto izquierda y derecha con línea inferior
        h = s.header; h.is_linked_to_previous = False
        p = h.paragraphs[0]; p.text = ""; p.style = d.styles["Normal"]
        ancho = s.page_width - s.left_margin - s.right_margin
        p.paragraph_format.tab_stops.add_tab_stop(ancho, WD_TAB_ALIGNMENT.RIGHT)
        r = p.add_run("Gestión Tecnológica"); _fuente(r, 9)
        r = p.add_run("\tUPB - Montería"); _fuente(r, 9)
        pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        for k, v in (("val", "single"), ("sz", "4"), ("space", "3"), ("color", "000000")):
            bt.set(qn(f"w:{k}"), v)
        b.append(bt); pPr.append(b)
        # pie: número de página centrado
        f = s.footer; f.is_linked_to_previous = False
        p = f.paragraphs[0]; p.style = d.styles["Normal"]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.text = ""
        r = p.add_run(); _fuente(r, 9)
        for tipo, txt in (("begin", None), (None, " PAGE "), ("end", None)):
            if tipo:
                e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tipo); r._r.append(e)
            else:
                e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r._r.append(e)

    # ---- columnas
    def _cols(self, sec, n, espacio_cm=0.76):
        sp = sec._sectPr
        c = sp.find(qn("w:cols"))
        if c is None:
            c = OxmlElement("w:cols"); sp.append(c)
        c.set(qn("w:num"), str(n)); c.set(qn("w:space"), str(int(espacio_cm * 567)))

    def dos_columnas(self):
        sec = self.d.add_section(WD_SECTION.CONTINUOUS)
        self._cols(sec, 2)

    def una_columna(self):
        sec = self.d.add_section(WD_SECTION.CONTINUOUS)
        self._cols(sec, 1)

    # ---- texto con marcas
    def _texto(self, p, texto, size=10, bold=None, italic=None, color=None):
        for parte in self.TOK.split(texto):
            if not parte:
                continue
            if parte.startswith("$"):
                p._p.append(omml(parte[1:-1])); continue
            m = re.match(r"\{(cite|citet|tab|fig|eq|sec):([^}]+)\}", parte)
            if m:
                tipo, arg = m.groups()
                if tipo in ("cite", "citet"):
                    claves = [c.strip() for c in arg.split(",")]
                    for c in claves:
                        if c not in self.citadas:
                            self.citadas.append(c)
                    if tipo == "citet":
                        s = "; ".join(cita_corta(c, True) for c in claves)
                    else:
                        s = "(" + "; ".join(cita_corta(c) for c in claves) + ")"
                else:
                    s = self.etiq.get(f"{tipo}:{arg.strip()}", "?")
                r = p.add_run(s); _fuente(r, size, bold, italic, color); continue
            if parte.startswith("**") and parte.endswith("**"):
                r = p.add_run(parte[2:-2]); _fuente(r, size, True, italic, color)
            elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
                r = p.add_run(parte[1:-1]); _fuente(r, size, bold, True, color)
            else:
                r = p.add_run(parte); _fuente(r, size, bold, italic, color)
        return p

    # ---- bloque de título (una columna)
    def titulo_bloque(self, titulo, autores, docente_lineas, resumen, kw_es, abstract, kw_en):
        d = self.d
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.0
        self._texto(p, titulo, 17, True, None, AZUL)
        for fila in autores:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._texto(p, fila, 11)
        d.add_paragraph().paragraph_format.space_after = Pt(2)
        for l in docente_lineas:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._texto(p, l, 10)
        self._regla(d.add_paragraph(), 14, 6)
        for rot, txt in (("Resumen.", resumen), ("Palabras clave:", kw_es), ("Abstract.", abstract), ("Keywords:", kw_en)):
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(5)
            r = p.add_run(rot + " "); _fuente(r, 9.5, True)
            self._texto(p, txt, 9.5)
        self._regla(d.add_paragraph(), 2, 8)
        self.dos_columnas()

    def _regla(self, p, antes, despues):
        p.paragraph_format.space_before = Pt(antes); p.paragraph_format.space_after = Pt(despues)
        p.paragraph_format.line_spacing = Pt(2)
        b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "000000")):
            bt.set(qn(f"w:{k}"), v)
        b.append(bt); p._p.get_or_add_pPr().append(b)

    # ---- secciones
    def sec(self, titulo, clave=None):
        self.n_sec += 1; self.n_sub = 0
        if clave:
            self.nuevas[f"sec:{clave}"] = str(self.n_sec)
        p = self.d.add_paragraph(); pf = p.paragraph_format
        pf.space_before = Pt(10); pf.space_after = Pt(4); pf.keep_with_next = True
        self._texto(p, f"{self.n_sec}. {titulo}", 12.5, True)

    def sub(self, titulo, clave=None):
        self.n_sub += 1
        if clave:
            self.nuevas[f"sec:{clave}"] = f"{self.n_sec}.{self.n_sub}"
        p = self.d.add_paragraph(); pf = p.paragraph_format
        pf.space_before = Pt(7); pf.space_after = Pt(3); pf.keep_with_next = True
        self._texto(p, f"{self.n_sec}.{self.n_sub} {titulo}", 10.5, True)

    def sec_sin_numero(self, titulo):
        p = self.d.add_paragraph(); pf = p.paragraph_format
        pf.space_before = Pt(12); pf.space_after = Pt(4); pf.keep_with_next = True
        self._texto(p, titulo, 12.5, True)

    def P(self, texto, sangria=True, keep=False):
        p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if sangria:
            p.paragraph_format.first_line_indent = Cm(0.5)
        p.paragraph_format.widow_control = True
        if keep:
            p.paragraph_format.keep_with_next = True
        self._texto(p, texto, 10)
        return p

    def B(self, items, size=10):
        for it in items:
            p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format; pf.left_indent = Cm(0.55); pf.first_line_indent = Cm(-0.4); pf.space_after = Pt(1.5)
            r = p.add_run("▪ "); _fuente(r, size - 2)
            self._texto(p, it, size)
        self.d.paragraphs[-1].paragraph_format.space_after = Pt(4)

    # ---- ecuaciones
    def eq(self, clave, latex):
        self.n_eq += 1
        self.nuevas[f"eq:{clave}"] = f"({self.n_eq})"
        t = self.d.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        t.allow_autofit = False
        ancho = 8.5
        for c, w in zip(t.rows[0].cells, (ancho * 0.84, ancho * 0.16)):
            c.width = Cm(w)
        c0, c1 = t.rows[0].cells
        c0.paragraphs[0]._p.append(omml(latex, display=True))
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = c1.paragraphs[0].add_run(f"({self.n_eq})"); _fuente(r, 10)
        for c in (c0, c1):
            c.paragraphs[0].paragraph_format.space_before = Pt(2); c.paragraphs[0].paragraph_format.space_after = Pt(2)
        t.rows[0].cells[0].vertical_alignment = 1
        self._sin_bordes(t)
        sp = self.d.add_paragraph(); sp.paragraph_format.line_spacing = Pt(3)

    def _sin_bordes(self, t):
        tblPr = t._tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
            x = OxmlElement(f"w:{lado}"); x.set(qn("w:val"), "nil"); b.append(x)
        tblPr.append(b)

    # ---- tablas estilo booktabs
    def tabla(self, clave, caption, cab, filas, anchos, size=8.5, alinear=None):
        self.n_tab += 1
        self.nuevas[f"tab:{clave}"] = f"Cuadro {self.n_tab}"
        p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p.paragraph_format; pf.space_before = Pt(6); pf.space_after = Pt(3); pf.keep_with_next = True
        r = p.add_run(f"Cuadro {self.n_tab}: "); _fuente(r, 9, True)
        self._texto(p, caption, 9)
        t = self.d.add_table(rows=1, cols=len(cab)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        t.allow_autofit = False
        self._sin_bordes(t)
        tot = sum(anchos); anchos = [a * 8.5 / tot for a in anchos]
        for i, c in enumerate(cab):
            cel = t.rows[0].cells[i]; cel.width = Cm(anchos[i])
            pp = cel.paragraphs[0]; pp.paragraph_format.keep_with_next = True
            if alinear and alinear[i] == "r":
                pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            self._texto(pp, c, size, True)
        for fila in filas:
            cs = t.add_row().cells
            for i, v in enumerate(fila):
                cs[i].width = Cm(anchos[i])
                pp = cs[i].paragraphs[0]
                if alinear and alinear[i] == "r":
                    pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                self._texto(pp, v, size)
        for row in t.rows:
            row.cantSplit = True
            for c in row.cells:
                for pp in c.paragraphs:
                    pp.paragraph_format.space_before = Pt(1); pp.paragraph_format.space_after = Pt(1); pp.paragraph_format.line_spacing = 1.0
        self._borde_celdas(t.rows[0], "top", 8); self._borde_celdas(t.rows[0], "bottom", 4); self._borde_celdas(t.rows[-1], "bottom", 8)
        for row in t.rows[:-1]:
            for c in row.cells:
                for pp in c.paragraphs:
                    pp.paragraph_format.keep_with_next = True
        sp = self.d.add_paragraph(); sp.paragraph_format.line_spacing = Pt(5)

    def _borde_celdas(self, row, lado, sz):
        for c in row.cells:
            tcPr = c._tc.get_or_add_tcPr(); b = tcPr.find(qn("w:tcBorders"))
            if b is None:
                b = OxmlElement("w:tcBorders"); tcPr.append(b)
            x = OxmlElement(f"w:{lado}")
            for k, v in (("val", "single"), ("sz", str(sz)), ("space", "0"), ("color", "000000")):
                x.set(qn(f"w:{k}"), v)
            b.append(x)

    # ---- figuras
    def figura(self, clave, archivo, caption, ancho_cm=8.3, ancha=False):
        self.n_fig += 1
        self.nuevas[f"fig:{clave}"] = f"Figura {self.n_fig}"
        if ancha:
            self.una_columna()
        p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6); p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(FIG / archivo), width=Cm(ancho_cm))
        c = self.d.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_before = Pt(3); c.paragraph_format.space_after = Pt(8)
        r = c.add_run(f"Figura {self.n_fig}: "); _fuente(r, 9, True)
        self._texto(c, caption, 9)
        if ancha:
            self.dos_columnas()

    # ---- referencias y cierre
    def referencias(self, extras=()):
        self.sec_sin_numero("Referencias")
        claves = sorted(set(self.citadas), key=_orden_alfa)
        for c in claves:
            p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf = p.paragraph_format; pf.left_indent = Cm(0.5); pf.first_line_indent = Cm(-0.5); pf.space_after = Pt(4)
            self._texto(p, ref_larga(c), 9)
        for e in extras:
            p = self.d.add_paragraph(); pf = p.paragraph_format; pf.left_indent = Cm(0.5); pf.first_line_indent = Cm(-0.5); pf.space_after = Pt(4)
            self._texto(p, e, 9)
        return len(claves)

    def guardar(self, ruta):
        self.d.save(str(ruta))


def construir(contenido, ruta, **kw):
    """Ejecuta `contenido(e)` dos veces para resolver referencias cruzadas y guarda el documento."""
    e1 = Escrito(); contenido(e1)
    e2 = Escrito(etiquetas=e1.nuevas); contenido(e2)
    assert e2.nuevas == e1.nuevas
    e2.guardar(ruta)
    return e2
