"""Ajusta ef_nucleo.py a las medidas del PDF de referencia (carta, márgenes 2 cm, Times 10/12 pt, columnas 8,4 cm, reglas finas)."""
s = open("ef_nucleo.py", encoding="utf-8").read()


def sub(a, b, n=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, n)


sub("AZUL = RGBColor(0x1F, 0x38, 0x64)", "AZUL = RGBColor(0x14, 0x37, 0x5A)")
sub('"prisma"' if False else '"wilsonci": "10.1080/01621459.1927.10502953", "wozniak": "10.55782/ane-1994-1003",',
    '"wilsonci": "10.1080/01621459.1927.10502953", "wozniak": "10.55782/ane-1994-1003", "prisma": "10.1136/bmj.n71",')
# página y texto
sub("pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(0); pf.line_spacing = 1.12",
    "pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(0); pf.line_spacing = Pt(12)")
sub("s.left_margin = s.right_margin = Cm(1.9); s.top_margin = Cm(2.4); s.bottom_margin = Cm(2.2)",
    "s.left_margin = s.right_margin = Cm(2.0); s.top_margin = Cm(2.0); s.bottom_margin = Cm(2.0)")
sub('s.header_distance = Cm(1.1); s.footer_distance = Cm(1.1)', 's.header_distance = Cm(0.9); s.footer_distance = Cm(0.9)')
# regla del encabezado 0,3 pt
sub('for k, v in (("val", "single"), ("sz", "4"), ("space", "3"), ("color", "000000")):\n            bt.set(qn(f"w:{k}"), v)\n        b.append(bt); pPr.append(b)\n        # pie',
    'for k, v in (("val", "single"), ("sz", "3"), ("space", "3"), ("color", "000000")):\n            bt.set(qn(f"w:{k}"), v)\n        b.append(bt); pPr.append(b)\n        # pie')
# columnas: separación 0,75 cm (ya) ; sangría 0,45
sub("p.paragraph_format.first_line_indent = Cm(0.5)\n        p.paragraph_format.widow_control = True", "p.paragraph_format.first_line_indent = Cm(0.45)\n        p.paragraph_format.widow_control = True")
# título y bloque inicial
sub("""        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.0
        self._texto(p, titulo, 17, True, None, AZUL)
        for fila in autores:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._texto(p, fila, 11)
        d.add_paragraph().paragraph_format.space_after = Pt(2)
        for l in docente_lineas:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._texto(p, l, 10)
        self._regla(d.add_paragraph(), 14, 6)
        for rot, txt in (("Resumen.", resumen), ("Palabras clave:", kw_es), ("Abstract.", abstract), ("Keywords:", kw_en)):
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(5)
            r = p.add_run(rot + " "); _fuente(r, 9.5, True)
            self._texto(p, txt, 9.5)
        self._regla(d.add_paragraph(), 2, 8)""",
    """        titulos = titulo if isinstance(titulo, (list, tuple)) else [titulo]
        for k, tt in enumerate(titulos):
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8 if k == 0 else 4); p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = Pt(21 if k == 0 else 16)
            self._texto(p, tt, 17 if k == 0 else 13, True, None, AZUL)
        for fila in autores:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = Pt(15)
            self._texto(p, fila, 12)
        d.add_paragraph().paragraph_format.space_after = Pt(0)
        for l in docente_lineas:
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._texto(p, l, 10)
        self._regla(d.add_paragraph(), 12, 6)
        for rot, txt in (("Resumen.", resumen), ("Palabras clave:", kw_es), ("Abstract.", abstract), ("Keywords:", kw_en)):
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(rot + " "); _fuente(r, 10, True)
            self._texto(p, txt, 10)
        self._regla(d.add_paragraph(), 2, 8)""")
sub('for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "000000")):\n            bt.set(qn(f"w:{k}"), v)\n        b.append(bt); p._p.get_or_add_pPr().append(b)',
    'for k, v in (("val", "single"), ("sz", "3"), ("space", "1"), ("color", "000000")):\n            bt.set(qn(f"w:{k}"), v)\n        b.append(bt); p._p.get_or_add_pPr().append(b)')
# secciones 12 / 10
sub('self._texto(p, f"{self.n_sec}. {titulo}", 12.5, True)', 'self._texto(p, f"{self.n_sec}. {titulo}", 12, True)')
sub('self._texto(p, f"{self.n_sec}.{self.n_sub} {titulo}", 10.5, True)', 'self._texto(p, f"{self.n_sec}.{self.n_sub} {titulo}", 10, True)')
sub("self._texto(p, titulo, 12.5, True)\n\n    def P(", "self._texto(p, titulo, 12, True)\n\n    def P(")
# tablas: 9 pt y reglas 0,8 / 0,5
sub("def tabla(self, clave, caption, cab, filas, anchos, size=8.5, alinear=None):", "def tabla(self, clave, caption, cab, filas, anchos, size=9, alinear=None):")
sub('self._borde_celdas(t.rows[0], "top", 8); self._borde_celdas(t.rows[0], "bottom", 4); self._borde_celdas(t.rows[-1], "bottom", 8)',
    'self._borde_celdas(t.rows[0], "top", 6); self._borde_celdas(t.rows[0], "bottom", 4); self._borde_celdas(t.rows[-1], "bottom", 6)')
# figuras: una o dos imágenes
sub("""        p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6); p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(FIG / archivo), width=Cm(ancho_cm))""",
    """        if isinstance(archivo, (list, tuple)) and len(archivo) > 1:
            t = self.d.add_table(rows=1, cols=len(archivo)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for i, a_ in enumerate(archivo):
                pc = t.rows[0].cells[i].paragraphs[0]; pc.alignment = WD_ALIGN_PARAGRAPH.CENTER; pc.paragraph_format.keep_with_next = True
                pc.add_run().add_picture(str(FIG / a_), width=Cm(ancho_cm))
        else:
            if isinstance(archivo, (list, tuple)):
                archivo = archivo[0]
            p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6); p.paragraph_format.keep_with_next = True
            p.add_run().add_picture(str(FIG / archivo), width=Cm(ancho_cm))""")
# referencias: 10 pt, sangría francesa 0,35, 7 pt
sub("pf = p.paragraph_format; pf.left_indent = Cm(0.5); pf.first_line_indent = Cm(-0.5); pf.space_after = Pt(4)\n            self._texto(p, ref_larga(c), 9)",
    "pf = p.paragraph_format; pf.left_indent = Cm(0.35); pf.first_line_indent = Cm(-0.35); pf.space_after = Pt(7)\n            self._texto(p, ref_larga(c), 10)")
# guionado automático y español
sub("        self._config()\n", "        self._config()\n        self._guionado()\n")
sub("    # ---- columnas\n", '''    def _guionado(self):
        ajustes = self.d.settings.element
        h = OxmlElement("w:autoHyphenation"); h.set(qn("w:val"), "true"); ajustes.append(h)
        z = OxmlElement("w:hyphenationZone"); z.set(qn("w:val"), "283"); ajustes.append(z)
        rpr = self.d.styles["Normal"].element.get_or_add_rPr()
        lg = OxmlElement("w:lang"); lg.set(qn("w:val"), "es-ES"); lg.set(qn("w:eastAsia"), "es-ES"); rpr.append(lg)

    # ---- columnas
''')
open("ef_nucleo.py", "w", encoding="utf-8").write(s)
print("ok")
