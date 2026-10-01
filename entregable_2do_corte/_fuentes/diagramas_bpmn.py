"""BPMN 2.0: proceso actual (As-Is) y proceso propuesto (To-Be) de Hand Sing Kids.

Los pasos del To-Be siguen el código de HandSingKids7 (ciclo de una nota:
cámara → detector → descriptor → clasificador → estabilizador → evaluador →
registro → gemelo digital → motor adaptativo → optimizador).
"""
from svglib import (SVG, INK, YELLOW, YELLOW_SOFT, GRAY_L, GRAY_D, RED, TEAL)


def as_is() -> SVG:
    s = SVG(1400, 705, "BPMN 2.0 As-Is: enseñanza de una nota musical en una escuela de música")
    s.pool(10, 10, 1380, 410, "Escuela de música", [("Docente", 205), ("Niño o niña", 205)])
    # --- carril Docente (y = 125) ---
    s.event(100, 125, "start", "Inicia la clase", lw=12)
    s.task(240, 125, 120, 62, "Explica y demuestra la seña de la nota", icon="user")
    s.task(440, 125, 140, 62, "Observa y corrige a cada niño, uno por uno", icon="user", fill="#FBE9E7")
    s.gateway(600, 125, "xor", "¿Acertó?", lw=10, lpos="below")
    s.task(730, 125, 120, 62, "Anota el avance en el cuaderno", icon="user", fill="#FBE9E7")
    s.task(890, 125, 150, 62, "Informa al acudiente de forma verbal o por mensaje", icon="user", fill="#FBE9E7")
    s.event(1050, 125, "end", "Fin de la clase", lw=12)
    # --- carril Niño (y = 330) ---
    s.task(240, 330, 120, 62, "Imita la seña y entona la nota", icon="user")
    # flujos
    s.flow([(115, 125), (180, 125)])
    s.flow([(240, 156), (240, 299)])
    s.flow([(300, 330), (440, 330), (440, 156)])
    s.flow([(510, 125), (574, 125)])
    s.flow([(626, 125), (670, 125)], "Sí", lx=648, ly=112)
    s.flow([(600, 99), (600, 52), (240, 52), (240, 94)], "No: se repite la demostración", lx=420, ly=40)
    s.flow([(790, 125), (815, 125)])
    s.flow([(965, 125), (1035, 125)])
    # --- pool acudiente ---
    s.pool(10, 455, 1380, 150, "Acudiente")
    s.event(890, 530, "msg-start", "Recibe informe", lw=12)
    s.task(1040, 530, 150, 62, "Lee un informe sin detalle por nota ni evidencia", icon="user", fill="#FBE9E7")
    s.event(1190, 530, "timer", "Hasta la próxima clase", lw=12)
    s.event(1310, 530, "end", "Sin repaso programado", lw=14)
    s.flow([(905, 530), (965, 530)])
    s.flow([(1115, 530), (1175, 530)])
    s.flow([(1205, 530), (1295, 530)])
    s.msg([(890, 156), (890, 515)], "Informe verbal o mensaje", lx=898, ly=300)
    # --- cuellos de botella ---
    for n, (x, y) in enumerate([(510, 92), (640, 100), (786, 92), (1115, 498), (1205, 498)], 1):
        s.badge(x, y, n)
    s.rect(10, 617, 1380, 82, fill="#FFF8F7", stroke=RED, sw=1.2, rx=6, dash="5 3")
    items = [
        "1  Atención individual 1:N: la corrección depende de la observación del docente.",
        "2  Criterio de acierto subjetivo: no se miden latencia, confianza ni confusiones entre notas.",
        "3  Registro manual en cuaderno: los datos no se agregan ni se consultan por habilidad.",
        "4  Retroalimentación tardía al acudiente, sin detalle por nota ni evidencia del avance.",
        "5  Sin repaso espaciado: el olvido entre clases no se mide ni se programa.",
    ]
    for i, t in enumerate(items):
        col, row = divmod(i, 3)
        s.text(28 + col * 690, 635 + row * 22, t, size=11.5, anchor="start", weight=500)
    return s


