"""Reverso infantil del póster (900 × 1200 mm): cómo funciona Hand Sing Kids, contado a un niño de 5 años.

Todo es vectorial (SVG en milímetros) salvo las tarjetas de señas y los logos, que son los archivos
oficiales del proyecto. Kiki se redibuja con la misma geometría de `ui/widgets/mascot.py` (QPainter),
añadiendo solo luz: degradados suaves, brillos en los ojos y sombra de contacto.

Salida:
    _fuentes/poster_ninos.html
    entrega_teams/03b_Poster_Reverso_Ninos_90x120_Equipo_XX.pdf
    entrega_teams/03b_Poster_Reverso_Ninos_90x120_Equipo_XX.png
    recursos/_previews/poster_ninos.png
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import logos  # noqa: E402
import render  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "recursos" / "assets"
APP = ROOT.parents[1] / "Hand_kid_Anexoo" / "HandSingKids7" / "handsingkids" / "ui" / "assets" / "gestos"
SENAS = A / "senas_hd"
OUT_DIR = ROOT / "entrega_teams"
NOMBRE = "03b_Poster_Reverso_Ninos_90x120_Equipo_XX"

W, H = 900, 1200

# Paleta de marca (manual de marca, cromestesia de la escala)
INK = "#241A0B"
INK2 = "#6B5B47"
CREAM = "#FFF8F4"
NOTAS = [  # código, nombre, color, bisel
    ("DO3", "Do", "#FF6B8B", "#D94263"),
    ("RE3", "Re", "#FF9F1C", "#C97400"),
    ("MI3", "Mi", "#FFD13B", "#D8A50B"),
    ("FA3", "Fa", "#2EC4B6", "#1E8F85"),
    ("SOL3", "Sol", "#38B6FF", "#1C88C7"),
    ("LA3", "La", "#7A5CFA", "#5638C4"),
    ("SI3", "Si", "#C94FD0", "#9B28A2"),
    ("DO4", "Do agudo", "#FF4F7B", "#C8214C"),
]
C = {c: (col, bev) for c, _, col, bev in NOTAS}

# Kiki (mascot.py)
VERDE, VERDE_OSCURO, VERDE_CLARO, PANZA, CRESTA = "#5FBF6A", "#3D9450", "#8FDC94", "#DFF5D8", "#F2A33C"


def uri(p: Path) -> str:
    return p.resolve().as_uri()


# ------------------------------------------------------------------ recursos
def preparar_senas() -> None:
    """Tarjetas oficiales a 3× con remuestreo Lanczos: bordes limpios al imprimir a 90 cm."""
    SENAS.mkdir(parents=True, exist_ok=True)
    for code, *_ in NOTAS:
        src = APP / f"{code}.png"
        dst = SENAS / f"{code}.png"
        if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
            continue
        im = Image.open(src).convert("RGBA")
        im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        im.save(dst, optimize=True)


def preparar_grano() -> Path:
    p = A / "backgrounds" / "grano_papel.png"
    if not p.exists():
        rng = np.random.default_rng(7)
        n = rng.normal(128, 38, (512, 512)).clip(0, 255).astype("uint8")
        img = Image.fromarray(n, "L").filter(ImageFilter.GaussianBlur(0.6))
        img.save(p)
    return p


# ------------------------------------------------------------------ primitivas
def estrella(cx, cy, r, rot=-90, ri=0.48) -> str:
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * ri
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def nota_musical(x, y, s, color, rot=0, doble=False) -> str:
    """Corchea (o semicorchea unida) dibujada a mano: óvalo, plica y bandera."""
    if doble:
        body = (f'<ellipse cx="0" cy="0" rx="6.2" ry="4.6" transform="rotate(-22)"/>'
                f'<ellipse cx="18" cy="-4" rx="6.2" ry="4.6" transform="rotate(-22 18 -4)"/>'
                f'<rect x="4.2" y="-30" width="2.4" height="30" rx="1.2"/>'
                f'<rect x="22.2" y="-34" width="2.4" height="30" rx="1.2"/>'
                f'<path d="M4.2,-30 L24.6,-34 L24.6,-28 L4.2,-24 Z"/>')
    else:
        body = (f'<ellipse cx="0" cy="0" rx="6.2" ry="4.6" transform="rotate(-22)"/>'
                f'<rect x="4.2" y="-30" width="2.4" height="30" rx="1.2"/>'
                f'<path d="M6.6,-30 C13,-27 17,-22 15.5,-13 C13.5,-19 10.5,-21 6.6,-21 Z"/>')
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s / 30:.3f})" fill="{color}">{body}</g>'


def brillo(cx, cy, r, op=0.9) -> str:
    """Destello de cuatro puntas."""
    return (f'<path d="M{cx},{cy - r} Q{cx + r * .16},{cy - r * .16} {cx + r},{cy} Q{cx + r * .16},{cy + r * .16} '
            f'{cx},{cy + r} Q{cx - r * .16},{cy + r * .16} {cx - r},{cy} Q{cx - r * .16},{cy - r * .16} {cx},{cy - r} Z" '
            f'fill="#fff" opacity="{op}"/>')


# ------------------------------------------------------------------ Kiki
def kiki(x, y, size, mood="contenta", brazos="abajo", flip=False) -> str:
    """Kiki en coordenadas de mascot.py (caja de 200 centrada en 0,0), escalada a `size` mm."""
    k = size / 200.0
    fx = -1 if flip else 1
    s = []
    # sombra de contacto
    s.append('<ellipse cx="0" cy="84" rx="58" ry="9" fill="#5A4630" opacity=".20" filter="url(#blur3)"/>')
    s.append('<ellipse cx="0" cy="82" rx="40" ry="5" fill="#5A4630" opacity=".18"/>')
    # cola
    s.append(f'<path d="M30,48 C84,56 96,20 70,2 C88,26 76,52 30,70 Z" fill="url(#kTail)" '
             f'stroke="{VERDE_OSCURO}" stroke-width="4" stroke-linejoin="round"/>')
    # cuerpo
    s.append(f'<rect x="-44" y="-6" width="88" height="84" rx="40" fill="url(#kBody)" stroke="{VERDE_OSCURO}" stroke-width="4"/>')
    s.append(f'<rect x="-26" y="14" width="52" height="54" rx="26" fill="url(#kBelly)"/>')
    s.append('<path d="M-18,24 Q-6,18 8,22" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>')
    s.append(f'<rect x="-40" y="6" width="6" height="44" rx="3" fill="{CRESTA}"/>'
             f'<rect x="-30" y="6" width="6" height="44" rx="3" fill="{CRESTA}"/>'
             f'<rect x="32" y="6" width="6" height="44" rx="3" fill="#FF6B8B"/>')
    # brazos con maracas
    poses = {"abajo": ((-1, -26, -50, 14), (1, 26, 50, 14)),
             "arriba": ((-1, 150, -44, 10), (1, -150, 44, 10)),
             "saludo": ((-1, -26, -50, 14), (1, -150, 44, 10))}[brazos]
    for side, ang, tx, ty in poses:
        s.append(f'<g transform="translate({tx} {ty}) rotate({ang})">'
                 f'<rect x="-7" y="-6" width="14" height="34" rx="7" fill="url(#kBody)" stroke="{VERDE_OSCURO}" stroke-width="4"/>'
                 f'<rect x="-2.2" y="22" width="4.4" height="6" fill="#B86A1C"/>'
                 f'<circle cx="0" cy="38" r="14" fill="url(#kMaraca)" stroke="{VERDE_OSCURO}" stroke-width="4"/>'
                 f'<ellipse cx="-4.5" cy="32" rx="4.5" ry="3.6" fill="#FFE7B8"/>'
                 f'<circle cx="-5.5" cy="42.5" r="2.5" fill="#FF6B8B"/><circle cx="2.5" cy="44" r="2.5" fill="#FF6B8B"/>'
                 f'<circle cx="8" cy="39" r="2.2" fill="#FF6B8B"/>'
                 f'</g>')
    # cabeza
    s.append(f'<rect x="-42" y="-74" width="84" height="72" rx="34" fill="url(#kHead)" stroke="{VERDE_OSCURO}" stroke-width="4"/>')
    s.append('<path d="M-30,-62 Q-14,-72 6,-70" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>')
    s.append(f'<rect x="-24" y="-30" width="48" height="26" rx="13" fill="url(#kSnout)" stroke="{VERDE_OSCURO}" stroke-width="4"/>')
    cerrados = mood == "celebrando"
    mira = 3.0 if mood == "pensando" else 0.0
    for cx in (-18.0, 18.0):
        if cerrados:
            s.append(f'<path d="M{cx - 11},-48 A11 8 0 0 1 {cx + 11},-48" stroke="#2E5B36" stroke-width="4" fill="none" stroke-linecap="round"/>')
            continue
        s.append(f'<ellipse cx="{cx}" cy="-47" rx="12" ry="13" fill="url(#kEye)" stroke="#3D9450" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="{cx + .5 + mira}" cy="-45.5" rx="5.5" ry="6.5" fill="#2E3A2F"/>')
        s.append(f'<circle cx="{cx + mira}" cy="-48" r="2.2" fill="#fff"/>')
        s.append(f'<circle cx="{cx + 3 + mira}" cy="-42.5" r="1" fill="#fff" opacity=".85"/>')
    s.append('<ellipse cx="-29" cy="-28" rx="9" ry="6" fill="#FF8CA0" opacity=".5"/>'
             '<ellipse cx="29" cy="-28" rx="9" ry="6" fill="#FF8CA0" opacity=".5"/>')
    s.append('<ellipse cx="-6.5" cy="-22" rx="2.5" ry="2" fill="#2E5B36"/><ellipse cx="6.5" cy="-22" rx="2.5" ry="2" fill="#2E5B36"/>')
    if mood in ("contenta", "celebrando"):
        s.append('<path d="M-15.04,-8.58 A16 10 0 0 0 15.04,-8.58" stroke="#2E5B36" stroke-width="4" fill="#C94F5E" stroke-linecap="round"/>')
        s.append('<path d="M-6,-3.6 Q0,-6.5 6,-3.6 Q0,-1.6 -6,-3.6 Z" fill="#FF8C9B"/>')
    elif mood == "pensando":
        s.append('<path d="M-8,-12 L8,-14" stroke="#2E5B36" stroke-width="4" stroke-linecap="round"/>')
    else:
        s.append('<path d="M-12.12,-8 A14 8 0 0 0 12.12,-8" stroke="#2E5B36" stroke-width="4" fill="none" stroke-linecap="round"/>')
    if mood == "celebrando":
        for ang in (-60, -20, 20, 60):
            r = math.radians(ang - 90)
            s.append(f'<line x1="{58 * math.cos(r):.1f}" y1="{-60 + 18 * math.sin(r):.1f}" x2="{70 * math.cos(r):.1f}" '
                     f'y2="{-66 + 22 * math.sin(r):.1f}" stroke="#FFD13B" stroke-width="5" stroke-linecap="round"/>')
    # cresta
    cres = []
    for i in range(5):
        cx = -30 + i * 15
        alto = 16 - abs(i - 2) * 3
        cres.append(f"M{cx - 7},-68 L{cx},{-68 - alto} L{cx + 7},-68 Z")
    s.append(f'<path d="{" ".join(cres)}" fill="url(#kCrest)" stroke="#D98A22" stroke-width="3" stroke-linejoin="round"/>')
    return f'<g transform="translate({x} {y}) scale({k * fx:.4f} {k:.4f})">{"".join(s)}</g>'


# ------------------------------------------------------------------ ilustraciones de cada paso
def avatar(cx, cy, r, tipo) -> str:
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gAv)" stroke="#fff" stroke-width="2.4"/>']
    s = r / 20
    t = f'transform="translate({cx} {cy}) scale({s:.3f})"'
    if tipo == "gato":
        g.append(f'<g {t}><path d="M-12,-6 L-13,-17 L-4,-11 Z M12,-6 L13,-17 L4,-11 Z" fill="#9A8F86" stroke="#5E554E" stroke-width="1.2"/>'
                 f'<circle cx="0" cy="1" r="12" fill="#B8ADA3" stroke="#5E554E" stroke-width="1.2"/>'
                 f'<circle cx="-4.5" cy="-1" r="1.8" fill="#2A2420"/><circle cx="4.5" cy="-1" r="1.8" fill="#2A2420"/>'
                 f'<path d="M-1.6,3 L1.6,3 L0,5 Z" fill="#E77F92"/>'
                 f'<path d="M-3,6.5 Q0,8.5 3,6.5 M-6,3.5 L-14,2 M-6,5 L-14,6 M6,3.5 L14,2 M6,5 L14,6" stroke="#5E554E" stroke-width=".8" fill="none" stroke-linecap="round"/></g>')
    elif tipo == "perro":
        g.append(f'<g {t}><circle cx="0" cy="1" r="12" fill="#D9A46A" stroke="#7A5530" stroke-width="1.2"/>'
                 f'<path d="M-11,-8 C-18,-6 -18,6 -13,9 C-10,4 -10,-2 -8,-6 Z M11,-8 C18,-6 18,6 13,9 C10,4 10,-2 8,-6 Z" fill="#8C5A2E" stroke="#5B3A1C" stroke-width="1"/>'
                 f'<ellipse cx="0" cy="5" rx="6" ry="4.5" fill="#F3D3AE"/>'
                 f'<circle cx="-4.5" cy="-1.5" r="1.8" fill="#2A2420"/><circle cx="4.5" cy="-1.5" r="1.8" fill="#2A2420"/>'
                 f'<ellipse cx="0" cy="3.2" rx="2.2" ry="1.6" fill="#2A2420"/>'
                 f'<path d="M-2.5,6.5 Q0,8.5 2.5,6.5" stroke="#5B3A1C" stroke-width=".9" fill="none" stroke-linecap="round"/></g>')
    else:  # zorro
        g.append(f'<g {t}><path d="M-12,-5 L-12,-17 L-3,-10 Z M12,-5 L12,-17 L3,-10 Z" fill="#E8762C" stroke="#9A4512" stroke-width="1.2"/>'
                 f'<path d="M-13,-5 Q0,-12 13,-5 Q12,8 0,13 Q-12,8 -13,-5 Z" fill="#F08A3C" stroke="#9A4512" stroke-width="1.2"/>'
                 f'<path d="M-12,1 Q-5,4 0,13 Q5,4 12,1 Q6,10 0,13 Q-6,10 -12,1 Z" fill="#FFF3E6"/>'
                 f'<circle cx="-4.5" cy="-1.5" r="1.8" fill="#2A2420"/><circle cx="4.5" cy="-1.5" r="1.8" fill="#2A2420"/>'
                 f'<ellipse cx="0" cy="10" rx="1.8" ry="1.3" fill="#2A2420"/></g>')
    g.append(f'<ellipse cx="{cx - r * .35}" cy="{cy - r * .55}" rx="{r * .38}" ry="{r * .18}" fill="#fff" opacity=".45"/>')
    return "".join(g)


def illo_hola(ox, oy) -> str:
    out = [kiki(ox + 62, oy + 74, 120, "contenta", "saludo")]
    for i, t in enumerate(("gato", "perro", "zorro")):
        out.append(avatar(ox + 150, oy + 22 + i * 40, 17, t))
    return "".join(out)


def illo_camara(ox, oy) -> str:
    """Cámara web sobre el monitor con el visor y los 21 puntos de la mano."""
    pts = logos._landmarks()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sc = 92 / (max(ys) - min(ys))
    cx0, cy0 = ox + 104, oy + 86
    P = [((x - (min(xs) + max(xs)) / 2) * sc + cx0, (y - (min(ys) + max(ys)) / 2) * sc + cy0) for x, y in pts]
    lines = "".join(f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}"/>' for a, b in logos.MP_EDGES)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.1 if i in (4, 8, 12, 16, 20) else 2.3}" '
                   f'fill="{"#2EC4B6" if i == 8 else "#fff"}" stroke="#1A1530" stroke-width=".8"/>' for i, (x, y) in enumerate(P))
    L, R, T, B, s = cx0 - 56, cx0 + 56, cy0 - 56, cy0 + 56, 16
    visor = (f'<path d="M{L},{T + s} V{T} H{L + s} M{R - s},{T} H{R} V{T + s} M{R},{B - s} V{B} H{R - s} M{L + s},{B} H{L} V{B - s}" '
             f'fill="none" stroke="#FF9F1C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    cam_x, cam_y = ox + 12, oy + 6
    cam = (f'<g transform="translate({cam_x} {cam_y})">'
           f'<rect x="0" y="0" width="58" height="30" rx="15" fill="url(#gCam)" stroke="#120E22" stroke-width="1.6"/>'
           f'<circle cx="29" cy="15" r="11" fill="#0D0B19" stroke="#4A4470" stroke-width="2"/>'
           f'<circle cx="29" cy="15" r="7" fill="url(#gLens)"/>'
           f'<circle cx="26" cy="12" r="2.4" fill="#fff" opacity=".9"/><circle cx="32" cy="18" r="1" fill="#fff" opacity=".6"/>'
           f'<circle cx="49" cy="15" r="2.2" fill="#2EC4B6"/><circle cx="49" cy="15" r="4.5" fill="#2EC4B6" opacity=".25"/>'
           f'<path d="M24,30 L22,40 L36,40 L34,30 Z" fill="#2B2540"/>'
           f'</g>')
    rayo = (f'<path d="M{cam_x + 40},{cam_y + 26} L{L + 10},{T + 6} L{R - 10},{T + 6} Z" fill="url(#gRay)" opacity=".55"/>')
    return (f'<rect x="{L - 8}" y="{T - 8}" width="{R - L + 16}" height="{B - T + 16}" rx="16" fill="#FFF4E2"/>'
            f'{rayo}{visor}<g stroke="#FFB13B" stroke-width="3.2" stroke-linecap="round">{lines}</g>{dots}{cam}')


def illo_sena(ox, oy) -> str:
    w = 106
    h = w * 452 / 336
    return (f'<g filter="url(#sombraCarta)"><image href="{uri(SENAS / "DO3.png")}" x="{ox + 50}" y="{oy - 6}" width="{w}" height="{h:.1f}" '
            f'transform="rotate(4 {ox + 50 + w / 2} {oy + h / 2})"/></g>'
            + brillo(ox + 160, oy + 10, 9) + brillo(ox + 44, oy + 120, 6, .8))


def illo_sonido(ox, oy) -> str:
    cx, cy = ox + 58, oy + 78
    parlante = (f'<g transform="translate({cx} {cy})">'
                f'<rect x="-34" y="-46" width="68" height="92" rx="14" fill="url(#gSpk)" stroke="#16323A" stroke-width="2"/>'
                f'<circle cx="0" cy="-22" r="11" fill="#173238" stroke="#2EC4B6" stroke-width="2.5"/>'
                f'<circle cx="0" cy="-22" r="4" fill="#2EC4B6"/>'
                f'<circle cx="0" cy="16" r="22" fill="#173238" stroke="#2EC4B6" stroke-width="3"/>'
                f'<circle cx="0" cy="16" r="13" fill="url(#gCone)"/>'
                f'<circle cx="0" cy="16" r="5" fill="#2EC4B6"/>'
                f'<path d="M-26,-40 Q-12,-46 6,-44" stroke="#fff" stroke-width="3" opacity=".35" fill="none" stroke-linecap="round"/>'
                f'</g>')
    ondas = "".join(f'<path d="M{cx + 44 + i * 13},{cy - 30 + i * -6} Q{cx + 62 + i * 15},{cy} {cx + 44 + i * 13},{cy + 30 - i * -6}" '
                    f'stroke="#2EC4B6" stroke-width="{5 - i}" fill="none" stroke-linecap="round" opacity="{.9 - i * .22:.2f}"/>'
                    for i in range(3))
    notas = (nota_musical(ox + 128, oy + 34, 34, "#FF6B8B", -8) + nota_musical(ox + 158, oy + 70, 28, "#FFD13B", 10)
             + nota_musical(ox + 140, oy + 130, 30, "#7A5CFA", -12, doble=True))
    return parlante + ondas + notas


def illo_estrellas(ox, oy) -> str:
    out = []
    for cx, cy, r, rot in ((ox + 52, oy + 52, 30, -96), (ox + 108, oy + 30, 38, -88), (ox + 160, oy + 56, 30, -84)):
        out.append(f'<polygon points="{estrella(cx, cy + 3, r, rot)}" fill="#C98A06" opacity=".55"/>')
        out.append(f'<polygon points="{estrella(cx, cy, r, rot)}" fill="url(#gStar)" stroke="#D89A0A" stroke-width="2.2" stroke-linejoin="round"/>')
        out.append(f'<ellipse cx="{cx - r * .22}" cy="{cy - r * .2}" rx="{r * .22}" ry="{r * .12}" fill="#fff" opacity=".65" transform="rotate(-25 {cx} {cy})"/>')
    out.append(brillo(ox + 186, oy + 14, 7) + brillo(ox + 22, oy + 18, 5))
    # letrero "¡Casi! Otra vez"
    lx, ly = ox + 70, oy + 98
    out.append(f'<g transform="rotate(-4 {lx + 50} {ly + 25})">'
               f'<rect x="{lx + 46}" y="{ly + 40}" width="7" height="26" rx="2" fill="#B07A45"/>'
               f'<rect x="{lx}" y="{ly}" width="100" height="44" rx="10" fill="#FFF6E4" stroke="#C9934F" stroke-width="2.5"/>'
               f'<text x="{lx + 50}" y="{ly + 19}" text-anchor="middle" class="f" font-weight="600" font-size="15" fill="#E04A6B">¡Casi!</text>'
               f'<text x="{lx + 50}" y="{ly + 36}" text-anchor="middle" class="n" font-weight="800" font-size="12" fill="{INK2}">otra vez 💡</text>'
               f'</g>')
    return "".join(out)


def illo_piensa(ox, oy) -> str:
    out = [kiki(ox + 52, oy + 98, 104, "pensando", "abajo")]
    # burbujas de pensamiento
    out.append(f'<circle cx="{ox + 92}" cy="{oy + 40}" r="5" fill="#fff" stroke="#CDBDF7" stroke-width="2"/>'
               f'<circle cx="{ox + 104}" cy="{oy + 26}" r="8" fill="#fff" stroke="#CDBDF7" stroke-width="2"/>')
    bx, by = ox + 108, oy - 8
    out.append(f'<path d="M{bx + 10},{by + 30} C{bx - 6},{by + 30} {bx - 4},{by + 6} {bx + 14},{by + 8} '
               f'C{bx + 18},{by - 8} {bx + 46},{by - 10} {bx + 52},{by + 2} C{bx + 70},{by - 6} {bx + 88},{by + 10} {bx + 80},{by + 26} '
               f'C{bx + 94},{by + 40} {bx + 78},{by + 60} {bx + 62},{by + 54} C{bx + 54},{by + 68} {bx + 26},{by + 68} {bx + 20},{by + 54} '
               f'C{bx + 2},{by + 60} {bx - 4},{by + 40} {bx + 10},{by + 30} Z" fill="#fff" stroke="#CDBDF7" stroke-width="2.4"/>')
    # mini mapa de aventura dentro de la nube
    camino = f"M{bx + 14},{by + 46} C{bx + 30},{by + 24} {bx + 44},{by + 54} {bx + 58},{by + 30} S{bx + 74},{by + 14} {bx + 76},{by + 22}"
    out.append(f'<path d="{camino}" stroke="#C9B3FF" stroke-width="4" fill="none" stroke-linecap="round" stroke-dasharray="1 7"/>')
    for (px, py, col) in ((bx + 14, by + 46, "#2EC4B6"), (bx + 36, by + 40, "#FFD13B"), (bx + 58, by + 30, "#FF6B8B")):
        out.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{col}" stroke="#fff" stroke-width="1.6"/>')
    out.append(f'<path d="M{bx + 76},{by + 24} V{by + 6}" stroke="#5638C4" stroke-width="2.4" stroke-linecap="round"/>'
               f'<path d="M{bx + 76},{by + 6} L{bx + 90},{by + 11} L{bx + 76},{by + 16} Z" fill="#7A5CFA"/>')
    # medidor "ni muy fácil ni muy difícil"
    mx, my = ox + 112, oy + 104
    out.append(f'<g>'
               f'<path d="M{mx},{my + 30} A34 34 0 0 1 {mx + 68},{my + 30}" stroke="#E9E2FF" stroke-width="10" fill="none" stroke-linecap="round"/>'
               f'<path d="M{mx},{my + 30} A34 34 0 0 1 {mx + 22},{my - .5}" stroke="#2EC4B6" stroke-width="10" fill="none" stroke-linecap="round"/>'
               f'<path d="M{mx + 22},{my - .5} A34 34 0 0 1 {mx + 54},{my + 6}" stroke="#FFD13B" stroke-width="10" fill="none"/>'
               f'<path d="M{mx + 54},{my + 6} A34 34 0 0 1 {mx + 68},{my + 30}" stroke="#FF6B8B" stroke-width="10" fill="none" stroke-linecap="round"/>'
               f'<line x1="{mx + 34}" y1="{my + 30}" x2="{mx + 44}" y2="{my + 2}" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
               f'<circle cx="{mx + 34}" cy="{my + 30}" r="5" fill="{INK}"/>'
               f'</g>')
    return "".join(out)


# ------------------------------------------------------------------ tarjetas de paso
def paso(x, y, w, h, num, color, bisel, titulo, sub, illo, illo_dx, esc=0.82) -> str:
    tx = x + 84
    lineas_t = "".join(f'<tspan x="{tx}" dy="{0 if i == 0 else 31}">{t}</tspan>' for i, t in enumerate(titulo))
    y_sub = y + 54 + 31 * (len(titulo) - 1) + 36
    lineas_s = "".join(f'<tspan x="{tx}" dy="{0 if i == 0 else 23}">{t}</tspan>' for i, t in enumerate(sub))
    return f'''
<g>
  <rect x="{x}" y="{y + 6}" width="{w}" height="{h}" rx="30" fill="{bisel}" opacity=".9"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="url(#gCard)" filter="url(#sombraCard)"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="none" stroke="{color}" stroke-width="4"/>
  <rect x="{x + 18}" y="{y + 8}" width="{w - 36}" height="10" rx="5" fill="#fff" opacity=".8"/>
  <circle cx="{x + 44}" cy="{y + 48}" r="29" fill="{bisel}"/>
  <circle cx="{x + 44}" cy="{y + 44}" r="29" fill="{color}"/>
  <circle cx="{x + 44}" cy="{y + 44}" r="29" fill="url(#gGloss)"/>
  <text x="{x + 44}" y="{y + 58}" text-anchor="middle" class="f" font-weight="700" font-size="38" fill="#fff" stroke="{bisel}" stroke-width="1.5" paint-order="stroke">{num}</text>
  <text x="{tx}" y="{y + 54}" class="f" font-weight="600" font-size="29" fill="{INK}">{lineas_t}</text>
  <text x="{tx}" y="{y_sub}" class="n" font-weight="700" font-size="18.5" fill="{INK2}">{lineas_s}</text>
  <g transform="translate({x + illo_dx} {y + 12}) scale({esc})">{illo(0, 0)}</g>
</g>'''


# ------------------------------------------------------------------ fondo
def fondo() -> str:
    rnd = random.Random(11)
    deco = []
    cols = [c for _, _, c, _ in NOTAS]
    zonas_libres = [(20, 380, 880, 410), (20, 935, 880, 980)]
    for _ in range(46):
        x, y = rnd.uniform(15, 885), rnd.uniform(130, 1150)
        col = rnd.choice(cols)
        if rnd.random() < .5:
            deco.append(f'<polygon points="{estrella(x, y, rnd.uniform(4, 9), rnd.uniform(-110, -70))}" fill="{col}" opacity="{rnd.uniform(.16, .3):.2f}"/>')
        else:
            deco.append(nota_musical(x, y, rnd.uniform(12, 22), col, rnd.uniform(-20, 20), rnd.random() < .3)
                        .replace(f'fill="{col}"', f'fill="{col}" opacity="{rnd.uniform(.14, .24):.2f}"'))
    _ = zonas_libres
    return f'''
<rect width="{W}" height="{H}" fill="url(#gBg)"/>
<circle cx="790" cy="150" r="420" fill="url(#gSol)"/>
<circle cx="80" cy="640" r="360" fill="url(#gCielo)"/>
<circle cx="840" cy="1040" r="330" fill="url(#gMenta)"/>
<g opacity=".55">{"".join(f'<path d="M0,{180 + i * 9} C220,{150 + i * 9} 420,{230 + i * 9} 900,{170 + i * 9}" stroke="#F2D9BF" stroke-width="1.2" fill="none"/>' for i in range(5))}</g>
{"".join(deco)}
<rect width="{W}" height="{H}" fill="url(#pGrano)" opacity=".07" style="mix-blend-mode:multiply"/>
'''


def camino(rows) -> str:
    """Camino de juego (cinta con pentagrama) que serpentea entre los pasos."""
    (y1, y2, y3) = rows
    m1, m2 = y1 + 152 / 2, y2 + 152 / 2
    m3 = y3 + 152 / 2
    d = (f"M80,{m1} H820 C905,{m1} 905,{m2} 820,{m2} H80 C-5,{m2} -5,{m3} 80,{m3} H820")
    return (f'<path d="{d}" stroke="#E7C9A6" stroke-width="58" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>'
            f'<path d="{d}" stroke="#FFF3E2" stroke-width="46" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            + "".join(f'<path d="{d}" transform="translate(0 {o})" stroke="#E6C7A3" stroke-width="1.3" fill="none"/>' for o in (-16, -8, 0, 8, 16)))


# ------------------------------------------------------------------ teclado de señas
def teclado(y) -> str:
    n = len(NOTAS)
    cw, gap = 88, 16
    x0 = (W - (n * cw + (n - 1) * gap)) / 2
    out = []
    # base de madera tipo xilófono
    out.append(f'<rect x="{x0 - 22}" y="{y + 114}" width="{n * cw + (n - 1) * gap + 44}" height="30" rx="17" fill="url(#gMadera)" filter="url(#sombraCard)"/>')
    out.append(f'<rect x="{x0 - 12}" y="{y + 117}" width="{n * cw + (n - 1) * gap + 24}" height="5" rx="3" fill="#fff" opacity=".25"/>')
    for i, (code, nombre, col, bev) in enumerate(NOTAS):
        x = x0 + i * (cw + gap)
        ratio = 452 / 336 if code not in ("DO4", "SI3") else (692 / 514 if code == "DO4" else 704 / 516)
        h = cw * ratio
        top = y
        out.append(f'<g filter="url(#sombraCarta)"><image href="{uri(SENAS / f"{code}.png")}" x="{x:.1f}" y="{top:.1f}" '
                   f'width="{cw}" height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/></g>')
        # tecla de color sobre la base
        out.append(f'<rect x="{x + 6}" y="{y + 122}" width="{cw - 12}" height="20" rx="8" fill="{bev}"/>'
                   f'<rect x="{x + 6}" y="{y + 120}" width="{cw - 12}" height="18" rx="8" fill="{col}"/>'
                   f'<rect x="{x + 14}" y="{y + 123}" width="{cw - 28}" height="5" rx="2.5" fill="#fff" opacity=".45"/>'
                   f'<circle cx="{x + 13}" cy="{y + 129}" r="2.2" fill="{bev}"/><circle cx="{x + cw - 13}" cy="{y + 129}" r="2.2" fill="{bev}"/>')
    return "".join(out)


# ------------------------------------------------------------------ cabecera
def cabecera() -> str:
    logos_g = f'''
<g filter="url(#sombraCard)">
  <rect x="34" y="26" width="372" height="96" rx="26" fill="#fff"/>
</g>
<rect x="44" y="34" width="66" height="80" rx="12" fill="#141414"/>
<image href="{uri(A / 'logos' / 'upb_logo_vertical_blanco.png')}" x="48" y="38" width="58" height="72" preserveAspectRatio="xMidYMid meet"/>
<image href="{uri(A / 'logos' / 'logo_his_engranaje.png')}" x="122" y="32" width="84" height="84" preserveAspectRatio="xMidYMid meet"/>
<clipPath id="cpSil"><rect x="218" y="34" width="178" height="80" rx="12"/></clipPath>
<rect x="218" y="34" width="178" height="80" rx="12" fill="#F6CE5A"/>
<image href="{uri(A / 'logos' / 'logo_siloge.png')}" x="218" y="34" width="178" height="80" preserveAspectRatio="xMidYMid slice" clip-path="url(#cpSil)"/>
'''
    etiqueta = (f'<text x="866" y="62" text-anchor="end" class="n" font-weight="800" font-size="15" fill="{INK2}" letter-spacing="1.5">'
                f'GESTIÓN TECNOLÓGICA · 2026-2</text>'
                f'<text x="866" y="86" text-anchor="end" class="n" font-weight="700" font-size="15" fill="{INK2}">'
                f'Facultad de Ingeniería Industrial · Montería</text>'
                f'<text x="866" y="110" text-anchor="end" class="n" font-weight="700" font-size="15" fill="{INK2}">'
                f'Semillero SILOGE · Hub Industrial Solution</text>')
    # título con "Kids" en los colores de la escala
    kids = "".join(f'<tspan fill="{c}">{ch}</tspan>' for ch, c in zip("Kids", ("#FF6B8B", "#FF9F1C", "#2EC4B6", "#7A5CFA")))
    titulo = f'''
<text x="330" y="232" class="f" font-weight="700" font-size="92" fill="#6E3B1D" opacity=".18" transform="translate(3 6)">Hand Sing</text>
<text x="330" y="232" class="f" font-weight="700" font-size="92" fill="{INK}" stroke="#fff" stroke-width="7" paint-order="stroke" stroke-linejoin="round">Hand Sing</text>
<text x="330" y="322" class="f" font-weight="700" font-size="100" fill="#6E3B1D" opacity=".18" transform="translate(3 6)">Kids</text>
<text x="330" y="322" class="f" font-weight="700" font-size="100" stroke="#fff" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{kids}</text>
<g transform="translate(578 262)">
  <rect x="0" y="0" width="290" height="62" rx="31" fill="#FFD13B"/>
  <rect x="0" y="0" width="290" height="62" rx="31" fill="url(#gGloss)"/>
  <text x="145" y="27" text-anchor="middle" class="f" font-weight="600" font-size="22" fill="{INK}">¡Tus manos crean</text>
  <text x="145" y="51" text-anchor="middle" class="f" font-weight="600" font-size="22" fill="{INK}">la música! 🎶</text>
</g>
'''
    burbuja = f'''
<g filter="url(#sombraCard)">
  <path d="M60,150 H258 Q276,150 276,168 V206 Q276,224 258,224 H170 L148,246 L150,224 H60 Q42,224 42,206 V168 Q42,150 60,150 Z" fill="#fff"/>
</g>
<text x="159" y="181" text-anchor="middle" class="f" font-weight="600" font-size="22" fill="{INK}">¡Hola! Soy Kiki 🦎</text>
<text x="159" y="208" text-anchor="middle" class="n" font-weight="800" font-size="17" fill="{INK2}">¿Jugamos con las manos?</text>
'''
    return logos_g + etiqueta + burbuja + kiki(160, 318, 150, "celebrando", "arriba") + titulo


def html() -> str:
    preparar_senas()
    grano = preparar_grano()
    fuentes = A / "fonts"
    rows = (420, 598, 776)
    xl, xr, cw, ch = 36, 468, 396, 152
    pasos = [
        (xl, rows[0], 1, "DO3", ["¡Hola,", "soy Kiki!"], ["Elige tu amigo", "para jugar"], illo_hola, 228),
        (xr, rows[0], 2, "RE3", ["Enséñale", "tus manos"], ["Kiki aprende", "tus señas"], illo_camara, 226),
        (xr, rows[1], 3, "MI3", ["Haz la", "seña"], ["¡Do son dos", "puñitos! ✊✊"], illo_sena, 222),
        (xl, rows[1], 4, "FA3", ["¡Suena", "la nota!"], ["Tus manos", "hacen música"], illo_sonido, 230),
        (xl, rows[2], 5, "SOL3", ["¡Ganas", "estrellas!"], ["Si fallas, Kiki", "te ayuda"], illo_estrellas, 226),
        (xr, rows[2], 6, "LA3", ["Kiki elige", "tu juego"], ["Ni muy fácil,", "ni muy difícil"], illo_piensa, 222),
    ]
    tarjetas = "".join(paso(x, y, cw, ch, n, C[c][0], C[c][1], t, s, il, dx) for x, y, n, c, t, s, il, dx in pasos)

    # flechas de dirección sobre el camino
    def flecha(x, y, rot, col):
        return (f'<g transform="translate({x} {y}) rotate({rot})"><circle r="16" fill="{col}"/><circle r="16" fill="url(#gGloss)"/>'
                f'<path d="M-5,-8 L6,0 L-5,8" stroke="#fff" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    m = [r + ch / 2 for r in rows]
    flechas = (flecha(450, m[0], 0, "#FF9F1C") + flecha(884, (m[0] + m[1]) / 2, 90, "#FFD13B")
               + flecha(450, m[1], 180, "#2EC4B6") + flecha(16, (m[1] + m[2]) / 2, 90, "#38B6FF")
               + flecha(450, m[2], 0, "#7A5CFA"))
    # lazo "¡otra vez!": del paso 6 vuelve al paso 3
    lazo = f'''
<path d="M{xr + cw - 40},{rows[2] + ch + 4} C{xr + cw + 30},{rows[2] + ch + 40} 905,{rows[1] + 40} {xr + cw + 6},{rows[1] + 20}"
      stroke="#7A5CFA" stroke-width="5" fill="none" stroke-dasharray="2 10" stroke-linecap="round"/>
<path d="M{xr + cw + 18},{rows[1] + 8} L{xr + cw + 2},{rows[1] + 20} L{xr + cw + 20},{rows[1] + 30}" stroke="#7A5CFA" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate({xr + 190} {rows[2] + ch + 10})">
  <rect x="0" y="0" width="206" height="40" rx="20" fill="#7A5CFA"/>
  <rect x="0" y="0" width="206" height="40" rx="20" fill="url(#gGloss)"/>
  <text x="103" y="27" text-anchor="middle" class="f" font-weight="600" font-size="20" fill="#fff">🔁 ¡Y otra vez!</text>
</g>'''
    seccion = f'''
<g transform="translate(450 384)">
  <rect x="-170" y="-26" width="340" height="50" rx="25" fill="{INK}"/>
  <text x="0" y="9" text-anchor="middle" class="f" font-weight="600" font-size="27" fill="#FFD13B">¿Cómo se juega?</text>
</g>'''
    ty = 986
    teclado_tit = f'''
<text x="450" y="{ty}" text-anchor="middle" class="f" font-weight="700" font-size="34" fill="{INK}">Las 8 señas de la música</text>
<text x="450" y="{ty + 26}" text-anchor="middle" class="n" font-weight="700" font-size="17" fill="{INK2}">Cada nota tiene su color y su seña con las dos manos</text>'''
    pie = f'''
<g transform="translate(450 1187)">
  <rect x="-372" y="-16" width="744" height="30" rx="15" fill="#fff" opacity=".92"/>
  <g transform="translate(-352 -12)">
    <rect x="0" y="7" width="15" height="12" rx="3" fill="#2EC4B6"/>
    <path d="M3,8 V4.5 a4.5,4.5 0 0 1 9,0 V8" stroke="#1E8F85" stroke-width="2.2" fill="none"/>
  </g>
  <text x="-326" y="4.5" class="n" font-weight="800" font-size="14.5" fill="{INK}">Todo pasa en tu computador: la cámara no graba ni envía nada.</text>
  <text x="360" y="4.5" text-anchor="end" class="n" font-weight="700" font-size="13" fill="{INK2}">Hand Sing Kids v2.0 · UPB Montería</text>
</g>'''
    defs = f'''
<defs>
  <linearGradient id="gBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFF9F2"/><stop offset=".55" stop-color="#FFF3E6"/><stop offset="1" stop-color="#FDEBDD"/>
  </linearGradient>
  <radialGradient id="gSol"><stop offset="0" stop-color="#FFD13B" stop-opacity=".42"/><stop offset=".55" stop-color="#FFD13B" stop-opacity=".12"/><stop offset="1" stop-color="#FFD13B" stop-opacity="0"/></radialGradient>
  <radialGradient id="gCielo"><stop offset="0" stop-color="#38B6FF" stop-opacity=".16"/><stop offset="1" stop-color="#38B6FF" stop-opacity="0"/></radialGradient>
  <radialGradient id="gMenta"><stop offset="0" stop-color="#2EC4B6" stop-opacity=".16"/><stop offset="1" stop-color="#2EC4B6" stop-opacity="0"/></radialGradient>
  <linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFF9F3"/></linearGradient>
  <radialGradient id="gGloss" cx=".35" cy=".25" r=".75">
    <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".45" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".10"/>
  </radialGradient>
  <radialGradient id="gAv" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#FFF6E8"/><stop offset="1" stop-color="#F6DDBF"/></radialGradient>
  <radialGradient id="kHead" cx=".38" cy=".28" r=".85"><stop offset="0" stop-color="#B4EDB7"/><stop offset=".55" stop-color="{VERDE_CLARO}"/><stop offset="1" stop-color="#6FC678"/></radialGradient>
  <radialGradient id="kBody" cx=".35" cy=".25" r=".9"><stop offset="0" stop-color="#7CD486"/><stop offset=".6" stop-color="{VERDE}"/><stop offset="1" stop-color="#4AA356"/></radialGradient>
  <radialGradient id="kSnout" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#78CF82"/><stop offset="1" stop-color="#55B061"/></radialGradient>
  <radialGradient id="kBelly" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#F6FFF2"/><stop offset="1" stop-color="{PANZA}"/></radialGradient>
  <linearGradient id="kTail" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A6E6AA"/><stop offset="1" stop-color="#6FC678"/></linearGradient>
  <radialGradient id="kMaraca" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFC266"/><stop offset=".6" stop-color="#FF9F1C"/><stop offset="1" stop-color="#E07F00"/></radialGradient>
  <linearGradient id="kCrest" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC163"/><stop offset="1" stop-color="{CRESTA}"/></linearGradient>
  <radialGradient id="kEye" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#E9F4EA"/></radialGradient>
  <linearGradient id="gStar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE680"/><stop offset=".6" stop-color="#FFD13B"/><stop offset="1" stop-color="#F5B300"/></linearGradient>
  <linearGradient id="gCam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4470"/><stop offset="1" stop-color="#231F3D"/></linearGradient>
  <radialGradient id="gLens" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#64D2FF"/><stop offset=".5" stop-color="#2A5DB0"/><stop offset="1" stop-color="#151226"/></radialGradient>
  <linearGradient id="gRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#64D2FF" stop-opacity=".55"/><stop offset="1" stop-color="#64D2FF" stop-opacity="0"/></linearGradient>
  <linearGradient id="gSpk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A6A73"/><stop offset="1" stop-color="#1E3F46"/></linearGradient>
  <radialGradient id="gCone" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#5E8D96"/><stop offset="1" stop-color="#173238"/></radialGradient>
  <linearGradient id="gMadera" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A066"/><stop offset=".5" stop-color="#C08048"/><stop offset="1" stop-color="#9C6334"/></linearGradient>
  <filter id="blur3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="sombraCard" x="-10%" y="-10%" width="120%" height="135%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#7A4A1E" flood-opacity=".16"/>
  </filter>
  <filter id="sombraCarta" x="-15%" y="-10%" width="130%" height="125%">
    <feDropShadow dx="0" dy="4" stdDeviation="3.5" flood-color="#5A3A1A" flood-opacity=".28"/>
  </filter>
  <pattern id="pGrano" width="120" height="120" patternUnits="userSpaceOnUse">
    <image href="{uri(grano)}" width="120" height="120"/>
  </pattern>
</defs>'''
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">'
           f'{defs}{fondo()}{cabecera()}{seccion}{camino(rows)}{flechas}{tarjetas}{lazo}{teclado_tit}{teclado(1022)}{pie}</svg>')
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Hand Sing Kids — Reverso infantil</title>
<style>
@font-face {{ font-family: "Fredoka"; src: url("{uri(fuentes / 'Fredoka[wdth,wght].ttf')}"); font-weight: 300 700; }}
@font-face {{ font-family: "Nunito"; src: url("{uri(fuentes / 'Nunito[wght].ttf')}"); font-weight: 200 1000; }}
@page {{ size: {W}mm {H}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; background: {CREAM}; }}
svg {{ display: block; }}
.f {{ font-family: "Fredoka", sans-serif; }}
.n {{ font-family: "Nunito", sans-serif; }}
</style></head><body>{svg}</body></html>'''


def construir() -> None:
    src = Path(__file__).resolve().parent / "poster_ninos.html"
    src.write_text(html(), encoding="utf-8")
    pdf = OUT_DIR / f"{NOMBRE}.pdf"
    png = OUT_DIR / f"{NOMBRE}.png"
    render.pdf(src, pdf)
    # 900 mm = 3401.6 px CSS; a escala 1.5 → 5102 × 6803 px (≈ 144 ppp a tamaño real)
    render.png(src, png, 3402, 4536, 1.5)
    prev = ROOT / "recursos" / "_previews" / "poster_ninos.png"
    Image.open(png).convert("RGB").resize((900, 1200), Image.LANCZOS).save(prev)
    print(pdf, png, prev, sep="\n")


if __name__ == "__main__":
    construir()
