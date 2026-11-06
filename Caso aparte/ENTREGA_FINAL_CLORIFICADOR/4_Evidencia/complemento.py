"""Cálculos y figuras complementarios (economía, consumo, umbral 0,3 mg/L, PRISMA, esquema). Todo sale de resultados_estudio.json,
de los documentos del proyecto y de busqueda_prisma.json. Uso: python -X utf8 complemento.py"""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
A = Path(__file__).resolve().parent; FIG = A / "fig"
R = json.loads((A / "resultados_estudio.json").read_text(encoding="utf-8"))
NB = A.parent / "8.clorificadordeAgua (2)" / "8.clorificadordeAgua" / "Documentos Digital de Desarrollo" / "output" / "simulacion_montecarlo_clorificador.csv"
rows = list(csv.DictReader(open(NB, encoding="utf-8")))
c = np.array([float(r["cloro_residual_mgL"]) for r in rows])
out = {}
out["escenarios_ge_0_3"] = int((c >= 0.3).sum()); out["escenarios_ge_0_2"] = int((c >= 0.2).sum()); out["escenarios_gt_0"] = int((c > 0).sum())
out["percentiles"] = {p: float(np.percentile(c, p)) for p in (50, 90, 95, 99)}
# --- economía (documentos del proyecto: BOM 159.991; beneficio supuesto 25.000 COP/hogar-mes; opex ~15.000 COP/mes; tasa 0,8 %)
INV, BEN, OPEX, I = 159991, 25000, 15000, 0.008
vpn_ben = sum(BEN / (1 + I) ** t for t in range(1, 13)) - INV
vpn_net = sum((BEN - OPEX) / (1 + I) ** t for t in range(1, 13)) - INV
out["vpn_12m_solo_beneficio"] = round(vpn_ben); out["vpn_12m_neto_de_opex_1hogar"] = round(vpn_net)
out["payback_meses_1hogar_bruto"] = INV / BEN; out["payback_meses_1hogar_neto"] = INV / (BEN - OPEX) if BEN > OPEX else None
pay = {}
for n in (1, 2, 3, 5, 10, 20):
    neto = n * BEN - OPEX
    pay[n] = INV / neto if neto > 0 else None
out["payback_por_hogares_compartidos"] = pay
# TIR mensual aproximada (1 hogar, flujo bruto) por bisección
def vpn(r, flujo): return -INV + sum(flujo / (1 + r) ** t for t in range(1, 13))
def tir(flujo):
    lo, hi = -0.5, 5
    if vpn(lo, flujo) * vpn(hi, flujo) > 0: return None
    for _ in range(100):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if vpn(lo, flujo) * vpn(m, flujo) > 0 else (lo, m)
    return m
out["tir_mensual_bruto"] = tir(BEN); out["tir_mensual_neto"] = tir(BEN - OPEX)
# --- consumo y costo de cloro por m3 (balance de masa, disolución ideal, TCCA 90 %, 1 kg ≈ 15.000 COP supuesto de la ficha)
cons = {}
for dosis in (0.4, 1.05):
    g_m3 = dosis / 0.90
    cons[str(dosis)] = {"g_TCCA_por_m3": round(g_m3, 3), "COP_por_m3": round(g_m3 / 1000 * 15000, 1)}
