"""Búsqueda reproducible para el flujo PRISMA (OpenAlex API). Guarda conteos y candidatos en busqueda_prisma.json.
Fase 1 (identificación): ecuación booleana sobre título y resumen, 2020-2026, artículos, inglés o español.
Fase 2 (cribado): el título debe contener chlorination, chlorinator o chlorine (regla automática, reproducible).
La elegibilidad y la inclusión se aplican después sobre los títulos del cribado (ver seleccion_prisma.py).
Uso: python -X utf8 busqueda_prisma.py"""
import json, urllib.parse, urllib.request, urllib.error, datetime, time
ECUACION = ('(chlorination OR chlorinator OR chlorine OR chlorinators) AND (passive OR "in-line" OR inline OR dispenser OR "tablet" OR "gravity-fed" OR "gravity-driven") '
            'AND (rural OR community OR household OR "low-cost" OR "point-of-collection" OR "point-of-use")')
BASE = "https://api.openalex.org/works"
def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "clorificador-prisma/1.0 (mailto:roxana.munoz@upb.edu.co)"})
    for intento in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as f:
                time.sleep(1.5); return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (intento + 1))
    raise RuntimeError("OpenAlex limita la tasa")
TA = "title_and_abstract.search:" + ECUACION
VENT = "from_publication_date:2020-01-01,to_publication_date:2026-11-06"
out = {"fecha": datetime.date.today().isoformat(), "ecuacion": ECUACION, "fuente": "OpenAlex API"}
out["identificados_total_sin_filtros"] = get({"filter": TA, "per-page": 1})["meta"]["count"]
out["identificados_ventana"] = get({"filter": f"{TA},{VENT}", "per-page": 1})["meta"]["count"]
F = f"{TA},{VENT},type:article,language:en|es,has_doi:true"
out["tras_filtros_tipo_idioma_doi"] = get({"filter": F, "per-page": 1})["meta"]["count"]
out["cribados_titulo_con_chlorin"] = get({"filter": F + ",title.search:(chlorination OR chlorinator OR chlorine OR chlorinators)", "per-page": 1})["meta"]["count"]
cands = []
for page in (1, 2, 3):
    r = get({"filter": F + ",title.search:(chlorination OR chlorinator OR chlorine OR chlorinators)", "sort": "relevance_score:desc", "search": "passive in-line chlorination rural community drinking water", "per-page": 100, "page": page,
             "select": "id,doi,title,publication_year,primary_location,authorships,cited_by_count"})
    for w in r["results"]:
        cands.append({"doi": (w.get("doi") or "").replace("https://doi.org/", ""), "titulo": w.get("title"), "anio": w.get("publication_year"),
                      "revista": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                      "citas": w.get("cited_by_count"), "autores": "; ".join(a["author"]["display_name"] for a in w["authorships"][:3])})
    if len(r["results"]) < 100: break
out["candidatos"] = cands
json.dump(out, open("busqueda_prisma.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v for k, v in out.items() if k != "candidatos"}, len(cands))
for i, c in enumerate(cands, 1):
    print(i, c["anio"], "|", (c["titulo"] or "")[:120], "|", (c["revista"] or "")[:28], "|", c["doi"])
