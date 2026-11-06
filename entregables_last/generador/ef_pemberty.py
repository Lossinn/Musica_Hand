"""Escrito final — Alejandro Pemberty: ingeniería reproducible y despliegue responsable."""
from ef_comun import *


def contenido(e):
    resumen = ("Un prototipo educativo que funciona en el computador de sus desarrolladores no está listo para un aula. Este trabajo documenta el estado de ingeniería de Hand Sing Kids, una aplicación de escritorio en Python que enseña las ocho notas de Do3 a Do4 con señas de las manos, "
               "y define las condiciones para llevarla a una prueba con niños en Montería. El repositorio evaluado tiene 62 módulos y 10.581 líneas, con ocho baterías de prueba que terminaron sin fallos, y las mediciones del reconocedor se pueden repetir con un solo comando y con semillas fijas. "
               f"En laboratorio, el reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, y el método disparó una nota por error en {f(FPG['pct'])} % de 640 posturas que no son seña. "
               "Se evalúa el nivel de madurez tecnológica con evidencia por nivel y se organizan las condiciones previas al piloto en una lista verificable: aprobación ética, consentimiento de acudientes, política de datos de menores conforme a la normativa colombiana, "
               "medición de la latencia de extremo a extremo y un protocolo con medición antes y después. El nivel de madurez es TRL 4; el paso a TRL 5 exige ese piloto.")
    abstract = ("An educational prototype that works on its developers' computer is not ready for a classroom. This paper documents the engineering status of Hand Sing Kids, a desktop application in Python that teaches the eight notes from C3 to C4 with hand signs, "
                "and defines the conditions for taking it to a test with children in Montería. The evaluated repository has 62 modules and 10,581 lines, with eight test suites that ran without failures, and the recognizer measurements can be repeated with a single command and fixed seeds. "
                f"In the laboratory, recognition was {f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09, and the method fired a wrong note in {f(FPG['pct'])} % of 640 non-sign postures. "
                "The technology readiness level is assessed with evidence per level and the conditions before a pilot are organized into a verifiable list: ethical approval, guardians' consent, a minors' data policy under Colombian regulation, end-to-end latency measurement and a protocol with before-and-after measurement. "
                "The readiness level is TRL 4; reaching TRL 5 requires that pilot.")
    titulo(e, "Pemberty", "De un prototipo a un aula: ingeniería reproducible y condiciones de despliegue responsable de Hand Sing Kids en Montería", resumen,
           "reproducibilidad; ingeniería de software; madurez tecnológica; datos de menores; despliegue responsable; Montería.", abstract,
           "reproducibility; software engineering; technology readiness; minors' data; responsible deployment; Montería.")

    e.sec("Introducción")
    e.P("Un prototipo educativo suele demostrarse con su autor al lado: él sabe cómo iluminar la escena, qué cámara usar y cuándo reiniciar el programa. Un aula no tiene esa persona. Entre la demostración y el uso hay un trecho de ingeniería que rara vez se documenta: instalación, pruebas, medición reproducible, manejo de datos y condiciones éticas. "
        "Este trabajo describe ese trecho para Hand Sing Kids, una aplicación que enseña las ocho notas de la escala con señas de las dos manos, con una cámara y seguimiento de manos {cite:mediapipe}.")
    e.P("La literatura sobre inteligencia artificial en educación musical y en primera infancia describe sobre todo sistemas y resultados de modelos {cite:yi}, y los estudios sobre aplicaciones musicales analizan su uso y su evaluación {cite:apay,barroso,leon}. En los títulos revisados no aparece el detalle del despliegue en un aula concreta; no se leyeron los textos completos, por lo que esa ausencia debe tomarse con cautela. "
        "Este trabajo se centra en lo que el equipo puede afirmar con lo que midió y en lo que falta para dar el siguiente paso con niños.")
    e.P("El objetivo es documentar el estado de ingeniería del prototipo, mostrar que sus mediciones son repetibles, evaluar su nivel de madurez tecnológica con evidencia por nivel y definir las condiciones técnicas y éticas para una prueba piloto.")

    e.sec("Contexto general")
    e.sub("El sistema y su entorno")
    e.P("La aplicación es de escritorio, escrita en Python con interfaz en PySide6, y guarda los intentos de cada niño en una base SQLite local, de modo que no necesita conexión a internet. El repositorio evaluado contiene 62 módulos con 10.581 líneas (8.613 de código efectivo, sin líneas en blanco ni comentarios) "
        "y 9 archivos de pruebas con 1.746 líneas, organizados en ocho baterías: audio, integración, dominio, optimizador, predictor, canciones, estabilizador y visión. La plataforma objetivo documentada incluye macOS y Python 3.10 a 3.12.")
    e.sub("Población de referencia")
    e.P("Según las proyecciones municipales del DANE, la población de Montería en 2026 es de 535.052 habitantes, y 80.254 tienen entre 3 y 12 años {cite:dane}. No se aporta una estadística local de educación musical; la razón para llevar la herramienta a un aula de la región es de diseño: funciona sin internet, en un computador con cámara.")
    e.sub("Supuestos y alcance")
    e.B(["Las mediciones se hicieron en **un solo equipo** con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0; **no** se evaluó macOS ni otras versiones de Python.",
         "La calibración de referencia es de **una persona** y las perturbaciones son simuladas.",
         "La lista de condiciones previas al piloto es **una propuesta del equipo**, no un protocolo aprobado.",
         "La normativa sobre datos personales se menciona como marco y **no** sustituye la asesoría jurídica.",
         "No hubo pruebas con niños."])

    e.sec("Marco de ingeniería")
    e.sub("Reproducibilidad")
    e.P("Las mediciones del reconocedor están en scripts que se ejecutan con una sola orden, con semillas fijas, y que escriben sus resultados en un archivo estructurado del que el artículo lee sus cifras. La verificación de las referencias se hizo contra Crossref y DataCite, con fecha de consulta, y no a mano. "
        "Cualquier cifra del texto puede rastrearse hasta el script que la produce. Esto permitió, además, encontrar diferencias entre la documentación del proyecto y el código, que se listan en el apartado de resultados.")
    e.sub("Madurez tecnológica")
    e.tabla("trl", "Evidencia por nivel de madurez tecnológica.", ["TRL", "Criterio", "Evidencia", "Estado"],
            [["1–2", "Concepto y aplicación formulados", "Documentos del proyecto", "Cumplido"], ["3", "Prueba de concepto analítica", "Modelos y fórmulas implementados", "Cumplido"],
             ["4", "Validación de componentes en laboratorio", "8 baterías sin fallos; mediciones repetibles", "Cumplido"], ["5", "Validación en entorno relevante", "Piloto con niños en aula", "Pendiente"], ["6", "Prototipo en entorno relevante", "Uso por docentes y niños", "Pendiente"]],
            [0.9, 3.0, 3.2, 1.4], size=8)
    e.P("Se propone TRL 4. La evidencia a favor es que los componentes funcionan integrados en una aplicación ejecutable y que sus mediciones son repetibles. En contra de un nivel superior, ningún componente se validó en el entorno de uso, con niños, cámaras y luz reales.")
    e.sub("Condiciones previas al piloto")
    e.figura("flujo", "flujo_condiciones.png", "Condiciones previas al piloto, en orden. Verde: cumplido; naranja: pendiente.", 7.6)

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Pruebas y mediciones")
    e.P("Las ocho baterías terminaron con código de salida 0. En el optimizador, la prueba que compara la solución del solucionador con la enumeración exacta pasó, y la sesión de ejemplo se resolvió en 40 ms. En la primera ejecución, en la consola con la codificación predeterminada de Windows, dos errores de impresión de caracteres especiales "
        "impidieron terminar; no eran de lógica, y con la salida en UTF-8 las ocho pasaron.")
    e.tabla("medidas", "Mediciones del reconocedor en laboratorio, reproducibles con un solo comando.", ["Medida", "Resultado"],
            [["Señas válidas, sin ruido", f"{f(A[0]['nuevo']['pct'], 0)} % (480 de 480)"], ["Señas válidas, ruido 0,09", f"{f(A[3]['nuevo']['pct'])} % ({A[3]['nuevo']['k']} de 480)"],
             ["Notas falsas, 640 posturas", f"{f(FPG['pct'])} % (IC 95 %: {f(FPG['ic95_lo'])}–{f(FPG['ic95_hi'])})"], ["Estabilidad con 30 semillas", f"media {f(RB['media'])} %; rango {f(RB['min'])}–{f(RB['max'])} %"],
             ["Descriptor y clasificador", f"{f(LT['media_ms'], 2)} ms por fotograma"]], [4.4, 4.1], size=8.5)
    e.P("Estos números describen el reconocedor en laboratorio, no en un aula. La latencia no incluye la captura de la cámara, el rastreo de MediaPipe ni el dibujo en pantalla.")
    e.sub("Discrepancias entre documentación y código")
    e.tabla("disc", "Algunas discrepancias halladas y su decisión.", ["Elemento", "Documentación", "Código o medición"],
            [["Fotogramas para soltar una seña", "2", "6"], ["Tamaño del repositorio", "8.599 líneas, 44 módulos", "10.581 líneas, 62 módulos"], ["Desglose del 8 % de notas falsas", "No figuraba", "13,8 % en transiciones; 2,2 % en manos cruzadas"]], [3.4, 2.5, 2.6], size=8.5)
    e.P("En todos los casos prevalece el código o la medición, y las diferencias quedan registradas.")
    e.sub("Datos de menores")
    e.P("La aplicación guarda los intentos de cada niño en una base local. Eso evita enviar datos a un servicio externo, pero no resuelve qué se guarda ni por cuánto tiempo. La Ley 1581 de 2012 regula en Colombia el tratamiento de datos personales; el equipo debe revisarla con un asesor jurídico antes del piloto y decidir qué es indispensable guardar, "
        "con identificadores que no revelen la identidad del niño. La calibración de referencia contiene solo coordenadas de puntos de la mano, sin imágenes, precisamente para que no haya fotografías de personas.")
    e.sub("Protocolo del piloto")
    e.tabla("fases", "Fases propuestas para el piloto.", ["Fase", "Contenido", "Responsable"],
            [["1", "Aprobación ética y autorización de la institución", "Comité y equipo"], ["2", "Consentimiento de acudientes y asentimiento de los niños", "Equipo e institución"], ["3", "Medición de latencia e iluminación con el equipo del aula", "Equipo"],
             ["4", "Medición inicial, sesiones con la herramienta y medición final; grupo con método tradicional", "Docente titular"], ["5", "Registro de notas falsas y señas repetidas con niños; opinión del docente", "Equipo y docente"]], [0.9, 5.3, 2.3], size=8)
    e.P("Con ese diseño se podría pasar de TRL 4 a TRL 5 y solo entonces hablar de efecto sobre el aprendizaje.")

    e.sec("Conclusiones")
    e.P("Hand Sing Kids tiene un estado de ingeniería verificable: ocho baterías de prueba sin fallos y mediciones repetibles con una sola orden. Eso no basta para llevarlo a un aula. Antes hacen falta la aprobación ética, el consentimiento de los acudientes, la política de datos de menores, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición antes y después. Hasta entonces, la herramienta está en TRL 4.")
    e.P("Como líneas de trabajo se identifican cinco: gestionar la aprobación ética y la autorización de una institución aliada; redactar la política de datos de menores con asesoría jurídica; medir la latencia de extremo a extremo y la iluminación en el aula; probar la instalación en un equipo limpio y en macOS; y diseñar el piloto con grupo de comparación.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
