# Faltante por corroborar o ajustar

Documento interno del equipo. No se incluye en el `.zip` de entrega. Estado al 1 de octubre de 2026.

Leyenda: **[Equipo]** solo el equipo puede resolverlo · **[Corroborar]** dato que debe verificarse con una fuente · **[Ajustar]** decisión o cambio pendiente.

## 0. Cambios de la revisión del 1 de octubre (prevalecen sobre lo que diga más abajo)

- Documento reducido de 59 a 31 páginas (3 preliminares + 25 de cuerpo + 3 de referencias). Se quitaron los anexos A a E, la comparación con el Equipo 13 y la figura de flujo de caja; el detalle sigue en `_fuentes/`.
- APA 7: márgenes de 2,54 cm también en páginas apaisadas; encabezados sin numerar y en mayúsculas y minúsculas; título repetido en la primera página del texto; portada de estudiante **sin logos** (APA no los contempla); figuras y tablas numeradas en orden de mención y todas citadas; texto de figuras ≥ 8 pt.
- Título canónico nuevo (acción + efecto + población + Montería/Córdoba + 2026), igual en documento y póster.
- **Población corregida** con el archivo oficial del DANE (proyecciones municipales post COVID-19): Montería 2026 = 535.052 hab.; 3 a 12 años = 80.254. La cifra anterior (585.029; 93.161) venía de Telencuestas y no coincide con el DANE. Punto 2.5 de abajo: resuelto.
- Córdoba 47,2 % / 25,2 % / 71,9 %: confirmados en el PDF del boletín (posición de etiqueta y valor). Punto 2.4: resuelto.
- BPMN To-Be corregido (faltaban evento de inicio del pool del sistema, flujo entre «Hace la seña» y «Oye la nota», y un mensaje llegaba a un evento de fin). DFD 0: rótulos de los flujos con el acudiente estaban invertidos; corregido. As-Is con nivelación manual y 6 marcas (sobrecosto, cuello de botella, reproceso, registro manual, redundancia, tiempo muerto).
- Pruebas (1 oct.): 7 suites pasan en lote; `test_integracion.py` agotó 600 s en lote y pasa sola en 8,7 s. Así se informa en la Tabla 5. Revisar por qué se cuelga tras el cierre anómalo de `test_rhythm.py` (0xc0000409).
- El `.zip` ahora contiene solo los 3 archivos exigidos (01, 03, 04).
- Sigue pendiente: número de equipo, nombres, fecha real de entrega (`FECHA` en `construir_documento.py`), y borrar el `.xlsx` duplicado de la raíz (bloqueado por Excel).

## 1. Antes de subir a Teams (bloqueantes)

| # | Tipo | Pendiente | Dónde se ve | Cómo cerrarlo |
|---|---|---|---|---|
| 1 | Equipo | Número de equipo (`XX`) en los nombres de archivo y del `.zip` | `entrega_teams/` | Renombrar los 3 archivos y el `.zip`; si se cambia el nombre del proyecto, mantener el patrón `GT_Corte2_Equipo_XX_NombreProyecto.zip` |
| 2 | Equipo | Nombres, códigos y correos institucionales | Portada del documento y encabezado del póster | Editar `TITULO`/`portada()` en `_fuentes/construir_documento.py` y la línea «Equipo XX» en `_fuentes/construir_poster.py`; regenerar |
| 3 | Equipo | Fecha de la portada (hoy figura 30 de septiembre de 2026) | Portada | Poner la fecha real de entrega |
| 4 | Corroborar | Que los DOI de las 15 referencias sigan resolviendo el día de la entrega | Referencias | Ejecutar `_fuentes/verificar_doi.py` |
| 5 | Corroborar | Que el QR del póster abre el repositorio correcto y es accesible para el docente | Póster, sección «Más información» | Escanear con un teléfono; si el repositorio es privado, hacerlo público o dar acceso |
| 6 | Ajustar | El archivo `04_Modelo_Financiero…xlsx` quedó duplicado en la raíz de `entregable_2do_corte/` porque estaba abierto en Excel | Raíz de la carpeta | Cerrar Excel y borrar el que está en la raíz y `~$04_…`; el vigente es el de `entrega_teams/` |

## 2. Por corroborar (datos con respaldo débil)

