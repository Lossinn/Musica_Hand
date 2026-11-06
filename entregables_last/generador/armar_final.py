"""Entrega final (versión 2): artículo en dos columnas, preprint manuscrito, soporte sobrio y ZIP solo con lo confirmado.
Uso: python -X utf8 armar_final.py"""
import html, json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
import docx
import pymupdf
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
from docx2pdf import convert

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
OUT = BASE / "ENTREGA_FINAL"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FECHA = "6 de noviembre de 2026"
PF = json.loads((AQUI / "out" / "prefiltro_dos_col.json").read_text(encoding="utf-8"))["contra_fuentes"]

CSS = """<style>
@page { size: Letter; margin: 2cm; }
body { font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.3; color: #000; text-align: justify; }
h1 { font-size: 15pt; margin: 0 0 6pt; text-align: left; } h2 { font-size: 12pt; margin: 12pt 0 4pt; text-align: left; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; margin: 4pt 0; border-top: 1px solid #000; border-bottom: 1px solid #000; }
th { border-bottom: 1px solid #000; text-align: left; padding: 3pt 5pt; } td { padding: 3pt 5pt; vertical-align: top; text-align: left; }
p, li { margin: 0 0 5pt; } ul { margin: 0 0 5pt 16pt; padding: 0; } .nota { font-size: 9.5pt; } a { color: #000; word-break: break-all; }
</style>"""


