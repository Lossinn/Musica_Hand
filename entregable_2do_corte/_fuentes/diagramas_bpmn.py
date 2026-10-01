"""BPMN 2.0: proceso actual (As-Is) y proceso propuesto (To-Be) de Hand Sing Kids.

Los pasos del To-Be siguen el código de HandSingKids7 (ciclo de una nota:
cámara → detector → descriptor → clasificador → estabilizador → evaluador →
registro → gemelo digital → motor adaptativo → optimizador).

Escala: lienzo de 1080 unidades de ancho para una página apaisada (9 in útiles),
así que 13,5 unidades de texto ≈ 8,1 pt impresos (APA 7: 8 a 14 pt en figuras).

Reglas de sintaxis que se respetan: cada pool tiene evento de inicio y de fin;
toda tarea tiene flujo de entrada y de salida; los flujos de secuencia no cruzan
pools (entre pools solo hay flujos de mensaje, punteados); las uniones de caminos
usan compuertas; los mensajes llegan a tareas o a eventos de captura, nunca a
compuertas ni a eventos de fin.
"""
from svglib import SVG, YELLOW_SOFT, GRAY_D

FS = 13.5          # texto mínimo
RED_T = "#FBE9E7"  # tarea con problema (As-Is)
Y = YELLOW_SOFT    # tarea del sistema (To-Be)
POOL = dict(fs=14, lfs=FS, band=32, lband=28)
ROT = dict(size=FS, weight=600, fill=GRAY_D)   # rótulos de condición


def as_is() -> SVG:
    s = SVG(1080, 470, "BPMN 2.0 As-Is: enseñanza de una nota musical en una escuela de música")
    s.pool(10, 10, 1060, 320, "Escuela de música", [("Docente", 185), ("Niño o niña", 135)], **POOL)
    y = 115
    s.event(100, y, "start", "Inicia la semana", lw=10, size=FS)
    s.task(193, y, 118, 74, "Prepara fichas y partituras de nivelación", fill=RED_T, icon="user", size=FS, chars=14)
    s.event(292, y, "timer", "Día de la clase", lw=9, size=FS)
    s.task(383, y, 112, 64, "Explica y demuestra la seña", icon="user", size=FS, chars=13)
    s.task(560, y, 128, 74, "Observa y corrige a cada niño, uno por uno", fill=RED_T, icon="user", size=FS, chars=15)
    s.gateway(672, y, "xor", "¿Acertó?", lpos="below", size=FS, s=25)
    s.task(780, y, 112, 64, "Anota el avance en el cuaderno", fill=RED_T, icon="user", size=FS, chars=13)
    s.task(912, y, 118, 64, "Informa al acudiente", fill=RED_T, icon="user", size=FS, chars=13)
    s.event(1030, y, "end", "Fin de la clase", lw=8, size=FS)
    yn = 262
    s.task(383, yn, 112, 60, "Imita la seña y entona la nota", icon="user", size=FS, chars=13)
    s.flow([(116, y), (134, y)]); s.flow([(252, y), (276, y)]); s.flow([(308, y), (327, y)])
    s.flow([(383, y + 32), (383, yn - 30)])
    s.flow([(439, yn), (560, yn), (560, y + 37)])
    s.flow([(624, y), (647, y)])
    s.flow([(697, y), (724, y)], "Sí", lx=710, ly=y - 12, size=FS)
    s.flow([(672, y - 25), (672, 42), (383, 42), (383, y - 32)], "No: repite la demostración", lx=560, ly=31, size=FS)
    s.flow([(836, y), (853, y)]); s.flow([(971, y), (1014, y)])
    # pool del acudiente
    ya = 405
    s.pool(10, 350, 1060, 110, "Acudiente", **POOL)
    s.event(660, ya, "msg-start", "Recibe el informe", lw=12, size=FS, lpos="left")
    s.task(780, ya, 140, 60, "Lee un informe sin detalle por nota", fill=RED_T, icon="user", size=FS, chars=17)
    s.event(908, ya, "timer", None)
    s.text(908, ya + 30, "Hasta la próxima clase", size=FS, weight=500)
    s.event(1030, ya, "end", "Sin repaso", lw=8, size=FS)
    s.flow([(676, ya), (710, ya)]); s.flow([(850, ya), (892, ya)]); s.flow([(924, ya), (1014, ya)])
    s.msg([(912, y + 32), (912, 340), (660, 340), (660, ya - 16)])
    s.text(922, 300, "Informe verbal o por mensaje", size=FS, weight=500, italic=True, fill=GRAY_D, anchor="start")
    # marcas de cuellos de botella (explicadas en la nota de la figura)
    R = dict(r=12, size=FS)
    s.badge(252, y - 37, 1, **R); s.badge(624, y - 37, 2, **R); s.badge(440, 42, 3, **R)
    s.badge(836, y - 32, 4, **R); s.badge(971, y - 32, 5, **R); s.badge(924, ya - 22, 6, **R)
    return s


