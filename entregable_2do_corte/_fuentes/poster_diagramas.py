"""Versiones simplificadas (texto grande) de los diagramas para el póster de 90 x 120 cm.

Mantienen la sintaxis BPMN 2.0 y DFD, pero con menos elementos para que se lean a un metro.
Los diagramas completos están en el documento (Figuras 4 a 8).
"""
from svglib import SVG, YELLOW_SOFT, GRAY_D
from diagramas_dfd import Canvas


def bpmn_as_is() -> SVG:
    s = SVG(700, 300, "BPMN As-Is simplificado")
    s.pool(4, 4, 692, 204, "Escuela de música", [("Docente", 108), ("Niño", 96)], band=26)
    s.event(86, 66, "start", None, r=13)
    s.task(178, 66, 108, 62, "Demuestra la seña", size=15, icon="user")
    s.task(304, 66, 110, 66, "Observa y corrige a cada niño", size=15, icon="user", fill="#FBE9E7")
    s.gateway(412, 66, "xor", None, s=23)
    s.text(412, 101, "¿Acertó?", size=14, weight=700)
    s.task(528, 66, 112, 62, "Anota en el cuaderno", size=15, icon="user", fill="#FBE9E7")
    s.event(636, 66, "end", None, r=13)
    s.task(178, 160, 108, 56, "Imita la seña", size=15, icon="user")
    s.flow([(99, 66), (126, 66)]); s.flow([(232, 66), (249, 66)]); s.flow([(359, 66), (389, 66)])
    s.flow([(435, 66), (472, 66)]); s.flow([(584, 66), (623, 66)])
    s.flow([(178, 94), (178, 134)])
    s.flow([(230, 160), (304, 160), (304, 94)])
    s.flow([(412, 43), (412, 24), (178, 24), (178, 38)])
    s.text(296, 14, "No: repite", size=13, weight=600, fill=GRAY_D)
    s.text(455, 53, "Sí", size=13, weight=700)
    s.pool(4, 216, 692, 80, "Acudiente", band=26)
    s.event(500, 258, "msg-start", None, r=13)
    s.task(610, 256, 140, 64, "Informe tardío y sin detalle por nota", size=15, icon="user", fill="#FBE9E7")
    s.flow([(513, 258), (544, 258)])
    s.msg([(500, 97), (500, 243)], None)
    s.text(508, 190, "Informe", size=13, anchor="start", italic=True, weight=500, fill=GRAY_D)
    s.badge(354, 36, 1); s.badge(572, 36, 2); s.badge(678, 228, 3)
    return s


def bpmn_to_be() -> SVG:
    Y = YELLOW_SOFT
    s = SVG(700, 500, "BPMN To-Be simplificado")
    s.pool(4, 4, 692, 80, "Niño", band=26)
    s.event(64, 44, "start", None, r=13)
    s.task(178, 44, 146, 62, "Hace la seña ante la cámara", size=15, icon="user")
    s.task(470, 44, 160, 62, "Oye la nota y ve el resultado", size=15, icon="user")
    s.event(650, 44, "end", None, r=13)
    s.flow([(77, 44), (105, 44)])
    s.flow([(251, 44), (390, 44)])
    s.flow([(550, 44), (637, 44)])
    s.pool(4, 94, 692, 308, "Sistema local", [("Visión", 100), ("Evaluación", 112), ("Planificación", 96)], band=26)
    s.task(178, 144, 130, 58, "Detectar y clasificar", size=15, fill=Y, icon="svc")
    s.gateway(306, 144, "xor", None, s=22)
    s.text(306, 176, "¿Aceptada?", size=13.5, weight=700)
    s.task(470, 144, 160, 58, "Sonido y dibujo de la nota", size=15, fill=Y, icon="svc")
    s.flow([(243, 144), (284, 144)]); s.flow([(328, 144), (390, 144)], "Sí", lx=359, ly=132, size=13)
    s.flow([(306, 122), (306, 106), (178, 106), (178, 115)], "No", lx=244, ly=99, size=13)
    s.task(178, 250, 134, 64, "Evaluar y registrar el intento", size=15, fill=Y, icon="svc")
    s.gateway(306, 250, "inc", None, s=22)
    s.task(452, 228, 132, 42, "Dominio y repaso", size=14.5, fill=Y, icon="svc")
    s.task(452, 274, 132, 42, "Estrellas y logros", size=14.5, fill=Y, icon="svc")
    s.gateway(578, 250, "inc", None, s=20)
    s.flow([(245, 250), (284, 250)])
    s.flow([(328, 250), (350, 250), (350, 228), (386, 228)])
    s.flow([(350, 250), (350, 274), (386, 274)])
    s.flow([(518, 228), (578, 228), (578, 230)])
    s.flow([(518, 274), (578, 274), (578, 270)])
    s.task(178, 354, 160, 64, "Planificar la sesión (MILP y reglas)", size=15, fill=Y, icon="svc")
    s.event(420, 354, "end", None, r=13)
    s.flow([(258, 354), (407, 354)])
    s.flow([(578, 270), (578, 326), (520, 326), (520, 354), (433, 354)])
    s.pool(4, 412, 692, 84, "Adulto", band=26)
    s.task(452, 456, 170, 50, "Consulta la Zona de Padres", size=15, icon="user")
    s.msg([(178, 75), (178, 115)], None)
    s.msg([(470, 115), (470, 75)], None)
    s.msg([(452, 295), (452, 431)], None)
    s.text(462, 408, "Informe", size=13, anchor="start", italic=True, weight=500, fill=GRAY_D)
    return s


