"""Versiones simplificadas de los diagramas para el póster de 90 x 120 cm.

Conservan la sintaxis BPMN 2.0 (evento de inicio y fin por pool, compuertas para unir caminos, solo flujos de
mensaje entre pools) y DFD (todos los flujos rotulados), con menos elementos y texto grande. En la columna
central del póster, 700 unidades ≈ 285 mm, así que 16 unidades ≈ 6,5 mm (unos 18 pt). Los diagramas completos
están en el documento (Figuras 4 a 8).
"""
from svglib import SVG, YELLOW_SOFT, GRAY_D
from diagramas_dfd import Canvas

FS = 16
RED_T = "#FBE9E7"
Y = YELLOW_SOFT
POOL = dict(band=30, fs=16, lfs=15, lband=28)


def bpmn_as_is() -> SVG:
    s = SVG(700, 318, "BPMN As-Is simplificado")
    s.pool(4, 4, 692, 212, "Aula de música", [("Docente", 128), ("Niño", 84)], **POOL)
    y = 72
    s.event(84, y, "start", None, r=13)
    s.task(166, y, 104, 58, "Prepara fichas", size=FS, icon="user", fill=RED_T, chars=9)
    s.task(282, y, 100, 58, "Explica la seña", size=FS, icon="user", chars=9)
    s.task(408, y, 120, 62, "Corrige uno por uno", size=FS, icon="user", fill=RED_T, chars=11)
    s.gateway(505, y, "xor", None, s=21)
    s.text(505, y + 36, "¿Acertó?", size=FS, weight=700)
    s.task(600, y, 104, 58, "Anota en cuaderno", size=FS, icon="user", fill=RED_T, chars=9)
    s.event(675, y, "end", None, r=12)
    s.flow([(97, y), (114, y)]); s.flow([(218, y), (232, y)]); s.flow([(466, y), (484, y)])
    s.flow([(526, y), (548, y)]); s.text(536, y - 13, "Sí", size=FS, weight=700)
    s.flow([(652, y), (663, y)])
    s.flow([(505, y - 21), (505, 18), (282, 18), (282, y - 29)])
    s.text(394, 30, "No: repite", size=15, weight=600, fill=GRAY_D)
    yn = 174
    s.task(282, yn, 100, 50, "Imita la seña", size=FS, icon="user", chars=9)
    s.flow([(282, y + 29), (282, yn - 25)])
    s.flow([(332, yn), (408, yn), (408, y + 31)])
    s.pool(4, 228, 692, 86, "Acudiente", **POOL)
    ya = 271
    s.event(470, ya, "msg-start", None, r=13)
    s.task(575, ya, 160, 56, "Lee un informe tardío", size=FS, icon="user", fill=RED_T, chars=15)
    s.event(678, ya, "end", None, r=12)
    s.flow([(483, ya), (495, ya)]); s.flow([(655, ya), (663, ya)])
    s.msg([(600, y + 29), (600, 222), (470, 222), (470, ya - 13)])
    R = dict(r=12, size=14)
    s.badge(218, y - 29, 1, **R); s.badge(468, y - 31, 2, **R); s.badge(330, 18, 3, **R)
    s.badge(652, y - 29, 4, **R); s.badge(655, ya - 28, 5, **R)
    return s


def bpmn_to_be() -> SVG:
    s = SVG(700, 516, "BPMN To-Be simplificado")
    s.pool(4, 4, 692, 80, "Niño", **POOL)
    yA = 44
    s.event(76, yA, "start", None, r=13)
    s.task(170, yA, 112, 56, "Hace la seña", size=FS, icon="user", chars=10)
    s.task(560, yA, 160, 56, "Oye la nota y ve el resultado", size=FS, icon="user", chars=16)
    s.event(670, yA, "end", None, r=12)
    s.flow([(89, yA), (114, yA)]); s.flow([(226, yA), (480, yA)]); s.flow([(640, yA), (658, yA)])
    top = 94
    hV, hE, hP = 112, 128, 104
    s.pool(4, top, 692, hV + hE + hP, "Sistema local", [("Visión", hV), ("Evaluación", hE), ("Planificación", hP)], **POOL)
    yV, yE, yP = top + 50, top + hV + 64, top + hV + hE + 54
    # visión
    s.event(98, yV, "msg-start", None, r=13)
    s.gateway(150, yV, "xor", None, s=19)
    s.task(258, yV, 132, 58, "Detectar y clasificar", size=FS, fill=Y, icon="svc", chars=12)
    s.gateway(370, yV, "xor", None, s=21)
    s.text(370, yV - 32, "¿Aceptada?", size=FS, weight=700)
    s.gateway(445, yV, "par", None, s=21)
    s.task(560, yV, 140, 56, "Sonido y dibujo", size=FS, fill=Y, icon="svc", chars=13)
    s.event(670, yV, "end", None, r=12)
    s.flow([(111, yV), (131, yV)]); s.flow([(169, yV), (192, yV)]); s.flow([(324, yV), (349, yV)])
    s.flow([(391, yV), (424, yV)]); s.text(407, yV - 13, "Sí", size=FS, weight=700)
    s.flow([(466, yV), (490, yV)]); s.flow([(630, yV), (658, yV)])
    yT = yV + 44
    s.flow([(370, yV + 21), (370, yT), (272, yT)])
    s.text(380, yV + 32, "No", size=FS, weight=700, anchor="start")
    s.event(258, yT, "timer", None, r=12)
    s.flow([(246, yT), (150, yT), (150, yV + 19)])
    # evaluación
    s.flow([(445, yV + 21), (445, yV + 58), (110, yV + 58), (110, yE - 27)])
    s.task(130, yE, 136, 54, "Evaluar y guardar", size=FS, fill=Y, icon="svc", chars=10)
    s.gateway(245, yE, "inc", None, s=21)
    s.task(380, yE - 30, 170, 44, "Dominio y repaso", size=FS, fill=Y, icon="svc", chars=17)
    s.task(380, yE + 30, 170, 44, "Estrellas y logros", size=FS, fill=Y, icon="svc", chars=17)
    s.gateway(510, yE, "inc", None, s=21)
    s.flow([(198, yE), (224, yE)])
    s.flow([(245, yE - 21), (245, yE - 30), (295, yE - 30)]); s.flow([(245, yE + 21), (245, yE + 30), (295, yE + 30)])
    s.flow([(465, yE - 30), (510, yE - 30), (510, yE - 21)]); s.flow([(465, yE + 30), (510, yE + 30), (510, yE + 21)])
    # planificación
    s.task(400, yP, 190, 52, "Planificar la sesión (MILP)", size=FS, fill=Y, icon="svc", chars=18)
    s.event(560, yP, "end", None, r=12)
    s.flow([(531, yE), (545, yE), (545, yP - 36), (400, yP - 36), (400, yP - 26)])
    s.flow([(495, yP), (548, yP)])
    # adulto
    yC = top + hV + hE + hP + 10 + 38
    s.pool(4, yC - 38, 692, 76, "Adulto", **POOL)
    s.event(300, yC, "start", None, r=12)
    s.task(430, yC, 180, 50, "Consulta la Zona de Padres", size=FS, icon="user", chars=16)
    s.event(600, yC, "msg-catch", None, r=13)
    s.event(670, yC, "end", None, r=12)
    s.flow([(312, yC), (340, yC)]); s.flow([(520, yC), (587, yC)]); s.flow([(613, yC), (658, yC)])
    # mensajes
    s.msg([(150, yA + 28), (150, top - 5), (98, top - 5), (98, yV - 13)])
    s.msg([(600, yV - 28), (600, yA + 28)])
    s.msg([(465, yE - 22), (620, yE - 22), (620, yC - 30), (600, yC - 30), (600, yC - 13)])
    return s


