"""DFD (notación Yourdon-DeMarco) de Hand Sing Kids, niveles 0, 1 y 2.

Los almacenes D1-D6 son tablas reales de SQLite (o archivos) de HandSingKids7:
  D1 profiles, rewards, profile_achievements      D4 skill_state
  D2 plantillas de calibración (JSON)             D5 skills, activities, achievements
  D3 sessions, attempts, activity_results         D6 meta (fila `predictor_<id>`)

El balanceo entre niveles se comprueba en `BALANCE` (abajo) y se imprime al
ejecutar el módulo: los flujos que cruzan la frontera de un proceso en un nivel
son exactamente los que entran y salen de sus hijos en el nivel siguiente.

Escala: nivel 0 en lienzo de 720 (página vertical, 6,5 in útiles) y niveles 1 y 2
en lienzo de 1080 (página apaisada, 9 in útiles): 13,5 unidades ≈ 8,1 a 8,8 pt.
"""
from __future__ import annotations

import math

from svglib import SVG, GRAY_D

FS = 13.5
G = "#ECECEC"   # vecinos del nivel superior en el nivel 2


class Canvas:
    """SVG + registro de nodos para conectar flujos por el borde de cada figura."""

    def __init__(self, w: int, h: int, title: str) -> None:
        self.s = SVG(w, h, title)
        self.nodes: dict[str, tuple] = {}

    # ------------------------------------------------------------- nodos
    def process(self, key, cx, cy, r, num, label, *, size=FS, fill="#fff"):
        self.nodes[key] = ("c", cx, cy, r)
        self.s.process(cx, cy, r, num, label, size=size, fill=fill)

    def entity(self, key, cx, cy, w, h, label, *, size=FS):
        self.nodes[key] = ("r", cx, cy, w, h)
        self.s.entity(cx, cy, w, h, label, size=size)

    def store(self, key, cx, cy, w, h, code, label, *, size=FS, dup=False):
        self.nodes[key] = ("r", cx, cy, w, h)
        self.s.store(cx, cy, w, h, code, label, size=size, dup=dup)

    # -------------------------------------------------------- geometría
    def _center(self, k):
        n = self.nodes[k]
        return n[1], n[2]

    def _edge(self, k, toward, off=0.0, sign=1, line=None):
        """Punto de conexión en el borde de `k`. Sin `line`, apunta al centro de
        `toward`; con `line=(u, p)` (dirección y normal del flujo) el punto es el de
        una recta paralela a la línea de centros, desplazada `off` (flujos paralelos)."""
        n = self.nodes[k]
        cx, cy = n[1], n[2]
        if line is not None:
            (ux, uy), (px, py) = line
            ox, oy = cx + px * off, cy + py * off
        else:
            dx, dy = toward[0] - cx, toward[1] - cy
            d = math.hypot(dx, dy) or 1.0
            ux, uy = dx / d, dy / d
            ox, oy = cx, cy
        ux, uy = ux * sign, uy * sign
        if n[0] == "c":
            r = n[3]
            h = math.sqrt(max(r * r - (off if line is not None else 0) ** 2, 1.0))
            return ox + ux * h, oy + uy * h
        w, h = n[3], n[4]
        tx = (w / 2) / abs(ux) if abs(ux) > 1e-9 else 1e9
        ty = (h / 2) / abs(uy) if abs(uy) > 1e-9 else 1e9
        t = min(tx, ty)
        return ox + ux * t, oy + uy * t

    def link(self, a, b, label=None, *, off=0.0, via=None, both=False, size=FS,
             lpos=None, anchor="middle"):
        """Flujo de `a` hacia `b`. `via` = puntos intermedios (codo). `off` separa
        flujos paralelos. `lpos` = (x, y) absoluto de la etiqueta."""
        ca, cb = self._center(a), self._center(b)
        via = via or []
        first = via[0] if via else cb
        last = via[-1] if via else ca
        if via or not off:
            p0 = self._edge(a, first)
            p1 = self._edge(b, last)
        else:
            dx, dy = cb[0] - ca[0], cb[1] - ca[1]
            d = math.hypot(dx, dy) or 1.0
            u = (dx / d, dy / d)
            line = (u, (-u[1], u[0]))
            p0 = self._edge(a, cb, off, 1, line)
            p1 = self._edge(b, ca, off, -1, line)
        pts = [p0, *via, p1] if via else [p0, p1]
        pts = [(round(x, 1), round(y, 1)) for x, y in pts]
        if lpos is None:
            best = max(range(len(pts) - 1), key=lambda i: math.dist(pts[i], pts[i + 1]))
            lpos = ((pts[best][0] + pts[best + 1][0]) / 2, (pts[best][1] + pts[best + 1][1]) / 2)
        self.s.dflow(pts, label, lx=lpos[0], ly=lpos[1], size=size, anchor=anchor, both=both)


