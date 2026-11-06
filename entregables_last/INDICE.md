# Índice de `entregables_last` — Hand Sing Kids, Corte 3

**Entrega final por integrante: `entregas_por_integrante/`.** Cada carpeta empieza con su `00_LEEME.md`.

| Carpeta | Integrante | Enfoque e hilo del artículo | Preprint |
|---|---|---|---|
| `01_Antolin_Vitola_Montes` | Antolin De Jesús Vitola Montes (000523062) | Acceso y valor pedagógico: las manos como instrumento | Escaneo propio (existente) |
| `02_Isaias_Petro_Rodriguez` | Isaías José Petro Rodríguez (000522944) | Visión: distinguir la seña intencional del gesto de paso | Nuevo, para copiar a mano |
| `03_Andres_Negrete_Pacheco` | Andrés Julián Negrete Pacheco (000506474) | Tiempo y retroalimentación: cuándo debe sonar la nota | Escaneo propio (existente) |
| `04_Juliana_Carrascal_Hernandez` | Juliana Esther Carrascal Hernández (000518109) | Aprendizaje adaptativo: del intento al dominio | Nuevo, para copiar a mano |
| `05_Angel_Quintana_Jimenez` | Angel Quintana Jiménez (000454040) | Optimización: la sesión como programación entera mixta | Nuevo, para copiar a mano |
| `06_Alejandro_Pemberty_Vergara` | Alejandro Pemberty Vergara (000362954) | Ingeniería reproducible y despliegue responsable | Nuevo, para copiar a mano |
| `07_Juan_Diego_Guerra_Gomez` | Juan Diego Guerra Gómez (000520912) | Lo reportado y lo medido: verificación de cifras | Escaneo propio (existente) |
| `_Evidencia_compartida` | — | Resultados, referencias verificadas, prefiltro y figuras comunes | — |

Dentro de cada carpeta: `01_Preprint`, `02_ESCRITO_FINAL_*`, `03_Articulo`, `04_Soporte`, `05_Envio`, `06_Entrega_Teams` (ZIP) y `00_LEEME.md`.

## Resto de la carpeta
| Carpeta | Contenido |
|---|---|
| `00_Instrucciones_del_curso/` | Guía del estudiante, instrucciones y publicación de Teams, rúbrica y prompt del Corte 3 |
| `01_Estado_y_planes/` | `LEEME_ENTREGA.md` y `00_PLAN_FASE0.md` (estado y plan del 5 de noviembre) |
| `pre_print/originales/` | Escaneos de Antolin Vitola, Juan Diego Guerra y Andrés Negrete (sin modificar) |
| `pre_print/nuevos/` | Textos fuente de los cuatro preprint nuevos (Petro, Carrascal, Pemberty, Quintana) |
| `generador/` | Scripts que producen los siete artículos y las carpetas (`construir_entregas.py`) |
| `analisis/` | Scripts, resultados, referencias verificadas y salida de pruebas que alimentan las cifras |
| `articulo/fig/` | Figuras de los artículos |
| `revista/` | Plantilla oficial y carta de licencia de la Revista UIS Ingenierías |
| `_versiones_anteriores/` | Artículos, ZIP, soporte y envío del primer intento (variantes Pemberty y Carrascal con el mismo texto); reemplazados por `entregas_por_integrante/` |

Para regenerar: `python -X utf8 generador/construir_entregas.py` (≈ 4 minutos; usa Word para convertir a PDF).
