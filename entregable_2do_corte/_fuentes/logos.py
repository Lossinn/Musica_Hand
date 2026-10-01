"""Tres conceptos de logotipo para Hand Sing Kids (SVG vectorial, texto a trazados).

Concepto A  «Mano-nota»      mano abierta con una corchea en la palma.
Concepto B  «Puntos de mano» esqueleto de 21 puntos (la salida real del detector
            MediaPipe, tomada de la calibración del proyecto) dentro de un visor.
Concepto C  «Nota-dedo»      corchea cuya plica es un dedo índice y cuya cabeza es un
            puño; arcos de movimiento a un lado.

Paleta: amarillo #FFCC00, negro #141414, gris claro #F5F5F5, gris oscuro #404040 y
un verde azulado #1FA99B que es el color de acento de la interfaz de la aplicación.
"""
from __future__ import annotations

import json
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = ROOT / "recursos" / "assets" / "fonts" / "Montserrat.ttf"
FIXTURE = ROOT.parent / "03_Codigo" / "HandSingKids7" / "tests" / "fixtures" / "calibracion_v1.json"

Y, K, GL, GD, T = "#FFCC00", "#141414", "#F5F5F5", "#404040", "#1FA99B"

_FONTS: dict[int, TTFont] = {}


def font(weight: int) -> TTFont:
    if weight not in _FONTS:
        f = TTFont(FONT_PATH)
        instancer.instantiateVariableFont(f, {"wght": weight}, inplace=True)
        _FONTS[weight] = f
    return _FONTS[weight]


def text_path(text: str, size: float, x: float, y: float, *, weight=800, tracking=0.0) -> tuple[str, float]:
    """Devuelve (d, ancho) con el texto convertido a trazados. `y` es la línea base."""
    f = font(weight)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    sc = size / upm
    cur, parts = x, []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cur, y)))
        parts.append(pen.getCommands())
        cur += f["hmtx"][g][0] * sc + tracking
    return " ".join(p for p in parts if p), cur - x - tracking


def svg_doc(w: int, h: int, body: str, *, bg: str | None = None, title="") -> str:
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}">{b}{body}</svg>')


# ============================================================ concepto A
def icon_a(ink=Y, bg=K, note=K) -> str:
    """Badge negro con mano amarilla y corchea en negativo."""
    fingers = "".join(
        f'<rect x="{x}" y="{y}" width="46" height="{h}" rx="23" fill="{ink}"/>'
        for x, y, h in ((136, 118, 200), (194, 88, 230), (252, 106, 212), (310, 152, 166)))
    return (
        f'<rect x="8" y="8" width="496" height="496" rx="116" fill="{bg}"/>'
        f'{fingers}'
        f'<rect x="132" y="262" width="228" height="170" rx="64" fill="{ink}"/>'
        f'<line x1="170" y1="392" x2="92" y2="300" stroke="{ink}" stroke-width="46" stroke-linecap="round"/>'
        # corchea en la palma
        f'<ellipse cx="236" cy="384" rx="30" ry="22" fill="{note}" transform="rotate(-22 236 384)"/>'
        f'<rect x="253" y="300" width="10" height="82" rx="3" fill="{note}"/>'
        f'<path d="M263,300 C286,304 300,318 300,342 C290,328 278,326 263,326 Z" fill="{note}"/>')


# ============================================================ concepto B
MP_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)]


def _landmarks() -> list[tuple[float, float]]:
    """Mano abierta esquemática con la topología de 21 puntos de MediaPipe Hands
    (0 muñeca; 1-4 pulgar; 5-8 índice; 9-12 corazón; 13-16 anular; 17-20 meñique)."""
    return [(256, 410),
            (208, 380), (170, 338), (146, 296), (126, 258),
            (212, 304), (200, 240), (194, 194), (190, 152),
            (252, 292), (254, 222), (256, 170), (258, 124),
            (292, 302), (306, 238), (314, 194), (322, 154),
            (326, 334), (350, 280), (362, 244), (372, 212)]


