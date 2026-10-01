"""Ensambla el documento (HTML APA 7) y lo exporta a PDF con Microsoft Edge."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datos import BASE, BENCH, INST, n  # noqa: E402
from doc_base import CSS, NUM, ROOT, ASSETS, REFS, resolver  # noqa: E402
import doc_secciones_a as A  # noqa: E402
import doc_secciones_b as B  # noqa: E402
import doc_secciones_c as C  # noqa: E402
import render  # noqa: E402

TITULO = ("Reconocimiento de Señas Manuales y Planificación Adaptativa de la Práctica para la Enseñanza de Notas "
          "Musicales a Niños de 3 a 12 Años en Montería, Córdoba, 2026")

RESUMEN = (
    "Hand Sing Kids, HSK, es una aplicación de escritorio que enseña las ocho notas del solfeo, de DO3 a DO4, a niños de "
    "3 a 12 años mediante señas de las manos que reconoce una cámara. En 2024 solo el 47,2 % de los hogares de Córdoba "
    "tenía internet, frente al 65,6 % nacional, y un estudio previo de aulas de Montería y Cereté reporta atención docente "
    "de uno a muchos, nivelación manual y registro sin datos. El modelo de procesos en BPMN 2.0 contrasta ese proceso "
    "actual con uno en que el reconocimiento, el registro y el repaso son automáticos. El prototipo procesa todo de forma "
    "local: un descriptor invariante de 120 componentes, un clasificador por distancia ponderada, un gemelo digital con "
    "repaso espaciado y una planificación de sesiones por programación lineal entera mixta. Sobre la calibración de "
    "referencia acierta el 100 % sin ruido y el 86,0 % con ruido alto, con un 8,0 % de notas por error en posturas que no "
    f"son seña, y calcula en {n(BENCH['total_ms']['media'], 1)} ms por fotograma. Con insumos rotulados por procedencia, el "
    f"modelo financiero de un aula arroja un retorno de {n(BASE['roi_pct'], 1)} % en el primer año y una recuperación en "
    f"{n(BASE['payback_meses'], 1)} meses; en una institución con cuatro aulas, {n(INST['roi_pct'], 1)} % y "
    f"{n(INST['payback_meses'], 1)} meses. Los supuestos y las constantes pedagógicas no se han validado con niños; esa "
    "validación es la fase siguiente.")

ABSTRACT = (
    "Hand Sing Kids, HSK, is a desktop application that teaches the eight solfège notes, C3 to C4, to children aged 3 to "
    "12 through hand signs recognized by a camera. In 2024 only 47.2 % of households in Córdoba had internet access, "
    "versus 65.6 % nationally, and a previous study of classrooms in Montería and Cereté reports one-to-many teacher "
    "attention, manual leveling and unrecorded progress. The BPMN 2.0 process model contrasts that current process with "
    "one where recognition, recording and review are automatic. The prototype runs entirely locally: a 120-component "
    "invariant descriptor, a block-weighted distance classifier, a learner digital twin with spaced repetition and a "
    "session planner formulated as a mixed-integer linear program. On the reference calibration it reaches 100 % "
    "accuracy without noise and 86.0 % under high noise, with 8.0 % wrong notes on non-sign postures, and computes in "
    f"{n(BENCH['total_ms']['media'], 1)} ms per frame. With inputs labeled by provenance, the financial model for one "
    f"classroom yields a first-year return on investment of {n(BASE['roi_pct'], 1)} % and a payback of "
    f"{n(BASE['payback_meses'], 1)} months; for an institution with four classrooms, {n(INST['roi_pct'], 1)} % and "
    f"{n(INST['payback_meses'], 1)} months. Assumptions and pedagogical constants have not yet been validated with "
    "children; that validation is the next phase.")


def palabras(t: str) -> int:
    return len(re.findall(r"\S+", t))


def portada() -> str:
    logo = lambda f: Path(ASSETS / "logos" / f).resolve().as_uri()
    hsk = (ROOT / "recursos" / "identidad_visual" / "concepto_A_icono.svg").resolve().as_uri()
    return f"""
<section class="portada">
  <div class="logos">
    <img src="{logo('upb_logo_vertical_blanco.png')}" alt="UPB" style="height:2.6cm;border-radius:4px">
    <img src="{hsk}" alt="Hand Sing Kids">
    <img src="{logo('logo_his_engranaje.png')}" alt="HIS">
    <img src="{logo('logo_siloge.png')}" alt="SILOGE" style="height:2.3cm;border-radius:4px">
  </div>
  <p class="titulo">{TITULO}</p>
  <p>Plan de desarrollo del proyecto EBT Hand Sing Kids, versión 2.0</p>
  <p>&nbsp;</p>
  <p>Equipo XX: [nombres completos, códigos y correos institucionales de los integrantes]</p>
  <p>&nbsp;</p>
  <p>Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería</p>
  <p>Grupo de Investigación SILOGE · Hub Industrial Solution, HIS</p>
  <p>Gestión Tecnológica (8830 0064 0), segundo corte, periodo 2026-2</p>
  <p>Docente: M.Sc. Cristian Javier Cano Mogollón</p>
  <p>30 de septiembre de 2026</p>
</section>"""


def resumen() -> str:
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
    cuerpo = "".join([
        A.sec1_introduccion(), A.sec2_diagnostico(), C.sec2_campo(), A.sec3_literatura(), A.sec4_metodologia(),
        A.sec5_prototipo(), C.sec5_extra(),
        B.sec6_bpmn(), C.sec6_extra(), B.sec7_dfd(), B.sec8_gobernanza(), C.sec9_financiero(), C.sec10_discusion(),
        B.referencias(), C.anexos()])
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
    print(h, p)
