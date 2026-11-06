"""Filtro previo de coincidencias textuales (NO sustituye a Turnitin).
Mide, con segmentos de 8 palabras normalizadas, (a) cuánto se parece cada artículo a los otros dos (Turnitin los comparará entre sí si los tres
se suben al mismo repositorio) y (b) cuánto coincide con textos propios del proyecto que Turnitin pudiera tener (documento final de Proyecto Integrador I,
entrega del 2.º corte, documentos técnicos .md). Excluye referencias. Uso: python -X utf8 prefiltro_similitud.py out/art_roxana.docx out/art_camilo.docx out/art_andrea.docx"""
import json, re, sys, unicodedata
from pathlib import Path
import docx

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent / "8.clorificadordeAgua (2)" / "8.clorificadordeAgua"
K = 8


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.findall(r"[a-z0-9ñ]+", "".join(c for c in t if not unicodedata.combining(c)))


def texto(ruta):
    d = docx.Document(str(ruta)); out = []
    for p in d.paragraphs:
        if p.text.strip().startswith("References"):
            break
        out.append(p.text)
    for t in d.tables[2:]:
        pass
    return "\n".join(out)


def sh(tok):
    return [" ".join(tok[i:i + K]) for i in range(len(tok) - K + 1)]


def tramo_max(marc):
    mx = c = 0
    for x in marc:
        c = c + 1 if x else 0
        mx = max(mx, c)
    return mx + K - 1 if mx else 0


arts = {Path(a).stem.replace("art_", ""): sh(norm(texto(a))) for a in sys.argv[1:]}
FUENTES = {
    "PI-I documento final (docx)": RAIZ / "Documentos tecnicos" / "PROYECTO CLORIFICADOR DE AGUA FINAL.docx",
    "Entrega 2.º corte (md)": RAIZ / "ENTREGA_SEGUNDO_CORTE_GESTION_TECNOLOGICA.md",
    "Modelo matemático (md)": RAIZ / "01_Documentacion_Tecnica" / "Modelo_Matematico_y_Mecanica_de_Fluidos.md",
    "Especificaciones (md)": RAIZ / "01_Documentacion_Tecnica" / "Especificaciones_Tecnicas_Prototipo_PVC.md",
    "Presupuesto (md)": RAIZ / "02_Contratos_y_CI" / "Presupuesto_y_Costos_Prototipo.md",
    "DOE (md)": RAIZ / "03_Protocolos_y_Ensayos_Laboratorio" / "Diseño_de_Experimentos_Estadisticos_DOE.md",
    "Propuesta CI (docx)": RAIZ / "Documentos del CI" / "Propuesta CI - Clorificador De Agua.docx",
}
res = {"palabras": {k: len(v) + K - 1 for k, v in arts.items()}, "entre_articulos": {}, "contra_fuentes": {}}
for a in arts:
    for b in arts:
        if a >= b:
            continue
        conj = set(arts[b]); marc = [s in conj for s in arts[a]]
        res["entre_articulos"][f"{a} vs {b}"] = {"pct_de_a": round(100 * sum(marc) / len(marc), 2), "tramo_max_palabras": tramo_max(marc)}
for nombre, ruta in FUENTES.items():
    if ruta.suffix == ".docx":
        d = docx.Document(str(ruta)); txt = "\n".join(p.text for p in d.paragraphs)
    else:
        txt = ruta.read_text(encoding="utf-8", errors="ignore")
    conj = set(sh(norm(txt)))
    res["contra_fuentes"][nombre] = {}
    for a, s in arts.items():
        marc = [x in conj for x in s]
        res["contra_fuentes"][nombre][a] = {"pct": round(100 * sum(marc) / len(marc), 2), "tramo_max_palabras": tramo_max(marc)}
(AQUI / "prefiltro_similitud.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
