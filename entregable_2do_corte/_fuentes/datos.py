"""Datos comunes del entregable: cifras verificadas, formato español y referencias APA 7."""
from __future__ import annotations

import html
import json
from pathlib import Path

F = Path(__file__).resolve().parent
ROOT = F.parent

FIN = json.loads((F / "modelo_financiero.json").read_text(encoding="utf-8"))
BENCH = json.loads((F / "bench_latencia.json").read_text(encoding="utf-8"))
CAT = json.loads((F / "catalogo_datos.json").read_text(encoding="utf-8"))
DOIS = {r["id"]: r for r in json.loads((F / "doi_verificados.json").read_text(encoding="utf-8"))}


# ------------------------------------------------------------------ formato
def n(v: float, d: int = 0) -> str:
    """Número con coma decimal y punto de miles."""
    s = f"{v:,.{d}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def cop(v: float) -> str:
    return "$ " + n(v)


def pct(v: float, d: int = 1) -> str:
    return n(v, d) + " %"


ESC = FIN["escenarios"]
BASE = ESC["Base (1 aula)"]
INST = ESC["Institución con 4 aulas"]
OPT = ESC["Optimista (con instrumental evitado)"]
CONS = ESC["Conservador (beneficios -25 %)"]
ESCALA = [v for k, v in ESC.items() if k.startswith("Escala (")][0]
TOT = FIN["totales"]

# Indicadores verificados (DANE ENTIC Hogares 2024, boletín técnico del 1 de agosto de 2025).
# Los de Córdoba se leyeron de los gráficos 6, 13 y 15 (posición de la etiqueta y del valor en el PDF).
# Población: archivo oficial del DANE de proyecciones municipales por edad simple, actualización
# post COVID-19, fila 23001 Montería, año 2026, área Total (dane_monteria_2026.json, 1 oct. 2026).
_POB = json.loads((F / "dane_monteria_2026.json").read_text(encoding="utf-8"))
DANE = dict(
    hog_internet_cor=47.2, hog_internet_nal=65.6, hog_internet_cab=72.5, hog_internet_rur=41.9,
    pers_comp_cor=25.2, pers_comp_nal=35.1, pers_int_cor=71.9, pers_int_nal=79.3, hog_comp_nal=35.7,
    mon_total=_POB["total"], mon_3_12=_POB["edad_3_12"],
    mon_3_5=_POB["edad_3_5"], mon_6_8=_POB["edad_6_8"], mon_9_12=_POB["edad_9_12"],
)

# Orden y metadatos de las referencias (id de la matriz bibliográfica)
REF_IDS = ["203", "075", "032", "077", "044", "046", "038", "144", "164", "129", "220", "002", "186", "161", "081"]
TITULO_APA = {   # títulos en minúscula de oración (APA 7)
    "203": "The key artificial intelligence technologies in early childhood education: A review",
    "075": "Deep reinforcement learning for personalised music learning pathways",
    "032": "A reinforcement learning-based adaptive evaluation framework for personalized music education",
    "077": "Deep learning-based personalized learning path planning and optimization model for music education",
    "044": "An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement",
    "046": "An affective computing framework for preschool music education using MoE architecture and neural radiance fields",
    "038": "AI-based feedback systems in piano education: Effects on technical accuracy and learner autonomy",
    "144": "Piano keyboard detection algorithm using deep learning",
    "164": "The application of deep reinforcement learning in music teaching interaction",
    "129": "Music teaching evaluation using multimodal deep reinforcement learning",
    "220": "Difficulty-aware score generation for piano sight-reading",
    "002": "Content analysis of music education studies related to augmented reality technology",
    "186": "Exploring the integration of bite-sized learning: A scoping review of research in education and related disciplines",
    "161": "El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: Un estudio experimental",
    "081": "Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos",
}


def _iniciales(nombre: str) -> str:
    partes = [p for p in nombre.replace("-", " - ").split() if p]
    out = []
    for p in partes:
        out.append("-" if p == "-" else p[0].upper() + ".")
    return " ".join(out).replace(" - ", "-")


def _autores_apa(aut: list[str]) -> str:
    fmt = []
    for a in aut:
        ap, _, nom = a.partition(", ")
        ap = ap.title() if ap.isupper() else ap
        fmt.append(f"{ap}, {_iniciales(nom)}" if nom else ap)
    if len(fmt) == 1:
        return fmt[0]
    if len(fmt) <= 20:
        return ", ".join(fmt[:-1]) + ", y " + fmt[-1]
    return ", ".join(fmt[:19]) + ", … " + fmt[-1]


