"""Figuras del artículo a partir de resultados_vision.json (sin cifras escritas a mano)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

AQUI = Path(__file__).resolve().parent
OUT = AQUI.parent / "articulo" / "fig"
OUT.mkdir(parents=True, exist_ok=True)
R = json.loads((AQUI / "resultados_vision.json").read_text(encoding="utf-8"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
AZUL, ROJO, GRIS, VERDE = "#1F4E79", "#B03A2E", "#6B7280", "#2E7D32"


def caja(ax, x, y, w, h, texto, fc="#EAF1F8", ec=AZUL, fs=6.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs)


def flecha(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.0))


def arquitectura() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.text(0.1, 6.25, "Percepción", fontsize=8, weight="bold", color=AZUL)
    fila1 = [("Cámara\n(fotograma)", 0.1, 1.9), ("MediaPipe Hands\n21 puntos × 2 manos", 2.2, 2.2),
             ("Descriptor\ninvariante\n(120 comp.)", 4.6, 1.9), ("Clasificador\n1-NN + confianza\ny margen", 6.8, 2.0),
             ("Estabilizador\n(refractario,\nsuelta)", 9.0, 2.0)]
    for t, x, w in fila1:
        caja(ax, x, 4.75, w, 1.25, t)
    for a, b in ((2.0, 2.2), (4.4, 4.6), (6.5, 6.8), (8.8, 9.0)):
        flecha(ax, a, 5.37, b, 5.37)
    caja(ax, 9.0, 3.2, 2.0, 1.0, "Nota confirmada\n+ sonido sintetizado", fc="#E8F5E9", ec=VERDE)
    flecha(ax, 10.0, 4.75, 10.0, 4.2)
    ax.text(0.1, 3.5, "Aprendizaje y decisión", fontsize=8, weight="bold", color=AZUL)
    fila2 = [("Dominio $M_s$\n(precisión, consistencia,\nvelocidad, retención)", 0.1, 2.9),
             ("Repaso espaciado\n(variante de SM-2)", 3.2, 2.2),
             ("Predictor logístico\n($p$ de acierto)", 5.6, 2.0)]
    for t, x, w in fila2:
        caja(ax, x, 1.55, w, 1.3, t)
    flecha(ax, 9.0, 3.7, 3.0, 2.85)
    flecha(ax, 3.0, 2.2, 3.2, 2.2); flecha(ax, 5.4, 2.2, 5.6, 2.2)
    caja(ax, 3.2, 0.1, 4.6, 0.95, "Optimizador de sesión (MILP con CBC;\nrespaldo: enumeración exacta)", fc="#FFF4E0", ec="#B7791F")
    flecha(ax, 4.2, 1.55, 4.9, 1.05); flecha(ax, 6.6, 1.55, 6.2, 1.05)
    caja(ax, 8.2, 0.1, 3.7, 0.95, "Actividades: ejercicio guiado,\nmodo libre y Canciones (RhythmRunner)", fc="#F3E8FF", ec="#6B21A8")
    flecha(ax, 7.8, 0.58, 8.2, 0.58)
    fig.savefig(OUT / "arquitectura.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def barras_aciertos() -> None:
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    xs = range(len(R["aciertos"]))
    nuevo = [a["nuevo"]["pct"] for a in R["aciertos"]]
    lo = [a["nuevo"]["pct"] - a["nuevo"]["ic95_lo"] for a in R["aciertos"]]
    hi = [a["nuevo"]["ic95_hi"] - a["nuevo"]["pct"] for a in R["aciertos"]]
    ax.bar([x - 0.2 for x in xs], nuevo, 0.4, yerr=[lo, hi], capsize=2, color=AZUL, label="Descriptor propuesto")
    ax.bar([x + 0.2 for x in xs], [a["v1"]["pct"] for a in R["aciertos"]], 0.4, color="#9CA3AF", label="Método v1")
    ax.set_xticks(list(xs)); ax.set_xticklabels([f"{a['ruido']:.2f}" for a in R["aciertos"]])
    ax.set_xlabel("Ruido σ (fracción del tamaño de la mano)"); ax.set_ylabel("Señas reconocidas (%)")
    ax.set_ylim(70, 101); ax.legend(fontsize=6.5, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / "aciertos.png", dpi=300); plt.close(fig)


def barras_fp() -> None:
    fp = R["falsos_positivos"]
    etiquetas = ["Global", "Transiciones", "Manos cruzadas"]
    n = [fp["global_nuevo"], fp["por_tipo"]["transicion"]["nuevo"], fp["por_tipo"]["manos_cruzadas"]["nuevo"]]
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    pct = [d["pct"] for d in n]
    err = [[d["pct"] - d["ic95_lo"] for d in n], [d["ic95_hi"] - d["pct"] for d in n]]
    ax.bar(etiquetas, pct, yerr=err, capsize=3, color=[AZUL, ROJO, VERDE])
    for i, d in enumerate(n):
        ax.text(i, d["ic95_hi"] + 0.6, f"{d['pct']:.1f} %\n({d['k']}/{d['n']})", ha="center", fontsize=6.5)
    ax.set_ylabel("Notas disparadas por error (%)"); ax.set_ylim(0, 24)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / "falsos_positivos.png", dpi=300); plt.close(fig)


if __name__ == "__main__":
    arquitectura(); barras_aciertos(); barras_fp()
    shutil.copy(AQUI / "matriz_similitud.png", OUT / "matriz_similitud.png")
    print("ok", sorted(p.name for p in OUT.iterdir()))
