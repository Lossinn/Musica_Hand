"""Exporta los logotipos a PNG (300 DPI), hoja de escalas, paleta con contrastes WCAG y comparativa."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

import logos as L
import render

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "recursos" / "identidad_visual"
PNG = OUT / "png_300dpi"
PNG.mkdir(exist_ok=True)


def png_desde_svg(svg_path: Path, salida: Path, w: int, h: int, factor: float, transparente: bool):
    render.png(svg_path, salida, w, h, scale=factor, transparent=transparente)
    im = Image.open(salida)
    im.save(salida, dpi=(300, 300))
    return im.size


# 1) icono 2400 px (8 pulgadas a 300 DPI), lockups 3280 px de ancho
tam = {}
for k in "ABC":
    tam[f"icono_{k}"] = png_desde_svg(OUT / f"concepto_{k}_icono.svg", PNG / f"concepto_{k}_icono_2400px.png", 512, 512, 2400 / 512, True)
    tam[f"horizontal_{k}"] = png_desde_svg(OUT / f"concepto_{k}_horizontal.svg", PNG / f"concepto_{k}_horizontal_3280px.png", 1640, 520, 2.0, False)
    tam[f"horizontal_oscuro_{k}"] = png_desde_svg(OUT / f"concepto_{k}_horizontal_oscuro.svg", PNG / f"concepto_{k}_horizontal_oscuro_3280px.png", 1640, 520, 2.0, False)


# 2) contraste WCAG de la paleta
def lum(hexc: str) -> float:
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a: str, b: str) -> float:
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


PAL = [("Amarillo industrial", L.Y, "Color de marca; fondos de acento y tarjetas KPI"),
       ("Negro industrial", L.K, "Texto, marcos y fondo oscuro"),
       ("Gris claro", L.GL, "Fondos de tarjetas"),
       ("Gris oscuro", L.GD, "Subtítulos y texto secundario"),
       ("Verde azulado", L.T, "Acento de la interfaz de la aplicación (movimiento, sonido)")]
pares = [("Negro sobre amarillo", L.K, L.Y), ("Amarillo sobre negro", L.Y, L.K), ("Negro sobre gris claro", L.K, L.GL),
         ("Gris oscuro sobre blanco", L.GD, "#FFFFFF"), ("Verde azulado sobre blanco", L.T, "#FFFFFF"),
         ("Negro sobre verde azulado", L.K, L.T), ("Blanco sobre negro", "#FFFFFF", L.K)]
filas = "".join(
    f'<tr><td>{n}</td><td style="background:{b};color:{a};padding:6px 14px;font-weight:700">Aa 123</td><td>{contraste(a, b):.2f}:1</td>'
    f'<td>{"AAA" if contraste(a, b) >= 7 else "AA" if contraste(a, b) >= 4.5 else "solo texto grande (AA ≥ 3)" if contraste(a, b) >= 3 else "insuficiente"}</td></tr>'
    for n, a, b in pares)
sw = "".join(f'<div style="width:210px"><div style="height:90px;background:{c};border:1px solid #999;border-radius:8px"></div>'
             f'<b>{n}</b><br>{c}<br><small>{u}</small></div>' for n, c, u in PAL)
html = f"""<html><head><meta charset="utf-8"><style>body{{font-family:Arial,sans-serif;margin:28px;width:1260px;color:#141414}}
h2{{margin:0 0 12px}} table{{border-collapse:collapse;margin-top:12px}} td,th{{border-bottom:1px solid #ccc;padding:5px 14px;text-align:left;font-size:15px}}
.f{{display:flex;gap:18px;flex-wrap:wrap}}</style></head><body><h2>Paleta de Hand Sing Kids</h2><div class="f">{sw}</div>
<h2 style="margin-top:26px">Contraste (WCAG 2.1)</h2><table><tr><th>Par</th><th>Muestra</th><th>Razón</th><th>Nivel</th></tr>{filas}</table></body></html>"""
(OUT / "paleta.html").write_text(html, encoding="utf-8")
render.png(OUT / "paleta.html", OUT / "paleta_y_contraste.png", 1320, 720, 1.0)

# 3) hoja de escalas: cada icono a 16, 24, 32, 48, 64 y 128 px sobre fondo claro y oscuro
filas = ""
for k in "ABC":
    celdas = ""
    for bg in ("#fff", "#141414"):
        celdas += f'<div style="background:{bg};padding:14px;display:flex;gap:18px;align-items:flex-end;border:1px solid #ccc">' + "".join(
            f'<img src="concepto_{k}_icono.svg" width="{s}" height="{s}">' for s in (16, 24, 32, 48, 64, 128)) + "</div>"
    filas += f'<div style="display:flex;gap:16px;align-items:center;margin-bottom:14px"><b style="width:210px;font-size:17px">Concepto {k}: {L.NAMES[k]}</b>{celdas}</div>'
(OUT / "escalas.html").write_text(f'<html><body style="font-family:Arial;margin:24px;width:1400px">'
                                  f'<h2>Legibilidad a distintas escalas (px)</h2>{filas}</body></html>', encoding="utf-8")
render.png(OUT / "escalas.html", OUT / "escalas_legibilidad.png", 1460, 640, 1.0)

# 4) comparativa
cmp_ = "".join(
    f'<div style="background:#fff;border:1px solid #ccc;border-radius:10px;padding:16px;width:440px"><img src="concepto_{k}_icono.svg" width="200"><br>'
    f'<b style="font-size:20px">Concepto {k}: {L.NAMES[k]}</b><br><img src="concepto_{k}_horizontal.svg" width="400"></div>' for k in "ABC")
(OUT / "comparativa.html").write_text(f'<html><body style="font-family:Arial;margin:24px;background:#eee;width:1440px"><div style="display:flex;gap:22px">{cmp_}</div></body></html>', encoding="utf-8")
render.png(OUT / "comparativa.html", OUT / "comparativa_conceptos.png", 1490, 520, 1.0)

print(json.dumps({k: list(v) for k, v in tam.items()}, indent=1))
print({n: round(contraste(a, b), 2) for n, a, b in pares})