def dfd0() -> SVG:
    c = Canvas(700, 230, "DFD nivel 0 simplificado")
    s = c.s
    c.process("0", 350, 115, 76, "0", "Hand Sing Kids (local)", size=16)
    c.entity("nino", 92, 40, 140, 50, "Niño o niña", size=16)
    c.entity("cam", 92, 190, 140, 50, "Cámara web", size=16)
    c.entity("adulto", 608, 115, 160, 60, "Padre, madre o docente", size=15)
    c.link("nino", "0", "Perfil y actividad", off=-10, lpos=(232, 60), size=14)
    c.link("0", "nino", "Nota y resultado", off=-10, lpos=(215, 104), size=14)
    c.link("cam", "0", "Fotogramas", lpos=(228, 170), size=14)
    c.link("adulto", "0", "Ajustes", off=-14, lpos=(486, 78), size=14)
    c.link("0", "adulto", "Informe", off=-14, lpos=(486, 152), size=14)
    return s


def dfd1() -> SVG:
    c = Canvas(700, 420, "DFD nivel 1 simplificado")
    s = c.s
    R = 48
    c.entity("nino", 58, 122, 96, 44, "Niño", size=15)
    c.entity("cam", 58, 322, 96, 44, "Cámara", size=15)
    c.entity("adulto", 644, 322, 96, 44, "Adulto", size=15)
    c.process("p1", 190, 62, R, "1.0", "Perfiles", size=14)
    c.process("p5", 350, 62, R, "5.0", "Planificar", size=14)
    c.process("p6", 190, 192, R, "6.0", "Interfaz", size=14)
    c.process("p3", 350, 192, R, "3.0", "Evaluar", size=14)
    c.process("p4", 510, 192, R, "4.0", "Gemelo", size=14)
    c.process("p2", 190, 322, R, "2.0", "Reconocer", size=14)
    c.process("p7", 510, 322, R, "7.0", "Informe", size=14)
    c.store("d1", 62, 22, 100, 28, "D1", "Perfil", size=13)
    c.store("d5", 560, 62, 112, 28, "D5", "Catálogo", size=13)
    c.store("d6", 640, 128, 112, 28, "D6", "Modelo", size=13)
    c.store("d4", 640, 258, 112, 28, "D4", "Habilidad", size=13)
    c.store("d3", 350, 272, 112, 28, "D3", "Intentos", size=13)
    c.store("d2", 190, 396, 112, 28, "D2", "Plantillas", size=13)
    for a, b in (("nino", "p1"), ("p1", "p5"), ("p5", "p6"), ("p5", "p3"), ("p2", "p3"), ("p3", "p6"), ("p3", "p4"),
                 ("cam", "p2"), ("p6", "nino"), ("adulto", "p7")):
        c.link(a, b)
    for a, b in (("d1", "p1"), ("p2", "d2"), ("p4", "d4"), ("p4", "d6")):
        c.link(a, b, both=True)
    for a, b in (("p3", "d3"), ("d3", "p7"), ("d4", "p7"), ("d5", "p5"), ("d6", "p5"), ("p7", "adulto")):
        c.link(a, b)
    return s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    for name, fn in (("poster_bpmn_as_is", bpmn_as_is), ("poster_bpmn_to_be", bpmn_to_be),
                     ("poster_dfd0", dfd0), ("poster_dfd1", dfd1)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
