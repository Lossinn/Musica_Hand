# por_clasificar — bandeja de entrada

Todo PDF nuevo entra aquí. Al procesarlo se renombra a `AAAA_Autor_palabra-clave.pdf`,
se mueve a la raíz de `70_documentos/`, se añade fila en `../../Matriz_bibliografica/` y
se crea ficha en `../../Resumenes/`.

## Estado (procesado 2026-09-09)

Los 226 archivos cargados el 2026-09-09 ya se procesaron:

- **189 PDF únicos** → renombrados y movidos a la raíz de `70_documentos/`.
- `_duplicados_exactos/` — **37 archivos** que eran copias byte-a-byte de otro
  (típicamente `... (1).pdf`). Se conservan por seguridad; se pueden borrar.
- `_scopus_zips/` — los **4 ZIP** de descarga de Scopus (`Scopus_09Sep2026_*.zip`).
  Solo contenían PDFs (ya extraídos), **no** el CSV/BibTeX de metadatos.

Ver el informe en `../../../04_Datos/bibliometria/resultados/informe_bibliometrico_corpus.md`.

## Pendiente

Para la bibliometría formal falta exportar de Scopus el **CSV "All available information"
+ BibTeX** de cada ecuación y dejarlo en `04_Datos/bibliometria/raw/`.
