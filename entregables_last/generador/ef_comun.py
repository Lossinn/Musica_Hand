"""Elementos comunes de los escritos finales de Hand Sing Kids (datos, bloque de título)."""
import json, sys
from pathlib import Path
from ef_nucleo import Escrito, construir, BASE

R = json.loads((BASE / "analisis" / "resultados_vision.json").read_text(encoding="utf-8"))
A = R["aciertos"]; FPG = R["falsos_positivos"]["global_nuevo"]; FPV = R["falsos_positivos"]["global_v1"]; FPT = R["falsos_positivos"]["por_tipo"]
RB = R["robustez_fp_nuevo"]; LT = R["latencia"]; MX = R["matrices"]

NOMBRES = {
    "Vitola": "Antolin Vitola", "Petro": "Isaías Petro", "Negrete": "Andrés Negrete", "Carrascal": "Juliana Carrascal",
    "Quintana": "Angel Quintana", "Pemberty": "Alejandro Pemberty", "Guerra": "Juan Diego Guerra",
}
ORDEN = ["Vitola", "Petro", "Negrete", "Carrascal", "Quintana", "Pemberty", "Guerra"]


def f(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def m(x):
    return f"{int(round(x)):,}".replace(",", ".")


def autores_filas(primero):
    nombres = [NOMBRES[primero]] + [NOMBRES[k] for k in ORDEN if k != primero]
    return ["    ".join(nombres[0:3]), "    ".join(nombres[3:5]), "    ".join(nombres[5:7])]


DOCENTE = ["Docente: M.Sc. Cristian Javier Cano Mogollón", "Universidad Pontificia Bolivariana, Seccional Montería",
           "Facultad de Ingeniería Industrial", "Gestión Tecnológica", "6 de noviembre de 2026"]


def titulo(e, primero, titulo_txt, resumen, kw, abstract, kwe):
    e.titulo_bloque(titulo_txt, autores_filas(primero), DOCENTE, resumen, kw, abstract, kwe)


def correr(contenido):
    ruta = Path(sys.argv[1])
    ruta.parent.mkdir(parents=True, exist_ok=True)
    e = construir(contenido, ruta)
    print("guardado", ruta.name, "| cuadros", e.n_tab, "| figuras", e.n_fig, "| ecuaciones", e.n_eq, "| refs", len(set(e.citadas)))