# =====================================================================
def dfd0() -> SVG:
    """Página vertical: lienzo de 720."""
    c = Canvas(720, 340, "DFD nivel 0: diagrama de contexto")
    c.process("0", 380, 170, 88, "0", "Sistema Hand Sing Kids (aplicación local)", size=16)
    c.entity("nino", 92, 50, 150, 56, "Niño o niña", size=16)
    c.entity("cam", 92, 290, 150, 56, "Cámara web", size=16)
    c.entity("adulto", 630, 170, 150, 76, "Acudiente o docente", size=16)
    c.link("nino", "0", "Selección de perfil\ny de actividad", off=-13, size=16, lpos=(268, 40))
    c.link("0", "nino", "Actividad, nota\nsonora y resultado", off=-13, size=16, lpos=(160, 125), anchor="start")
    c.link("cam", "0", "Fotogramas RGB", size=16, lpos=(205, 262), anchor="start")
    # con off < 0, el flujo adulto→0 queda debajo y el 0→adulto encima
    c.link("adulto", "0", "Perfil, ajustes y\nsolicitud de informe", off=-16, size=16, lpos=(552, 238))
    c.link("0", "adulto", "Informe de\nprogreso", off=-16, size=16, lpos=(552, 102))
    return c.s


def dfd1() -> SVG:
    c = Canvas(1080, 660, "DFD nivel 1: descomposición en siete procesos")
    R = 62
    L = dict(size=FS, weight=500, fill=GRAY_D)
    c.entity("nino", 80, 222, 120, 54, "Niño o niña")
    c.entity("cam", 80, 560, 120, 54, "Cámara web")
    c.entity("adulto", 995, 560, 140, 60, "Acudiente o docente")
    c.process("p1", 320, 112, R, "1.0", "Gestionar perfiles y ajustes")
    c.process("p5", 600, 112, R, "5.0", "Planificar la sesión adaptativa")
    c.process("p6", 320, 335, R, "6.0", "Interactuar con el niño")
    c.process("p3", 600, 335, R, "3.0", "Evaluar y registrar intentos")
    c.process("p4", 860, 335, R, "4.0", "Actualizar el gemelo digital")
    c.process("p2", 320, 560, R, "2.0", "Reconocer señas")
    c.process("p7", 800, 560, R, "7.0", "Generar el informe")
    c.store("d1", 112, 38, 190, 36, "D1", "Perfiles y logros")
    c.store("d5", 870, 40, 230, 36, "D5", "Catálogo de actividades")
    c.store("d4", 860, 196, 200, 36, "D4", "Estado de habilidades")
    c.store("d6", 990, 270, 140, 52, "D6", "Modelo del predictor")
    c.store("d3", 600, 470, 220, 36, "D3", "Intentos y resultados")
    c.store("d4b", 660, 632, 220, 34, "D4", "Estado de habilidades", dup=True)
    c.store("d2", 320, 640, 230, 34, "D2", "Plantillas de calibración")
    # entidades externas
    c.link("nino", "p1", "Selección\nde perfil", lpos=(186, 150), anchor="end")
    c.link("nino", "p6", "Elección de\nactividad", off=-11, lpos=(212, 250), anchor="start")
    c.link("p6", "nino", "Actividad, nota\nsonora y resultado", off=-11, lpos=(192, 318), anchor="end")
    c.link("cam", "p2", "Fotogramas RGB", lpos=(205, 584))
    c.link("adulto", "p1", "Perfil y ajustes", via=[(1072, 560), (1072, 8), (380, 8), (380, 61)], lpos=(735, 8))
    c.link("adulto", "p7", "Solicitud\nde informe", off=12, lpos=(882, 518))
    c.link("p7", "adulto", "Informe de\nprogreso", off=12, lpos=(882, 602))
    # flujos internos
    c.link("d1", "p1", None, both=True)
    c.s.text(112, 70, "Perfil, estrellas y racha", **L)
    c.link("p1", "p5", "Perfil, edad y\ntiempo de sesión", lpos=(460, 92))
    c.link("p2", "p1", "Calibración\ncompletada", via=[(200, 522), (200, 135)], lpos=(200, 440))
    c.link("p5", "p6", "Ruta del día y\ndecisión adaptativa", off=12, lpos=(440, 196), anchor="end")
    c.link("p6", "p5", "Actividad elegida\ny tiempo jugado", off=12, lpos=(468, 238), anchor="start")
    c.link("p5", "p3", "Actividad y\nsecuencia\nesperada", lpos=(612, 232), anchor="start")
    c.link("p2", "p3", "Gesto confirmado\ny confianza", lpos=(430, 445))
    c.link("p3", "p6", "Acierto o fallo\ny puntaje", lpos=(465, 362))
    c.link("p3", "p4", "Resultado\npor nota", lpos=(730, 312))
    c.link("p3", "d3", "Intentos y\nresultado", lpos=(612, 410), anchor="start")
    c.link("d3", "p4", "Historial", lpos=(745, 425), anchor="start")
    c.link("d3", "p7", "Intentos y\nconfusiones", lpos=(690, 545), anchor="end")
    c.link("p4", "d4", "Dominio y\npróximo repaso", both=True, lpos=(852, 245), anchor="end")
    c.link("d4", "p5", "Estado por\nhabilidad", lpos=(706, 166))
    c.link("d5", "p5", "Actividades y\nhabilidades", lpos=(700, 52))
    c.link("p4", "d6", "Pesos", both=True, lpos=(958, 322))
    c.link("d6", "p5", "Modelo de éxito", via=[(990, 112)], lpos=(800, 112))
    c.link("d4b", "p7", "Estado por habilidad", lpos=(640, 602), anchor="end")
    c.link("p2", "d2", None, both=True)
    c.s.text(372, 608, "Muestras y plantillas", **L, anchor="start")
    return c.s