def pdf_html(cuerpo, destino):
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "d.html"
        h.write_text(f"<!doctype html><html lang='es'><head><meta charset='utf-8'>{CSS}</head><body>{cuerpo}</body></html>", encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={destino}", h.as_uri()], check=True, capture_output=True, timeout=120)


FICHA = f"""
<h1>Ficha de revista indexada</h1>
<p class='nota'>Gestión Tecnológica, Universidad Pontificia Bolivariana, Seccional Montería. Consulta realizada el {FECHA}.</p>
<h2>1. Revista elegida: Revista UIS Ingenierías</h2>
<table>
<tr><th style='width:26%'>Dato</th><th>Información</th></tr>
<tr><td>Enlace</td><td><a href='https://revistas.uis.edu.co/index.php/revistauisingenierias'>https://revistas.uis.edu.co/index.php/revistauisingenierias</a></td></tr>
<tr><td>Editor</td><td>Facultad de Ingenierías Fisicomecánicas, Universidad Industrial de Santander. Revista arbitrada, trimestral y de acceso abierto.</td></tr>
<tr><td>Indexación</td><td>Su sitio declara categoría B en Publindex (MinCiencias) y presencia en Emerging Sources Citation Index, Latindex, Redalyc, EBSCO, Dialnet, REDIB, DOAJ, MIAR y PKP Index. Es la información de la propia revista; no se contrastó en el aplicativo de MinCiencias, porque SCImago no respondió en la consulta.</td></tr>
<tr><td>Alcance</td><td>Investigación original en ingeniería y ciencias aplicadas, con énfasis en ciencia de materiales, ciencias de la decisión e ingeniería de manufactura (<a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/about'>about</a>).</td></tr>
<tr><td>Idioma y tipo de artículo</td><td>Español o inglés. Investigación científica y tecnológica, revisión y reporte de caso. No publica memorias de congreso.</td></tr>
<tr><td>Formato</td><td>De 6 a 20 páginas con referencias; márgenes de 2,0 cm arriba y abajo y 2,5 cm a los lados; Verdana 10; resumen de un solo párrafo, sin citas ni fórmulas. Estructura: resumen, introducción, métodos, resultados, conclusiones y referencias.</td></tr>
<tr><td>Referencias</td><td>Estilo IEEE, con un mínimo de 15 referencias científicas.</td></tr>
<tr><td>Costos</td><td>No cobra por el envío, el procesamiento ni la publicación.</td></tr>
<tr><td>Plazos</td><td>No publica un tiempo total de decisión. Pide aceptar la revisión en 10 días y devolver el formulario en 20 como máximo; el autor responde a las correcciones en un mes.</td></tr>
<tr><td>Envío</td><td>Open Journal Systems: <a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/about/submissions'>enviar un artículo</a>. Guía para autores: <a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/information/authors'>enlace</a>.</td></tr>
<tr><td>Preprints</td><td>La guía para autores consultada no dice nada al respecto.</td></tr>
<tr><td>Licencia</td><td>La página «about» menciona CC BY-ND 4.0, pero el enlace de licencia apunta a CC BY 4.0. Conviene aclararlo con el editor.</td></tr>
</table>
<h2>2. Por qué esta revista</h2>
<p>El artículo evalúa un sistema de ingeniería con visión por computador, modelos de decisión y optimización entera mixta, y eso encaja con el alcance de la revista. No cobra, acepta español, usa OJS y ofrece plantilla en Word. El encaje temático con la educación musical es medio, porque su alcance no menciona la educación.</p>
<h2>3. Otras revistas consultadas</h2>
<table>
<tr><th style='width:24%'>Revista</th><th>Qué se encontró</th><th style='width:30%'>Por qué no</th></tr>
<tr><td>Ingeniería y Competitividad (Universidad del Valle)</td><td>Máximo 20 páginas, estilo Vancouver, resumen gráfico, figuras en blanco y negro y tres revisores sugeridos; sin cobro de envío. Su categoría B aparece en un anuncio de 2020 y en el anexo de una convocatoria anterior.</td><td>No se verificó la categoría vigente y exige más trabajo de preparación.</td></tr>
<tr><td>TecnoLógicas (ITM)</td><td>Ingeniería y tecnología aplicada, sin cobros, OJS y evaluación doble ciego. La página consultada no muestra su indexación.</td><td>No se obtuvo evidencia de una categoría vigente.</td></tr>
</table>
"""

GUIA = f"""
<h1>Guía de una página: subir el artículo a Turnitin</h1>
<p class='nota'>Archivo que se sube: Articulo_Maquetado_EquipoNN.pdf, en su versión final. Esta guía no produce el certificado; lo emite Turnitin.</p>
<h2>Antes de subir</h2>
<ul><li>Subir solo la versión final, con referencias y declaraciones, y no reutilizar borradores.</li>
<li>El filtro previo del equipo midió {PF['documento_tecnico.md']['unico']['pct']:.1f} % de coincidencia con el documento técnico del proyecto, con un tramo continuo máximo de {PF['documento_tecnico.md']['unico']['tramo_max']} palabras, y {PF['documento_2do_corte (html)']['unico']['pct']:.1f} % con el documento del segundo corte. No reemplaza a Turnitin, que compara contra internet y su propia base.</li>
<li>Si el documento técnico, el del segundo corte o un borrador anterior ya pasaron por Turnitin, aparecerán como fuente; hay que avisar al docente.</li></ul>
<h2>Configuración que pide el curso</h2>
<table><tr><th>Opción</th><th>Valor</th></tr>
<tr><td>Excluir bibliografía</td><td>Sí</td></tr><tr><td>Excluir citas textuales entre comillas</td><td>Sí</td></tr>
<tr><td>Excluir fuentes menores</td><td>No (no activar ningún umbral de palabras)</td></tr></table>
<h2>Criterios</h2>
<ul><li>Similitud total de 20 % o menos; de 15 % o menos para la nota excelente de la rúbrica.</li>
<li>Ninguna fuente individual por encima de 2 %, y sin bloques continuos largos de una sola fuente.</li>
<li>Si se supera el límite, se reescriben los fragmentos resaltados y se vuelve a subir antes de pensar en el envío.</li></ul>
<h2>Qué guardar</h2>
<p>El reporte PDF con el desglose de fuentes, con el nombre Certificado_Turnitin_EquipoNN.pdf, para añadirlo al ZIP.</p>
<h2>Orden</h2>
<p>Artículo final, Turnitin aprobado, visto bueno del docente sobre su vinculación como co-autor y, por último, el envío a la revista.</p>
"""


def main():
    previo = OUT / "1_Articulo" / "Articulo_Maquetado_EquipoNN.docx"
    ant = BASE / "_versiones_anteriores" / "articulo_plantilla_UIS"
    if previo.exists() and not ant.exists():
        ant.mkdir(parents=True)
        for ext in (".docx", ".pdf"):
            shutil.copy2(previo.with_suffix(ext), ant / f"Articulo_plantilla_UIS{ext}")
    if OUT.exists():
        for hijo in OUT.iterdir():
            if hijo.name != "_trabajo":
                shutil.rmtree(hijo) if hijo.is_dir() else hijo.unlink()
    for sub in ("1_Articulo", "2_Preprint", "3_Soporte", "4_Envio", "5_Evidencia", "6_ZIP_para_Teams"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    # artículo (dos columnas)
    dx = OUT / "1_Articulo" / "Articulo_Maquetado_EquipoNN.docx"
    r = subprocess.run([sys.executable, "-X", "utf8", str(AQUI / "ef_equipo.py"), str(dx)], cwd=AQUI, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    convert(str(dx), str(dx.with_suffix(".pdf")))
    npag = len(pymupdf.open(str(dx.with_suffix(".pdf"))))
    # preprint manuscrito: los tres escaneos reales, en un solo PDF
    pre = OUT / "2_Preprint"
    disp = {p.name: p for p in (BASE / "pre_print" / "originales").glob("*.pdf")}
    orden = [next(k for k in disp if k.startswith(pref)) for pref in ("Antolin_Vitola", "Preprint Andr", "CamScanner")]
    m = pymupdf.open()
    for n in orden:
        m.insert_pdf(pymupdf.open(str(BASE / "pre_print" / "originales" / n)))
    m.save(str(pre / "Preprint_Manuscrito_EquipoNN.pdf")); npre = len(m)
    (pre / "originales").mkdir()
    for n in orden:
        shutil.copy2(BASE / "pre_print" / "originales" / n, pre / "originales" / n)
    # soporte
    pdf_html(FICHA, OUT / "3_Soporte" / "Ficha_Revista_Indexada_EquipoNN.pdf")
    pdf_html(GUIA, OUT / "3_Soporte" / "Guia_Turnitin_1pagina.pdf")
    # envío
    d = docx.Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
    for s in d.sections:
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.5)
    texto = ["Montería, ____ de __________ de 2026", "", "Comité Editorial", "Revista UIS Ingenierías, Universidad Industrial de Santander", "",
             "Asunto: envío del manuscrito «Hand Sing Kids: señas de las manos, aprendizaje adaptativo y selección de actividades para enseñar música a niños»", "",
             "Estimados señores:", "",
             "Les enviamos para su consideración el manuscrito indicado, un artículo de investigación científica y tecnológica sobre una aplicación que enseña las ocho notas de la escala con señas de las dos manos. "
             "El texto describe el reconocedor de señas, el modelo de aprendizaje y la selección de actividades por programación entera mixta, y presenta una evaluación de laboratorio con intervalos de confianza. Creemos que encaja con el alcance de la revista en ingeniería aplicada y ciencias de la decisión.",
             "", "El manuscrito dice expresamente que no se hicieron pruebas con niños y ubica el desarrollo en el nivel de madurez tecnológica 4. El uso de un asistente de inteligencia artificial se declara en el texto.",
             "", "Quedamos atentos a sus comentarios.", "", "Cordialmente,", "", "", "______________________________",
             "Por los autores: Antolin De Jesús Vitola Montes, Isaías José Petro Rodríguez, Andrés Julián Negrete Pacheco, Juliana Esther Carrascal Hernández, Angel Quintana Jiménez, Alejandro Pemberty Vergara, Juan Diego Guerra Gómez y Cristian Javier Cano Mogollón."]
    for t in texto:
        p = d.add_paragraph(t); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.paragraph_format.space_after = Pt(0)
    d.save(str(OUT / "4_Envio" / "carta_presentacion_editor.docx"))
    ex = docx.Document(str(dx))
    ptxt = [p.text for p in ex.paragraphs]
    (OUT / "4_Envio" / "pasos_radicacion.md").write_text(f"""# Pasos para radicar en la Revista UIS Ingenierías

Hacerlos solo después del Turnitin y del visto bueno del docente.

1. Confirmar en Publindex la categoría vigente de la revista y guardar una captura.
2. Con el Turnitin aprobado (20 % o menos) y el visto bueno del docente, congelar la versión final del artículo.
3. Crear la cuenta de autor en https://revistas.uis.edu.co/index.php/revistauisingenierias, con el correo institucional de quien envía.
4. Entrar a «Enviar un artículo» y seguir los pasos de OJS: sección, requisitos, carga del archivo, metadatos, autores con filiación y comentarios al editor (la carta).
5. Cargar el artículo y las figuras en alta resolución como material complementario.
6. Finalizar el envío y guardar el acuse en pantalla y el correo automático de la revista, que deben mostrar fecha, título, autores y código de radicado.
7. Guardar la constancia como Constancia_Envio_Revista_EquipoNN.pdf y añadirla al ZIP.
8. Tras la revisión inicial, la revista pedirá la carta de presentación y licencia firmada por cada autor.

La rúbrica exige el radicado: un correo de confirmación sin él se valora como «Bueno».
""", encoding="utf-8")
    # evidencia
    ev = OUT / "5_Evidencia"; (ev / "fig").mkdir()
    for f_ in ("resultados_vision.json", "sensibilidad_umbrales.json", "salida_pruebas.txt", "refs_crossref.json", "verificacion_referencias.csv", "evidencia_vision.py", "sensibilidad_umbrales.py", "verificar_refs.py"):
        shutil.copy2(BASE / "analisis" / f_, ev / f_)
    for f_ in ("quintana_demo.py", "quintana_demo.json", "prefiltro_equipo.py"):
        shutil.copy2(AQUI / f_, ev / f_)
    shutil.copy2(AQUI / "out" / "prefiltro_dos_col.json", ev / "prefiltro_similitud.json")
    for f_ in ("prisma_hsk.png", "arquitectura.png", "capturas_app.png", "aciertos.png", "falsos_positivos.png", "matriz_similitud.png"):
        shutil.copy2(BASE / "articulo" / "fig" / f_, ev / "fig" / f_)
    corp = BASE.parent / "04_Datos" / "bibliometria" / "resultados"
    for f_ in ("informe_bibliometrico_corpus.md", "03_relacion_proyecto.csv"):
        shutil.copy2(corp / f_, ev / f_)
    shutil.copy2(BASE.parent / "07_Ecuaciones_booleanas" / "Scopus" / "ecuaciones_scopus.md", ev / "ecuaciones_scopus.md")
    # ZIP: solo lo que existe y está confirmado
    z = OUT / "6_ZIP_para_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(pre / "Preprint_Manuscrito_EquipoNN.pdf", "Preprint_Manuscrito_EquipoNN.pdf")
        zf.write(OUT / "3_Soporte" / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
        zf.write(dx.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
    (OUT / "LEEME.md").write_text(f"""# Entrega del equipo: Hand Sing Kids, Corte 3

Gestión Tecnológica, UPB Seccional Montería. Preparada el {FECHA}.

## Qué hay
| Carpeta | Contenido |
|---|---|
| `1_Articulo/` | Artículo del equipo en dos columnas, PDF y Word ({npag} páginas, 22 referencias verificadas). Autores: los siete integrantes y el docente Cristian Cano |
| `2_Preprint/` | Preprint manuscrito: los tres escaneos existentes unidos en un PDF ({npre} páginas) y los originales |
| `3_Soporte/` | Ficha de la revista y guía de una página para Turnitin |
| `4_Envio/` | Carta al editor y pasos de radicación en OJS |
| `5_Evidencia/` | Resultados, sensibilidad de umbrales, salida de pruebas, referencias, corpus, ecuaciones de búsqueda y filtro de similitud |
| `6_ZIP_para_Teams/` | `02_GT_Corte3_CierreProyecto_EquipoNN.zip` con lo que ya existe y está confirmado |

## El ZIP
Contiene `Preprint_Manuscrito_EquipoNN.pdf`, `Ficha_Revista_Indexada_EquipoNN.pdf` y `Articulo_Maquetado_EquipoNN.pdf`. No incluye marcadores ni archivos simulados.

Faltan dos archivos de la rúbrica que solo pueden emitir terceros:
- `Certificado_Turnitin_EquipoNN.pdf`: se genera subiendo el PDF del artículo a Turnitin (guía en `3_Soporte/`).
- `Constancia_Envio_Revista_EquipoNN.pdf`: la entrega el portal de la revista al radicar, después del Turnitin y del visto bueno del docente (pasos en `4_Envio/`).
Cuando existan, se añaden al ZIP con esos nombres.

## Notas para el equipo
- Los tres preprints manuscritos suman {npre} páginas; la guía pide de 2 a 3 para el equipo. Si el docente lo exige, conviene dejar una sola versión.
- El artículo no incluye ORCID, autor de correspondencia, financiación ni conflicto de intereses, porque no están confirmados. Hay que añadirlos antes del envío si la revista los pide.
- No hubo pruebas con niños: las cifras son de laboratorio, con la calibración de una persona y perturbaciones simuladas. El nivel de madurez es TRL 4.
- La búsqueda bibliográfica es una muestra de conveniencia y no se anotó el número de resultados de cada ecuación en Scopus.
- Los análisis de la ventana de Canciones y del dominio frente a la retención son cálculos con las fórmulas, y la instancia del optimizador es ilustrativa; el artículo lo dice.
- Del código de la asignatura hay dos versiones en los documentos del curso (8830 0048 0 y 8830 0064 0); conviene confirmar cuál va en la entrega.
- Filtro previo de similitud del equipo: {PF['documento_tecnico.md']['unico']['pct']:.1f} % contra el documento técnico y {PF['documento_2do_corte (html)']['unico']['pct']:.1f} % contra el del segundo corte. No sustituye a Turnitin.
- Se verificó que cada referencia existe y que sus metadatos coinciden; no se leyeron los textos completos.
- El artículo declara el uso de un asistente de inteligencia artificial. Antes de defenderlo, todos deben haberlo leído completo.
""", encoding="utf-8")
    print("listo:", npag, "pág. artículo;", npre, "pág. preprint;", [i.filename for i in zipfile.ZipFile(z).infolist()])


main()
