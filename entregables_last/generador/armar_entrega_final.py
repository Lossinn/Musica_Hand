"""Arma la entrega final del equipo: artículo único, preprint, soporte, envío, evidencia y ZIP.
Uso: python -X utf8 armar_entrega_final.py"""
import html, json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
import docx
import pymupdf
from docx.shared import Pt
from docx2pdf import convert

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
OUT = BASE / "ENTREGA_FINAL"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FECHA = "6 de noviembre de 2026"
ORIG = (BASE / "analisis" / "generar_soporte.py").read_text(encoding="utf-8")
CSS = re.search(r'CSS = """(.*?)"""', ORIG, re.S).group(1)
PREF = json.loads((AQUI / "out" / "prefiltro_unico.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(AQUI))
import nucleo_hsk as NH

AUT = [NH.EQUIPO[k] for k in ("Vitola", "Petro", "Negrete", "Carrascal", "Quintana", "Pemberty", "Guerra")]


def pdf_html(cuerpo, destino):
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "d.html"
        h.write_text(f"<!doctype html><html lang='es'><head><meta charset='utf-8'>{CSS}</head><body>{cuerpo}</body></html>", encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={destino}", h.as_uri()], check=True, capture_output=True, timeout=120)


def marcador(titulo, quien, detalle, destino):
    pdf_html(f"<div class='caja'><h1>PENDIENTE: {html.escape(titulo)}</h1><p><b>{html.escape(quien)}</b></p><p>{html.escape(detalle)}</p>"
             f"<p class='nota'>Marcador de posición generado el {FECHA}. No es un documento oficial ni tiene validez. Debe reemplazarse por el archivo real, con este mismo nombre, antes de subir el ZIP a Teams.</p></div>", destino)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for sub in ("1_Articulo", "2_Preprint", "3_Soporte", "4_Envio", "5_Evidencia", "6_ZIP_para_Teams"):
        (OUT / sub).mkdir(parents=True)
    # ---------------- artículo único
    docx_path = OUT / "1_Articulo" / "Articulo_Maquetado_EquipoNN.docx"
    r = subprocess.run([sys.executable, "-X", "utf8", str(AQUI / "art_unico.py"), str(docx_path)], cwd=AQUI, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    convert(str(docx_path), str(docx_path.with_suffix(".pdf")))
    npag = len(pymupdf.open(str(docx_path.with_suffix(".pdf"))))
    txt = docx_path.with_suffix(".txt").read_text(encoding="utf-8"); docx_path.with_suffix(".txt").unlink()
    bloques = txt.split("\n\n")
    titulo = next(x for x in bloques if x.startswith("[Título art]"))[len("[Título art] "):]
    titulo_en = [x for x in bloques if x.startswith("[Título art]")][1][len("[Título art] "):]
    def despues(rot):
        for i, x in enumerate(bloques):
            if x == f"[Subtitulos] {rot}":
                return re.sub(r"^\[[^\]]+\] ", "", bloques[i + 1])
    resumen, kw, abstract, kwe = despues("Resumen:"), despues("Palabras clave:"), despues("Abstract:"), despues("Keywords:")
    # ---------------- preprint
    pre = OUT / "2_Preprint"
    pe = pre / "Preprint_del_equipo_para_copiar_a_mano.docx"
    subprocess.run([sys.executable, "-X", "utf8", str(AQUI / "preprint_equipo.py"), str(pe)], cwd=AQUI, check=True, capture_output=True)
    ind = pre / "preprints_individuales"; ind.mkdir()
    for f in (BASE / "pre_print" / "originales").glob("*.pdf"):
        shutil.copy2(f, ind / f.name)
    for f in (BASE / "pre_print" / "nuevos").glob("*.md"):
        shutil.copy2(f, ind / f.name)
    # ---------------- soporte
    sop = OUT / "3_Soporte"
    a = ORIG.index('ficha = f"""') + len('ficha = f"""'); b = ORIG.index('"""\npdf("ficha"')
    ficha = eval('f"""' + ORIG[a:b] + '"""', {"FECHA": FECHA})
    pdf_html(ficha, sop / "Ficha_Revista_Indexada_EquipoNN.pdf")
    g = eval('f"""' + re.search(r'guia = f"""(.*?)"""\npdf\("guia"', ORIG, re.S).group(1) + '"""', {"FECHA": FECHA})
    cf = PREF["contra_fuentes"]
    g = re.sub(r"<li>El filtro previo del equipo.*?</li>", f"<li>El filtro previo del equipo (<i>prefiltro_equipo.py</i>) midió {cf['documento_tecnico.md']['unico']['pct']:.1f} % de coincidencia con el documento técnico del proyecto (tramo continuo máximo de {cf['documento_tecnico.md']['unico']['tramo_max']} palabras), "
               f"{cf['documento_2do_corte (html)']['unico']['pct']:.1f} % con el documento del 2.º corte y 0 % con el README. No sustituye a Turnitin: no ve internet ni su base.</li>", g, flags=re.S)
    g = g.replace("<li>Si el documento del 2.º corte o el repositorio ya se subieron a Turnitin, aparecerán como fuente; avisar al docente.</li>",
                  "<li>Si el documento técnico, el del 2.º corte o un borrador anterior ya se subieron a Turnitin, aparecerán como fuente; avisar al docente. Subir una sola versión final y no reutilizar borradores.</li>")
    pdf_html(g, sop / "Guia_Turnitin_1pagina.pdf")
    marcador("escaneo del preprint manuscrito", "Preprint_Manuscrito_EquipoNN.pdf", "Aquí va el escaneo del borrador a mano (2 a 3 páginas, con el diagrama PRISMA dibujado). El texto para copiar está en 2_Preprint.", sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf")
    marcador("lo emite Turnitin", "Certificado_Turnitin_EquipoNN.pdf", "Aquí va el reporte oficial de originalidad de Turnitin (similitud ≤ 20 %, objetivo ≤ 15 %).", sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf")
    marcador("lo emite la revista", "Constancia_Envio_Revista_EquipoNN.pdf", "Aquí va el acuse oficial del portal OJS de la Revista UIS Ingenierías, con radicado, fecha, título y autores.", sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf")
    # ---------------- envío
    env = OUT / "4_Envio"
    (env / "metadatos_OJS.md").write_text(f"""# Metadatos para el formulario de OJS — Revista UIS Ingenierías
Preparado el {FECHA}. **No se ha enviado nada.** Los campos [CONFIRMAR] los decide el equipo.

## Título
- Español: {titulo}
- Inglés: {titulo_en}

## Resumen
{resumen}

## Abstract
{abstract}

## Palabras clave
- Español: {kw}
- English: {kwe}

## Autores [CONFIRMAR orden definitivo y autor de correspondencia]
""" + "\n".join(f"{i}. {n} — Universidad Pontificia Bolivariana, Seccional Montería, Colombia — {m} — ID {idn} — ORCID: [CONFIRMAR]" for i, (n, m, idn) in enumerate(AUT, 1)) + f"""
{len(AUT) + 1}. **Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón** — Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia — cristian.cano@upb.edu.co — ORCID: [CONFIRMAR]

Autor de correspondencia propuesto: Alejandro Pemberty-Vergara [CONFIRMAR].

## Tipo de artículo
Investigación científica y tecnológica original.

## Archivos
1. Artículo: `Articulo_Maquetado_EquipoNN.pdf` y `.docx` ({npag} páginas).
2. Carta de presentación y licencia firmada por cada autor (formato oficial; la revista la pide tras la revisión inicial).
3. Figuras en alta resolución (300 dpi), en `5_Evidencia/fig/`.
""", encoding="utf-8")
    d = docx.Document(); d.styles["Normal"].font.name = "Verdana"; d.styles["Normal"].font.size = Pt(10)
    for t in ["Montería, [fecha de envío]", "", "Comité Editorial", "Revista UIS Ingenierías — Universidad Industrial de Santander", "", f"Asunto: Sometimiento del manuscrito «{titulo}»", "", "Estimado Comité Editorial:", "",
              f"Los autores someten a su consideración el manuscrito «{titulo}», un artículo de investigación científica y tecnológica que describe y evalúa técnicamente, en laboratorio, un sistema de enseñanza de notas musicales a niños mediante señas manuales: "
              "su reconocedor, su modelo de aprendizaje y su selección de actividades por optimización. El trabajo se ajusta al alcance de la revista en ingeniería aplicada y ciencias de la decisión, y reporta resultados reproducibles con intervalos de confianza.",
              "", "El manuscrito declara de forma explícita que no se hicieron pruebas con niños y estima un nivel de madurez tecnológica TRL 4. Los autores [CONFIRMAR: certifican que] el manuscrito es original, no ha sido publicado ni está en evaluación en otra revista, "
              "y que todos aprobaron su envío. El uso de una herramienta de inteligencia artificial se declara en el texto.", "", "Se adjuntan la carta de licencia de uso parcial firmada por cada autor y las figuras en alta resolución.", "", "Atentamente,", "",
              "[Autor de correspondencia, CONFIRMAR]", "En nombre de los autores: " + ", ".join(a[0] for a in AUT) + " y Cristian Javier Cano-Mogollón."]:
        d.add_paragraph(t)
    d.save(str(env / "carta_presentacion_editor.docx"))
    pasos = re.search(r'pasos = f"""(.*?)"""\n\(ENV', ORIG, re.S).group(1)
    (env / "pasos_radicacion.md").write_text(eval('f"""' + pasos + '"""', {"FECHA": FECHA}), encoding="utf-8")
    # ---------------- evidencia
    ev = OUT / "5_Evidencia"; (ev / "fig").mkdir()
    for f_ in ("resultados_vision.json", "sensibilidad_umbrales.json", "salida_pruebas.txt", "refs_crossref.json", "verificacion_referencias.csv", "evidencia_vision.py", "sensibilidad_umbrales.py", "verificar_refs.py"):
        shutil.copy2(BASE / "analisis" / f_, ev / f_)
    for f_ in ("quintana_demo.py", "quintana_demo.json", "prefiltro_equipo.py"):
        shutil.copy2(AQUI / f_, ev / f_)
    shutil.copy2(AQUI / "out" / "prefiltro_unico.json", ev / "prefiltro_similitud.json")
    for f_ in ("prisma_hsk.png", "arquitectura.png", "capturas_app.png", "aciertos.png", "falsos_positivos.png", "matriz_similitud.png", "umbral_confianza.png", "ventana_tempo.png", "dominio_retencion.png"):
        shutil.copy2(BASE / "articulo" / "fig" / f_, ev / "fig" / f_)
    corp = BASE.parent / "04_Datos" / "bibliometria" / "resultados"
    for f_ in ("informe_bibliometrico_corpus.md", "03_relacion_proyecto.csv"):
        shutil.copy2(corp / f_, ev / f_)
    shutil.copy2(BASE.parent / "07_Ecuaciones_booleanas" / "Scopus" / "ecuaciones_scopus.md", ev / "ecuaciones_scopus.md")
    json.dump({"identificados": 226, "duplicados": 37, "unicos": 189, "marginales_excluidos": 41, "evaluados": 148, "metodo_contexto_excluidos": 61, "incluidos": 87, "nucleo": 22,
               "nota": "Conteo de resultados de cada ecuación en Scopus: no registrado. Muestra de conveniencia."}, open(ev / "prisma_cifras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ---------------- ZIP
    z = OUT / "6_ZIP_para_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf", "Preprint_Manuscrito_EquipoNN.pdf")
        zf.write(sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf", "Certificado_Turnitin_EquipoNN.pdf")
        zf.write(sop / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
        zf.write(docx_path.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
        zf.write(sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf", "Constancia_Envio_Revista_EquipoNN.pdf")
    print("ENTREGA_FINAL lista:", npag, "páginas;", [i.filename for i in zipfile.ZipFile(z).infolist()])


main()
