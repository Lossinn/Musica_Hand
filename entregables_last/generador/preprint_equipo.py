"""Preprint del equipo (texto para copiar a mano, 2 a 3 páginas) con PRISMA, formulación y síntesis de la discusión."""
import re, sys
from pathlib import Path
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = Path(__file__).resolve().parent.parent
SALIDA = Path(sys.argv[1])

TEXTO = [
    ("Título", "Hand Sing Kids: enseñar las notas con las manos, estimar lo que aprende cada niño y elegir sus actividades. Diseño y evaluación de laboratorio en Montería"),
    ("Autores", "Antolin Vitola, Isaías Petro, Andrés Negrete, Juliana Carrascal, Angel Quintana, Alejandro Pemberty y Juan Diego Guerra. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Gestión Tecnológica, tercer corte. 6 de noviembre de 2026. Co-autor: M.Sc. Cristian Javier Cano Mogollón (SILOGE, HIS)."),
    ("Resumen preliminar", "Hand Sing Kids es una aplicación de escritorio, en Python, que enseña las ocho notas de Do3 a Do4 con señas de las dos manos. Una cámara y MediaPipe entregan los puntos de las manos; un descriptor invariante y un clasificador reconocen la seña; "
     "un modelo de dominio con repaso espaciado estima lo que sabe el niño; y un problema de optimización elige la siguiente sesión. Evaluamos todo en laboratorio, con una calibración de una persona y ruido simulado. No hubo niños. Los resultados son técnicos y el efecto en el aprendizaje queda como hipótesis."),
    ("1. Problema en Montería y Córdoba", "Enseñar música con las manos es antiguo: cada nota tiene una seña. Falta quien corrija. En Montería hay 535.052 habitantes y 80.254 de ellos tienen de 3 a 12 años (DANE, 2026). No encontramos una estadística local de educación musical y no la inventamos. "
     "Nuestra razón es de diseño: la aplicación corre en un computador con cámara, guarda sus datos en una base local y no necesita internet. El problema técnico tiene tres partes: reconocer cuándo el niño hizo una seña de verdad y no un gesto de paso, estimar lo que sabe y decidir qué practicar."),
    ("2. Búsqueda de literatura (PRISMA)", "Usamos dos ecuaciones en Scopus: música con IA y tecnología educativa, y gesto o visión con música. Obtuvimos 226 archivos y quitamos 37 copias idénticas, y quedaron 189 documentos únicos. "
     "Marginales excluidos: 41. Evaluados: 148. Método o contexto sin uso directo: 61. Incluidos: 87, de los cuales 22 son el núcleo. No registramos el número de resultados de cada ecuación. Solo ocho documentos tratan música infantil: ahí está el hueco."),
    ("3. Formulación esencial", "a) Aceptar una nota si d_mejor ≤ 0,95, P_mejor ≥ 0,55 y P_mejor − P_segunda ≥ 0,08, con P(c|x) = exp(−(d_c − d_mín)/T) / Σ_k exp(−(d_k − d_mín)/T).\n"
     "b) Dominio: M = (λ + (1 − λ)·R^γ)·(0,55·P + 0,25·C + 0,20·V), con R = exp(−Δt/τ), λ = 0,65 y γ = 0,40. Dominada si M ≥ 0,80 con al menos 6 intentos.\n"
     "c) Sesión: máx Σ_i (α1·g_i + α2·r_i + α3·m_i − α4·f_i)·x_i, con x_i ∈ {0, 1}, sujeta a tiempo total, K actividades, prerrequisitos, una lúdica como mínimo, dificultad media ≤ 0,72 y un repaso vencido. g = ganancia, r = repaso, m = motivación, f = fatiga."),
    ("4. Resultados y síntesis de la discusión", "Con 480 señas por nivel de ruido, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido 0,09. Ante 640 posturas que no son seña, el método nuevo disparó una nota por error en 8,0 % de los casos (51 de 640), frente a 100 % del método inicial, que acierta siempre porque responde siempre. "
     "El error viene casi todo de las transiciones. Variar el umbral de confianza mueve el compromiso entre acertar y abstenerse; los umbrales de distancia y de margen no cambiaron nada. Ocho baterías de pruebas pasaron. "
     "Contrastamos las cifras que la documentación reportaba: una se reprodujo, una resultó del mismo orden, una no coincide, una no es comparable y una no se midió."),
    ("5. Límites y cierre", "Calibración de una sola persona, ruido simulado, constantes de diseño sin datos de niños y ningún piloto en el aula. Nivel de madurez TRL 4. El siguiente paso es un piloto con aprobación ética, consentimiento de los acudientes y medición antes y después. "
     "El aporte es un sistema explicable, con cifras repetibles y límites dichos con claridad."),
]


def main():
    d = docx.Document()
    d.styles["Normal"].font.name = "Calibri"; d.styles["Normal"].font.size = Pt(11)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    d.add_heading("Preprint del equipo — para transcribir a mano", 1)
    p = d.add_paragraph()
    p.add_run("Instrucciones. ").bold = True
    p.add_run("Copien el recuadro con su letra en 2 o 3 páginas (hojas de examen o cuaderno), dibujen a mano el diagrama PRISMA de la última página con las mismas cifras y escaneen el resultado en PDF nítido con el nombre Preprint_Manuscrito_EquipoNN.pdf. "
              "Léanlo antes para entenderlo y háganlo suyo: el objetivo de la rúbrica es que se note su autoría. Pueden cambiar palabras, pero no las cifras. Si lo escriben varios, repartan las secciones.")
    t = d.add_table(rows=1, cols=1); t.alignment = 1
    bd = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right"):
        x = OxmlElement(f"w:{lado}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "18"); x.set(qn("w:color"), "1F4E79"); bd.append(x)
    t._tbl.tblPr.append(bd)
    c = t.rows[0].cells[0]
    h = c.paragraphs[0]; r = h.add_run("ESCRITO FINAL — PREPRINT DEL EQUIPO"); r.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    for rot, txt in TEXTO:
        q = c.add_paragraph(); q.add_run(rot).bold = True
        for linea in txt.split("\n"):
            pp = c.add_paragraph(linea); pp.paragraph_format.space_after = Pt(3)
    d.add_page_break()
    d.add_heading("Diagrama PRISMA para dibujar a mano", 2)
    d.add_paragraph("Cuatro fases, de arriba abajo: identificación, cribado, elegibilidad e inclusión. Las cajas rojas son las exclusiones. Dibújenlo con las mismas cifras.")
    d.add_picture(str(BASE / "articulo" / "fig" / "prisma_hsk.png"), width=Cm(11.5))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph("Distribución sugerida de las páginas. Página 1: título, autores, resumen y problema. Página 2: búsqueda con el diagrama PRISMA y formulación. Página 3: resultados, discusión y límites.")
    d.save(str(SALIDA))
    print("ok")


main()