def to_be() -> SVG:
    s = SVG(1420, 815, "BPMN 2.0 To-Be: sesión de práctica con Hand Sing Kids")
    Y = YELLOW_SOFT
    # ----------------------------------------------------------- Pool A: niño
    s.pool(10, 10, 1400, 110, "Niño o niña")
    s.event(84, 62, "start", "Abre la app", lw=12)
    s.task(160, 62, 100, 54, "Elige su perfil", icon="user")
    s.task(285, 62, 118, 54, "Ve la actividad y la nota", icon="user")
    s.task(420, 62, 120, 54, "Hace la seña ante la cámara", icon="user")
    s.task(850, 62, 130, 54, "Oye la nota y ve el resultado", icon="user")
    s.event(1348, 62, "end", "Fin de la sesión", lw=12, lpos="above")
    s.flow([(99, 62), (110, 62)]); s.flow([(210, 62), (226, 62)]); s.flow([(344, 62), (360, 62)])
    s.flow([(915, 62), (1333, 62)])
    # --------------------------------------------------------- Pool B: sistema
    s.pool(10, 135, 1400, 530, "Sistema Hand Sing Kids (local)",
           [("Planificación", 150), ("Visión artificial", 175), ("Evaluación y datos", 205)])
    # Planificación (y = 215)
    s.task(180, 215, 130, 60, "Planificar la ruta del día (MILP)", fill=Y, icon="svc")
    s.task(340, 215, 130, 60, "Presentar la actividad y la nota esperada", fill=Y, icon="svc")
    s.task(1120, 215, 140, 60, "Decidir la siguiente acción (reglas)", fill=Y, icon="svc")
    s.gateway(1255, 215, "xor", "¿F ≥ 1?", lw=10, lpos="below")
    s.task(1350, 215, 96, 60, "Cerrar y sugerir descanso", fill=Y, icon="svc", size=11)
    s.flow([(245, 215), (275, 215)])
    s.flow([(1190, 215), (1229, 215)])
    s.flow([(1281, 215), (1302, 215)], "Sí", lx=1292, ly=203)
    s.flow([(1255, 189), (1255, 158), (392, 158), (392, 185)], "No: siguiente actividad", lx=820, ly=148)
    # Visión (y = 360)
    s.task(420, 360, 140, 60, "Detectar manos y extraer el descriptor (120)", fill=Y, icon="svc", size=11)
    s.task(570, 360, 122, 60, "Clasificar y estabilizar el gesto", fill=Y, icon="svc")
    s.gateway(680, 360, "xor", "¿Seña aceptada?", lw=12)
    s.text(680, 297, "d ≤ 0,95 · P ≥ 0,55 · margen ≥ 0,08", size=9.5, weight=500, fill=GRAY_D)
    s.gateway(750, 360, "par")
    s.task(850, 360, 100, 56, "Sintetizar la nota y dibujar", fill=Y, icon="svc", size=11)
    s.event(955, 360, "end", "Retro entregada", lw=10, size=10)
    s.flow([(490, 360), (509, 360)]); s.flow([(631, 360), (654, 360)])
    s.flow([(706, 360), (724, 360)], "Sí", lx=715, ly=347)
    s.flow([(776, 360), (800, 360)]); s.flow([(900, 360), (940, 360)])
    s.event(540, 420, "timer", "Siguiente fotograma (~42 ms)", lw=40, size=10, lpos="below")
    s.flow([(680, 386), (680, 420), (555, 420)], "No", lx=689, ly=406)
    s.flow([(525, 420), (420, 420), (420, 390)])
    # Evaluación y datos (y = 562)
    s.task(750, 562, 110, 60, "Evaluar el paso frente a la nota esperada", fill=Y, icon="svc", size=11)
    s.gateway(865, 562, "xor", "¿Terminó la actividad?", lw=12, lpos="above")
    s.gateway(940, 562, "inc")
    s.task(1045, 510, 130, 46, "Dar estrellas y logros (si corresponde)", fill=Y, icon="svc", size=10.5)
    s.task(1045, 562, 130, 46, "Actualizar dominio y repaso (siempre)", fill=Y, icon="svc", size=10.5)
    s.task(1045, 614, 130, 46, "Abrir habilidades nuevas (si hay prerrequisitos)", fill=Y, icon="svc", size=10.5)
    s.gateway(1160, 562, "inc")
    s.flow([(750, 386), (750, 532)])
    s.flow([(805, 562), (839, 562)])
    s.flow([(891, 562), (914, 562)], "Sí", lx=902, ly=549)
    s.flow([(940, 536), (940, 510), (980, 510)])
    s.flow([(966, 562), (980, 562)])
    s.flow([(940, 588), (940, 614), (980, 614)])
    s.flow([(1110, 510), (1160, 510), (1160, 536)])
    s.flow([(1110, 562), (1134, 562)])
    s.flow([(1110, 614), (1160, 614), (1160, 588)])
    s.flow([(1186, 562), (1192, 562), (1192, 245)])
    s.flow([(865, 588), (865, 648), (92, 648), (92, 158), (392, 158)], "No: siguiente nota", lx=560, ly=638)
    s.task(405, 562, 150, 60, "Construir el gemelo digital y el informe (bajo demanda)", fill=Y, icon="svc", size=11)
    # mensajes entre pools
    s.msg([(160, 89), (160, 185)], "Inicio de sesión", lx=168, ly=130)
    s.msg([(338, 185), (338, 89)], "Actividad propuesta", lx=346, ly=112)
    s.msg([(420, 89), (420, 330)], "Fotogramas RGB (solo en RAM)", lx=428, ly=245)
    s.msg([(850, 332), (850, 89)], "Nota sonora", lx=858, ly=180)
    s.msg([(1350, 185), (1350, 79)], "Sugerencia de descanso", lx=1342, ly=112, anchor="end")
    # ----------------------------------------------------------- Pool C: adulto
    s.pool(10, 680, 1400, 125, "Padre, madre o docente")
    s.event(200, 750, "start", "Quiere ver el avance", lw=14)
    s.task(330, 750, 130, 56, "Consulta la Zona de Padres", icon="user")
    s.event(470, 750, "msg-catch", "Recibe el informe", lw=14)
    s.event(600, 750, "end", "Decide cómo reforzar", lw=14)
    s.flow([(215, 750), (265, 750)]); s.flow([(395, 750), (455, 750)]); s.flow([(485, 750), (585, 750)])
    s.msg([(340, 722), (340, 592)], "Solicitud", lx=332, ly=700, anchor="end")
    s.msg([(470, 592), (470, 735)], "Dominio, confusiones y reacción", lx=478, ly=700)
    return s


if __name__ == "__main__":
    import sys
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    out.mkdir(exist_ok=True)
    for name, fn in (("bpmn_as_is", as_is), ("bpmn_to_be", to_be)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
