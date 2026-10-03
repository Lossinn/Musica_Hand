"""Capas de arte abstracto y tecnológico para los pósteres (SVG vectorial, unidades en mm).

Motivos: buses de circuito con giros de 45° y pads, ondas sonoras en cinta, anillos de radar con marcas,
constelaciones de la mano (21 puntos de MediaPipe) y retícula de puntos. Todo se genera con semilla fija, de
modo que cada regeneración produce la misma composición. Las capas van detrás de las tarjetas: se ven en los
márgenes, en los canales entre columnas y dentro de la cabecera oscura.
"""
from __future__ import annotations

import math
import random

import logos

AM = "#FFCC00"
NE = "#141414"


# ------------------------------------------------------------------ utilidades
def _poly(pts) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def _offset(pts, d):
    """Polilínea paralela a distancia d (unión en inglete), para trazar buses de varias pistas."""
    out = []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            ax, ay = pts[1][0] - x, pts[1][1] - y
            n = math.hypot(ax, ay); nx, ny = -ay / n, ax / n; k = 1.0
        elif i == len(pts) - 1:
            ax, ay = x - pts[i - 1][0], y - pts[i - 1][1]
            n = math.hypot(ax, ay); nx, ny = -ay / n, ax / n; k = 1.0
        else:
            a1 = (x - pts[i - 1][0], y - pts[i - 1][1]); a2 = (pts[i + 1][0] - x, pts[i + 1][1] - y)
            n1, n2 = math.hypot(*a1), math.hypot(*a2)
            m1 = (-a1[1] / n1, a1[0] / n1); m2 = (-a2[1] / n2, a2[0] / n2)
            bx, by = m1[0] + m2[0], m1[1] + m2[1]
            nb = math.hypot(bx, by) or 1.0
            nx, ny = bx / nb, by / nb
            k = 1.0 / max(0.5, nx * m1[0] + ny * m1[1])
        out.append((x + nx * d * k, y + ny * d * k))
    return out


DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def _ruta(rng, x, y, di, pasos, lmin, lmax):
    pts = [(x, y)]
    for _ in range(pasos):
        dx, dy = DIRS[di]
        f = 1 / math.sqrt(2) if dx and dy else 1.0
        L = rng.uniform(lmin, lmax)
        x, y = x + dx * L * f, y + dy * L * f
        pts.append((x, y))
        di = (di + rng.choice([-1, 0, 1])) % 8
    return pts


