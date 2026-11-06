# Ecuaciones booleanas — Scopus

> Base: Scopus (Elsevier) · Búsqueda avanzada (Advanced search) · Campo `TITLE-ABS-KEY`
> El conteo depende de la suscripción institucional y de la fecha de consulta.
> Registrar SIEMPRE: fecha, nº de resultados, filtros aplicados.

---

## Ecuación 1 — Aprendizaje musical asistido por tecnología e IA (núcleo pedagógico)

Cubre el objeto de estudio del proyecto (§2, §4): enseñanza/aprendizaje de música
infantil apoyada en tecnología, IA y personalización.

```
TITLE-ABS-KEY (
  ( "music education" OR "music learning" OR "music teaching" OR "musical training"
    OR "music training" OR "music instruction" OR "learning music" OR "music tuition"
    OR "music pedagogy" OR "musical education" )
  AND
  ( "artificial intelligence" OR "machine learning" OR "deep learning"
    OR "adaptive learning" OR "personalized learning" OR "personalised learning"
    OR "intelligent tutoring" OR "educational technology" OR "technology-enhanced learning"
    OR "e-learning" OR gamification OR "serious game" OR "serious games"
    OR "digital game" OR "learning analytics" OR multimedia OR software OR "mobile app" )
)
```

- **Magnitud esperada:** varios miles. Muy por encima de 500.
- **Para acotar** (sin bajar de 500): añadir por facetas
  `AND PUBYEAR > 2009`, `LIMIT-TO ( LANGUAGE , "English" )`,
  `LIMIT-TO ( SUBJAREA , "COMP" ) OR LIMIT-TO ( SUBJAREA , "SOCI" )`.

---

## Ecuación 2 — Interacción gestual y visión por computador aplicada a la música (núcleo de interacción)

Cubre la capa de entrada del sistema (§6–§7): reconocimiento de manos/gestos con
cámara para interactuar con notas musicales.

```
TITLE-ABS-KEY (
  ( "gesture recognition" OR "hand gesture" OR "hand-gesture recognition"
    OR "hand tracking" OR "hand pose estimation" OR "hand pose"
    OR "gesture-based interaction" OR "gestural interaction" OR "gesture interface"
    OR "computer vision" OR "pose estimation" OR "motion capture"
    OR "body movement" OR "mid-air interaction" )
  AND
  ( music OR musical OR "musical instrument" OR "music performance"
    OR "musical expression" OR "musical interaction" OR "sound synthesis"
    OR "note recognition" OR "music learning" OR "music education" )
)
```

- **Magnitud esperada:** ~1000–3000. Por encima de 500.
- **Para acotar:** `AND PUBYEAR > 2012`, `LIMIT-TO ( LANGUAGE , "English" )`,
  o intersecar con `AND ( child* OR kid* OR "early childhood" OR pediatric )`
  para el subconjunto infantil (ese sí bajará bastante — usarlo solo en el cribado,
  no para el conteo que pide el profesor).

---

## Registro de ejecución

| # | Fecha (AAAA-MM-DD) | Filtros aplicados | Nº de resultados | Observaciones |
|---|--------------------|-------------------|------------------|---------------|
| 1 |                    | ninguno           |                  |               |
| 2 |                    | ninguno           |                  |               |

---

## Notas de sintaxis Scopus

- Frase exacta: comillas dobles `"..."`. Sin comillas = búsqueda con lematización y stemming.
- Operadores: `AND`, `OR`, `AND NOT` (en mayúsculas). Precedencia con paréntesis.
- Comodín: `*` (varios caracteres), `?` (un carácter). Ej.: `child*` → child, children, childhood.
- Proximidad: `W/n` (n palabras en cualquier orden), `PRE/n` (en orden).
- Los `LIMIT-TO(...)` se aplican normalmente desde las facetas tras lanzar la búsqueda.
```