def dfd2() -> SVG:
    """Explosión del proceso 5.0 (planificación adaptativa)."""
    c = Canvas(1080, 640, "DFD nivel 2: explosión del proceso 5.0")
    s = c.s
    R = 62
    s.rect(225, 30, 640, 580, fill="none", stroke="#888", sw=1.4, rx=16, dash="9 6")
    s.text(245, 50, "5.0 Planificar la sesión adaptativa", size=FS, anchor="start", weight=700, fill=GRAY_D)
    # vecinos del nivel 1
    c.process("p1", 95, 110, 50, "1.0", "Gestionar perfiles", size=FS, fill=G)
    c.process("p6a", 95, 300, 50, "6.0", "Interactuar con el niño", size=FS, fill=G)
    c.store("d4", 110, 450, 200, 38, "D4", "Estado de habilidades")
    c.store("d6", 110, 570, 200, 38, "D6", "Modelo del predictor")
    c.store("d5", 975, 60, 190, 52, "D5", "Catálogo de actividades")
    c.process("p6b", 975, 300, 50, "6.0", "Interactuar con el niño", size=FS, fill=G)
    c.process("p3", 975, 520, 50, "3.0", "Evaluar intentos", size=FS, fill=G)
    # hijos
    c.process("c1", 360, 230, R, "5.1", "Construir el contexto")
    c.process("c2", 610, 120, R, "5.2", "Decidir la acción (reglas)")
    c.process("c3", 420, 480, R, "5.3", "Estimar la probabilidad de éxito")
    c.process("c4", 700, 330, R, "5.4", "Generar candidatas")
    c.process("c5", 720, 520, R, "5.5", "Seleccionar la sesión (MILP)")
    # entradas
    c.link("p1", "c1", "Perfil, edad y\ntiempo de sesión", lpos=(165, 112), anchor="start")
    c.link("p6a", "c1", "Actividad elegida\ny tiempo jugado", lpos=(160, 238), anchor="start")
    c.link("d4", "c1", "Estado por\nhabilidad", lpos=(245, 352), anchor="end")
    c.link("d6", "c3", "Modelo de éxito", lpos=(255, 540), anchor="start")
    c.link("d5", "c4", "Actividades y\nhabilidades", lpos=(930, 162), anchor="start")
    # internos
    c.link("c1", "c2", "Dominio, fatiga\ny fallos", lpos=(470, 152), anchor="end")
    c.link("c1", "c3", "Dominio medio", lpos=(400, 360), anchor="start")
    c.link("c1", "c5", "Tiempo, tamaño y dificultad máxima", via=[(330, 285), (330, 595), (720, 595)], lpos=(520, 595))
    c.link("c2", "c4", "Tipo de\nactividad", lpos=(668, 222), anchor="start")
    c.link("c3", "c5", "Probabilidad\nde éxito", lpos=(570, 488))
    c.link("c4", "c5", "Candidatas", lpos=(722, 425), anchor="start")
    # salidas
    c.link("c2", "p6b", "Decisión adaptativa", via=[(890, 120), (890, 285)], lpos=(780, 105))
    c.link("c5", "p6b", "Ruta del día", via=[(845, 470), (845, 315)], lpos=(853, 395), anchor="start")
    c.link("c5", "p3", "Actividad y secuencia\nesperada", lpos=(848, 560), anchor="middle")
    return s


