"""DFD (notación Yourdon-DeMarco) de Hand Sing Kids, niveles 0, 1 y 2.\n\nLos almacenes D1-D6 son tablas reales de SQLite (o archivos) de HandSingKids7:\n  D1 profiles, rewards, profile_achievements      D4 skill_state\n  D2 plantillas de calibración (JSON)             D5 skills, activities, achievements\n  D3 sessions, attempts, activity_results         D6 meta (fila `predictor_<id>`)\n\nEl balanceo entre niveles se comprueba en `BALANCE` (abajo) y se imprime al\nejecutar el módulo: los flujos que cruzan la frontera de un proceso en un nivel\nson exactamente los que entran y salen de sus hijos en el nivel siguiente.\n"""
from __future__ import annotations

import math

from svglib import SVG, GRAY_D, GRAY_L


class Canvas:
    """SVG + registro de nodos para conectar flujos por el borde de cada figura."""

    def __init__(self, w: int, h: int, title: str) -> None:
        self.s = SVG(w, h, title)
        self.nodes: dict[str, tuple] = {}

    # ------------------------------------------------------------- nodos
    def process(self, key, cx, cy, r, num, label, *, size=11, fill="#fff"):
        self.nodes[key] = ("c", cx, cy, r)
        self.s.process(cx, cy, r, num, label, size=size, fill=fill)

    def entity(self, key, cx, cy, w, h, label, *, size=13):
        self.nodes[key] = ("r", cx, cy, w, h)
        self.s.entity(cx, cy, w, h, label, size=size)

    def store(self, key, cx, cy, w, h, code, label, *, size=11):
        self.nodes[key] = ("r", cx, cy, w, h)
        self.s.store(cx, cy, w, h, code, label, size=size)

    # -------------------------------------------------------- geometría
    def _center(self, k):
        n = self.nodes[k]
        return n[1], n[2]

    def _edge(self, k, toward, off=0.0, sign=1, line=None):
        """Punto de conexión en el borde de `k`. Sin `line`, apunta al centro de\n        `toward`; con `line=(u, p)` (dirección y normal del flujo) el punto es el de\n        una recta paralela a la línea de centros, desplazada `off` (flujos paralelos)."""
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

    def link(self, a, b, label=None, *, off=0.0, via=None, both=False, size=10,
             lpos=None, anchor="middle"):
        """Flujo de `a` hacia `b`. `via` = puntos intermedios (codo). `off` separa\n        flujos paralelos. `lpos` = (x, y) absoluto de la etiqueta."""
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
        if via:
            pts = [p0, *via, p1]
        else:
            pts = [p0, p1]
        pts = [(round(x, 1), round(y, 1)) for x, y in pts]
        if lpos is None:
            # punto medio del segmento más largo
            best = max(range(len(pts) - 1), key=lambda i: math.dist(pts[i], pts[i + 1]))
            lpos = ((pts[best][0] + pts[best + 1][0]) / 2, (pts[best][1] + pts[best + 1][1]) / 2)
        self.s.dflow(pts, label, lx=lpos[0], ly=lpos[1], size=size, anchor=anchor, both=both)


# =====================================================================
def dfd0() -> SVG:
    c = Canvas(1100, 520, "DFD nivel 0: diagrama de contexto")
    s = c.s
    c.process("0", 550, 250, 108, "0", "Sistema Hand Sing Kids (aplicación local)", size=14)
    c.entity("nino", 140, 120, 180, 64, "Niño o niña", size=14)
    c.entity("cam", 140, 390, 180, 64, "Cámara web", size=14)
    c.entity("adulto", 960, 250, 200, 76, "Padre, madre o docente", size=14)
    c.link("nino", "0", "Selección de perfil\ny de actividad", off=-14, size=11.5, lpos=(300, 130))
    c.link("0", "nino", "Actividad, nota sonora,\nresultado y estrellas", off=-14, size=11.5, lpos=(420, 228))
    c.link("cam", "0", "Fotogramas RGB\nde las manos", size=11.5, lpos=(300, 360))
    c.link("adulto", "0", "Perfil, ajustes y\nsolicitud de informe", off=-16, size=11.5, lpos=(780, 205))
    c.link("0", "adulto", "Informe de progreso\ny diagnóstico", off=-16, size=11.5, lpos=(780, 300))
    s.text(550, 478, "La aplicación no se comunica con servicios externos: el diagrama no tiene entidades en la nube.",
           size=12, weight=500, fill=GRAY_D, italic=True)
    return s


