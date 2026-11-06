"""Arma la carpeta de entrega de cada integrante (preprint, ESCRITO FINAL, artículo, soporte, envío, ZIP, LEEME).
Uso: python -X utf8 construir_entregas.py"""
from __future__ import annotations

import html, json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

import docx
import pymupdf
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor
from docx2pdf import convert

from datos_personas import PERSONAS

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
OUT = BASE / "entregas_por_integrante"
PRE = BASE / "pre_print"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FECHA = "6 de noviembre de 2026"
ORIG = (BASE / "analisis" / "generar_soporte.py").read_text(encoding="utf-8")
CSS = re.search(r'CSS = """(.*?)"""', ORIG, re.S).group(1)
EQUIPO_ORDEN = ["Vitola", "Petro", "Negrete", "Carrascal", "Quintana", "Pemberty", "Guerra"]
sys.path.insert(0, str(AQUI))
import nucleo_hsk as NH   # solo para EQUIPO (nombres y correos)
PREF = json.loads((AQUI / "out" / "prefiltro.json").read_text(encoding="utf-8")) if (AQUI / "out" / "prefiltro.json").exists() else {}
PREF_EF = json.loads((AQUI / "out" / "prefiltro_ef.json").read_text(encoding="utf-8")) if (AQUI / "out" / "prefiltro_ef.json").exists() else {}


