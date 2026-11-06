"""Artículo — primer autor: Juan Diego Guerra Gómez. Hilo: qué cifras se pueden sostener; contraste entre lo reportado y lo medido."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FPG = R["falsos_positivos"]["global_nuevo"]; RB = R["robustez_fp_nuevo"]; LT = R["latencia"]; MX = R["matrices"]

TITULO_ES = ("Lo reportado y lo medido: verificación independiente de las cifras de desempeño de Hand Sing Kids")
TITULO_EN = ("What was reported and what was measured: independent verification of the performance figures of Hand Sing Kids")
RES_ES = ("Los proyectos de ingeniería suelen reportar cifras de desempeño que se copian de un documento a otro sin que nadie las repita. Se contrastan las cifras que la documentación de Hand Sing Kids, una aplicación que enseña "
          "las ocho notas de Do3 a Do4 con señas de las manos, reportaba (30 fotogramas por segundo, precisión superior a 94,2 % en ocho gestos, 38 ms para asignar actividades, 8 % de notas falsas, 2,3 ms de latencia) con mediciones "
          "propias, hechas con scripts reproducibles sobre el código del repositorio. Se reprodujo el 8 % de notas falsas "
          f"({f(FPG['pct'])} %; IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %; estable en 30 semillas: media {f(RB['media'])} %, desviación {f(RB['sd'])}); la latencia del descriptor y el clasificador fue de {f(LT['media_ms'], 2)} ms; y una sesión de ejemplo del optimizador se resolvió en 40 ms. "
          "La precisión de 94,2 % no pudo reproducirse porque el protocolo que la produjo no está documentado; con el protocolo propio, el reconocimiento fue de "
          f"{f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09. Los 30 fotogramas por segundo no se midieron. Además se hallaron seis discrepancias entre documentación y código, que se enumeran. "
          "Se propone una regla para reportar: toda cifra debe indicar el script que la produce, el tamaño de muestra y su intervalo. No hubo pruebas con niños; el nivel de madurez es TRL 4.")
RES_EN = ("Engineering projects often report performance figures that are copied from one document to another without anyone repeating them. The figures that the documentation of Hand Sing Kids, an application that teaches "
          "the eight notes from C3 to C4 with hand signs, reported (30 frames per second, accuracy above 94.2 % on eight gestures, 38 ms to assign activities, 8 % false notes, 2.3 ms latency) are contrasted with our own measurements, made "
          "with reproducible scripts on the repository code. The 8 % false-note rate was reproduced "
          f"({f(FPG['pct'])} %; 95 % CI {f(FPG['ic95_lo'])} to {f(FPG['ic95_hi'])} %; stable across 30 seeds: mean {f(RB['media'])} %, SD {f(RB['sd'])}); descriptor and classifier latency was {f(LT['media_ms'], 2)} ms; and an example optimizer session was solved in 40 ms. "
          "The 94.2 % accuracy could not be reproduced because the protocol that produced it is not documented; with our protocol, recognition was "
          f"{f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09. The 30 frames per second were not measured. Six discrepancies between documentation and code were also found and are listed. "
          "A reporting rule is proposed: every figure should state the script that produces it, the sample size and its interval. No tests with children were done; the readiness level is TRL 4.")
KW_ES = "verificación de resultados; reproducibilidad; métricas de desempeño; intervalos de confianza; trazabilidad; educación musical infantil; Montería"
KW_EN = "results verification; reproducibility; performance metrics; confidence intervals; traceability; children's music education; Montería"
autores = encabezado("Guerra", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("Una cifra sin origen")
T("«Precisión superior al 94,2 %». La frase aparece en resúmenes y presentaciones de Hand Sing Kids, y suena a un resultado. Pero una cifra de desempeño solo es un resultado si se sabe con qué datos se obtuvo, cuántas "
  "pruebas fueron, cómo se contó el acierto y si alguien más puede repetirla. En los proyectos de ingeniería es común que una cifra nazca en un informe, se copie a un resumen y viaje de documento en documento perdiendo su contexto. "
  "Este trabajo propone lo contrario: tomar las cifras reportadas y comprobar, una por una, si se pueden sostener.")
T("La literatura sobre inteligencia artificial en educación musical describe sistemas y resultados de modelos {c:li_hong,li_peerj,li_disc,tang,wang,deng_sci,shi,deng_piano,chulu,ramoneda}, con revisiones generales {c:yi} y estudios "
  "de aplicaciones {c:apay,barroso,leon}. Para estimar incertidumbre de una proporción se usa el intervalo de Wilson {c:wilsonci}; el seguimiento de manos proviene de MediaPipe {c:mediapipe}. Este trabajo no discute el contenido "
  "de esos estudios: aprovecha la práctica de reportar con intervalos y la lleva a un proyecto de clase.")
H2("Qué se reportaba")
tabla("Tabla 1. Cifras reportadas por la documentación o por documentos previos del proyecto",
      ["Cifra reportada", "Origen", "Pregunta de verificación"],
      [["30 fotogramas por segundo", "Documento previo del proyecto", "¿Se puede medir sin cámara y en este equipo?"],
       ["Precisión superior a 94,2 % en ocho gestos", "Documento previo del proyecto", "¿Qué protocolo y cuántas pruebas la produjeron?"],
       ["38 ms para asignar actividades", "Documento previo del proyecto", "¿Qué tarda el optimizador?"],
       ["8 % de notas falsas", "Documentación técnica", "¿Se reproduce y es estable?"],
       ["2,3 ms por fotograma, descriptor y clasificador", "Documento previo del proyecto", "¿Coincide en este equipo?"]],
      "Fuente: documentación del proyecto; las cifras se citan tal como aparecen allí.", [5.0, 4.4, 6.6])
H2("Objetivo")
T("Contrastar con mediciones propias las cifras de desempeño de Hand Sing Kids, registrar las discrepancias entre documentación y código y proponer una regla simple para reportar cifras de forma trazable.")

H1("Métodos")
H2("Regla de verificación")
T("Cada cifra reportada se clasificó en una de cuatro categorías: reproducida (se repitió con un protocolo equivalente y coincide), no comparable (se midió algo distinto), no medida (requiere un equipo del que no se dispone) "
  "o no reproducible (falta el protocolo). Las mediciones se hicieron con scripts que escriben sus salidas en un archivo estructurado y con semillas fijas, en un solo equipo con Windows 11 y Python 3.12.10.")
H2("Protocolo propio")
T("Se usó una calibración de ocho señas de una persona y perturbaciones simuladas de tamaño, giro y ruido. Se midió el reconocimiento de 480 señas válidas por nivel de ruido, las notas disparadas por error en 640 posturas que no son "
  "seña (320 transiciones y 320 combinaciones de manos), la estabilidad de esa tasa con 30 semillas distintas, la latencia del descriptor y el clasificador con 2.000 repeticiones y una sesión de ejemplo del optimizador. Las proporciones "
  "llevan intervalos de Wilson al 95 %.")
H1("Resultados")
H2("Qué se pudo sostener")
tabla("Tabla 2. Cifras reportadas frente a cifras medidas",
      ["Cifra", "Reportado", "Medido en esta evaluación", "Clasificación"],
      [["Notas falsas ante posturas que no son seña", "8 %", f"{f(FPG['pct'])} % (51 de 640; IC 95 %: {f(FPG['ic95_lo'])}–{f(FPG['ic95_hi'])}); 30 semillas: media {f(RB['media'])} %, mín. {f(RB['min'])} %, máx. {f(RB['max'])} %", "Reproducida"],
       ["Latencia del descriptor y el clasificador", "2,3 ms", f"{f(LT['media_ms'], 2)} ms (p95 {f(LT['p95_ms'], 2)} ms; máx. {f(LT['max_ms'], 2)} ms)", "No coincide; otro equipo y otro método"],
       ["Tiempo para asignar actividades", "38 ms", "40 ms en una sesión de ejemplo con CBC", "Mismo orden; una sola ejecución"],
       ["Precisión en ocho gestos", "> 94,2 %", f"{f(A[0]['nuevo']['pct'], 0)} % sin ruido; {f(A[2]['nuevo']['pct'])} % con 0,06; {f(A[3]['nuevo']['pct'])} % con 0,09 (480 señas por nivel)", "No comparable; protocolo original no documentado"],
       ["Fotogramas por segundo", "30", "No medido", "No medida; requiere cámara"]],
      "Fuente: elaboración propia; analisis/resultados_vision.json y salida de las pruebas del repositorio.", [4.0, 2.2, 6.6, 3.2])
T(f"La tasa de notas falsas se reproduce con una precisión notable: {f(FPG['pct'])} % frente al 8 % reportado, y no depende de una semilla favorable, porque con 30 semillas distintas la media fue de {f(RB['media'])} % y el rango, de {f(RB['min'])} a {f(RB['max'])} %. "
  f"La latencia medida, de {f(LT['media_ms'], 2)} ms, es menor que la reportada, pero no puede decirse que la contradiga: el documento previo midió en otro equipo y no queda claro si con el mismo alcance. Ninguna de las dos incluye la captura de la cámara. "
  "El tiempo de 40 ms del optimizador es del mismo orden que el reportado, aunque proviene de una sola sesión.")
T("La cifra de precisión merece una explicación aparte. Un 94,2 % solo tiene sentido con un protocolo: qué señas, de cuántas personas, con qué perturbaciones y cuántas pruebas. Ese protocolo no está en la documentación revisada. Con el "
  f"protocolo propio, el reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09. No son cifras contradictorias, porque miden cosas distintas, y por eso no se declara que la primera sea falsa, "
  "sino que no puede reproducirse ni compararse.")
figura(["reportado_medido.png"], 12.0, "Figura 1. (a) Tasa de notas falsas medida con 30 semillas (media y rango) frente al 8 % reportado. (b) Latencia reportada y medida.")
H2("Discrepancias entre documentación y código")
tabla("Tabla 3. Discrepancias halladas entre la documentación y el código",
      ["Elemento", "Documentación", "Código o medición", "Decisión"],
      [["Fotogramas para considerar soltada una seña", "2 (sección 3.5)", "6", "Prevalece el código"],
       ["Ventana mínima de acierto", "380 ms (sección 11.3.2)", "480 ms; la sección 11.6.2 lo actualiza", "Prevalece el código"],
       ["Tamaño del repositorio", "8.599 líneas, 44 módulos", "10.581 líneas, 62 módulos (8.613 de código efectivo)", "Prevalece la medición"],
       ["Pares de señas similares", "30 de 56", "30 pares ordenados = 15 pares no ordenados de 28", "Aclarado"],
       ["Aceleración progresiva en el método inicial", "Atribuida", "No existía; la velocidad era constante", "Corregido"],
       ["Desglose del 8 % de notas falsas", "No figuraba", "13,8 % en transiciones y 2,2 % en manos cruzadas", "Registrado"]],
      "Fuente: elaboración propia a partir de la revisión del código y de la documentación.", [4.6, 3.6, 5.2, 2.6])

H1("Discusión")
bloque("disc_comp")
T("**Una regla para reportar.** A partir de lo anterior se propone que toda cifra de desempeño que aparezca en un resumen, una presentación o un artículo indique tres cosas: el script o el procedimiento que la produce, el tamaño de la muestra y "
  "su intervalo de confianza. Con esa regla, una frase como «precisión superior al 94,2 %» no pasaría a un resumen sin su protocolo. La regla es sencilla y se puede aplicar en un proyecto de clase.")
resto("Para los componentes de aprendizaje personalizado y estimación del dominio del sistema, véanse los trabajos sobre seguimiento del conocimiento y práctica distribuida")
H2("Madurez tecnológica")
T("Con estas verificaciones, el nivel de madurez que mejor se sostiene es TRL 4: componentes validados en laboratorio, mediciones repetibles y ningún componente probado en el entorno de uso. Las cifras que no se pudieron medir, como los fotogramas por segundo, "
  "deben medirse con la cámara real antes de hablar de TRL 5, que además exige un piloto con niños.")

H1("Conclusiones")
T("De cinco cifras reportadas, una se reprodujo (8 % de notas falsas), una resultó del mismo orden (38 ms), una no coincide pero se midió en otro equipo (latencia), una no pudo compararse por falta de protocolo (94,2 %) y una no se midió "
  "(30 fotogramas por segundo). Además se hallaron seis discrepancias entre documentación y código, resueltas a favor del código y de la medición. El nivel de madurez es TRL 4.")
H1("Recomendaciones")
T("(1) Documentar el protocolo de cualquier cifra de precisión, con su muestra. (2) Medir los fotogramas por segundo con la cámara real. (3) Repetir la medición de latencia en el equipo de aula. (4) Aplicar la regla de reporte "
  "(script, muestra, intervalo) en las presentaciones del proyecto. (5) Mantener actualizada la lista de discrepancias.")
from decl_personas import DECL
declaraciones(DECL["guerra"])
cierre(autores, TITULO_ES, "Lo reportado y lo medido en Hand Sing Kids", Path(sys.argv[1]))
