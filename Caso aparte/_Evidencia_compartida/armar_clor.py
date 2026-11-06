"""Entrega final del clorificador: artículo único en dos columnas, soporte, envío, evidencia y ZIP (solo lo existente).
Uso: python -X utf8 armar_clor.py"""
import json, re, shutil, subprocess, sys, zipfile
from pathlib import Path
import docx
import pymupdf
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
from docx2pdf import convert

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
OUT = RAIZ / "ENTREGA_FINAL_CLORIFICADOR"
GEN = RAIZ.parent / "entregables_last" / "generador"
FECHA = "6 de noviembre de 2026"
PF = json.loads((AQUI / "prefiltro_similitud.json").read_text(encoding="utf-8"))["contra_fuentes"]
pi1 = PF["PI-I documento final (docx)"]["clor"]; seg = PF["Entrega 2.º corte (md)"]["clor"]

# se reutilizan los textos y el estilo sobrio de la entrega de Hand Sing Kids (misma revista, mismo curso)
src = (GEN / "armar_final.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")
ns = {"__file__": str(GEN / "armar_final.py")}
exec(compile(src, "armar_final", "exec"), ns)
pdf_html, FICHA, GUIA = ns["pdf_html"], ns["FICHA"], ns["GUIA"]
GUIA = re.sub(r"<li>El filtro previo.*?</li>",
              f"<li>El filtro previo del equipo midió {pi1['pct']:.1f} % de coincidencia con el documento final del Proyecto Integrador I (tramo continuo máximo de {pi1['tramo_max_palabras']} palabras) y {seg['pct']:.1f} % con el documento del segundo corte. No reemplaza a Turnitin, que compara contra internet y su propia base.</li>", GUIA, flags=re.S)