# ---------------------------------------------------------------------- motivos
def bus(rng, x, y, di, *, pistas=4, sep=3.2, pasos=4, lmin=18, lmax=60, color=NE, op=.2, sw=.55, pad=1.3,
        pad_fill="none", pad_color=None) -> str:
    """Bus de pistas paralelas que nace en (x, y) y termina en pads circulares."""
    base = _ruta(rng, x, y, di, pasos, lmin, lmax)
    pc = pad_color or color
    g = [f'<g opacity="{op}" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    for k in range(pistas):
        d = (k - (pistas - 1) / 2) * sep
        p = _offset(base, d)
        corte = rng.randint(max(2, len(p) - 2), len(p))   # pistas de largo distinto
        p = p[:corte]
        g.append(f'<polyline points="{_poly(p)}" stroke="{color}" stroke-width="{sw}"/>')
        ex, ey = p[-1]
        g.append(f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="{pad}" fill="{pad_fill}" stroke="{pc}" stroke-width="{sw}"/>')
    g.append("</g>")
    return "".join(g)


def anillos(cx, cy, r0, n, paso, *, color=NE, op=.14, sw=.5, marcas=True) -> str:
    """Anillos concéntricos de radar con trazos discontinuos y marcas cada 10°."""
    g = [f'<g opacity="{op}" fill="none" stroke="{color}">']
    for i in range(n):
        r = r0 + i * paso
        dash = ["", ' stroke-dasharray="1.2 2.4"', ' stroke-dasharray="14 4 2 4"'][i % 3]
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="{sw * (1.6 if i == n - 1 else 1)}"{dash}/>')
    if marcas:
        r = r0 + (n - 1) * paso
        for a in range(0, 360, 10):
            t = math.radians(a); L = 4 if a % 30 else 8
            x1, y1 = cx + r * math.cos(t), cy + r * math.sin(t)
            x2, y2 = cx + (r + L) * math.cos(t), cy + (r + L) * math.sin(t)
            g.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke-width="{sw}"/>')
    g.append("</g>")
    return "".join(g)


def onda(x0, x1, y0, amp, lam, *, lineas=7, color=NE, op=.16, sw=.5, fase=0.0) -> str:
    """Cinta de ondas sonoras: varias sinusoides desfasadas con envolvente suave."""
    g = [f'<g opacity="{op}" fill="none" stroke="{color}" stroke-width="{sw}">']
    for k in range(lineas):
        ph = fase + k * 0.45
        a = amp * (1 - 0.09 * k)
        pts = []
        x = x0
        while x <= x1:
            u = (x - x0) / (x1 - x0)
            env = math.sin(math.pi * u) ** 1.4
            pts.append((x, y0 + a * env * math.sin(2 * math.pi * x / lam + ph) * math.cos(2 * math.pi * x / (lam * 5.3))))
            x += 1.5
        g.append(f'<polyline points="{_poly(pts)}"/>')
    g.append("</g>")
    return "".join(g)


def barras(x0, y0, ancho, alto, n, *, color=AM, op=.25, seed=3) -> str:
    """Ecualizador: barras verticales de altura variable."""
    rng = random.Random(seed)
    w = ancho / n
    g = [f'<g opacity="{op}" fill="{color}">']
    for i in range(n):
        h = alto * (0.15 + 0.85 * abs(math.sin(i * 0.55)) * rng.uniform(.55, 1))
        g.append(f'<rect x="{x0 + i * w:.2f}" y="{y0 - h:.2f}" width="{w * .55:.2f}" height="{h:.2f}" rx="{w * .27:.2f}"/>')
    g.append("</g>")
    return "".join(g)


def constelacion(cx, cy, alto, *, rot=0, color=NE, punto=AM, op=.18, sw=.6, r=1.3) -> str:
    """Mano abierta de 21 puntos (topología MediaPipe) como red de nodos."""
    pts = logos._landmarks()
    mx = sum(p[0] for p in pts) / 21; my = sum(p[1] for p in pts) / 21
    s = alto / 286
    t = math.radians(rot)
    P = [(cx + ((x - mx) * math.cos(t) - (y - my) * math.sin(t)) * s,
          cy + ((x - mx) * math.sin(t) + (y - my) * math.cos(t)) * s) for x, y in pts]
    g = [f'<g opacity="{op}">']
    for a, b in logos.MP_EDGES:
        g.append(f'<line x1="{P[a][0]:.2f}" y1="{P[a][1]:.2f}" x2="{P[b][0]:.2f}" y2="{P[b][1]:.2f}" stroke="{color}" '
                 f'stroke-width="{sw}" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(P):
        rr = r * (1.5 if i in (4, 8, 12, 16, 20) else 1)
        g.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rr}" fill="{punto}" stroke="{color}" stroke-width="{sw * .8}"/>')
    g.append("</g>")
    return "".join(g)


def puntos(w, h, paso=7, r=.42, color=NE, op=.16) -> str:
    """Retícula de puntos con líneas discontinuas de extremo redondo (vectorial; un patrón SVG se rasteriza)."""
    filas = "".join(f'<line x1="{paso / 2}" y1="{y:.2f}" x2="{w}" y2="{y:.2f}"/>'
                    for y in [paso / 2 + k * paso for k in range(int(h / paso) + 1)])
    return (f'<g opacity="{op}" stroke="{color}" stroke-width="{2 * r}" stroke-linecap="round" '
            f'stroke-dasharray="0 {paso}">{filas}</g>')


def halo(cx, cy, r, color=AM, op=.30, pasos=8) -> str:
    """Resplandor radial con círculos concéntricos translúcidos (un degradado radial se rasteriza)."""
    a = 1 - (1 - op) ** (1 / pasos)
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * (k + 1) / pasos:.1f}" fill="{color}" opacity="{a:.3f}"/>'
                   for k in range(pasos))


