"""Genera los documentos de soporte del Corte 3 (sin simular nada que emita un tercero).

Salidas (en entrega_corte3/):
  soporte/Ficha_Revista_Indexada_EquipoNN.pdf
  soporte/Guia_Turnitin_1pagina.pdf
  soporte/PENDIENTE_Certificado_Turnitin_EquipoNN.pdf          (marcador, no es un certificado)
  soporte/PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf      (marcador, no es una constancia)
  soporte/PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf           (marcador del escaneo del equipo)
  envio/*  (metadatos, carta, lista de pasos)
  analisis/verificacion_referencias.csv
Uso: python -X utf8 generar_soporte.py
"""
from __future__ import annotations

import csv
import html
import json
import subprocess
import tempfile
from pathlib import Path

import docx
from docx.shared import Pt

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
SOP = BASE / "soporte"; ENV = BASE / "envio"
SOP.mkdir(exist_ok=True); ENV.mkdir(exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FECHA = "5 de noviembre de 2026"
TITULO = ("Reconocimiento invariante de señas manuales y selección óptima de sesiones para la enseñanza de "
          "notas musicales a niños: evaluación técnica de laboratorio de Hand Sing Kids")
TITULO_EN = ("Invariant hand-sign recognition and optimal session selection for teaching musical notes to "
             "children: laboratory technical evaluation of Hand Sing Kids")

CSS = """<style>
@page { size: Letter; margin: 2cm; }
body { font-family: Verdana, 'Segoe UI', sans-serif; font-size: 10pt; line-height: 1.35; color: #111; }
h1 { font-size: 16pt; margin: 0 0 4pt; } h2 { font-size: 11.5pt; margin: 14pt 0 4pt; border-bottom: 1px solid #999; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; } td, th { border: 1px solid #aaa; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #eee; } .nota { font-size: 8.5pt; color: #444; } a { color: #0b4f8a; word-break: break-all; }
.caja { border: 3px solid #b00020; padding: 18pt; margin-top: 60pt; text-align: center; }
.caja h1 { color: #b00020; font-size: 22pt; }
</style>"""


def pdf(nombre_html: str, cuerpo: str, destino: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "d.html"
        h.write_text(f"<!doctype html><html lang='es'><head><meta charset='utf-8'>{CSS}</head><body>{cuerpo}</body></html>",
                     encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={destino}", h.as_uri()], check=True, capture_output=True, timeout=120)


def marcador(titulo: str, quien: str, detalle: str, destino: Path) -> None:
    pdf("m", f"<div class='caja'><h1>PENDIENTE: {html.escape(titulo)}</h1><p><b>{html.escape(quien)}</b></p>"
             f"<p>{html.escape(detalle)}</p><p class='nota'>Este archivo es un marcador de posición generado el {FECHA}. "
             "No es un documento oficial ni tiene validez. Debe reemplazarse por el archivo real, con este mismo nombre, "
             "antes de subir el ZIP a Teams.</p></div>", destino)


# ------------------------------------------------------------------ ficha de revista
ficha = f"""
<h1>Ficha de revista indexada</h1>
<p class='nota'>Equipo NN · Gestión Tecnológica (8830 0048 0) · UPB Seccional Montería · 2026-2 · Consulta realizada el {FECHA}.</p>
<h2>1. Revista seleccionada: Revista UIS Ingenierías</h2>
<table>
<tr><th style='width:28%'>Dato</th><th>Valor y evidencia</th></tr>
<tr><td>Enlace oficial</td><td><a href='https://revistas.uis.edu.co/index.php/revistauisingenierias'>https://revistas.uis.edu.co/index.php/revistauisingenierias</a></td></tr>
<tr><td>Editor</td><td>Facultad de Ingenierías Fisicomecánicas, Universidad Industrial de Santander (UIS). Revista arbitrada, trimestral, de acceso abierto.</td></tr>
<tr><td>Indexación declarada</td><td><b>Publindex (MinCiencias), categoría B</b>; además Emerging Sources Citation Index (Web of Science), Latindex, Redalyc, EBSCO Fuente Académica Premier, Dialnet, REDIB, DOAJ, MIAR y PKP Index. Evidencia: página de inicio de la revista, consultada el {FECHA} (número vigente: Vol. 25, n.º 4, 2026, vista temprana publicada el 21 de septiembre de 2026).</td></tr>
<tr><td>Límite de la evidencia</td><td>La categoría B proviene del sitio de la propia revista. No se pudo contrastar en el aplicativo de MinCiencias ni en SCImago (el sitio de SCImago respondió «403 Forbidden» y las búsquedas no devolvieron resultados oficiales de las convocatorias recientes). <b>Antes del envío, el equipo debe confirmar la categoría vigente en Publindex y guardar la captura.</b> No se afirma cuartil Scopus.</td></tr>
<tr><td>Alcance (aims and scope)</td><td>Investigación original en ingeniería y ciencias aplicadas, con énfasis en ciencia de materiales, ciencias de la decisión e ingeniería de manufactura (<a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/about'>about</a>).</td></tr>
<tr><td>Idiomas</td><td>Español o inglés (título y resumen en ambos).</td></tr>
<tr><td>Tipos de artículo</td><td>Investigación científica y tecnológica original, revisión y reporte de caso. No publica memorias de congreso.</td></tr>
<tr><td>Extensión y formato</td><td>6 a 20 páginas incluyendo referencias; márgenes superior e inferior 2,0 cm, laterales 2,5 cm; interlineado sencillo; Verdana 10; resumen en un solo párrafo, sin citas ni fórmulas, menos de 400 palabras (la plantilla recomienda 150 a 250); estilo impersonal. Estructura mínima: resumen, introducción, métodos, resultados, conclusiones, referencias.</td></tr>
<tr><td>Referencias</td><td>Estilo IEEE, mínimo 15 referencias científicas.</td></tr>
<tr><td>Costos</td><td>Sin cobro por envío, procesamiento ni publicación (declarado en la página «about»).</td></tr>
<tr><td>Tiempos de revisión</td><td>La revista no publica un tiempo total de decisión. Plazos declarados: 10 días para aceptar la revisión y máximo 20 días para entregar el formulario; el autor debe responder a las correcciones en un mes.</td></tr>
<tr><td>Plataforma de envío</td><td>Open Journal Systems (OJS): <a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/about/submissions'>enviar un artículo</a>.</td></tr>
<tr><td>Política de preprints</td><td>No figura en la guía para autores consultada.</td></tr>
<tr><td>Guía y plantilla</td><td><a href='https://revistas.uis.edu.co/index.php/revistauisingenierias/information/authors'>Guía para autores</a>; plantilla Word y carta de presentación y licencia (guardadas en <i>revista/</i>).</td></tr>
<tr><td>Licencia</td><td>La página «about» menciona CC BY-ND 4.0, pero el enlace de licencia apunta a CC BY 4.0: la revista es inconsistente; conviene confirmarlo con el editor.</td></tr>
</table>
<h2>2. Justificación</h2>
<p>El artículo es una evaluación técnica de un sistema de ingeniería con optimización (programación entera mixta), modelos de decisión y visión por computador; el alcance de la revista cubre ingeniería aplicada y ciencias de la decisión. No cobra por enviar ni publicar, acepta español, usa OJS y tiene plantilla Word oficial, lo que hace viable cumplir el plazo. La categoría B figura en su sitio vigente. Ajuste temático: <b>medio</b>, porque el alcance no menciona educación; es una decisión de compromiso que el docente puede objetar.</p>
<h2>3. Candidatas descartadas</h2>
<table>
<tr><th style='width:22%'>Revista</th><th>Qué se encontró (consulta del {FECHA})</th><th style='width:30%'>Motivo del descarte</th></tr>
<tr><td>Ingeniería y Competitividad (Universidad del Valle)</td><td>Guía: máximo 20 páginas, estilo Vancouver, resumen de hasta 300 palabras, resumen gráfico, figuras en blanco y negro, mínimo tres revisores sugeridos, sin cobro de envío; indexada en Publindex, ESCI y SciELO según su guía. La categoría B se documenta en un anuncio de 2020 y en el anexo de la convocatoria 910, sin resultado más reciente. <a href='https://revistaingenieria.univalle.edu.co/index.php/ingenieria_y_competitividad/autores'>Guía</a></td><td>Categoría vigente no verificada; exige tres revisores sugeridos, resumen gráfico y figuras en blanco y negro, lo que alarga la preparación; no publica plantilla.</td></tr>
<tr><td>TecnoLógicas (ITM)</td><td>Revista de ingeniería y tecnología aplicada (incluye ciencias de la computación), sin cobros, OJS, evaluación doble ciego con al menos dos pares. La página consultada no muestra la sección de indexación. <a href='https://revistas.itm.edu.co/index.php/tecnologicas/about'>About</a></td><td>No se obtuvo evidencia de categoría Publindex ni de Scopus/WoS vigentes; sin ella no cumple el requisito del curso.</td></tr>
<tr><td>DYNA</td><td>No se consultó su sitio en esta ronda.</td><td>Sin evidencia; no se evaluó.</td></tr>
</table>
<p class='nota'>Evidencia guardada: páginas oficiales citadas arriba. Pendiente del equipo: captura de Publindex con la categoría vigente.</p>
"""
pdf("ficha", ficha, SOP / "Ficha_Revista_Indexada_EquipoNN.pdf")

# ------------------------------------------------------------------ guía Turnitin
guia = f"""
<h1>Guía de una página: subir el artículo a Turnitin</h1>
<p class='nota'>Archivo a subir: <b>Articulo_Maquetado_EquipoNN.pdf</b> (versión final). Esta guía no genera el certificado: lo emite Turnitin.</p>
<h2>Antes de subir</h2>
<ul><li>Subir el PDF final, no un borrador. Revisar que sea la versión con las referencias y las declaraciones.</li>
<li>El filtro previo del equipo (<i>analisis/prefiltro_similitud.py</i>) midió 0,75 % de coincidencia con <i>documento_tecnico.md</i> y 0,37 % con el documento del 2.º corte. No sustituye a Turnitin: no ve internet ni su base.</li>
<li>Si el documento del 2.º corte o el repositorio ya se subieron a Turnitin, aparecerán como fuente; avisar al docente.</li></ul>
<h2>Configuración (según la guía del curso)</h2>
<table><tr><th>Opción</th><th>Valor</th></tr>
<tr><td>Excluir bibliografía / referencias</td><td>Sí</td></tr><tr><td>Excluir citas textuales entre comillas</td><td>Sí</td></tr>
<tr><td>Excluir fuentes menores</td><td><b>No</b> (no activar ningún umbral de palabras)</td></tr></table>
<h2>Criterios</h2>
<ul><li>Aprobación: similitud <b>≤ 20 %</b>. Para nota excelente en la rúbrica: <b>≤ 15 %</b>.</li>
<li>Ninguna fuente individual puede superar el 2 % ni haber bloques continuos extensos de una sola fuente.</li>
<li>Si se supera el umbral, reescribir los fragmentos resaltados y repetir; no enviar a la revista.</li></ul>
<h2>Qué guardar</h2>
<ul><li>El reporte PDF con el desglose de fuentes, nombrado <b>Certificado_Turnitin_EquipoNN.pdf</b>.</li>
<li>Sustituir el marcador PENDIENTE de la carpeta de entrega por ese archivo.</li></ul>
<h2>Orden obligatorio</h2>
<p>Artículo final → Turnitin aprobado → visto bueno del docente sobre la vinculación como co-autor → envío a la revista.</p>
"""
pdf("guia", guia, SOP / "Guia_Turnitin_1pagina.pdf")

# ------------------------------------------------------------------ marcadores
marcador("lo emite Turnitin", "Certificado_Turnitin_EquipoNN.pdf",
         "Aquí va el reporte oficial de originalidad de Turnitin (similitud ≤ 20 %, objetivo ≤ 15 %).",
         SOP / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf")
marcador("lo emite la revista", "Constancia_Envio_Revista_EquipoNN.pdf",
         "Aquí va el acuse oficial del portal OJS de la Revista UIS Ingenierías, con radicado, fecha, título y autores.",
         SOP / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf")
marcador("escaneo del preprint manuscrito", "Preprint_Manuscrito_EquipoNN.pdf",
         "Aquí va el escaneo del borrador a mano que ya elaboró el equipo. No estaba en el repositorio y no se reconstruyó.",
         SOP / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf")

# ------------------------------------------------------------------ paquete de envío
AUT = [("Angel Quintana", "angel.quintana@upb.edu.co"), ("Andrés Negrete", "andres.negreten@upb.edu.co"),
       ("Antolin Vitola", "Antolin.vitola@upb.edu.co"), ("Juliana Esther Carrascal", "juliana.carrascal@upb.edu.co"),
       ("Alejandro Pemberty-Vergara", "alejandro.pemberty@upb.edu.co")]
meta = f"""# Metadatos para el formulario de OJS — Revista UIS Ingenierías

Preparado el {FECHA}. **No se ha enviado nada.** Los campos marcados [CONFIRMAR] los decide el equipo.

## Título
- Español: {TITULO}
- Inglés: {TITULO_EN}

## Resumen (español)
Copiar del artículo (párrafo «Resumen»). Menos de 400 palabras; sin citas ni fórmulas.

## Abstract
Copiar del artículo (párrafo «Abstract»).

## Palabras clave
- Español: reconocimiento de gestos; educación musical; primera infancia; MediaPipe; descriptor invariante; repaso espaciado; programación entera mixta; aprendizaje adaptativo; madurez tecnológica; Montería
- English: gesture recognition; music education; early childhood; MediaPipe; invariant descriptor; spaced repetition; mixed-integer programming; adaptive learning; technology readiness; Montería
- La guía para autores pide entre 10 y 15 por idioma; la plantilla recomienda de 5 a 10. Se usaron 10.

## Autores (orden por confirmar) [CONFIRMAR orden y autor de correspondencia]
""" + "\n".join(f"{i}. {n} — Universidad Pontificia Bolivariana, Seccional Montería, Colombia — {m} — ORCID: [CONFIRMAR]"
                 for i, (n, m) in enumerate(AUT, 1)) + f"""
{len(AUT) + 1}. **Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón** — Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia — cristian.cano@upb.edu.co — ORCID: [CONFIRMAR]

## Tipo de artículo
Investigación científica y tecnológica original.

## Declaraciones (ya incluidas en el artículo)
Contribución de autores (CRediT) [CONFIRMAR], financiación [CONFIRMAR], conflicto de intereses [CONFIRMAR], consentimiento informado (no aplica), junta de revisión (no aplica), disponibilidad de datos y código, uso de IA.

## Archivos
1. Artículo: Articulo_Maquetado_EquipoNN.pdf y .docx. Anonimización: la guía consultada no menciona revisión a ciegas; si el formulario de OJS la exige, retirar autores, filiaciones y el enlace del repositorio.
2. Carta de presentación y licencia de uso parcial (formato oficial en revista/carta_presentacion_licencia.docx): firmada por cada autor; la revista la pide después de la revisión inicial.
3. Figuras en alta resolución (300 dpi): articulo/fig/*.png
"""
(ENV / "metadatos_OJS.md").write_text(meta, encoding="utf-8")

d = docx.Document()
st = d.styles["Normal"]; st.font.name = "Verdana"; st.font.size = Pt(10)
for t in ["Montería, [fecha de envío]", "", "Comité Editorial", "Revista UIS Ingenierías — Universidad Industrial de Santander", "",
          "Asunto: Sometimiento del manuscrito «" + TITULO + "»", "", "Estimado Comité Editorial:", "",
          "Los autores someten a consideración de la Revista UIS Ingenierías el manuscrito titulado «" + TITULO + "», "
          "un artículo de investigación científica y tecnológica que describe y evalúa técnicamente, en laboratorio, "
          "un sistema de reconocimiento de señas manuales y de selección de sesiones para la enseñanza de notas musicales "
          "a niños. El trabajo se ajusta al alcance de la revista en ingeniería aplicada y ciencias de la decisión, "
          "porque formula y resuelve la selección de actividades como un problema de programación entera mixta y reporta "
          "mediciones reproducibles con intervalos de confianza.",
          "", "El manuscrito declara de forma explícita que no se realizaron pruebas con niños y estima un nivel de "
          "madurez tecnológica TRL 4. Los autores [CONFIRMAR: certifican que] el manuscrito es original, no ha sido "
          "publicado ni está en evaluación en otra revista, y que todos los autores aprobaron su envío. Se declara el uso "
          "de una herramienta de inteligencia artificial en la sección de declaraciones.",
          "", "Se adjuntan la carta de licencia de uso parcial firmada por cada autor y las figuras en alta resolución.",
          "", "Atentamente,", "", "[Nombre del autor de correspondencia — CONFIRMAR]", "En nombre de los autores: "
          + ", ".join(n for n, _ in AUT) + " y Cristian Javier Cano-Mogollón."]:
    d.add_paragraph(t)
d.save(str(ENV / "carta_presentacion_editor.docx"))

pasos = f"""# Pasos para radicar en la Revista UIS Ingenierías (hacer SOLO después del Turnitin y del visto bueno docente)

1. Confirmar en Publindex (aplicativo de MinCiencias) la categoría vigente de la revista y guardar la captura.
2. Con el Turnitin aprobado (≤ 20 %) y el visto bueno del docente sobre su vinculación, congelar la versión final del artículo.
3. Crear la cuenta de autor en https://revistas.uis.edu.co/index.php/revistauisingenierias (Registrarse). Usar el correo institucional del autor de correspondencia.
4. Entrar a «Enviar un artículo» (https://revistas.uis.edu.co/index.php/revistauisingenierias/about/submissions) y seguir los pasos de OJS: sección, requisitos, carga del archivo, metadatos (usar envio/metadatos_OJS.md), autores con filiación y comentarios al editor (carta).
5. Cargar el artículo en la plantilla de la revista y las figuras en alta resolución como material complementario.
6. Finalizar el envío. **Capturar como constancia**: el acuse en pantalla y el correo automático de la revista, que deben mostrar fecha, título, autores y código de radicado del envío.
7. Guardar la constancia como PDF con el nombre Constancia_Envio_Revista_EquipoNN.pdf y reemplazar el marcador PENDIENTE.
8. Después de la revisión inicial, la revista pedirá la carta de presentación y licencia firmada por cada autor.

Rúbrica: sin radicado no hay nota máxima; un correo de confirmación sin radicado equivale a «Bueno».
"""
(ENV / "pasos_radicacion.md").write_text(pasos, encoding="utf-8")

# ------------------------------------------------------------------ verificación de referencias
refs = json.loads((AQUI / "refs_crossref.json").read_text(encoding="utf-8"))
usados = {"10.1007/s10462-023-10637-7", "10.1007/s40745-026-00689-1", "10.7717/peerj-cs.3464", "10.1007/s44163-026-01115-4",
          "10.1038/s41598-026-53749-0", "10.1007/s44163-026-01858-0", "10.5216/mh.v26.85176", "10.1007/s11042-026-21667-y",
          "10.1007/s10791-026-10022-2", "10.1007/s44163-026-00832-0", "10.1016/j.eswa.2026.132088", "10.31681/jetol.1243501",
          "10.6018/red.602301", "10.17811/rifie.20620", "10.1037/0033-2909.132.3.354", "10.1007/BF01099821",
          "10.1038/s41467-019-12552-4", "10.1080/01621459.1927.10502953", "10.48550/arXiv.2006.10214", "10.55782/ane-1994-1003"}
with open(AQUI / "verificacion_referencias.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["doi_o_url", "titulo_en_la_fuente", "autores", "anio", "publicado_en", "fuente_de_verificacion",
                "estado", "fecha_consulta", "en_el_articulo", "nota"])
    for r in refs:
        w.writerow([r["doi"], r["titulo"], r["autores"], r["anio"], r["revista"], r["fuente"] + " API", r["estado"],
                    r["fecha_consulta"], "sí" if r["doi"] in usados else "no (se descartó)",
                    "Se verificó existencia y metadatos; el equipo debe leer el texto completo antes de afirmar más que lo que dice el título."
                    if r["doi"] in usados else "Verificada pero no usada."])
    w.writerow(["https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx",
                "Proyecciones de población municipal 2020-2035 (post COVID-19)", "DANE", "", "DANE", "HTTP HEAD 200",
                "VERIFICADO (archivo accesible)", "2026-11-05", "sí",
                "Cifras (Montería 2026: 535.052; 3 a 12 años: 80.254) leídas de la fila 23001 el 2026-10-01 (entregable_2do_corte/_fuentes/dane_monteria_2026.json); el archivo sigue accesible."])
print("soporte generado")