def cita(rid: str, largo: bool = False) -> str:
    """Cita en texto (Autor, año)."""
    r = DOIS[rid]
    ap = [a.split(",")[0] for a in r["autores"]]
    ap = [x.title() if x.isupper() else x for x in ap]
    if len(ap) == 1:
        a = ap[0]
    elif len(ap) == 2:
        a = f"{ap[0]} y {ap[1]}"
    else:
        a = f"{ap[0]} et al."
    return f"{a} ({r['anio']})" if largo else f"{a}, {r['anio']}"


def referencia_html(rid: str) -> str:
    r = DOIS[rid]
    rev = html.escape(r["revista"].replace("&amp;", "&"))
    vol = r.get("volumen"); num = r.get("numero"); pag = r.get("paginas") or r.get("articulo")
    det = f"<em>{rev}</em>"
    if vol:
        det += f", <em>{vol}</em>"
        if num:
            det += f"({num})"
    if pag:   # APA 7: intervalo de páginas con raya corta; si no, número de artículo (e-locator)
        import re
        det += f", {pag.replace('-', '–')}" if re.fullmatch(r"\d+-\d+", pag) else f", Artículo {pag}"
    url = f"https://doi.org/{r['doi']}"
    return (f"{html.escape(_autores_apa(r['autores']))} ({r['anio']}). {html.escape(TITULO_APA[rid])}. {det}. "
            f'<a href="{url}">{url}</a>')


REF_EXTRA = [
    ("Equipo 13", "",
     "Equipo 13. (2026). <em>Documento técnico de ingeniería y arquitectura de proyecto: Desarrollo de un sistema inteligente adaptativo mediante "
     "visión computacional, gamificación e inteligencia artificial para el aprendizaje de teoría musical infantil en el Departamento de Córdoba 2026</em> "
     "[Manuscrito no publicado, Proyecto Integrador II]. Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería."),
    ("Zhang", '<a href="https://doi.org/10.48550/arXiv.2006.10214">https://doi.org/10.48550/arXiv.2006.10214</a>',
     "Zhang, F., Bazarevsky, V., Vakunov, A., Tkachenka, A., Sung, G., Chang, C.-L., y Grundmann, M. (2020). "
     "<em>MediaPipe Hands: On-device real-time hand tracking</em> (arXiv:2006.10214). arXiv. "),
    ("Departamento Administrativo Nacional de Estadistica 2", '<a href="https://www.dane.gov.co/files/operaciones/ENTIC/bol-ENTICHogares-2024.pdf">'
     'https://www.dane.gov.co/files/operaciones/ENTIC/bol-ENTICHogares-2024.pdf</a>',
     "Departamento Administrativo Nacional de Estadística. (2025, 1 de agosto). <em>Encuesta de Tecnologías de la "
     "Información y las Comunicaciones en Hogares (ENTIC Hogares) 2024: Boletín técnico</em>. "),
    ("Departamento Administrativo Nacional de Estadistica 1", '<a href="https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/'
     'DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx">https://www.dane.gov.co/files/censo2018/'
     'proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx</a>',
     "Departamento Administrativo Nacional de Estadística. (s. f.). <em>Proyecciones de población municipal por área, "
     "sexo y edad, periodo 2020-2035: Actualización post COVID-19</em> [Conjunto de datos]. Recuperado el 1 de octubre "
     "de 2026, de "),
    ("DAMA International", "",
     "DAMA International. (2017). <em>DAMA-DMBOK: Data management body of knowledge</em> (2.ª ed.). Technics Publications."),
    ("Congreso de la Republica de Colombia", '<a href="https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981">'
     'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981</a>',
     "Congreso de la República de Colombia. (2012, 17 de octubre). <em>Ley Estatutaria 1581 de 2012, por la cual se dictan "
     "disposiciones generales para la protección de datos personales</em>. Función Pública. "),
]


def referencias_ordenadas() -> list[str]:
    items = []
    for rid in REF_IDS:
        r = DOIS[rid]
        ap = r["autores"][0].split(",")[0]
        items.append((ap.title() if ap.isupper() else ap, referencia_html(rid)))
    for clave, url, txt in REF_EXTRA:
        items.append((clave, txt + url))
    items.sort(key=lambda t: t[0].lower().replace("á", "a").replace("é", "e").replace("í", "i"))
    return [h for _, h in items]
