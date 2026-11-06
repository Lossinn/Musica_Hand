"""Búsqueda reproducible para el flujo PRISMA (OpenAlex). Guarda conteos y candidatos en busqueda_prisma.json.
Ecuación (campo título/resumen/palabras): ver ECUACION. Filtros: 2020-2026, tipo artículo, inglés o español.
Uso: python -X utf8 busqueda_prisma.py"""
import json, urllib.parse, urllib.request, datetime, time
ECUACION = ('("chlorination" OR "chlorinator" OR "chlorine dosing" OR "chlorine dispenser" OR "chlorine tablet") '
            'AND ("rural" OR "low-cost" OR "community" OR "point-of-use") '
            'AND ("passive" OR "gravity" OR "in-line" OR "bypass" OR "residual" OR "decay")')
BASE = "https://api.openalex.org/works"
def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "clorificador-prisma/1.0 (mailto:roxana.munoz@upb.edu.co)"})
    for intento in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as f:
                time.sleep(1.5)
                return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (intento + 1))
    raise RuntimeError("OpenAlex limita la tasa")
out = {"fecha": datetime.date.today().isoformat(), "ecuacion": ECUACION, "fuente": "OpenAlex API"}
f0 = "from_publication_date:2020-01-01,to_publication_date:2026-11-06"
# 1 identificados (sin filtros de tipo/idioma, solo ventana temporal)
r = get({"search": ECUACION, "filter": f0, "per-page": 1})
out["identificados_ventana_2020_2026"] = r["meta"]["count"]
# 2 sin filtro temporal (referencia)
r = get({"search": ECUACION, "per-page": 1}); out["identificados_sin_filtro_tiempo"] = r["meta"]["count"]
# 3 tipo artículo + idioma
f1 = f0 + ",type:article,language:en|es"
r = get({"search": ECUACION, "filter": f1, "per-page": 1}); out["tras_filtros_tipo_idioma"] = r["meta"]["count"]
# 4 con DOI
f2 = f1 + ",has_doi:true"
r = get({"search": ECUACION, "filter": f2, "per-page": 1}); out["con_doi"] = r["meta"]["count"]
# 5 candidatos: 200 más relevantes
cands = []
for page in (1, 2):
    r = get({"search": ECUACION, "filter": f2, "per-page": 100, "page": page,
             "select": "id,doi,title,publication_year,primary_location,authorships,cited_by_count,type,language"})
    for w in r["results"]:
        cands.append({"doi": (w.get("doi") or "").replace("https://doi.org/", ""), "titulo": w.get("title"),
                      "anio": w.get("publication_year"), "revista": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                      "citas": w.get("cited_by_count"), "autores": "; ".join(a["author"]["display_name"] for a in w["authorships"][:3])})
    time.sleep(0.5)
out["candidatos"] = cands
json.dump(out, open("busqueda_prisma.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v for k, v in out.items() if k != "candidatos"}, len(cands))
for i, c in enumerate(cands[:200], 1):
    print(i, c["anio"], "|", (c["titulo"] or "")[:110], "|", (c["revista"] or "")[:35], "|", c["doi"])
