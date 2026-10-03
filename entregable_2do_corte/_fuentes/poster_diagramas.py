"""Versiones simplificadas de los diagramas para los pósteres de 90 x 120 cm.

Conservan la sintaxis BPMN 2.0 (evento de inicio y fin por pool, compuertas para unir caminos, solo flujos de
mensaje entre pools) y DFD (todos los flujos rotulados), con menos elementos y texto grande. El lienzo es de 600
unidades de ancho y el texto de 16 a 18: en la columna central del póster (≈ 270 mm) 17 unidades ≈ 7,6 mm, unos
22 pt, legibles a simple vista. Estilo de póster: sombras vectoriales desplazadas (sin filtros, para que el PDF
siga siendo vectorial), bandas de pool negras con título amarillo y carriles en crema. Los diagramas completos
están en el documento (Figuras 4 a 8).
"""
from svglib import SVG, YELLOW, YELLOW_SOFT, GRAY_D, INK
from diagramas_dfd import Canvas

FS = 17
RED_T = "#FBE3DF"
Y = YELLOW_SOFT
SOMBRA = "#D9D2BF"
CREMA = "#FFF8E1"
POOL = dict(band=34, fs=18, lfs=16, lband=30)


class PSVG(SVG):
    """SVG con el acabado del póster; mismas primitivas que svglib.SVG."""

    def path(self, pts, *, stroke=INK, sw=1.9, dash=None, end="arr", start=None, fill="none") -> None:
        super().path(pts, stroke=stroke, sw=sw, dash=dash, end=end, start=start, fill=fill)

    def pool(self, x, y, w, h, title, lanes=None, *, band=34, fill="#fff", fs=18, lfs=16, lband=30) -> None:
        self.rect(x + 3, y + 3.5, w, h, fill=SOMBRA, stroke="none", rx=6)
        self.rect(x, y, w, h, fill=fill, sw=1.8, rx=6)
        self.add(f'<path d="M{x + 6},{y} H{x + band} V{y + h} H{x + 6} Q{x},{y + h} {x},{y + h - 6} V{y + 6} Q{x},{y} {x + 6},{y} Z" '
                 f'fill="{INK}"/>')
        self.text(x + band / 2, y + h / 2, title, size=fs, weight=800, rotate=-90, fill=YELLOW,
                  width=max(10, int(h / (fs * 0.6))))
        if lanes:
            ly = y
            for i, (name, lh) in enumerate(lanes):
                if i:
                    self.line(x + band, ly, x + w, ly, sw=1.1, stroke="#9A9A9A", dash="5 4")
                self.rect(x + band, ly, lband, lh, fill=CREMA, stroke="none")
                self.line(x + band + lband, ly, x + band + lband, ly + lh, sw=1.1, stroke="#BDBDBD")
                self.text(x + band + lband / 2, ly + lh / 2, name, size=lfs, weight=700, rotate=-90,
                          width=max(8, int(lh / (lfs * 0.6))))
                ly += lh

    def task(self, cx, cy, w, h, label, *, fill="#fff", size=FS, chars=None, icon=None, stroke=INK, sw=1.8) -> None:
        self.rect(cx - w / 2 + 2.5, cy - h / 2 + 3, w, h, fill=SOMBRA, stroke="none", rx=10)
        super().task(cx, cy, w, h, label, fill=fill, size=size, chars=chars, icon=icon, stroke=stroke, sw=sw)

    def process(self, cx, cy, r, num, label, *, size=FS, fill="#fff", chars=None) -> None:
        self.add(f'<circle cx="{cx + 2.5}" cy="{cy + 3}" r="{r}" fill="{SOMBRA}"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.1"/>')
        self.add(f'<path d="M{cx - r * 0.86},{cy - r * 0.42} A{r},{r} 0 0 1 {cx + r * 0.86},{cy - r * 0.42} Z" fill="{YELLOW}" '
                 f'stroke="{INK}" stroke-width="1.2"/>')
        self.text(cx, cy - r * 0.70, num, size=size - 1, weight=800)
        self.text(cx, cy + r * 0.18, label, size=size, width=chars or max(9, int(r * 1.5 / (size * 0.56))), weight=600)

    def entity(self, cx, cy, w, h, label, *, size=FS, fill=INK) -> None:
        self.rect(cx - w / 2 + 2.5, cy - h / 2 + 3, w, h, fill=SOMBRA, stroke="none", rx=4)
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, sw=1.9, rx=4)
        self.text(cx, cy, label, size=size, width=max(8, int(w / (size * 0.56))), weight=700, fill="#fff")

    def store(self, cx, cy, w, h, code, label, *, size=FS, dup=False) -> None:
        x0, y0 = cx - w / 2, cy - h / 2
        self.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{YELLOW}" stroke="none"/>')
        self.add(f'<rect x="{x0}" y="{y0}" width="38" height="{h}" fill="{INK}" stroke="none"/>')
        self.line(x0, y0, x0 + w, y0, sw=2); self.line(x0, y0 + h, x0 + w, y0 + h, sw=2)
        self.text(x0 + 19, cy, code, size=size - 1, weight=800, fill=YELLOW)
        self.text(x0 + 42 + (w - 42) / 2, cy, label, size=size, width=max(8, int((w - 46) / (size * 0.56))), weight=600)

    def dflow(self, pts, label=None, *, lx=None, ly=None, size=16, anchor="middle", both=False) -> None:
        self.path(pts, start="arr" if both else None)
        if label:
            x, y = (lx, ly) if lx is not None else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 8)
            self.add(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="central" '
                     f'font-weight="600" font-style="italic" fill="{GRAY_D}" paint-order="stroke" stroke="#fff" '
                     f'stroke-width="5" stroke-linejoin="round">{label}</text>')