def dfd0() -> SVG:
    c = Canvas(700, 236, "DFD nivel 0 simplificado")
    c.process("0", 350, 118, 78, "0", "Hand Sing Kids (local)", size=17)
    c.entity("nino", 88, 42, 150, 54, "Niño o niña", size=17)
    c.entity("cam", 88, 196, 150, 54, "Cámara web", size=17)
    c.entity("adulto", 610, 118, 168, 64, "Acudiente o docente", size=17)
    c.link("nino", "0", "Perfil y actividad", off=-11, lpos=(240, 52), size=FS)
    c.link("0", "nino", "Nota y resultado", off=-11, lpos=(210, 108), size=FS)
    c.link("cam", "0", "Fotogramas", lpos=(230, 186), size=FS)
    # con off < 0 el flujo adulto→0 va abajo y el 0→adulto arriba
    c.link("adulto", "0", "Ajustes y solicitud", off=-15, lpos=(478, 158), size=FS)
    c.link("0", "adulto", "Informe", off=-15, lpos=(478, 82), size=FS)
    return c.s


def dfd1() -> SVG:
    c = Canvas(700, 420, "DFD nivel 1 simplificado")
    R = 50
    L = dict(size=15)
    c.entity("nino", 58, 60, 100, 46, "Niño", size=FS)
    c.entity("cam", 58, 360, 100, 46, "Cámara", size=FS)
    c.entity("adulto", 640, 360, 104, 46, "Adulto", size=FS)
    c.process("p6", 225, 60, R, "6.0", "Interfaz", size=15)
    c.process("p5", 470, 60, R, "5.0", "Planificar", size=15)
    c.process("p3", 350, 200, R, "3.0", "Evaluar", size=15)
    c.process("p4", 560, 200, R, "4.0", "Gemelo", size=15)
    c.process("p2", 225, 360, R, "2.0", "Reconocer", size=15)
    c.process("p7", 470, 360, R, "7.0", "Informe", size=15)
    c.store("d3", 350, 296, 116, 32, "D3", "Intentos", size=15)
    c.store("d4", 640, 112, 112, 40, "D4", "Habilidad", size=15)
    c.link("nino", "p6", "Actividad", off=-9, lpos=(140, 34), **L)
    c.link("p6", "nino", "Resultado", off=-9, lpos=(140, 88), **L)
    c.link("cam", "p2", "Fotogramas", lpos=(140, 344), **L)
    c.link("p2", "p3", "Seña", lpos=(262, 262), anchor="end", **L)
    c.link("p3", "p6", "Acierto", lpos=(266, 140), anchor="end", **L)
    c.link("p5", "p6", "Ruta del día", lpos=(348, 48), **L)
    c.link("p5", "p3", "Secuencia", lpos=(430, 128), anchor="start", **L)
    c.link("p3", "p4", "Resultado", lpos=(456, 186), **L)
    c.link("p3", "d3", "Intento", lpos=(360, 262), anchor="start", **L)
    c.link("d3", "p7", "Historial", lpos=(372, 336), anchor="start", **L)
    c.link("p4", "d4", "Dominio", both=True, lpos=(612, 160), anchor="start", **L)
    c.link("d4", "p5", "Estado", lpos=(560, 76), **L)
    c.link("p7", "adulto", "Informe", off=-9, lpos=(554, 336), **L)
    c.link("adulto", "p7", "Solicitud", off=-9, lpos=(554, 388), **L)
    return c.s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    for name, fn in (("poster_bpmn_as_is", bpmn_as_is), ("poster_bpmn_to_be", bpmn_to_be),
                     ("poster_dfd0", dfd0), ("poster_dfd1", dfd1)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