out["costo_cloro_por_m3_ideal"] = cons
# Q de operación típica: 0,5 L/s; tanque lleno 4 h/día (supuesto ilustrativo de Camilo/Andrea, se rotula como supuesto)
vol_dia = 0.5 * 3600 * 4 / 1000
out["ejemplo_vol_dia_m3_0_5Ls_4h"] = vol_dia
out["ejemplo_kg_mes"] = {str(d): round(d / 0.9 * vol_dia * 30 / 1000, 2) for d in (0.4, 1.05)}
(A / "resultados_complemento.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))

plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
# --- figura: payback vs hogares
fig, ax = plt.subplots(figsize=(3.6, 2.6))
ns = np.arange(1, 21); pb = [INV / (n * BEN - OPEX) for n in ns]
ax.plot(ns, pb, "o-", color="#1F4E79", ms=3); ax.axhline(12, color="#B03A2E", ls="--", lw=.8)
ax.text(19.5, 12.6, "12 meses", color="#B03A2E", ha="right", fontsize=7)
ax.set_xlabel("Hogares que comparten una unidad"); ax.set_ylabel("Recuperación simple (meses)")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(FIG / "payback.png", dpi=300); plt.close(fig)
# --- figura: PRISMA con cifras reales
B = json.loads((A / "busqueda_prisma.json").read_text(encoding="utf-8"))
P = json.loads((A / "prisma_cifras.json").read_text(encoding="utf-8")) if (A / "prisma_cifras.json").exists() else None
cand = B["candidatos"]
EVALUADOS = [5, 8, 10, 11, 12, 16, 18, 20, 21, 28, 29, 30, 31, 34, 35, 36, 38]
EXCL_ELEG = {5: "Sin resumen en el registro; programa de emergencia en campamentos, no un dispositivo",
             35: "Contexto hospitalario (lavamanos), no abastecimiento comunitario",
             36: "Protocolo de estudio sin resultados",
             38: "Gestión de proyectos; no mide cloro residual ni desempeño del dispositivo"}
INCLUIDOS = [i for i in EVALUADOS if i not in EXCL_ELEG]
cif = {"fecha_busqueda": B["fecha"], "base": B["fuente"], "ecuacion": B["ecuacion"],
       "identificados_total": B["identificados_total_sin_filtros"], "identificados_ventana_2020_2026": B["identificados_ventana"],
       "tras_filtros_tipo_idioma_doi": B["tras_filtros_tipo_idioma_doi"], "cribados_titulo": B["cribados_titulo_con_chlorin"],
       "excluidos_filtros": B["identificados_ventana"] - B["tras_filtros_tipo_idioma_doi"],
       "excluidos_cribado_titulo": B["tras_filtros_tipo_idioma_doi"] - B["cribados_titulo_con_chlorin"],
       "evaluados_titulo_resumen": len(EVALUADOS), "excluidos_evaluacion_tema": B["cribados_titulo_con_chlorin"] - len(EVALUADOS),
       "excluidos_elegibilidad": len(EXCL_ELEG), "incluidos_busqueda": len(INCLUIDOS), "otras_fuentes": 10,
       "motivos_exclusion_elegibilidad": {str(k): v for k, v in EXCL_ELEG.items()},
       "incluidos_doi": [cand[i - 1]["doi"] for i in INCLUIDOS],
       "criterios": {"inclusion": ["Cloración de agua de consumo humano", "Dispositivo pasivo, en línea o dosificador, o evaluación de su desempeño, costo o adopción",
                                   "Contexto rural, comunitario o de bajos recursos", "Artículo 2020-2026 en inglés o español con DOI"],
                     "exclusion": ["Cloración de aguas residuales, de procesos industriales o química atmosférica", "Sensores sin dispositivo de dosificación",
                                   "Protocolos sin resultados", "Registro sin resumen"]},
       "nota": "Elegibilidad por título y resumen. La lectura completa de los 13 incluidos queda como tarea del equipo antes del envío."}
(A / "prisma_cifras.json").write_text(json.dumps(cif, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nPRISMA", {k: v for k, v in cif.items() if isinstance(v, int)})

def n(x): return f"n = {x:,}".replace(",", ".")
fig, ax = plt.subplots(figsize=(6.6, 6.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-0.3, 10.8)
def caja(x, y, w, h, t, fc, ec, fs=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
def flecha(x1, y1, x2, y2): ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=.9))
AZ, RJ = ("#EAF1F8", "#1F4E79"), ("#FDECEA", "#B03A2E")
for t, y in (("IDENTIFICACIÓN", 8.9), ("CRIBADO", 6.1), ("ELEGIBILIDAD", 3.3), ("INCLUSIÓN", 0.4)): ax.text(0.15, y + .5, t, rotation=90, va="center", fontsize=7, weight="bold")
caja(1, 8.7, 4.6, 1.6, f"Registros identificados en OpenAlex\n{n(cif['identificados_total'])}\nVentana 2020-2026: {n(cif['identificados_ventana_2020_2026'])}", *AZ)
caja(6.2, 8.7, 3.5, 1.6, f"Otras fuentes (norma, guías,\nrevisiones, método)\n{n(cif['otras_fuentes'])}", "#F3F3F3", "#555555")
flecha(3.3, 8.7, 3.3, 7.6)
caja(1, 6.0, 4.6, 1.6, f"Artículos 2020-2026 con DOI,\ncribados por título\n{n(cif['tras_filtros_tipo_idioma_doi'])}", *AZ)
caja(6.2, 6.8, 3.5, 1.1, f"Excluidos por filtros\n(tipo, idioma, DOI)\n{n(cif['excluidos_filtros'])}", *RJ)
flecha(5.6, 7.35, 6.2, 7.35)
caja(6.2, 5.0, 3.5, 1.2, f"Excluidos: el título no\ntrata de cloración\n{n(cif['excluidos_cribado_titulo'])}", *RJ)
flecha(3.3, 6.0, 3.3, 4.9); flecha(5.6, 5.6, 6.2, 5.6)
caja(1, 3.3, 4.6, 1.6, f"Evaluados por título y resumen\n{n(cif['cribados_titulo'])}", *AZ)
caja(6.2, 2.5, 3.5, 2.0, f"Excluidos al leer el resumen\n{n(cif['excluidos_evaluacion_tema'] + cif['excluidos_elegibilidad'])}\n{cif['excluidos_evaluacion_tema']} sin relación con agua de\nconsumo; {cif['excluidos_elegibilidad']} por criterio", *RJ, fs=7.2)
flecha(3.3, 3.3, 3.3, 1.7); flecha(5.6, 3.9, 6.2, 3.7)
caja(1, 0.3, 4.6, 1.4, f"Estudios incluidos (búsqueda)\n{n(cif['incluidos_busqueda'])}", "#E8F5E9", "#2E7D32")
caja(6.2, 0.3, 3.5, 1.4, f"+ otras fuentes: {cif['otras_fuentes']}\nTotal citado: {cif['incluidos_busqueda'] + cif['otras_fuentes']}", "#F3F3F3", "#555555", fs=7.4)
fig.savefig(FIG / "prisma.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# --- esquema del prototipo (a partir de las especificaciones: Tee 1", bypass con válvula, cámara 2" con válvulas de entrada y salida, Tee de mezcla)
fig, ax = plt.subplots(figsize=(6.4, 2.9)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 5.6)
def tubo(x1, y1, x2, y2, lw=5): ax.plot([x1, x2], [y1, y2], color="#6C7A89", lw=lw, solid_capstyle="butt", zorder=1)
tubo(0.3, 2.7, 1.6, 2.7); tubo(1.6, 2.7, 1.6, 4.4); tubo(1.6, 4.4, 10.2, 4.4); tubo(10.2, 4.4, 10.2, 2.7); tubo(10.2, 2.7, 11.7, 2.7)
tubo(1.6, 2.7, 1.6, 1.0); tubo(1.6, 1.0, 3.0, 1.0); tubo(7.6, 1.0, 10.2, 1.0); tubo(10.2, 1.0, 10.2, 2.7)
ax.add_patch(Rectangle((3.0, 0.35), 4.6, 1.3, fc="#FFF3E0", ec="#F57C00", lw=1.6, zorder=2)); ax.text(5.3, 1.0, "Cámara PVC 2\" (0,50 m)\npastillas de tricloro 90 %", ha="center", va="center", fontsize=7)
for xv, yv, t in ((5.9, 4.4, "V_bp"), (2.3, 1.0, "V_in"), (8.4, 1.0, "V_out")):
    ax.plot([xv], [yv], marker="D", color="#B03A2E", ms=9, zorder=3); ax.text(xv, yv + .35 if yv > 2 else yv - .6, t, ha="center", fontsize=7.5, color="#B03A2E", weight="bold")
ax.text(0.3, 3.1, "Agua cruda\nQ_total, C = 0", fontsize=7.2); ax.text(11.7, 3.1, "Mezcla\nC_salida = α·C_cámara", fontsize=7.2, ha="right")
ax.text(5.9, 5.1, "Derivación (bypass) 1\" · Q_bypass", ha="center", fontsize=7.2); ax.text(1.0, 1.9, "Q_cámara = α·Q_total", fontsize=7.2, ha="right")
ax.text(1.6, 2.7, "Tee 1\"", fontsize=6.5, ha="center", va="bottom", bbox=dict(fc="white", ec="none", pad=.5), zorder=4); ax.text(10.2, 2.7, "Tee 1\"", fontsize=6.5, ha="center", va="bottom", bbox=dict(fc="white", ec="none", pad=.5), zorder=4)
fig.savefig(FIG / "esquema.png", dpi=300, bbox_inches="tight"); plt.close(fig)
print("figuras:", [p.name for p in FIG.iterdir()])
