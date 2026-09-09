# Matriz bibliográfica

## `matriz_bibliografica.csv`

Una fila por documento único de `70_documentos/` (189 tras el procesado del 2026-09-09).
Codificación UTF-8 con BOM (abre bien en Excel). Columnas:

| Columna | Descripción |
|---|---|
| `id` | Identificador interno (número de orden de procesado) |
| `archivo_nuevo` | Nombre del PDF en `70_documentos/` (`AAAA_Autor_slug.pdf`) |
| `archivo_original` | Nombre con el que llegó a `por_clasificar/` |
| `n_copias` | Nº de copias byte-a-byte que había (1 = sin duplicados) |
| `anio` | Año de publicación (heurística + verificación manual de portada) |
| `autor_principal` | Apellido del primer autor |
| `pais` | País de afiliación del primer autor / correspondencia |
| `titulo` | Título (autogenerado del nombre de archivo o de la portada — **revisar**) |
| `tipo` / `tipo_desc` | RS, SCOP, BIB, EMP, TEC, CONC, CONF, PROC, EDIT |
| `tecnologia` | Tecnología / método principal |
| `dominio` | Área o dominio musical |
| `poblacion` | Población del estudio (edad / nivel) |
| `relacion` / `relacion_desc` | Cribado A/B/C/D respecto al proyecto (ver informe) |
| `keywords` | Palabras clave de autor (extraídas del PDF) |
| `doi` | DOI |
| `abstract` | Resumen (extraído del texto completo) |

### Cribado de relación

- **A — Núcleo:** visión/gesto/manos + música · aprendizaje musical adaptativo con
  RL/ITS/gemelo digital · feedback en tiempo real · música infantil + tecnología.
- **B — Relevante:** IA/tecnología en educación musical en general.
- **C — Método/contexto:** revisiones y bibliometrías de IA en educación no musical,
  método bibliométrico, RV/RA/gamificación en educación general.
- **D — Marginal:** temas alejados.

### Pendiente

- Revisar la columna `titulo` (autogenerada).
- La bibliometría formal (co-citación, redes) necesita el export CSV de Scopus, no estos PDF.
