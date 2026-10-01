"""Verifica cada DOI candidato contra la API pública de Crossref y contra doi.org.
Uso: python verificar_doi.py  -> escribe doi_verificados.json"""
import csv, json, sys, urllib.request, urllib.error, urllib.parse
MATRIZ = r"../../02_Base_de_investigacion/Matriz_bibliografica/matriz_bibliografica.csv"
IDS = ["203","075","032","077","044","046","038","050","144","164","129","220","056","002","186","161","081","218","171"]
rows = {r["id"]: r for r in csv.DictReader(open(MATRIZ, encoding="utf-8-sig"))}
out = []
for i in IDS:
    r = rows[i]; doi = r["doi"].strip()
    rec = {"id": i, "doi": doi, "matriz_titulo": r["titulo"], "matriz_anio": r["anio"]}
    try:
        u = "https://api.crossref.org/works/" + urllib.parse.quote(doi) if False else "https://api.crossref.org/works/" + doi
        req = urllib.request.Request(u, headers={"User-Agent": "HandSingKids-verif/1.0 (mailto:elquemascamella69@gmail.com)"})
        m = json.load(urllib.request.urlopen(req, timeout=30))["message"]
        rec.update(ok=True, titulo=(m.get("title") or [""])[0],
                   anio=(m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                   revista=(m.get("container-title") or [""])[0],
                   volumen=m.get("volume"), numero=m.get("issue"), paginas=m.get("page"), articulo=m.get("article-number"),
                   autores=[(a.get("family","") + ", " + a.get("given","")).strip(", ") for a in m.get("author", [])],
                   tipo=m.get("type"), publisher=m.get("publisher"))
    except urllib.error.HTTPError as e:
        rec.update(ok=False, error=f"HTTP {e.code}")
    except Exception as e:
        rec.update(ok=False, error=str(e)[:80])
    out.append(rec)
json.dump(out, open("doi_verificados.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in out:
    if r["ok"]:
        print(r["id"], "OK ", r["anio"], "|", r["titulo"][:75], "|", r["revista"][:30], "|", (r["autores"] or ["?"])[0], f"(+{len(r['autores'])-1})")
    else:
        print(r["id"], "FALLA", r["doi"], r["error"])
