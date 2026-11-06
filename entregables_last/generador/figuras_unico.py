"""Figuras del artículo único: flujo PRISMA con las cifras reales del corpus del proyecto y composición de capturas de la aplicación."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image

FIG = Path(__file__).resolve().parent.parent / "articulo" / "fig"
CAP = Path(__file__).resolve().parents[2] / "09_Imagenes" / "capturas_app"
plt.rcParams.update({"font.family": "DejaVu Sans"})

# ---------------- PRISMA (cifras de 04_Datos/bibliometria/resultados/informe_bibliometrico_corpus.md)
fig, ax = plt.subplots(figsize=(6.6, 6.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-0.2, 10.8)
AZ, RJ, GR = ("#EAF1F8", "#1F4E79"), ("#FDECEA", "#B03A2E"), ("#F3F3F3", "#555555")


def caja(x, y, w, h, t, c, fs=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=c[0], ec=c[1], lw=1))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)


def flecha(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=.9))


for t, y in (("IDENTIFICACIÓN", 8.9), ("CRIBADO", 6.2), ("ELEGIBILIDAD", 3.5), ("INCLUSIÓN", 0.6)):
    ax.text(0.15, y + .5, t, rotation=90, va="center", fontsize=7, weight="bold")
caja(1, 8.5, 5.0, 1.9, "Archivos obtenidos con las dos ecuaciones de\nScopus y con artículos de método\nn = 226 (218 PDF y 4 ZIP con 8 PDF)", AZ)
caja(6.4, 8.5, 3.4, 1.9, "Conteo de resultados de\ncada ecuación en Scopus:\nno se registró", GR, 7.2)
flecha(3.5, 8.5, 3.5, 7.6)
caja(1, 6.0, 5.0, 1.5, "Documentos únicos clasificados\nn = 189", AZ)
caja(6.4, 6.4, 3.4, 1.2, "Duplicados eliminados\n(copias idénticas)\nn = 37", RJ, 7.4)
flecha(6.0, 7.0, 6.4, 7.0)
flecha(3.5, 6.0, 3.5, 5.1)
caja(1, 3.5, 5.0, 1.5, "Evaluados por su relación con el proyecto\n(categorías A, B y C)  n = 148", AZ)
caja(6.4, 5.0, 3.4, 1.2, "Marginales (D),\nexcluidos\nn = 41", RJ, 7.4)
flecha(6.0, 5.6, 6.4, 5.6)
flecha(3.5, 3.5, 3.5, 2.6)
caja(6.4, 3.0, 3.4, 1.7, "Método o contexto (C),\nsin uso directo en la\ncomparación  n = 61", RJ, 7.2)
flecha(6.0, 4.0, 6.4, 3.9)
caja(1, 0.6, 5.0, 1.9, "Incluidos en la síntesis cualitativa\nn = 87\nNúcleo (A): 22  ·  Relevantes (B): 65", ("#E8F5E9", "#2E7D32"))
caja(6.4, 0.6, 3.4, 1.9, "22 documentos del núcleo\ncon lectura profunda\ny ficha de resumen", GR, 7.2)
flecha(6.0, 1.55, 6.4, 1.55)
fig.savefig(FIG / "prisma_hsk.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------------- capturas de la aplicación (2 x 2)
nombres = [("06_calibracion.png", "(a) Calibración"), ("11_ejercicio.png", "(b) Ejercicio guiado"), ("13_canciones.png", "(c) Canciones"), ("07_progreso.png", "(d) Progreso del niño")]
W, H = 720, 450
lienzo = Image.new("RGB", (W * 2 + 30, (H + 38) * 2), "white")
fig2, axs = plt.subplots(2, 2, figsize=(7.2, 4.9))
for a, (f, t) in zip(axs.ravel(), nombres):
    a.imshow(Image.open(CAP / f)); a.set_title(t, fontsize=8, pad=3); a.axis("off")
fig2.tight_layout(pad=0.4); fig2.savefig(FIG / "capturas_app.png", dpi=220); plt.close(fig2)
print("figuras ok")
