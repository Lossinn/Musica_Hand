# Plan Fase 0 — Cierre del proyecto, Corte 3 (Gestión Tecnológica)

Fecha del plan: 5 de noviembre de 2026. Estado: **esperando aprobación (punto de control 1)**.

## 1. Inventario de lo que existe

| Insumo | Estado | Ubicación |
|---|---|---|
| Prompt guía + 4 documentos del corte (rúbrica, guía, instrucciones, publicación) | Leídos | `musica_hand/entregables_last/` |
| Código `HandSingKids7` | Presente. Las dos copias (`Hand_kid_Anexoo/` y `03_Codigo/`) son idénticas (diff sin diferencias) | `musica_hand/03_Codigo/HandSingKids7/` |
| `documento_tecnico.md` | 1.352 líneas, secciones 1 a 12 con anexos 11.1 a 11.7 | `Hand_kid_Anexoo/HandSingKids7/docs/` (copia idéntica en `06_Documentos_por_capitulo/Capitulo_6/anexos/`) |
| Pruebas | 8 archivos `test_*.py` (audio, integracion, mastery, optimizer, predictor, rhythm, stabilizer, vision) | `03_Codigo/HandSingKids7/tests/` |
| Entregable 2.º corte (documento EBT 31 págs., póster, modelo financiero, scripts de verificación de DOI) | Presente. Declara TRL 4 | `musica_hand/entregable_2do_corte/` |
| Corpus bibliométrico (189 documentos únicos, 2017-2026) y scripts | Presente, pero es **muestra de conveniencia**, no flujo PRISMA | `04_Datos/bibliometria/` |
| Ecuaciones booleanas de Scopus (2 ecuaciones) | Presentes; **registro de ejecución vacío** (sin fecha ni nº de resultados) | `07_Ecuaciones_booleanas/Scopus/` |
| Pipeline de pruebas Python | Python 3.12.10 disponible en esta máquina | — |

## 2. Huecos de información (bloquean fases)

1. **Preprint manuscrito (escaneo o transcripción): no está en el repositorio.** Los dos `.docx` de la raíz (`Preprint LSTM y Q-Learning… Gastrobar Oxono.docx`, `preprint_parrafos.docx`) son de **otro proyecto** (inventario perecedero, Equipo 6, autor distinto, otra asignatura). No los usé. Sin el preprint no puedo garantizar coherencia de título, problema ni cifras.
2. **Cifras PRISMA** (identificados, duplicados, cribados, excluidos, texto completo, incluidos; bases y ecuación) y **lista de artículos incluidos**: ausentes. El corpus de 189 documentos no equivale a un flujo PRISMA y no lo voy a reconstruir por mi cuenta.
3. **Número de equipo (NN), integrantes con correo/ORCID, orden de autores y fecha límite en Teams.**
4. **Revista objetivo**: no definida (se elige en Fase 1 con tu aprobación).
5. **Confirmación de la EBT**: debo confirmar que Hand Sing Kids (educación musical y tecnología educativa en primera infancia, Montería/Córdoba) es la EBT que presentan.

## 3. Discrepancias detectadas (reporto, no resuelvo)

