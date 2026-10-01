# Hand Sing Kids

Aplicación de escritorio que enseña música a niños de 3 a 12 años mediante
señas de las manos. La cámara reconoce el gesto, el gesto se convierte en nota,
la nota se evalúa y el resultado modifica lo que la aplicación propone después.

Todo ocurre en el equipo: no hay conexión a internet, no se graba vídeo y no se
envía nada a ningún servidor.

---

## Instalación en macOS

1. Descomprime la carpeta donde quieras tenerla (por ejemplo, en Documentos).
2. Haz doble clic en **`instalar_mac.command`** y espera a que termine.
3. Haz doble clic en **`iniciar_mac.command`**.

### Si macOS bloquea el archivo

Al descargar un `.command`, macOS lo marca en cuarentena y muestra un aviso de
seguridad. Hay dos salidas:

- Clic derecho sobre el archivo → **Abrir** → **Abrir** de nuevo en el aviso.
- O bien, desde Terminal, dentro de la carpeta del proyecto:

  ```bash
  xattr -dr com.apple.quarantine .
  chmod +x instalar_mac.command iniciar_mac.command
  ```

### Permiso de cámara

La primera vez que arranques, macOS pedirá permiso de cámara **para Terminal**,
que es quien ejecuta la aplicación. Hay que aceptarlo. Si el aviso no aparece y
la cámara no se ve:

**Ajustes del Sistema → Privacidad y seguridad → Cámara → activar Terminal.**

### Requisitos

- macOS con **Python 3.10, 3.11 o 3.12**. MediaPipe todavía no publica versiones
  para 3.13; el instalador lo comprueba y avisa.
- Cámara web (la integrada sirve).
- Unos 700 MB libres para las dependencias.

Instalación manual, si prefieres hacerlo a mano:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Cómo se usa

1. **Crear un perfil.** Nombre, edad y personaje.
2. **Calibrar las señas.** El niño hace cada una de las ocho señas frente a la
   cámara y la aplicación guarda tres muestras de cada una. Es lo único que hay
   que hacer antes de jugar, y se puede repetir cuando se quiera.
3. **Jugar.** Desde el inicio, el botón *Continuar aventura* abre la ruta que el
   optimizador armó para hoy. También se puede elegir nivel y actividad a mano
   desde el mapa. Junto al catálogo fijo, cada ruta incluye actividades nuevas
   generadas para ese niño (marcadas "🤖 generado para ti"): el catálogo va
   creciendo con el progreso en vez de repetirse siempre igual. Una seña
   cuenta apenas se reconoce, sin ninguna espera: no hay ninguna "barra de
   aceptación" que llenar antes de que la nota suene.
4. **Canciones.** Es un módulo aparte, con su propia mecánica: la nota viaja
   por la pantalla hacia una línea de impacto y hay que hacer la seña justo
   cuando llega, en vez de esperar a que el niño reaccione (como en el juego
   original de la primera versión de la aplicación). Ahí solo suena la nota
   que se está pidiendo: si el niño hace otra seña, no suena nada y la nota
   sigue esperando — puede reintentarla cuantas veces quiera mientras siga a
   tiempo, tal como en el juego original — así el sonido confirma el acierto
   en vez de competir con él. Como en ese juego original, la racha y el
   puntaje (con su multiplicador, que crece cada 10 aciertos seguidos) y un
   aviso de "¡Perfecto!"/"¡Bien!"/"Vale" en cada nota completan la mecánica.
   Cada canción del
   catálogo se puede jugar a tres velocidades — 🐢 lento, normal o 🐇 rápido,
   con un botón para cada una junto a "Jugar" — y elegir una más lenta no
   solo separa más las notas: también ensancha su ventana de acierto, así
   que de paso se vuelve menos exigente. Ahí vive el catálogo completo de
   melodías —diecinueve, entre las propias y las tradicionales— y también
   las melodías que el niño grabó en *Modo libre*, que se pueden tocar
   "a mi ritmo" (respetando el tiempo real que dejó entre nota y nota al
   grabarlas) o "a tempo fijo". Las canciones del catálogo cuentan para el
   dominio por nota y para el Agente Adaptativo, igual que cualquier otra
   actividad; las melodías grabadas se tocan solo por diversión y no afectan
   esas estadísticas. Esas mismas canciones del catálogo también se pueden
   tocar paso a paso de siempre desde el mapa de aventura: son la misma
   melodía, con dos formas distintas de jugarla.
