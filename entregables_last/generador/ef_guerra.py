"""Escrito final — Juan Diego Guerra: lo reportado y lo medido (verificación de cifras)."""
import json
from ef_comun import *

S = json.loads((BASE / "analisis" / "sensibilidad_umbrales.json").read_text(encoding="utf-8"))


def contenido(e):
    resumen = ("Los proyectos de ingeniería suelen reportar cifras de desempeño que pasan de un documento a otro sin que nadie las repita. Este trabajo contrasta las cifras que la documentación de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 con señas de las manos, reportaba "
               "(30 fotogramas por segundo, precisión superior a 94,2 % en ocho gestos, 38 ms para asignar actividades, 8 % de notas falsas y 2,3 ms de latencia) con mediciones propias, hechas con scripts reproducibles sobre el código del repositorio. Se reprodujo el 8 % de notas falsas "
               f"({f(FPG['pct'])} %; IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %; estable en 30 semillas, con media de {f(RB['media'])} % y desviación de {f(RB['sd'], 2)}), la latencia del descriptor y el clasificador fue de {f(LT['media_ms'], 2)} ms y una sesión del optimizador se resolvió en 40 ms. "
               "La precisión de 94,2 % no pudo reproducirse porque el protocolo que la produjo no está documentado, y los 30 fotogramas por segundo no se midieron. Se muestra, además, que una cifra como la de notas falsas depende de un parámetro (el umbral de confianza): con 0,45 sube a 30,3 % y con 0,65 baja a 0,5 %. "
               "Se hallaron seis discrepancias entre documentación y código, resueltas a favor del código. Se propone una regla de reporte: toda cifra debe indicar el script que la produce, el tamaño de la muestra, su intervalo y los parámetros de los que depende. No hubo pruebas con niños; el nivel de madurez es TRL 4.")
    abstract = ("Engineering projects often report performance figures that pass from one document to another without anyone repeating them. This paper contrasts the figures that the documentation of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs, reported "
                "(30 frames per second, accuracy above 94.2 % on eight gestures, 38 ms to assign activities, 8 % false notes and 2.3 ms latency) with our own measurements, made with reproducible scripts on the repository code. The 8 % false-note rate was reproduced "
                f"({f(FPG['pct'])} %; 95 % CI {f(FPG['ic95_lo'])} to {f(FPG['ic95_hi'])} %; stable across 30 seeds, mean {f(RB['media'])} %, SD {f(RB['sd'], 2)}), descriptor and classifier latency was {f(LT['media_ms'], 2)} ms and an optimizer session was solved in 40 ms. "
                "The 94.2 % accuracy could not be reproduced because the protocol that produced it is not documented, and the 30 frames per second were not measured. It is also shown that a figure such as the false-note rate depends on a parameter (the confidence threshold): it rises to 30.3 % at 0.45 and falls to 0.5 % at 0.65. "
                "Six discrepancies between documentation and code were found and resolved in favour of the code. A reporting rule is proposed: every figure should state the script that produces it, the sample size, its interval and the parameters it depends on. No tests with children were done; the readiness level is TRL 4.")
    titulo(e, "Guerra", "Lo reportado y lo medido: verificación independiente de las cifras de desempeño de Hand Sing Kids", resumen,
           "verificación de resultados; reproducibilidad; métricas de desempeño; intervalos de confianza; trazabilidad.", abstract,
           "results verification; reproducibility; performance metrics; confidence intervals; traceability.")

    e.sec("Introducción")
    e.P("«Precisión superior al 94,2 %». La frase aparece en resúmenes y presentaciones de Hand Sing Kids y suena a un resultado. Pero una cifra de desempeño solo es un resultado si se sabe con qué datos se obtuvo, cuántas pruebas fueron, cómo se contó el acierto y si alguien más puede repetirla. "
        "En los proyectos de ingeniería es común que una cifra nazca en un informe, se copie a un resumen y viaje de documento en documento perdiendo su contexto. Este trabajo propone lo contrario: tomar las cifras reportadas y comprobar, una por una, si se pueden sostener.")
    e.P("La literatura sobre inteligencia artificial en educación musical reporta sistemas y resultados de modelos {cite:li_hong,wang,ramoneda,deng_piano} y revisiones generales {cite:yi}. Para estimar la incertidumbre de una proporción se usa el intervalo de Wilson {cite:wilsonci}, y el seguimiento de manos proviene de MediaPipe {cite:mediapipe}. "
        "Este trabajo no discute el contenido de esos estudios: aprovecha la práctica de reportar con intervalos y la lleva a un proyecto de clase, donde la trazabilidad de las cifras es todavía más importante porque el equipo cambia y los documentos se reescriben.")
    e.P("El objetivo es contrastar con mediciones propias las cifras de desempeño de Hand Sing Kids, registrar las discrepancias entre documentación y código, mostrar de qué parámetros depende una de esas cifras y proponer una regla simple para reportar cifras de forma trazable.")

    e.sec("Contexto general")
    e.P("Hand Sing Kids reconoce ocho señas de las dos manos con una cámara y MediaPipe Hands, estima el dominio de cada nota y elige la siguiente sesión. La documentación técnica y presentaciones previas del proyecto reportan indicadores que se resumen en el cuadro siguiente.")
    e.tabla("rep", "Cifras reportadas por la documentación o por documentos previos del proyecto.", ["Cifra reportada", "Origen", "Pregunta de verificación"],
            [["30 fotogramas por segundo", "Documento previo", "¿Se puede medir sin cámara?"], ["Precisión > 94,2 % en ocho gestos", "Documento previo", "¿Qué protocolo y cuántas pruebas la produjeron?"], ["38 ms para asignar actividades", "Documento previo", "¿Cuánto tarda el optimizador?"],
             ["8 % de notas falsas", "Documentación técnica", "¿Se reproduce y es estable?"], ["2,3 ms por fotograma", "Documento previo", "¿Coincide en este equipo?"]], [3.1, 2.2, 3.2], size=8)
    e.sub("Supuestos y alcance")
    e.B(["Todo se midió en **un equipo** con Windows 11 y Python 3.12.10 (NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21), sin registro de su procesador.",
         "La calibración es de **una persona** y las perturbaciones son simuladas.",
         "Una cifra «no reproducible» no es una cifra falsa: significa que falta el protocolo para repetirla.",
         "No se midió nada que requiera la cámara en funcionamiento ni la pantalla.",
         "Se adopta el valor del código o de la medición cuando hay diferencia con la documentación."])

    e.sec("Método de verificación")
    e.sub("Clasificación de las cifras")
    e.tabla("cat", "Categorías de verificación.", ["Categoría", "Significado"],
            [["Reproducida", "Se repitió con un protocolo equivalente y coincide"], ["No comparable", "Se midió algo distinto de lo reportado"], ["No medida", "Requiere un equipo del que no se dispone"], ["No reproducible", "Falta el protocolo para repetirla"]], [2.4, 6.1], size=8.5)
    e.sub("Protocolo propio")
    e.P("Se usó una calibración de ocho señas de una persona, con perturbaciones simuladas de tamaño, giro y ruido. Se midió el reconocimiento de 480 señas válidas por nivel de ruido, las notas disparadas por error ante 640 posturas que no son seña (320 transiciones y 320 combinaciones de manos), la estabilidad de esa tasa con 30 semillas distintas, "
        "la latencia del descriptor y el clasificador con 2.000 repeticiones y una sesión de ejemplo del optimizador. Las proporciones llevan intervalos de Wilson al 95 %:")
    e.eq("wilson", r"\mathrm{IC}_{95\,\%}=\frac{\hat p+\dfrac{z^2}{2n}\pm z\sqrt{\dfrac{\hat p(1-\hat p)}{n}+\dfrac{z^2}{4n^2}}}{1+\dfrac{z^2}{n}}")
    e.sub("Regla de reporte")
    e.P("Se propone que toda cifra de desempeño que aparezca en un resumen, una presentación o un artículo indique cuatro cosas: el script o procedimiento que la produce, el tamaño de la muestra, su intervalo de confianza y los parámetros de los que depende.")

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Lo reportado frente a lo medido")
    e.tabla("rm", "Cifras reportadas frente a cifras medidas.", ["Cifra", "Reportado", "Medido", "Estado"],
            [["Notas falsas, 640 posturas", "8 %", f"{f(FPG['pct'])} % (51 de 640)", "Reproducida"], ["Latencia descriptor y clasificador", "2,3 ms", f"{f(LT['media_ms'], 2)} ms", "No coincide; otro equipo"],
             ["Tiempo para asignar actividades", "38 ms", "40 ms (una sesión)", "Mismo orden"], ["Precisión en ocho gestos", "> 94,2 %", f"{f(A[0]['nuevo']['pct'], 0)} % a {f(A[3]['nuevo']['pct'])} % según el ruido", "No comparable"], ["Fotogramas por segundo", "30", "No medido", "No medida"]],
            [2.5, 1.5, 2.5, 2.0], size=8)
    e.P(f"La tasa de notas falsas se reproduce con precisión: {f(FPG['pct'])} % frente al 8 % reportado, y no depende de una semilla favorable, porque con 30 semillas distintas la media fue de {f(RB['media'])} % y el rango, de {f(RB['min'])} a {f(RB['max'])} % ({{fig:rm}}). "
        f"La latencia medida, de {f(LT['media_ms'], 2)} ms, es menor que la reportada, pero no puede decirse que la contradiga: el documento previo midió en otro equipo y no consta que con el mismo alcance. Ninguna de las dos incluye la captura de la cámara. El tiempo de 40 ms del optimizador es del mismo orden que el reportado, aunque proviene de una sola sesión.")
    e.figura("rm", "reportado_medido.png", "(a) Tasa de notas falsas medida con 30 semillas (media y rango) frente al 8 % reportado. (b) Latencia reportada y medida.", 8.3)
    e.P(f"La cifra de precisión merece una explicación aparte. Un 94,2 % solo tiene sentido con un protocolo: qué señas, de cuántas personas, con qué perturbaciones y cuántas pruebas. Ese protocolo no está en la documentación revisada. Con el protocolo propio, el reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09. "
        "No son cifras contradictorias, porque miden cosas distintas; por eso no se declara que la primera sea falsa, sino que no puede reproducirse ni compararse.")
    e.sub("Una cifra depende de sus parámetros")
    c = S["confidence_threshold"]
    filas = [[f(r["valor"], 2), f(r["ac_009"]), f(r["fp"])] for r in c]
    e.tabla("par", "Dependencia de las notas falsas y del reconocimiento con ruido 0,09 respecto del umbral de confianza (%).", ["Confianza mínima", "Reconocimiento", "Notas falsas"], filas, [2.6, 2.6, 2.6], alinear=["l", "r", "r"])
    e.P("El 8 % reportado corresponde a un umbral de confianza de 0,55. Con 0,45 la misma medición da 30,3 % de notas falsas y con 0,65 da 0,5 %, aunque a costa de bajar el reconocimiento con ruido alto de 86,0 % a 66,0 %. Una cifra sin su umbral es, por tanto, incompleta: dos equipos podrían reportar «8 %» y «0,5 %» sobre el mismo sistema. "
        "Esto justifica el cuarto elemento de la regla de reporte.")
    e.sub("Discrepancias entre documentación y código")
    e.tabla("disc", "Discrepancias halladas entre la documentación y el código.", ["Elemento", "Documentación", "Código o medición"],
            [["Fotogramas para soltar una seña", "2 (sección 3.5)", "6"], ["Ventana mínima de acierto", "380 ms (sección 11.3.2)", "480 ms; la sección 11.6.2 lo actualiza"], ["Tamaño del repositorio", "8.599 líneas, 44 módulos", "10.581 líneas, 62 módulos"],
             ["Pares de señas similares", "30 de 56", "30 pares ordenados = 15 no ordenados de 28"], ["Aceleración en el método inicial", "Atribuida", "No existía; la velocidad era constante"], ["Desglose del 8 % de notas falsas", "No figuraba", "13,8 % en transiciones; 2,2 % en manos cruzadas"]],
            [3.0, 2.5, 3.0], size=8)
    e.P("En todos los casos se adoptó el valor del código o de la medición, y las diferencias quedan registradas.")

    e.sub("Trazabilidad de las cifras")
    e.P("Aplicando la regla propuesta, cada cifra remite a su origen en el cuadro siguiente.")
    e.tabla("traza", "Origen de las cifras principales.", ["Cifra", "Origen"], [['8 % de notas falsas y 30 semillas', 'resultados_vision.json'], ['Latencia', 'resultados_vision.json'], ['40 ms del optimizador', 'salida_pruebas.txt'], ['Dependencia del umbral de confianza', 'sensibilidad_umbrales.json'], ['Cifras reportadas', 'Documentación y documentos previos del proyecto'], ['Discrepancias', 'Revisión del código y la documentación']], [3.4, 5.1], size=8)

    e.sec("Conclusiones")
    e.P("De cinco cifras reportadas, una se reprodujo (8 % de notas falsas), una resultó del mismo orden (38 ms), una no coincide pero se midió en otro equipo (latencia), una no pudo compararse por falta de protocolo (94,2 %) y una no se midió (30 fotogramas por segundo). Se mostró además que la tasa de notas falsas depende del umbral de confianza, "
        "y se hallaron seis discrepancias entre documentación y código, resueltas a favor del código y de la medición.")
    e.P("Como líneas de trabajo se identifican cinco: documentar el protocolo de cualquier cifra de precisión con su muestra; medir los fotogramas por segundo con la cámara real; repetir la medición de latencia en el equipo del aula; aplicar la regla de reporte (script, muestra, intervalo y parámetros) en las presentaciones del proyecto; y mantener actualizada la lista de discrepancias. El nivel de madurez es TRL 4.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
