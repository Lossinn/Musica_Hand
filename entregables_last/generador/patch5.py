import re
nuevo = open("cf_nuevo.py", encoding="utf-8").read()
partes = dict(re.findall(r"#@@(\w+)\n(.*?)(?=\n#@@|\Z)", nuevo, re.S))
s = open("construir_entregas.py", encoding="utf-8").read()
# 1) escrito_final -> guia_estudio
a = s.index("def escrito_final("); b = s.index("# ------------------------------------------------------------------ envío")
s = s[:a] + partes["GUIA"].rstrip() + "\n\n\n" + s[b:]
# 2) leeme + main -> nuevos
a = s.index("def leeme(")
s = s[:a] + partes["LEEME"].rstrip() + "\n\n\n" + partes["MAIN"].rstrip() + "\n"
# 3) PREF_EF
s = s.replace('PREF = json.loads((AQUI / "out" / "prefiltro.json").read_text(encoding="utf-8")) if (AQUI / "out" / "prefiltro.json").exists() else {}',
              'PREF = json.loads((AQUI / "out" / "prefiltro.json").read_text(encoding="utf-8")) if (AQUI / "out" / "prefiltro.json").exists() else {}\nPREF_EF = json.loads((AQUI / "out" / "prefiltro_ef.json").read_text(encoding="utf-8")) if (AQUI / "out" / "prefiltro_ef.json").exists() else {}')
assert "PREF_EF" in s
open("construir_entregas.py", "w", encoding="utf-8").write(s)
# 4) meta del escrito final
n = open("ef_nucleo.py", encoding="utf-8").read()
n = n.replace("    def titulo_bloque(self, titulo, autores, docente_lineas, resumen, kw_es, abstract, kw_en):\n        d = self.d\n",
              "    def titulo_bloque(self, titulo, autores, docente_lineas, resumen, kw_es, abstract, kw_en):\n        d = self.d\n        self.meta = dict(titulo=titulo, resumen=resumen, kw=kw_es, abstract=abstract, kwe=kw_en)\n")
assert "self.meta" in n
open("ef_nucleo.py", "w", encoding="utf-8").write(n)
c = open("ef_comun.py", encoding="utf-8").read()
c = c.replace('    e = construir(contenido, ruta)\n', '    e = construir(contenido, ruta)\n    ruta.with_suffix(".json").write_text(json.dumps(e.meta, ensure_ascii=False), encoding="utf-8")\n')
assert "e.meta" in c
open("ef_comun.py", "w", encoding="utf-8").write(c)
print("ok")
