# -*- coding: utf-8 -*-
"""Enriquece la matriz con metadatos de Crossref + OpenAlex a partir del DOI.

Genera en 04_Datos/bibliometria/processed/:
  - metadatos_enriquecidos.csv   (una fila por documento, campos bibliometricos)
  - corpus.bib                    (BibTeX para gestor de referencias)
  - referenced_works.json         (obras citadas por cada doc, OpenAlex -> co-citacion/acoplamiento)

APIs publicas, sin clave. Uso:  .venv/Scripts/python.exe 04_Datos/bibliometria/enriquecer_metadatos.py
"""
import csv, os, re, json, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(BASE, "..", ".."))
MATRIZ = os.path.join(PROJ, "02_Base_de_investigacion", "Matriz_bibliografica", "matriz_bibliografica.csv")
OUT = os.path.join(BASE, "processed")
os.makedirs(OUT, exist_ok=True)
MAIL = "elquemascamella69@gmail.com"
UA = f"HandSingKids-biblio/1.0 (mailto:{MAIL})"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def crossref(doi):
    try:
        return get("https://api.crossref.org/works/" + urllib.parse.quote(doi)).get("message", {})
    except Exception as e:
        return {"_error": str(e)}

def openalex_by_doi(doi):
    try:
        return get(f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi)}?mailto={MAIL}")
    except Exception:
        return {}

def openalex_by_title(title):
    try:
        q = urllib.parse.quote(title[:200])
        d = get(f"https://api.openalex.org/works?filter=title.search:{q}&per-page=1&mailto={MAIL}")
        res = d.get("results", [])
        return res[0] if res else {}
    except Exception:
        return {}

def cr_authors(m):
    out = []
    for a in m.get("author", []) or []:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        aff = "; ".join(x.get("name", "") for x in a.get("affiliation", []) or [])
        out.append(nm + (f" ({aff})" if aff else ""))
    return " | ".join(out)

def oa_countries(w):
    cc = set()
    for a in w.get("authorships", []) or []:
        for c in a.get("countries", []) or []:
            cc.add(c)
        for inst in a.get("institutions", []) or []:
            if inst.get("country_code"):
                cc.add(inst["country_code"])
    return ",".join(sorted(cc))

def oa_institutions(w):
    ins = []
    for a in w.get("authorships", []) or []:
        for inst in a.get("institutions", []) or []:
            if inst.get("display_name"):
                ins.append(inst["display_name"])
    seen = []
    for i in ins:
        if i not in seen:
            seen.append(i)
    return "; ".join(seen[:8])

def oa_concepts(w):
    return "; ".join(f"{c['display_name']}({c['score']:.2f})" for c in (w.get("concepts") or [])[:6])

def bibtex(row, m):
    key = re.sub(r"[^A-Za-z0-9]", "", (row["autor_principal"] or "anon")) + str(row["anio"])
    t = (m.get("title") or [row["titulo"]])
    t = t[0] if isinstance(t, list) else t
    j = m.get("container-title") or []
    j = j[0] if j else ""
    fields = {
        "title": t, "journal": j, "year": row["anio"], "doi": row["doi"],
        "volume": m.get("volume", ""), "number": m.get("issue", ""),
        "pages": m.get("page", ""), "publisher": m.get("publisher", ""),
    }
    au = []
    for a in m.get("author", []) or []:
        fam, giv = a.get("family", ""), a.get("given", "")
        if fam:
            au.append(f"{fam}, {giv}".strip().strip(","))
    if au:
        fields["author"] = " and ".join(au)
    body = ",\n  ".join(f'{k} = {{{v}}}' for k, v in fields.items() if v)
    return f"@article{{{key},\n  {body}\n}}\n"

rows = list(csv.DictReader(open(MATRIZ, encoding="utf-8-sig")))
res_fields = ["id", "anio", "autor_principal", "relacion", "doi",
              "titulo_oficial", "autores", "n_autores", "revista", "issn", "editorial",
              "tipo_publicacion", "volumen", "numero", "paginas", "fecha_publicacion",
              "citas_crossref", "citas_openalex", "n_referencias", "acceso_abierto", "licencia",
              "paises_openalex", "instituciones_openalex", "conceptos_openalex", "financiacion",
              "openalex_id", "fuente_metadatos"]