def nodos(rng, x0, y0, x1, y1, n, *, color=NE, op=.18, sw=.45, dmax=60) -> str:
    """Red de nodos (malla de datos): puntos aleatorios unidos con su vecino más cercano."""
    P = [(rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n)]
    g = [f'<g opacity="{op}" stroke="{color}" stroke-width="{sw}">']
    for i, p in enumerate(P):
        cerca = sorted(range(n), key=lambda j: math.dist(p, P[j]))[1:3]
        for j in cerca:
            if j > i and math.dist(p, P[j]) < dmax:
                g.append(f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{P[j][0]:.2f}" y2="{P[j][1]:.2f}"/>')
    for x, y in P:
        g.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rng.choice([.8, 1.1, 1.6])}" fill="{color}" stroke="none"/>')
    g.append("</g>")
    return "".join(g)


def svg(w, h, cuerpo: str, defs: str = "", cls: str = "arte", par: str = "none") -> str:
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="{par}">'
            f'<defs>{defs}</defs>{cuerpo}</svg>')


# ------------------------------------------------------------- composiciones
def fondo_principal() -> str:
    """Póster principal (900 x 1200, fondo kraft): segunda capa en márgenes y canales."""
    rng = random.Random(11)
    d = ""
    c = [puntos(900, 1200, paso=11, r=.6, op=.22)]
    c.append(anillos(60, 1190, 30, 6, 14, op=.16))
    c.append(anillos(860, 300, 20, 5, 12, op=.13))
    c.append(onda(40, 860, 362, 9, 38, lineas=6, op=.22, sw=.55))
    for x, y, di in ((36, 400, 0), (36, 700, 7), (36, 980, 1), (864, 520, 4), (864, 860, 5), (864, 1100, 3)):
        c.append(bus(rng, x, y, di, pistas=4, pasos=3, lmin=10, lmax=22, op=.42, sw=.7, pad_fill=AM))
    c.append(constelacion(870, 1160, 90, rot=-28, op=.2))
    c.append(constelacion(28, 250, 70, rot=24, op=.18))
    return svg(900, 1200, "".join(c), d)


def cabecera_principal(w=800, h=330) -> str:
    """Arte para la cabecera oscura del póster principal (en mm del bloque)."""
    rng = random.Random(5)
    d = ""
    c = [puntos(w, h, paso=8, r=.5, color="#fff", op=.10)]
    c.append(onda(w * .38, w + 10, h * .22, 16, 34, lineas=8, color=AM, op=.16, sw=.6))
    c.append(anillos(w - 40, h * .62, 18, 5, 13, color=AM, op=.12))
    for x, y, di in ((w, 40, 4), (w, h - 30, 5), (w * .55, 0, 2)):
        c.append(bus(rng, x, y, di, pistas=5, pasos=3, lmin=16, lmax=40, color=AM, op=.14, pad_fill=NE))
    c.append(nodos(rng, w * .45, h * .05, w * .95, h * .5, 26, color="#fff", op=.10))
    return svg(w, h, "".join(c), d, "arte-cab", "xMaxYMid slice")


