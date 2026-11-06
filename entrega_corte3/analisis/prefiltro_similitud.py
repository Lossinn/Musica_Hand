"""Filtro previo de coincidencias textuales (NO sustituye a Turnitin).

Compara el texto del artículo con las fuentes propias del proyecto que Turnitin podría tener en su
base: documento_tecnico.md, el documento EBT del 2.º corte (documento.html) y los .md del repositorio.
Método: segmentos (shingles) de 8 palabras normalizadas; informa el % de segmentos del artículo que
aparecen en cada fuente y las coincidencias consecutivas más largas.
Uso: python -X utf8 prefiltro_similitud.py
"""
import re, sys, json, unicodedata, zipfile
from pathlib import Path
import docx

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
K = 8

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9ñ]+", t)

def texto_articulo():
    d = docx.Document(str(AQUI.parent / "articulo" / "Articulo_Maquetado_EquipoNN.docx"))
    partes = []
    cortar = False
    for p in d.paragraphs:
        if p.text.strip().startswith("References"):
            break  # se excluye la bibliografía, como en la configuración de Turnitin
        partes.append(p.text)
    return "\n".join(partes)

FUENTES = {
    "documento_tecnico.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/anexos/documento_tecnico.md",
    "motor_analitico_y_estado_avance.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/anexos/motor_analitico_y_estado_avance.md",
    "borrador_cap6.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/borrador.md",
    "documento_2do_corte (html)": RAIZ / "entregable_2do_corte/_fuentes/documento.html",
    "README_03_Codigo.md": RAIZ / "03_Codigo/README.md",
}

def shingles(tokens):
    return [" ".join(tokens[i:i + K]) for i in range(len(tokens) - K + 1)]

art = norm(texto_articulo())
sh_art = shingles(art)
res = {"palabras_articulo": len(art), "segmentos": len(sh_art), "fuentes": {}}
for nombre, ruta in FUENTES.items():
    if not ruta.exists():
        continue
    txt = ruta.read_text(encoding="utf-8", errors="ignore")
    if ruta.suffix == ".html":
        txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", txt)
    tok = norm(txt)
    conj = set(shingles(tok))
    marcados = [s in conj for s in sh_art]
    pct = 100 * sum(marcados) / max(1, len(sh_art))
    # tramos consecutivos
    tramos, i = [], 0
    while i < len(marcados):
        if marcados[i]:
            j = i
            while j < len(marcados) and marcados[j]:
                j += 1
            tramos.append((i, j - i + K - 1))
            i = j
        else:
            i += 1
    tramos.sort(key=lambda x: -x[1])
    res["fuentes"][nombre] = {"pct_segmentos_coincidentes": round(pct, 2),
        "tramos_top": [{"palabras": n, "texto": " ".join(art[a:a + n])[:260]} for a, n in tramos[:6]]}
(AQUI / "prefiltro_similitud.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("palabras del artículo (sin referencias):", res["palabras_articulo"])
for n, r in res["fuentes"].items():
    print(f"\n== {n}: {r['pct_segmentos_coincidentes']} % de los segmentos de 8 palabras")
    for t in r["tramos_top"][:4]:
        print(f"   [{t['palabras']} palabras] {t['texto']}")
