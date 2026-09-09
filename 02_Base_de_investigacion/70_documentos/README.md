# 70_documentos

**Aquí van los PDF** de los artículos, tesis, libros y normas que se usarán para la
bibliografía y el marco teórico.

## Nombrado

```
AAAA_PrimerAutor_palabra-clave.pdf
```

Ejemplos:
- `2019_Zhang_gesture-recognition-music.pdf`
- `2021_Holland_music-interaction-review.pdf`

## Organización

- `por_clasificar/` — bandeja de entrada. Todo PDF nuevo entra aquí primero.
- Al procesarlo: se renombra, se mueve a la raíz de `70_documentos/`, se añade fila en
  `../Matriz_bibliografica/` y se crea su ficha en `../Resumenes/` con el mismo nombre.

## Importante

- Los PDF son solo el **texto completo** para leer y citar.
- Los **metadatos** para el estudio bibliométrico (conteos, redes, mapas) NO salen de
  estos PDF, sino de los exportes CSV/BibTeX de Scopus → `04_Datos/bibliometria/raw/`.
- Si el repositorio crece mucho, considerar no versionar los PDF (mover el patrón a
  `.gitignore`) y mantener solo la matriz bibliográfica y las fichas.