def icon_b(ink=Y, bg=K, node="#fff", accent=T) -> str:
    pts = _landmarks()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    box = 290.0
    sc = box / max(x1 - x0, y1 - y0)
    ox = 256 - (x1 - x0) * sc / 2
    oy = 258 - (y1 - y0) * sc / 2
    P = [((x - x0) * sc + ox, (y - y0) * sc + oy) for x, y in pts]
    lines = "".join(f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" '
                    f'stroke="{ink}" stroke-width="11" stroke-linecap="round"/>' for a, b in MP_EDGES)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{13 if i in (4, 8, 12, 16, 20) else 9}" '
                   f'fill="{accent if i == 8 else node}"/>' for i, (x, y) in enumerate(P))
    c = 4  # esquinas del visor
    L, R, TOP, BOT, s = 64, 448, 64, 448, 52
    corners = (f'<path d="M{L},{TOP + s} V{TOP} H{L + s} M{R - s},{TOP} H{R} V{TOP + s} '
               f'M{R},{BOT - s} V{BOT} H{R - s} M{L + s},{BOT} H{L} V{BOT - s}" fill="none" '
               f'stroke="{ink}" stroke-width="{c * 2.2:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<rect x="8" y="8" width="496" height="496" rx="116" fill="{bg}"/>{corners}{lines}{dots}')


# ============================================================ concepto C
def icon_c(bg=Y, ink=K, accent=T) -> str:
    """Corchea-dedo sobre fondo amarillo: plica = índice, cabeza = puño, arcos = movimiento."""
    return (
        f'<rect x="8" y="8" width="496" height="496" rx="116" fill="{bg}"/>'
        # plica: dedo índice
        f'<rect x="266" y="74" width="62" height="280" rx="31" fill="{ink}"/>'
        f'<path d="M281,116 Q297,100 313,116" fill="none" stroke="{bg}" stroke-width="7" stroke-linecap="round"/>'
        # cabeza: puño
        f'<ellipse cx="226" cy="368" rx="92" ry="70" fill="{ink}" transform="rotate(-18 226 368)"/>'
        f'<path d="M170,352 Q200,334 232,344 M176,382 Q206,364 240,374" fill="none" stroke="{bg}" '
        f'stroke-width="7" stroke-linecap="round" transform="rotate(-18 226 368)"/>'
        # bandera: pulgar
        f'<path d="M328,86 C330,150 424,160 410,256 C398,214 364,194 328,186 Z" fill="{ink}"/>'
        # arcos de movimiento
        f'<path d="M96,150 Q62,200 96,250 M60,128 Q8,200 60,272" fill="none" stroke="{accent}" '
        f'stroke-width="16" stroke-linecap="round" transform="translate(40 -6)"/>')


ICONS = {"A": icon_a, "B": icon_b, "C": icon_c}
NAMES = {"A": "Mano-nota", "B": "Puntos de mano", "C": "Nota-dedo"}


def lockup(concept: str, *, dark=False) -> str:
    """Logotipo horizontal: icono + 'Hand Sing Kids' + línea descriptiva. 1560 x 520."""
    txt = GL if dark else K
    sub = "#BDBDBD" if dark else GD
    icon = ICONS[concept]()
    d1, w1 = text_path("Hand Sing", 124, 0, 0, weight=800, tracking=-2)
    d2, w2 = text_path("Kids", 124, 0, 0, weight=800, tracking=-2)
    d3, _ = text_path("Aprende las notas con las manos", 36, 0, 0, weight=500, tracking=0.5)
    kx = 560 + w1 + 30
    kids_fill = Y if dark else K
    under = "" if dark else f'<rect x="{kx:.0f}" y="292" width="{w2 + 4:.0f}" height="13" rx="6.5" fill="{Y}"/>'
    body = (f'<g transform="translate(20 4)">{icon}</g>'
            f'<path transform="translate(560 262)" d="{d1}" fill="{txt}"/>'
            f'<path transform="translate({kx:.0f} 262)" d="{d2}" fill="{kids_fill}"/>'
            f'{under}'
            f'<path transform="translate(564 352)" d="{d3}" fill="{sub}"/>')
    return svg_doc(1640, 520, body, bg=(K if dark else "#fff"), title=f"Hand Sing Kids, concepto {concept}")


def icon_only(concept: str, *, bg=None) -> str:
    return svg_doc(512, 512, ICONS[concept](), bg=bg, title=f"Icono de Hand Sing Kids, concepto {concept}")


if __name__ == "__main__":
    out = ROOT / "recursos" / "identidad_visual"
    out.mkdir(exist_ok=True)
    for k in "ABC":
        (out / f"concepto_{k}_icono.svg").write_text(icon_only(k), encoding="utf-8")
        (out / f"concepto_{k}_horizontal.svg").write_text(lockup(k), encoding="utf-8")
        (out / f"concepto_{k}_horizontal_oscuro.svg").write_text(lockup(k, dark=True), encoding="utf-8")
        print("ok", k, NAMES[k])
