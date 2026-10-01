"""Utilidades de maquetación APA 7 para el documento: figuras, tablas, fórmulas y CSS."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAG = ROOT / "recursos" / "diagramas"
ASSETS = ROOT / "recursos" / "assets"


REFS: dict[tuple[str, str], int] = {}


class Numerador:
    def __init__(self) -> None:
        self.fig = 0
        self.tab = 0
        self.eq = 0


NUM = Numerador()


def svg_inline(nombre: str) -> str:
    """Inserta un SVG del directorio diagramas/ en línea, adaptado al ancho."""
    s = (DIAG / f"{nombre}.svg").read_text(encoding="utf-8")
    return s.replace(' width="', ' data-w="', 1).replace("<svg ", '<svg style="width:100%;height:auto" ', 1)


def figura(titulo: str, cuerpo: str, nota: str = "", *, ancha: bool = False, ref: str | None = None) -> str:
    NUM.fig += 1
    n = NUM.fig
    if ref:
        REFS[('F', ref)] = n
    cls = "figura ancha" if ancha else "figura"
    idd = f' id="{ref}"' if ref else ""
    nt = f'<p class="nota"><em>Nota.</em> {nota}</p>' if nota else ""
    return (f'<figure class="{cls}"{idd}><p class="cap-num">Figura {n}</p><p class="cap-tit"><em>{titulo}</em></p>'
            f'<div class="fig-cuerpo">{cuerpo}</div>{nt}</figure>')


def img(nombre: str, *, carpeta: str = "capturas", ancho: str = "100%", alt: str = "") -> str:
    p = (ASSETS / carpeta / nombre).resolve().as_uri()
    return f'<img src="{p}" alt="{html.escape(alt)}" style="width:{ancho};height:auto">'


def tabla(titulo: str, cabeceras: list[str], filas: list[list[str]], nota: str = "", *,
          anchos: list[str] | None = None, clase: str = "", ref: str | None = None) -> str:
    NUM.tab += 1
    n = NUM.tab
    if ref:
        REFS[('T', ref)] = n
    cols = ""
    if anchos:
        cols = "<colgroup>" + "".join(f'<col style="width:{a}">' for a in anchos) + "</colgroup>"
    th = "".join(f"<th>{c}</th>" for c in cabeceras)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    nt = f'<p class="nota"><em>Nota.</em> {nota}</p>' if nota else ""
    idd = f' id="{ref}"' if ref else ""
    return (f'<div class="tabla {clase}"{idd}><p class="cap-num">Tabla {n}</p><p class="cap-tit"><em>{titulo}</em></p>'
            f'<table class="apa">{cols}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{nt}</div>')


def resolver(html_txt: str) -> str:
    """Sustituye [[F:clave]] y [[T:clave]] por «Figura N» y «Tabla N»."""
    import re

    def rep(m):
        k = (m.group(1), m.group(2))
        assert k in REFS, f"referencia sin destino: {k}"
        return ("Figura " if k[0] == "F" else "Tabla ") + str(REFS[k])
    return re.sub(r"\[\[([FT]):(\w+)\]\]", rep, html_txt)


def ecuacion(expr: str) -> str:
    NUM.eq += 1
    return f'<div class="ecuacion"><span class="eq">{expr}</span><span class="eqn">({NUM.eq})</span></div>'


def H1(t: str, *, salto: bool = False) -> str:
    return f'<h1{" class=salto" if salto else ""}>{t}</h1>'


def H2(t: str) -> str:
    return f"<h2>{t}</h2>"


def H3(t: str) -> str:
    return f"<h3>{t}</h3>"


def P(t: str) -> str:
    return f"<p>{t}</p>"


def UL(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


FONT_FACE = f"""
@font-face {{ font-family: 'Montserrat'; src: url('{(ASSETS / 'fonts' / 'Montserrat.ttf').resolve().as_uri()}'); font-weight: 100 900; font-style: normal; }}
@font-face {{ font-family: 'Montserrat'; src: url('{(ASSETS / 'fonts' / 'Montserrat-Italic.ttf').resolve().as_uri()}'); font-weight: 100 900; font-style: italic; }}
"""

CSS = FONT_FACE + """
@page { size: Letter; margin: 2.54cm; @top-right { content: counter(page); font: 12pt 'Times New Roman', serif; } }
@page wide { size: Letter landscape; margin: 1.8cm 1.6cm; @top-right { content: counter(page); font: 12pt 'Times New Roman', serif; } }
* { box-sizing: border-box; }
html { font-family: 'Times New Roman', Times, serif; font-size: 12pt; color: #000; }
body { margin: 0; line-height: 2; }
p { margin: 0; text-indent: 1.27cm; text-align: left; orphans: 2; widows: 2; }
em { font-style: italic; }
a { color: #000; text-decoration: none; word-break: break-all; }
h1 { font-size: 12pt; font-weight: bold; text-align: center; margin: 0; line-height: 2; break-after: avoid; }
h1.salto { break-before: page; }
h2 { font-size: 12pt; font-weight: bold; text-align: left; margin: 0; line-height: 2; break-after: avoid; }
h3 { font-size: 12pt; font-weight: bold; font-style: italic; text-align: left; margin: 0; line-height: 2; break-after: avoid; }
ul { margin: 0 0 0 1.9cm; padding: 0; line-height: 2; }
li { margin: 0; }
.portada { text-align: center; page-break-after: always; padding-top: 3.2cm; }
.portada p { text-indent: 0; text-align: center; }
.portada .titulo { font-weight: bold; line-height: 1.5; margin: 0 0 1.2cm 0; }
.portada .logos { display: flex; justify-content: center; align-items: center; gap: 1cm; margin: 0 0 1.4cm 0; }
.portada .logos img { height: 2.3cm; width: auto; }
.resumen p { text-indent: 0; }
.palabras { text-indent: 1.27cm; }
.ref p { text-indent: -1.27cm; padding-left: 1.27cm; margin: 0; }
figure { margin: 0; }
.figura, .tabla { break-inside: avoid; margin: 0.35cm 0 0.45cm 0; line-height: 1.25; }
.figura .cap-num, .tabla .cap-num { font-weight: bold; text-indent: 0; margin: 0; }
.figura .cap-tit, .tabla .cap-tit { text-indent: 0; margin: 0 0 0.12cm 0; }
.fig-cuerpo { text-align: center; }
.fig-cuerpo img, .fig-cuerpo svg { max-width: 100%; }
.nota { text-indent: 0; font-size: 10pt; margin: 0.12cm 0 0 0; line-height: 1.25; }
.ancha { page: wide; break-before: page; break-after: page; }
.ancha .fig-cuerpo svg { width: 100%; height: auto; }
table.apa { border-collapse: collapse; width: 100%; font-size: 9.5pt; line-height: 1.22; border-top: 1.2pt solid #000; border-bottom: 1.2pt solid #000; }
table.apa th { text-align: left; font-weight: normal; border-bottom: 0.8pt solid #000; padding: 3pt 5pt; vertical-align: bottom; }
table.apa td { padding: 2.5pt 5pt; vertical-align: top; text-align: left; }
table.apa tr { break-inside: avoid; }
.tabla.larga { break-inside: auto; }
.tabla.chica table.apa { font-size: 9pt; }
.ecuacion { display: flex; justify-content: space-between; align-items: center; margin: 0.15cm 0; line-height: 1.5; text-indent: 0; break-inside: avoid; }
.ecuacion .eq { flex: 1; text-align: center; font-style: italic; }
.ecuacion .eqn { width: 1.6cm; text-align: right; }
.duo { display: flex; gap: 0.4cm; align-items: flex-start; }
.duo > div { flex: 1; }
.pie-fig { font-size: 10pt; text-indent: 0; }
sub, sup { line-height: 0; font-size: 75%; }
.nb { white-space: nowrap; }
"""
