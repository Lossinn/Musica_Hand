"""Figuras de apoyo: linaje del dato, árbol de problemas y arquitectura en capas."""
from svglib import SVG, INK, YELLOW, YELLOW_SOFT, GRAY_L, GRAY_D, GRAY_M, TEAL, RED


def linaje() -> SVG:
    s = SVG(1400, 600, "Linaje del dato: de la cámara al informe para adultos")
    xs = [20 + i * 192 for i in range(7)]
    W, Hh, Y0 = 158, 150, 70
    etapas = [
        ("1", "Cámara web", "Fotogramas RGB\n(~24 fps)", "eph", "RAM; no se guarda"),
        ("2", "Detector MediaPipe", "21 puntos 3D\npor mano", "eph", "RAM; no se guarda"),
        ("3", "Descriptor invariante", "120 componentes\n(2 manos)", "eph", "RAM; no se guarda"),
        ("4", "Clasificador y estabilizador", "Nota detectada\n+ confianza", "ses", "Memoria de la sesión"),
        ("5", "Evaluación por paso", "Acierto y\nlatencia (ms)", "ses", "Memoria de la actividad"),
        ("6", "Cierre de la actividad", "Intentos y resultado\nde la actividad", "per", "SQLite: attempts,\nactivity_results"),
        ("7", "Gemelo y predictor", "Dominio, repaso\ny coeficientes", "per", "SQLite: skill_state,\nmeta"),
    ]
    estilo = {"eph": ("#fff", "6 4", GRAY_D), "ses": (YELLOW_SOFT, None, INK), "per": (YELLOW, None, INK)}
    for i, (n, t, d, k, loc) in enumerate(etapas):
        fill, dash, st = estilo[k]
        s.rect(xs[i], Y0, W, Hh, fill=fill, stroke=st, sw=2, rx=10, dash=dash)
        s.add(f'<circle cx="{xs[i] + 22}" cy="{Y0 + 22}" r="14" fill="{INK}"/>')
        s.text(xs[i] + 22, Y0 + 22, n, size=13, weight=700, fill="#fff")
        s.text(xs[i] + W / 2, Y0 + 62, t, size=13, weight=700, width=17)
        s.text(xs[i] + W / 2, Y0 + 104, d, size=11.5, weight=500, fill=GRAY_D)
        s.text(xs[i] + W / 2, Y0 + Hh + 26, loc, size=11, weight=600, fill=GRAY_D)
        if i < len(etapas) - 1:
            s.path([(xs[i] + W + 2, Y0 + 75), (xs[i + 1] - 3, Y0 + 75)], sw=2)
    # consumidores (leen el estado persistente de la etapa 7)
    s.path([(xs[6] + 79, Y0 + Hh + 52), (xs[6] + 79, 318)], sw=2, end=None)
    s.path([(xs[6] + 79, 318), (xs[5] + 75, 318), (xs[5] + 75, 350)], sw=2)
    s.path([(xs[6] + 79, 318), (xs[6] + 115, 318), (xs[6] + 115, 350)], sw=2)
    s.rect(xs[5] - 25, 350, 200, 66, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(xs[5] + 75, 383, "Planificador de sesión\n(MILP y reglas)", size=12, weight=700)
    s.rect(xs[6] + 15, 350, 200, 66, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(xs[6] + 115, 383, "Zona de Padres\n(consulta bajo demanda)", size=12, weight=700)
    # calibración
    s.rect(300, 350, 190, 66, fill="#fff", stroke=INK, sw=2, rx=10)
    s.text(395, 383, "Calibración\n(3 muestras por nota)", size=12, weight=700)
    s.rect(540, 350, 190, 66, fill=YELLOW, stroke=INK, sw=2, rx=10)
    s.text(635, 383, "Plantillas de calibración\n(archivo JSON por perfil)", size=12, weight=700)
    s.path([(492, 383), (538, 383)], sw=2)
    s.path([(635, 350), (635, Y0 + Hh + 40)], sw=2)
    s.text(645, 318, "se compara en la etapa 4", size=11, anchor="start", weight=500, fill=GRAY_D, italic=True)
    # leyenda
    lx = 20
    for lab, (fill, dash, st) in (("Efímero: solo en RAM", estilo["eph"]), ("De sesión: memoria del proceso", estilo["ses"]),
                                  ("Persistente: disco local del usuario", estilo["per"])):
        s.rect(lx, 548, 26, 18, fill=fill, stroke=st, sw=1.6, rx=4, dash=dash)
        s.text(lx + 36, 557, lab, size=12, anchor="start", weight=600)
        lx += 330
    s.text(700, 30, "Ningún fotograma ni imagen se escribe en disco: solo coordenadas numéricas de 21 puntos por mano.",
           size=12.5, weight=600, fill=GRAY_D, italic=True)
    return s


def arbol_problemas() -> SVG:
    s = SVG(1400, 800, "Árbol de problemas")
    def box(x, y, w, h, t, fill="#fff", stroke=INK, size=13.5, weight=500, chars=None):
        s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.8, rx=10)
        s.text(x + w / 2, y + h / 2, t, size=size, weight=weight, width=chars or int(w / (size * 0.56)) - 2)
    s.text(700, 28, "EFECTOS", size=14, weight=700, fill=GRAY_D)
    efectos = ["Retroalimentación tardía y abandono de la práctica musical",
               "Brecha de acceso a una educación musical con seguimiento individual",
               "Docentes sin datos objetivos para decidir qué reforzar",
               "Olvido entre clases por falta de repaso programado"]
    for i, t in enumerate(efectos):
        box(20 + i * 345, 50, 320, 92, t, fill=GRAY_L)
        s.path([(180 + i * 345, 300), (180 + i * 345, 147)], sw=1.8)
    box(20, 300, 1360, 130,
        "Niños de 3 a 12 años de Montería aprenden las notas musicales sin retroalimentación individual inmediata "
        "ni registro objetivo de su progreso", fill=YELLOW, size=17, weight=700)
    s.text(700, 272, "PROBLEMA CENTRAL", size=14, weight=700, fill=GRAY_D)
    s.text(700, 500, "CAUSAS", size=14, weight=700, fill=GRAY_D)
    causas = ["Atención docente de uno a muchos en el aula de música",
              "Evaluación manual y subjetiva, sin registro por nota",
              "Conectividad limitada: 47,2 % de los hogares de Córdoba con internet (DANE, 2024)",
              "Pocas herramientas adaptativas que funcionen sin nube ni cuentas para menores"]
    for i, t in enumerate(causas):
        box(20 + i * 345, 540, 320, 120, t, fill="#fff")
        s.path([(180 + i * 345, 535), (180 + i * 345, 435)] if False else [(180 + i * 345, 540), (180 + i * 345, 435)], sw=1.8)
    s.text(700, 725, "Las causas 1 y 2 se observan en el proceso actual (As-Is); la causa 3 proviene de la ENTIC Hogares 2024 del DANE; "
           "la causa 4 es la brecha identificada en los 15 estudios revisados.", size=12, weight=500, fill=GRAY_D, italic=True, width=150)
    return s


def arquitectura() -> SVG:
    s = SVG(1400, 640, "Arquitectura en cinco capas de HandSingKids7")
    capas = [
        ("INTERFAZ", "ui/screens (14 pantallas) · ui/widgets · ui/theme", "PySide6", "#fff"),
        ("APLICACIÓN", "app.py (contexto, navegación y sesión) · core/config · core/events (bus de eventos)", "Python", GRAY_L),
        ("DOMINIO", "domain/entities (perfil, habilidad, actividad, intento) · domain/notes (8 notas, DO3 a DO4)", "Python", "#fff"),
        ("INTELIGENCIA", "intelligence/(digital_twin, predictor, optimizer) · learning/(mastery, adaptation, generator, "
                         "evaluation, rhythm, progression, session_flow)", "NumPy · PuLP (CBC)", YELLOW_SOFT),
        ("INFRAESTRUCTURA", "vision/(camera, detector, features, classifier, stabilizer, templates, service) · "
                            "music/(synth, audio, engine) · data/(database, repositories, seed, melodies)",
         "OpenCV · MediaPipe · SQLite", GRAY_L),
    ]
    y = 30
    for n, mods, tech, fill in capas:
        s.rect(130, y, 1150, 100, fill=fill, stroke=INK, sw=2, rx=10)
        s.text(255, y + 50, n, size=16, weight=700)
        s.text(780, y + 38, mods, size=13, weight=500, width=84)
        s.text(780, y + 80, tech, size=12.5, weight=700, fill=GRAY_D)
        if n != "INFRAESTRUCTURA":
            s.path([(700, y + 100), (700, y + 118)], sw=2)
        y += 118
    s.rect(1310, 30, 70, 572, fill="#fff", stroke=INK, sw=1.6, rx=8, dash="6 4")
    s.text(1345, 316, "Bus de eventos", size=13, weight=700, rotate=-90)
    s.text(70, 316, "Dependencias solo hacia abajo", size=12.5, weight=600, rotate=-90, fill=GRAY_D)
    s.path([(40, 60), (40, 570)], sw=2)
    return s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    for name, fn in (("linaje_dato", linaje), ("arbol_problemas", arbol_problemas), ("arquitectura_capas", arquitectura)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
