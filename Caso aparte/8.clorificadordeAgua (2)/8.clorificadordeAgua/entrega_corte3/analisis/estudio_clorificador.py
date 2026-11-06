"""Estudio reproducible del clorificador pasivo (Corte 3).

Todo sale de los parámetros del notebook montecarlo_clorificador.ipynb y de las ecuaciones de
01_Documentacion_Tecnica/Modelo_Matematico_y_Mecanica_de_Fluidos.md. Nada se mide aquí: es una
simulación con distribuciones SUPUESTAS por el equipo. Salidas: resultados_estudio.json y figuras.
Uso: python -X utf8 estudio_clorificador.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
FIG = AQUI.parent / "articulo" / "fig"
FIG.mkdir(parents=True, exist_ok=True)
CSV_NB = RAIZ / "Documentos Digital de Desarrollo" / "output" / "simulacion_montecarlo_clorificador.csv"
LO, HI, META = 0.2, 0.5, 0.4


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - m), 100 * (c + m)


def escenarios(N, g, escala_dosis=1.0, demanda_media=0.65):
    """Mismo modelo y mismas distribuciones del notebook (orden de sorteo idéntico)."""
    Q = np.clip(g.normal(1.0, 0.25, N), 0.2, None)
    t = np.clip(g.normal(20, 4, N), 5, None)
    C0 = np.clip(g.normal(1.2, 0.3, N), 0.2, None)
    dem = np.clip(g.normal(demanda_media, 0.18, N), 0.1, None)
    frac = np.clip(g.beta(2.5, 5.5, N), 0.05, 0.95)
    k = np.clip(g.normal(0.035, 0.01, N), 0.005, None)
    T = np.clip(g.normal(28, 3, N), 18, None)
    pH = np.clip(g.normal(7.2, 0.4, N), 6.0, 8.5)
    turb = np.clip(g.gamma(2.2, 0.6, N), 0.1, None)
    fT = np.exp(0.03 * (T - 25))
    fpH = 1 + 0.06 * np.abs(pH - 7.2)
    fturb = 1 + 0.15 * turb
    fQ = 1 + 0.08 * (Q - 1.0)
    neto = C0 * frac * escala_dosis - dem
    cres = np.maximum(neto * np.exp(-k * t) / (fT * fpH) / fturb / fQ, 0)
    X = dict(Q=Q, t=t, C0=C0, demanda=dem, frac=frac, k=k, T=T, pH=pH, turb=turb)
    return X, cres, neto


class GlobalRNG:
    """Adaptador al generador global de NumPy, para conservar el orden de sorteo del notebook."""
    normal = staticmethod(np.random.normal)
    beta = staticmethod(np.random.beta)
    gamma = staticmethod(np.random.gamma)


def pct_ok(c):
    return float(100 * ((c >= LO) & (c <= HI)).mean())


def main():
    res = {}
    # 1) reproducción exacta del notebook (semilla 42)
    np.random.seed(42)
    X, cres, neto = escenarios(1000, GlobalRNG)
    with open(CSV_NB, encoding="utf-8") as f:
        ref = np.array([float(r["cloro_residual_mgL"]) for r in csv.DictReader(f)])
    res["reproduccion"] = {"max_diferencia_vs_csv_del_notebook": float(np.max(np.abs(ref - cres))), "N": 1000}
    sub = int((cres < LO).sum())
    ade = int(((cres >= LO) & (cres <= HI)).sum())
    sob = int((cres > HI).sum())
    res["base"] = {"sub": sub, "adecuada": ade, "sobre": sob, "media": float(cres.mean()), "max": float(cres.max()),
                   "ceros": int((cres == 0).sum()), "ic_adecuada": wilson(ade, 1000), "ic_sub": wilson(sub, 1000),
                   "dosis_efectiva_media": float((X["C0"] * X["frac"]).mean()), "demanda_media": float(X["demanda"].mean()),
                   "p_dosis_mayor_demanda": float(((X["C0"] * X["frac"]) > X["demanda"]).mean())}
    # 2) sensibilidad (Spearman sobre el valor neto antes de recortar a cero, que sí es continuo)
    rho = {}
    for k_, v in X.items():
        r, p = stats.spearmanr(v, neto)
        rho[k_] = {"rho": float(r), "p": float(p)}
    res["spearman_neto"] = rho
    # 3) mapa de cumplimiento: escala de la dosis (C0*frac) x demanda media
    escalas = np.round(np.linspace(0.5, 6.0, 23), 3)
    demandas = np.round(np.linspace(0.05, 1.0, 20), 3)
    M = np.zeros((len(demandas), len(escalas)))
    for i, d in enumerate(demandas):
        for j, e in enumerate(escalas):
            _, c, _ = escenarios(20000, np.random.default_rng(7), escala_dosis=e, demanda_media=d)
            M[i, j] = pct_ok(c)
    res["mapa"] = {"escalas": escalas.tolist(), "demandas": demandas.tolist(), "cumple_pct": M.round(2).tolist()}
    i_mx = np.unravel_index(np.argmax(M), M.shape)
    res["mapa_resumen"] = {"max_cumplimiento_pct": float(M.max()), "en_demanda": float(demandas[i_mx[0]]),
                           "en_escala": float(escalas[i_mx[1]]), "celdas_ge_90": int((M >= 90).sum()), "celdas_totales": int(M.size)}
    res["mejor_por_demanda"] = [{"demanda": float(d), "mejor_pct": float(M[i].max()), "escala": float(escalas[int(M[i].argmax())])}
                                for i, d in enumerate(demandas)]
    # 4) ¿cuánto del incumplimiento restante es variabilidad y no falta de dosis?
    # Con la dosis ajustada al mejor punto del mapa, se compara la fracción dosificada variable (beta) con una fija en su media.
    e_best, d_best = float(escalas[i_mx[1]]), float(demandas[i_mx[0]])
    _, c_var, _ = escenarios(20000, np.random.default_rng(11), escala_dosis=e_best, demanda_media=d_best)
    Xf, _, _ = escenarios(20000, np.random.default_rng(11), escala_dosis=1.0, demanda_media=d_best)
    frac_media = 2.5 / (2.5 + 5.5)
    neto_f = Xf["C0"] * frac_media * e_best - Xf["demanda"]
    fT = np.exp(0.03 * (Xf["T"] - 25))
    fpH = 1 + 0.06 * np.abs(Xf["pH"] - 7.2)
    fturb = 1 + 0.15 * Xf["turb"]
    fQ = 1 + 0.08 * (Xf["Q"] - 1)
    c_fija = np.maximum(neto_f * np.exp(-Xf["k"] * Xf["t"]) / (fT * fpH) / fturb / fQ, 0)
    res["variabilidad_vs_dosis"] = {"punto": {"escala": e_best, "demanda": d_best},
                                    "cumple_fraccion_variable_pct": pct_ok(c_var), "cumple_fraccion_fija_pct": pct_ok(c_fija)}
    # 5) requerimiento de disolución y consumo de tabletas (balance de masa)
    filas = []
    for Q in (0.2, 0.5, 1.0, 1.5, 2.5):
        for dosis in (0.4, 1.05):   # 0,4 = solo el residual meta; 1,05 = demanda media supuesta (0,65) + residual meta
            mg_s = dosis * Q
            g_dia = mg_s * 86400 / 1000
            tcca = g_dia / 0.90
            filas.append({"Q_Ls": Q, "dosis_mgL": dosis, "mg_por_s": round(mg_s, 3), "cloro_g_dia": round(g_dia, 1),
                          "TCCA90_g_dia": round(tcca, 1), "TCCA90_kg_mes_24h": round(tcca * 30 / 1000, 2)})
    res["consumo"] = filas
    res["alcance_1kg_TCCA90_m3"] = {"dosis_1_05": 900000 / 1.05 / 1000, "dosis_0_4": 900000 / 0.4 / 1000}
    res["C_camara_requerida_mgL"] = {f"alpha={a_}": round(META / a_, 2) for a_ in (0.05, 0.1, 0.2, 0.5)}
    # 6) potencia del DOE 2^3 x 3 réplicas (N = 24, gl del error = 16)
    pot = []
    crit = stats.f.ppf(0.95, 1, 16)
    for sigma in (0.03, 0.05, 0.10, 0.15):
        for f_ in np.linspace(0.05, 2.0, 4000):
            if 1 - stats.ncf.cdf(crit, 1, 16, 24 * f_ ** 2) >= 0.8:
                pot.append({"sigma_mgL": sigma, "f": round(float(f_), 3), "delta_min_mgL": round(float(2 * f_ * sigma), 3)})
                break
    res["potencia_DOE"] = pot
    rng = np.random.default_rng(2026)
    corridas = [(q, v, p) for q in (0.5, 1.5) for v in (25, 75) for p in (1, 2) for _ in range(3)]
    orden = rng.permutation(len(corridas))
    with open(AQUI.parent / "soporte" / "DOE_hoja_aleatorizacion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["orden_ejecucion", "caudal_Ls", "V_bypass_pct", "pastillas", "cloro_residual_mgL", "observaciones"])
        for k_, idx in enumerate(orden, 1):
            q, v, p = corridas[idx]
            w.writerow([k_, q, v, p, "", ""])
    # 7) auditoría del CSV de ensayos (procedencia sin confirmar; NO se usa como resultado)
    aud = []
    with open(RAIZ / "04_Toma_de_Datos_y_Seguimiento" / "Formato_Captura_Datos_Ensayos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            Qc = float(r["volumen_colectado_L"]) / float(r["tiempo_aforo_s"])
            c = float(r["cloro_residual_mgL"])
            est = "Sin_Cloro" if r["num_pastillas"] == "0" else ("Subclorada" if c < LO else ("Adecuada" if c <= HI else "Sobreclorada"))
            aud.append({"id": int(r["id_ensayo"]), "Q_recalculado": round(Qc, 3), "Q_registrado": float(r["caudal_L_s"]),
                        "Q_ok": abs(Qc - float(r["caudal_L_s"])) < 0.002, "estado_ok": est == r["estado_cloracion"],
                        "pastillas": int(r["num_pastillas"]), "v_bp": int(r["posicion_v_bp_pct"]), "cres": c})
    res["auditoria_csv"] = {"filas": len(aud), "Q_consistente": all(a["Q_ok"] for a in aud),
                            "estado_consistente": all(a["estado_ok"] for a in aud),
                            "con_cloro": sum(1 for a in aud if a["pastillas"] > 0), "detalle": aud}
    (AQUI / "resultados_estudio.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- figuras
    plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.hist(cres, bins=40, color="#1F4E79")
    ax.axvspan(LO, HI, color="#2E7D32", alpha=.25, label="Rango 0,2–0,5 mg/L")
    ax.set_xlabel("Cloro residual simulado (mg/L)")
    ax.set_ylabel("Escenarios (n = 1000)")
    ax.legend(frameon=False, fontsize=6.5)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "hist_cloro.png", dpi=300); plt.close(fig)

    nombres = {"Q": "Caudal Q", "t": "Tiempo de contacto", "C0": "Cloro inicial C0", "demanda": "Demanda de cloro",
               "frac": "Fracción dosificada", "k": "Constante de decaimiento", "T": "Temperatura", "pH": "pH", "turb": "Turbidez"}
    orden_v = sorted(rho, key=lambda k_: abs(rho[k_]["rho"]))
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.barh([nombres[k_] for k_ in orden_v], [rho[k_]["rho"] for k_ in orden_v],
            color=["#B03A2E" if rho[k_]["rho"] < 0 else "#1F4E79" for k_ in orden_v])
    ax.axvline(0, color="k", lw=.6)
    ax.set_xlabel("Correlación de Spearman con el cloro neto")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "spearman.png", dpi=300); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    im = ax.imshow(M, origin="lower", aspect="auto", cmap="viridis",
                   extent=[escalas[0], escalas[-1], demandas[0], demandas[-1]], vmin=0, vmax=100)
    if (M >= 90).any():
        ax.contour(escalas, demandas, M, levels=[90], colors="white", linewidths=1.2)
    ax.plot([1.0], [0.65], "r*", ms=11, label="Supuestos del notebook")
    ax.set_xlabel("Escala de la dosis efectiva (× media del notebook, 0,3 mg/L)")
    ax.set_ylabel("Demanda media de cloro (mg/L)")
    ax.legend(loc="upper right", fontsize=7)
    fig.colorbar(im, ax=ax).set_label("Escenarios en 0,2–0,5 mg/L (%)")
    fig.tight_layout(); fig.savefig(FIG / "mapa_cumplimiento.png", dpi=300); plt.close(fig)

    show = {k_: res[k_] for k_ in ("reproduccion", "base", "mapa_resumen", "variabilidad_vs_dosis",
                                   "alcance_1kg_TCCA90_m3", "C_camara_requerida_mgL", "potencia_DOE")}
    print(json.dumps(show, indent=1, ensure_ascii=False))
    print("spearman", {k_: round(v["rho"], 2) for k_, v in rho.items()})
    print("auditoria CSV", {k_: v for k_, v in res["auditoria_csv"].items() if k_ != "detalle"})
    print("mejor por demanda", [(m["demanda"], round(m["mejor_pct"], 1)) for m in res["mejor_por_demanda"][::3]])


main()
