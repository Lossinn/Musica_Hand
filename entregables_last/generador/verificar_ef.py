"""Verificación automática del formato de los escritos finales (márgenes, fuentes, restos de marcas, numeración, figuras dentro de página)."""
import re, sys
import pymupdf
from pathlib import Path
from docx2pdf import convert
rutas = sorted(Path("out").glob("ef_*.docx"))
for r in rutas:
    pdf = r.with_suffix(".pdf")
    if "--skip" not in sys.argv: convert(str(r), str(pdf))
    d = pymupdf.open(str(pdf)); W, H = d[0].rect.width, d[0].rect.height
    fuentes = set(f[3].split("+")[-1] for p in d for f in p.get_fonts())
    txt = "".join(p.get_text() for p in d)
    malos = [m for m in ("{cite", "{tab", "{fig", "{eq", "**", "$", "?)") if m in txt]
    interrogaciones = len(re.findall(r"Cuadro \?|Figura \?|\(\?\)", txt))
    mnx = mny = 1e9; mxx = mxy = 0; fuera = 0; ult = None
    for i, p in enumerate(d):
        bl = [b for b in p.get_text("blocks") if b[4].strip() and 40 < b[1] < H - 45]
        if bl:
            mnx = min(mnx, min(b[0] for b in bl)); mxx = max(mxx, max(b[2] for b in bl))
            mny = min(mny, min(b[1] for b in bl)); mxy = max(mxy, max(b[3] for b in bl))
        for im in p.get_image_info():
            x0, y0, x1, y1 = im["bbox"]
            if x0 < 0 or x1 > W + 1 or y1 > H + 1: fuera += 1
        if i == len(d) - 1:
            ult = max([b[3] for b in bl], default=0) / H
    cuadros = sorted(set(int(x) for x in re.findall(r"Cuadro (\d+):", txt))); figs = sorted(set(int(x) for x in re.findall(r"Figura (\d+):", txt)))
    print(f"{r.stem}: {len(d)} págs | {W/72*2.54:.1f}x{H/72*2.54:.1f} cm | márgenes texto x[{mnx/72*2.54:.2f}, {(W-mxx)/72*2.54:.2f}] cm | fuentes {sorted(fuentes)} | marcas sobrantes {malos} | '?' {interrogaciones} | cuadros {cuadros} | figuras {figs} | img fuera {fuera} | última pág. llena hasta {ult:.0%}")
