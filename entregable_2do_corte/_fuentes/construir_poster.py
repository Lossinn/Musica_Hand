"""Póster científico 90 x 120 cm (vertical) en HTML/CSS -> PDF con Microsoft Edge.

Identidad del evento HIS: amarillo industrial #FFCC00, negro mate #141414, grises, cartón corrugado,
tiras amarillas rasgadas y marca de agua HIS. Sobre esa base se añaden franjas de seguridad industrial,
paneles tipo etiqueta, cinta adhesiva y un esqueleto de mano (los 21 puntos del detector).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datos import BASE, BENCH, DANE, DOIS, INST, TOT, cita, cop, n, pct  # noqa: E402
import doc_base  # noqa: E402
import logos  # noqa: E402
import render  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "recursos" / "assets"
D = ROOT / "recursos" / "diagramas"


def uri(p: Path) -> str:
    return p.resolve().as_uri()


def svg(nombre: str) -> str:
    s = (D / f"{nombre}.svg").read_text(encoding="utf-8")
    return s.replace(' width="', ' data-w="', 1).replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)


def mano_svg() -> str:
    """Esqueleto de mano abierta (21 puntos, topología de MediaPipe) para la cabecera."""
    pts = logos._landmarks()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    ln = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="#FFCC00" stroke-width="7" stroke-linecap="round"/>'
                 for a, b in logos.MP_EDGES)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{10 if i in (4, 8, 12, 16, 20) else 7}" fill="#fff"/>' for i, (x, y) in enumerate(pts))
    return f'<svg viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" xmlns="http://www.w3.org/2000/svg">{ln}{dots}</svg>'


TITULO = ("Reconocimiento de señas manuales y planificación adaptativa de la práctica para la enseñanza de notas "
          "musicales a niños de 3 a 12 años en Montería, Córdoba, 2026")

CSS = doc_base.FONT_FACE + f"""
@page {{ size: 900mm 1200mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 900mm; height: 1200mm; }}
body {{ font-family: 'Montserrat', Helvetica, Arial, sans-serif; color: #141414; }}
.poster {{ position: relative; width: 900mm; height: 1200mm; overflow: hidden; background: #B98E52; }}
.corrugado {{ position: absolute; inset: 0; background:
  repeating-linear-gradient(90deg, rgba(70,42,10,.34) 0 1.6mm, rgba(255,226,170,.26) 1.6mm 3.6mm, rgba(70,42,10,.14) 3.6mm 5.6mm, rgba(255,226,170,.10) 5.6mm 7mm),
  linear-gradient(180deg, #C69A5C, #B98E52 50%, #C29656); }}
.papel {{ position: absolute; inset: 0; background: url('{uri(A / 'backgrounds' / 'papel_arrugado.jpg')}') center/cover; opacity: .30; mix-blend-mode: multiply; }}
.marca {{ position: absolute; left: 50%; top: 53%; width: 700mm; transform: translate(-50%, -50%); opacity: .07; }}
.engranaje {{ position: absolute; width: 330mm; opacity: .10; }}
.tira {{ position: absolute; top: 0; height: 1200mm; }}
.tira.izq {{ left: 0; width: 36mm; }}
.tira.der {{ right: 0; width: 36mm; }}
.cab {{ position: absolute; left: 52mm; right: 52mm; top: 26mm; height: 198mm; background: #141414; border-radius: 8mm; padding: 13mm 18mm; color: #fff; overflow: hidden; box-shadow: 0 3mm 6mm rgba(0,0,0,.35); }}
.cab .mano {{ position: absolute; right: 8mm; bottom: -6mm; width: 118mm; opacity: .20; }}
.cab .trama {{ position: absolute; inset: 0; background: repeating-linear-gradient(135deg, rgba(255,204,0,.07) 0 3mm, transparent 3mm 9mm); }}
.logos {{ position: relative; display: flex; gap: 12mm; align-items: center; justify-content: space-between; height: 50mm; }}
.logo {{ background: #fff; border-radius: 6mm; height: 50mm; padding: 4mm 8mm; display: flex; align-items: center; justify-content: center; }}
.logo.upb {{ background: #1D1D1B; padding: 0; overflow: hidden; border: .8mm solid #FFCC00; }}
.logo.upb img {{ height: 50mm; }}
.logo img {{ height: 42mm; width: auto; display: block; }}
.logo.vacio {{ border: 1.6mm dashed #888; color: #555; font-size: 15pt; font-weight: 700; text-align: center; line-height: 1.15; width: 150mm; }}
h1.titulo {{ position: relative; margin-top: 8mm; color: #FFCC00; font-weight: 800; text-transform: uppercase; font-size: 54pt; line-height: 1.1; letter-spacing: .2pt; }}
.sub {{ position: relative; margin-top: 5mm; font-size: 28pt; font-weight: 600; line-height: 1.2; color: #fff; }}
.equipo {{ position: relative; margin-top: 4mm; font-size: 20pt; color: #D6D6D6; font-weight: 500; line-height: 1.3; }}
.franja {{ position: absolute; left: 52mm; right: 52mm; height: 11mm; border-radius: 2mm; background: repeating-linear-gradient(135deg, #FFCC00 0 9mm, #141414 9mm 18mm); }}
.cols {{ position: absolute; left: 52mm; right: 52mm; top: 250mm; bottom: 72mm; display: grid; grid-template-columns: .93fr 1.04fr .93fr; gap: 14mm; }}
.col {{ display: flex; flex-direction: column; gap: 10mm; min-width: 0; }}
.card {{ background: rgba(255,255,255,.96); border-radius: 4mm; padding: 0 10mm 10mm 10mm; position: relative; box-shadow: 0 2mm 4mm rgba(60,35,5,.35); border-bottom: 3mm solid #141414; }}
.card.oscura {{ background: #1c1c1c; color: #fff; }}
.card h2 {{ margin: 0 -10mm 7mm -10mm; padding: 3.5mm 10mm; background: #141414; color: #FFCC00; border-radius: 4mm 4mm 0 0; font-size: 31pt; font-weight: 800; text-transform: uppercase; line-height: 1.08; letter-spacing: .2pt; display: flex; align-items: center; }}
.card.oscura h2 {{ background: #FFCC00; color: #141414; }}
h2 .n {{ flex: none; display: inline-block; background: #FFCC00; color: #141414; border-radius: 50%; width: 13mm; height: 13mm; text-align: center; line-height: 13mm; margin-right: 4mm; font-size: 24pt; }}
.card.oscura h2 .n {{ background: #141414; color: #FFCC00; }}
.cinta {{ position: absolute; top: -5mm; right: 14mm; width: 34mm; height: 11mm; background: rgba(255,204,0,.85); transform: rotate(4deg); box-shadow: 0 .6mm 1.4mm rgba(0,0,0,.25); z-index: 2; }}
p, li {{ font-size: 27pt; line-height: 1.26; font-weight: 500; }}
ul {{ list-style: none; }}
li {{ padding-left: 9mm; position: relative; margin-bottom: 3mm; }}
li::before {{ content: ''; position: absolute; left: 0; top: 4.8mm; width: 4.5mm; height: 4.5mm; background: #FFCC00; border: .8mm solid #141414; border-radius: 1mm; }}
.card.oscura li::before {{ border-color: #FFCC00; }}
.fuente {{ font-size: 16pt; color: #555; margin-top: 3mm; line-height: 1.2; }}
.kpis {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5mm; margin-bottom: 5mm; }}
.kpi {{ background: #F5F5F5; border-radius: 4mm; padding: 4mm 3mm; text-align: center; border-top: 2.4mm solid #FFCC00; }}
.kpi b {{ display: block; font-size: 42pt; font-weight: 800; line-height: 1; }}
.kpi span {{ display: block; font-size: 16pt; line-height: 1.15; margin-top: 2mm; font-weight: 500; color: #404040; }}
.arbol {{ display: grid; gap: 4mm; }}
.fila {{ display: grid; gap: 4mm; grid-template-columns: 1fr 1fr; }}
.caja {{ background: #F5F5F5; border: .9mm solid #141414; border-radius: 3mm; padding: 3mm 3.5mm; font-size: 18pt; line-height: 1.18; text-align: center; font-weight: 500; }}
.caja.centro {{ background: #FFCC00; font-weight: 700; font-size: 20pt; }}
.flecha {{ text-align: center; font-size: 20pt; line-height: .6; font-weight: 800; }}
.ods {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; }}
.od {{ background: #141414; color: #fff; border-radius: 3mm; padding: 3mm 2mm; text-align: center; }}
.od b {{ display: block; font-size: 36pt; color: #FFCC00; font-weight: 800; line-height: 1; }}
.od span {{ display: block; font-size: 14.5pt; line-height: 1.15; margin-top: 1mm; font-weight: 500; }}
.brecha {{ background: #FFCC00; border-radius: 4mm; padding: 5mm 6mm; margin-top: 4mm; border: 1.2mm solid #141414; }}
.brecha p {{ font-size: 25pt; font-weight: 700; }}
.dia {{ background: #fff; border: .7mm solid #BBB; border-radius: 3mm; padding: 1.2mm; }}
.leyenda {{ font-size: 18pt; line-height: 1.15; color: #404040; margin: 1.5mm 0 3mm 0; font-weight: 500; }}
table.var {{ width: 100%; border-collapse: collapse; font-size: 19pt; margin-bottom: 4mm; }}
table.var td, table.var th {{ border-bottom: .5mm solid #BBB; padding: 1.6mm 2mm; text-align: left; vertical-align: top; line-height: 1.15; font-weight: 500; }}
table.var th {{ border-bottom: 1mm solid #141414; font-weight: 700; }}
.linaje {{ display: flex; gap: 1.6mm; align-items: stretch; margin: 2mm 0 4mm 0; }}
.paso {{ flex: 1; font-size: 15pt; line-height: 1.12; text-align: center; padding: 2.5mm 1mm; border-radius: 2.5mm; border: .7mm solid #141414; font-weight: 600; }}
.paso.e {{ background: #fff; border-style: dashed; }} .paso.s {{ background: #FFF1BF; }} .paso.p {{ background: #FFCC00; }}
.chips {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-bottom: 3mm; }}
.chip {{ background: #F5F5F5; border-radius: 3mm; padding: 3mm 3.5mm; font-size: 18pt; line-height: 1.15; font-weight: 500; border-left: 2.4mm solid #141414; }}
.chip b {{ font-size: 25pt; display: block; font-weight: 800; line-height: 1.05; }}
.shot {{ border: .8mm solid #FFCC00; border-radius: 3mm; overflow: hidden; margin-bottom: 4mm; background: #fff; }}
.shot img {{ width: 100%; display: block; }}
.stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 3mm; }}
.stat {{ background: #FFCC00; color: #141414; border-radius: 3mm; padding: 3mm 1mm; text-align: center; }}
.stat b {{ display: block; font-size: 26pt; font-weight: 800; line-height: 1; }}
.stat span {{ display: block; font-size: 13pt; line-height: 1.1; margin-top: 1mm; font-weight: 600; }}
table.fin {{ width: 100%; border-collapse: collapse; font-size: 20pt; margin-bottom: 5mm; }}
table.fin td {{ padding: 1.8mm 2mm; border-bottom: .5mm solid #BBB; font-weight: 500; }}
table.fin td:last-child {{ text-align: right; white-space: nowrap; }}
table.fin tr.tot td {{ border-top: 1mm solid #141414; font-weight: 700; }}
.kpi-fin {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; margin-bottom: 4mm; }}
.big {{ background: #FFCC00; border-radius: 5mm; border: 1.4mm solid #141414; text-align: center; padding: 5mm 3mm 4mm; }}
.big.sec {{ background: #141414; color: #FFCC00; }}
.big small {{ display: block; font-size: 17pt; font-weight: 700; text-transform: uppercase; letter-spacing: .3pt; line-height: 1.1; }}
.big b {{ display: block; font-size: 62pt; font-weight: 800; line-height: 1.05; }}
.big.sec b {{ font-size: 52pt; }}
.big span {{ display: block; font-size: 16pt; font-weight: 600; }}
.nota {{ font-size: 18.5pt; line-height: 1.22; color: #404040; margin-top: 4mm; font-weight: 500; }}
.qr {{ display: flex; gap: 7mm; align-items: center; }}
.qr img {{ width: 70mm; height: 70mm; border: 1mm solid #141414; border-radius: 3mm; background: #fff; }}
.qr p {{ font-size: 20pt; line-height: 1.22; }}
.pie {{ position: absolute; left: 52mm; right: 52mm; bottom: 12mm; height: 42mm; background: #141414; color: #E6E6E6; border-radius: 6mm; padding: 5mm 12mm; font-size: 14pt; line-height: 1.28; font-weight: 500; }}
.pie b {{ color: #FFCC00; font-weight: 700; }}
"""


def logos_html() -> str:
    upb = A / "logos" / "upb_logo_vertical_blanco.png"
    hsk = ROOT / "recursos" / "identidad_visual" / "concepto_A_icono.svg"
    partes = []
    if upb.exists():
        partes.append(f'<div class="logo upb"><img src="{uri(upb)}" alt="UPB"></div>')
    else:
        partes.append('<div class="logo vacio">ESCUDO UPB<br>(insertar assets/logos/upb_30a.png)</div>')
    partes.append(f'<div class="logo"><img src="{uri(A / "logos" / "logo_his_engranaje.png")}" alt="HIS"></div>')
    partes.append(f'<div class="logo"><img src="{uri(A / "logos" / "logo_siloge.png")}" alt="SILOGE"></div>')
    partes.append(f'<div class="logo"><img src="{uri(hsk)}" alt="Hand Sing Kids"></div>')
    return "".join(partes)


def html() -> str:
    cinta = '<div class="cinta"></div>'
    c1 = f"""
<div class="card">{cinta}<h2><span class="n">1</span>Problemática regional</h2>
  <div class="kpis">
    <div class="kpi"><b>{n(DANE['hog_internet_cor'], 1)} %</b><span>de los hogares de Córdoba con internet (2024)</span></div>
    <div class="kpi"><b>−{n(DANE['hog_internet_nal'] - DANE['hog_internet_cor'], 1)}</b><span>puntos frente al {n(DANE['hog_internet_nal'], 1)} % nacional</span></div>
    <div class="kpi"><b>{n(DANE['mon_5_9'] + DANE['mon_10_14'])}</b><span>niños de 5 a 14 años en Montería (2026)</span></div>
  </div>
  <ul><li>En aulas de Montería y Cereté: nivelación manual de 1,0 a 1,5 h por semana y $ 600.000 al año en papelería por aula (estudio previo, no verificado).</li>
  <li>Una solución en la nube deja fuera a más de la mitad de los hogares de Córdoba.</li></ul>
  <p class="fuente">Fuentes: DANE, ENTIC Hogares 2024 y proyecciones 2026; Equipo 13 (2026), caracterización de campo.</p>
</div>
<div class="card"><h2><span class="n">2</span>Árbol de problemas</h2>
  <div class="arbol">
    <div class="fila"><div class="caja">Abandono y retroalimentación tardía</div><div class="caja">Docentes sin datos objetivos</div></div>
    <div class="flecha">▲ ▲</div>
    <div class="caja centro">Niños de Montería aprenden las notas musicales sin retroalimentación individual inmediata ni registro objetivo</div>
    <div class="flecha">▲ ▲</div>
    <div class="fila"><div class="caja">Atención 1:N y evaluación manual</div><div class="caja">Conectividad: {n(DANE['hog_internet_cor'], 1)} % de hogares con internet</div></div>
  </div>
  <div class="ods" style="margin-top:6mm">
    <div class="od"><b>4</b><span>Educación de calidad</span></div>
    <div class="od"><b>9</b><span>Industria e innovación</span></div>
    <div class="od"><b>10</b><span>Reducción de desigualdades</span></div>
  </div>
</div>
<div class="card"><h2><span class="n">3</span>Pregunta y objetivos</h2>
  <p style="font-style:italic;margin-bottom:4mm">¿En qué medida un sistema local de reconocimiento de señas y planificación adaptativa ofrece retroalimentación inmediata y registro objetivo del dominio de las notas en niños de 3 a 12 años?</p>
  <ul>
    <li>General: diseñar, construir y verificar el prototipo y evaluar su viabilidad financiera.</li>
    <li>Diagnosticar la brecha y revisar la literatura.</li>
    <li>Construir visión, gemelo digital, planificador y gobernanza local.</li>
    <li>Verificar el desempeño y estimar el ROI.</li>
  </ul>
</div>
<div class="card"><h2><span class="n">4</span>Estado del arte</h2>
  <ul><li>15 estudios (2023 a 2026) con DOI verificado en Crossref.</li>
  <li>Predominan el refuerzo profundo, los universitarios y el piano.</li></ul>
  <div class="brecha"><p>Brecha: no se identificó un sistema con señas manuales, niños de 3 a 12 años, procesamiento local y adaptación interpretable.</p></div>
</div>"""

    c2 = f"""
<div class="card">{cinta}<h2><span class="n">5</span>Procesos BPMN 2.0</h2>
  <div class="dia">{svg('poster_bpmn_as_is')}</div>
  <p class="leyenda">As-Is: 1 atención 1:N · 2 registro manual · 3 informe tardío.</p>
  <div class="dia">{svg('poster_bpmn_to_be')}</div>
  <p class="leyenda">To-Be: reconocimiento inmediato, registro en SQLite y repaso programado.</p>
</div>
<div class="card"><h2><span class="n">6</span>Flujo de datos (DFD)</h2>
  <div class="dia">{svg('poster_dfd0')}</div>
  <p class="leyenda">Nivel 0: sin entidades en la nube.</p>
  <div class="dia">{svg('poster_dfd1')}</div>
  <p class="leyenda">Nivel 1: siete procesos y seis almacenes (D1 a D6).</p>
</div>
<div class="card"><h2><span class="n">7</span>Gobernanza de datos</h2>
  <table class="var"><tr><th>Variable</th><th>Tipo</th><th>Significado</th></tr>
    <tr><td>mastery</td><td>REAL [0,1]</td><td>Dominio por nota</td></tr>
    <tr><td>confidence</td><td>REAL [0,1]</td><td>Confianza del reconocedor</td></tr>
    <tr><td>reaction_ms</td><td>INTEGER</td><td>Tiempo de reacción</td></tr>
  </table>
  <div class="linaje"><div class="paso e">Cámara<br>RAM</div><div class="paso e">21 puntos<br>RAM</div><div class="paso e">120 comp.<br>RAM</div><div class="paso s">Nota<br>sesión</div><div class="paso p">Intento<br>SQLite</div><div class="paso p">Gemelo<br>SQLite</div></div>
  <p class="leyenda">Linaje: efímero (línea punteada), de sesión y persistente.</p>
  <div class="chips">
    <div class="chip"><b>0</b>imágenes guardadas en disco</div>
    <div class="chip"><b>0</b>módulos de red en el código</div>
    <div class="chip"><b>4 de 8</b>reglas de integridad impuestas; 16 CHECK propuestas y probadas</div>
    <div class="chip"><b>{n(BENCH['total_ms']['media'], 1)} ms</b>por fotograma (cómputo)</div>
  </div>
</div>"""

    c3 = f"""
<div class="card oscura">{cinta}<h2><span class="n">8</span>Prototipo funcional</h2>
  <div class="shot"><img src="{uri(A / 'capturas' / '05_aventura.png')}" alt="Mapa de aventura"></div>
  <div class="shot"><img src="{uri(A / 'capturas' / '11_ejercicio.png')}" alt="Ejercicio"></div>
  <div class="stats">
    <div class="stat"><b>14</b><span>pantallas</span></div>
    <div class="stat"><b>63</b><span>actividades, 17 logros</span></div>
    <div class="stat"><b>8/8</b><span>suites de pruebas</span></div>
    <div class="stat"><b>TRL 4</b><span>validado en banco</span></div>
  </div>
</div>
<div class="card"><h2><span class="n">9</span>Retorno de la inversión</h2>
  <table class="fin">
    <tr><td>Inversión inicial (CAPEX)</td><td>{cop(TOT['capex'])}</td></tr>
    <tr><td>Costos anuales (OPEX)</td><td>{cop(TOT['opex'])}</td></tr>
    <tr><td>Beneficios brutos anuales</td><td>{cop(TOT['beneficios'])}</td></tr>
    <tr class="tot"><td>Beneficio neto anual</td><td>{cop(BASE['beneficio_neto'])}</td></tr>
  </table>
  <div class="kpi-fin">
    <div class="big"><small>ROI año 1 · 1 aula</small><b>{n(BASE['roi_pct'], 1)} %</b><span>meta de la guía: ≥ 30 %</span></div>
    <div class="big"><small>Payback · 1 aula</small><b>{n(BASE['payback_meses'], 1)}</b><span>meses (guía: ≤ 12)</span></div>
    <div class="big sec"><small>ROI · institución, 4 aulas</small><b>{n(INST['roi_pct'], 1)} %</b></div>
    <div class="big sec"><small>Payback · 4 aulas</small><b>{n(INST['payback_meses'], 1)}</b><span>meses</span></div>
  </div>
  <p class="nota">Un aula no se paga en 12 meses: la rentabilidad exige escala. Insumos de campo del estudio previo y supuestos por validar en un piloto.</p>
</div>
<div class="card"><h2><span class="n">10</span>Escalabilidad y proyección</h2>
  <ul><li>El mismo software se replica en más aulas e instituciones de Córdoba, sin nube.</li>
  <li>Siguiente fase: piloto con grupo de control, PIN de adulto y respaldo.</li>
  <li>Con 4 aulas por institución el ROI supera el 30 % exigido.</li></ul>
</div>
<div class="card"><h2>Más información</h2>
  <div class="qr"><img src="{uri(A / 'qr_repositorio.svg')}" alt="QR"><p>Escanee para abrir el repositorio del proyecto en GitHub.<br><span style="font-size:13pt;color:#404040">github.com/Lossinn/Musica_Hand</span></p></div>
</div>"""

    refs = "; ".join(f"{cita(i)}, doi:{DOIS[i]['doi']}" for i in ("203", "075", "186", "220", "002"))
    pie = (f"<b>Fuentes.</b> DANE (2025), ENTIC Hogares 2024 · Equipo 13 (2026), Proyecto Integrador II · Zhang et al. (2020), doi:10.48550/arXiv.2006.10214 · {refs}. "
           "Cifras técnicas verificadas en el código y en pruebas ejecutadas; las financieras dependen de supuestos.")
    eng = uri(A / "logos" / "logo_his_engranaje.png")
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Póster científico 90 x 120 cm</title><style>{CSS}</style></head>
<body><div class="poster">
<div class="corrugado"></div><div class="papel"></div>
<img class="marca" src="{uri(A / 'logos' / 'logo_his_texto.png')}" alt="">
<img class="engranaje" style="left:-110mm;top:640mm" src="{eng}" alt=""><img class="engranaje" style="right:-120mm;top:980mm" src="{eng}" alt="">
<img class="tira izq" src="{uri(A / 'backgrounds' / 'borde_amarillo_b.png')}" alt=""><img class="tira der" src="{uri(A / 'backgrounds' / 'borde_amarillo_a.png')}" alt="">
<header class="cab"><div class="trama"></div><div class="mano">{mano_svg()}</div>
<div class="logos">{logos_html()}</div>
<h1 class="titulo">{TITULO}</h1>
<p class="sub">Hand Sing Kids v2.0 · Empresa de Base Tecnológica · Gestión Tecnológica, 2026-2</p>
<p class="equipo">Equipo XX: [integrantes, códigos y correos] · Docente: M.Sc. Cristian Javier Cano Mogollón · Facultad de Ingeniería Industrial, Semillero SILOGE, Universidad Pontificia Bolivariana, Seccional Montería</p></header>
<div class="franja" style="top:232mm"></div>
<main class="cols"><section class="col">{c1}</section><section class="col">{c2}</section><section class="col">{c3}</section></main>
<div class="franja" style="bottom:56mm"></div>
<footer class="pie">{pie}</footer>
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
