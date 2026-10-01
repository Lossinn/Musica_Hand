# Capítulo 6 — notas de revisión

Fuentes incorporadas el 2026-09-30:

- `borrador.md` ← `capitulo_6_gobernanza_de_datos.md` (sin cambios).
- `anexos/documento_tecnico.md` — documento técnico v2.0, la descripción más
  detallada del sistema y la que se toma como referencia.
- `anexos/motor_analitico_y_estado_avance.md` — motor analítico y estado de
  avance.

El código de la v2 (`handsingkids`, con SQLite) no está en este repositorio.
Por eso **no se ha comprobado contra el código** ninguna afirmación del esquema:
restricciones `CHECK`, modo WAL, tabla `skills`, respaldos, purga ni permisos.

## Contradicciones entre documentos, pendientes de resolver

| # | Tema | Cap. 6 / motor analítico | Documento técnico |
|---|------|--------------------------|-------------------|
| 1 | Descriptor | Vector de **38** dimensiones | **120** componentes (58 por mano + 4 entre manos), §3.2 |
| 2 | Clasificador | "Angular", k-NN / coseno | Distancia euclídea ponderada por bloques + softmax con T adaptativa, §3.3–3.4. El coseno era el método v1, descartado |
| 3 | Estabilizador | N = 3 fotogramas; "cero disparos accidentales" | N = 1 de fábrica, `release_frames = 6`; acepta **8 %** de falsos positivos, §3.5, §10, §11.5–11.6 |
| 4 | Fórmula de dominio | Suma: 0,40P + 0,25C + 0,20V + 0,15R | Producto: (λ + (1−λ)R^γ)(0,55P + 0,25C + 0,20V). La suma se descartó explícitamente, §4 |
| 5 | Velocidad | Rango 400–2500 ms | t_ref por edad 5200/4000/3200 ms, t_min 700 ms, §4 |
| 6 | Cámara | 30 FPS | ~24 fps, §3.5 |
| 7 | Exactitud temporal | El recuadro dice "< 35 ms" y la tabla dice "< 5 ms", dentro del mismo cap. 6 | — |
| 8 | Fatiga / frustración | Alerta si F ≥ 0,85; frustración si acierto < 60 % en 3 intentos | Descanso si F ≥ 1; juego si F ≥ 0,7; escalera de ayuda si precisión < 55 %, §6 |
| 9 | Ajuste del predictor | Descenso de gradiente *estocástico* | Descenso de gradiente por lotes (300 épocas, tasa 0,35), §11.2.3 |
| 10 | Módulos | `handsingkids.intelligence.*` | `learning.mastery`, `learning.generator`, `learning.session_flow`… |

## Puntos débiles del propio capítulo 6

- **Ciclo de vida:** la fase activa llega a 90 días y la purga empieza a partir
  de 180. No se dice qué pasa entre los días 90 y 180.
- **Purga frente a predictor:** compactar los intentos en agregados semanales
  destruye los datos de cada intento. `MasteryPredictor` los necesita para
  reentrenarse (§11.2.2), así que la política debe decir cómo conviven.
- **Permisos POSIX 0600/0700:** no aplican en Windows, que es la plataforma de
  desarrollo. Hay que indicar el equivalente (ACL del perfil de usuario).
- **"WAL con escrituras asíncronas no bloqueantes":** WAL no convierte las
  escrituras en asíncronas; permite que haya lecturas mientras se escribe.
  Conviene reformularlo.
- **RBAC:** falta describir cómo se separa el rol Padre/Tutor del rol Niño en
  la interfaz (PIN, gesto de adulto…). Sin ese mecanismo, la matriz es solo una
  declaración.
- **`skill_state.retention`:** el documento técnico calcula R al consultar,
  según los días sin practicar (§8). Hay que aclarar si también se guarda en la
  tabla o si solo se calcula.