GUIA = GUIA.replace("el documento técnico, el del segundo corte", "el documento del Proyecto Integrador I, el del segundo corte")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for sub in ("1_Articulo", "2_Soporte", "3_Envio", "4_Evidencia", "5_ZIP_para_Teams"):
        (OUT / sub).mkdir(parents=True)
    dx = OUT / "1_Articulo" / "Articulo_Maquetado_EquipoNN.docx"
    r = subprocess.run([sys.executable, "-X", "utf8", str(AQUI / "ef_clor.py"), str(dx)], cwd=AQUI, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    convert(str(dx), str(dx.with_suffix(".pdf")))
    npag = len(pymupdf.open(str(dx.with_suffix(".pdf"))))
    sop = OUT / "2_Soporte"
    pdf_html(FICHA, sop / "Ficha_Revista_Indexada_EquipoNN.pdf")
    pdf_html(GUIA, sop / "Guia_Turnitin_1pagina.pdf")
    # carta
    d = docx.Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
    for s in d.sections:
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.5)
    texto = ["Montería, ____ de __________ de 2026", "", "Comité Editorial", "Revista UIS Ingenierías, Universidad Industrial de Santander", "",
             "Asunto: envío del manuscrito «Clorificador pasivo de PVC con derivación para una vereda rural de Montería: balance de masa, sensibilidad, diseño experimental y viabilidad económica»", "",
             "Estimados señores:", "",
             "Les enviamos para su consideración el manuscrito indicado, un artículo de investigación científica y tecnológica sobre un clorificador pasivo de bajo costo para una vereda rural de Montería. "
             "El texto plantea el balance de masa del dispositivo, simula su cumplimiento con 1.000 escenarios de Monte Carlo, analiza qué variables controlan el cloro residual, propone un diseño factorial 2³ para validarlo y calcula su costo y tiempo de recuperación. "
             "Creemos que encaja con el alcance de la revista en ingeniería aplicada y ciencias de la decisión.",
             "", "El manuscrito dice expresamente que sus resultados provienen de simulación con supuestos del equipo, sin validación experimental, y ubica el desarrollo en el nivel de madurez tecnológica 3. El uso de un asistente de inteligencia artificial se declara en el texto.",
             "", "Quedamos atentos a sus comentarios.", "", "Cordialmente,", "", "", "______________________________",
             "Por los autores: Roxana Elena Muñoz Rodiño, Camilo Esteban Alvarez Durán, Andrea Guzmán Gómez y Cristian Javier Cano Mogollón."]
    for t in texto:
        p = d.add_paragraph(t); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.paragraph_format.space_after = Pt(0)
    d.save(str(OUT / "3_Envio" / "carta_presentacion_editor.docx"))
    pasos = (GEN.parent / "ENTREGA_FINAL" / "4_Envio" / "pasos_radicacion.md").read_text(encoding="utf-8")
    (OUT / "3_Envio" / "pasos_radicacion.md").write_text(pasos, encoding="utf-8")
    # evidencia
    ev = OUT / "4_Evidencia"; (ev / "fig").mkdir()
    for f_ in ("estudio_clorificador.py", "complemento.py", "busqueda_prisma.py", "verificar_refs.py", "prefiltro_similitud.py", "resultados_estudio.json", "resultados_complemento.json",
               "prisma_cifras.json", "busqueda_prisma.json", "abstracts_seleccion.json", "refs_crossref.json", "verificacion_referencias.csv", "DOE_hoja_aleatorizacion.csv", "prefiltro_similitud.json"):
        shutil.copy2(AQUI / f_, ev / f_)
    for g in (AQUI / "fig").glob("*.png"):
        shutil.copy2(g, ev / "fig" / g.name)
    z = OUT / "5_ZIP_para_Teams" / "02_GT_Corte3_CierreProyecto_EquipoNN.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(sop / "Ficha_Revista_Indexada_EquipoNN.pdf", "Ficha_Revista_Indexada_EquipoNN.pdf")
        zf.write(dx.with_suffix(".pdf"), "Articulo_Maquetado_EquipoNN.pdf")
    (OUT / "LEEME.md").write_text(f"""# Entrega del equipo: clorificador de agua para El Vidrial, Corte 3

Gestión Tecnológica, UPB Seccional Montería. Preparada el {FECHA}.

## Qué hay
| Carpeta | Contenido |
|---|---|
| `1_Articulo/` | Artículo único del equipo en dos columnas, PDF y Word ({npag} páginas, 22 referencias verificadas). Autores: Roxana Muñoz, Camilo Alvarez, Andrea Guzmán y el docente Cristian Cano |
| `2_Soporte/` | Ficha de la revista y guía de una página para Turnitin |
| `3_Envio/` | Carta al editor y pasos de radicación en OJS |
| `4_Evidencia/` | Scripts, resultados de la simulación, búsqueda bibliográfica, referencias, hoja de aleatorización del diseño 2³ y figuras |
| `5_ZIP_para_Teams/` | `02_GT_Corte3_CierreProyecto_EquipoNN.zip` con lo que ya existe |

## El ZIP
Contiene `Ficha_Revista_Indexada_EquipoNN.pdf` y `Articulo_Maquetado_EquipoNN.pdf`. No hay archivos simulados.

Los otros tres archivos de la rúbrica se añaden cuando existan, con estos nombres:
- `Preprint_Manuscrito_EquipoNN.pdf`: el escaneo del preprint escrito a mano.
- `Certificado_Turnitin_EquipoNN.pdf`: lo emite Turnitin al subir el PDF del artículo (guía en `2_Soporte/`).
- `Constancia_Envio_Revista_EquipoNN.pdf`: la entrega el portal de la revista al radicar (pasos en `3_Envio/`).

## Notas
- Los resultados provienen de una simulación con distribuciones supuestas por el equipo; no hay mediciones del prototipo. El artículo lo dice y ubica el desarrollo en TRL 3.
- Los tres análisis personales anteriores (balance de masa, sensibilidad y diseño experimental, costo y viabilidad) quedaron integrados en este único artículo; las versiones individuales están en las carpetas de cada integrante.
- La búsqueda bibliográfica se hizo en OpenAlex y la elegibilidad se evaluó sobre título y resumen. Se verificó que cada referencia existe y que sus metadatos coinciden.
- El artículo no incluye ORCID, autor de correspondencia, financiación ni conflicto de intereses; hay que añadirlos antes del envío si la revista los pide.
- Filtro previo de similitud: {pi1['pct']:.1f} % contra el documento final del Proyecto Integrador I y {seg['pct']:.1f} % contra el del segundo corte. No sustituye a Turnitin.
- El artículo declara el uso de un asistente de inteligencia artificial. Antes de defenderlo, todos deben haberlo leído completo.
""", encoding="utf-8")
    # carpeta plana de entregables
    pl = RAIZ / "ENTREGABLES_CLORIFICADOR"
    if pl.exists():
        shutil.rmtree(pl)
    pl.mkdir()
    for a in (dx, dx.with_suffix(".pdf"), sop / "Ficha_Revista_Indexada_EquipoNN.pdf", z):
        shutil.copy2(a, pl / a.name)
    print("listo:", npag, "páginas;", [i.filename for i in zipfile.ZipFile(z).infolist()])


main()
