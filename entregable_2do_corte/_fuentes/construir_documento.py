"""Ensambla el documento (HTML en APA 7, trabajo de estudiante) y lo exporta a PDF con Microsoft Edge."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datos import BASE, BENCH, DANE, INST, n  # noqa: E402
from doc_base import CSS, NUM, ROOT, REFS, resolver  # noqa: E402
import doc_apa as D  # noqa: E402
import render  # noqa: E402

# Fórmula canónica: [acción] + [efecto] + [población] + [Montería/Córdoba] + [2026]
TITULO = ("Reconocimiento de Señas Manuales y Planificación Adaptativa para la Retroalimentación Inmediata y el "
          "Registro Objetivo del Aprendizaje de Notas Musicales en Niños de 3 a 12 Años de Montería, Córdoba, 2026")
FECHA = "1 de octubre de 2026"

RESUMEN = (
    f"En 2024 solo el {n(DANE['hog_internet_cor'], 1)} % de los hogares de Córdoba tenía internet, frente al "
    f"{n(DANE['hog_internet_nal'], 1)} % nacional, y en aulas de Montería y Cereté la enseñanza de las notas musicales "
    "depende de la atención de un docente a muchos niños, con nivelación manual y sin registro por nota. Hand Sing Kids, "
    "HSK, es una aplicación de escritorio que enseña las ocho notas del solfeo, de DO3 a DO4, a niños de 3 a 12 años "
    "mediante señas de las manos reconocidas por una cámara, y que procesa todo en el equipo del usuario. El modelo de "
    "procesos en BPMN 2.0 contrasta la clase actual con un proceso en que el reconocimiento, el registro y el repaso son "
    "automáticos. El prototipo combina un descriptor invariante de 120 componentes, un clasificador por distancia "
    "ponderada, un gemelo digital con repaso espaciado y una planificación de sesiones por programación lineal entera "
    "mixta. Sobre la calibración de referencia acierta el 100 % sin ruido y el 86,0 % con ruido alto, dispara una nota "
    f"por error en el 8,0 % de las posturas que no son seña y calcula en {n(BENCH['total_ms']['media'], 1)} ms por "
    "fotograma. Con insumos rotulados por procedencia, un aula obtiene un retorno de la inversión de "
    f"{n(BASE['roi_pct'], 1)} % en el primer año y la recupera en {n(BASE['payback_meses'], 1)} meses; una institución "
    f"con cuatro aulas, {n(INST['roi_pct'], 1)} % y {n(INST['payback_meses'], 1)} meses. Los supuestos y las constantes "
    "pedagógicas aún no se han validado con niños.")

ABSTRACT = (
    f"In 2024 only {n(DANE['hog_internet_cor'], 1).replace(',', '.')} % of households in Córdoba had internet access, "
    f"versus {n(DANE['hog_internet_nal'], 1).replace(',', '.')} % nationally, and in classrooms of Montería and Cereté "
    "music-note teaching relies on one teacher attending many children, with manual leveling and no per-note record. "
    "Hand Sing Kids, HSK, is a desktop application that teaches the eight solfège notes, C3 to C4, to children aged 3 to "
    "12 through hand signs recognized by a camera, processing everything on the user's computer. The BPMN 2.0 process "
    "model contrasts the current class with a process where recognition, recording and review are automatic. The "
    "prototype combines a 120-component invariant descriptor, a weighted-distance classifier, a learner digital twin with "
    "spaced repetition and a session planner formulated as a mixed-integer linear program. On the reference calibration "
    "it reaches 100 % accuracy without noise and 86.0 % under high noise, fires a wrong note on 8.0 % of non-sign "
    f"postures and computes in {n(BENCH['total_ms']['media'], 1).replace(',', '.')} ms per frame. With inputs labeled by "
    f"provenance, one classroom yields a first-year return on investment of {n(BASE['roi_pct'], 1).replace(',', '.')} % "
    f"and a payback of {n(BASE['payback_meses'], 1).replace(',', '.')} months; an institution with four classrooms, "
    f"{n(INST['roi_pct'], 1).replace(',', '.')} % and {n(INST['payback_meses'], 1).replace(',', '.')} months. "
    "Assumptions and pedagogical constants have not yet been validated with children.")


def palabras(t: str) -> int:
    return len(re.findall(r"\S+", t))


AUTORES = [("Alejandro Pemberty Vergara", "alejandro.pemberty@upb.edu.co"),
           ("Juliana Esther Carrascal", "juliana.carrascal@upb.edu.co"),
           ("Andrés Julian Negrete Pacheco", "andresj.negretep@upb.edu.co"),
           ("Juan Diego Guerra Gómez", "juan.guerra@upb.edu.co"),
           ("Isaias José Petro", "isaias.petro@upb.edu.co")]


def portada() -> str:
    """Portada de trabajo de estudiante (APA 7, sección 2.3): título, autores, afiliación, curso, docente y fecha."""
    return f"""
<section class="portada">
  <p class="titulo">{TITULO}</p>
  <p>{", ".join(a for a, _ in AUTORES[:-1])} y {AUTORES[-1][0]}</p>
  <p>Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería</p>
  <p>8830 0064 0: Gestión Tecnológica</p>
  <p>M.Sc. Cristian Javier Cano Mogollón</p>
  <p>{FECHA}</p>
</section>"""


def resumen() -> tuple[str, int, int]:
    nr, na = palabras(RESUMEN), palabras(ABSTRACT)
    assert nr <= 250 and na <= 250, (nr, na)
    return f"""
<section class="resumen">
  <h1>Resumen</h1>
  <p>{RESUMEN}</p>
  <p class="palabras"><em>Palabras clave:</em> reconocimiento de señas, educación musical, aprendizaje adaptativo, gemelo digital, programación lineal entera mixta, gobernanza de datos</p>
  <h1 class="salto">Abstract</h1>
  <p>{ABSTRACT}</p>
  <p class="palabras"><em>Keywords:</em> sign recognition, music education, adaptive learning, digital twin, mixed-integer linear programming, data governance</p>
</section>""", nr, na


def construir() -> tuple[Path, Path]:
    NUM.fig = NUM.tab = NUM.eq = 0
    REFS.clear()
    res, nr, na = resumen()
    cuerpo = "".join([D.introduccion(TITULO), D.diagnostico(), D.literatura(), D.metodo(), D.prototipo(),
                      D.bpmn(), D.dfd(), D.gobernanza(), D.finanzas(), D.discusion(), D.referencias()])
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{TITULO}</title><style>{CSS}</style></head>
<body>{portada()}{res}{cuerpo}</body></html>"""
    html = resolver(html)
    out_html = ROOT / "_fuentes" / "documento.html"
    out_html.write_text(html, encoding="utf-8")
    pdf = ROOT / "entrega_teams" / "01_Documento_EBT_GestionTecnologica_Equipo_XX.pdf"
    render.pdf(out_html, pdf)
    print(f"Resumen: {nr} palabras | Abstract: {na} palabras | figuras {NUM.fig} | tablas {NUM.tab} | ecuaciones {NUM.eq}")
    return out_html, pdf


if __name__ == "__main__":
    h, p = construir()
    import pymupdf
    d = pymupdf.open(p)
    print(p, "| páginas:", len(d))
