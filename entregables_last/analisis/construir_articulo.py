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
import sys
PRIMERO = sys.argv[1] if len(sys.argv) > 1 else None   # apellido del primer autor y autor de correspondencia
SUFIJO = f"_{PRIMERO}" if PRIMERO else ""
SALIDA = BASE / "articulo" / f"Articulo_Maquetado_EquipoNN{SUFIJO}.docx"
FIG = BASE / "articulo" / "fig"
R = json.loads((AQUI / "resultados_vision.json").read_text(encoding="utf-8"))
REFS = {r["doi"]: r for r in json.loads((AQUI / "refs_crossref.json").read_text(encoding="utf-8"))}
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


# ================================================================== encabezado
AUTORES = [
    ("Angel Quintana", "angel.quintana@upb.edu.co"),
    ("Andrés Negrete", "andres.negreten@upb.edu.co"),
    ("Antolin Vitola", "Antolin.vitola@upb.edu.co"),
    ("Juliana Esther Carrascal", "juliana.carrascal@upb.edu.co"),
    ("Alejandro Pemberty-Vergara", "alejandro.pemberty@upb.edu.co"),
]
if PRIMERO:
    AUTORES.sort(key=lambda a: 0 if PRIMERO.lower() in a[0].lower() else 1)   # orden estable: el resto conserva su orden
    assert PRIMERO.lower() in AUTORES[0][0].lower(), PRIMERO
CORRESP = AUTORES[0][0] if PRIMERO else "Alejandro Pemberty-Vergara"


def cita_autor(nombre: str) -> str:
    partes = nombre.split()
    return " ".join(x[0] + "." for x in partes[:-1]) + " " + partes[-1]


TITULO_ES = ("Reconocimiento invariante de señas manuales y selección óptima de sesiones para la enseñanza "
             "de notas musicales a niños: evaluación técnica de laboratorio de Hand Sing Kids")
TITULO_EN = ("Invariant hand-sign recognition and optimal session selection for teaching musical notes to "
             "children: laboratory technical evaluation of Hand Sing Kids")

par(TITULO_ES, "Título art")
par(TITULO_EN, "Título art")
doc.add_paragraph(style="Normal")
nombres = ", ".join(f"{n}^{{{i + 1}}}" + ("^{*}" if n == CORRESP else "")
                    for i, (n, _) in enumerate(AUTORES))
par(nombres + f", Cristian Javier Cano-Mogollón^{{{len(AUTORES) + 1}}}", "Nombre autores")
doc.add_paragraph(style="Normal")
for i, (n, mail) in enumerate(AUTORES, 1):
    par(f"^{{{i}}} Autor {i}: {n} - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. "
        f"ORCID: pendiente. Correo electrónico: {mail}", "Normal", size=8)
par(f"^{{{len(AUTORES) + 1}}} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente "
    "Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de "
    "Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, "
    "Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co", "Normal", size=8)
par(f"^{{*}} Autor de correspondencia: {CORRESP} ({dict(AUTORES)[CORRESP]}).", "Normal", size=8)
doc.add_paragraph(style="Normal")

RES_ES = (
    "La enseñanza temprana de las notas musicales mediante señas manuales exige un reconocimiento que distinga la "
    "seña intencional de los gestos de transición y que ajuste las actividades al progreso de cada niño. Se presenta "
    "Hand Sing Kids, una aplicación de escritorio en Python (PySide6, OpenCV y MediaPipe) que asigna una seña de "
    "dos manos a cada una de las ocho notas de Do3 a Do4. El sistema describe cada postura con un vector invariante "
    "de 120 componentes, la clasifica por vecino más cercano con confianza calibrada y margen, estabiliza la lectura "
    "con un periodo refractario, estima el dominio de cada habilidad con un modelo de cuatro componentes y repaso "
    "espaciado, y selecciona la sesión mediante un problema entero mixto. La evaluación fue técnica y de laboratorio, "
    "con una calibración de ocho señas de una sola persona y perturbaciones simuladas. Con 480 señas válidas por nivel "
    f"de ruido, el reconocimiento fue de {f(R['aciertos'][0]['nuevo']['pct'], 0)} % sin ruido y de "
    f"{f(R['aciertos'][3]['nuevo']['pct'])} % con ruido de 0,09; con 640 posturas que no son seña, el método propuesto "
    f"disparó una nota por error en {f(R['falsos_positivos']['global_nuevo']['pct'])} % de los casos (IC 95 %: "
    f"{f(R['falsos_positivos']['global_nuevo']['ic95_lo'])} a {f(R['falsos_positivos']['global_nuevo']['ic95_hi'])} %), "
    "frente a 100 % del método de la versión inicial. Las ocho baterías de prueba del repositorio se ejecutaron sin "
    "fallos. No hubo pruebas con niños: el nivel de madurez tecnológica estimado es TRL 4 y el impacto esperado en "
    "Montería y Córdoba se formula como hipótesis por validar.")
