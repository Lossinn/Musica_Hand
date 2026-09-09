# Ruta de Aprendizaje Musical — Hand Sing Music

> **Entregable 1 de 3.** Define *qué* aprende el niño y *en qué orden*.
> Es la fuente de verdad de la que dependen `game.py`, `adaptive/optimizer.py`,
> `adaptive/environment.py`, `adaptive/predictor.py` y el editor de canciones.
> La versión legible por máquina está en [`curriculum.py`](../curriculum.py) y
> **debe** mantenerse sincronizada con este texto. Los tests
> [`tests/test_curriculum.py`](../tests/test_curriculum.py) verifican la coherencia.

---

## 0. Principios de diseño

1. **Dos pilares entrelazados: Notas y Ritmo.** Se alternan. Cuando entra una
   **nota** nueva, el ritmo se queda con figuras ya dominadas; cuando entra una
   **figura rítmica** que subdivide el pulso (corcheas, semicorcheas, puntillo),
   no entra ninguna nota nueva. Así el niño enfrenta **una sola dificultad fuerte
   a la vez**. Excepción: la Etapa 1, que arranca de cero y necesariamente
   presenta las dos primeras notas *y* el pulso.
2. **Un gesto = un sonido.** Sistema monofónico: la mano produce una nota a la
   vez (`recognizer.py`). El ritmo se aprende como *el momento* del gesto, no como
   acordes.
3. **Sin niveles fijos estrictos.** Las **13 etapas** (0–12) son *hitos de
   contenido*: acotan qué notas y figuras están desbloqueadas. La dificultad real
   es **continua** y la ajusta la IA (`adaptive/`, ver §6 y Entregable 2 §11).
   La Etapa 12 (Modo Infinito) no termina.
4. **De lo concreto a lo abstracto.** Primero color y personaje; luego el
   pentagrama; al final lectura a primera vista. Cada etapa indica qué apoyos
   siguen activos.
5. **El número de etapas es ajustable.** Lo que hay que respetar es la
   *estructura* (alternancia Notas/Ritmo, orden de notas Kodály, reglas de
   consolidación y de avance). Se pueden fusionar o dividir etapas siempre que
   `curriculum.py` y sus tests se actualicen juntos.

---

## 1. Convenciones heredadas (NO cambiar sin acuerdo)

| Convención | Valor | Fuente |
|---|---|---|
| Conjunto de notas | `DO3 RE3 MI3 FA3 SOL3 LA3 SI3 DO4` — **octava reducida** de la versión anterior (MusicaManos) | `config.NOTAS` |
| Cierre de octava | `DO4` (mismo nombre que DO3, más agudo) | `config.NOTAS`, `curriculum.DO_AGUDO` |
| Orden de aparición de las notas | `SOL3, MI3, LA3, DO3, RE3, FA3, SI3, DO4` (Kodály: sol-mi primero; fa y si al final) | `curriculum.ORDEN_NOTAS` |
| Correspondencia **gesto → nota** | ✅ **RESUELTO**: cada nota es una **seña de dos manos** que el niño calibra; el reconocedor compara por similitud coseno (umbral `config.GESTURE_SIMILARITY_THRESHOLD = 0.65`) y devuelve la nota de la plantilla más parecida. El gesto que sale ES el nombre de la nota (identidad). | `recognizer.GestureRecognizer`, `calibration.Calibrator`, `curriculum.GESTO_NOTA` |
| Dinámicas de juego | `tutorial`, `libre`, `ritmico`, `reaccion` | `config.DINAMICAS` |
| Dificultad interna | entero `1..5` (knob grueso) + parámetros continuos (§6) | `config.py` |
| Edad objetivo | 3–12 años | `config.EDAD_MIN/MAX` |
| Calibración | El niño calibra sus 8 señas (una vez); se guardan en `data/calibration/<user_id>.json`. Fallback de solo lectura: `pentagrama_calibrado.reference.json` (plantillas de MusicaManos) | `calibration.py` |
| Vocabulario rítmico base | `TA` (negra) / `TITI` (dos corcheas) + aplauso a dos manos | `rhythm/` (de MusicaManos) |

### 1.1 Color de cada nota (provisional)