| # | Discrepancia | Detalle |
|---|---|---|
| D1 | Código de la asignatura | El prompt y los documentos del corte dicen **8830 0048 0**; el LEEME del 2.º corte dice **8830 0064 0**. Confirmar cuál es el vigente. |
| D2 | Tamaño del código | El prompt dice 8.599 líneas en 44 módulos + 999 de pruebas. Conteo rápido hoy: **10.581 líneas en 62 archivos `.py`** de `handsingkids/` y **1.746 líneas** en `tests/`. Se recontará con criterio explícito (¿con comentarios y líneas en blanco?) en Fase 2. |
| D3 | Número de baterías de prueba | El prompt dice cinco; hay ocho archivos de prueba y el LEEME del 2.º corte habla de "8 de 8 suites". |
| D4 | Pruebas inestables | El FALTANTE del 2.º corte registra que `test_integracion.py` agotó 600 s en lote y que `test_rhythm.py` cerró con error 0xc0000409. Hay que reproducirlo y reportarlo. |
| D5 | Tasa de falsos positivos | El 8,0 % (posturas sin seña) aparece en el 2.º corte; falta verificar tamaño de muestra y generar el intervalo de Wilson. |
| D6 | Memoria del proyecto desactualizada | Mi nota previa describe Pygame y la "Fase 4: calibración automática"; el código vigente es PySide6 y `HandSingKids7`. No afecta el artículo, pero indica que `Prototipo/` quedó como versión antigua (el README de `03_Codigo` lo reconoce: "pendiente decidir fusión"). Usaré solo `HandSingKids7`. |
| D7 | Datos regionales del 2.º corte | Varios son de fuente secundaria no verificada (nivelación docente, papelería) y los DANE de Córdoba están "leídos de gráficos". Para el artículo uso solo cifras del DANE que pueda abrir y citar (p. ej. 535.052 habitantes de Montería en 2026 y 80.254 de 3 a 12 años, según el propio FALTANTE) y las re-verifico en la fuente el día de la redacción. |
| D8 | Intervalo Turnitin | La rúbrica premia ≤ 15 %; el umbral de aprobación es ≤ 20 % y máximo 2 % por fuente. Objetivo de diseño: ≤ 15 %. |
| D9 | Reutilización del texto del 2.º corte | El documento EBT y el `documento_tecnico.md` son del mismo equipo y estarán en la base de Turnitin si se subieron. Riesgo de autoplagio: el artículo se redactará de nuevo, no se copiará. |

## 4. Estado de los entregables

| Entregable | Lo produce | Estado |
|---|---|---|
| Preprint manuscrito | Equipo (ya hecho) | **Falta el archivo** para copiarlo al ZIP |
| Certificado Turnitin | Turnitin / institución | PENDIENTE: lo emite Turnitin (solo marcador y guía) |
| Ficha de revista | Yo, con verificación en vivo | Fase 1 |
| Artículo maquetado (PDF + editable) | Yo, con tu revisión | Fases 2 a 5 |
| Constancia de envío | La revista | PENDIENTE: lo emite la revista (solo marcador, guía y paquete de envío) |
| ZIP `02_GT_Corte3_CierreProyecto_EquipoNN.zip` | Yo | Fase 7 |

## 5. Cronograma hacia atrás

La fecha límite no está definida. Con **F = fecha límite en Teams**, los pasos secuenciales son:

| Hito | Plazo | Depende de |
|---|---|---|
| Envío a la revista y captura del acuse | F − 1 día | Visto bueno del docente |
| Visto bueno del docente (vinculación y artículo) | F − 3 días | Turnitin aprobado |
| Turnitin aprobado (≤ 15 % objetivo) | F − 5 días (considerar una repetición si supera el 20 %) | Artículo final |
| Artículo maquetado + prefiltro de similitud (Fases 5 y 6) | F − 8 días | Borrador revisado |
| Borrador revisado por el equipo (punto de control 3) | F − 11 días | Fases 2 a 4 |
| Evidencia técnica reproducible (Fase 2) y PRISMA (Fase 3) | F − 16 días | Preprint, cifras PRISMA, lista de incluidos |
| Revista elegida y plantilla (Fase 1) | F − 18 días | Aprobación de este plan |

Si F está a menos de 18 días, hay que comprimir Fase 1 y 2 en paralelo y eliminar el margen de repetición de Turnitin; lo ajusto cuando me digas F.

## 6. Qué necesito de ti para pasar a la Fase 1

1. Fecha límite F y número de equipo NN.
2. El escaneo del preprint (o su texto) y las cifras PRISMA con la lista de artículos incluidos. Puedes dejarlos en `entrega_corte3/insumos/`.
3. Integrantes con correo institucional y orden de autores (el FALTANTE del 2.º corte menciona dos correos con errores).
4. Confirmar código de asignatura (D1).
5. Confirmar que Hand Sing Kids es la EBT.
6. ¿Ya tienen revista en mente? Si no, empiezo la Fase 1 (puede avanzar sin el preprint).
