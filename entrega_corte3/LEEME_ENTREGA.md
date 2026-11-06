# Entrega Corte 3 — estado al 5 de noviembre de 2026 (entrega: 6 de noviembre)

## Qué está listo
| Entregable | Archivo | Estado |
|---|---|---|
| Artículo maquetado (plantilla oficial Revista UIS Ingenierías, 11 págs.) | `articulo/Articulo_Maquetado_EquipoNN.pdf` y `.docx` | Listo. Ecuaciones OMML editables; cifras leídas de `analisis/resultados_vision.json` |
| Ficha de revista | `soporte/Ficha_Revista_Indexada_EquipoNN.pdf` | Lista. Categoría B tomada del sitio de la revista; **falta captura de Publindex** |
| Evidencia técnica | `analisis/` (`salida_pruebas.txt`, `evidencia_vision.py`, `resultados_vision.json`, `matriz_similitud.csv/png/svg`) | 8/8 baterías con código 0; 8,0 % = 51/640 reproducido |
| Verificación de referencias | `analisis/verificacion_referencias.csv` | 21 DOI verificados en Crossref/DataCite (20 usados) + DANE |
| Prefiltro de similitud | `analisis/prefiltro_similitud.py/.json` | 0,75 % vs documento_tecnico.md; 0,37 % vs documento del 2.º corte. No sustituye a Turnitin |
| Guía Turnitin (1 pág.) | `soporte/Guia_Turnitin_1pagina.pdf` | Lista |
| Paquete de envío | `envio/` (metadatos OJS, carta, pasos) | Listo, sin enviar |
| ZIP | `entrega_final/02_GT_Corte3_CierreProyecto_EquipoNN.zip` | Armado con **3 marcadores PENDIENTE** |

## Pendientes que NO puedo producir (rotulados como PENDIENTE)
1. `Preprint_Manuscrito_EquipoNN.pdf`: escaneo del preprint del equipo (no estaba en el repositorio).
2. `Certificado_Turnitin_EquipoNN.pdf`: lo emite Turnitin.
3. `Constancia_Envio_Revista_EquipoNN.pdf`: la emite la revista.
Para sustituirlos: poner los reales en `entrega_final/reales/` con el nombre final y ejecutar `python -X utf8 analisis/empaquetar.py <NN>`.

## Decisiones/datos que faltan del equipo
- Número de equipo (NN) y renombrar archivos (el script lo hace con `empaquetar.py NN`; el PDF del artículo y la ficha conservan "NN" en su nombre fuente).
- Orden de autores, autor de correspondencia, ORCID de todos, roles CRediT, financiación y conflicto de intereses (el artículo los marca «por confirmar»).
- Cifras PRISMA y lista de artículos incluidos del preprint: el artículo **no** afirma ser revisión sistemática ni incluye diagrama PRISMA inventado. `analisis/prisma_cifras.json` + `prisma.py` generan la figura cuando se completen las cifras.
- Confirmar código de asignatura (8830 0048 0 en los documentos del corte; 8830 0064 0 en el LEEME del 2.º corte).
- La lista de autores difiere de la del 2.º corte (allí: Guerra, Petro; ahora: Quintana, Vitola). Correo de Andrés: `andres.negreten@` (¿falta o sobra una «n»?).

## Discrepancias encontradas (código vs. documentación)
- `release_frames`: documento_tecnico §3.5 dice 2; el código usa 6 (el artículo usa 6).
- documento_tecnico §11.3.2 dice `MIN_WINDOW_MS = 380`; el código usa 480 (la propia §11.6.2 lo actualiza).
- Tamaño del código: 10.581 líneas / 62 módulos (8.613 sin blancos ni comentarios) vs. 8.599 / 44 del prompt.
- «30 de 56 pares» son pares ordenados = 15 pares no ordenados de 28. Si Si–Do agudo: 0,902 ✔.
- Guía para autores (web) dice dos columnas; la plantilla dice una columna. Se siguió la plantilla.
- Latencia medida 0,89 ms/fotograma (este equipo) vs. 2,3 ms del 2.º corte (otro equipo).
- El desglose del 8 %: 13,8 % transiciones y 2,2 % manos cruzadas (no estaba documentado).

## Riesgos
- Las referencias se verificaron por existencia y metadatos; no se leyeron los textos completos. El artículo solo afirma lo que dicen los títulos. Leerlas antes de enviar.
- Evidencia de Publindex solo del sitio de la revista.
- El tiempo hasta mañana no permite pasar Turnitin + visto bueno docente + envío si el docente tarda; el orden es obligatorio.
