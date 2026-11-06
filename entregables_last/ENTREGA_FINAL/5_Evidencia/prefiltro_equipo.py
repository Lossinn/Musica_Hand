"""Filtro previo de coincidencias (NO sustituye a Turnitin): compara entre sí los artículos del equipo y contra fuentes propias.
Segmentos de 8 palabras normalizadas; se excluyen las referencias. Uso: python -X utf8 prefiltro_equipo.py <carpeta_con_art_*.docx> <salida.json>"""
import json, re, sys, unicodedata
from pathlib import Path
import docx

K = 8
RAIZ = Path(r"C:\Users\Alejando\Desktop\Hand_Kid_Sing\musica_hand")


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.findall(r"[a-z0-9ñ]+", "".join(c for c in t if not unicodedata.combining(c)))


def texto(ruta):
    out = []
    for p in docx.Document(str(ruta)).paragraphs:
        if p.text.strip().startswith(("References", "Referencias")):
            break
        out.append(p.text)
    return "\n".join(out)


def sh(tok):
    return set(" ".join(tok[i:i + K]) for i in range(len(tok) - K + 1)), [" ".join(tok[i:i + K]) for i in range(len(tok) - K + 1)]


def tramo(marc):
    mx = c = 0
    for x in marc:
        c = c + 1 if x else 0
        mx = max(mx, c)
    return mx + K - 1 if mx else 0


carpeta = Path(sys.argv[1])
patron = sys.argv[3] if len(sys.argv) > 3 else "art_*.docx"
arts = {p.stem.split("_", 1)[1]: sh(norm(texto(p)))[1] for p in sorted(carpeta.glob(patron))}
res = {"palabras": {k: len(v) + K - 1 for k, v in arts.items()}, "entre_articulos": {}, "contra_fuentes": {}}
for a in arts:
    for b in arts:
        if a < b:
            conj = set(arts[b]); marc = [s in conj for s in arts[a]]
            res["entre_articulos"][f"{a} vs {b}"] = {"pct": round(100 * sum(marc) / len(marc), 2), "tramo_max": tramo(marc)}
FUENTES = {
    "documento_tecnico.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/anexos/documento_tecnico.md",
    "documento_2do_corte (html)": RAIZ / "entregable_2do_corte/_fuentes/documento.html",
    "motor_analitico_y_estado_avance.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/anexos/motor_analitico_y_estado_avance.md",
    "articulo_anterior_Pemberty.docx": RAIZ / "entregables_last/_versiones_anteriores/articulo/Articulo_Maquetado_EquipoNN_Pemberty.docx",
    "capitulo6_borrador.md": RAIZ / "06_Documentos_por_capitulo/Capitulo_6/borrador.md",
    "README.md": RAIZ / "README.md",
}
for nombre, ruta in FUENTES.items():
    if not ruta.exists():
        continue
    if ruta.suffix == ".docx":
        txt = texto(ruta)
    else:
        txt = ruta.read_text(encoding="utf-8", errors="ignore")
        if ruta.suffix == ".html":
            txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S); txt = re.sub(r"<[^>]+>", " ", txt)
    conj = sh(norm(txt))[0]
    res["contra_fuentes"][nombre] = {a: {"pct": round(100 * sum(x in conj for x in s) / len(s), 2), "tramo_max": tramo([x in conj for x in s])} for a, s in arts.items()}
Path(sys.argv[2]).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("palabras", res["palabras"])
print("entre artículos (máx):", max(v["pct"] for v in res["entre_articulos"].values()), "tramo máx", max(v["tramo_max"] for v in res["entre_articulos"].values()))
for k, v in res["entre_articulos"].items():
    if v["pct"] > 8: print("  ", k, v)
for n, d in res["contra_fuentes"].items(): print(n, {a: x["pct"] for a, x in d.items()})
