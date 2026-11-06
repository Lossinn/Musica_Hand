"""Artículo — primer autor: Alejandro Pemberty Vergara. Hilo: ingeniería de software, reproducibilidad y despliegue responsable hacia el aula."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FP = R["falsos_positivos"]["global_nuevo"]

TITULO_ES = ("De un prototipo a un aula: ingeniería reproducible y condiciones de despliegue responsable de Hand Sing Kids en Montería")
TITULO_EN = ("From a prototype to a classroom: reproducible engineering and responsible deployment conditions for Hand Sing Kids in Montería")
RES_ES = ("Un prototipo educativo que funciona en el computador de sus desarrolladores no está listo para un aula. Se documenta el estado de ingeniería de Hand Sing Kids, una aplicación de escritorio en Python que enseña las ocho notas de Do3 a Do4 "
          "con señas de las manos, y se definen las condiciones para llevarla a una prueba con niños en Montería. El repositorio evaluado tiene 62 módulos y 10.581 líneas, con ocho baterías de prueba que terminaron sin fallos, y las mediciones del "
          "reconocedor se pueden repetir con un solo comando y con semillas fijas. En laboratorio, el reconocimiento fue de "
          f"{f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, y el método disparó una nota por error en {f(FP['pct'])} % de 640 posturas que no son seña. Los datos se guardan en una base local y la aplicación no necesita internet. "
          "Para pasar al aula faltan, en orden, la aprobación ética y el consentimiento de los acudientes, el tratamiento de datos de menores conforme a la normativa colombiana, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición "
          "antes y después. El nivel de madurez es TRL 4; el paso a TRL 5 exige ese piloto.")
RES_EN = ("An educational prototype that works on its developers' computer is not ready for a classroom. The engineering status of Hand Sing Kids, a desktop application in Python that teaches the eight notes from C3 to C4 with hand signs, "
          "is documented, and the conditions for taking it to a test with children in Montería are defined. The evaluated repository has 62 modules and 10,581 lines, with eight test suites that ran without failures, and the recognizer measurements can be repeated "
          f"with a single command and fixed seeds. In the laboratory, recognition was {f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09, and the method fired a wrong note in {f(FP['pct'])} % of 640 non-sign postures. "
          "Data are stored locally and the application needs no internet. Before moving to the classroom, the following are missing, in order: ethical approval and guardians' consent, handling of minors' data under Colombian regulation, "
          "end-to-end latency measurement and a pilot protocol with before-and-after measurement. The readiness level is TRL 4; reaching TRL 5 requires that pilot.")
KW_ES = "reproducibilidad; ingeniería de software; despliegue responsable; datos de menores; madurez tecnológica; educación musical infantil; Montería"
KW_EN = "reproducibility; software engineering; responsible deployment; minors' data; technology readiness; children's music education; Montería"
autores = encabezado("Pemberty", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("El trecho entre «funciona» y «se puede usar»")
T("Un prototipo educativo suele demostrarse con su autor al lado: él sabe cómo iluminar la escena, qué cámara usar y cuándo reiniciar el programa. Un aula no tiene esa persona. Entre la demostración y el uso hay "
  "un trecho de ingeniería que rara vez se documenta: instalación, pruebas, medición reproducible, manejo de datos y condiciones éticas. Este trabajo describe ese trecho para Hand Sing Kids, una aplicación de escritorio que enseña las ocho notas de la "
  "escala con señas de las dos manos, con una cámara y seguimiento de manos {c:mediapipe}.")
T("La literatura sobre IA en educación musical presenta sobre todo resultados de modelos: trayectorias personalizadas {c:li_hong,li_peerj,li_disc,tang,wang}, sistemas con emoción {c:deng_sci,shi}, "
  "retroalimentación en piano {c:deng_piano,chulu}, partituras según dificultad {c:ramoneda}, revisiones {c:yi} y análisis de aplicaciones {c:apay,barroso,leon}. En los títulos revisados no aparece el detalle del "
  "despliegue en un aula concreta; no se leyeron los textos completos, por lo que esa ausencia debe tomarse con cautela.")
T("En Montería, las proyecciones municipales del DANE para 2026 indican 535.052 habitantes, con 80.254 entre 3 y 12 años {c:dane}. No se aporta una estadística local de educación musical; la razón para llevar la herramienta "
  "a un aula de la región es de diseño: funciona sin internet, en un computador con cámara.")
tabla("Tabla 1. Lista de condiciones antes de una prueba con niños",
      ["Condición", "Estado actual", "Quién decide", "Evidencia necesaria"],
      [["Pruebas automáticas", "Cumplida: 8 de 8 baterías sin fallos", "Equipo", "Salida de las pruebas"],
       ["Mediciones reproducibles", "Cumplida: scripts con semillas fijas", "Equipo", "resultados_vision.json"],
       ["Latencia de extremo a extremo", "Pendiente", "Equipo", "Medición con cámara y pantalla reales"],
       ["Aprobación ética", "Pendiente", "Comité de ética", "Acta de aprobación"],
       ["Consentimiento de acudientes", "Pendiente", "Acudientes e institución", "Formatos firmados"],
       ["Tratamiento de datos de menores", "Pendiente", "Equipo y asesor jurídico", "Política de datos y revisión normativa"],
       ["Protocolo de piloto", "Pendiente", "Docente titular", "Diseño con medición antes y después"]],
      "Fuente: elaboración propia.", [4.2, 4.4, 3.2, 4.2])
H2("Objetivo")
T("Documentar el estado de ingeniería de Hand Sing Kids, demostrar que sus mediciones son repetibles y definir las condiciones técnicas y éticas para una prueba piloto con niños.")

H1("Métodos")
bloque("sistema")
H2("Reproducibilidad")
T("Las mediciones del reconocedor están en scripts que se ejecutan con una sola orden, con semillas fijas, y que escriben sus resultados en un archivo estructurado del que el artículo lee sus cifras. La verificación de las referencias se hizo "
  "contra Crossref y DataCite, con fecha de consulta, y no a mano. Cualquier cifra del texto se puede rastrear hasta el script que la produce.")
H1("Resultados")
bloque("res_verif")
H2("Desempeño en laboratorio")
T(f"El reconocimiento de señas válidas fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, sobre 480 señas por nivel. Ante 640 posturas que no son seña, el método disparó una nota por error en {f(FP['pct'])} % de los casos "
  f"(IC 95 %: {f(FP['ic95_lo'])} a {f(FP['ic95_hi'])} %). La calibración es de una sola persona y el ruido es simulado; estos números describen el reconocedor en laboratorio, no en un aula.")

H1("Discusión")
T("**Lo que la repetibilidad permite.** Que cada cifra salga de un script permite que otra persona del equipo, o un revisor, repita la medición y compruebe el resultado. También permitió encontrar diferencias entre la documentación del "
  "proyecto y el código: el número de fotogramas de la suelta, el tamaño del repositorio y el desglose del error entre transiciones y manos cruzadas. En todos los casos prevalece el código, y las diferencias quedan registradas.")
T("**Datos de menores.** La aplicación guarda los intentos de cada niño en una base local. Eso evita enviar datos a un servicio externo, pero no resuelve el problema de qué se guarda y por cuánto tiempo. La Ley 1581 de 2012 de Colombia "
  "regula el tratamiento de datos personales; el equipo debe revisarla con un asesor jurídico antes del piloto y decidir qué es indispensable guardar, con identificadores que no revelen la identidad del niño. La calibración de referencia del estudio "
  "contiene solo coordenadas de puntos de la mano, sin imágenes, precisamente para que no haya fotografías de personas.")
T("**Orden del piloto.** (1) Aprobación del comité de ética y autorización de la institución. (2) Consentimiento de los acudientes y asentimiento de los niños. (3) Medición de latencia y de iluminación en el aula con el equipo real. "
  "(4) Medición inicial de conocimientos de notas, sesiones con la herramienta y medición final, con un grupo que aprenda por el método tradicional como comparación. (5) Registro de las notas falsas y de las señas repetidas con niños "
  "reales. (6) Opinión del docente. Con ese diseño se podría pasar de TRL 4 a TRL 5, y solo entonces hablar de efecto sobre el aprendizaje.")
T("**Límites.** Esta lista de condiciones es una propuesta del equipo, no un protocolo aprobado; la plataforma objetivo documentada incluye macOS, que no se evaluó; y la validez de las mediciones depende de una calibración de una persona y de perturbaciones "
  "simuladas.")
resto("Los componentes de aprendizaje adaptativo del sistema, como el seguimiento del dominio y el repaso espaciado, se fundamentan en trabajos sobre práctica distribuida, seguimiento del conocimiento y estimación estadística")
H1("Conclusiones")
T("Hand Sing Kids tiene un estado de ingeniería verificable: ocho baterías de prueba sin fallos y mediciones repetibles con una sola orden. Eso no basta para llevarlo a un aula. Antes hacen falta la aprobación ética, el consentimiento de los "
  "acudientes, la política de datos de menores, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición antes y después. Hasta entonces, la herramienta está en TRL 4.")
H1("Recomendaciones")
T("(1) Gestionar la aprobación ética y la autorización de una institución aliada. (2) Redactar la política de datos de menores con asesoría jurídica. (3) Medir la latencia de extremo a extremo y la iluminación en el aula. "
  "(4) Probar la instalación en un equipo limpio y en la plataforma macOS documentada. (5) Diseñar el piloto con grupo de comparación.")
from decl_personas import DECL
declaraciones(DECL["pemberty"])
cierre(autores, TITULO_ES, "De un prototipo a un aula: ingeniería reproducible de Hand Sing Kids", Path(sys.argv[1]))
