"""Dibuja el flujo PRISMA 2020 (cuatro fases) con las cifras de prisma_cifras.json. No inventa valores."""
import json
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
A = Path(__file__).resolve().parent
c = json.loads((A / "prisma_cifras.json").read_text(encoding="utf-8"))
v = lambda k: "PENDIENTE" if c.get(k) is None else f"n = {c[k]:,}".replace(",", ".")
fases = [("Identificación", f"Registros identificados\n{v('identificados')}", f"Duplicados eliminados\n{v('duplicados_eliminados')}"),
         ("Cribado", f"Registros cribados\n{v('cribados')}", f"Excluidos\n{v('excluidos_cribado')}"),
         ("Elegibilidad", f"Texto completo evaluado\n{v('texto_completo_evaluados')}", f"Excluidos con motivo\n{v('excluidos_texto_completo')}"),
         ("Inclusión", f"Estudios incluidos\n{v('incluidos')}", "")]
fig, ax = plt.subplots(figsize=(6.4, 6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
for i, (fase, caja, lado) in enumerate(fases):
    y = 8.3 - i * 2.6
    ax.text(0.1, y + 0.45, fase, rotation=90, va="center", fontsize=8, weight="bold")
    ax.add_patch(FancyBboxPatch((1, y), 4.4, 0.95, boxstyle="round,pad=0.02", fc="#EAF1F8", ec="#1F4E79")); ax.text(3.2, y + .47, caja, ha="center", va="center", fontsize=8)
    if lado:
        ax.add_patch(FancyBboxPatch((6.2, y), 3.4, 0.95, boxstyle="round,pad=0.02", fc="#FDECEA", ec="#B03A2E")); ax.text(7.9, y + .47, lado, ha="center", va="center", fontsize=8)
        ax.annotate("", xy=(6.2, y + .47), xytext=(5.4, y + .47), arrowprops=dict(arrowstyle="-|>"))
    if i < 3: ax.annotate("", xy=(3.2, y - 1.65), xytext=(3.2, y), arrowprops=dict(arrowstyle="-|>"))
fig.savefig(A.parent / "articulo" / "fig" / "prisma.png", dpi=300, bbox_inches="tight"); print("prisma.png generado (valores nulos = PENDIENTE)")
