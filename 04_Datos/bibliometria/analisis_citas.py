# -*- coding: utf-8 -*-
"""Analisis de citas, revistas, colaboracion, co-citacion y acoplamiento del corpus.
Usa 04_Datos/bibliometria/processed/{metadatos_enriquecidos.csv, referenced_works.json}.
Ejecutar con .venv/Scripts/python.exe
"""
import csv, os, re, json, time, itertools, collections, urllib.request, urllib.parse
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(BASE, "processed")
OUT = os.path.join(BASE, "resultados")
MAIL = "elquemascamella69@gmail.com"
UA = f"HandSingKids-biblio/1.0 (mailto:{MAIL})"
C1 = "#2f5d8a"

meta = {r["id"]: r for r in csv.DictReader(open(os.path.join(PROC, "metadatos_enriquecidos.csv"), encoding="utf-8-sig"))}
rw = json.load(open(os.path.join(PROC, "referenced_works.json")))
N = len(meta)

def barh(counter, title, fname, top=20):
    items = counter.most_common(top)[::-1]
    labels = [k for k, _ in items]; vals = [v for _, v in items]
    fig, ax = plt.subplots(figsize=(8, max(2.5, 0.42*len(labels)+1)))
    ax.barh(labels, vals, color=C1)
    for i, v in enumerate(vals): ax.text(v, i, " "+str(v), va="center", fontsize=9)
    ax.set_title(title, weight="bold"); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=130); plt.close(fig)