De la botonera de la imagen de referencia. **Provisional**. En `curriculum.COLOR_NOTA`.

| DO3 | RE3 | MI3 | FA3 | SOL3 | LA3 | SI3 | DO4 |
|---|---|---|---|---|---|---|---|
| rojo/coral | naranja | amarillo | verde | turquesa | azul | morado | rosa |

El color es un **apoyo que se retira gradualmente**, no una propiedad permanente
de la nota.

---

## 2. Vocabulario rítmico (sílabas tipo Kodály)

En `curriculum.py` cada figura es `Figura(nombre, silaba, pulsos, simbolo, subdivide)`.
`subdivide=True` marca las figuras "difíciles" (más de un evento por pulso).

| Figura | Sílaba | Pulsos (4/4) | ¿subdivide? | Entra en |
|---|---|---|---|---|
| Negra | `ta` | 1 | no | Etapa 1 |
| Silencio de negra | `sh` (mano quieta) | 1 | no | Etapa 3 |
| Dos corcheas | `ti-ti` | 1 | **sí** | Etapa 5 |
| Blanca | `ta-a` | 2 | no | Etapa 7 |
| Redonda | `ta-a-a-a` | 4 | no | Etapa 7 (solo cierre de frase) |
| Negra con puntillo + corchea | `ta—i-ti` | 2 | **sí** | Etapa 9 |
| Cuatro semicorcheas | `ti-ri-ti-ri` | 1 | **sí** | Etapa 10 |
| Anacrusa (arranque antes del 1) | — | — | — | Etapa 9 |
| Compás 3/4 (vals) | — | — | — | Etapa 10 |
| Tempo variable (lento/andante/rápido) | — | — | — | Etapa 11 |

**Tolerancia de tiempo** (ventana de acierto): parámetro continuo que la IA
estrecha con el progreso — de ±250 ms (Etapa 1) a ±90 ms (Etapa 11). Ver
`RangoDificultad.tol_ms` por etapa.

---

## 3. Las 13 etapas

Cada etapa: **Notas** · **Ritmo** · **Cómo sube la dificultad** ·
**Qué consolida** · **Apoyos visuales** · **Repertorio**.
(Los valores exactos de tempo, longitud, tolerancia, etc. están en
`curriculum.CURRICULUM[i].rango`.)

> En la prosa de abajo se usan nombres cortos (SOL, MI…); los identificadores
> reales llevan octava (SOL3, MI3…, DO4). Fuente de verdad: `curriculum.py`.

| # | Nombre | Pilar | Nota(s) nueva(s) | Ritmo nuevo |
|--:|---|---|---|---|
| 0 | Conoce tus manos | base | — (calibra SOL3, MI3…) | pulso lento |
| 1 | Dos sonidos | base | **SOL3, MI3** | negra `ta` |
| 2 | Tres sonidos | notas | **LA3** + pentagrama | — |
| 3 | El silencio también suena | ritmo | — | silencio de negra `sh` |
| 4 | La escalera baja | notas | **DO3, RE3** (graves) | — |
| 5 | El eco del ritmo | ritmo | — | dos corcheas `ti-ti` |
| 6 | La escala completa | notas | **FA3, SI3** → escala de 7 | — |
| 7 | Notas que duran | ritmo | — | blanca, redonda |
| 8 | La octava | notas | **DO4** | — |
| 9 | Ritmos con puntillo | ritmo | — | `ta—i-ti` + anacrusa |
| 10 | Vals y carreras | ritmo | — | semicorcheas + 3/4 |
| 11 | Canciones completas | consolida | — | tempo variable, fraseo |
| 12 | Modo Infinito + Compositor | infinito | — | — |

### Etapa 0 — «Conoce tus manos» (calibración, no puntúa)

- **Notas:** ninguna aún. El pingüino hace un gesto y pide imitarlo; se registra
  una referencia por cada nota que usará la Etapa 1 (mín. SOL y MI).
- **Ritmo:** seguir un pulso lento con la mano. Sin evaluación.
- **Sube:** no aplica; se repite hasta calibración estable
  (`calibration.detect_stable_pose`).