def canvas(w: int, h: int, title: str) -> Canvas:
    c = Canvas(w, h, title)
    c.s = PSVG(w, h, title)
    return c


def bpmn_as_is() -> SVG:
    s = PSVG(600, 326, "BPMN As-Is simplificado")
    s.pool(4, 4, 588, 220, "Aula de música", [("Docente", 132), ("Niño", 88)], **POOL)
    y = 80
    s.event(86, y, "start", None, r=12)
    s.task(146, y, 80, 58, "Prepara fichas", icon="user", fill=RED_T, chars=7)
    s.task(240, y, 84, 58, "Explica la seña", icon="user", chars=8)
    s.task(345, y, 100, 58, "Corrige uno a uno", icon="user", fill=RED_T, chars=9)
    s.gateway(428, y, "xor", None, s=18)
    s.text(428, y + 32, "¿Acertó?", size=16, weight=700)
    s.task(506, y, 82, 58, "Anota en cuaderno", icon="user", fill=RED_T, chars=8)
    s.event(574, y, "end", None, r=11)
    s.flow([(98, y), (106, y)]); s.flow([(186, y), (198, y)]); s.flow([(282, y), (295, y)])
    s.flow([(395, y), (410, y)]); s.flow([(446, y), (465, y)]); s.text(455, y - 13, "Sí", size=16, weight=800)
    s.flow([(547, y), (563, y)])
    s.flow([(428, y - 18), (428, 22), (240, 22), (240, y - 29)])
    s.text(372, 35, "No: repite", size=15, weight=700, fill=GRAY_D)
    yn = 180
    s.task(240, yn, 92, 52, "Imita la seña", icon="user", chars=8)
    s.flow([(240, y + 29), (240, yn - 26)])
    s.flow([(286, yn), (345, yn), (345, y + 29)])
    s.pool(4, 236, 588, 86, "Acudiente", **{**POOL, "fs": 15})
    ya = 279
    s.event(395, ya, "msg-start", None, r=12)
    s.task(490, ya, 140, 54, "Lee un informe tardío", icon="user", fill=RED_T, chars=14)
    s.event(578, ya, "end", None, r=10)
    s.flow([(407, ya), (420, ya)]); s.flow([(560, ya), (568, ya)])
    s.msg([(506, y + 29), (506, 230), (395, 230), (395, ya - 12)])
    R = dict(r=11, size=14)
    s.badge(186, y - 29, 1, **R); s.badge(395, y - 29, 2, **R); s.badge(300, 22, 3, **R)
    s.badge(547, y - 29, 4, **R); s.badge(560, ya - 27, 5, **R)
    return s