# ------------------------------------------------------------------ utilidades
def pdf_html(cuerpo: str, destino: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "d.html"
        h.write_text(f"<!doctype html><html lang='es'><head><meta charset='utf-8'>{CSS}</head><body>{cuerpo}</body></html>", encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={destino}", h.as_uri()], check=True, capture_output=True, timeout=120)


def marcador(titulo, quien, detalle, destino):
    pdf_html(f"<div class='caja'><h1>PENDIENTE: {html.escape(titulo)}</h1><p><b>{html.escape(quien)}</b></p><p>{html.escape(detalle)}</p>"
             f"<p class='nota'>Marcador de posición generado el {FECHA}. No es un documento oficial ni tiene validez. Debe reemplazarse por el archivo real, con este mismo nombre, antes de subir el ZIP a Teams.</p></div>", destino)


def runs_md(par, texto, size=None):
    for parte in re.split(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*)", texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            r = par.add_run(parte[2:-2]); r.bold = True
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            r = par.add_run(parte[1:-1]); r.italic = True
        else:
            r = par.add_run(parte)
        if size:
            r.font.size = Pt(size)


def caja(doc, titulo, parrafos):
    """Marco «ESCRITO FINAL»: tabla de una celda con borde grueso. parrafos: lista de (rótulo, texto) con markdown ligero."""
    t = doc.add_table(rows=1, cols=1); t.alignment = 1
    bd = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right"):
        x = OxmlElement(f"w:{lado}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "18"); x.set(qn("w:color"), "1F4E79"); bd.append(x)
    t._tbl.tblPr.append(bd)
    c = t.rows[0].cells[0]
    h = c.paragraphs[0]; r = h.add_run(titulo); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    for sub, txt in parrafos:
        if sub:
            q = c.add_paragraph(); rr = q.add_run(sub); rr.bold = True
        if txt:
            q = c.add_paragraph(); runs_md(q, txt); q.paragraph_format.space_after = Pt(4); q.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.add_paragraph()


def leer_preprint_md(nombre: str):
    s = (PRE / "nuevos" / nombre).read_text(encoding="utf-8")
    cuerpo = s.split("## ESCRITO FINAL (para copiar a mano)")[1].split("\n---\n")[0]
    return [p.strip() for p in cuerpo.strip().split("\n\n") if p.strip()]


def ficha_html(p, titulo):
    a = ORIG.index('ficha = f"""') + len('ficha = f"""'); b = ORIG.index('"""\npdf("ficha"')
    t = eval('f"""' + ORIG[a:b] + '"""', {"FECHA": FECHA})
    return t.replace("Equipo NN ·", f"{p['nombre']} · ")


# ------------------------------------------------------------------ preprint formal (nuevos)
def preprint_formal(p, destino: Path):
    d = docx.Document(); st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(12)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    d.add_heading(f"Preprint para transcribir a mano — {p['nombre']}", 1)
    q = d.add_paragraph(); runs_md(q, "**Instrucciones.** Copia el recuadro con tu letra, en 2 a 3 páginas (hojas de examen o cuaderno). Léelo antes para entenderlo; puedes ajustar palabras, pero no cambies las cifras. "
                                      "Luego escanea el manuscrito en PDF nítido y guárdalo como **Preprint_Manuscrito_EquipoNN.pdf**.", 10)
    caja(d, "ESCRITO FINAL — PREPRINT", [("", par) for par in leer_preprint_md(p["preprint"]["md"])])
    d.add_heading("Guía de páginas", 2)
    d.add_paragraph("Página 1: título, encabezado y resumen o introducción. Página 2: desarrollo (métodos o modelo, con las ecuaciones y la definición de las variables). Página 3: resultados, discusión, límites y referencia.")
    d.add_paragraph("Diagrama PRISMA: si el docente lo exige en el manuscrito, usa el de `_Evidencia_compartida`, o dibuja uno con tus propias cifras de búsqueda. Este proyecto no tiene cifras PRISMA verificadas: no las inventes.")
    d.save(str(destino))


def preprint_existente(p, carpeta: Path):
    src = PRE / "originales" / p["preprint"]["scan"]
    if not src.exists():
        src = next(f for f in (PRE / "originales").glob("*.pdf") if f.name.split()[0] == p["preprint"]["scan"].split()[0] and "gr" not in f.name[:2].lower() or f.name[:4] == p["preprint"]["scan"][:4])
    dst = carpeta / "01_Preprint" / f"Preprint_Manuscrito_EquipoNN_{p['corto'].split()[-1]}.pdf"
    shutil.copy2(src, dst)
    d = docx.Document(); d.styles["Normal"].font.name = "Calibri"; d.styles["Normal"].font.size = Pt(11)
    d.add_heading(f"Transcripción de tu preprint — {p['nombre']}", 1)
    q = d.add_paragraph()
    runs_md(q, "El escaneo manuscrito original se conserva sin cambios (`" + dst.name + "`). Esta transcripción es para que lo estudies"
            + (" y es **aproximada**: la letra era difícil de leer, compárala con el original." if p["preprint"]["aprox"] else ". Compárala con el original ante cualquier duda."), 10)
    caja(d, "ESCRITO FINAL — TU PREPRINT (transcripción)", [("", x) for x in p["preprint"]["trans"].split("\n\n")])
    d.save(str(carpeta / "01_Preprint" / f"Transcripcion_preprint_{p['corto'].split()[-1]}.docx"))
    return dst


# ------------------------------------------------------------------ ESCRITO FINAL completo
def guia_estudio(p, meta: dict, carpeta: Path):
    ap = p["corto"].split()[-1]
    doc = docx.Document(); doc.styles["Normal"].font.name = "Calibri"; doc.styles["Normal"].font.size = Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    doc.add_heading(f"Guía de estudio y defensa — {p['nombre']}", 0)
    ident = NH.EQUIPO[[k for k, v in PERSONAS.items() if v is p][0]]
    doc.add_paragraph(f"ID {ident[2]} · {ident[1]} · Gestión Tecnológica, Corte 3 · UPB Seccional Montería · {FECHA}")
    q = doc.add_paragraph(); r = q.add_run("Tu hilo argumental: "); r.bold = True; q.add_run(p["hilo"])
    q = doc.add_paragraph(); r = q.add_run("Cómo conecta tu preprint con tu escrito final: "); r.bold = True; q.add_run(p["conecta"])
    doc.add_paragraph("Cómo usar esta guía: los recuadros «ESCRITO FINAL» son los textos que debes leer, entender y hacer tuyos. El 1 es tu preprint; el 2 es el resumen y el abstract de tu escrito final, que es el artículo "
                      "de proyecto final de la carpeta `02_ESCRITO_FINAL`. Las cifras salen de scripts reproducibles; si cambias una, cámbiala en todos los documentos.")
    pp = p["preprint"]
    if pp["modo"] == "nuevo":
        caja(doc, "ESCRITO FINAL 1 — Preprint para transcribir a mano (2 a 3 páginas)", [("", x) for x in leer_preprint_md(pp["md"])])
    else:
        caja(doc, "ESCRITO FINAL 1 — Tu preprint (ya escrito a mano; transcripción" + (" aproximada" if pp["aprox"] else "") + ")", [("", x) for x in pp["trans"].split("\n\n")])
    caja(doc, "ESCRITO FINAL 2 — Resumen y abstract del artículo de proyecto final",
         [("Título", meta["titulo"]), ("Resumen", meta["resumen"]), ("Palabras clave", meta["kw"]), ("Abstract", meta["abstract"]), ("Keywords", meta["kwe"])])
    doc.add_heading("Avisos para ti", 1)
    for n_ in p["notas"]:
        q = doc.add_paragraph(style="List Bullet"); runs_md(q, n_)
    doc.add_heading("Guion de defensa: 5 preguntas que te pueden hacer", 1)
    for qn_, ans in p["defensa"]:
        qq = doc.add_paragraph(); r = qq.add_run(qn_); r.bold = True
        doc.add_paragraph(ans)
    doc.save(str(carpeta / "03_Guia_de_estudio" / f"Guia_de_estudio_{ap}.docx"))
    md = [f"# Guía de estudio y defensa — {p['nombre']}\n\n**Tu hilo:** {p['hilo']}\n\n**Preprint y escrito final:** {p['conecta']}\n\n---\n## ESCRITO FINAL 1 — Preprint\n\n"]
    md.append("\n\n".join(leer_preprint_md(pp["md"])) if pp["modo"] == "nuevo" else pp["trans"])
    md.append(f"\n\n---\n## ESCRITO FINAL 2 — Resumen y abstract\n\n**{meta['titulo']}**\n\n**Resumen.** {meta['resumen']}\n\n**Palabras clave:** {meta['kw']}\n\n**Abstract.** {meta['abstract']}\n\n**Keywords:** {meta['kwe']}\n")
    md.append("\n---\n## Avisos\n\n" + "\n".join("- " + n_ for n_ in p["notas"]) + "\n\n## Guion de defensa\n")
    for q_, a_ in p["defensa"]:
        md.append(f"\n**{q_}**  \n{a_}\n")
    (carpeta / "03_Guia_de_estudio" / f"Guia_de_estudio_{ap}.md").write_text("".join(md), encoding="utf-8")


# ------------------------------------------------------------------ envío
def envio(p, clave, titulo, titulo_en, kw, kwe, carpeta: Path, ap):
    env = carpeta / "05_Envio"
    orden = [clave] + [k for k in EQUIPO_ORDEN if k != clave]
    autores = [NH.EQUIPO[k] for k in orden]
    (env / "metadatos_OJS.md").write_text(f"""# Metadatos para el formulario de OJS — Revista UIS Ingenierías
Preparado el {FECHA}. **No se ha enviado nada.** Los campos [CONFIRMAR] los decide el equipo.

## Título
- Español: {titulo}
- Inglés: {titulo_en}

## Resumen y abstract
Copiar de `02_ESCRITO_FINAL_{ap}` (recuadro 2). Menos de 400 palabras; sin citas ni fórmulas.

## Palabras clave
- Español: {kw}
- English: {kwe}

## Autores [CONFIRMAR orden definitivo y autor de correspondencia]
""" + "\n".join(f"{i}. {n} — Universidad Pontificia Bolivariana, Seccional Montería, Colombia — {m} — ID {idn} — ORCID: [CONFIRMAR]" for i, (n, m, idn) in enumerate(autores, 1)) + f"""
{len(autores) + 1}. **Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón** — Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia — cristian.cano@upb.edu.co — ORCID: [CONFIRMAR]

## Tipo de artículo
Investigación científica y tecnológica original.

## Archivos
1. Artículo: `Articulo_Maquetado_EquipoNN_{ap}.pdf` y `.docx`.
2. Carta de presentación y licencia firmada por cada autor (formato oficial; la revista la pide tras la revisión inicial).
3. Figuras en alta resolución (300 dpi), en `articulo/fig/`.
""", encoding="utf-8")
    d = docx.Document(); d.styles["Normal"].font.name = "Verdana"; d.styles["Normal"].font.size = Pt(10)
    for t in ["Montería, [fecha de envío]", "", "Comité Editorial", "Revista UIS Ingenierías — Universidad Industrial de Santander", "", f"Asunto: Sometimiento del manuscrito «{titulo}»", "", "Estimado Comité Editorial:", "",
              f"Los autores someten a su consideración el manuscrito «{titulo}», un artículo de investigación científica y tecnológica que describe y evalúa técnicamente, en laboratorio, un componente de Hand Sing Kids, "
              "una aplicación de enseñanza de notas musicales a niños mediante señas manuales. El trabajo se ajusta al alcance de la revista en ingeniería aplicada y ciencias de la decisión y reporta resultados reproducibles con intervalos de confianza.",
              "", "El manuscrito declara de forma explícita que no se hicieron pruebas con niños y estima un nivel de madurez tecnológica TRL 4. Los autores [CONFIRMAR: certifican que] el manuscrito es original, no ha sido publicado "
              "ni está en evaluación en otra revista, y que todos aprobaron su envío. El uso de una herramienta de inteligencia artificial se declara en el texto.",
              "", "Se adjuntan la carta de licencia de uso parcial firmada por cada autor y las figuras en alta resolución.", "", "Atentamente,", "", f"[{p['nombre']} — autor(a) de correspondencia, CONFIRMAR]",
              "En nombre de los autores: " + ", ".join(a[0] for a in autores) + " y Cristian Javier Cano-Mogollón."]:
        d.add_paragraph(t)
    d.save(str(env / "carta_presentacion_editor.docx"))
    pasos = re.search(r'pasos = f"""(.*?)"""\n\(ENV', ORIG, re.S).group(1)
    (env / "pasos_radicacion.md").write_text(eval('f"""' + pasos + '"""', {"FECHA": FECHA}), encoding="utf-8")


# ------------------------------------------------------------------ LEEME
def leeme(p, carpeta: Path, nart: int, nef: int, ap: str, clave: str):
    pp = p["preprint"]; ident = NH.EQUIPO[clave]
    pre_txt = (f"`Preprint_Manuscrito_EquipoNN_{ap}.pdf` es **tu escaneo real** (ya está en el ZIP) y `Transcripcion_preprint_{ap}.docx` es su transcripción." if pp["modo"] == "existente"
               else f"`Preprint_{ap}_para_copiar_a_mano.docx` es tu preprint **redactado para que lo copies con tu letra** y lo escanees.")
    zip_txt = "Armado con **2 marcadores PENDIENTE** (Turnitin y constancia); el preprint es el real." if pp["modo"] == "existente" else "Armado con **3 marcadores PENDIENTE** (preprint escaneado, Turnitin y constancia)."
    ent = PREF.get("entre_articulos", {}); ef = PREF_EF.get("entre_articulos", {})
    clave_art = p["art"].replace("art_", "")
    mios = [v["pct"] for k, v in ent.items() if clave_art in k.split(" vs ")]
    mios_ef = [v["pct"] for k, v in ef.items() if clave_art in k.split(" vs ")]
    (carpeta / "00_LEEME.md").write_text(f"""# Entrega Corte 3 — {p['nombre']} (ID {ident[2]})
Gestión Tecnológica · UPB Seccional Montería · generado el {FECHA}. Proyecto: Hand Sing Kids.

**Tu hilo:** {p['hilo']}

## Qué hay en esta carpeta
| Carpeta | Qué es | Estado |
|---|---|---|
| `01_Preprint/` | {pre_txt} | {'Listo' if pp['modo'] == 'existente' else 'Redactado; falta copiarlo a mano y escanearlo'} |
| `02_ESCRITO_FINAL/` | **Escrito final**: tu proyecto presentado como artículo científico (dos columnas, carta, {nef} páginas), en PDF y DOCX editable | Listo |
| `03_Guia_de_estudio/` | Tu preprint, el resumen del escrito final, avisos y 5 preguntas de defensa | Listo para leer |
| `04_Articulo_revista_UIS/` | Artículo en la plantilla de la Revista UIS Ingenierías, tú primera autora o primer autor, docente co-autor ({nart} páginas) | Listo |
| `05_Soporte/` | Ficha de la revista, guía de Turnitin de una página y marcadores PENDIENTE | Ficha lista |
| `06_Envio/` | Metadatos OJS, carta al editor, pasos de radicación | Listo, **sin enviar** |
| `07_Entrega_Teams/02_GT_Corte3_CierreProyecto_EquipoNN.zip` | ZIP de cinco archivos con los nombres de la rúbrica (incluye el artículo UIS, no el escrito final) | {zip_txt} |

## Escrito final y artículo UIS: cuál es cuál
- **Escrito final** (`02_ESCRITO_FINAL`): presentación del proyecto final con formato de artículo (Introducción, Contexto, Modelo, Datos y resultados, Conclusiones, Referencias).
- **Artículo UIS** (`04_Articulo_revista_UIS`): versión para la revista, en su plantilla, y es el que entra al ZIP de Teams y a Turnitin.
Los dos comparten datos y cifras, y cada uno está redactado de forma independiente.

## Lo que NO puedo producir y debes conseguir tú
{"1. Nada del preprint: ya tienes tu escaneo." if pp['modo'] == 'existente' else "1. El **escaneo de tu preprint a mano** (copia el recuadro 1 con tu letra)."}
2. El **certificado de Turnitin** (≤ 20 %): lo emite Turnitin. Sube el PDF del artículo UIS (ver `05_Soporte/Guia_Turnitin_1pagina.pdf`).
3. La **constancia de envío** a la revista: la emite el portal OJS, después del Turnitin y del visto bueno del docente.
Sustituye cada marcador por el archivo real, con el mismo nombre, y vuelve a comprimir.

## Datos por confirmar con el equipo
- Número de equipo (NN) y orden definitivo de autores (cada documento lleva a su dueño primero y al resto en el orden de la lista del equipo).
- ORCID, roles CRediT, financiación y conflicto de intereses (marcados «por confirmar»).
- Categoría vigente de la revista en Publindex (captura): la categoría B viene del sitio de la revista.
- Leer el texto completo de las referencias: solo se verificaron existencia y metadatos.
- Código de asignatura: 8830 0064 0 (2.º corte) frente a 8830 0048 0 (Corte 3).

## Qué tiene de diferente tu versión
Las siete versiones usan los mismos datos, los mismos scripts y referencias verificadas, pero cada una defiende una tesis distinta, con tablas, figuras y redacción propias. Coincidencia textual de tu documento con cada uno de los otros seis (prefiltro propio, no es Turnitin): artículo UIS, entre {min(mios) if mios else '—'} % y {max(mios) if mios else '—'} %; escrito final, entre {min(mios_ef) if mios_ef else '—'} % y {max(mios_ef) if mios_ef else '—'} %. Gran parte corresponde a la lista común de autores.

## Avisos para ti
""" + "\n".join("- " + n_ for n_ in p["notas"]) + """

## Advertencias generales
- No hubo pruebas con niños: las cifras son de laboratorio, con una calibración de una persona y perturbaciones simuladas. TRL 4.
- Ninguna cifra debe cambiarse sin cambiarla también en el escrito final, el artículo UIS y el preprint.
""", encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    ev = OUT / "_Evidencia_compartida"; (ev / "fig").mkdir(parents=True, exist_ok=True)
    for f_ in ("resultados_vision.json", "refs_crossref.json", "verificacion_referencias.csv", "salida_pruebas.txt", "prisma_cifras.json", "sensibilidad_umbrales.json"):
        shutil.copy2(BASE / "analisis" / f_, ev / f_)
    for f_ in (BASE / "articulo" / "fig").glob("*.png"):
        shutil.copy2(f_, ev / "fig" / f_.name)
    for f_, dst in (("prefiltro.json", "prefiltro_similitud_articulos_UIS.json"), ("prefiltro_ef.json", "prefiltro_similitud_escritos_finales.json")):
        if (AQUI / "out" / f_).exists():
            shutil.copy2(AQUI / "out" / f_, ev / dst)
    shutil.copy2(AQUI / "quintana_demo.json", ev / "quintana_instancia_ilustrativa.json")
    for clave in EQUIPO_ORDEN:
        p = PERSONAS[clave]; ap = p["corto"].split()[-1]
        carpeta = OUT / p["carpeta"]
        for sub in ("01_Preprint", "02_ESCRITO_FINAL", "03_Guia_de_estudio", "04_Articulo_revista_UIS", "05_Soporte", "06_Envio", "07_Entrega_Teams"):
            (carpeta / sub).mkdir(parents=True, exist_ok=True)
        # escrito final (artículo de proyecto final)
        ef_base = f"Escrito_Final_{p['nombre'].replace(' ', '_')}"
        ef_docx = carpeta / "02_ESCRITO_FINAL" / f"{ef_base}.docx"
        r = subprocess.run([sys.executable, "-X", "utf8", str(AQUI / f"ef_{clave_ef(clave)}.py"), str(ef_docx)], cwd=AQUI, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-1500:]
        convert(str(ef_docx), str(ef_docx.with_suffix(".pdf")))
        nef = len(pymupdf.open(str(ef_docx.with_suffix(".pdf"))))
        meta = json.loads(ef_docx.with_suffix(".json").read_text(encoding="utf-8")); ef_docx.with_suffix(".json").unlink()
        # artículo UIS
        docx_path = carpeta / "04_Articulo_revista_UIS" / f"Articulo_Maquetado_EquipoNN_{ap}.docx"
        r = subprocess.run([sys.executable, "-X", "utf8", str(AQUI / f"{p['art']}.py"), str(docx_path)], cwd=AQUI, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-1500:]
        convert(str(docx_path), str(docx_path.with_suffix(".pdf")))
        nart = len(pymupdf.open(str(docx_path.with_suffix(".pdf"))))
        art_txt = docx_path.with_suffix(".txt").read_text(encoding="utf-8")
        docx_path.with_suffix(".txt").unlink()
        titulo = next(x for x in art_txt.split("\n\n") if x.startswith("[Título art]"))[len("[Título art] "):]
        titulo_en = [x for x in art_txt.split("\n\n") if x.startswith("[Título art]")][1][len("[Título art] "):]
        kw = art_txt.split("[Subtitulos] Palabras clave:\n\n[Normal] ")[1].split("\n\n")[0]
        kwe = art_txt.split("[Subtitulos] Keywords:\n\n[Normal] ")[1].split("\n\n")[0]
        # preprint
        sop = carpeta / "05_Soporte"
        if p["preprint"]["modo"] == "nuevo":
            preprint_formal(p, carpeta / "01_Preprint" / f"Preprint_{ap}_para_copiar_a_mano.docx")
            marcador("escaneo del preprint manuscrito", "Preprint_Manuscrito_EquipoNN.pdf", "Aquí va el escaneo de tu borrador a mano (2 a 3 páginas). Está redactado en 01_Preprint; debes copiarlo con tu letra.", sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf")
            pre_src = sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf"
        else:
            pre_src = preprint_existente(p, carpeta)
        # soporte
        pdf_html(ficha_html(p, titulo), sop / "Ficha_Revista_Indexada_EquipoNN.pdf")
        g = eval('f"""' + re.search(r'guia = f"""(.*?)"""\npdf\("guia"', ORIG, re.S).group(1) + '"""', {"FECHA": FECHA})
        g = re.sub(r"<li>El filtro previo del equipo.*?</li>", "<li>El filtro previo del equipo (<i>prefiltro_equipo.py</i>) midió una coincidencia de menos de 4 % entre los siete artículos UIS del equipo y menos de 1 % con los documentos propios del proyecto. No sustituye a Turnitin: no ve internet ni su base.</li>", g, flags=re.S)
        g = g.replace("<li>Si el documento del 2.º corte o el repositorio ya se subieron a Turnitin, aparecerán como fuente; avisar al docente.</li>",
                      "<li>Si el documento del 2.º corte, el artículo anterior o los artículos de los otros integrantes ya se subieron a Turnitin, aparecerán como fuente; avisar al docente. Cada integrante sube solo su versión y no comparte borradores.</li>")
        pdf_html(g, sop / "Guia_Turnitin_1pagina.pdf")
        marcador("lo emite Turnitin", "Certificado_Turnitin_EquipoNN.pdf", "Aquí va el reporte oficial de originalidad de Turnitin (similitud ≤ 20 %, objetivo ≤ 15 %).", sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf")
        marcador("lo emite la revista", "Constancia_Envio_Revista_EquipoNN.pdf", "Aquí va el acuse oficial del portal OJS de la Revista UIS Ingenierías, con radicado, fecha, título y autores.", sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf")
        envio(p, clave, titulo, titulo_en, kw, kwe, carpeta, ap)
        guia_estudio(p, meta, carpeta)
        z = carpeta / "07_Entrega_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(pre_src, "Preprint_Manuscrito_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf", "Certificado_Turnitin_EquipoNN.pdf")
            zf.write(sop / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
            zf.write(docx_path.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf", "Constancia_Envio_Revista_EquipoNN.pdf")
        leeme(p, carpeta, nart, nef, ap, clave)
        print(clave, "OK", carpeta.name, "UIS", nart, "págs; escrito final", nef, "págs")


def clave_ef(clave):
    return {"Vitola": "vitola", "Petro": "petro", "Negrete": "negrete", "Carrascal": "carrascal", "Quintana": "quintana", "Pemberty": "pemberty", "Guerra": "guerra"}[clave]


main()
