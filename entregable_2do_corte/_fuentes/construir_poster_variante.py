"""Variante del póster 90 x 120 cm: versión académica compacta, menos gráfica y con todo el contenido.

Estructura de póster de congreso: cabecera con los tres logos, título, autores y correos; cuerpo en dos columnas
de texto que fluyen (CSS multicolumna) con secciones numeradas IMRyD; tres figuras pequeñas (BPMN To-Be, DFD
nivel 1 y captura de la app), tablas breves, tarjeta de ROI y payback, conclusiones, referencias con DOI y QR.
Salida: entrega_teams/poster_variante.pdf y recursos/_previews/poster_variante.png.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datos import BASE, BENCH, CAT, DANE, INST, TOT, cita, cop, n, referencia_html, REF_EXTRA, DOIS  # noqa: E402
import doc_base  # noqa: E402
import render  # noqa: E402
from construir_documento import AUTORES, TITULO  # noqa: E402
from construir_poster import SOBRE, svg, uri  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "recursos" / "assets"
BRECHA = DANE["hog_internet_nal"] - DANE["hog_internet_cor"]
REFS = ["075", "038", "203"]
EXTRA = ("Zhang", "Departamento Administrativo Nacional de Estadistica 2", "Departamento Administrativo Nacional de Estadistica 1",
         "DAMA International", "Congreso de la Republica de Colombia")


def referencias() -> list[str]:
    """Subconjunto APA 7 de las referencias del documento, en orden alfabético."""
    items = [(DOIS[r]["autores"][0].split(",")[0], referencia_html(r)) for r in REFS]
    items += [(c, t + u) for c, u, t in REF_EXTRA if c in EXTRA]
    items.sort(key=lambda t: t[0].lower())
    return [h for _, h in items]

CSS = doc_base.FONT_FACE + """
@page { size: 900mm 1200mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 900mm; height: 1200mm; }
body { font-family: 'Montserrat', Helvetica, Arial, sans-serif; color: #1A1A1A; background: #FAFAF7; }
.poster { width: 900mm; height: 1200mm; display: flex; flex-direction: column; padding: 22mm 34mm 18mm; gap: 8mm;
  position: relative; overflow: hidden; }
.poster::before { content: ''; position: absolute; left: 14mm; right: 14mm; top: 10mm; bottom: 8mm;
  border: .5mm solid #C9C9C2; border-radius: 6mm; }
.cab, .cuerpo, .pie { position: relative; }
/* cabecera */
.cab { background: #141414; color: #fff; border-radius: 5mm; padding: 9mm 14mm 9mm; border-bottom: 3mm solid #FFCC00; }
.fila1 { display: grid; grid-template-columns: auto 1fr auto auto; gap: 9mm; align-items: center; }
.tile { height: 44mm; border-radius: 3.5mm; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.tile img { height: 100%; width: auto; display: block; }
.tile.upb { border: .8mm solid #FFCC00; background: #1D1D1B; }
.tile.his { background: #fff; padding: 3mm 5mm; } .tile.his img { height: 38mm; }
.tile.siloge { background: #F5CF5C; }
.evento { font-size: 17pt; letter-spacing: 3pt; font-weight: 800; color: #FFCC00; text-transform: uppercase; }
h1 { font-size: 44pt; line-height: 1.1; font-weight: 800; text-transform: uppercase; margin-top: 2mm; }
.inst { margin-top: 3mm; font-size: 17pt; color: #CFCFCF; font-weight: 500; }
.gente { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4mm; margin-top: 7mm; padding-top: 5mm;
  border-top: .4mm solid #3A3A3A; }
.p { border-left: 1.2mm solid #FFCC00; padding-left: 3.5mm; }
.p b { display: block; font-size: 18pt; font-weight: 700; line-height: 1.15; }
.p span { display: flex; align-items: center; gap: 1.4mm; font-size: 14pt; color: #FFCC00; font-weight: 600; margin-top: 1mm; }
.p svg { width: 4.2mm; height: 4.2mm; flex: none; }
.doc { margin-top: 4mm; font-size: 15pt; color: #BDBDBD; }
.doc b { color: #fff; }
/* cuerpo en dos columnas que fluyen */
.cuerpo { flex: 1; min-height: 0; column-count: 2; column-gap: 14mm; column-fill: balance;
  column-rule: .4mm solid #D6D6CF; }
.sec { break-inside: avoid; margin-bottom: 7mm; }
.sec h2 { display: flex; align-items: center; gap: 3.5mm; background: #141414; color: #fff; font-size: 23pt; font-weight: 800;
  text-transform: uppercase; letter-spacing: .4pt; padding: 2.2mm 5mm; border-radius: 2mm; margin-bottom: 3.5mm; }
.sec h2 i { font-style: normal; background: #FFCC00; color: #141414; border-radius: 1.4mm; padding: 0 2.6mm; font-size: 20pt; }
p, li { font-size: 19.5pt; line-height: 1.32; font-weight: 500; text-align: justify; hyphens: auto; }
p + p { margin-top: 2.4mm; }
em { font-style: italic; }
ul { padding-left: 7mm; margin-top: 2mm; } li { margin-bottom: 1mm; } li::marker { color: #B38F00; }
.fig { background: #fff; border: .4mm solid #D6D6CF; border-radius: 2mm; padding: 2mm; margin: 3mm 0 1.5mm; }
.fig img { width: 100%; display: block; border-radius: 1.4mm; }
.flot { float: right; width: 46%; margin: 2mm 0 2mm 5mm; }
.cap { font-size: 15pt; color: #555; line-height: 1.25; font-weight: 500; text-align: left; }
.cap b { color: #1A1A1A; }
table { width: 100%; border-collapse: collapse; margin: 3mm 0 1.5mm; font-size: 16.5pt; line-height: 1.22; }
th { background: #EDEDE6; text-align: left; font-weight: 800; padding: 1.6mm 2mm; border-bottom: .6mm solid #141414; }
td { padding: 1.4mm 2mm; border-bottom: .3mm solid #D6D6CF; font-weight: 500; vertical-align: top; }
td.r, th.r { text-align: right; white-space: nowrap; }
tr.t td { font-weight: 800; border-top: .6mm solid #141414; border-bottom: none; }
.eq { font-size: 18pt; text-align: center; background: #fff; border-left: 1.4mm solid #FFCC00; padding: 2mm 3mm; margin: 2.5mm 0;
  font-family: 'Cambria Math', 'Times New Roman', serif; }
.kpi { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0 2mm; }
.kpi div { border: .8mm solid #141414; border-radius: 2.5mm; text-align: center; padding: 2mm 1mm; background: #fff; }
.kpi div.hl { background: #FFCC00; }
.kpi small { display: block; font-size: 12.5pt; font-weight: 800; text-transform: uppercase; line-height: 1.1; }
.kpi b { display: block; font-size: 36pt; font-weight: 800; line-height: 1.05; }
.kpi span { display: block; font-size: 12.5pt; font-weight: 600; }
.refs p { font-size: 14pt; line-height: 1.25; text-align: left; padding-left: 6mm; text-indent: -6mm; margin-top: 1.2mm; }
.refs a { color: #1A1A1A; text-decoration: none; }
.qr { display: flex; gap: 5mm; align-items: center; margin-top: 3mm; }
.qr img { width: 46mm; height: 46mm; border: .6mm solid #141414; border-radius: 2mm; background: #fff; flex: none; }
.qr p { font-size: 17pt; text-align: left; }
.pie { flex: none; display: flex; justify-content: space-between; font-size: 13pt; color: #555; font-weight: 600;
  border-top: .6mm solid #141414; padding-top: 2.5mm; }
"""


def cabecera() -> str:
    gente = "".join(f'<div class="p"><b>{a}</b><span>{SOBRE}{m}</span></div>' for a, m in AUTORES)
    return f"""<header class="cab">
  <div class="fila1">
    <div class="tile upb"><img src="{uri(A / 'logos' / 'upb_logo_vertical_blanco.png')}" alt="UPB"></div>
    <div><p class="evento" style="text-align:left">Gestión Tecnológica · Segundo corte · 2026-2</p>
      <h1>{TITULO}</h1>
      <p class="inst" style="text-align:left">Universidad Pontificia Bolivariana, Seccional Montería · Facultad de Ingeniería Industrial ·
        Grupo de Investigación SILOGE · Hub Industrial Solution, HIS</p></div>
    <div class="tile his"><img src="{uri(A / 'logos' / 'logo_his_engranaje.png')}" alt="HIS"></div>
    <div class="tile siloge"><img src="{uri(A / 'logos' / 'logo_siloge.png')}" alt="SILOGE"></div>
  </div>
  <div class="gente">{gente}</div>
  <p class="doc">Equipo XX · Docente asesor: <b>M.Sc. Cristian Javier Cano Mogollón</b> · Gestión Tecnológica (8830 0064 0)</p>
</header>"""


def sec(num: int, titulo: str, cuerpo: str) -> str:
    return f'<section class="sec"><h2><i>{num}</i>{titulo}</h2>{cuerpo}</section>'


def cuerpo() -> str:
    s = []
    s.append(sec(1, "Introducción", f"""
<p>Hand Sing Kids, HSK, es una aplicación de escritorio que enseña las ocho notas del solfeo, de DO3 a DO4, a niños de
3 a 12 años mediante señas de las manos que reconoce una cámara. Cada seña se convierte en una nota, la nota se evalúa
y el resultado modifica la actividad siguiente. Todo el procesamiento ocurre en el equipo del usuario: no se graba video
y ningún dato sale hacia servidores externos. El proyecto se plantea como Empresa de Base Tecnológica, EBT.</p>"""))
    s.append(sec(2, "Problemática y brecha tecnológica", f"""
<p>En el aula, un docente atiende a muchos niños a la vez, nivela de forma manual y no conserva un registro por nota que
le permita decidir qué reforzar. La conectividad agrava el problema: una solución en la nube excluiría a la mitad de los
hogares de Córdoba.</p>
<table><tr><th>Indicador</th><th class="r">Valor</th><th>Fuente</th></tr>
<tr><td>Hogares de Córdoba con internet (nacional: {n(DANE['hog_internet_nal'], 1)} %)</td><td class="r">{n(DANE['hog_internet_cor'], 1)} %</td><td>DANE (2025)</td></tr>
<tr><td>Brecha frente al promedio nacional</td><td class="r">−{n(BRECHA, 1)} p. p.</td><td>DANE (2025)</td></tr>
<tr><td>Niños de 3 a 12 años en Montería, 2026</td><td class="r">{n(DANE['mon_3_12'])}</td><td>DANE (s. f.)</td></tr>
<tr><td>Nivelación manual por aula*</td><td class="r">1,0 a 1,5 h/sem</td><td>Equipo 13 (2026)</td></tr>
<tr><td>Papelería por aula al año*</td><td class="r">$ 600.000</td><td>Equipo 13 (2026)</td></tr></table>
<p class="cap">*Dato de campo no verificado. En la revisión de 15 estudios 2023-2026 con DOI verificado no se halló un
sistema que combine señas manuales, niños de 3 a 12 años, procesamiento local y adaptación interpretable.</p>"""))
    s.append(sec(3, "Pregunta y objetivos", """
<p><em>¿En qué medida un sistema local que reconoce señas manuales y planifica de forma adaptativa la práctica puede
ofrecer retroalimentación individual inmediata y un registro objetivo del dominio de las notas musicales?</em></p>
<ul><li><b>OE1.</b> Diagnosticar la brecha regional con indicadores oficiales y revisar la literatura reciente.</li>
<li><b>OE2.</b> Construir el prototipo: reconocimiento de señas, gemelo digital, planificación adaptativa y gobernanza local.</li>
<li><b>OE3.</b> Verificar el desempeño técnico y estimar el retorno de la inversión.</li></ul>"""))
    s.append(sec(4, "Método", """
<p>Ciclo IMRyD de diseño, construcción y verificación en cinco fases: diagnóstico (DANE, campo y proceso As-Is);
revisión (15 estudios, DOI verificados); construcción en Python con PySide6, MediaPipe, OpenCV, NumPy, PuLP y SQLite
(10.581 líneas de código y 1.746 de pruebas); verificación (pruebas automáticas, latencia y auditoría de integridad);
y evaluación financiera (CAPEX, OPEX, ROI y payback). Cada cifra se rotuló como verificada en código, en prueba,
de fuente oficial o supuesta.</p>"""))
    s.append(sec(5, "Arquitectura y prototipo (MVP)", f"""
<p>Cinco capas que solo dependen de las inferiores y un bus de eventos: interfaz, aplicación, dominio (evaluador,
gemelo, motor adaptativo), visión y persistencia. Ninguna pantalla importa MediaPipe, lo que permite probar sin cámara.
De los 21 puntos de cada mano se calcula un <em>descriptor invariante</em> de 120 componentes, con escala
σ = ‖p₉ − p₀‖ y curvatura por dedo, clasificado por distancia ponderada. El <em>gemelo digital</em> combina precisión,
consistencia, velocidad y retención con repaso espaciado; la sesión se elige con un programa lineal entero mixto, MILP:</p>
<p class="eq">máx Σ<sub>i</sub> (1,00 g<sub>i</sub> + 0,70 r<sub>i</sub> + 0,35 m<sub>i</sub> − 0,55 f<sub>i</sub>) x<sub>i</sub>,
x<sub>i</sub> ∈ {{0, 1}}, sujeto a 7 restricciones</p>
<div class="flot"><div class="fig" style="margin-top:0"><img src="{uri(A / 'capturas' / '11_ejercicio.png')}" alt="Ejercicio"></div>
<p class="cap"><b>Figura 1.</b> Ejercicio guiado: cada mano se reconoce y responde en pantalla.</p></div>
<p><b>Estado funcional:</b> 14 pantallas, 63 actividades, 8 suites de pruebas automáticas y perfiles por
niño en SQLite local. Nivel de madurez TRL 4, validación en laboratorio.</p><div style="clear:both"></div>"""))
    s.append(sec(6, "Procesos BPMN 2.0", f"""
<p><em>As-Is</em>: el docente prepara fichas, explica, corrige uno a uno con reproceso, anota en cuaderno y el acudiente
recibe un informe tardío. <em>To-Be</em>: pools y carriles para niño, sistema local (visión, evaluación, planificación)
y adulto; compuertas exclusivas, paralelas e inclusivas, eventos de temporizador y de mensaje.</p>
<div class="fig" style="width:82%;margin-left:auto;margin-right:auto">{svg('poster_bpmn_to_be')}</div>
<p class="cap"><b>Figura 2.</b> Proceso To-Be: reconocimiento en cada fotograma, registro automático y repaso programado.</p>"""))
    s.append(sec(7, "Flujos de datos (DFD)", f"""
<p>Nivel 0: el sistema intercambia datos con el niño, la cámara y el acudiente o docente, sin entidades en la nube.
Nivel 1: reconocer, evaluar, gemelo, planificar, interfaz e informe, con los almacenes D3 Intentos y D4 Habilidad.
Nivel 2: detalle del proceso crítico de evaluación y actualización del gemelo.</p>
<div class="fig" style="width:64%;margin-left:auto;margin-right:auto">{svg('poster_dfd1')}</div>
<p class="cap"><b>Figura 3.</b> DFD nivel 1 simplificado; los niveles completos están en el documento.</p>"""))
    s.append(sec(8, "Gobernanza de datos (DAMA-DMBOK)", f"""
<table><tr><th>Componente</th><th>Implementación</th></tr>
<tr><td>Catálogo y diccionario</td><td>{CAT['_resumen']['tablas']} tablas y {CAT['_resumen']['columnas']} campos con tipo, cardinalidad y regla de validación</td></tr>
<tr><td>Linaje</td><td>Cámara → 21 puntos → descriptor (efímero) → nota (sesión) → intento, gemelo y decisión (persistente)</td></tr>
<tr><td>Calidad</td><td>Completitud 100 %; exactitud 96,9 %; consistencia parcial (4 de 8 reglas en la base); oportunidad en la misma sesión</td></tr>
<tr><td>Seguridad y privacidad</td><td>0 imágenes en disco, 0 módulos de red; RBAC niño, adulto con PIN (propuesto) y sistema; respaldo y retención propuestos; Ley 1581 de 2012</td></tr></table>"""))
    s.append(sec(9, "Resultados", f"""
<table><tr><th>Prueba (calibración de referencia)</th><th class="r">Resultado</th></tr>
<tr><td>Acierto en señas válidas sin ruido</td><td class="r">100 %</td></tr>
<tr><td>Acierto con ruido moderado (σ = 0,06)</td><td class="r">96,9 %</td></tr>
<tr><td>Acierto con ruido alto (σ = 0,09)</td><td class="r">86,0 %</td></tr>
<tr><td>Posturas que no son seña con nota disparada (n = 640)</td><td class="r">8,0 %</td></tr>
<tr><td>Cómputo por fotograma (media; percentil 95: {n(BENCH['total_ms']['p95'], 1)} ms)</td><td class="r">{n(BENCH['total_ms']['media'], 1)} ms</td></tr></table>
<p class="cap">La versión 1 disparaba nota en el 100 % de las posturas que no eran seña. La latencia excluye la captura de
cámara y MediaPipe.</p>"""))
    s.append(sec(10, "Viabilidad financiera: ROI y payback", f"""
<table><tr><th>Concepto (un aula)</th><th class="r">COP</th></tr>
<tr><td>CAPEX: ingeniería, hardware, licencias, capacitación y consulta jurídica</td><td class="r">{cop(TOT['capex'])}</td></tr>
<tr><td>OPEX anual: soporte, reposición y energía (nube y API: $ 0)</td><td class="r">{cop(TOT['opex'])}</td></tr>
<tr><td>Beneficios anuales: horas de nivelación y papelería</td><td class="r">{cop(TOT['beneficios'])}</td></tr>
<tr class="t"><td>Beneficio neto anual</td><td class="r">{cop(BASE['beneficio_neto'])}</td></tr></table>
<p class="eq">ROI = beneficio neto anual / CAPEX · Payback = CAPEX / beneficio neto mensual</p>
<div class="kpi">
  <div class="hl"><small>ROI · 4 aulas</small><b>{n(INST['roi_pct'], 1)} %</b><span>guía ≥ 30 %</span></div>
  <div class="hl"><small>Payback · 4 aulas</small><b>{n(INST['payback_meses'], 1)}</b><span>meses (guía ≤ 12)</span></div>
  <div><small>ROI · 1 aula</small><b>{n(BASE['roi_pct'], 1)} %</b><span>no cumple</span></div>
  <div><small>Payback · 1 aula</small><b>{n(BASE['payback_meses'], 1)}</b><span>meses</span></div></div>
<p class="cap">La viabilidad depende de la escala: un aula aislada no alcanza los criterios de la guía.</p>"""))
    s.append(sec(11, "Conclusiones", """
<p>El prototipo reconoce las ocho señas en 2,3 ms de cómputo por fotograma, rechaza 92 de cada 100 posturas que no son
seña y adapta la práctica con un gemelo digital y una planificación MILP explicable a un docente. La brecha de
conectividad de 18,4 puntos justifica el diseño local. Limitaciones: una sola calibración, sin pruebas con niños y
beneficios basados en cifras secundarias. Siguiente fase: piloto cuasi-experimental de ocho semanas con grupo de control.</p>"""))
    refs = "".join(f"<p>{r}</p>" for r in referencias())
    s.append(sec(12, "Referencias", f"""<div class="refs">{refs}</div>
<div class="qr"><img src="{uri(A / 'qr_repositorio.svg')}" alt="QR"><p><b>Código, pruebas y documento completo</b><br>
github.com/Lossinn/Musica_Hand</p></div>"""))
    return "".join(s)


def html() -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Póster variante 90 x 120 cm</title>
<style>{CSS}</style></head><body><div class="poster">
{cabecera()}
<main class="cuerpo">{cuerpo()}</main>
<footer class="pie"><span>Hand Sing Kids · Empresa de Base Tecnológica · Montería, Córdoba</span>
<span>Cifras técnicas medidas en el código; las financieras dependen de supuestos declarados en el documento</span></footer>
</div></body></html>"""


def construir() -> Path:
    out_html = ROOT / "_fuentes" / "poster_variante.html"
    out_html.write_text(html(), encoding="utf-8")
    pdf = ROOT / "entrega_teams" / "poster_variante.pdf"
    render.pdf(out_html, pdf)
    return pdf


if __name__ == "__main__":
    p = construir()
    import pymupdf
    d = pymupdf.open(p)
    r = d[0].rect
    print("páginas:", len(d), "| tamaño:", round(r.width / 72 * 25.4), "x", round(r.height / 72 * 25.4), "mm")
    d[0].get_pixmap(dpi=22).save(ROOT / "recursos" / "_previews" / "poster_variante.png")