def bpmn_to_be() -> SVG:
    s = PSVG(600, 548, "BPMN To-Be simplificado")
    s.pool(4, 4, 588, 78, "Niño", **POOL)
    yA = 43
    s.event(92, yA, "start", None, r=12)
    s.task(172, yA, 100, 56, "Hace la seña", icon="user", chars=8)
    s.task(470, yA, 164, 56, "Oye la nota y ve el resultado", icon="user", chars=15)
    s.event(576, yA, "end", None, r=11)
    s.flow([(104, yA), (122, yA)]); s.flow([(222, yA), (388, yA)]); s.flow([(552, yA), (565, yA)])
    top = 94
    hV, hE, hP = 124, 132, 108
    s.pool(4, top, 588, hV + hE + hP, "Sistema local", [("Visión", hV), ("Evaluación", hE), ("Planificación", hP)], **POOL)
    yV, yE, yP = top + 54, top + hV + 66, top + hV + hE + 50
    # visión
    s.event(96, yV, "msg-start", None, r=12)
    s.gateway(140, yV, "xor", None, s=17)
    s.task(238, yV, 110, 56, "Detectar y clasificar", fill=Y, icon="svc", chars=10)
    s.gateway(330, yV, "xor", None, s=19)
    s.text(330, yV - 33, "¿Aceptada?", size=16, weight=800)
    s.gateway(392, yV, "par", None, s=18)
    s.task(482, yV, 108, 56, "Sonido y dibujo", fill=Y, icon="svc", chars=8)
    s.event(574, yV, "end", None, r=11)
    s.flow([(108, yV), (123, yV)]); s.flow([(157, yV), (183, yV)]); s.flow([(293, yV), (311, yV)])
    s.flow([(349, yV), (374, yV)]); s.text(361, yV - 13, "Sí", size=16, weight=800)
    s.flow([(410, yV), (428, yV)]); s.flow([(536, yV), (563, yV)])
    yT = yV + 44
    s.flow([(330, yV + 19), (330, yT), (250, yT)])
    s.text(339, yV + 31, "No", size=16, weight=800, anchor="start")
    s.event(238, yT, "timer", None, r=12)
    s.flow([(226, yT), (140, yT), (140, yV + 17)])
    # evaluación
    s.flow([(392, yV + 18), (392, yV + 64), (122, yV + 64), (122, yE - 27)])
    s.task(126, yE, 112, 54, "Evaluar y guardar", fill=Y, icon="svc", chars=9)
    s.gateway(222, yE, "inc", None, s=18)
    s.task(345, yE - 30, 170, 42, "Dominio y repaso", fill=Y, icon="svc", chars=17)
    s.task(345, yE + 30, 170, 42, "Estrellas y logros", fill=Y, icon="svc", chars=18)
    s.gateway(466, yE, "inc", None, s=18)
    s.flow([(182, yE), (204, yE)])
    s.flow([(222, yE - 18), (222, yE - 30), (260, yE - 30)]); s.flow([(222, yE + 18), (222, yE + 30), (260, yE + 30)])
    s.flow([(430, yE - 30), (466, yE - 30), (466, yE - 18)]); s.flow([(430, yE + 30), (466, yE + 30), (466, yE + 18)])
    # planificación
    s.task(360, yP, 200, 52, "Planificar la sesión (MILP)", fill=Y, icon="svc", chars=14)
    s.event(520, yP, "end", None, r=11)
    s.flow([(484, yE), (500, yE), (500, yP - 38), (360, yP - 38), (360, yP - 26)])
    s.flow([(460, yP), (509, yP)])
    # adulto
    yC = 506
    s.pool(4, yC - 38, 588, 76, "Adulto", **POOL)
    s.event(250, yC, "start", None, r=11)
    s.task(370, yC, 168, 52, "Consulta la Zona de Padres", icon="user", chars=14)
    s.event(520, yC, "msg-catch", None, r=12)
    s.event(576, yC, "end", None, r=11)
    s.flow([(261, yC), (286, yC)]); s.flow([(454, yC), (508, yC)]); s.flow([(532, yC), (565, yC)])
    # mensajes
    s.msg([(172, yA + 28), (172, top - 6), (96, top - 6), (96, yV - 12)])
    s.msg([(500, yV - 28), (500, yA + 28)])
    s.msg([(430, yE - 38), (548, yE - 38), (548, yC - 44), (520, yC - 44), (520, yC - 12)])
    return s


