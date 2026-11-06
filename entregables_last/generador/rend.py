import sys, pymupdf
from docx2pdf import convert
d='../ENTREGA_FINAL/_trabajo/'
convert(d+'Articulo_EquipoNN_articulo.docx', d+'Articulo_EquipoNN_articulo.pdf')
doc=pymupdf.open(d+'Articulo_EquipoNN_articulo.pdf'); print('paginas',len(doc))
for i,p in enumerate(doc): p.get_pixmap(dpi=80).save(d+f'pg{i+1:02d}.png')