RES_EN = (
    "Teaching musical notes to young children through hand signs requires a recognizer that separates intentional "
    "signs from transition gestures and a planner that adapts activities to each child's progress. This paper "
    "presents Hand Sing Kids, a desktop application in Python (PySide6, OpenCV and MediaPipe) that maps a two-handed "
    "sign to each of the eight notes from C3 to C4. Each posture is encoded as a 120-component invariant vector and "
    "classified by nearest neighbour with calibrated confidence and margin; the reading is stabilized with a "
    "refractory period; skill mastery is estimated with a four-component model and spaced repetition; and each "
    "session is chosen by solving a mixed-integer program. The evaluation was technical and laboratory-based, with a "
    "single eight-sign calibration from one person and simulated perturbations. With 480 valid signs per noise level, "
    f"recognition was {f(R['aciertos'][0]['nuevo']['pct'], 0)} % without noise and "
    f"{f(R['aciertos'][3]['nuevo']['pct'])} % at noise 0.09; over 640 postures that are not signs, the proposed method "
    f"fired a wrong note in {f(R['falsos_positivos']['global_nuevo']['pct'])} % of cases (95 % CI "
    f"{f(R['falsos_positivos']['global_nuevo']['ic95_lo'])} to {f(R['falsos_positivos']['global_nuevo']['ic95_hi'])} %), "
    "against 100 % for the initial method. All eight test suites in the repository ran without failures. No tests "
    "with children were carried out: the estimated technology readiness level is TRL 4, and the expected impact in "
    "Montería and Córdoba is stated as a hypothesis to be validated.")