5. **Revisar.** *Mi progreso* es la vista del niño; *Zona de padres* muestra el
   dominio por habilidad, las confusiones frecuentes y una recomendación. Al
   terminar cada actividad, la pantalla de resultados muestra también qué
   decidió el **Agente Adaptativo** y por qué. Al principio funciona con
   reglas fijas; en cuanto un perfil acumula unos 40 intentos propios, se
   entrena con sus propios datos (nunca con los de otro perfil ni con datos
   inventados) y se reajusta cada vez que el niño sigue jugando — la pantalla
   de resultados y la Zona de padres siempre dicen si ya está entrenado y con
   cuántos intentos.

### Atajos útiles

- **Modo espejo** (botón ⇄ durante el ejercicio): invierte la imagen. Con algunos
  niños ayuda; con otros confunde. Se prueba y se deja como funcione.
- **Ver la seña** (💡): muestra el dibujo de la seña calibrada por el propio niño.
- **Volver a calibrar**: en Ajustes. Se puede rehacer solo algunas notas; las que
  no se toquen se conservan.
- **Imágenes de las señas en toda la aplicación**: la misma ilustración
  genérica de cada seña se usa en cualquier burbuja de nota suelta —las
  notas que viajan en Canciones, la pista del ejercicio guiado, la fila de
  referencia de Modo libre y la fila de notas de la Calibración—, en vez de
  solo el color y el nombre cantado. Ya vienen incluidas en
  `handsingkids/ui/assets/gestos/` (`DO3.png`, `RE3.png`, `MI3.png`,
  `FA3.png`, `SOL3.png`, `LA3.png`, `SI3.png`, `DO4.png`; también se aceptan
  `.jpg`, `.jpeg` y `.webp` para quien quiera reemplazarlas). Si faltara
  alguna, esa burbuja simplemente se ve como antes: nada se rompe por no
  tenerlas todas. La excepción a propósito es "Ver la seña" y las tarjetas
  de *Mi progreso*: ahí se sigue dibujando la seña que el propio niño
  calibró (personalizada), porque es más útil que una ilustración genérica
  para saber si el reconocedor la va a aceptar.
- **Sonido de cada nota**: por defecto suena una grabación real incluida en
  `handsingkids/ui/assets/audio/` (`nota_DO3.wav` … `nota_DO4.wav`), no el
  timbre sintético — ese solo se usa de respaldo para lo que falte. Una
  familia puede reemplazar cualquiera de estos con los suyos en
  `sonidos_personalizados/` (ver "Dónde se guardan los datos"), que siempre
  tiene la última palabra.
- **Música de fondo**: suena en bucle en las pantallas principales (inicio,
  mapa, progreso, Zona de padres, Ajustes, catálogo de Canciones…) y se
  apaga por completo en cuanto la cámara entra a evaluar gestos —
  calibración, un ejercicio, Modo libre o una canción jugada desde
  Canciones — para que ahí el único sonido sea el de la nota. Falta el
  archivo `musica_fondo.wav`: sin él, esas pantallas quedan en silencio (no
  es un error) hasta que se agregue en `handsingkids/ui/assets/audio/` o en
  `sonidos_personalizados/`.

---

## Qué hacer si algo falla

| Síntoma | Causa probable | Solución |
|---|---|---|
| «No se encontró ninguna cámara» | Permiso denegado, u otra app la está usando | Ajustes del Sistema → Privacidad → Cámara → Terminal. Cerrar Zoom, Meet, Photo Booth |
| La imagen se ve pero no reconoce señas | Falta calibrar, o las manos no se ven completas | Calibrar de nuevo con buena luz y las dos manos dentro del encuadre |
| Confunde dos notas seguido | Esas dos señas quedaron demasiado parecidas al calibrar | Zona de padres → *Detalle técnico* muestra cuáles son. Recalibrarlas más distintas |
| Reconoce notas cuando el niño no hace nada | Exigencia del reconocedor demasiado baja — con el reconocimiento instantáneo de fábrica, una postura ambigua tiene menos filtro que antes | Ajustes → subir *Exigencia del reconocedor*, o subir *Tiempo de sostener la seña* para volver a exigir que se sostenga varios fotogramas |
| Cuesta que acepte una seña correcta | Exigencia demasiado alta, o poca luz | Ajustes → bajar la exigencia, o mejorar la luz. *Tiempo de sostener la seña* ya viene al mínimo (instantáneo) de fábrica |
| Va lento | Equipo justo | La aplicación baja sola a detectar un fotograma de cada dos por debajo de 14 fps |
| Error al instalar mediapipe | Python 3.13 | Instalar Python 3.12 (`brew install python@3.12`) y reinstalar |

