"""Póster científico 90 x 120 cm (vertical) en HTML/CSS -> PDF con Microsoft Edge.

Sigue PLANTILLA_CONTENIDO_POSTER.md: identidad HIS (amarillo #FFCC00, negro #141414, grises, fondo de
papel con capa kraft y marca de agua HIS al 5 %), logos UPB, HIS y SILOGE en la cabecera, tres columnas
(contexto | procesos y datos | desarrollo, ROI y proyección), poco texto y tarjetas de KPI.

Maquetación: el póster es una columna flexible (cabecera, cuerpo, pie). El cuerpo es una rejilla de tres
columnas; en cada columna la última tarjeta crece para que las tres terminen a la misma altura.
Tipografía: título 58 pt, encabezados de tarjeta 34 pt, texto 27 pt (legible a 1 m), notas 19 pt.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datos import BASE, BENCH, CAT, DANE, INST, TOT, cita, cop, n, pct  # noqa: E402
import doc_base  # noqa: E402
import logos  # noqa: E402
import render  # noqa: E402
from construir_documento import TITULO  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "recursos" / "assets"
D = ROOT / "recursos" / "diagramas"
BRECHA = DANE["hog_internet_nal"] - DANE["hog_internet_cor"]


def uri(p: Path) -> str:
    return p.resolve().as_uri()


def svg(nombre: str) -> str:
    s = (D / f"{nombre}.svg").read_text(encoding="utf-8")
    return s.replace(' width="', ' data-w="', 1).replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)


def mano_svg() -> str:
    """Esqueleto de mano abierta (21 puntos, topología de MediaPipe) como marca de agua de la cabecera."""
    pts = logos._landmarks()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    ln = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="#FFCC00" '
                 f'stroke-width="7" stroke-linecap="round"/>' for a, b in logos.MP_EDGES)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{10 if i in (4, 8, 12, 16, 20) else 7}" fill="#fff"/>'
                   for i, (x, y) in enumerate(pts))
    return f'<svg viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" xmlns="http://www.w3.org/2000/svg">{ln}{dots}</svg>'


CSS = doc_base.FONT_FACE + """
@page { size: 900mm 1200mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 900mm; height: 1200mm; }
body { font-family: 'Montserrat', Helvetica, Arial, sans-serif; color: #141414; }
.poster { position: relative; width: 900mm; height: 1200mm; overflow: hidden; background: #C9A26B;
  display: flex; flex-direction: column; padding: 22mm 50mm 16mm; gap: 9mm; }
.fondo, .kraft { position: absolute; inset: 0; }
.fondo { background: url('__FONDO__') center/cover; opacity: .55; mix-blend-mode: multiply; }
.kraft { background: linear-gradient(180deg, rgba(214,178,122,.45), rgba(196,156,98,.45)); }
.marca { position: absolute; left: 50%; top: 56%; width: 640mm; transform: translate(-50%, -50%); opacity: .05; }
.tira { position: absolute; top: 0; height: 1200mm; width: 34mm; }
.tira.izq { left: 0; } .tira.der { right: 0; }
.cab, .cuerpo, .pie, .franja { position: relative; }
/* ------------------------------------------------------------- cabecera */
.cab { background: #141414; border-radius: 8mm; padding: 11mm 16mm 12mm; color: #fff; overflow: hidden;
  box-shadow: 0 3mm 6mm rgba(0,0,0,.35); }
.cab .mano { position: absolute; right: -4mm; bottom: -10mm; width: 120mm; opacity: .13; }
.logos { display: grid; grid-template-columns: auto 1fr auto auto; gap: 10mm; align-items: center; }
.tile { height: 54mm; border-radius: 5mm; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.tile img { height: 100%; width: auto; display: block; }
.tile.upb { border: .9mm solid #FFCC00; background: #1D1D1B; }
.tile.his { background: #fff; padding: 4mm 6mm; } .tile.his img { height: 46mm; }
.tile.siloge { background: #F5CF5C; }
.inst { text-align: center; font-size: 21pt; line-height: 1.3; color: #E6E6E6; font-weight: 500; }
.inst b { display: block; color: #fff; font-size: 25pt; font-weight: 700; }
h1.titulo { margin-top: 9mm; color: #FFCC00; font-weight: 800; text-transform: uppercase; font-size: 56pt;
  line-height: 1.08; letter-spacing: .2pt; }
.sub { margin-top: 5mm; font-size: 27pt; font-weight: 600; color: #fff; }
.equipo { margin-top: 3mm; font-size: 21pt; color: #CFCFCF; font-weight: 500; line-height: 1.3; }
.franja { height: 10mm; border-radius: 2mm; background: repeating-linear-gradient(135deg, #FFCC00 0 9mm, #141414 9mm 18mm); flex: none; }
/* ---------------------------------------------------------------- cuerpo */
.cuerpo { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 1.3fr 1fr; gap: 12mm; }
.col { display: flex; flex-direction: column; gap: 10mm; min-width: 0; }
.col > .card:last-child { flex: 1; }
.card { background: rgba(255,255,255,.97); border-radius: 4mm; padding: 0 9mm 8mm; box-shadow: 0 2mm 4mm rgba(60,35,5,.3);
  border-bottom: 3mm solid #141414; display: flex; flex-direction: column; }
.card.oscura { background: #1c1c1c; color: #fff; }
.card h2 { margin: 0 -9mm 6mm; padding: 3.5mm 9mm; background: #141414; color: #FFCC00; border-radius: 4mm 4mm 0 0;
  font-size: 32pt; font-weight: 800; text-transform: uppercase; line-height: 1.1; display: flex; align-items: center; gap: 4mm; }
.card.oscura h2 { background: #FFCC00; color: #141414; }
h2 .n { flex: none; background: #FFCC00; color: #141414; border-radius: 50%; width: 13mm; height: 13mm; text-align: center;
  line-height: 13mm; font-size: 24pt; }
.card.oscura h2 .n { background: #141414; color: #FFCC00; }
p, li { font-size: 26pt; line-height: 1.25; font-weight: 500; }
ul { list-style: none; display: grid; gap: 2.5mm; }
li { padding-left: 9mm; position: relative; }
li::before { content: ''; position: absolute; left: 0; top: 4.2mm; width: 4.4mm; height: 4.4mm; background: #FFCC00;
  border: .8mm solid #141414; border-radius: 1mm; }
.card.oscura li::before { border-color: #FFCC00; }
.fuente { font-size: 18pt; color: #555; line-height: 1.2; margin-top: auto; padding-top: 3mm; }
.card.oscura .fuente { color: #BDBDBD; }
.kpis { display: grid; gap: 4mm; margin-bottom: 5mm; }
.kpis.k3 { grid-template-columns: repeat(3, 1fr); } .kpis.k2 { grid-template-columns: 1fr 1fr; } .kpis.k4 { grid-template-columns: repeat(4, 1fr); }
.kpi { background: #F5F5F5; border-radius: 3mm; padding: 4mm 2mm 3mm; text-align: center; border-top: 2.4mm solid #FFCC00; }
.kpi b { display: block; font-size: 44pt; font-weight: 800; line-height: 1; }
.kpi span { display: block; font-size: 18pt; line-height: 1.15; margin-top: 2mm; font-weight: 600; color: #404040; }
.card.oscura .kpi { background: #FFCC00; border-top-color: #fff; } .card.oscura .kpi span { color: #141414; }
.card.oscura .kpi b { color: #141414; font-size: 38pt; }
.arbol { display: grid; gap: 3mm; }
.fila { display: grid; gap: 3mm; grid-template-columns: 1fr 1fr; }
.caja { border: .9mm solid #141414; border-radius: 3mm; padding: 2.5mm 3mm; font-size: 19pt; line-height: 1.15; text-align: center; font-weight: 600; }
.caja.e { background: #F5F5F5; } .caja.c { background: #fff; }
.caja.p { background: #FFCC00; font-size: 21pt; font-weight: 800; }
.rot { font-size: 16pt; font-weight: 800; letter-spacing: 1pt; color: #707070; text-align: center; }
.ods { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 5mm; }
.od { background: #141414; color: #fff; border-radius: 3mm; padding: 2.5mm 2mm; text-align: center; }
.od b { display: block; font-size: 34pt; color: #FFCC00; font-weight: 800; line-height: 1; }
.od span { display: block; font-size: 15pt; line-height: 1.15; margin-top: 1mm; font-weight: 600; }
.pregunta { font-style: italic; font-weight: 600; background: #FFF6D6; border-left: 2.4mm solid #FFCC00; padding: 3mm 4mm; margin-bottom: 4mm; }
.oe b { color: #141414; font-weight: 800; }
.brecha { background: #FFCC00; border-radius: 3mm; padding: 4mm 5mm; margin-top: 4mm; border: 1.2mm solid #141414; }
.brecha p { font-size: 24pt; font-weight: 700; }
.dia { background: #fff; border: .7mm solid #C8C8C8; border-radius: 3mm; padding: 1.5mm; }
.cap { font-size: 18pt; color: #404040; font-weight: 600; margin: 2mm 0 0; line-height: 1.2; }
.paso { text-align: center; font-size: 22pt; font-weight: 800; margin: 3mm 0; color: #141414; }
.paso span { background: #FFCC00; border-radius: 10mm; padding: 1mm 8mm; }
.dos { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; align-items: start; }
.chips { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; }
.chip { background: #F5F5F5; border-radius: 3mm; padding: 3mm 3.5mm; font-size: 18pt; line-height: 1.15; font-weight: 600; border-left: 2.4mm solid #141414; }
.chip b { font-size: 34pt; display: block; font-weight: 800; line-height: 1.05; }
.linaje { display: flex; gap: 1.6mm; margin: 4mm 0 2mm; }
.lp { flex: 1; font-size: 16pt; line-height: 1.12; text-align: center; padding: 2.5mm 1mm; border-radius: 2.5mm; border: .7mm solid #141414; font-weight: 700; }
.lp.e { background: #fff; border-style: dashed; } .lp.s { background: #FFF1BF; } .lp.p { background: #FFCC00; }
.shot { border: .8mm solid #FFCC00; border-radius: 3mm; overflow: hidden; margin-bottom: 4mm; }
.shot img { width: 100%; display: block; }
table.fin { width: 100%; border-collapse: collapse; font-size: 22pt; margin-bottom: 5mm; }
table.fin td { padding: 1.6mm 1mm; border-bottom: .5mm solid #C8C8C8; font-weight: 600; }
table.fin td:last-child { text-align: right; white-space: nowrap; }
table.fin tr.tot td { border-top: 1mm solid #141414; border-bottom: none; font-weight: 800; }
.roi { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.big { border-radius: 4mm; border: 1.4mm solid #141414; text-align: center; padding: 4mm 2mm 3mm; background: #FFF6D6; }
.big.hl { background: #FFCC00; }
.big small { display: block; font-size: 17pt; font-weight: 800; text-transform: uppercase; line-height: 1.1; }
.big b { display: block; font-size: 66pt; font-weight: 800; line-height: 1.02; }
.big span { display: block; font-size: 17pt; font-weight: 600; }
.nota { font-size: 19pt; line-height: 1.2; color: #404040; margin-top: 4mm; font-weight: 600; }
.qr { display: flex; gap: 7mm; align-items: center; }
.qr img { width: 74mm; height: 74mm; border: 1mm solid #141414; border-radius: 3mm; background: #fff; flex: none; }
.qr p { font-size: 22pt; line-height: 1.25; }
.qr small { display: block; font-size: 17pt; color: #404040; margin-top: 2mm; }
.pie { background: #141414; color: #E6E6E6; border-radius: 6mm; padding: 4.5mm 12mm; font-size: 15pt; line-height: 1.3; font-weight: 500; flex: none; }
.pie b { color: #FFCC00; font-weight: 700; }
""".replace("__FONDO__", uri(A / "backgrounds" / "papel_arrugado.jpg"))


def cabecera() -> str:
    return f"""
<header class="cab"><div class="mano">{mano_svg()}</div>
  <div class="logos">
    <div class="tile upb"><img src="{uri(A / 'logos' / 'upb_logo_vertical_blanco.png')}" alt="UPB"></div>
    <div class="inst"><b>Universidad Pontificia Bolivariana, Seccional Montería</b>Facultad de Ingeniería Industrial ·
      Grupo de Investigación SILOGE · Hub Industrial Solution, HIS</div>
    <div class="tile his"><img src="{uri(A / 'logos' / 'logo_his_engranaje.png')}" alt="HIS"></div>
    <div class="tile siloge"><img src="{uri(A / 'logos' / 'logo_siloge.png')}" alt="SILOGE"></div>
  </div>
  <h1 class="titulo">{TITULO}</h1>
  <p class="sub">Hand Sing Kids: visión por computador y programación entera mixta, procesamiento 100 % local</p>
  <p class="equipo">Equipo XX: [integrantes, códigos y correos institucionales] · Docente asesor: M.Sc. Cristian Javier
    Cano Mogollón · Gestión Tecnológica, 2026-2</p>
</header>"""


def columna1() -> str:
    return f"""
<div class="card"><h2><span class="n">1</span>Problemática regional</h2>
  <div class="kpis k3">
    <div class="kpi"><b>{n(DANE['hog_internet_cor'], 1)} %</b><span>hogares de Córdoba con internet</span></div>
    <div class="kpi"><b>−{n(BRECHA, 1)}</b><span>puntos frente al promedio nacional</span></div>
    <div class="kpi"><b>{n(DANE['mon_3_12'] / 1000, 1)} mil</b><span>niños de 3 a 12 años en Montería</span></div>
  </div>
  <ul><li>Nivelación manual: 1,0 a 1,5 h por semana en cada aula*</li>
      <li>Papelería: $ 600.000 al año por aula*</li>
      <li>Una solución en la nube excluye a la mitad de los hogares</li></ul>
  <p class="fuente">DANE (2025; s. f.). *Equipo 13 (2026), dato de campo no verificado.</p>
</div>
<div class="card"><h2><span class="n">2</span>Árbol de problemas</h2>
  <div class="arbol">
    <div class="rot">EFECTOS</div>
    <div class="fila"><div class="caja e">Abandono y retroalimentación tardía</div><div class="caja e">Docentes sin datos para reforzar</div></div>
    <div class="caja p">Los niños aprenden las notas sin retroalimentación inmediata ni registro objetivo</div>
    <div class="fila"><div class="caja c">Atención de uno a muchos</div><div class="caja c">Evaluación manual, sin registro</div></div>
    <div class="rot">CAUSAS</div>
  </div>
  <div class="ods"><div class="od"><b>4</b><span>Educación de calidad</span></div>
    <div class="od"><b>9</b><span>Industria e innovación</span></div>
    <div class="od"><b>10</b><span>Menos desigualdad</span></div></div>
</div>
<div class="card"><h2><span class="n">3</span>Pregunta y objetivos</h2>
  <p class="pregunta">¿Puede un sistema local de reconocimiento de señas dar retroalimentación inmediata y registro objetivo
    del dominio de las notas a niños de 3 a 12 años?</p>
  <ul class="oe"><li><b>OE1</b> Diagnosticar la brecha y revisar la literatura</li>
      <li><b>OE2</b> Construir visión, gemelo digital y planificador</li>
      <li><b>OE3</b> Verificar el desempeño y estimar el ROI</li></ul>
</div>
<div class="card"><h2><span class="n">4</span>Estado del arte</h2>
  <div class="kpis k2">
    <div class="kpi"><b>15</b><span>estudios 2023 a 2026 con DOI verificado</span></div>
    <div class="kpi"><b>189</b><span>documentos en la matriz bibliográfica</span></div>
  </div>
  <div class="brecha"><p>Brecha: ningún estudio combina señas manuales, niños de 3 a 12 años, procesamiento local y
    adaptación interpretable.</p></div>
  <p class="fuente">Predominan el refuerzo profundo, los universitarios y el piano ({cita('075')}; {cita('038')}).</p>
</div>"""


def columna2() -> str:
    return f"""
<div class="card"><h2><span class="n">5</span>Procesos BPMN 2.0</h2>
  <div class="dia">{svg('poster_bpmn_as_is')}</div>
  <p class="cap">As-Is: 1 nivelación manual · 2 atención uno a uno · 3 reproceso · 4 registro en papel · 5 informe tardío</p>
  <p class="paso"><span>▼ To-Be con Hand Sing Kids</span></p>
  <div class="dia">{svg('poster_bpmn_to_be')}</div>
  <p class="cap">To-Be: reconocimiento en cada fotograma, registro automático y repaso programado</p>
</div>
<div class="card"><h2><span class="n">6</span>Flujo de datos (DFD)</h2>
  <div class="dia">{svg('poster_dfd0')}</div>
  <p class="cap">Nivel 0: sin entidades en la nube</p>
  <div class="dia" style="margin-top:3mm">{svg('poster_dfd1')}</div>
  <p class="cap">Nivel 1 simplificado (los niveles 1 y 2 completos están en el documento)</p>
</div>
<div class="card"><h2><span class="n">7</span>Gobernanza de datos</h2>
  <div class="chips">
    <div class="chip"><b>0</b>imágenes guardadas en disco</div>
    <div class="chip"><b>0</b>módulos de red en el código</div>
    <div class="chip"><b>{CAT['_resumen']['tablas']} · {CAT['_resumen']['columnas']}</b>tablas y campos en el diccionario</div>
    <div class="chip"><b>4 de 8</b>reglas de integridad impuestas por la base</div>
  </div>
  <div class="linaje"><div class="lp e">Cámara</div><div class="lp e">21 puntos</div><div class="lp e">Descriptor</div>
    <div class="lp s">Nota</div><div class="lp p">Intento</div><div class="lp p">Gemelo</div><div class="lp p">Decisión</div></div>
  <p class="cap">Linaje: efímero (punteado), de sesión y persistente. RBAC: niño, acudiente o docente (PIN propuesto) y sistema</p>
</div>"""


def columna3() -> str:
    return f"""
<div class="card oscura"><h2><span class="n">8</span>Prototipo funcional</h2>
  <div class="shot"><img src="{uri(A / 'capturas' / '05_aventura.png')}" alt="Mapa de aventura"></div>
  <div class="shot"><img src="{uri(A / 'capturas' / '11_ejercicio.png')}" alt="Ejercicio guiado"></div>
  <div class="kpis k4">
    <div class="kpi"><b>14</b><span>pantallas</span></div>
    <div class="kpi"><b>63</b><span>actividades</span></div>
    <div class="kpi"><b>8</b><span>suites de pruebas</span></div>
    <div class="kpi"><b>TRL 4</b><span>en laboratorio</span></div>
  </div>
  <p class="fuente">Python · PySide6 · MediaPipe · OpenCV · PuLP · SQLite</p>
</div>
<div class="card"><h2><span class="n">9</span>Retorno de la inversión</h2>
  <table class="fin">
    <tr><td>CAPEX (un aula)</td><td>{cop(TOT['capex'])}</td></tr>
    <tr><td>OPEX anual</td><td>{cop(TOT['opex'])}</td></tr>
    <tr><td>Beneficios brutos anuales</td><td>{cop(TOT['beneficios'])}</td></tr>
    <tr class="tot"><td>Beneficio neto anual</td><td>{cop(BASE['beneficio_neto'])}</td></tr>
  </table>
  <div class="roi">
    <div class="big hl"><small>ROI año 1 · 4 aulas</small><b>{n(INST['roi_pct'], 1)} %</b><span>guía: ≥ 30 %</span></div>
    <div class="big hl"><small>Payback · 4 aulas</small><b>{n(INST['payback_meses'], 1)}</b><span>meses (guía: ≤ 12)</span></div>
    <div class="big"><small>ROI · 1 aula</small><b>{n(BASE['roi_pct'], 1)} %</b></div>
    <div class="big"><small>Payback · 1 aula</small><b>{n(BASE['payback_meses'], 1)}</b><span>meses</span></div>
  </div>
  <p class="nota">Un aula sola no cumple la guía; la viabilidad depende de la escala.</p>
</div>
<div class="card"><h2><span class="n">10</span>Resultados y proyección</h2>
  <ul><li>{n(BENCH['total_ms']['media'], 1)} ms de cómputo por fotograma</li>
      <li>92 de cada 100 posturas que no son seña se rechazan</li>
      <li>96,9 % de acierto con ruido moderado</li>
      <li>Siguiente fase: piloto de 8 semanas con grupo de control</li></ul>
  <div class="qr" style="margin-top:auto;padding-top:5mm"><img src="{uri(A / 'qr_repositorio.svg')}" alt="QR">
    <p>Código, pruebas y documento<small>github.com/Lossinn/Musica_Hand</small></p></div>
</div>"""


def pie() -> str:
    return ("<b>Referencias.</b> DANE (2025), ENTIC Hogares 2024 · DANE (s. f.), proyecciones municipales 2020-2035 · "
            "Equipo 13 (2026), Proyecto Integrador II · Zhang et al. (2020), doi:10.48550/arXiv.2006.10214 · "
            f"{cita('075')}, doi:10.1007/s40745-026-00689-1 · {cita('038')}, doi:10.5216/mh.v26.85176. "
            "Cifras técnicas medidas en el código y en pruebas ejecutadas; las financieras dependen de supuestos "
            "declarados en el documento.")


def html() -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Póster científico 90 x 120 cm</title>
<style>{CSS}</style></head><body><div class="poster">
<div class="fondo"></div><div class="kraft"></div>
<img class="marca" src="{uri(A / 'logos' / 'logo_his_texto.png')}" alt="">
<img class="tira izq" src="{uri(A / 'backgrounds' / 'borde_amarillo_b.png')}" alt="">
<img class="tira der" src="{uri(A / 'backgrounds' / 'borde_amarillo_a.png')}" alt="">
{cabecera()}
<div class="franja"></div>
<main class="cuerpo"><section class="col">{columna1()}</section><section class="col">{columna2()}</section>
<section class="col">{columna3()}</section></main>
<footer class="pie">{pie()}</footer>
</div></body></html>"""


def construir() -> tuple[Path, Path]:
    out_html = ROOT / "_fuentes" / "poster.html"
    out_html.write_text(html(), encoding="utf-8")
    pdf = ROOT / "entrega_teams" / "03_Poster_Cientifico_90x120_Equipo_XX.pdf"
    render.pdf(out_html, pdf)
    return out_html, pdf


if __name__ == "__main__":
    h, p = construir()
    import pymupdf
    d = pymupdf.open(p)
    r = d[0].rect
    print("páginas:", len(d), "| tamaño:", round(r.width / 72 * 25.4), "x", round(r.height / 72 * 25.4), "mm")
    d[0].get_pixmap(dpi=22).save(ROOT / "recursos" / "_previews" / "poster.png")
