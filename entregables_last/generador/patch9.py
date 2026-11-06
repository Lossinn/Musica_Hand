"""Etiquetas «Tabla/Figura», subtítulo sin número y nota de fuente en ef_nucleo.py."""
s = open("ef_nucleo.py", encoding="utf-8").read()


def sub(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


sub('self.nuevas[f"tab:{clave}"] = f"Cuadro {self.n_tab}"', 'self.nuevas[f"tab:{clave}"] = f"Tabla {self.n_tab}"')
sub('r = p.add_run(f"Cuadro {self.n_tab}: "); _fuente(r, 9, True)', 'r = p.add_run(f"Tabla {self.n_tab}. "); _fuente(r, 9, True)')
sub('r = c.add_run(f"Figura {self.n_fig}: "); _fuente(r, 9, True)', 'r = c.add_run(f"Figura {self.n_fig}. "); _fuente(r, 9, True)')
sub("    def P(self, texto, sangria=True, keep=False):", '''    def sub3(self, titulo):
        p = self.d.add_paragraph(); pf = p.paragraph_format
        pf.space_before = Pt(4); pf.space_after = Pt(2); pf.keep_with_next = True
        self._texto(p, titulo, 10, True, True)

    def nota(self, texto):
        p = self.d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(8)
        self._texto(p, texto, 8.5)

    def P(self, texto, sangria=True, keep=False):''')
open("ef_nucleo.py", "w", encoding="utf-8").write(s)
print("ok")