def dfd1() -> SVG:
    c = Canvas(1420, 930, "DFD nivel 1: descomposición en siete procesos")
    s = c.s
    R = 64
    c.entity("nino", 85, 250, 130, 60, "Niño o niña")
    c.entity("cam", 85, 690, 130, 60, "Cámara web")
    c.entity("adulto", 1335, 690, 150, 70, "Padre, madre o docente")
    c.process("p1", 330, 120, R, "1.0", "Gestionar perfiles y ajustes")
    c.process("p5", 680, 120, R, "5.0", "Planificar la sesión adaptativa")
    c.process("p6", 330, 400, R, "6.0", "Interactuar con el niño (interfaz y audio)")
    c.process("p3", 680, 400, R, "3.0", "Evaluar y registrar intentos")
    c.process("p4", 1030, 400, R, "4.0", "Actualizar el gemelo digital")
    c.process("p2", 330, 690, R, "2.0", "Reconocer señas")
    c.process("p7", 1030, 690, R, "7.0", "Generar el informe para adultos")
    c.store("d1", 110, 50, 180, 40, "D1", "Perfiles y logros")
    c.store("d5", 1040, 60, 200, 40, "D5", "Catálogo de actividades")
    c.store("d6", 1040, 215, 200, 40, "D6", "Modelo del predictor")
    c.store("d4b", 900, 305, 200, 40, "D4", "Estado de habilidades")
    c.store("d4", 1030, 550, 200, 40, "D4", "Estado de habilidades")
    c.store("d3", 680, 590, 200, 40, "D3", "Intentos y resultados")
    c.store("d2", 330, 850, 210, 40, "D2", "Plantillas de calibración")
    # entradas del niño / salidas hacia el niño
    c.link("nino", "p1", "Selección de perfil", lpos=(180, 175))
    c.link("nino", "p6", "Elección de actividad\no modo de juego", off=-12, lpos=(248, 312), anchor="start")
    c.link("p6", "nino", "Actividad, nota sonora,\nresultado y estrellas", off=-12, lpos=(205, 338), anchor="end")
    c.link("cam", "p2", "Fotogramas RGB", lpos=(205, 668))
    c.link("adulto", "p1", "Datos del perfil y ajustes", via=[(1335, 20), (330, 20)], lpos=(830, 10))
    c.link("d1", "p1", None, both=True)
    s.text(150, 88, "Perfil, estrellas y racha", size=10, weight=500, fill=GRAY_D)
    c.link("p1", "p5", "Perfil activo, edad y\ntiempo de sesión", lpos=(505, 92))
    c.link("p2", "p1", "Calibración completada", via=[(215, 640), (215, 150)], lpos=(227, 560), anchor="start")
    # planificación <-> interfaz
    c.link("p5", "p6", "Ruta del día y decisión\nadaptativa", off=10, lpos=(430, 235), anchor="end")
    c.link("p6", "p5", "Actividad elegida y\ntiempo jugado", off=10, lpos=(545, 300), anchor="start")
    c.link("p5", "p3", "Actividad y\nsecuencia\nesperada", lpos=(692, 255), anchor="start")
    # visión → evaluación → interfaz / gemelo
    c.link("p2", "p3", "Gesto confirmado\ny confianza", lpos=(500, 590))
    c.link("p3", "p6", "Acierto o fallo\ny puntaje", lpos=(505, 372))
    c.link("p3", "p4", "Resultado de la actividad\ny aciertos por nota", lpos=(855, 372))
    # almacenes
    c.link("p2", "d2", None, both=True)
    s.text(340, 800, "Muestras y plantillas", size=10, weight=500, fill=GRAY_D, anchor="start")
    c.link("p3", "d3", "Intentos y resultado\nde la actividad", lpos=(692, 505), anchor="start")
    c.link("d3", "p4", "Historial de intentos", lpos=(905, 490), anchor="start")
    c.link("p4", "d4", None, both=True)
    s.text(1044, 480, "Dominio, retención\ny próximo repaso", size=10, weight=500, fill=GRAY_D, anchor="start")
    c.link("p4", "d6", None, both=True)
    s.text(1044, 330, "Pesos del predictor", size=10, weight=500, fill=GRAY_D, anchor="start")
    c.link("d6", "p5", "Modelo de éxito", lpos=(865, 165))
    c.link("d5", "p5", "Actividades y habilidades", lpos=(885, 62))
    c.link("d4b", "p5", "Estado por\nhabilidad", lpos=(836, 235), anchor="start")
    # informe
    c.link("d3", "p7", "Intentos y confusiones", lpos=(860, 665), anchor="middle")
    c.link("d4", "p7", "Estado por habilidad", lpos=(1042, 625), anchor="start")
    c.link("adulto", "p7", "Solicitud de informe", off=-14, lpos=(1215, 730))
    c.link("p7", "adulto", "Informe de progreso\ny diagnóstico", off=-14, lpos=(1215, 650))

    s.text(710, 905, "Los almacenes D4 aparecen dos veces por legibilidad. No hay flujos hacia servicios externos.",
           size=11, weight=500, fill=GRAY_D, italic=True)
    return s


