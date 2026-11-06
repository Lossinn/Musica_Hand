"""Consulta Crossref (y DataCite para arXiv) y guarda metadatos reales de cada DOI candidato."""
import csv, json, sys, time, urllib.request, datetime
DOIS = """10.1007/s10462-023-10637-7 10.1007/s40745-026-00689-1 10.7717/peerj-cs.3464 10.1007/s44163-026-01115-4
10.1038/s41598-026-53749-0 10.1007/s44163-026-01858-0 10.5216/mh.v26.85176 10.1007/s11042-026-21667-y
10.1007/s10791-026-10022-2 10.1007/s44163-026-00832-0 10.1016/j.eswa.2026.132088 10.31681/jetol.1243501
10.30935/cedtech/13622 10.6018/red.602301 10.17811/rifie.20620 10.1136/bmj.n71
10.1080/01621459.1927.10502953 10.1038/s41467-019-12552-4 10.1037/0033-2909.132.3.354 10.1007/BF01099821
10.48550/arXiv.2006.10214 10.55782/ane-1994-1003""".split()
def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "HandSingKids-verif/1.0 (mailto:alejandro.pemberty@upb.edu.co)"})
    with urllib.request.urlopen(r, timeout=30) as f: return json.load(f)
rows = []
for d in DOIS:
    try:
        if "arXiv" in d:
            m = get("https://api.datacite.org/dois/" + d.lower())["data"]["attributes"]
            row = dict(doi=d, fuente="DataCite", titulo=m["titles"][0]["title"], anio=m["publicationYear"],
                       revista="arXiv", autores="; ".join(a["name"] for a in m["creators"]), volumen="", numero="", paginas="")
        else:
            m = get("https://api.crossref.org/works/" + d)["message"]
            au = "; ".join(f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", []))
            row = dict(doi=d, fuente="Crossref", titulo=m["title"][0], anio=(m.get("issued", {}).get("date-parts") or [[""]])[0][0],
                       revista=(m.get("container-title") or [""])[0], autores=au, volumen=m.get("volume", ""),
                       numero=m.get("issue", ""), paginas=m.get("page", m.get("article-number", "")))
        row["estado"] = "VERIFICADO"
    except Exception as e:
        row = dict(doi=d, fuente="", titulo="", anio="", revista="", autores="", volumen="", numero="", paginas="", estado=f"NO VERIFICADO: {e}")
    row["fecha_consulta"] = datetime.date.today().isoformat()
    row["url"] = "https://doi.org/" + d
    rows.append(row); time.sleep(0.3)
with open("refs_crossref.json", "w", encoding="utf8") as f: json.dump(rows, f, ensure_ascii=False, indent=1)
for r in rows: print(r["estado"][:12], r["doi"], "|", r["anio"], "|", r["titulo"][:90], "|", r["revista"][:30], "|", r["autores"][:60])
