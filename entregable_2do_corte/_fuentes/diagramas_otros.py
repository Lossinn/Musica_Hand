"""Figuras de apoyo: linaje del dato, árbol de problemas y arquitectura en capas.

Lienzo de 720 unidades para página vertical (6,5 in útiles): 13,5 unidades ≈ 8,8 pt.
"""
from svglib import SVG, INK, YELLOW, YELLOW_SOFT, GRAY_L, GRAY_D

FS = 13.5


def linaje() -> SVG:
    s = SVG(720, 516, "Linaje del dato: de la cámara al informe para adultos")
    W, H = 162, 112
    xs = [8 + i * (W + 20) for i in range(4)]
    estilo = {"eph": ("#fff", "6 4", GRAY_D), "ses": (YELLOW_SOFT, None, INK), "per": (YELLOW, None, INK)}

    def etapa(x, y, n, t, d, k, loc):
        fill, dash, st = estilo[k]
        s.rect(x, y, W, H, fill=fill, stroke=st, sw=2, rx=10, dash=dash)
        s.add(f'<circle cx="{x + 18}" cy="{y + 18}" r="12" fill="{INK}"/>')
        s.text(x + 18, y + 18, n, size=FS, weight=700, fill="#fff")
        s.text(x + W / 2 + 8, y + 26, t, size=14, weight=700, width=16, valign="middle")
        s.text(x + W / 2, y + 78, d, size=FS, weight=500, fill=GRAY_D)
        s.text(x + W / 2, y + H + 18, loc, size=FS, weight=600, fill=GRAY_D)

    # calibración (fila superior), alimenta la etapa 4
    yc = 34
    s.rect(xs[2], yc, W, 54, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(xs[2] + W / 2, yc + 27, "Calibración\n(3 muestras por nota)", size=FS, weight=600)
    s.rect(xs[3], yc, W, 54, fill=YELLOW, stroke=INK, sw=2, rx=10)
    s.text(xs[3] + W / 2, yc + 27, "Plantillas (JSON\npor perfil)", size=FS, weight=700)
    s.path([(xs[2] + W + 2, yc + 27), (xs[3] - 3, yc + 27)], sw=2)
    y1 = 124
    s.path([(xs[3] + W / 2, yc + 54), (xs[3] + W / 2, y1 - 3)], sw=2)
    # fila 1: etapas 1 a 4
    f1 = [("1", "Cámara web", "Fotogramas RGB\n(24 por segundo)", "eph", "RAM; no se guarda"),
          ("2", "Detector MediaPipe", "21 puntos 3D\npor mano", "eph", "RAM; no se guarda"),
          ("3", "Descriptor invariante", "120 componentes\n(dos manos)", "eph", "RAM; no se guarda"),
          ("4", "Clasificador y estabilizador", "Nota detectada\ny confianza", "ses", "Memoria de la sesión")]
    for i, e in enumerate(f1):
        etapa(xs[i], y1, *e)
        if i < 3:
            s.path([(xs[i] + W + 2, y1 + H / 2), (xs[i + 1] - 3, y1 + H / 2)], sw=2)
    # fila 2: etapas 5 a 7 (de izquierda a derecha)
    y2 = 312
    f2 = [("5", "Evaluación por paso", "Acierto y\nlatencia (ms)", "ses", "Memoria de la actividad"),
          ("6", "Cierre de la actividad", "Intentos y\nresultado", "per", "SQLite: attempts,\nactivity_results"),
          ("7", "Gemelo y predictor", "Dominio, repaso\ny coeficientes", "per", "SQLite: skill_state,\nmeta")]
    for i, e in enumerate(f2):
        etapa(xs[i], y2, *e)
        if i < 2:
            s.path([(xs[i] + W + 2, y2 + H / 2), (xs[i + 1] - 3, y2 + H / 2)], sw=2)
    # de la etapa 4 a la 5
    yb = y1 + H + 40
    s.path([(xs[3] + W / 2, y1 + H + 30), (xs[3] + W / 2, yb + 8), (xs[0] + W / 2, yb + 8), (xs[0] + W / 2, y2 - 3)], sw=2)
    # consumidores
    s.rect(xs[3], y2, W, 50, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(xs[3] + W / 2, y2 + 25, "Planificador\n(MILP y reglas)", size=FS, weight=700)
    s.rect(xs[3], y2 + 62, W, 50, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(xs[3] + W / 2, y2 + 87, "Zona de Padres\n(bajo demanda)", size=FS, weight=700)
    s.path([(xs[2] + W + 2, y2 + 25), (xs[3] - 3, y2 + 25)], sw=2)
    s.path([(xs[2] + W + 10, y2 + 25), (xs[2] + W + 10, y2 + 87), (xs[3] - 3, y2 + 87)], sw=2)
    # leyenda
    ly = 462
    for lx, lab, k in ((8, "Efímero: solo en RAM", "eph"), (236, "De sesión: en memoria", "ses"),
                       (472, "Persistente: disco local", "per")):
        fill, dash, st = estilo[k]
        s.rect(lx, ly, 26, 18, fill=fill, stroke=st, sw=1.6, rx=4, dash=dash)
        s.text(lx + 34, ly + 9, lab, size=FS, anchor="start", weight=600)
    s.text(360, 502, "Ningún fotograma se escribe en disco: solo coordenadas de 21 puntos por mano.",
           size=FS, weight=600, fill=GRAY_D, italic=True)
    return s


def arbol_problemas() -> SVG:
    s = SVG(720, 420, "Árbol de problemas")
    w, g = 168, 16

    def box(x, y, h, t, fill="#fff", size=FS, weight=500, ww=w, chars=20):
        s.rect(x, y, ww, h, fill=fill, stroke=INK, sw=1.8, rx=9)
        s.text(x + ww / 2, y + h / 2, t, size=size, weight=weight, width=chars)

    s.text(360, 14, "EFECTOS", size=14, weight=700, fill=GRAY_D)
    efectos = ["Retroalimentación tardía y abandono de la práctica",
               "Acceso desigual a una educación musical con seguimiento",
               "Docentes sin datos objetivos para decidir qué reforzar",
               "Olvido entre clases por falta de repaso programado"]
    for i, t in enumerate(efectos):
        x = i * (w + g)
        box(x, 30, 84, t, fill=GRAY_L)
        s.path([(x + w / 2, 186), (x + w / 2, 118)], sw=1.8)
    s.text(360, 152, "PROBLEMA CENTRAL", size=14, weight=700, fill=GRAY_D)
    box(0, 186, 70, "Niños de 3 a 12 años de Montería aprenden las notas musicales sin retroalimentación "
        "individual inmediata ni registro objetivo de su progreso", fill=YELLOW, size=15, weight=700, ww=720, chars=70)
    s.text(360, 290, "CAUSAS", size=14, weight=700, fill=GRAY_D)
    causas = ["Atención docente de uno a muchos en el aula",
              "Evaluación manual y subjetiva, sin registro por nota",
              "Conectividad: 47,2 % de los hogares de Córdoba con internet",
              "Pocas herramientas adaptativas sin nube ni cuentas para menores"]
    for i, t in enumerate(causas):
        x = i * (w + g)
        box(x, 312, 100, t)
        s.path([(x + w / 2, 312), (x + w / 2, 260)], sw=1.8)
    return s


def arquitectura() -> SVG:
    s = SVG(720, 558, "Arquitectura en cinco capas de HandSingKids7")
    capas = [
        ("INTERFAZ", "ui/screens (14 pantallas), ui/widgets, ui/theme", "PySide6", "#fff"),
        ("APLICACIÓN", "app.py (contexto, navegación y sesión), core/config, core/events", "Python", GRAY_L),
        ("DOMINIO", "domain/entities (perfil, habilidad, actividad, intento), domain/notes (DO3 a DO4)", "Python", "#fff"),
        ("INTELIGENCIA", "intelligence/ (digital_twin, predictor, optimizer); learning/ (mastery, adaptation, "
                         "generator, evaluation, rhythm, progression, session_flow)", "NumPy, PuLP (CBC)", YELLOW_SOFT),
        ("INFRAESTRUCTURA", "vision/ (camera, detector, features, classifier, stabilizer, templates, service); "
                            "music/ (synth, audio, engine); data/ (database, repositories, seed, melodies)",
         "OpenCV, MediaPipe, SQLite", GRAY_L),
    ]
    y, gap = 8, 14
    for n, mods, tech, fill in capas:
        hh = 112 if n == "INFRAESTRUCTURA" else 92
        s.rect(40, y, 600, hh, fill=fill, stroke=INK, sw=2, rx=10)
        s.text(118, y + hh / 2, n, size=14, weight=700)
        s.line(196, y + 10, 196, y + hh - 10, sw=1, stroke="#999")
        s.text(418, y + (36 if hh == 92 else 44), mods, size=FS, weight=500, width=52)
        s.text(418, y + hh - 14, tech, size=FS, weight=700, fill=GRAY_D)
        if n != "INFRAESTRUCTURA":
            s.path([(340, y + hh), (340, y + hh + gap - 1)], sw=2)
        y += hh + gap
    s.rect(652, 8, 60, y - gap - 8, fill="#fff", stroke=INK, sw=1.6, rx=8, dash="6 4")
    s.text(682, (y - gap) / 2 + 4, "Bus de eventos (core/events)", size=FS, weight=700, rotate=-90)
    s.text(16, (y - gap) / 2 + 4, "Dependencias solo hacia abajo", size=FS, weight=600, rotate=-90, fill=GRAY_D)
    return s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    for name, fn in (("linaje_dato", linaje), ("arbol_problemas", arbol_problemas), ("arquitectura_capas", arquitectura)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
