"""Repara cadenas de una línea que quedaron partidas por saltos de línea literales."""
import ast, sys
BS = chr(92)
for p in sys.argv[1:]:
    L = open(p, encoding="utf-8").read().split("\n"); out = []; i = 0
    while i < len(L):
        line = L[i]
        while line.count(chr(34)) % 2 == 1 and i + 1 < len(L) and not line.lstrip().startswith("#") and '"""' not in line:
            i += 1; line = line + BS + "n" + L[i]
        out.append(line); i += 1
    open(p, "w", encoding="utf-8").write("\n".join(out))
    ast.parse(open(p, encoding="utf-8").read()); print(p, "sintaxis ok")
