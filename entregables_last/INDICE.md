# Índice de `entregables_last` — Hand Sing Kids, Corte 3

**Lo que se entrega: `ENTREGA_FINAL/`** (empieza por su `LEEME.md`, que contiene la verificación contra las cuatro guías del curso).

| Carpeta | Contenido |
|---|---|
| `ENTREGA_FINAL/` | Artículo único en dos columnas, preprint manuscrito (3 escaneos unidos), soporte, envío, evidencia y ZIP para Teams (solo con lo confirmado) |
| `00_Instrucciones_del_curso/` | Guía del estudiante, instrucciones y publicación de Teams, rúbrica y prompt del Corte 3 |
| `01_Estado_y_planes/` | Estado y plan del 5 de noviembre |
| `pre_print/` | Escaneos originales (Antolin Vitola, Juan Diego Guerra, Andrés Negrete) y textos de los cuatro preprint individuales nuevos |
| `analisis/` | Scripts, resultados, referencias verificadas, sensibilidad de umbrales y salida de pruebas |
| `articulo/fig/` | Figuras del artículo |
| `revista/` | Plantilla oficial y carta de licencia de la Revista UIS Ingenierías |
| `generador/` | Scripts que producen el artículo y la entrega (`ef_equipo.py` para el artículo de dos columnas, `armar_final.py` para la entrega; `art_unico.py` es la fuente del texto y la versión en plantilla UIS); incluye material de intentos descartados (artículos por integrante y escritos finales de dos columnas) |
| `_versiones_anteriores/` | Primer intento, los siete artículos por integrante (descartados) y `articulo_plantilla_UIS/` (versión en la plantilla de la revista, con datos sin confirmar) |

Para regenerar la entrega: `python -X utf8 generador/armar_final.py` (≈ 1 minuto; usa Word para convertir a PDF).
