# -*- coding: utf-8 -*-
"""Bibliometria descriptiva del CORPUS recolectado (189 PDF unicos de por_clasificar).

IMPORTANTE: esto describe la coleccion de textos completos descargados a mano
(muestra de conveniencia procedente de 2 ecuaciones Scopus + refs de metodo), NO el
conjunto completo de resultados de la busqueda. Para la bibliometria formal
(co-citacion, acoplamiento, mapas VOSviewer) hace falta el export CSV/BibTeX de Scopus
en 04_Datos/bibliometria/raw/.

Uso:  .venv/Scripts/python.exe 04_Datos/bibliometria/analisis_corpus.py
"""
import csv, os, re, collections, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip()
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(BASE, "..", ".."))
MATRIZ = os.path.join(PROJ, "02_Base_de_investigacion", "Matriz_bibliografica", "matriz_bibliografica.csv")
OUT = os.path.join(BASE, "resultados")
os.makedirs(OUT, exist_ok=True)

rows = list(csv.DictReader(open(MATRIZ, encoding="utf-8-sig")))
N = len(rows)

C1 = "#2f5d8a"; C2 = "#c05d3a"

def barplot(counter, title, fname, top=None, horizontal=True):
    items = counter.most_common(top) if top else sorted(counter.items())
    labels = [str(k) for k, _ in items]
    vals = [v for _, v in items]
    fig, ax = plt.subplots(figsize=(8, max(2.5, 0.42*len(labels)+1)))
    if horizontal:
        labels = labels[::-1]; vals = vals[::-1]
        ax.barh(labels, vals, color=C1)
        for i, v in enumerate(vals): ax.text(v+max(vals)*0.01, i, str(v), va="center", fontsize=9)
    else:
        ax.bar(labels, vals, color=C1)
        for i, v in enumerate(vals): ax.text(i, v+max(vals)*0.01, str(v), ha="center", fontsize=9)
    ax.set_title(title, fontsize=12, weight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)