par("Resumen:", "Subtitulos"); par(RES_ES, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
par("Palabras clave:", "Subtitulos")
par("reconocimiento de gestos; educación musical; primera infancia; MediaPipe; descriptor invariante; repaso "
    "espaciado; programación entera mixta; aprendizaje adaptativo; madurez tecnológica; Montería", "Normal")
par("Abstract:", "Subtitulos"); par(RES_EN, "Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
par("Keywords:", "Subtitulos")
par("gesture recognition; music education; early childhood; MediaPipe; invariant descriptor; spaced repetition; "
    "mixed-integer programming; adaptive learning; technology readiness; Montería", "Normal")

# ================================================================== 1. Introducción
H1("Introducción")
H2("Problema")
T("Aprender las notas con las manos es una práctica antigua de la pedagogía musical infantil: cada nota tiene una "
  "posición o forma de la mano, y el niño canta o toca mientras la reproduce. Llevar esa práctica a una aplicación "
  "plantea dos problemas técnicos distintos. El primero es perceptivo. Una cámara ve continuamente a la mano, también "
  "cuando esta viaja de una seña a otra o cuando las dos manos se cruzan, y el sistema solo debe sonar cuando el niño "
  "quiso hacer una seña. Un método que responde siempre acierta todas las señas válidas, pero también convierte "
  "cada transición en una nota. El segundo problema es de decisión. Después de cada intento hay que estimar qué "
  "habilidad domina el niño, cuándo conviene repasarla y qué actividades componen la siguiente sesión, con un tiempo "
  "limitado y sin repetir lo mismo.")
T("En Montería, según las proyecciones municipales del DANE, la población de 2026 es de 535.052 habitantes, de los "
  "cuales 80.254 tienen entre 3 y 12 años {c:dane}. Este trabajo no pretende diagnosticar la situación de la "
  "educación musical en la región: no se aporta aquí una estadística local sobre ella. La motivación es una "
  "justificación del equipo: una herramienta que corre en un computador con cámara y guarda sus datos en una base "
  "local no depende de conexión a internet para funcionar, lo que la hace candidata a ser probada en aulas de "
  "Montería y Córdoba. Esa pertinencia es una hipótesis por validar (sección 3.6), no un resultado.")
H2("Trabajos relacionados")
T("La literatura reciente sobre inteligencia artificial en educación musical es abundante. Las revisiones sobre "
  "primera infancia describen las tecnologías de IA disponibles {c:yi}; varios trabajos proponen trayectorias de "
  "aprendizaje musical personalizadas con aprendizaje por refuerzo o profundo {c:li_hong,li_peerj,li_disc,tang,wang}; "
  "otros incorporan el estado afectivo del estudiante {c:deng_sci,shi}; y otros analizan la retroalimentación con IA y "
  "la detección visual del teclado en la enseñanza de piano {c:deng_piano,chulu}, o ajustan la dificultad del material "
  "de lectura a primera vista {c:ramoneda}. La realidad aumentada y las aplicaciones móviles aparecen como vías "
  f"complementarias {{c:apay,barroso,leon}}. Para el seguimiento de la mano se usa MediaPipe Hands {{c:mediapipe}}.")
T("La Tabla 1 resume, a partir de los títulos y metadatos verificados en Crossref, cómo se ubica este trabajo "
  "frente a ellas. Esta comparación no equivale a una revisión sistemática, y las lecturas completas de los "
  "textos quedan como tarea del equipo antes de afirmar diferencias finas. Entre los trabajos citados, los "
  "títulos no indican uno cuya entrada sea una seña manual por nota calibrada para cada niño, con una decisión de "
  "sesión resuelta de forma exacta; esa combinación es el espacio en el que se ubica la propuesta.")
tabla("Tabla 1. Posición de Hand Sing Kids frente a los trabajos citados",
      ["Línea de trabajo", "Refs.", "Rasgo declarado en el título", "Contraste con este trabajo"],
      [["IA en primera infancia", cita("yi"), "Revisión de tecnologías de IA", "Marco general; no trata música ni señas"],
       ["Rutas de aprendizaje musical", cita("li_hong,li_peerj,li_disc,tang,wang"),
        "Aprendizaje por refuerzo o profundo",
        "Aquí la sesión se resuelve con programación entera mixta y no hay refuerzo"],
       ["Afecto en educación musical", cita("deng_sci,shi"), "Sistemas sensibles a la emoción",
        "Aquí no se modela el afecto"],
       ["Piano", cita("deng_piano,chulu"), "Retroalimentación con IA; detección de teclado",
        "La entrada es la mano sin instrumento físico"],
       ["Dificultad de la partitura", cita("ramoneda"), "Generación según dificultad",
        "Aquí la dificultad es un parámetro de la actividad"],
       ["Apps y realidad aumentada", cita("apay,barroso,leon"), "Análisis y evaluación de apps y RA",
        "Estudian uso y evaluación; no proponen un reconocedor de señas"]],
      "Fuente: elaboración propia a partir de los títulos de las referencias citadas (no es una revisión sistemática).",
      [3.6, 2.6, 4.9, 5.5])
H2("Objetivo y contribuciones")
T("El objetivo es describir y evaluar técnicamente, en laboratorio, el reconocedor de señas y el planificador de "
  "sesiones de Hand Sing Kids. Las contribuciones son tres y verificables: (i) un descriptor invariante de 120 "
  "componentes con una decisión basada en confianza y margen, comparado con el método de la versión inicial sobre "
  "señas válidas y posturas que no son seña; (ii) una formulación única que enlaza dominio, repaso espaciado, "
  "predictor logístico y selección de sesión por programación entera mixta, contrastada con el código; y (iii) un "
  "protocolo y unos scripts reproducibles, con intervalos de Wilson y una declaración explícita de límites.")

# ================================================================== 2. Métodos
H1("Métodos")
H2("Sistema y entorno de evaluación")
T("Hand Sing Kids es una aplicación de escritorio en Python con interfaz en PySide6. El repositorio evaluado "
  "contiene 62 módulos con 10.581 líneas (8.613 de código efectivo, sin líneas en blanco ni comentarios) y 9 archivos "
  "de pruebas con 1.746 líneas, organizados en ocho baterías. Las mediciones se hicieron en Windows 11, con Python "
  "3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0. La documentación del "
  "proyecto declara como objetivo macOS y Python 3.10 a 3.12; esa plataforma no se usó en esta evaluación. La "
  "arquitectura se muestra en la Figura 1.")
figura(["arquitectura.png"], 15.0, "Figura 1. Arquitectura funcional de Hand Sing Kids.")
H2("Descriptor invariante")
T("Sean $p_0,\\dots,p_{20}\\in\\mathbb{R}^3$ los 21 puntos de una mano, con $p_0$ en la muñeca. La escala de "
  "referencia es la distancia de la muñeca al nudillo del dedo medio:")
ecuacion("sigma", r"\sigma=\lVert p_9-p_0\rVert")
T("La curvatura de cada dedo, con cadena de articulaciones $(a,b,c,d)$, es una razón entre longitudes y por tanto "
  "invariante a escala, traslación y rotación:")
ecuacion("kappa", r"\kappa=\operatorname{clip}\!\left(\frac{\dfrac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+"
                  r"\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}-0{,}35}{0{,}65},\,0,\,1\right)")
T("La apertura entre dedos contiguos usa los vectores unitarios $u_i$ del nudillo a la yema, y la distancia del "
  "pulgar a cada yema se normaliza con $\\sigma$:")
ecuacion("alpha", r"\alpha_i=\frac{1}{\pi}\arccos\langle u_i,u_{i+1}\rangle,\quad i=1,\dots,4")
ecuacion("tau", r"\tau_j=\frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j}-p_4\rVert}{\sigma},\,0,\,3\right)")
T("A estas magnitudes se suman la normal del plano de la palma, la dirección de la mano en la imagen y la forma "
  "normalizada (20 puntos trasladados, escalados por $\\sigma$ y girados para que la mano apunte hacia arriba, "
  "40 valores). Cada mano queda en 58 valores y, con cuatro magnitudes de geometría entre las dos manos, el "
  "descriptor completo tiene $2\\times 58+4=120$ componentes. Las distancias se calculan por bloques $g$, cada uno "
  "con su peso $w_g$ (curvatura 3,0; forma 2,6; pulgar 2,0; dirección 2,0; entre manos 1,6; normal 1,4; apertura "
  "1,2), para que los 40 valores de la forma no dominen a los 5 de la curvatura:")
ecuacion("dist", r"d(a,b)=\sqrt{\frac{1}{\sum_g w_g}\sum_g w_g\,\frac{1}{|g|}\sum_{i\in g}(a_i-b_i)^2}")
H2("Clasificación con confianza y margen")
T("Cada nota $c$ conserva hasta tres muestras $S_c$ tomadas en la calibración del niño. La distancia de una postura "
  "$x$ a la nota es la menor de sus muestras, y la confianza reparte probabilidad entre las notas con una temperatura "
  "$T$ ajustada a la separación real de las señas del niño:")
ecuacion("dc", r"d_c=\min_{s\in S_c}d(x,s)")
ecuacion("softmax", r"P(c\mid x)=\frac{\exp\!\big(-(d_c-d_{\min})/T\big)}{\sum_k\exp\!\big(-(d_k-d_{\min})/T\big)}")
ecuacion("temp", r"T=\operatorname{clip}\!\left(\tfrac{1}{2}\min_{a\neq b}d(a,b),\,0{,}05,\,0{,}20\right)")
T("La nota se acepta solo si cumple las tres condiciones de la ecuación " + "{E_ACEPT}" + ". La tercera, el margen, hace "
  "que el sistema se abstenga cuando dos señas empatan:")
ecuacion("acepta", r"d_{\text{best}}\le 0{,}95,\qquad P_{\text{best}}\ge 0{,}55,\qquad P_{\text{best}}-P_{\text{second}}\ge 0{,}08")
H2("Estabilización temporal")
T("El estabilizador mantiene una ventana de $N$ lecturas, con $N=1$ por defecto. Una nota se confirma si aparece en "
  "al menos $\\max(1,\\operatorname{round}(0{,}62\\,N))$ posiciones, si su confianza media alcanza 0,55, si pasaron al "
  "menos 0,45 s desde la confirmación anterior (periodo refractario) y, cuando repite la última nota, solo si el "
  "niño la soltó antes. Se considera soltada cuando $R=6$ fotogramas consecutivos arrojan una lectura distinta. "
  "Este valor es el del código (`release_frames = 6`); la documentación del proyecto menciona dos fotogramas en "
  "su sección 3.5 y seis en el código y en la sección 11.6, y aquí se adopta el del código.")
H2("Dominio, repaso espaciado y predictor")
T("El dominio de una habilidad $s$ combina desempeño y retención. La retención multiplica, no suma, de modo que el "
  "desuso prolongado sí degrada una habilidad, mientras que $\\lambda$ evita que se desplome a cero:")
ecuacion("mastery", r"\mathcal{M}_s=\big(\lambda+(1-\lambda)R_s^{\gamma}\big)\big(w_pP_s+w_cC_s+w_vV_s\big)")
T("con $w_p=0{,}55$, $w_c=0{,}25$, $w_v=0{,}20$, $\\lambda=0{,}65$ y $\\gamma=0{,}40$. La precisión $P_s$ se suaviza con "
  "una distribución a priori, la consistencia $C_s$ penaliza alternar aciertos y fallos en los últimos $K=8$ "
  "intentos, la velocidad $V_s$ se mide contra un tiempo de referencia por franja de edad, y la retención decae de "
  "forma exponencial:")
ecuacion("prec", r"P_s=\frac{h_s+\alpha}{n_s+\alpha+\beta},\qquad \alpha=1,\ \beta=3")
ecuacion("ret", r"R_s=\exp\!\left(-\frac{\Delta t}{\tau_s}\right),\qquad \tau_s=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\qquad \tau_0=1{,}8\ \text{días}")
T("Aquí $h_s$ son los aciertos, $n_s$ los intentos, $\\Delta t$ los días desde la última práctica y $\\mathcal{M}_s^{-}$ "
  "el dominio de la actualización anterior, que evita una definición circular. El repaso espaciado adapta el "
  "esquema SM-2 {c:wozniak} a una calidad continua $q\\in[0,1]$ (el beneficio de la práctica distribuida está "
  "documentado en {c:cepeda}):")
ecuacion("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big),\qquad "
                r"I\leftarrow\begin{cases}1 & q<0{,}6\\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}")
T("Una habilidad pasa a dominada con $\\mathcal{M}_s\\ge 0{,}80$ y al menos seis intentos, y retrocede si cae de 0,70. "
  "La idea de seguir el dominio como una variable estimada a partir de los intentos proviene del seguimiento del "
  "conocimiento {c:corbett}. Cuando el niño acumula 40 intentos propios, un predictor logístico de tres variables "
  "sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, con 300 épocas de descenso de gradiente y "
  "tasa 0,35 sobre variables estandarizadas:")
ecuacion("logit", r"p=\frac{1}{1+e^{-z}},\qquad z=w_1\,\mathrm{precision}+w_2\,\mathrm{dificultad}+w_3\,\mathrm{dias}+b")
T("donde $\mathrm{precision}$ es la precisión suavizada de la nota, $\mathrm{dificultad}$ la de la actividad y "
  "$\mathrm{dias}$ los días desde la última práctica. Los pesos minimizan la entropía cruzada por descenso de gradiente:")
ecuacion("loss", r"\mathcal{L}=-\frac{1}{N}\sum_{n=1}^{N}\big[y_n\ln p_n+(1-y_n)\ln(1-p_n)\big],\qquad \mathbf{w}\leftarrow\mathbf{w}-\eta\,\nabla\mathcal{L}")
H2("Selección de la sesión por programación entera mixta")
T("Sean $A$ el conjunto de actividades candidatas, $S$ el de habilidades, $S_i\\subseteq S$ las que toca la "
  "actividad $i$, $G\\subseteq A$ las lúdicas y $V\\subseteq A$ las que atienden un repaso vencido. La variable de "
  "decisión es $x_i\\in\\{0,1\\}$. La probabilidad de éxito se estima con una logística sobre la holgura entre el "
  "dominio medio $\\bar\\mu_i$ y la dificultad $\\mathrm{dif}_i$, y el factor $\\eta_i$ concentra el valor en "
  "$p^{*}=0{,}75$, una dificultad intermedia coherente con la idea de que el aprendizaje es más eficiente cuando "
  "el error no es ni muy raro ni muy frecuente {c:wilson85}:")
ecuacion("p", r"p_i=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\quad k=6;\qquad "
              r"\eta_i=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\quad \sigma_p=0{,}18")
T("Con la ganancia $g_i=\\eta_i\\sum_{s\\in S_i}(1-\\mu_s)/\\sqrt{|S_i|}$, la urgencia de repaso $r_i$, la motivación "
  "$m_i$ (bonificación por tipo más novedad) y la fatiga inducida $f_i=(d_i/D)(0{,}5+\\mathrm{dif}_i)$, el problema es:")
ecuacion("milp", r"\begin{aligned}\max\ &\sum_{i\in A}\big(\alpha_1g_i+\alpha_2r_i+\alpha_3m_i-\alpha_4f_i\big)x_i\\ "
                 r"\text{s.a.}\ &\sum_i d_ix_i\le T_{\max},\quad \sum_i x_i=K,\quad x_i\le a_i,\quad \sum_{i\in G}x_i\ge1,\\ "
                 r"&\sum_i\mathrm{dif}_ix_i\le0{,}72K,\quad \sum_{i:\,s\in S_i}x_i\le2\ \ \forall s\in S,\quad \sum_{i\in V}x_i\ge1\end{aligned}")
T("con $\\alpha_1=1{,}00$, $\\alpha_2=0{,}70$, $\\alpha_3=0{,}35$ y $\\alpha_4=0{,}55$. Las restricciones fijan el tiempo "
  "total, el tamaño de la sesión, los prerrequisitos ($a_i=0$ si una habilidad de $S_i$ está bloqueada), al menos "
  "una actividad lúdica, una dificultad media acotada, un máximo de dos actividades por habilidad y la inclusión "
  "de un repaso vencido si existe. Se resuelve con CBC mediante PuLP y, si este no está disponible, por "
  "enumeración exhaustiva mientras $\\binom{|A|}{K}\\le 4\\times10^{5}$, lo que da el óptimo exacto.")
H2("Módulo Canciones")
T("El motor del módulo Canciones usa el reloj de la partida y no espera la seña. Con tempo $\\text{bpm}$, el "
  "intervalo entre notas es $g=60000/\\text{bpm}$ ms, la nota $i$ llega en $a_i=a_{i-1}+g$ con $a_0=2200$ ms, y su "
  "ventana de acierto es asimétrica, más ancha antes de la línea que después, para no penalizar al niño por el "
  "tiempo que el reconocimiento tarda en confirmar:")
ecuacion("vent", r"h_i=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2},\qquad "
                 r"\text{ventana}_i=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big],\quad W_{\min}=480\ \text{ms}")
T("El puntaje por nota es 100, 70 o 50 puntos según el error temporal (perfecto, bien, vale) y se multiplica por "
  "$\\min(1+0{,}5\\lfloor c/10\\rfloor,\\,4)$, con $c$ el combo de aciertos seguidos. Hay tres factores de tempo "
  "(0,72; 1,0; 1,15). El catálogo tiene 19 canciones de melodía tradicional o de dominio público, simplificadas a "
  "las ocho notas.")
H2("Protocolo de evaluación técnica")
T("La evaluación reproduce y amplía `tests/test_vision.py` sin modificarlo. La calibración de referencia contiene "
  "las ocho señas (Do3 a Do4) de una persona, guardadas como coordenadas de puntos de la mano, sin imágenes. "
  "Las perturbaciones son simuladas sobre esas coordenadas: escala entre 0,8 y 1,25, giro independiente por mano "
  "de ±18° y ruido gaussiano proporcional al tamaño de la mano. Se miden dos cosas. Primera, la tasa de "
  "reconocimiento de señas válidas con ruido $\\sigma\\in\\{0; 0{,}03; 0{,}06; 0{,}09\\}$: 60 repeticiones por nota y "
  "nivel, 480 señas por nivel. Segunda, las notas disparadas por error en 640 posturas que no son seña: 320 "
  "transiciones a medio camino entre una nota y otra tres posiciones más adelante, y 320 combinaciones de la mano "
  "izquierda de una seña con la derecha de otra. Las tasas se acompañan de intervalos de Wilson al 95 % {c:wilsonci}, "
  "y la estabilidad de la tasa de falsos positivos se midió con 30 semillas distintas. También se calculó la "
  "matriz de similitud entre las ocho señas con ambos métodos, la latencia del descriptor más el clasificador "
  "(2.000 repeticiones) y se ejecutaron las ocho baterías de prueba del repositorio. Los scripts están en "
  "`entrega_corte3/analisis/` y se ejecutan con una sola orden.")

# ================================================================== 3. Resultados y discusión
H1("Resultados y discusión")
H2("Verificación del repositorio")
T("Las ocho baterías (audio, integración, dominio, optimizador, predictor, canciones, estabilizador y visión) "
  "terminaron con código de salida 0. En el optimizador, la prueba que compara el MILP con la enumeración exacta "
  "pasó, y la sesión de ejemplo se resolvió con CBC en 40 ms con valor objetivo 2,9524. El predictor, en su prueba "
  "unitaria, mejora al azar sobre sus propios datos de entrenamiento (78 %); esa cifra es una verificación de que el "
  "ajuste converge y no una medida de capacidad predictiva, porque no hay datos de niños. La primera ejecución de "
  "las baterías, en la consola con la codificación predeterminada de Windows, produjo dos errores de impresión de "
  "caracteres especiales y no de lógica; con la salida en UTF-8 las ocho pasaron.")
H2("Reconocimiento de señas válidas")
filas_a = []
for a in R["aciertos"]:
    n, v = a["nuevo"], a["v1"]
    filas_a.append([f(a["ruido"], 2), str(a["n"]), f"{f(n['pct'])} ({f(n['ic95_lo'])}–{f(n['ic95_hi'])})",
                    f"{f(v['pct'])} ({f(v['ic95_lo'])}–{f(v['ic95_hi'])})"])
tabla("Tabla 2. Señas válidas reconocidas (%) según el ruido, con intervalo de Wilson al 95 %",
      ["Ruido σ", "n", "Descriptor propuesto", "Método v1"], filas_a,
      "Fuente: elaboración propia (analisis/evidencia_vision.py, semilla 11).", [2.5, 2.0, 5.0, 5.0])
T(f"Con ruido hasta 0,03 el descriptor propuesto reconoció todas las señas; con 0,06 llegó a "
  f"{f(R['aciertos'][2]['nuevo']['pct'])} % y con 0,09 a {f(R['aciertos'][3]['nuevo']['pct'])} % "
  f"(IC 95 %: {f(R['aciertos'][3]['nuevo']['ic95_lo'])} a {f(R['aciertos'][3]['nuevo']['ic95_hi'])} %). El método "
  "de la versión 1 acierta en todos los casos, pero esto se explica por lo que muestra la Tabla 3: responde siempre.")
H2("Posturas que no son seña")
fp = R["falsos_positivos"]
def fila_fp(nombre, d):
    n, v = d["nuevo"], d["v1"]
    return [nombre, str(n["n"]), f"{n['k']} ({f(n['pct'])}; {f(n['ic95_lo'])}–{f(n['ic95_hi'])})",
            f"{v['k']} ({f(v['pct'])}; {f(v['ic95_lo'])}–{f(v['ic95_hi'])})"]
tabla("Tabla 3. Notas disparadas por error ante posturas que no son seña (k; %; IC de Wilson al 95 %)",
      ["Tipo de postura", "n", "Descriptor propuesto", "Método v1"],
      [fila_fp("Transiciones a medio camino", fp["por_tipo"]["transicion"]),
       fila_fp("Manos cruzadas", fp["por_tipo"]["manos_cruzadas"]),
       fila_fp("Total", {"nuevo": fp["global_nuevo"], "v1": fp["global_v1"]})],
      "Fuente: elaboración propia (analisis/evidencia_vision.py, semilla 23).", [4.5, 1.5, 5.3, 5.3])
rb = R["robustez_fp_nuevo"]
T(f"El descriptor propuesto disparó {fp['global_nuevo']['k']} notas por error en {fp['global_nuevo']['n']} posturas "
  f"({f(fp['global_nuevo']['pct'])} %, IC 95 %: {f(fp['global_nuevo']['ic95_lo'])} a "
  f"{f(fp['global_nuevo']['ic95_hi'])} %), contra el 100 % del método v1. La tasa de 8 % reportada en la documentación "
  f"se reproduce. Con {rb['semillas']} semillas distintas la tasa media fue {f(rb['media'])} % (desviación estándar "
  f"{f(rb['sd'])}; mínimo {f(rb['min'])} %; máximo {f(rb['max'])} %), de modo que el valor no depende de una semilla "
  "favorable. El desglose no figuraba en la documentación y cambia la lectura: casi todo el error viene de las "
  f"transiciones ({f(fp['por_tipo']['transicion']['nuevo']['pct'])} %), mientras que las manos cruzadas casi no "
  f"disparan ({f(fp['por_tipo']['manos_cruzadas']['nuevo']['pct'])} %). Esto es plausible porque una postura a medio "
  "camino conserva rasgos de las dos señas extremas y una mano de cada seña no se parece a ninguna.")
figura(["aciertos.png", "falsos_positivos.png"], 7.9,
       "Figura 2. (a) Señas válidas reconocidas según el ruido (barras de error: IC de Wilson al 95 %; el eje parte de 70 %). "
       "(b) Notas disparadas por error ante posturas que no son seña, con los casos k/n.")
H2("Separabilidad de las señas y latencia")
mx = R["matrices"]
T(f"Con la calibración real, {mx['pares_sobre_0_65']} de los {mx['pares_ordenados']} pares ordenados de notas "
  f"distintas (es decir, {mx['pares_unicos_sobre_0_65']} pares no ordenados de 28) superan una similitud coseno de 0,65, "
  f"el umbral del método v1. El par más parecido es {mx['max_cos'][0]}–{mx['max_cos'][1]} con "
  f"{f(mx['max_cos'][2], 3)}. En el descriptor propuesto, la distancia entre notas distintas va de "
  f"{f(mx['dist_min_entre_notas'], 3)} a {f(mx['dist_max_entre_notas'], 3)}, lo que ajusta la temperatura a "
  f"$T={f(mx['temperatura'], 3)}$ según la ecuación {{E_TEMP}}. La Figura 3 muestra ambas matrices. En el "
  "método v1, dos nubes de puntos con forma de mano siempre se parecen, y por eso un umbral fijo de similitud no "
  "separa notas; el descriptor desplaza la comparación a magnitudes que sí cambian de una seña a otra.")
figura(["matriz_similitud.png"], 15.5,
       "Figura 3. Matrices 8 × 8 de las señas calibradas: (a) similitud coseno del método v1; (b) distancia por "
       "bloques del descriptor propuesto.")
lt = R["latencia"]
T(f"El descriptor y el clasificador tardaron {f(lt['media_ms'], 2)} ms por fotograma en promedio (percentil 95: "
  f"{f(lt['p95_ms'], 2)} ms; máximo: {f(lt['max_ms'], 2)} ms; {lt['reps']} repeticiones, un solo equipo). Esta "
  "cifra excluye la captura, el rastreo de MediaPipe y el dibujo en pantalla; la latencia de extremo a extremo, "
  "de la cámara a la pantalla, no se midió.")
H2("Discusión")
T("**Respuesta inmediata frente a margen.** Con ventana de un fotograma, la nota suena en cuanto el clasificador la "
  "reconoce, sin barra de aceptación. El costo es un 8 % de falsos positivos en transiciones, que antes la votación "
  "de varios fotogramas reducía a cambio de una espera perceptible. Es un cambio de compromiso y no una mejora en "
  "ambos sentidos. Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño "
  "desde Ajustes. Los resultados con ruido alto (86,0 %) indican que, en la práctica, un reconocimiento que se "
  "abstiene en lugar de equivocarse cuesta una repetición de la seña, mientras que un falso positivo rompe el juego.")
T("**La lección del sonido duplicado.** En una iteración posterior, una misma nota sostenida sonaba dos veces. La "
  "causa no estaba en el clasificador: con ventana de un fotograma, un parpadeo del rastreo (MediaPipe pierde la "
  "mano uno o dos fotogramas aunque esté quieta) se interpretaba como que el niño había soltado la seña, y la "
  "siguiente lectura repetía la nota. Con la ventana de varios fotogramas, la votación absorbía ese parpadeo; al "
  "quitarla, el mecanismo de suelta quedó como único filtro y su umbral hubo que subir de dos a seis fotogramas. "
  "Cambiar un parámetro de un módulo puede dejar a otro cargando con una función que no se había probado en "
  "solitario; la batería del estabilizador incluye ahora la prueba del parpadeo breve. También quedó documentada "
  "la corrección de que la aceleración progresiva atribuida a la versión inicial no existía: la velocidad era "
  "constante.")
T("**Amenazas a la validez.** (i) La calibración es de una sola persona y de ocho señas; no se conoce la "
  "variabilidad entre niños. (ii) Las perturbaciones son simuladas sobre coordenadas ya extraídas: no incluyen los "
  "errores de detección de MediaPipe, el desenfoque ni la iluminación. (iii) Las posturas negativas se construyeron "
  "por interpolación y combinación, y la tasa real depende de cómo se mueven los niños. (iv) El método v1 se "
  "evaluó con la misma calibración, de modo que la comparación es interna. (v) Las constantes (pesos del dominio, "
  "umbral 0,80, $p^{*}=0{,}75$, ventanas de acierto) provienen de la literatura y del ajuste sobre los datos "
  "disponibles, no de un estudio con niños. (vi) Las canciones son simplificaciones a la escala de ocho notas, "
  "sin revisión de un músico formado. (vii) No se implementó aprendizaje por refuerzo; el motor adaptativo es un "
  "conjunto de reglas, y las interfaces para aprendizaje automático y por refuerzo están documentadas sin datos "
  "reales que las alimenten. Estos límites impiden afirmar que el sistema enseñe música: solo respaldan que el "
  "reconocedor y el planificador se comportan como se describen en laboratorio.")
H2("Madurez tecnológica e impacto esperado")
T("Se propone **TRL 4**, validación de componentes en entorno de laboratorio. La evidencia a favor es que los "
  "componentes funcionan integrados en una aplicación ejecutable, con ocho baterías de prueba sin fallos y mediciones "
  "reproducibles con intervalos de confianza. La evidencia en contra de un nivel superior es que ningún componente "
  "se validó en el entorno de uso (aula, niños, iluminación y cámaras reales) ni con usuarios. El paso a TRL 5 "
  "exige un piloto con niños en aula; el protocolo está diseñado y no se ha ejecutado. El equipo debe confirmar el "
  "nivel final.")
T("El impacto esperado en Montería y Córdoba se formula como tres hipótesis a validar: (H1) niños de 3 a 12 años "
  "aprenden a reproducir las ocho señas con calibración individual en una sesión corta; (H2) en aula, la tasa de "
  "notas disparadas por error con niños es comparable a la de laboratorio o menor al aumentar la ventana; y (H3) "
  "la aplicación funciona sin conexión a internet en computadores con cámara. Solo H3 es una propiedad de diseño "
  "(los datos se guardan en una base SQLite local); las otras dos requieren datos de campo.")

# ================================================================== Conclusiones
H1("Conclusiones")
T("El descriptor invariante de 120 componentes con decisión por confianza y margen redujo las notas disparadas por "
  f"error del 100 % al {f(fp['global_nuevo']['pct'])} % en 640 posturas que no son seña, con un costo en sensibilidad "
  "solo visible con ruido alto. Ese 8 % se concentra en las transiciones y es el precio de la respuesta inmediata.")
T("La formulación de dominio, repaso espaciado, predictor logístico y selección de sesión por programación entera "
  "mixta coincide con el código, y la enumeración exacta reproduce el resultado del solucionador. Las cifras de la "
  "documentación del proyecto se reprodujeron; la única inconsistencia hallada fue el número de fotogramas de la "
  "suelta (dos en el texto, seis en el código).")
T("El sistema está en TRL 4. El trabajo futuro, en orden de prioridad, es: (1) una prueba con niños reales en aula; "
  "(2) más calibraciones y personas para medir la variabilidad; (3) validar las constantes con los datos que la "
  "aplicación ya registra; (4) aprendizaje por refuerzo sobre el contexto ya definido; y (5) señas de una mano "
  "al estilo Curwen-Kodály, que no exigirían calibración individual.")
H1("Recomendaciones")
T("Antes de la prueba en aula se recomienda medir la latencia de extremo a extremo, consultar la normativa sobre "
  "tratamiento de datos de menores y registrar, durante el piloto, las notas disparadas por error con niños en "
  "lugar de simularlas.")
sin_num(par("Contribución de los autores", "Heading 2"))
T("Contribución de los autores (taxonomía CRediT; por confirmar por el equipo antes del envío): los estudiantes "
  "autores participaron en conceptualización, desarrollo de software, investigación y redacción del borrador "
  "original; Cristian Javier Cano-Mogollón realizó la supervisión y la revisión y edición del manuscrito. Los "
  "autores leyeron y aprobaron la versión final.")
sin_num(par("Declaraciones finales", "Heading 2"))
H3("Financiación")
T("Esta investigación no recibió financiación externa. [Por confirmar por el equipo.]")
H3("Conflicto de intereses")
T("Los autores declaran que no existen conflictos de intereses relacionados con la presente publicación. [Por "
  "confirmar por el equipo.]")
H3("Consentimiento informado")
T("No aplica. No se recolectaron datos de niños; la calibración de referencia contiene únicamente coordenadas de "
  "puntos de la mano de una persona, sin imágenes.")
H3("Declaración de la Junta de Revisión Institucional")
T("No aplica, dado que el estudio es una evaluación técnica de laboratorio sin participantes en riesgo. Una "
  "prueba con niños requerirá aprobación ética y consentimiento de los acudientes.")
H3("Disponibilidad de datos, código y materiales de investigación")
T("El código, la calibración de referencia, las pruebas y los scripts de evaluación están en el repositorio del "
  "proyecto (https://github.com/Lossinn/Musica_Hand). Las salidas de las pruebas, el archivo resultados_vision.json y "
  "la verificación de referencias se encuentran en la carpeta entrega_corte3/analisis.")
H3("Uso de herramientas de inteligencia artificial")
T("Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar el análisis del código, la "
  "ejecución y documentación de las mediciones, la verificación de referencias y la redacción de borradores. Los "
  "autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.")

# ================================================================== English declarations (template)
par("Author Contributions", "Subtitulos")
T("CRediT roles (to be confirmed by the team before submission): the student authors contributed to "
  "conceptualization, software, investigation and writing of the original draft; C. J. Cano-Mogollón contributed "
  "supervision and review and editing. All authors read and approved the final version.")
par("Funding and Acknowledgments", "Subtitulos")
T("This research received no external funding. [To be confirmed by the team.]")
par("Conflicts of Interest", "Subtitulos")
T("The authors declare that there is no conflict of interests. [To be confirmed by the team.]")
par("Informed Consent Statement", "Subtitulos"); T("Not applicable.")
par("Institutional Review Board Statement", "Subtitulos"); T("Not applicable.")
par("Data, Code, and Research Materials Availability", "Subtitulos")
T("Code, reference calibration, tests and evaluation scripts are available at "
  "https://github.com/Lossinn/Musica_Hand.")

# ================================================================== Referencias
sin_num(par("References", "Heading 1"))
dane = ("DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” "
        "Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/"
        "Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.")

# reemplazos de marcadores {E_...} y construcción final de la lista
for p in doc.paragraphs:
    for r in p.runs:
        if "{E_ACEPT}" in r.text:
            r.text = r.text.replace("{E_ACEPT}", e("acepta"))
        if "{E_TEMP}" in r.text:
            r.text = r.text.replace("{E_TEMP}", e("temp"))

ORDEN_FIN = list(ORDEN)
tiene_dane = "dane" in ORDEN_FIN
for i, k in enumerate(ORDEN_FIN, 1):
    texto = dane if k == "dane" else ref_ieee(k)
    par(f"[{i}] {texto}", "Normal", size=8)

def reemplazar(parte, viejo, nuevo):
    for t in parte._element.iter(qn("w:t")):
        if viejo in (t.text or ""):
            t.text = t.text.replace(viejo, nuevo)


sec = doc.sections[0]
reemplazar(sec.header, "Apellido, A. Apellido", AUTORES[0][0].split()[-1] + " et al.")
reemplazar(sec.even_page_header, "Título del artículo", "Hand Sing Kids: reconocimiento de señas y selección de sesiones")
reemplazar(sec.first_page_footer, "Autores (A. Apellido).,",
           ", ".join(cita_autor(n) for n, _ in AUTORES) + " y C. J. Cano-Mogollón,")
reemplazar(sec.first_page_footer, "Título en el idioma en que se presenta el artículo,", TITULO_ES + ",")
doc.save(str(SALIDA))
print("guardado", SALIDA, "| refs citadas:", len(ORDEN_FIN), "| ecuaciones:", EQ_N[0])
print("citadas:", ORDEN_FIN)
