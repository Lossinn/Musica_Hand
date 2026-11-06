from ef_nucleo import *
def contenido(e):
    e.titulo_bloque("Título de prueba para verificar el formato del escrito final de Hand Sing Kids",
                    ["Antolin Vitola    Isaías Petro", "Andrés Negrete    Juliana Carrascal", "Angel Quintana    Alejandro Pemberty"],
                    ["Docente: M.Sc. Cristian Javier Cano Mogollón", "Universidad Pontificia Bolivariana", "Facultad de Ingeniería Industrial", "Gestión Tecnológica", "6 de noviembre de 2026"],
                    "Resumen de prueba " * 40, "uno; dos; tres", "Abstract test " * 40, "one; two")
    e.sec("Introducción")
    e.P("Texto de prueba con una cita {cite:yi,mediapipe} y una narrativa {citet:wilsonci}. Véase {tab:a}, {fig:a} y la ecuación {eq:a}. " * 6)
    e.sub("Supuestos")
    e.B(["Primer supuesto de la lista con texto largo para ver el ajuste de línea en la columna.", "Segundo supuesto."])
    e.eq("a", r"C_r=\max\!\left(\frac{(C_s-D)\,e^{-kt}}{f_T},\,0\right)")
    e.tabla("a", "Tabla de prueba.", ["Conjunto", "Descripción", "Valor"], [["$D$", "Bodega", "1,0"], ["$C$", "Clientes", "499"]], [2, 5, 1.5], alinear=["l", "l", "r"])
    e.figura("a", "esquema_ejemplo.png" if False else "arquitectura.png", "Figura de prueba.", 8.3)
    e.P("Más texto. " * 120)
    e.referencias()
construir(contenido, "out/prueba_ef.docx")
from docx2pdf import convert; convert("out/prueba_ef.docx", "out/prueba_ef.pdf")
import pymupdf; d = pymupdf.open("out/prueba_ef.pdf"); print(len(d)); d[0].get_pixmap(dpi=70).save("out/pe1.png"); d[1].get_pixmap(dpi=70).save("out/pe2.png")
print(set(f[3] for p in d for f in p.get_fonts()))
