"""Consulta Crossref por cada DOI candidato y guarda los metadatos reales en refs_crossref.json / verificacion_referencias.csv."""
import csv, json, time, urllib.request, urllib.error, datetime
DOIS = """10.3362/1756-3488.20-00014 10.1021/acs.est.2c03133 10.1038/s41545-020-00091-1 10.1021/acs.est.1c01308
10.1021/acs.estlett.2c00781 10.1061/(asce)ee.1943-7870.0001883 10.1371/journal.pwat.0000295 10.1061/(asce)ee.1943-7870.0002063
10.1021/acsestwater.3c00425 10.2166/washdev.2024.407 10.1371/journal.pwat.0000255 10.1371/journal.pwat.0000440
10.1371/journal.pwat.0000575 10.1146/annurev-environ-031411-091819 10.4269/ajtmh.2007.76.354
10.1016/S0140-6736(23)00458-0 10.1002/14651858.CD004794.pub3 10.1016/S0043-1354(99)00097-4 10.1080/01621459.1927.10502953
10.1016/S2214-109X(19)30315-8 10.1016/j.watres.2020.115854 10.1136/bmj.n71""".split()
def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "clorificador-verif/1.0 (mailto:roxana.munoz@upb.edu.co)"})
    with urllib.request.urlopen(r, timeout=40) as f: return json.load(f)
rows = []
for d in DOIS:
    try:
        m = get("https://api.crossref.org/works/" + urllib.request.quote(d, safe="/()"))["message"]
        au = "; ".join(f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", []))
        row = dict(doi=d, fuente="Crossref", titulo=m["title"][0], anio=(m.get("issued", {}).get("date-parts") or [[""]])[0][0],
                   revista=(m.get("container-title") or [""])[0], autores=au, volumen=m.get("volume", ""), numero=m.get("issue", ""),
                   paginas=m.get("page", m.get("article-number", "")), estado="VERIFICADO")
    except Exception as e:
        row = dict(doi=d, fuente="", titulo="", anio="", revista="", autores="", volumen="", numero="", paginas="", estado=f"NO VERIFICADO: {e}")
    row["fecha_consulta"] = datetime.date.today().isoformat(); row["url"] = "https://doi.org/" + d
    rows.append(row); time.sleep(0.4)
json.dump(rows, open("refs_crossref.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
with open("verificacion_referencias.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r["estado"][:14], r["doi"], "|", r["anio"], "|", r["titulo"][:80], "|", r["revista"][:28], "|", r["autores"][:50], "|", r["volumen"], r["numero"], r["paginas"])