def dump_csv(counter, fname, col="valor"):
    with open(os.path.join(OUT, fname), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow([col, "n", "%"])
        for k, v in counter.most_common():
            w.writerow([k, v, round(100*v/N, 1)])

# --- 1. produccion por anio ---
anio = collections.Counter(r["anio"] for r in rows)
barplot(anio, f"Produccion por anio (n={N})", "01_produccion_anio.png", horizontal=False)
dump_csv(anio, "01_produccion_anio.csv", "anio")

# --- 2. tipo de documento ---
tipo = collections.Counter(norm(r["tipo_desc"]) for r in rows)
barplot(tipo, "Tipo de documento", "02_tipo_documento.png")
dump_csv(tipo, "02_tipo_documento.csv", "tipo")

# --- 3. relacion con el proyecto ---
rel = collections.Counter(norm(r["relacion_desc"]) for r in rows)
barplot(rel, "Relacion con el proyecto (cribado)", "03_relacion_proyecto.png")
dump_csv(rel, "03_relacion_proyecto.csv", "relacion")

# --- 4. pais del primer autor ---
pais = collections.Counter(norm(r["pais"]) for r in rows)
barplot(pais, "Pais de afiliacion del primer autor", "04_pais.png", top=15)
dump_csv(pais, "04_pais.csv", "pais")

# --- 5. tecnologia: categoria controlada ---
CATS = [
 ("Aprendizaje por refuerzo (RL/DRL)", r"refuerzo|reinforcement|\bdrl\b|deep rl|\bppo\b|\bdqn\b|actor-critic|\bmdp\b"),
 ("Vision por computador / pose / gesto", r"vision por computador|pose|esqueleto|mediapipe|gesto|gestual|origami|resnet|icm_pixinfo|captura de movimiento|realsense|handskeleton"),
 ("IA generativa / LLM", r"generativa|\bllm\b|chatgpt|midjourney|dall-e|gan|leak-gan|trans-gan|seq2seq|agente"),
 ("Deep learning (CNN/RNN/Transformer)", r"deep learning|\bcnn\b|\brnn\b|transformer|conformer|bilstm|lstm|dcnn|red neuronal|spikes|stdp|u-net|atencion"),
 ("Multimodal / afectivo", r"multimodal|affective|emocion|sentiment|emosic|nerf|radiancia"),
 ("Realidad virtual / aumentada / XR", r"realidad virtual|realidad aumentada|\brv\b|\bra\b|\bxr\b|realidad extendida|metaverso"),
 ("Wearables / sensores", r"wearable|sensor|eeg|fnirs|nanogenerador|seguimiento ocular|biomecanic|gemelo digital"),
 ("Audio / MIR / procesamiento de senal", r"audio|espectral|mfcc|amdf|\bdtw\b|separacion de fuentes|omr|transcripcion|mmdensenet|yamnet|yoho"),
 ("Metodo bibliometrico", r"bibliometric|vosviewer|biblioshiny|scientopy|co-word|co-citac|minia de texto|mineria de texto|\br\b\b"),
 ("Sistemas de recomendacion / rutas / ITS", r"recomendac|colaborativ|ncf|colonia de hormigas|tutoria inteligente|earmaster|ruta|path|diagnostico cognitivo|big data|analitica"),
 ("Gamificacion / juegos serios", r"gamificac|exergame|videojuego|juego serio"),
 ("Apps moviles / plataformas / TIC", r"apps? movil|plataforma|wechat|tic\b|tecnologia educativa|tecnologia digital|tecnologia musical|herramientas digitales|singtrue|plectrus|audacity|lms|tiktok|redes sociales|coil|software libre|marco tpack|competencias digitales|transformacion digital|aula invertida|microaprendizaje"),
 ("Otro / sin tecnologia", r".*"),
]
def tech_cat(s):
    s = norm(s).lower()
    for name, pat in CATS:
        if re.search(pat, s): return name
    return "Otro / sin tecnologia"
techc = collections.Counter(tech_cat(r["tecnologia"]) for r in rows)
barplot(techc, "Categoria tecnologica dominante", "05_tecnologia.png")
dump_csv(techc, "05_tecnologia.csv", "categoria_tecnologica")

# --- 6. dominio: categoria controlada ---
DCATS = [
 ("Educacion musical infantil / preescolar", r"infantil|preescolar|primera infancia|coral infantil|nin"),
 ("Piano / teclado", r"piano|teclado|sight-reading|lectura a primera vista|digitacion"),
 ("Canto / educacion vocal / coral", r"vocal|canto|coral|solfeo|conduct|conductor|conducc"),
 ("Instrumento de cuerda / arco", r"viola|violin|guitarra|bajo|guzheng|cuerda|arco"),
 ("Musica tradicional / patrimonio / etnomusicologia", r"tradicional|folcloric|folk|etnomusicolog|patrimonio|minor|silk road|ruta de la seda|cultural|turismo"),
 ("Educacion musical (general / superior / secundaria)", r"educacion musical|musica majors|teoria musical|curriculo|instrumental|practica musical|musicalidad|acompanamiento"),
 ("Generacion / transcripcion / MIR de musica", r"transcripcion|generacion|separacion de fuentes|score|partitura|composicion|coreografia|danza|interfaz musical|omr"),
 ("Musica y bienestar / cognicion / salud", r"ansiedad|tdah|bienestar|cognitiv|salud|ejercicio|estetica|percepcion|emocional"),
 ("Educacion general / superior (no musical)", r"educacion general|educacion superior|stem|ciencias|ingenieria|matematic|idiomas|religiosa|liderazgo|emprendimiento|ciudadania|programacion|artistica|museistica|docente|competencia intercultural|lms|internacionalizacion|social|neurociencia|especialidad|breakdance|consultoria|medicina|salud en adultos|construccion"),
 ("Otro", r".*"),
]
def dom_cat(s):
    s = norm(s).lower()
    for name, pat in DCATS:
        if re.search(pat, s): return name
    return "Otro"
domc = collections.Counter(dom_cat(r["dominio"]) for r in rows)
barplot(domc, "Dominio / area (categoria)", "06_dominio.png")
dump_csv(domc, "06_dominio.csv", "categoria_dominio")

# matriz enriquecida con categorias
with open(os.path.join(OUT, "matriz_enriquecida.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id","anio","autor_principal","pais","titulo","tipo","relacion","categoria_tecnologica","categoria_dominio","tecnologia","dominio","doi"])
    for r in rows:
        w.writerow([r["id"],r["anio"],r["autor_principal"],r["pais"],r["titulo"],r["tipo"],r["relacion"],
                    tech_cat(r["tecnologia"]),dom_cat(r["dominio"]),r["tecnologia"],r["dominio"],r["doi"]])

# --- 7. autores recurrentes ---
aut = collections.Counter(norm(r["autor_principal"]) for r in rows)
rec = collections.Counter({k: v for k, v in aut.items() if v > 1})
if rec:
    barplot(rec, "Primeros autores con >1 documento", "07_autores_recurrentes.png")
dump_csv(aut, "07_autores.csv", "autor_principal")

# --- 8. co-ocurrencia de palabras clave (author keywords) ---
STOP = set("a an the of and or in on for to with using based study review analysis systematic literature "
           "research education learning technology approach model system its this new via el la los las de "
           "una un y en para del con".split())
kwc = collections.Counter()
for r in rows:
    kws = re.split(r"[;,]", norm(r["keywords"]).lower())
    for k in kws:
        k = re.sub(r"[^a-z0-9\- ]", "", k).strip()
        if len(k) < 3 or k in STOP: continue
        kwc[k] += 1
dump_csv(kwc, "08_keywords.csv", "keyword")
barplot(collections.Counter({k: v for k, v in kwc.items() if v >= 3}),
        "Palabras clave de autor (>=3 apariciones)", "08_keywords.png", top=25)

# --- 9. terminos frecuentes en titulos ---
titterm = collections.Counter()
for r in rows:
    for w in re.findall(r"[a-zA-Z]{4,}", norm(r["titulo"]).lower()):
        if w in STOP: continue
        titterm[w] += 1
dump_csv(titterm, "09_terminos_titulo.csv", "termino")

# --- 10. cruce anio x relacion ---
cruce = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    cruce[r["anio"]][r["relacion"][0]] += 1
with open(os.path.join(OUT, "10_anio_x_relacion.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["anio", "A", "B", "C", "D", "total"])
    for y in sorted(cruce):
        c = cruce[y]; w.writerow([y, c["A"], c["B"], c["C"], c["D"], sum(c.values())])

# stacked bar anio x relacion
years = sorted(cruce)
tiers = ["A", "B", "C", "D"]
colors = ["#1f7a4d", "#2f5d8a", "#c9a227", "#b0b0b0"]
bottoms = [0]*len(years)
fig, ax = plt.subplots(figsize=(8, 4))
for ti, t in enumerate(tiers):
    vals = [cruce[y][t] for y in years]
    ax.bar(years, vals, bottom=bottoms, label=f"Tier {t}", color=colors[ti])
    bottoms = [b+v for b, v in zip(bottoms, vals)]
ax.set_title("Produccion por anio y relacion con el proyecto", weight="bold")
ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "10_anio_x_relacion.png"), dpi=130); plt.close(fig)

print(f"OK. {N} documentos analizados. Resultados en {OUT}")
print("Anios:", dict(sorted(anio.items())))
print("Relacion:", dict(rel))
print("Top paises:", pais.most_common(8))
print("Categorias tecnologicas:", techc.most_common())
print("Categorias dominio:", domc.most_common())
