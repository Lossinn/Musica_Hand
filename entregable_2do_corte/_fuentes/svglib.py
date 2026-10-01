"""Primitivas SVG para diagramas BPMN 2.0 y DFD (Yourdon-DeMarco).

Todo es vectorial: se inserta en línea en el documento y en el póster.
"""
from __future__ import annotations

import html

INK = "#141414"
YELLOW = "#FFCC00"
YELLOW_SOFT = "#FFF1BF"
GRAY_L = "#F5F5F5"
GRAY_M = "#D9D9D9"
GRAY_D = "#404040"
TEAL = "#1FA99B"
RED = "#B3261E"
FONT = "Helvetica, Arial, sans-serif"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def wrap(text: str, width: int) -> list[str]:
    """Corte de línea por número de caracteres, respetando palabras y '\n'."""
    out: list[str] = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            if line and len(line) + 1 + len(w) > width:
                out.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        out.append(line)
    return out


class SVG:
    def __init__(self, w: int, h: int, title: str = "") -> None:
        self.w, self.h, self.title = w, h, title
        self.parts: list[str] = []
        self.parts.append(
            f'<defs>'
            f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="arrO" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="#fff" stroke="{INK}" stroke-width="1.2"/></marker>'
            f'<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7">'
            f'<circle cx="5" cy="5" r="3.6" fill="#fff" stroke="{INK}" stroke-width="1.4"/></marker>'
            f'<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
            f'</defs>')

    # ------------------------------------------------------------ básicos
    def add(self, s: str) -> None:
        self.parts.append(s)

    def rect(self, x, y, w, h, *, fill="#fff", stroke=INK, sw=1.4, rx=0, dash=None, opacity=None) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def line(self, x1, y1, x2, y2, *, stroke=INK, sw=1.2, dash=None) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, text, *, size=12, anchor="middle", weight=500, fill=INK,
             italic=False, width=None, lh=1.22, rotate=None, valign="middle") -> None:
        lines = wrap(text, width) if width else text.split("\n")
        n = len(lines)
        if valign == "middle":
            y0 = y - (n - 1) * size * lh / 2
        elif valign == "top":
            y0 = y + size * 0.9
        else:
            y0 = y - (n - 1) * size * lh
        st = ' font-style="italic"' if italic else ""
        tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        if n == 1:
            spans = esc(lines[0])
        else:
            spans = "".join(
                f'<tspan x="{x}" dy="{0 if i == 0 else size * lh}">{esc(l)}</tspan>' for i, l in enumerate(lines))
        self.add(f'<text x="{x}" y="{y0}" font-size="{size}" text-anchor="{anchor}" '
                 f'dominant-baseline="central" font-weight="{weight}" fill="{fill}"{st}{tr}>{spans}</text>')

    def path(self, pts, *, stroke=INK, sw=1.5, dash=None, end="arr", start=None, fill="none") -> None:
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{end})"' if end else ""
        ms = f' marker-start="url(#{start})"' if start else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{me}{ms} '
                 f'stroke-linejoin="round"/>')

    # ------------------------------------------------------------- BPMN
    def pool(self, x, y, w, h, title, lanes=None, *, band=30, fill="#fff") -> None:
        """Pool con banda de título vertical; `lanes` = [(nombre, alto), ...]."""
        self.rect(x, y, w, h, fill=fill, sw=1.8)
        self.rect(x, y, band, h, fill=GRAY_L, sw=1.8)
        self.text(x + band / 2, y + h / 2, title, size=13, weight=700, rotate=-90, width=max(10, int(h / 7.5)))
        if lanes:
            ly = y
            for i, (name, lh) in enumerate(lanes):
                if i:
                    self.line(x + band, ly, x + w, ly, sw=1.2)
                self.rect(x + band, ly, 24, lh, fill="#fff", sw=1.2)
                self.text(x + band + 12, ly + lh / 2, name, size=11, weight=600, rotate=-90,
                          width=max(8, int(lh / 6.6)))
                ly += lh

    def task(self, cx, cy, w, h, label, *, fill="#fff", size=11.5, chars=None, icon=None, stroke=INK, sw=1.6) -> None:
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=stroke, sw=sw, rx=9)
        ch = chars or max(8, int((w - (14 if icon else 6)) / (size * 0.56)))
        self.text(cx, cy + (3 if icon else 0), label, size=size, width=ch, weight=500)
        if icon == "user":   # tarea manual / usuario
            self.add(f'<circle cx="{cx - w/2 + 11}" cy="{cy - h/2 + 9}" r="3.2" fill="none" stroke="{INK}" stroke-width="1.1"/>'
                     f'<path d="M{cx - w/2 + 5},{cy - h/2 + 18} q6,-7 12,0" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        elif icon == "svc":  # tarea de servicio (engranaje simplificado)
            self.add(f'<circle cx="{cx - w/2 + 11}" cy="{cy - h/2 + 11}" r="4.2" fill="none" stroke="{INK}" stroke-width="1.1"/>'
                     f'<circle cx="{cx - w/2 + 11}" cy="{cy - h/2 + 11}" r="1.4" fill="{INK}"/>')

    def event(self, cx, cy, kind="start", label=None, *, r=15, lpos="below", lw=16, size=11) -> None:
        sw = 4 if kind.startswith("end") else 1.6
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="{sw}"/>')
        if kind in ("timer", "msg-catch"):
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r - 3.5}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        if kind == "timer":
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r - 7}" fill="none" stroke="{INK}" stroke-width="1.1"/>'
                     f'<path d="M{cx},{cy - r + 8.5} L{cx},{cy} L{cx + 3.6},{cy + 2.4}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        if kind in ("msg-start", "msg-catch"):
            a = r * 0.5
            self.add(f'<rect x="{cx - a}" y="{cy - a * 0.72}" width="{2 * a}" height="{1.44 * a}" fill="none" stroke="{INK}" stroke-width="1.1"/>'
                     f'<path d="M{cx - a},{cy - a * 0.72} L{cx},{cy + 0.05 * a} L{cx + a},{cy - a * 0.72}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        if label:
            if lpos == "below":
                self.text(cx, cy + r + 10 + (0), label, size=size, width=lw, weight=500, valign="top")
            elif lpos == "above":
                self.text(cx, cy - r - 10, label, size=size, width=lw, weight=500, valign="bottom")
            elif lpos == "right":
                self.text(cx + r + 6, cy, label, size=size, anchor="start", width=lw, weight=500)

    def gateway(self, cx, cy, kind="xor", label=None, *, s=26, lpos="above", lw=22, size=11) -> None:
        self.add(f'<polygon points="{cx},{cy - s} {cx + s},{cy} {cx},{cy + s} {cx - s},{cy}" fill="#fff" '
                 f'stroke="{INK}" stroke-width="1.8"/>')
        k = s * 0.42
        if kind == "xor":
            self.line(cx - k, cy - k, cx + k, cy + k, sw=2.4); self.line(cx - k, cy + k, cx + k, cy - k, sw=2.4)
        elif kind == "par":
            self.line(cx - k * 1.2, cy, cx + k * 1.2, cy, sw=2.6); self.line(cx, cy - k * 1.2, cx, cy + k * 1.2, sw=2.6)
        elif kind == "inc":
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{k * 1.05}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
        if label:
            if lpos == "above":
                self.text(cx, cy - s - 9, label, size=size, width=lw, weight=600, valign="bottom")
            elif lpos == "below":
                self.text(cx, cy + s + 9, label, size=size, width=lw, weight=600, valign="top")

    def flow(self, pts, label=None, *, lx=None, ly=None, size=10.5, anchor="middle") -> None:
        self.path(pts)
        if label:
            x, y = (lx, ly) if lx is not None else (pts[0][0], pts[0][1])
            self.text(x, y, label, size=size, weight=600, anchor=anchor, fill=GRAY_D)

    def msg(self, pts, label=None, *, lx=None, ly=None, size=10.5, anchor="start") -> None:
        self.path(pts, dash="6 4", sw=1.4, end="arrO", start="dot")
        if label:
            x, y = (lx, ly) if lx is not None else (pts[0][0] + 5, (pts[0][1] + pts[-1][1]) / 2)
            self.text(x, y, label, size=size, weight=500, anchor=anchor, italic=True, fill=GRAY_D)

    def badge(self, cx, cy, n) -> None:
        self.add(f'<circle cx="{cx}" cy="{cy}" r="10.5" fill="{RED}"/>')
        self.text(cx, cy + 0.5, str(n), size=11.5, weight=700, fill="#fff")

    # -------------------------------------------------------------- DFD
    def process(self, cx, cy, r, num, label, *, size=11.5, fill="#fff", chars=None) -> None:
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.9"/>')
        self.line(cx - r * 0.86, cy - r * 0.42, cx + r * 0.86, cy - r * 0.42, sw=1.1)
        self.text(cx, cy - r * 0.68, num, size=size, weight=700)
        self.text(cx, cy + r * 0.14, label, size=size, width=chars or max(9, int(r * 1.5 / (size * 0.56))), weight=500)

    def entity(self, cx, cy, w, h, label, *, size=12, fill=GRAY_L) -> None:
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, sw=1.9)
        self.text(cx, cy, label, size=size, width=max(8, int(w / (size * 0.56))), weight=600)

    def store(self, cx, cy, w, h, code, label, *, size=11) -> None:
        x0, y0 = cx - w / 2, cy - h / 2
        self.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{YELLOW_SOFT}" stroke="none"/>')
        self.line(x0, y0, x0 + w, y0, sw=1.9); self.line(x0, y0 + h, x0 + w, y0 + h, sw=1.9)
        self.line(x0 + 40, y0, x0 + 40, y0 + h, sw=1.2)
        self.text(x0 + 20, cy, code, size=size, weight=700)
        self.text(x0 + 46 + (w - 46) / 2, cy, label, size=size, width=max(8, int((w - 50) / (size * 0.56))), weight=500)

    def dflow(self, pts, label=None, *, lx=None, ly=None, size=10, anchor="middle", both=False) -> None:
        self.path(pts, start="arr" if both else None)
        if label:
            x, y = (lx, ly) if lx is not None else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 8)
            self.add(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="central" '
                     f'font-weight="500" fill="{GRAY_D}" paint-order="stroke" stroke="#fff" stroke-width="4" '
                     f'stroke-linejoin="round">' + "".join(
                         f'<tspan x="{x}" dy="{0 if i == 0 else size * 1.2}">{esc(l)}</tspan>'
                         for i, l in enumerate(label.split("\n"))) + "</text>")

    # ------------------------------------------------------------ salida
    def svg(self, *, bg="#fff", standalone=True) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'font-family="{FONT}" role="img" aria-label="{esc(self.title)}"')
        if standalone:
            head += f' width="{self.w}" height="{self.h}"'
        else:
            head += ' width="100%"'
        head += ">"
        body = f'<rect width="{self.w}" height="{self.h}" fill="{bg}"/>' + "".join(self.parts)
        return head + body + "</svg>"