def to_be() -> SVG:
    s = SVG(1080, 651, "BPMN 2.0 To-Be: sesión de práctica con Hand Sing Kids")
    PB = dict(POOL, band=34)
    # ------------------------------------------------------------ Pool A: niño
    yA = 50
    s.pool(10, 6, 1060, 88, "Niño o niña", **PB)
    s.event(100, yA, "start", None)
    s.text(100, yA + 28, "Abre la app", size=FS, weight=500)
    s.task(192, yA, 104, 60, "Elige su perfil", icon="user", size=FS, chars=11)
    s.gateway(284, yA, "xor", None, s=21)
    s.task(380, yA, 104, 60, "Ve la actividad y la nota", icon="user", size=FS, chars=11)
    s.task(497, yA, 108, 60, "Hace la seña ante la cámara", icon="user", size=FS, chars=12)
    s.task(885, yA, 112, 60, "Oye la nota y ve el resultado", icon="user", size=FS, chars=12)
    s.gateway(965, yA, "xor", None, s=21)
    s.event(1010, yA, "msg-catch", None, r=14)
    s.event(1048, yA, "end", None, r=13)
    s.flow([(116, yA), (140, yA)]); s.flow([(244, yA), (263, yA)]); s.flow([(305, yA), (328, yA)])
    s.flow([(432, yA), (443, yA)]); s.flow([(551, yA), (829, yA)]); s.flow([(941, yA), (944, yA)])
    s.flow([(986, yA), (996, yA)]); s.flow([(1024, yA), (1035, yA)])
    s.flow([(965, yA - 21), (965, 13), (284, 13), (284, yA - 21)])
    s.text(690, 25, "¿Cerró la sesión? No: continúa", **ROT)
    s.text(1062, yA + 32, "Sí: descanso", size=FS, weight=600, anchor="end")
    # ------------------------------------------------------- Pool B: sistema
    top = 102
    hP, hV, hE = 120, 145, 190
    s.pool(10, top, 1060, hP + hV + hE, "Sistema Hand Sing Kids (local)",
           [("Planificación", hP), ("Visión artificial", hV), ("Evaluación y datos", hE)], **PB)
    vTop, eTop = top + hP, top + hP + hV
    yP, yV, yE = top + 66, vTop + 62, eTop + 98
    # Planificación
    s.event(112, yP, "msg-start", None)
    s.text(112, yP + 28, "Inicio", size=FS, weight=500)
    s.task(205, yP, 104, 64, "Planificar la ruta del día (MILP)", fill=Y, icon="svc", size=FS, chars=11)
    s.gateway(290, yP, "xor", None, s=21)
    s.task(380, yP, 104, 64, "Presentar la actividad", fill=Y, icon="svc", size=FS, chars=11)
    s.task(600, yP, 110, 64, "Decidir la acción (reglas)", fill=Y, icon="svc", size=FS, chars=11)
    s.gateway(700, yP, "xor", None, s=22)
    s.text(700, yP + 33, "¿F ≥ 1?", size=FS, weight=600)
    s.task(795, yP, 104, 64, "Cerrar y sugerir descanso", fill=Y, icon="svc", size=FS, chars=11)
    s.event(870, yP, "end", None, r=14)
    s.flow([(128, yP), (153, yP)]); s.flow([(257, yP), (269, yP)]); s.flow([(311, yP), (328, yP)])
    s.flow([(655, yP), (678, yP)])
    s.flow([(722, yP), (743, yP)], "Sí", lx=732, ly=yP - 12, size=FS)
    s.flow([(847, yP), (856, yP)])
    s.flow([(700, yP - 22), (700, top + 12), (290, top + 12), (290, yP - 21)])
    s.text(500, top + 24, "No: siguiente actividad", **ROT)
    # Visión artificial
    s.gateway(380, yV, "xor", None, s=21)
    s.task(487, yV, 120, 64, "Detectar manos y extraer el descriptor", fill=Y, icon="svc", size=FS, chars=14)
    s.task(612, yV, 104, 64, "Clasificar y estabilizar", fill=Y, icon="svc", size=FS, chars=11)
    s.gateway(712, yV, "xor", None, s=22)
    s.text(712, yV - 47, "¿Seña aceptada? d ≤ 0,95; P ≥ 0,55; margen ≥ 0,08", size=FS, weight=600)
    s.gateway(790, yV, "par", None, s=22)
    s.task(885, yV, 104, 64, "Sintetizar la nota y dibujar", fill=Y, icon="svc", size=FS, chars=11)
    s.event(975, yV, "end", None)
    s.text(1000, yV + 22, "Retro-\nalimentación", size=FS, weight=500, valign="top")
    s.flow([(380, yP + 32), (380, yV - 21)])
    s.flow([(401, yV), (427, yV)]); s.flow([(547, yV), (560, yV)]); s.flow([(664, yV), (690, yV)])
    s.flow([(734, yV), (768, yV)], "Sí", lx=751, ly=yV - 12, size=FS)
    s.flow([(812, yV), (833, yV)]); s.flow([(937, yV), (959, yV)])
    yT = yV + 47
    s.flow([(712, yV + 22), (712, yT), (566, yT)], "No", lx=722, ly=yV + 34, size=FS, anchor="start")
    s.event(550, yT, "timer", None)
    s.text(550, yT + 18, "Siguiente fotograma (≈ 42 ms)", size=FS, weight=500, valign="top")
    s.flow([(534, yT), (380, yT), (380, yV + 21)])
    # Evaluación y datos
    s.flow([(790, yV + 22), (790, eTop + 12), (205, eTop + 12), (205, yE - 28)])
    s.task(205, yE, 108, 56, "Evaluar el paso", fill=Y, icon="svc", size=FS, chars=12)
    s.gateway(315, yE, "xor", None, s=22)
    s.text(315, yE - 27, "¿Terminó la actividad?", size=FS, weight=600, width=12, valign="bottom")
    s.gateway(400, yE, "inc", None, s=22)
    tx, dy = 600, 54
    s.task(tx, yE - dy, 140, 44, "Dar estrellas y logros", fill=Y, icon="svc", size=FS, chars=17)
    s.task(tx, yE, 140, 44, "Guardar intentos, dominio y repaso", fill=Y, icon="svc", size=FS, chars=17)
    s.task(tx, yE + dy, 140, 44, "Abrir habilidades nuevas", fill=Y, icon="svc", size=FS, chars=17)
    s.gateway(710, yE, "inc", None, s=22)
    s.flow([(259, yE), (293, yE)])
    s.flow([(337, yE), (378, yE)], "Sí", lx=356, ly=yE - 12, size=FS)
    s.flow([(400, yE - 22), (400, yE - dy), (530, yE - dy)])
    s.flow([(422, yE), (530, yE)])
    s.flow([(400, yE + 22), (400, yE + dy), (530, yE + dy)])
    C = dict(size=FS, weight=500, fill=GRAY_D, anchor="start")
    s.text(408, yE - dy - 12, "si mejora el récord", **C)
    s.text(428, yE - 11, "siempre", **C)
    s.text(408, yE + dy + 14, "si hay prerrequisitos", **C)
    s.flow([(670, yE - dy), (710, yE - dy), (710, yE - 22)])
    s.flow([(670, yE), (688, yE)])
    s.flow([(670, yE + dy), (710, yE + dy), (710, yE + 22)])
    s.flow([(732, yE), (1058, yE), (1058, yP + 50), (600, yP + 50), (600, yP + 32)])
    yB = eTop + hE - 9
    s.flow([(315, yE + 22), (315, yB), (128, yB), (128, yV), (359, yV)])
    s.text(138, yB - 12, "No: siguiente nota", size=FS, weight=600, fill=GRAY_D, anchor="start")
    # informe bajo demanda (inicio por mensaje)
    yR = yE + 50
    s.event(760, yR, "msg-start", None)
    s.task(870, yR, 150, 56, "Construir el gemelo digital y el informe", fill=Y, icon="svc", size=FS, chars=19)
    s.event(985, yR, "end-msg", None)
    s.flow([(776, yR), (795, yR)]); s.flow([(945, yR), (969, yR)])
    # -------------------------------------------------------- Pool C: adulto
    cTop = top + hP + hV + hE + 8
    yC = cTop + 40
    s.pool(10, cTop, 1060, 80, "Acudiente o docente", **PB)
    s.event(560, yC, "start", None)
    s.text(542, yC, "Quiere ver el avance", size=FS, weight=500, anchor="end")
    s.task(680, yC, 124, 54, "Consulta la Zona de Padres", icon="user", size=FS, chars=13)
    s.event(950, yC, "msg-catch", None)
    s.text(922, yC + 24, "Recibe el informe", size=FS, weight=500, anchor="end")
    s.event(1045, yC, "end", None)
    s.text(1066, yC + 24, "Decide qué reforzar", size=FS, weight=500, anchor="end")
    s.flow([(576, yC), (618, yC)]); s.flow([(742, yC), (934, yC)]); s.flow([(966, yC), (1029, yC)])
    # --------------------------------------------------- flujos de mensaje
    g = top - 4      # franja entre los pools A y B
    s.msg([(192, yA + 30), (192, g), (112, g), (112, yP - 16)])
    s.msg([(380, yP - 32), (380, yA + 30)])
    s.msg([(497, yA + 30), (497, yV - 32)])
    s.text(559, yA + 36, "Fotogramas (solo en RAM)", size=FS, weight=500, italic=True, fill=GRAY_D, anchor="start")
    s.msg([(905, yV - 32), (905, yA + 30)], "Nota sonora", lx=913, ly=yP - 36, size=FS)
    s.msg([(795, yP - 32), (795, g), (1010, g), (1010, yA + 14)])
    s.msg([(680, yC - 27), (680, cTop - 4), (760, cTop - 4), (760, yR + 16)])
    s.text(768, yR + 31, "Solicitud", size=FS, weight=500, italic=True, fill=GRAY_D, anchor="start")
    s.text(993, yR + 31, "Informe", size=FS, weight=500, italic=True, fill=GRAY_D, anchor="start")
    s.msg([(985, yR + 16), (985, cTop - 4), (950, cTop - 4), (950, yC - 16)])
    return s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    out.mkdir(exist_ok=True)
    for name, fn in (("bpmn_as_is", as_is), ("bpmn_to_be", to_be)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