- **Consolida:** —
- **Apoyos:** máximos (personaje demuestra, texto corto, color, sonido).
- **Salida:** `data/calibration/<user_id>.json`. A partir de aquí el
  reconocimiento usa *sus* gestos.

### Etapa 1 — «Dos sonidos» · SOL – MI

- **Notas:** reconocer y producir **SOL** y **MI** (tercera menor, "el canto del
  cucú"). Distinguir agudo/grave. Sin pentagrama: burbujas de color.
- **Ritmo:** pulso constante; **negra (`ta`) = 1 pulso**; patrones de 4 negras;
  4/4 como "una caja de 4".
- **Sube:** de 2 gestos a ~60 BPM → 4–6 notas a ~80 BPM; ventana ±250→±180 ms.
- **Consolida:** los gestos de la Etapa 0.
- **Apoyos:** color + nombre hablado + personaje que modela cada nota.
- **Repertorio:** motivos de 2 notas ("cu-cú"), llamada-respuesta.

### Etapa 2 — «Tres sonidos» · + LA · aparece el pentagrama

- **Notas:** añadir **LA**; melodías SOL-MI-LA. Se introduce el **pentagrama**
  (líneas y espacios; SOL en 2.ª línea como ancla).
- **Ritmo:** sin figura nueva — se afianza la negra mientras la atención va a la
  nota nueva.
- **Sube:** +1 nota; primera lectura en pentagrama (color detrás → sin color);
  5–8 eventos.
- **Consolida:** SOL y MI ahora se **leen**, no solo por color; pulso estable.
- **Apoyos:** color al 50 % del tiempo; nombre de nota bajo demanda.
- **Repertorio:** canciones de 3 notas, ostinatos.

### Etapa 3 — «El silencio también suena» · silencio de negra

- **Notas:** consolidar SOL-MI-LA; frases hasta 8 notas; primeros saltos MI↔LA.
- **Ritmo:** **silencio de negra (`sh`)** = 1 pulso de mano quieta; patrones de
  4 tiempos con 1 silencio.
- **Sube:** primera figura de reposo — hay que "no hacer" en el momento justo.
- **Consolida:** lectura de SOL-MI-LA; pulso.
- **Apoyos:** metrónomo visual (el pingüino balancea); color bajo demanda.
- **Repertorio:** ostinatos con silencio, preguntas/respuestas rítmicas.

### Etapa 4 — «La escalera baja» · + DO, RE graves

- **Notas:** añadir **DO** y **RE**. Pentacordo DO-RE-MI-FA-SOL (aún sin FA).
  DO en 1.ª línea adicional inferior ("nota con sombrero"). Grados conjuntos
  DO→SOL.
- **Ritmo:** sin figura nueva — negra y silencio se combinan libremente.
- **Sube:** +2 notas; ámbito de 5; el tricordio pasa a ser el centro de un rango
  mayor.
- **Consolida:** silencio de negra; lectura líneas/espacios.
- **Apoyos:** color bajo demanda; nombres ocultos por defecto.
- **Repertorio:** *Arroz con leche* (fragmento), melodías de pentacordo.

### Etapa 5 — «El eco del ritmo» · dos corcheas

- **Notas:** consolidar el pentacordo DO→SOL con frases de 8–10 notas.
- **Ritmo:** **dos corcheas (`ti-ti`)** = 1 pulso (dos gestos en un tiempo);
  combinar `ta`, `sh`, `ti-ti`. Dinámica **`ritmico`**: eco (el personaje toca,
  el niño repite).
- **Sube:** primera **subdivisión del pulso**; densidad variable; hasta ~104 BPM.
- **Consolida:** pentacordo DO→SOL; silencio de negra.
- **Apoyos:** color solo en notas nuevas del patrón; metrónomo visual.
- **Repertorio:** rimas y juegos de palmas transcritos a gesto.

### Etapa 6 — «La escala completa» · + FA, SI

- **Notas:** añadir **FA** y **SI** (los semitonos) → **escala diatónica completa
  DO-RE-MI-FA-SOL-LA-SI** ascendente y descendente. Grado de la escala (1.º = DO,
  "reposo"). **Todos los gestos calibrados en uso.**
- **Ritmo:** sin figura nueva — `ta` / `sh` / `ti-ti` sobre la escala completa.
- **Sube:** rango completo de 7; los semitonos MI-FA y SI-DO exigen precisión de
  gesto fina.
- **Consolida:** corcheas; pentacordo; lectura fluida.
- **Apoyos:** mínimos — ayuda solo tras un error.
- **Repertorio:** escalas cantadas, *Estrellita* (primera frase).

### Etapa 7 — «Notas que duran» · blanca y redonda

- **Notas:** consolidar la escala de 7 con frases de 10–14 notas y cadencia en DO.
- **Ritmo:** **blanca (`ta-a`)** = 2 pulsos; **redonda** solo para cerrar frase;
  mezclar negra, corchea, silencio y blanca. Sostener la atención sin repetir el
  gesto.
- **Sube:** duraciones largas — el reto es *esperar* sin volver a tocar.
- **Consolida:** escala de 7; corcheas.
- **Apoyos:** ninguno por defecto.
- **Repertorio:** *Arroz con leche* (completa), melodías con finales largos.

### Etapa 8 — «La octava» · + DO4

- **Notas:** **DO agudo** (8.ª tecla). Concepto de **octava** ("mismo nombre, más
  alto"). Saltos de 3.ª, 5.ª y 8.ª además de grados conjuntos.
- **Ritmo:** sin figura nueva — todo el vocabulario rítmico hasta aquí.
- **Sube:** ámbito de octava (8 sonidos); los saltos exigen mayor precisión.
- **Consolida:** escala de 7; blanca y redonda.
- **Apoyos:** ninguno; una "pista" cuesta una estrella.
- **Repertorio:** *Estrellita* (completa), melodías con salto de octava.

### Etapa 9 — «Ritmos con puntillo» · `ta—i-ti` + anacrusa

- **Notas:** consolidar la octava con frases de 12–18 notas.
- **Ritmo:** **negra con puntillo + corchea (`ta—i-ti`)** — ritmo "cojo";
  **anacrusa** (empezar antes del primer tiempo).
- **Sube:** ritmos irregulares y arranques a contratiempo.
- **Consolida:** octava; subdivisión en corcheas.
- **Apoyos:** ninguno.
- **Repertorio:** *Cumpleaños feliz* (con anacrusa), melodías con puntillo.

### Etapa 10 — «Vals y carreras» · semicorcheas + 3/4

- **Notas:** consolidar la octava en dos compases distintos.
- **Ritmo:** **cuatro semicorcheas (`ti-ri-ti-ri`)** en contextos simples;
  **compás de 3/4 (vals)** junto al 4/4; cambiar de compás en una sesión.
- **Sube:** subdivisión más fina + un compás ternario nuevo.
- **Consolida:** puntillo; anacrusa; octava.
- **Apoyos:** ninguno.
- **Repertorio:** valses cortos, *Cumpleaños feliz* (completa).

### Etapa 11 — «Canciones completas» · fraseo y tempo

- **Notas:** piezas reales que usan toda la octava — **Estrellita, Arroz con
  leche, Cumpleaños feliz** (las 3 tarjetas de la imagen). Frase musical y
  cadencia (reposo en DO). Memorizar una canción entera.
- **Ritmo:** combinación libre de todo lo anterior; **tempo variable**
  (lento/andante/rápido); **mantener el tempo** durante 16–24 notas.
- **Sube:** longitud (piezas completas), memoria, estabilidad de tempo medida
  sobre toda la pieza.
- **Consolida:** **todo.**
- **Apoyos:** ninguno; modo "concierto".
- **Repertorio:** las 3 canciones + banco ampliable en `assets/music/`.

### Etapa 12 — «Modo Infinito» + Compositor (sin fin)

- **Notas / Ritmo:** **no entra contenido nuevo.** La IA genera retos combinando
  *solo* lo dominado y mueve de forma continua: tempo · longitud · densidad
  rítmica · proporción de saltos · proporción de lectura a primera vista ·
  tolerancia de tiempo · apoyos visuales · compás.
- **Progresión:** definida enteramente por §6 (predictor + MILP + DQN). Sin
  final: el reto se mantiene en la zona de desarrollo próximo.
- **Editor de canciones** (botón "Crea tus canciones"):
  - **Modo Nivel X:** paleta restringida a las notas y figuras de la etapa
    alcanzada → composición "válida por nivel".
  - **Modo Libre:** paleta completa, sin restricciones, con **grabación**
    (secuencia de gestos + tiempos) y **guardado** en `data/songs/<user_id>/`.
- **Consolida:** el modo infinito *es* consolidación permanente.

---

## 4. Reglas de avance entre etapas

Una etapa se **supera** (y la siguiente se **desbloquea**) cuando, sobre las
últimas `VENTANA_AVANCE = 12` actividades de esa etapa:

| Métrica | Umbral | Fuente |
|---|---|---|
| Precisión de nota (`P_t`) | ≥ 0.85 | `adaptive/profile.StateVector.precision` |
| Tasa de error (`E_t`) | ≤ 0.15 | `profile.error_rate()` |
| Aciertos de tiempo dentro de ventana | ≥ 0.80 | `game.ActivityResult.timing_ok` (campo nuevo) |
| Tendencia | `estable` o `mejorando` | `profile.tendencia` |

Implementado en `curriculum.puede_avanzar(metricas)`; umbrales en
`curriculum.UMBRALES_AVANCE`.

- **Los niveles desbloqueados nunca se bloquean** (requisito del flujo). Si el
  desempeño baja, la IA reduce la dificultad *dentro* de la etapa actual
  (acciones `disminuir_dificultad` / `repetir_actividad` del entorno RL), no
  expulsa al niño de la etapa.
- El niño puede **volver** a cualquier etapa desbloqueada desde la pantalla de
  niveles; la IA recalibra la dificultad a su estado actual.

---

## 5. Mapa Etapa → resto del sistema

| Consumidor | Qué toma del currículo |
|---|---|
| `game.MusicGame.next_activity` | notas activas, figuras activas, compás, dinámica permitida |
| `adaptive/optimizer.py` (MILP) | `notas_disponibles`, `figuras_disponibles`, `dificultad_max`, nº máx. de notas nuevas por sesión, variedad de dinámicas |
| `adaptive/environment.py` (RL) | `introducir_nueva_nota` avanza el puntero de currículo; el estado incluye `etapa` y `dominio` |
| `adaptive/predictor.py` (ML) | `etapa` y `nota_idx` son features de entrada |
| Editor de canciones | `curriculum.paleta_editor(etapa, modo)` |
| Pantalla de niveles (UI) | `N_ETAPAS`, etapa actual, etapas desbloqueadas, progreso dentro de la etapa |

---

## 6. Parámetros continuos que mueve la IA (detalle en Entregable 2 §11)

`curriculum.py` expone por etapa el **rango** de cada parámetro
(`RangoDificultad`); la IA elige el valor puntual. `interpolar_rango(etapa, p)`
suaviza la transición entre etapas.

| Parámetro | Campo | Rango (Etapa 1 → 11) |
|---|---|---|
| Tempo | `bpm` | 60 → 132 |
| Longitud de secuencia | `n_eventos` | 4 → 24 |
| Densidad rítmica (eventos/pulso) | `densidad` | 1.0 → 2.5 |
| Proporción lectura a primera vista | `p_lectura` | 0.0 → 1.0 |
| Proporción de saltos vs. grados conjuntos | `p_salto` | 0.0 → 0.5 |
| Ventana de acierto de tiempo | `tol_ms` | ±250 → ±90 |
| Apoyos visuales (0 = ninguno) | `ayudas` | 3 → 0 |

---

## 7. Qué falta para cerrar este entregable

1. ~~Correspondencia gesto → nota~~ → **RESUELTO** con la versión anterior
   (MusicaManos): señas de dos manos, similitud coseno. Ver §1 e
   `docs/03_integracion_prototipo.md`.
2. ~~Nombre de producto~~ → **Hand Sing Music** (decidido 2026-09-09).
3. Validar el nº de etapas (13) o ajustarlo; la estructura de alternancia y el
   orden de notas no cambian.
4. Fase 4: calibración automática + normalización por escala de mano — las
   plantillas de referencia se solapan bastante (MI3~FA3 ≈ 0.93 en coseno);
   funciona con el argmax pero conviene endurecerlo (umbrales por nota, más
   muestras por seña).