Para cualquier problema con la cámara, el diagnóstico rápido es:

```bash
source .venv/bin/activate
python probar_camara.py
```

Dice qué puertos responden, si MediaPipe detecta las manos y a cuántos
fotogramas por segundo va el equipo.

---

## Estructura del proyecto

```
HandSingKids/
├── main.py                      punto de entrada
├── probar_camara.py             diagnóstico de cámara, por si algo falla
├── requirements.txt
├── instalar_mac.command
├── iniciar_mac.command
├── handsingkids/
│   ├── app.py                   contenedor de servicios, ventana y navegación
│   ├── core/                    configuración, tema y bus de eventos
│   ├── domain/                  entidades y notas; sin dependencias externas
│   ├── data/                    SQLite, repositorios, melodías y contenido inicial
│   ├── vision/                  cámara, descriptor, clasificador, estabilizador
│   ├── music/                   síntesis, reproducción y motor musical
│   ├── learning/                evaluación, dominio, repaso, adaptación y nota viajera
│   ├── intelligence/            optimización, gemelo digital y predicción
│   └── ui/                      tema, componentes y pantallas
├── docs/
│   └── documento_tecnico.md     formulación matemática y decisiones de diseño
└── tests/
    ├── test_vision.py           comparación con el método de la versión 1
    ├── test_stabilizer.py
    ├── test_mastery.py
    ├── test_optimizer.py
    ├── test_predictor.py        el modelo entrenable y el generador procedural
    ├── test_audio.py            las tres capas de sonido y la música de fondo
    ├── test_rhythm.py           el motor de nota viajera del módulo Canciones
    ├── test_integracion.py      el ciclo completo, sin cámara y sin ventana
    └── capturas.py              renderiza todas las pantallas sin abrir ventana
```

La regla que organiza todo: **una pantalla no reconoce manos ni decide nada**.
La visión publica eventos, el motor musical los convierte en notas, el evaluador
juzga, el motor de dominio actualiza el perfil y el optimizador elige lo
siguiente. Cada pieza se puede probar sin las demás, y de hecho se prueba así.

---

## Ejecutar las pruebas

```bash
source .venv/bin/activate
python tests/test_vision.py        # incluye la comparación con la versión 1
python tests/test_stabilizer.py
python tests/test_mastery.py
python tests/test_optimizer.py
python tests/test_predictor.py     # fit() converge y el generador procedural
python tests/test_audio.py         # sonidos incluidos/personalizados y música de fondo
python tests/test_rhythm.py        # ventana de acierto y "sigue sin parar" de Canciones
python tests/test_integracion.py   # ciclo completo de extremo a extremo
python tests/capturas.py           # genera una imagen de cada pantalla
```

---

## Dónde se guardan los datos

En `~/Library/Application Support/Hand Sing Kids/`:

- `handsingkids.sqlite3` — perfiles, intentos, resultados, progreso.
- `gestos/perfil_N.json` — las plantillas de señas de cada niño: solo coordenadas
  de puntos, ninguna imagen.
- `audio/` — los sonidos generados en el primer arranque (xilófono sintético,
  de respaldo para lo que no tenga una grabación real incluida ni una propia
  de la familia).
- `sonidos_personalizados/` — aquí una familia puede dejar sus propios archivos
  `.wav` (por ejemplo `nota_DO3.wav` o `musica_fondo.wav`) para reemplazar
  cualquier sonido, incluidas las grabaciones reales que ya trae la
  aplicación en `handsingkids/ui/assets/audio/`; la carpeta trae un
  `LEEME.txt` con los nombres exactos que reconoce la aplicación. Hay que
  reiniciar la aplicación después de agregar un archivo.
- `melodias/` — las canciones que el niño guarda en el modo libre, con su
  duración en segundos, los silencios que agregó y el tiempo real entre cada
  nota y la siguiente (es lo que permite tocarlas "a mi ritmo" en el módulo
  Canciones). Aparecen ahí mismo, en la pantalla Canciones, junto al catálogo.

Borrar esa carpeta deja la aplicación como recién instalada.