| # | Dato | Estado | Acción |
|---|---|---|---|
| 1 | Menos del 15 % de los niños tiene instrumento; 1,0 a 1,5 h/semana de nivelación docente; $ 600.000 por aula al año en papelería | Fuente secundaria (estudio del Equipo 13), no verificada; rotulada así en documento y póster | Confirmar con el Equipo 13 o con un docente de Montería/Cereté; si no se confirma, retirar del póster y recalcular beneficios |
| 2 | Beneficios de $ 1.800.000 por aula (valoración del tiempo docente y papelería) | Derivado del punto anterior | Recalcular con `_fuentes/modelo_financiero.py` si cambia algún insumo |
| 3 | 80 horas de ingeniería para el corte, tarifa de $ 30.000/h, 4 aulas por institución | Supuestos del equipo; la tarifa está en el rango de la guía (25.000–40.000) | Validar con el docente; el ROI institucional (71,4 %) depende de las 4 aulas |
| 4 | Hogares de Córdoba con internet, 47,2 % (nacional 65,6 %) | Valores de Córdoba leídos de gráficos del DANE (ENTIC Hogares 2024) | Contrastar con el anexo estadístico oficial del DANE |
| 5 | 93.161 niños de 5 a 14 años en Montería (2026) | Proyecciones del DANE | Confirmar cifra y cohorte en la fuente |
| 6 | Exactitud 100 % sin ruido, 86,0 % con ruido alto, 8,0 % de notas por error en posturas sin seña | Medida sobre la calibración de referencia del prototipo, no con niños | Mantener la redacción «no validado con niños»; medir en el piloto |
| 7 | Latencia: 2,3 ms por fotograma (descriptor y clasificador); solver MILP 0,13 a 1,8 s | Medida en este equipo; la latencia de extremo a extremo (cámara a pantalla) no se midió | Medirla antes de afirmarla en la defensa |
| 8 | Aspectos jurídicos de datos de menores (Ley 1581 de 2012 y reglamentación) | Sin consulta jurídica | Consultar con la oficina jurídica o el docente antes del piloto |

## 3. Por ajustar

| # | Tema | Situación | Acción sugerida |
|---|---|---|---|
| 1 | ROI de un aula | 18,9 % y recuperación en 63,4 meses: **no cumple** la guía (ROI ≥ 30 %, recuperación ≤ 12 meses) | Decidir qué caso se defiende. El documento ya declara el caso base y los seis escenarios; con 4 aulas se obtiene 71,4 % y 16,8 meses, aún sobre los 12 meses. Preparar la justificación para la defensa |
| 2 | Brechas entre gobernanza y código | El código no tiene restricciones CHECK, respaldos, purga, PIN/RBAC y eliminar un perfil no borra sus gestos ni melodías | Están documentadas en los Anexos A y D como propuesta. La migración CHECK se probó (16 restricciones) pero no se aplicó al repositorio; decidir si se aplica antes de la defensa |
| 3 | Nivel de madurez | Se declara TRL 4 (validación en laboratorio) | Mantener; subir a TRL 5 solo tras el piloto |
| 4 | Piloto | Diseñado (protocolo y tamaño de muestra), no ejecutado | Ejecutar o presentarlo como fase siguiente |
| 5 | Capturas del póster | 1440 × 900 px (≈150 dpi a escala de póster); la fuente de la app no cargó al intentar regenerarlas | Capturar de nuevo en una máquina con la fuente instalada y reemplazar `recursos/assets/capturas/`; luego `construir_poster.py` |
| 6 | Logo UPB | Se usó la versión vertical blanca (fondo oscuro) entregada; el póster la muestra sobre su propio fondo | Confirmar con el manual de marca UPB que esa versión es la permitida; si se entrega otra, reemplazar `recursos/assets/logos/upb_logo_vertical_blanco.png` |
| 7 | Documento 02 (BPMN, DFD y gobernanza) | Va insertado en el documento (la instrucción lo permite) y por eso el `.zip` no trae un `02_…pdf` aparte | Confirmar con el docente; si lo exige separado, extraer las secciones 6 a 8 |
| 8 | Impresión del póster | PDF vectorial de una página, 900 × 1200 mm | Pedir prueba de color a la imprenta; el fondo de cartón corrugado puede variar |
| 9 | Referencias del Equipo 13 | Cinco DOI de su estudio no existen o no corresponden y no se usaron | Avisar al Equipo 13 (opcional); el detalle está en el Anexo E |
| 10 | Revisión final contra la rúbrica | Se hizo punto por punto, pero conviene una lectura humana del PDF completo (59 páginas) | Una persona distinta a quien redactó debe leerlo antes de subirlo |

## 4. Cómo regenerar tras un cambio

```
cd entregable_2do_corte/_fuentes
python modelo_financiero.py      # xlsx y figura de flujo
python construir_documento.py    # documento PDF
python construir_poster.py       # póster PDF
python empaquetar.py             # .zip en entrega_teams/
```

Si Edge se cuelga al exportar, terminar los procesos `msedge` y repetir. PuLP debe ser la versión 2.9.0 (la 4.x no trae el solver CBC).