def dfd0() -> SVG:
    c = canvas(600, 236, "DFD nivel 0 simplificado")
    c.process("0", 300, 118, 74, "0", "Hand Sing Kids (local)", size=18)
    c.entity("nino", 78, 42, 136, 52, "Niño o niña", size=17)
    c.entity("cam", 78, 196, 136, 52, "Cámara web", size=17)
    c.entity("adulto", 522, 118, 140, 64, "Acudiente o docente", size=17)
    c.link("nino", "0", "Perfil y actividad", off=-11, lpos=(212, 40), size=16)
    c.link("0", "nino", "Nota y resultado", off=-11, lpos=(170, 112), size=16)
    c.link("cam", "0", "Fotogramas", lpos=(196, 196), size=16)
    c.link("adulto", "0", "Ajustes", off=-15, lpos=(412, 160), size=16)
    c.link("0", "adulto", "Informe", off=-15, lpos=(412, 78), size=16)
    return c.s


def dfd1() -> SVG:
    c = canvas(600, 400, "DFD nivel 1 simplificado")
    R = 52
    L = dict(size=16)
    c.entity("nino", 52, 60, 92, 46, "Niño", size=FS)
    c.entity("cam", 52, 345, 92, 46, "Cámara", size=FS)
    c.entity("adulto", 555, 345, 86, 46, "Adulto", size=FS)
    c.process("p6", 200, 60, R, "6.0", "Interfaz", size=FS)
    c.process("p5", 420, 60, R, "5.0", "Planificar", size=FS)
    c.process("p3", 305, 200, R, "3.0", "Evaluar", size=FS)
    c.process("p4", 490, 200, R, "4.0", "Gemelo", size=FS)
    c.process("p2", 200, 345, R, "2.0", "Reconocer", size=FS)
    c.process("p7", 405, 345, R, "7.0", "Informe", size=FS)
    c.store("d3", 305, 290, 124, 34, "D3", "Intentos", size=16)
    c.store("d4", 545, 120, 106, 36, "D4", "Habilidad", size=15)
    c.link("nino", "p6", "Actividad", off=-9, lpos=(130, 27), **L)
    c.link("p6", "nino", "Resultado", off=-9, lpos=(130, 95), **L)
    c.link("cam", "p2", "Fotogramas", lpos=(124, 311), **L)
    c.link("p2", "p3", "Seña", lpos=(244, 270), anchor="end", **L)
    c.link("p3", "p6", "Acierto", lpos=(246, 130), anchor="end", **L)
    c.link("p5", "p6", "Ruta del día", lpos=(310, 46), **L)
    c.link("p5", "p3", "Secuencia", lpos=(372, 132), anchor="start", **L)
    c.link("p3", "p4", "Resultado", lpos=(397, 186), **L)
    c.link("p3", "d3", "Intento", lpos=(314, 261), anchor="start", **L)
    c.link("d3", "p7", "Historial", lpos=(372, 281), anchor="start", **L)
    c.link("p4", "d4", "Dominio", both=True, lpos=(530, 172), anchor="start", **L)
    c.link("d4", "p5", "Estado", lpos=(488, 80), anchor="start", **L)
    c.link("p7", "adulto", "Informe", off=-9, lpos=(478, 316), **L)
    c.link("adulto", "p7", "Solicitud", off=-9, lpos=(478, 376), **L)
    return c.s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "recursos" / "diagramas"
    for name, fn in (("poster_bpmn_as_is", bpmn_as_is), ("poster_bpmn_to_be", bpmn_to_be),
                     ("poster_dfd0", dfd0), ("poster_dfd1", dfd1)):
        (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
        print("ok", name)