def dfd2() -> SVG:
    """Explosión del proceso 5.0 (planificación adaptativa)."""
    c = Canvas(1400, 900, "DFD nivel 2: explosión del proceso 5.0")
    s = c.s
    R = 68
    G = "#ECECEC"
    # frontera del proceso 5.0
    s.rect(290, 40, 850, 790, fill="none", stroke="#888", sw=1.4, rx=16, dash="9 6")
    s.text(312, 60, "5.0 Planificar la sesión adaptativa", size=12, anchor="start", weight=700, fill=GRAY_D)
    # vecinos del nivel 1 (frontera)
    c.process("p1", 110, 150, 52, "1.0", "Gestionar perfiles", size=10, fill=G)
    c.process("p6a", 110, 330, 52, "6.0", "Interactuar con el niño", size=10, fill=G)
    c.store("d4b", 140, 520, 210, 40, "D4", "Estado de habilidades")
    c.store("d6", 140, 700, 210, 40, "D6", "Modelo del predictor")
    c.store("d5", 1290, 110, 210, 40, "D5", "Catálogo de actividades")
    c.process("p6b", 1290, 340, 52, "6.0", "Interactuar con el niño", size=10, fill=G)
    c.process("p3", 1290, 690, 52, "3.0", "Evaluar intentos", size=10, fill=G)
    # hijos
    c.process("c1", 450, 290, R, "5.1", "Construir el contexto")
    c.process("c2", 760, 160, R, "5.2", "Decidir la acción (reglas)")
    c.process("c3", 560, 600, R, "5.3", "Estimar la probabilidad de éxito")
    c.process("c4", 850, 400, R, "5.4", "Generar y reunir candidatas")
    c.process("c5", 930, 650, R, "5.5", "Seleccionar la sesión (MILP)")
    # entradas
    c.link("p1", "c1", "Perfil activo, edad y\ntiempo de sesión", lpos=(270, 190), anchor="end")
    c.link("p6a", "c1", "Actividad elegida y\ntiempo jugado", lpos=(265, 300), anchor="end")
    c.link("d4b", "c1", "Estado por habilidad", lpos=(285, 440), anchor="start")
    c.link("d6", "c3", "Modelo de éxito", lpos=(330, 640), anchor="start")
    c.link("d5", "c4", "Actividades y habilidades", lpos=(1080, 235), anchor="middle")
    # internos
    c.link("c1", "c2", "Contexto: dominio,\nfatiga y fallos", lpos=(590, 195))
    c.link("c1", "c3", "Dominio medio\npor habilidad", lpos=(520, 430), anchor="start")
    c.link("c1", "c5", "Tiempo, tamaño y\ndificultad máxima", via=[(410, 705), (862, 705)], lpos=(640, 726))

    c.link("c2", "c4", "Tipo de actividad\nrequerido", lpos=(860, 270), anchor="start")
    c.link("c3", "c5", "Probabilidad de éxito", lpos=(745, 590))
    c.link("c4", "c5", "Actividades\ncandidatas", lpos=(910, 530), anchor="start")
    # salidas
    c.link("c2", "p6b", "Decisión adaptativa", via=[(1100, 160), (1290, 160)], lpos=(1040, 145))

    c.link("c5", "p6b", "Ruta del día", via=[(1110, 600), (1110, 360)], lpos=(1122, 480), anchor="start")

    c.link("c5", "p3", "Actividad y secuencia\nesperada", lpos=(1120, 715), anchor="middle")
    s.text(710, 862, "Las figuras grises son los procesos y almacenes vecinos del nivel 1.",
           size=11, weight=500, fill=GRAY_D, italic=True)
    return s


# Flujos que cruzan la frontera de cada proceso padre (comprobación de balanceo)
BALANCE = {
    "Nivel 0 → Nivel 1": {
        "Niño → 0: Selección de perfil y de actividad": ["Niño → 1.0: Selección de perfil",
                                                         "Niño → 6.0: Elección de actividad o modo de juego"],
        "0 → Niño: Actividad, nota sonora, resultado y estrellas": ["6.0 → Niño: Actividad, nota sonora, resultado y estrellas"],
        "Cámara → 0: Fotogramas RGB de las manos": ["Cámara → 2.0: Fotogramas RGB"],
        "Adulto → 0: Perfil, ajustes y solicitud de informe": ["Adulto → 1.0: Datos del perfil y ajustes",
                                                               "Adulto → 7.0: Solicitud de informe"],
        "0 → Adulto: Informe de progreso y diagnóstico": ["7.0 → Adulto: Informe de progreso y diagnóstico"],
    },
    "Nivel 1 → Nivel 2 (proceso 5.0)": {
        "1.0 → 5.0: Perfil activo, edad y tiempo de sesión": ["1.0 → 5.1"],
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
    for nivel, d in BALANCE.items():
        print(nivel)
        for padre, hijos in d.items():
            print("  ", padre, "=>", "; ".join(hijos))
