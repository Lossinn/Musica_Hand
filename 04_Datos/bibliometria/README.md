# Bibliometría

Datos y resultados del estudio bibliométrico. **Aquí NO van los PDF** (esos van a
`02_Base_de_investigacion/70_documentos/`). Aquí van los **metadatos exportados** de
las bases y los productos del análisis.

| Carpeta       | Contenido                                                                 |
|---------------|--------------------------------------------------------------------------|
| `raw/`        | Exportes crudos de Scopus / WoS: `.csv`, `.bib`, `.ris`, `savedrecs.txt`. Un archivo por ecuación y base, sin editar. |
| `processed/`  | Datos limpios y unificados: dataset combinado, duplicados eliminados, campos normalizados. |
| `resultados/` | Figuras y tablas: producción por año, países, autores, revistas, co-citación, co-ocurrencia de palabras clave, mapas VOSviewer. |

## Flujo

```
07_Ecuaciones_booleanas/Scopus  →  ejecutar en Scopus
        →  exportar metadatos (CSV completo + BibTeX)  →  04_Datos/bibliometria/raw/
        →  limpieza / merge                            →  processed/
        →  análisis (Bibliometrix / Biblioshiny / VOSviewer / bibliometrix en R,
                     o pandas)                          →  resultados/
        →  redacción                                   →  06_Documentos_por_capitulo/Capitulo_2
```

## Al exportar desde Scopus

- Seleccionar **todos** los registros de la búsqueda (o el subconjunto tras aplicar facetas).
- Formato: **CSV** con *"All available information"* (para Biblioshiny/pandas) y además
  **BibTeX** o **RIS** (para el gestor de referencias).
- Nombrado sugerido: `scopus_ecuacion1_AAAA-MM-DD.csv`, `scopus_ecuacion2_AAAA-MM-DD.bib`.
- Anotar el nº de registros exportados en
  `07_Ecuaciones_booleanas/Scopus/ecuaciones_scopus.md`.

## Nota de versionado

`raw/` y `processed/` pueden pesar. Si algún export supera ~50 MB, no lo subas a git
(añádelo a `.gitignore`) y dejá una nota en `raw/FUENTES.md` con la fecha y el nº de registros.