def fondo_variante() -> str:
    """Póster variante (fondo claro): manchas cálidas, retícula, circuitos, ondas y constelaciones."""
    rng = random.Random(23)
    d = ""
    c = ['<rect x="0" y="0" width="900" height="1200" fill="#F2EEE3"/>',
         halo(80, 420, 300, op=.30), halo(860, 1050, 340, op=.30),
         halo(840, 560, 240, NE, op=.08), halo(120, 1150, 220, NE, op=.08),
         puntos(900, 1200, paso=10, r=.6, op=.20)]
    c.append(anillos(450, 760, 40, 9, 28, op=.10))
    c.append(anillos(30, 1180, 26, 5, 14, op=.16))
    c.append(onda(20, 880, 290, 12, 44, lineas=8, op=.22, sw=.6))
    c.append(onda(20, 880, 1178, 7, 30, lineas=5, op=.20, sw=.5, fase=1.3))
    for x, y, di in ((18, 380, 0), (18, 620, 7), (18, 900, 1), (882, 460, 4), (882, 740, 3), (882, 1000, 5),
                     (450, 1192, 6)):
        c.append(bus(rng, x, y, di, pistas=4, pasos=3, lmin=8, lmax=18, op=.32, pad_fill=AM))
    c.append(constelacion(120, 760, 260, rot=-14, op=.07, sw=1.2, r=2.4))
    c.append(constelacion(780, 400, 230, rot=18, op=.07, sw=1.2, r=2.4))
    c.append(nodos(rng, 380, 560, 520, 1100, 30, op=.12))
    return svg(900, 1200, "".join(c), d)


def cabecera_variante(w=832, h=300) -> str:
    rng = random.Random(9)
    d = ""
    c = [puntos(w, h, paso=8, r=.5, color="#fff", op=.10)]
    c.append(onda(w * .30, w - 120, h * .74, 12, 30, lineas=8, color=AM, op=.14, sw=.6))
    c.append(barras(w * .30, h - 2, w * .4, 26, 70, op=.16))
    c.append(anillos(w * .63, h * .25, 14, 5, 12, color=AM, op=.10))
    for x, y, di in ((w * .2, 0, 1), (w * .75, h, 7), (w, h * .5, 4)):
        c.append(bus(rng, x, y, di, pistas=5, pasos=3, lmin=14, lmax=36, color=AM, op=.14, pad_fill=NE))
    c.append(nodos(rng, w * .55, h * .1, w * .8, h * .9, 22, color="#fff", op=.10))
    return svg(w, h, "".join(c), d, "arte-cab", "xMaxYMid slice")


def esquina(color=NE, op=.09, seed=2) -> str:
    """Motivo de esquina de las tarjetas (SVG en línea, vectorial): bus de circuito y anillos."""
    rng = random.Random(seed)
    c = [anillos(78, 52, 6, 4, 6, color=color, op=1, sw=.35, marcas=False)]
    c.append(bus(rng, 80, 30, 4, pistas=5, sep=2.6, pasos=3, lmin=8, lmax=16, color=color, op=1, sw=.4, pad=1))
    c.append(bus(rng, 60, 60, 5, pistas=3, sep=2.6, pasos=2, lmin=8, lmax=14, color=color, op=1, sw=.4, pad=1))
    return (f'<svg class="esq-card" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 60">'
            f'<g opacity="{op}">{"".join(c)}</g></svg>')


def firma(w=400, h=120) -> str:
    """Firma visual de Hand Sing Kids: mano de 21 puntos sobre radar, ondas sonoras y ecualizador."""
    rng = random.Random(31)
    c = [anillos(w * .5, h * .5, 10, 6, 9, op=.22, sw=.6)]
    c.append(onda(0, w, h * .5, h * .28, 26, lineas=7, op=.35, sw=.7))
    c.append(barras(w * .05, h * .97, w * .9, h * .22, 90, op=.45))
    c.append(nodos(rng, 0, 0, w * .3, h, 18, op=.25))
    c.append(nodos(rng, w * .7, 0, w, h, 18, op=.25))
    c.append(constelacion(w * .5, h * .5, h * .78, op=.95, sw=1.1, r=2.0))
    return svg(w, h, "".join(c), cls="firma-svg", par="xMidYMid meet")