out_rows = []
bibs = []
refmap = {}
for i, row in enumerate(rows, 1):
    doi = (row["doi"] or "").strip().rstrip(".")
    rec = {k: "" for k in res_fields}
    rec.update(id=row["id"], anio=row["anio"], autor_principal=row["autor_principal"],
               relacion=row["relacion"], doi=doi)
    m, w = {}, {}
    try:
        if doi and re.match(r"10\.\d{4,9}/", doi):
            m = crossref(doi); time.sleep(0.3)
            w = openalex_by_doi(doi); time.sleep(0.3)
            rec["fuente_metadatos"] = "crossref+openalex"
        else:
            w = openalex_by_title(row["titulo"]); time.sleep(0.3)
            rec["fuente_metadatos"] = "openalex(title)" if w else "sin_doi"
        m = m or {}
        w = w or {}
        if m and "_error" not in m:
            tt = m.get("title") or []
            rec["titulo_oficial"] = (tt[0] if tt else "")
            rec["autores"] = cr_authors(m)
            rec["n_autores"] = str(len(m.get("author", []) or []))
            jt = m.get("container-title") or []
            rec["revista"] = jt[0] if jt else ""
            rec["issn"] = ",".join(m.get("ISSN") or [])
            rec["editorial"] = m.get("publisher", "")
            rec["tipo_publicacion"] = m.get("type", "")
            rec["volumen"] = m.get("volume", "")
            rec["numero"] = m.get("issue", "")
            rec["paginas"] = m.get("page", "")
            dp = (m.get("published") or {}).get("date-parts", [[]])
            rec["fecha_publicacion"] = "-".join(str(x) for x in dp[0]) if dp and dp[0] else ""
            rec["citas_crossref"] = str(m.get("is-referenced-by-count", ""))
            rec["n_referencias"] = str(m.get("references-count", len(m.get("reference", []) or [])))
            lic = m.get("license") or []
            rec["licencia"] = lic[0].get("URL", "") if lic else ""
            rec["financiacion"] = "; ".join(f.get("name", "") for f in (m.get("funder") or []))
            bibs.append(bibtex(row, m))
        if w:
            if not rec["titulo_oficial"]:
                rec["titulo_oficial"] = w.get("title", "") or ""
            rec["citas_openalex"] = str(w.get("cited_by_count", ""))
            rec["openalex_id"] = (w.get("id", "") or "").split("/")[-1]
            rec["acceso_abierto"] = str((w.get("open_access") or {}).get("is_oa", ""))
            rec["paises_openalex"] = oa_countries(w)
            rec["instituciones_openalex"] = oa_institutions(w)
            rec["conceptos_openalex"] = oa_concepts(w)
            if not rec["revista"]:
                src = (w.get("primary_location") or {}).get("source") or {}
                rec["revista"] = src.get("display_name", "") or ""
            if not rec["n_referencias"]:
                rec["n_referencias"] = str(len(w.get("referenced_works", []) or []))
            refmap[row["id"]] = w.get("referenced_works", []) or []
    except Exception as e:
        rec["fuente_metadatos"] = f"error: {e}"
    out_rows.append(rec)
    if i % 20 == 0:
        print(f"  {i}/{len(rows)} ...")


with open(os.path.join(OUT, "metadatos_enriquecidos.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=res_fields)
    w.writeheader()
    w.writerows(out_rows)
with open(os.path.join(OUT, "corpus.bib"), "w", encoding="utf-8") as f:
    f.write("\n".join(bibs))
with open(os.path.join(OUT, "referenced_works.json"), "w", encoding="utf-8") as f:
    json.dump(refmap, f)

ok = sum(1 for r in out_rows if r["titulo_oficial"])
cit = sum(1 for r in out_rows if r["citas_openalex"] not in ("", "0"))
print(f"\nOK. {len(out_rows)} filas | con metadatos: {ok} | con >=1 cita: {cit}")
print("Archivos en", OUT)
