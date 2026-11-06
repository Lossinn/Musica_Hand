"""Arma la carpeta individual de cada integrante: artículo, ESCRITO FINAL, soporte, envío, evidencia y ZIP.
Uso: python -X utf8 entrega_personal.py   (ejecuta antes art_*.py y prefiltro_similitud.py)"""
from __future__ import annotations

import html, json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor
from docx2pdf import convert

from contenido_personal import PERSONAS

AQUI = Path(__file__).resolve().parent
CASO = AQUI.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FECHA = "6 de noviembre de 2026"
ORIG = Path(r"C:\Users\Alejando\Desktop\Hand_Kid_Sing\musica_hand\entregables_last\analisis\generar_soporte.py").read_text(encoding="utf-8")
PREF = json.loads((AQUI / "prefiltro_similitud.json").read_text(encoding="utf-8"))
CSS = re.search(r'CSS = """(.*?)"""', ORIG, re.S).group(1)
ORDEN_ART = {"Muñoz": "roxana", "Alvarez": "camilo", "Guzmán": "andrea"}


def pdf_html(cuerpo: str, destino: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "d.html"
        h.write_text(f"<!doctype html><html lang='es'><head><meta charset='utf-8'>{CSS}</head><body>{cuerpo}</body></html>", encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={destino}", h.as_uri()],
                       check=True, capture_output=True, timeout=120)


def marcador(titulo, quien, detalle, destino):
    pdf_html(f"<div class='caja'><h1>PENDIENTE: {html.escape(titulo)}</h1><p><b>{html.escape(quien)}</b></p><p>{html.escape(detalle)}</p>"
             f"<p class='nota'>Marcador de posición generado el {FECHA}. No es un documento oficial ni tiene validez. Debe reemplazarse por el archivo real, "
             "con este mismo nombre, antes de subir el ZIP a Teams.</p></div>", destino)


def ficha_html(p, titulo):
    a = ORIG.index('ficha = f"""') + len('ficha = f"""')
    b = ORIG.index('"""\npdf("ficha"')
    t = eval('f"""' + ORIG[a:b] + '"""', {"FECHA": FECHA})
    t = t.replace("Equipo NN ·", f"{p['nombre']} · ")
    j0 = t.index("<h2>2. Justificación</h2>"); j1 = t.index("<h2>3. Candidatas descartadas</h2>")
    just = (f"<h2>2. Justificación</h2><p>El artículo «{html.escape(titulo)}» es un trabajo de ingeniería aplicada (diseño de un dispositivo, modelación y simulación) para agua de consumo rural. "
            "El alcance de la revista cubre ingeniería aplicada y ciencias de la decisión; no cobra por enviar ni publicar, acepta español, usa OJS y tiene plantilla Word oficial, "
            "lo que hace viable cumplir el plazo. La categoría B figura en su sitio vigente. Ajuste temático: <b>medio</b>, porque el alcance enumerado no menciona agua ni saneamiento; "
            "es una decisión de compromiso que el docente puede objetar.</p>")
    return t[:j0] + just + t[j1:]


def caja(doc, titulo, parrafos):
    """Marco «ESCRITO FINAL»: tabla de una celda con borde grueso."""
    t = doc.add_table(rows=1, cols=1); t.alignment = 1
    tblPr = t._tbl.tblPr; bd = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right"):
        x = OxmlElement(f"w:{lado}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "18"); x.set(qn("w:color"), "1F4E79"); bd.append(x)
    tblPr.append(bd)
    c = t.rows[0].cells[0]
    h = c.paragraphs[0]; r = h.add_run(titulo); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    for sub, txt in parrafos:
        if sub:
            q = c.add_paragraph(); rr = q.add_run(sub); rr.bold = True
        q = c.add_paragraph(txt); q.paragraph_format.space_after = Pt(4); q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.add_paragraph()


def escrito_final(p, art_txt: str, destino: Path):
    global doc
    doc = docx.Document()
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    doc.add_heading(f"ESCRITO FINAL — {p['nombre']}", 0)
    doc.add_paragraph(f"ID {p['id']} · {p['correo']} · Gestión Tecnológica, Corte 3 · UPB Seccional Montería · {FECHA}")
    q = doc.add_paragraph(); r = q.add_run("Tu hilo argumental: "); r.bold = True; q.add_run(p["hilo"])
    doc.add_paragraph("Cómo usar este documento: los tres recuadros «ESCRITO FINAL» son los textos que debes leer, entender y hacer tuyos. El recuadro 1 es el preprint para copiar a mano "
                      "(2 a 3 páginas, con tu letra); el 2 es el resumen que sube a la plataforma; el 3 es el texto del artículo maquetado. Los números salen de scripts reproducibles; "
                      "si cambias una cifra, cámbiala también en el artículo.")
    pp = p["preprint"]
    caja(doc, "ESCRITO FINAL 1 — Preprint para transcribir a mano (2 a 3 páginas)", [("Título", pp["titulo"])] + pp["secciones"])
    doc.add_paragraph("Dibuja a mano el diagrama PRISMA de la figura siguiente (cuatro fases: identificación, cribado, elegibilidad, inclusión) en la página 2 o 3 del manuscrito, con las mismas "
                      "cifras. Copia también las ecuaciones de la sección 3 con su definición de variables. Distribución sugerida: página 1, título, resumen y problema; página 2, PRISMA y búsqueda; "
                      "página 3, modelo, hallazgos y límites.")
    doc.add_picture(str(AQUI / "fig" / "prisma.png"), width=Cm(11))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    res = [l for l in art_txt.split("\n\n")]
    def bloque(estilo): return [re.sub(r"^\[[^\]]+\] ", "", x) for x in res if x.startswith(f"[{estilo}]")]
    # resumen y abstract: párrafo tras 'Resumen:' / 'Abstract:'
    idx = {x: i for i, x in enumerate(res)}
    def despues(rotulo):
        for i, x in enumerate(res):
            if x == f"[Subtitulos] {rotulo}": return re.sub(r"^\[[^\]]+\] ", "", res[i + 1])
    caja(doc, "ESCRITO FINAL 2 — Resumen y abstract (para la ficha, el formulario de la revista y la plataforma)",
         [("Resumen", despues("Resumen:")), ("Abstract", despues("Abstract:")), ("Palabras clave", despues("Palabras clave:")), ("Keywords", despues("Keywords:"))])
    cuerpo = []
    for x in res:
        m_ = re.match(r"^\[([^\]]+)\] (.*)$", x, re.S)
        if not m_: continue
        est, txt = m_.groups()
        if est in ("Título art", "Nombre autores") or (est == "Normal" and txt.startswith(("^{", "["))):
            continue
        if est.startswith("Heading"): cuerpo.append(("\n" + txt.upper() if est == "Heading 1" else "› " + txt, ""))
        elif est in ("Tabla Título", "Figura Título"): cuerpo.append(("", "[" + txt + "]"))
        elif est == "Subtitulos": cuerpo.append((txt, ""))
        else: cuerpo.append(("", re.sub(r"\^\{[^}]*\}", "", txt)))
    caja(doc, "ESCRITO FINAL 3 — Texto del artículo (las ecuaciones y figuras están en el artículo maquetado)", [c for c in cuerpo if c[0] or c[1]])
    doc.add_heading("Guion de defensa: 5 preguntas que te pueden hacer", 1)
    for qn_, ans in p["defensa"]:
        qq = doc.add_paragraph(); r = qq.add_run(qn_); r.bold = True
        doc.add_paragraph(ans)
    doc.save(str(destino))


def leeme(p, carpeta: Path, nart: int):
    prim = p["sufijo"]
    (carpeta / "00_LEEME.md").write_text(f"""# Entrega Corte 3 — {p['nombre']} ({p['id']})
Gestión Tecnológica · UPB Seccional Montería · generado el {FECHA}. Proyecto: clorificador pasivo de PVC para El Vidrial (Montería).

**Tu hilo:** {p['hilo']}

## Qué hay en esta carpeta
| Carpeta / archivo | Qué es | Estado |
|---|---|---|
| `01_ESCRITO_FINAL_{prim}.docx` (y `.md`) | Tres recuadros ESCRITO FINAL (preprint a mano, resumen, texto del artículo) + guion de defensa | Listo para leer y transcribir |
| `02_Articulo/Articulo_Maquetado_EquipoNN_{prim}.pdf` y `.docx` | Artículo en la plantilla oficial de la Revista UIS Ingenierías, tú como primera autora/autor, docente co-autor | Listo ({nart} páginas) |
| `03_Soporte/` | Ficha de la revista, guía de Turnitin de una página y marcadores PENDIENTE | Ficha lista; marcadores a reemplazar |
| `04_Envio/` | Metadatos OJS, carta al editor, pasos de radicación | Listo, **sin enviar** |
| `05_Evidencia/` | Resultados numéricos, búsqueda PRISMA, verificación de referencias, scripts y figuras | Reproducible |
| `06_Entrega_Teams/02_GT_Corte3_CierreProyecto_EquipoNN.zip` | ZIP de cinco archivos con los nombres de la rúbrica | Armado con **3 marcadores PENDIENTE** |

## Lo que NO puedo producir y debes conseguir tú
1. **Preprint manuscrito escaneado** (`Preprint_Manuscrito_EquipoNN.pdf`): copia a mano el recuadro ESCRITO FINAL 1 (con el diagrama PRISMA dibujado) y escanéalo.
2. **Certificado de Turnitin** (≤ 20 %): lo emite Turnitin. Sube el PDF del artículo (ver `03_Soporte/Guia_Turnitin_1pagina.pdf`).
3. **Constancia de envío** a la revista: la emite el portal OJS; antes necesitas el Turnitin y el visto bueno del docente.
Sustituye cada marcador por el archivo real con el mismo nombre y vuelve a comprimir (o corre `empaquetar` según `04_Envio/pasos_radicacion.md`).

## Datos que debes completar o confirmar con el equipo
- Número de equipo (NN) y orden definitivo de autores (en tu versión apareces primera/o; las otras dos versiones ordenan distinto).
- ORCID de todos, roles CRediT, financiación y conflicto de intereses (están marcados «por confirmar»).
- Categoría vigente de la revista en Publindex (captura): la categoría B viene del sitio de la revista.
- Leer el texto completo de los 13 estudios incluidos en la búsqueda: solo se leyeron título y resumen.
- Código de asignatura: 8830 0064 0 (2.º corte) vs 8830 0048 0 (Corte 3).

## Qué tiene de diferente tu versión
Los tres artículos comparten los mismos datos, la misma búsqueda PRISMA (328 → 13 + 10 fuentes) y las mismas 23 referencias verificadas en Crossref, pero cada uno defiende una tesis distinta, usa tablas y figuras propias, y redacta de forma independiente. Prefiltro de coincidencia textual entre los tres artículos: {', '.join(f'{k}: {v["pct_de_a"]} %' for k, v in PREF['entre_articulos'].items())} (no sustituye a Turnitin).

## Advertencias honestas
- No hay mediciones validadas: las distribuciones de la simulación son supuestos del equipo. TRL 3.
- Con esos supuestos, solo 1,0 % de los escenarios queda en 0,2–0,5 mg/L. Es un hallazgo, no un error del script (reproduce el cuaderno con diferencia 0).
- Diez registros de septiembre de 2026 en `Formato_Captura_Datos_Ensayos.csv` tienen procedencia sin confirmar: no se usan como resultado. Si son mediciones reales, díselo al equipo: cambiaría el artículo.
- Las referencias Lantagne (2008) y Amrose (2015) del archivo `Referencias_APA` del proyecto tienen DOI o título incorrectos; no se usaron. Amrose et al. 2015 se citó con su DOI correcto (10.1146/annurev-environ-031411-091819, «Safe Drinking Water for Low-Income Regions»).
- El ROI de 361,2 % y el payback de 3,32 meses del 2.º corte no se usan: dependen de 60 familias y 44,5 millones COP de beneficios sin respaldo medido.
""", encoding="utf-8")


def main():
    for clave, p in PERSONAS.items():
        carpeta = CASO / p["carpeta"]
        for sub in ("02_Articulo", "03_Soporte", "04_Envio", "05_Evidencia", "06_Entrega_Teams"):
            (carpeta / sub).mkdir(parents=True, exist_ok=True)
        prim = p["sufijo"]
        # artículo
        docx_path = carpeta / "02_Articulo" / f"Articulo_Maquetado_EquipoNN_{prim}.docx"
        subprocess.run([sys.executable, "-X", "utf8", str(AQUI / f"{p['art']}.py"), str(docx_path)], check=True, cwd=AQUI, capture_output=True)
        convert(str(docx_path), str(docx_path.with_suffix(".pdf")))
        import pymupdf
        nart = len(pymupdf.open(str(docx_path.with_suffix(".pdf"))))
        art_txt = docx_path.with_suffix(".txt").read_text(encoding="utf-8")
        shutil.move(str(docx_path.with_suffix(".txt")), str(carpeta / "05_Evidencia" / f"texto_articulo_{prim}.txt"))
        art_txt_ = (carpeta / "05_Evidencia" / f"texto_articulo_{prim}.txt").read_text(encoding="utf-8")
        # título
        titulo = next(x for x in art_txt_.split("\n\n") if x.startswith("[Título art]"))[len("[Título art] "):]
        # soporte
        sop = carpeta / "03_Soporte"
        pdf_html(ficha_html(p, titulo), sop / "Ficha_Revista_Indexada_EquipoNN.pdf")
        g = re.search(r'guia = f"""(.*?)"""\npdf\("guia"', ORIG, re.S).group(1)
        g = eval('f"""' + g + '"""', {"FECHA": FECHA})
        g = re.sub(r"<li>El filtro previo del equipo.*?</li>", "<li>El filtro previo (<i>prefiltro_similitud.py</i>) midió coincidencia menor de 7 % entre los tres artículos del equipo y menor de 0,2 % con los documentos del proyecto (PI-I, 2.º corte, fichas). No sustituye a Turnitin: no ve internet ni su base.</li>", g, flags=re.S)
        g = g.replace("<li>Si el documento del 2.º corte o el repositorio ya se subieron a Turnitin, aparecerán como fuente; avisar al docente.</li>",
                      "<li>Si el documento del 2.º corte, el PI-I o los artículos de las otras dos integrantes ya se subieron a Turnitin, aparecerán como fuente; avisar al docente. Suban cada versión por separado y no compartan borradores.</li>")
        pdf_html(g, sop / "Guia_Turnitin_1pagina.pdf")
        marcador("lo emite Turnitin", "Certificado_Turnitin_EquipoNN.pdf", "Aquí va el reporte oficial de originalidad de Turnitin (similitud ≤ 20 %, objetivo ≤ 15 %).", sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf")
        marcador("lo emite la revista", "Constancia_Envio_Revista_EquipoNN.pdf", "Aquí va el acuse oficial del portal OJS de la Revista UIS Ingenierías, con radicado, fecha, título y autores.", sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf")
        marcador("escaneo del preprint manuscrito", "Preprint_Manuscrito_EquipoNN.pdf", "Aquí va el escaneo de tu borrador a mano (2 a 3 páginas, con diagrama PRISMA). Está redactado en 01_ESCRITO_FINAL; debes copiarlo con tu letra.", sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf")
        # envío
        env = carpeta / "04_Envio"
        orden = [clave] + [k for k in PERSONAS if k != clave]
        autores = [(PERSONAS[k]["nombre"], PERSONAS[k]["correo"]) for k in orden]
        res_es = next(x for x in art_txt_.split("\n\n") if x.startswith("[Normal]") and "Se concluye" in x or ("concluye" in x and x.startswith("[Normal]"))) if False else None
        kw = art_txt_.split("[Subtitulos] Palabras clave:\n\n[Normal] ")[1].split("\n\n")[0]
        kwe = art_txt_.split("[Subtitulos] Keywords:\n\n[Normal] ")[1].split("\n\n")[0]
        titulo_en = [x for x in art_txt_.split("\n\n") if x.startswith("[Título art]")][1][len("[Título art] "):]
        (env / "metadatos_OJS.md").write_text(f"""# Metadatos para el formulario de OJS — Revista UIS Ingenierías
Preparado el {FECHA}. **No se ha enviado nada.** Los campos [CONFIRMAR] los decide el equipo.

## Título
- Español: {titulo}
- Inglés: {titulo_en}

## Resumen y abstract
Copiar de `01_ESCRITO_FINAL_{prim}` (recuadro 2). Menos de 400 palabras; sin citas ni fórmulas.

## Palabras clave
- Español: {kw}
- English: {kwe}

## Autores [CONFIRMAR orden y autor de correspondencia]
""" + "\n".join(f"{i}. {n} — Universidad Pontificia Bolivariana, Seccional Montería, Colombia — {m_} — ORCID: [CONFIRMAR]" for i, (n, m_) in enumerate(autores, 1)) + f"""
{len(autores) + 1}. **Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón** — Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia — cristian.cano@upb.edu.co — ORCID: [CONFIRMAR]

## Tipo de artículo
Investigación científica y tecnológica original.

## Archivos
1. Artículo: `Articulo_Maquetado_EquipoNN_{prim}.pdf` y `.docx`.
2. Carta de presentación y licencia firmada por cada autor (formato oficial de la revista; se pide tras la revisión inicial).
3. Figuras en alta resolución (300 dpi), en `05_Evidencia/fig/`.
""", encoding="utf-8")
        d = docx.Document(); d.styles["Normal"].font.name = "Verdana"; d.styles["Normal"].font.size = Pt(10)
        for t in ["Montería, [fecha de envío]", "", "Comité Editorial", "Revista UIS Ingenierías — Universidad Industrial de Santander", "", f"Asunto: Sometimiento del manuscrito «{titulo}»", "",
                  "Estimado Comité Editorial:", "",
                  f"Los autores someten a su consideración el manuscrito «{titulo}», un artículo de investigación científica y tecnológica sobre el diseño y el análisis de un clorificador pasivo de PVC "
                  "para agua de consumo en una comunidad rural de Montería, Córdoba. El trabajo se ajusta al alcance de la revista en ingeniería aplicada y ciencias de la decisión, porque formula "
                  "un balance de masa, una simulación y un diseño experimental, y reporta resultados reproducibles con intervalos de confianza.",
                  "", "El manuscrito declara de forma explícita que no incluye validación experimental y estima un nivel de madurez tecnológica TRL 3. Los autores [CONFIRMAR: certifican que] el manuscrito "
                  "es original, no ha sido publicado ni está en evaluación en otra revista, y que todos aprobaron su envío. El uso de una herramienta de inteligencia artificial se declara en el texto.",
                  "", "Se adjuntan la carta de licencia de uso parcial firmada por cada autor y las figuras en alta resolución.", "", "Atentamente,", "", f"[{p['nombre']} — autor(a) de correspondencia, CONFIRMAR]",
                  "En nombre de los autores: " + ", ".join(n for n, _ in autores) + " y Cristian Javier Cano-Mogollón."]:
            d.add_paragraph(t)
        d.save(str(env / "carta_presentacion_editor.docx"))
        pasos = re.search(r'pasos = f"""(.*?)"""\n\(ENV', ORIG, re.S).group(1)
        (env / "pasos_radicacion.md").write_text(eval('f"""' + pasos + '"""', {"FECHA": FECHA}), encoding="utf-8")
        # evidencia
        ev = carpeta / "05_Evidencia"; (ev / "fig").mkdir(exist_ok=True)
        for f_ in ("resultados_estudio.json", "resultados_complemento.json", "prisma_cifras.json", "busqueda_prisma.json", "abstracts_seleccion.json", "verificacion_referencias.csv",
                   "refs_crossref.json", "prefiltro_similitud.json", "DOE_hoja_aleatorizacion.csv", "estudio_clorificador.py", "complemento.py", "busqueda_prisma.py", "verificar_refs.py", "prefiltro_similitud.py"):
            shutil.copy2(AQUI / f_, ev / f_)
        for f_ in (AQUI / "fig").glob("*.png"):
            shutil.copy2(f_, ev / "fig" / f_.name)
        # escrito final
        ef = carpeta / f"01_ESCRITO_FINAL_{prim}.docx"
        escrito_final(p, art_txt_, ef)
        # md del escrito final
        md = [f"# ESCRITO FINAL — {p['nombre']}\n", f"**Tu hilo:** {p['hilo']}\n", "\n---\n## ESCRITO FINAL 1 — Preprint para transcribir a mano\n", f"**{p['preprint']['titulo']}**\n"]
        for s_, t_ in p["preprint"]["secciones"]:
            md.append(f"\n**{s_}.** {t_}\n")
        md.append("\n---\n## ESCRITO FINAL 2 — Resumen y abstract\n\n(ver recuadro 2 en el .docx)\n\n---\n## ESCRITO FINAL 3 — Texto del artículo\n\n" + re.sub(r"\n\n\[(Heading 1)\] ", "\n\n# ", re.sub(r"\n\n\[(Heading 2)\] ", "\n\n## ", art_txt_)).replace("[Normal] ", "").replace("[Subtitulos] ", "**").replace("[Tabla Título] ", "*").replace("[Figura Título] ", "*"))
        md.append("\n\n---\n## Guion de defensa\n")
        for q_, a_ in p["defensa"]:
            md.append(f"\n**{q_}**  \n{a_}\n")
        (carpeta / f"01_ESCRITO_FINAL_{prim}.md").write_text("".join(md), encoding="utf-8")
        # ZIP
        z = carpeta / "06_Entrega_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf", "Preprint_Manuscrito_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf", "Certificado_Turnitin_EquipoNN.pdf")
            zf.write(sop / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
            zf.write(docx_path.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf", "Constancia_Envio_Revista_EquipoNN.pdf")
        leeme(p, carpeta, nart)
        print(clave, "OK", carpeta.name, nart, "págs")


main()