# Flujos que cruzan la frontera de cada proceso padre (comprobación de balanceo)
BALANCE = {
    "Nivel 0 → Nivel 1": {
        "Niño → 0: Selección de perfil y de actividad": ["Niño → 1.0: Selección de perfil",
                                                         "Niño → 6.0: Elección de actividad"],
        "0 → Niño: Actividad, nota sonora y resultado": ["6.0 → Niño: Actividad, nota sonora y resultado"],
        "Cámara → 0: Fotogramas RGB": ["Cámara → 2.0: Fotogramas RGB"],
        "Acudiente → 0: Perfil, ajustes y solicitud de informe": ["Acudiente → 1.0: Perfil y ajustes",
                                                                  "Acudiente → 7.0: Solicitud de informe"],
        "0 → Acudiente: Informe de progreso": ["7.0 → Acudiente: Informe de progreso"],
    },
    "Nivel 1 → Nivel 2 (proceso 5.0)": {
        "1.0 → 5.0: Perfil, edad y tiempo de sesión": ["1.0 → 5.1"],
        "6.0 → 5.0: Actividad elegida y tiempo jugado": ["6.0 → 5.1"],
        "D4 → 5.0: Estado por habilidad": ["D4 → 5.1"],
        "D6 → 5.0: Modelo de éxito": ["D6 → 5.3"],
        "D5 → 5.0: Actividades y habilidades": ["D5 → 5.4"],
        "5.0 → 6.0: Ruta del día y decisión adaptativa": ["5.2 → 6.0: Decisión adaptativa", "5.5 → 6.0: Ruta del día"],
        "5.0 → 3.0: Actividad y secuencia esperada": ["5.5 → 3.0"],
    },
}

if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    out.mkdir(exist_ok=True)
    for name, fn in (("dfd_nivel0", dfd0), ("dfd_nivel1", dfd1), ("dfd_nivel2", dfd2)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
