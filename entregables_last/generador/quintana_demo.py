"""Instancia ilustrativa (12 actividades) para estudiar la sensibilidad del problema de selección de sesión. NO es el catálogo de la aplicación."""
import itertools, json, math
import numpy as np
S = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI", "DO4"]
mu0 = dict(zip(S, [0.90, 0.80, 0.55, 0.35, 0.30, 0.20, 0.10, 0.05]))
urg = {"DO": 0.6, "RE": 0.5}
A = [  # nombre, duración (min), dificultad, habilidades, tipo
    ("Imitar DO–RE", 4, .25, ["DO", "RE"], "guiada"), ("Eco de notas", 5, .35, ["RE", "MI"], "guiada"),
    ("Escalera ascendente", 6, .45, ["DO", "RE", "MI", "FA"], "guiada"), ("La nota escondida", 5, .40, ["MI", "FA"], "lúdica"),
    ("Canción corta A", 7, .55, ["MI", "FA", "SOL"], "lúdica"), ("Mini-reto FA–SOL", 4, .50, ["FA", "SOL"], "guiada"),
    ("Pares de notas", 5, .60, ["SOL", "LA"], "guiada"), ("Canción corta B", 8, .70, ["SOL", "LA", "SI"], "lúdica"),
    ("Memoria de señas", 5, .45, ["DO", "MI", "SOL"], "lúdica"), ("Subir hasta SI", 6, .80, ["LA", "SI"], "guiada"),
    ("Cierre en DO agudo", 4, .65, ["SI", "DO4"], "guiada"), ("Repaso DO–RE–MI", 5, .30, ["DO", "RE", "MI"], "guiada")]
def valores(mu, w):
    out = []
    for nom, d, dif, sk, tipo in A:
        mb = np.mean([mu[s] for s in sk]); p = 1 / (1 + math.exp(-6 * (mb - dif))); eta = math.exp(-(p - .75) ** 2 / (2 * .18 ** 2))
        g = eta * sum(1 - mu[s] for s in sk) / math.sqrt(len(sk)); r = max([urg.get(s, 0.1) for s in sk])
        m = 0.6 if tipo == "lúdica" else 0.3; f = d / 30 * (0.5 + dif)
        out.append(dict(g=g, r=r, m=m, f=f, d=d, dif=dif, sk=sk, lud=tipo == "lúdica", venc=any(s in urg for s in sk)))
    return out
def resolver(mu=mu0, w=(1.0, 0.7, 0.35, 0.55), K=4, T=30, ludica=True, dmax=0.72):
    v = valores(mu, w); mejor = None; fact = 0
    for c in itertools.combinations(range(len(A)), K):
        if sum(v[i]["d"] for i in c) > T: continue
        if ludica and not any(v[i]["lud"] for i in c): continue
        if sum(v[i]["dif"] for i in c) > dmax * K: continue
        if not any(v[i]["venc"] for i in c): continue
        if any(sum(s in v[i]["sk"] for i in c) > 2 for s in S): continue
        fact += 1
        z = sum(w[0] * v[i]["g"] + w[1] * v[i]["r"] + w[2] * v[i]["m"] - w[3] * v[i]["f"] for i in c)
        if mejor is None or z > mejor[0] + 1e-12: mejor = (z, c)
    return mejor, fact
esc = {"Base": {}, "Peso del repaso ×2": dict(w=(1.0, 1.4, 0.35, 0.55)), "Peso de la fatiga ×2": dict(w=(1.0, 0.7, 0.35, 1.1)),
       "Peso de la ganancia ×2": dict(w=(2.0, 0.7, 0.35, 0.55)), "Tiempo máximo 16 min": dict(T=16), "Tiempo máximo 14 min": dict(T=14), "Dificultad media máxima 0,50": dict(dmax=0.50),
       "Sesión de K = 3": dict(K=3), "Sesión de K = 5": dict(K=5), "Sin exigir actividad lúdica": dict(ludica=False),
       "Niño más avanzado (+0,2)": dict(mu={s: min(1, x + .2) for s, x in mu0.items()})}
res = {}
base = None
for n, kw in esc.items():
    m, f = resolver(**kw)
    if m is None: res[n] = dict(factible=0); continue
    z, c = m; res[n] = dict(obj=z, sesion=[i + 1 for i in c], nombres=[A[i][0] for i in c], minutos=sum(A[i][1] for i in c), factibles=f)
    if n == "Base": base = set(c)
for n, r in res.items():
    if "sesion" in r: r["cambia"] = sorted(set(r["sesion"]) ^ {i + 1 for i in base})
json.dump(dict(catalogo=[dict(i=i + 1, nombre=a[0], d=a[1], dif=a[2], hab=a[3], tipo=a[4]) for i, a in enumerate(A)], mu=mu0, escenarios=res), open("quintana_demo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for n, r in res.items(): print(n, r.get("obj") and round(r["obj"], 4), r.get("sesion"), r.get("minutos"), r.get("factibles"))
