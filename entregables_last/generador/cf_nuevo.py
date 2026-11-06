#@@GUIA
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


#@@LEEME
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


#@@MAIN
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
