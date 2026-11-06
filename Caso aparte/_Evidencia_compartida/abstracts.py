import json, urllib.parse, urllib.request, time
d = json.load(open("busqueda_prisma.json", encoding="utf-8"))
idx = [5,8,10,11,12,16,18,20,21,28,29,30,31,34,35,36,38,2,26]
out = {}
for i in idx:
    c = d["candidatos"][i-1]
    url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(c["doi"], safe="/") + "?select=title,abstract_inverted_index,publication_year"
    for k in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "clorificador/1.0 (mailto:roxana.munoz@upb.edu.co)"}), timeout=60)); break
        except Exception as e:
            time.sleep(10*(k+1)); r = None
    ab = ""
    if r and r.get("abstract_inverted_index"):
        pos = {}
        for w, ps in r["abstract_inverted_index"].items():
            for p in ps: pos[p] = w
        ab = " ".join(pos[p] for p in sorted(pos))
    out[c["doi"]] = {"i": i, "titulo": c["titulo"], "anio": c["anio"], "abstract": ab}
    time.sleep(1.2)
json.dump(out, open("abstracts_seleccion.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in out.items(): print("\n##", v["i"], k, v["anio"], v["titulo"], "\n", v["abstract"][:1300])