def dump(counter, fname, col):
    with open(os.path.join(OUT, fname), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow([col, "n"])
        for k, v in counter.most_common(): w.writerow([k, v])

# ---------- 1. Revistas / fuentes ----------
jr = collections.Counter(re.sub(r"&amp;", "&", r["revista"]).strip() for r in meta.values() if r["revista"])
dump(jr, "11_revistas.csv", "revista")
barh(jr, "Revistas / fuentes del corpus (top 20)", "11_revistas.png", 20)
# Bradford (zonas de igual nº de articulos)
arts = sorted(jr.values(), reverse=True)
tot = sum(arts); zone = tot/3
z, acc, cuts = 1, 0, []
for a in arts:
    acc += a
    if acc >= zone*z and z <= 3:
        cuts.append(acc); z += 1

# ---------- 2. Citas ----------
def toi(x):
    try: return int(x)
    except: return 0
cit = [(i, toi(r["citas_openalex"]), toi(r["citas_crossref"]), r) for i, r in meta.items()]
cit.sort(key=lambda t: -t[1])
with open(os.path.join(OUT, "12_citas_top.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "anio", "autor", "relacion", "citas_openalex", "citas_crossref", "revista", "titulo"])
    for i, oc, cc, r in cit[:30]:
        w.writerow([i, r["anio"], r["autor_principal"], r["relacion"], oc, cc, r["revista"], r["titulo_oficial"]])
oc_all = [oc for _, oc, _, _ in cit]
print("Citas OpenAlex: total %d | media %.1f | mediana %d | max %d | con 0 citas %d/%d"
      % (sum(oc_all), np.mean(oc_all), np.median(oc_all), max(oc_all), oc_all.count(0), N))
# citas por tier
tiercit = collections.defaultdict(list)
for _, oc, _, r in cit: tiercit[r["relacion"][0]].append(oc)
with open(os.path.join(OUT, "12_citas_por_tier.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["tier", "n", "citas_totales", "media", "mediana"])
    for t in "ABCD":
        v = tiercit[t]
        w.writerow([t, len(v), sum(v), round(np.mean(v), 1) if v else 0, np.median(v) if v else 0])

# ---------- 3. Paises (OpenAlex) + colaboracion ----------
pais = collections.Counter()
multi = 0
for r in meta.values():
    cs = [c for c in r["paises_openalex"].split(",") if c]
    for c in cs: pais[c] += 1
    if len(set(cs)) > 1: multi += 1
dump(pais, "13_paises_openalex.csv", "pais_iso")
barh(pais, "Paises (codigos OpenAlex, recuento por documento)", "13_paises_openalex.png", 15)
print("Documentos con colaboracion internacional (>1 pais):", multi)

# ---------- 4. Co-citacion: base intelectual del corpus ----------
allrefs = collections.Counter(x for v in rw.values() for x in v)
base = [(w, n) for w, n in allrefs.items() if n >= 3]
base.sort(key=lambda t: -t[1])
# resolver titulos via OpenAlex (batch)
titles = {}
ids = [w.split("/")[-1] for w, _ in base]
for k in range(0, len(ids), 50):
    chunk = "|".join(ids[k:k+50])
    try:
        url = f"https://api.openalex.org/works?filter=openalex_id:{chunk}&per-page=50&select=id,title,publication_year,cited_by_count,primary_location&mailto={MAIL}"
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40))
        for wobj in d.get("results", []):
            src = (wobj.get("primary_location") or {}).get("source") or {}
            titles[wobj["id"].split("/")[-1]] = (wobj.get("title", ""), wobj.get("publication_year", ""),
                                                 wobj.get("cited_by_count", ""), src.get("display_name", ""))
    except Exception as e:
        print("  co-cit resolve error:", e)
    time.sleep(0.3)
with open(os.path.join(OUT, "14_cocitacion_base.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["veces_citado_en_corpus", "anio", "citas_globales", "revista", "titulo", "openalex_id"])
    for wid, n in base:
        k = wid.split("/")[-1]
        t, y, gc, src = titles.get(k, ("(sin resolver)", "", "", ""))
        w.writerow([n, y, gc, src, t, k])
print(f"Base intelectual: {len(base)} obras citadas por >=3 documentos del corpus")

# ---------- 5. Acoplamiento bibliografico (bibliographic coupling) ----------
docs = [i for i in meta if rw.get(i)]
sets = {i: set(rw[i]) for i in docs}
edges = []
for a, b in itertools.combinations(docs, 2):
    s = len(sets[a] & sets[b])
    if s >= 2:
        edges.append((a, b, s))
edges.sort(key=lambda e: -e[2])
with open(os.path.join(OUT, "15_acoplamiento_edges.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["doc_a", "titulo_a", "rel_a", "doc_b", "titulo_b", "rel_b", "refs_compartidas"])
    for a, b, s in edges:
        w.writerow([a, meta[a]["titulo_oficial"][:70], meta[a]["relacion"][0],
                    b, meta[b]["titulo_oficial"][:70], meta[b]["relacion"][0], s])
print(f"Acoplamiento: {len(edges)} pares de documentos con >=2 referencias compartidas")

# red simple (layout por resortes manual con numpy) de los nodos con al menos una arista >=2
nodes = sorted({x for e in edges for x in e[:2]})
if nodes:
    idx = {n: k for k, n in enumerate(nodes)}
    P = np.random.RandomState(1).rand(len(nodes), 2)
    A = np.zeros((len(nodes), len(nodes)))
    for a, b, s in edges:
        A[idx[a], idx[b]] = A[idx[b], idx[a]] = s
    for _ in range(300):
        disp = np.zeros_like(P)
        for i in range(len(nodes)):
            d = P[i] - P
            dist = np.linalg.norm(d, axis=1) + 1e-6
            rep = (d / dist[:, None]**2 * 0.01).sum(axis=0)
            att = -(d * (A[i][:, None]) * 0.02).sum(axis=0)
            disp[i] = rep + att
        P += np.clip(disp, -0.05, 0.05)
    colmap = {"A": "#1f7a4d", "B": "#2f5d8a", "C": "#c9a227", "D": "#b0b0b0"}
    fig, ax = plt.subplots(figsize=(9, 7))
    for a, b, s in edges:
        x = [P[idx[a], 0], P[idx[b], 0]]; y = [P[idx[a], 1], P[idx[b], 1]]
        ax.plot(x, y, "-", lw=0.4+0.5*s, color="#999", alpha=0.5, zorder=1)
    deg = A.sum(axis=1)
    for n in nodes:
        i = idx[n]
        ax.scatter(P[i, 0], P[i, 1], s=60+18*deg[i], color=colmap[meta[n]["relacion"][0]], zorder=2, edgecolors="white")
        ax.annotate(f'{n} {meta[n]["autor_principal"]}', (P[i, 0], P[i, 1]), fontsize=7, ha="center", va="bottom")
    ax.set_title("Acoplamiento bibliografico del corpus (>=2 refs compartidas)\nverde=A nucleo  azul=B  amarillo=C  gris=D", weight="bold")
    ax.axis("off")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "15_acoplamiento_red.png"), dpi=130); plt.close(fig)

print("\nOK. Nuevas tablas/figuras 11-15 en", OUT)
