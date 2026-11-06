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
            q = c.add_paragraph(); runs_md(q, txt); q.paragraph_format.space_after = Pt(4); q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
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
def escrito_final(p, art_txt: str, carpeta: Path):
    doc = docx.Document(); doc.styles["Normal"].font.name = "Calibri"; doc.styles["Normal"].font.size = Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    doc.add_heading(f"ESCRITO FINAL — {p['nombre']}", 0)
    ident = NH.EQUIPO[[k for k, v in PERSONAS.items() if v is p][0]]
    doc.add_paragraph(f"ID {ident[2]} · {ident[1]} · Gestión Tecnológica, Corte 3 · UPB Seccional Montería · {FECHA}")
    q = doc.add_paragraph(); r = q.add_run("Tu hilo argumental: "); r.bold = True; q.add_run(p["hilo"])
    q = doc.add_paragraph(); r = q.add_run("Cómo conecta tu preprint con tu artículo: "); r.bold = True; q.add_run(p["conecta"])
    doc.add_paragraph("Cómo usar este documento: los recuadros «ESCRITO FINAL» son los textos que debes leer, entender y hacer tuyos. El 1 es tu preprint; el 2, el resumen y el abstract; el 3, el texto del artículo maquetado. "
                      "Las cifras salen de scripts reproducibles; si cambias una, cámbiala también en el artículo.")
    pp = p["preprint"]
    if pp["modo"] == "nuevo":
        caja(doc, "ESCRITO FINAL 1 — Preprint para transcribir a mano (2 a 3 páginas)", [("", x) for x in leer_preprint_md(pp["md"])])
    else:
        caja(doc, "ESCRITO FINAL 1 — Tu preprint (ya escrito a mano; transcripción" + (" aproximada" if pp["aprox"] else "") + ")", [("", x) for x in pp["trans"].split("\n\n")])
    bloques = art_txt.split("\n\n")

    def despues(rot):
        for i, x in enumerate(bloques):
            if x == f"[Subtitulos] {rot}":
                return re.sub(r"^\[[^\]]+\] ", "", bloques[i + 1])
    caja(doc, "ESCRITO FINAL 2 — Resumen y abstract (ficha, formulario de la revista y plataforma)",
         [("Resumen", despues("Resumen:")), ("Abstract", despues("Abstract:")), ("Palabras clave", despues("Palabras clave:")), ("Keywords", despues("Keywords:"))])
    cuerpo = []
    for x in bloques:
        m = re.match(r"^\[([^\]]+)\] (.*)$", x, re.S)
        if not m:
            continue
        est, txt = m.groups()
        if est in ("Título art", "Nombre autores") or (est == "Normal" and txt.startswith(("^{", "["))):
            continue
        if est.startswith("Heading"):
            cuerpo.append(("\n" + txt.upper() if est == "Heading 1" else "› " + txt, ""))
        elif est in ("Tabla Título", "Figura Título"):
            cuerpo.append(("", "[" + txt + "]"))
        elif est == "Subtitulos":
            cuerpo.append((txt, ""))
        else:
            cuerpo.append(("", re.sub(r"\^\{[^}]*\}", "", txt)))
    caja(doc, "ESCRITO FINAL 3 — Texto del artículo (ecuaciones y figuras: ver el artículo maquetado)", [c for c in cuerpo if c[0] or c[1]])
    doc.add_heading("Avisos para ti", 1)
    for n_ in p["notas"]:
        q = doc.add_paragraph(style="List Bullet"); runs_md(q, n_)
    doc.add_heading("Guion de defensa: 5 preguntas que te pueden hacer", 1)
    for qn_, ans in p["defensa"]:
        qq = doc.add_paragraph(); r = qq.add_run(qn_); r.bold = True
        doc.add_paragraph(ans)
    doc.save(str(carpeta / f"02_ESCRITO_FINAL_{p['corto'].split()[-1]}.docx"))
    md = [f"# ESCRITO FINAL — {p['nombre']}\n\n**Tu hilo:** {p['hilo']}\n\n**Preprint y artículo:** {p['conecta']}\n\n---\n## ESCRITO FINAL 1 — Preprint\n\n"]
    md.append("\n\n".join(leer_preprint_md(pp["md"])) if pp["modo"] == "nuevo" else pp["trans"])
    md.append("\n\n---\n## ESCRITO FINAL 2 — Resumen y abstract\n\n**Resumen.** " + despues("Resumen:") + "\n\n**Abstract.** " + despues("Abstract:") + "\n\n---\n## ESCRITO FINAL 3 — Texto del artículo\n\n")
    md.append(re.sub(r"\n\n\[Heading 1\] ", "\n\n# ", re.sub(r"\n\n\[Heading 2\] ", "\n\n## ", art_txt)).replace("[Normal] ", "").replace("[Subtitulos] ", "**").replace("[Tabla Título] ", "*").replace("[Figura Título] ", "*"))
    md.append("\n\n---\n## Avisos\n\n" + "\n".join("- " + n_ for n_ in p["notas"]) + "\n\n## Guion de defensa\n")
    for q_, a_ in p["defensa"]:
        md.append(f"\n**{q_}**  \n{a_}\n")
    (carpeta / f"02_ESCRITO_FINAL_{p['corto'].split()[-1]}.md").write_text("".join(md), encoding="utf-8")


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
def leeme(p, carpeta: Path, nart: int, ap: str, clave: str):
    pp = p["preprint"]; ident = NH.EQUIPO[clave]
    pre_txt = (f"`01_Preprint/Preprint_Manuscrito_EquipoNN_{ap}.pdf` es **tu escaneo real** (ya incluido en el ZIP) y `Transcripcion_preprint_{ap}.docx` es su transcripción." if pp["modo"] == "existente"
               else f"`01_Preprint/Preprint_{ap}_para_copiar_a_mano.docx` es tu preprint **redactado para que lo copies con tu letra** y lo escanees.")
    zip_txt = "Armado con **2 marcadores PENDIENTE** (Turnitin y constancia); el preprint es el real." if pp["modo"] == "existente" else "Armado con **3 marcadores PENDIENTE** (preprint escaneado, Turnitin y constancia)."
    ent = PREF.get("entre_articulos", {})
    mios = [v["pct"] for k, v in ent.items() if p["art"].replace("art_", "") in k.split(" vs ")]
    (carpeta / "00_LEEME.md").write_text(f"""# Entrega Corte 3 — {p['nombre']} (ID {ident[2]})
Gestión Tecnológica · UPB Seccional Montería · generado el {FECHA}. Proyecto: Hand Sing Kids.

**Tu hilo:** {p['hilo']}

## Qué hay en esta carpeta
| Carpeta / archivo | Qué es | Estado |
|---|---|---|
| `01_Preprint/` | {pre_txt} | {'Listo' if pp['modo'] == 'existente' else 'Redactado; falta copiarlo a mano y escanearlo'} |
| `02_ESCRITO_FINAL_{ap}.docx` (y `.md`) | Recuadros ESCRITO FINAL (preprint, resumen, texto del artículo), avisos y guion de defensa | Listo para leer |
| `03_Articulo/Articulo_Maquetado_EquipoNN_{ap}.pdf` y `.docx` | Artículo en la plantilla de la Revista UIS Ingenierías, tú como primera autora o primer autor, docente co-autor | Listo ({nart} páginas) |
| `04_Soporte/` | Ficha de la revista, guía de Turnitin de una página y marcadores PENDIENTE | Ficha lista |
| `05_Envio/` | Metadatos OJS, carta al editor, pasos de radicación | Listo, **sin enviar** |
| `06_Entrega_Teams/02_GT_Corte3_CierreProyecto_EquipoNN.zip` | ZIP de cinco archivos con los nombres de la rúbrica | {zip_txt} |

## Lo que NO puedo producir y debes conseguir tú
{"1. Nada del preprint: ya tienes tu escaneo." if pp['modo'] == 'existente' else "1. El **escaneo de tu preprint a mano** (copia el recuadro 1 con tu letra)."}
2. El **certificado de Turnitin** (≤ 20 %): lo emite Turnitin. Sube el PDF del artículo (ver `04_Soporte/Guia_Turnitin_1pagina.pdf`).
3. La **constancia de envío** a la revista: la emite el portal OJS, después del Turnitin y del visto bueno del docente.
Sustituye cada marcador por el archivo real, con el mismo nombre, y vuelve a comprimir.

## Datos por confirmar con el equipo
- Número de equipo (NN) y orden definitivo de autores (aquí cada artículo lleva a su dueño primero y al resto en el orden de la lista del equipo).
- ORCID, roles CRediT, financiación y conflicto de intereses (marcados «por confirmar»).
- Categoría vigente de la revista en Publindex (captura): la categoría B viene del sitio de la revista.
- Leer el texto completo de las referencias: solo se verificaron existencia y metadatos.
- Código de asignatura: 8830 0064 0 (2.º corte) frente a 8830 0048 0 (Corte 3).

## Qué tiene de diferente tu versión
Las siete versiones usan los mismos datos, los mismos scripts y las mismas 21 referencias verificadas, pero cada una defiende una tesis distinta, con tablas, figuras y redacción propias. Coincidencia textual de tu artículo con cada uno de los otros seis (prefiltro propio, no es Turnitin): entre {min(mios) if mios else '—'} % y {max(mios) if mios else '—'} %; gran parte corresponde a la lista común de autores.

## Avisos para ti
""" + "\n".join("- " + n_ for n_ in p["notas"]) + """

## Advertencias generales
- No hubo pruebas con niños: las cifras son de laboratorio, con una calibración de una persona y perturbaciones simuladas. TRL 4.
- Ninguna cifra debe cambiarse sin cambiarla también en el artículo y en el preprint.
""", encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    ev = OUT / "_Evidencia_compartida"; (ev / "fig").mkdir(parents=True, exist_ok=True)
    for f_ in ("resultados_vision.json", "refs_crossref.json", "verificacion_referencias.csv", "salida_pruebas.txt", "prisma_cifras.json"):
        shutil.copy2(BASE / "analisis" / f_, ev / f_)
    for f_ in (BASE / "articulo" / "fig").glob("*.png"):
        shutil.copy2(f_, ev / "fig" / f_.name)
    if (AQUI / "out" / "prefiltro.json").exists():
        shutil.copy2(AQUI / "out" / "prefiltro.json", ev / "prefiltro_similitud_equipo.json")
    for clave in EQUIPO_ORDEN:
        p = PERSONAS[clave]; ap = p["corto"].split()[-1]
        carpeta = OUT / p["carpeta"]
        for sub in ("01_Preprint", "03_Articulo", "04_Soporte", "05_Envio", "06_Entrega_Teams"):
            (carpeta / sub).mkdir(parents=True, exist_ok=True)
        # artículo
        docx_path = carpeta / "03_Articulo" / f"Articulo_Maquetado_EquipoNN_{ap}.docx"
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
        sop = carpeta / "04_Soporte"
        if p["preprint"]["modo"] == "nuevo":
            preprint_formal(p, carpeta / "01_Preprint" / f"Preprint_{ap}_para_copiar_a_mano.docx")
            marcador("escaneo del preprint manuscrito", "Preprint_Manuscrito_EquipoNN.pdf", "Aquí va el escaneo de tu borrador a mano (2 a 3 páginas). Está redactado en 01_Preprint; debes copiarlo con tu letra.", sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf")
            pre_src = sop / "PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf"
        else:
            pre_src = preprint_existente(p, carpeta)
        # soporte
        pdf_html(ficha_html(p, titulo), sop / "Ficha_Revista_Indexada_EquipoNN.pdf")
        g = eval('f"""' + re.search(r'guia = f"""(.*?)"""\npdf\("guia"', ORIG, re.S).group(1) + '"""', {"FECHA": FECHA})
        g = re.sub(r"<li>El filtro previo del equipo.*?</li>", "<li>El filtro previo del equipo (<i>prefiltro_equipo.py</i>) midió una coincidencia de entre 9 y 14 % entre los siete artículos del equipo (mayormente la lista común de autores) y menos de 1 % con los documentos propios del proyecto. No sustituye a Turnitin: no ve internet ni su base.</li>", g, flags=re.S)
        g = g.replace("<li>Si el documento del 2.º corte o el repositorio ya se subieron a Turnitin, aparecerán como fuente; avisar al docente.</li>",
                      "<li>Si el documento del 2.º corte, el artículo anterior o los artículos de los otros integrantes ya se subieron a Turnitin, aparecerán como fuente; avisar al docente. Cada integrante sube solo su versión y no comparte borradores.</li>")
        pdf_html(g, sop / "Guia_Turnitin_1pagina.pdf")
        marcador("lo emite Turnitin", "Certificado_Turnitin_EquipoNN.pdf", "Aquí va el reporte oficial de originalidad de Turnitin (similitud ≤ 20 %, objetivo ≤ 15 %).", sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf")
        marcador("lo emite la revista", "Constancia_Envio_Revista_EquipoNN.pdf", "Aquí va el acuse oficial del portal OJS de la Revista UIS Ingenierías, con radicado, fecha, título y autores.", sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf")
        envio(p, clave, titulo, titulo_en, kw, kwe, carpeta, ap)
        escrito_final(p, art_txt, carpeta)
        z = carpeta / "06_Entrega_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(pre_src, "Preprint_Manuscrito_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Certificado_Turnitin_EquipoNN.pdf", "Certificado_Turnitin_EquipoNN.pdf")
            zf.write(sop / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
            zf.write(docx_path.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
            zf.write(sop / "PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf", "Constancia_Envio_Revista_EquipoNN.pdf")
        leeme(p, carpeta, nart, ap, clave)
        print(clave, "OK", carpeta.name, nart, "págs")


main()
