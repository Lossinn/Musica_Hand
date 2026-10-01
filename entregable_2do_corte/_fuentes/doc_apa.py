"""Cuerpo del documento EBT en APA 7 (trabajo de estudiante), estructura IMRyD.

Orden según la instrucción del segundo corte: título canónico, resumen y abstract, diagnóstico y brecha,
arquitectura y prototipo (MVP), BPMN 2.0, DFD 0-1-2, gobernanza DAMA-DMBOK, viabilidad financiera.
Encabezados sin numeración (APA 7, sección 2.27); las referencias cruzadas usan el nombre del apartado.
Reglas SILOGE: tercera persona, cursiva para conceptos técnicos, sin negrita en el cuerpo, siglas entre
comas en su primer uso y «optimización» solo junto a la formulación MILP.
"""
from __future__ import annotations

import json
from pathlib import Path

import modelo_financiero as MF
from datos import BENCH, CAT, DANE, ESC, FIN, TOT, cita, cop, n, pct, referencias_ordenadas
from doc_base import H1, H2, P, UL, ecuacion, figura, img, svg_inline, tabla

F = Path(__file__).resolve().parent
AUD = json.loads((F / "auditoria_calidad.json").read_text(encoding="utf-8"))
CON = json.loads((F / "contraste_pint2.json").read_text(encoding="utf-8"))
PRUEBAS = json.loads((F / "pruebas.json").read_text(encoding="utf-8"))
B1, INST, ESCA = ESC[MF.ESC_BASE], ESC[MF.ESC_INST], ESC[MF.ESC_ESCALA]
PAR = FIN["parametros"]
MILP = CON["solver_milp_cbc_ms"]
BRECHA = DANE["hog_internet_nal"] - DANE["hog_internet_cor"]


# ============================================================ introducción
def introduccion(titulo: str) -> str:
    h = [f'<h1 class="salto">{titulo}</h1>']
    h.append(P(
        "Hand Sing Kids, HSK, es una aplicación de escritorio que enseña las ocho notas del solfeo, de DO3 a DO4, a niños "
        "de 3 a 12 años mediante señas de las manos que una cámara reconoce. Cada seña se convierte en una nota, la nota "
        "se evalúa y el resultado modifica la actividad siguiente. Todo el procesamiento ocurre en el equipo del usuario: "
        "no se graba video y ningún dato sale hacia servidores externos."))
    h.append(P(
        "El proyecto se plantea como <em>Empresa de Base Tecnológica</em>, EBT, en la asignatura Gestión Tecnológica, GT, "
        "de la Universidad Pontificia Bolivariana, Seccional Montería. El documento consolida la ingeniería de detalle "
        "del segundo corte: el diagnóstico de la brecha tecnológica, el prototipo funcional mínimo, <em>Minimum Viable "
        "Product</em>, MVP, el modelado de procesos en <em>Business Process Model and Notation</em>, BPMN 2.0, los "
        "diagramas de flujo de datos, DFD, la gobernanza de datos y la evaluación financiera. Las cifras técnicas se "
        "comprobaron en el código y en pruebas ejecutadas; las financieras dependen de supuestos que se declaran como tales."))
    h.append(H2("Planteamiento del problema"))
    h.append(P(
        "El aprendizaje de las notas musicales requiere retroalimentación inmediata y repaso a intervalos adecuados. En "
        "un aula, el docente atiende a muchos niños a la vez, evalúa de forma manual y no conserva un registro por nota "
        "que le permita decidir qué reforzar. La [[F:arbol]] organiza el problema central con sus causas y efectos; una de "
        "las causas es la conectividad: en 2024 solo el "
        f"{n(DANE['hog_internet_cor'], 1)} % de los hogares de Córdoba tenía internet, frente al "
        f"{n(DANE['hog_internet_nal'], 1)} % nacional (Departamento Administrativo Nacional de Estadística [DANE], 2025)."))
    h.append(figura("Árbol de problemas de la enseñanza de notas musicales en niños de Montería", svg_inline("arbol_problemas"),
                    "Elaboración propia. La causa de conectividad proviene de DANE (2025); las de atención y evaluación "
                    "corresponden al proceso actual modelado en BPMN; la última es la brecha hallada en la revisión de la literatura.",
                    ref="arbol"))
    h.append(H2("Pregunta de investigación y objetivos"))
    h.append(P(
        "La pregunta que orienta el proyecto es: ¿en qué medida un sistema local que reconoce señas manuales y planifica "
        "de forma adaptativa la práctica puede ofrecer retroalimentación individual inmediata y un registro objetivo del "
        "dominio de las notas musicales en niños de 3 a 12 años de Montería? El objetivo general es <em>diseñar, construir "
        "y verificar técnicamente</em> un prototipo que reconozca las señas de las ocho notas y adapte la práctica de cada "
        "niño, y evaluar su viabilidad financiera. Los objetivos específicos, OE, son:"))
    h.append(UL([
        "OE1: diagnosticar la brecha tecnológica regional con indicadores oficiales y revisar la literatura reciente;",
        "OE2: construir el prototipo, con reconocimiento de señas, gemelo digital del aprendiz, planificación adaptativa "
        "y gobernanza local de los datos;",
        "OE3: verificar el desempeño técnico del prototipo y estimar el retorno de la inversión con supuestos explícitos."]))
    h.append(H2("Justificación"))
    h.append(P(
        "El diseño se orienta a tres Objetivos de Desarrollo Sostenible, ODS: el 4, educación de calidad, por la práctica "
        "individual con seguimiento; el 9, industria, innovación e infraestructura, por tratarse de tecnología que funciona "
        "sin nube en un territorio con conectividad desigual; y el 10, reducción de las desigualdades, porque solo requiere "
        "un computador y una cámara web. Se trata de una orientación del diseño, no de un impacto medido."))
    return "".join(h)


# ============================================================ diagnóstico
def diagnostico() -> str:
    h = [H1("Diagnóstico y brecha tecnológica")]
    h.append(H2("Fuentes y método"))
    h.append(P(
        "Los indicadores provienen del boletín técnico de la Encuesta de Tecnologías de la Información y las Comunicaciones "
        "en Hogares, ENTIC Hogares, 2024 (DANE, 2025). Los valores nacionales figuran en el texto del boletín y los de Córdoba "
        "se leyeron de sus gráficos departamentales. La población de Montería se tomó del archivo oficial de proyecciones "
        "municipales por edad simple, actualización posterior a la COVID-19 (DANE, s. f.). La caracterización de aulas "
        "proviene de un estudio previo del mismo proyecto (Equipo 13, 2026), tratado como fuente secundaria no verificada."))
    h.append(H2("Indicadores regionales"))
    filas = [
        ["Hogares con conexión a internet", pct(DANE["hog_internet_cor"]), pct(DANE["hog_internet_nal"]),
         "−" + n(BRECHA, 1)],
        ["Personas que usaron computador", pct(DANE["pers_comp_cor"]), pct(DANE["pers_comp_nal"]),
         "−" + n(DANE["pers_comp_nal"] - DANE["pers_comp_cor"], 1)],
        ["Personas de 5 años o más que usaron internet", pct(DANE["pers_int_cor"]), pct(DANE["pers_int_nal"]),
         "−" + n(DANE["pers_int_nal"] - DANE["pers_int_cor"], 1)],
        ["Hogares con computador", "Sin dato", pct(DANE["hog_comp_nal"]), "—"],
    ]
    h.append(P(
        f"La [[T:indic]] compara Córdoba con el total nacional. La brecha más amplia es la de hogares con internet, {n(BRECHA, 1)} "
        f"puntos porcentuales: en {n(100 - DANE['hog_internet_cor'], 1)} de cada 100 hogares del departamento no hay conexión, "
        "de modo que una solución que dependa de la nube excluye a más de la mitad de ellos."))
    h.append(tabla("Acceso a tecnologías de la información en Córdoba y en el total nacional, 2024",
                   ["Indicador", "Córdoba", "Nacional", "Diferencia (p. p.)"], filas,
                   f"Datos de DANE (2025), gráficos 2, 6, 13 y 15. p. p. = puntos porcentuales. En el total nacional, el "
                   f"{pct(DANE['hog_internet_cab'])} de los hogares de las cabeceras tenía internet, frente al "
                   f"{pct(DANE['hog_internet_rur'])} de los centros poblados y el área rural dispersa.",
                   anchos=["46%", "16%", "16%", "22%"], ref="indic"))
    h.append(H2("Población objetivo"))
    h.append(P(
        f"La proyección oficial para Montería en 2026 es de {n(DANE['mon_total'])} habitantes, de los cuales "
        f"{n(DANE['mon_3_12'])} tienen entre 3 y 12 años, el {n(DANE['mon_3_12'] / DANE['mon_total'] * 100, 1)} % del "
        f"municipio ({n(DANE['mon_3_5'])} de 3 a 5 años, {n(DANE['mon_6_8'])} de 6 a 8 y {n(DANE['mon_9_12'])} de 9 a 12; "
        "DANE, s. f.). Esta cifra acota el universo potencial, pero no es la demanda: el número de aulas de música de la "
        "ciudad y su matrícula no se encontraron en fuentes oficiales, por lo que el modelo financiero parte de un aula."))
    h.append(H2("Caracterización de campo"))
    h.append(P(
        "El Equipo 13 (2026) reporta observaciones en aulas de instituciones de Montería y Cereté, con un recorrido de campo "
        "adaptado del <em>Gemba Walk</em> ([[T:campo]]). El estudio no documenta el tamaño de la muestra ni los instrumentos, "
        "por lo que sus cifras se usan para dimensionar el modelo financiero y no para sostener conclusiones sobre el efecto del sistema."))
    filas = [
        ["Nivelación individual: preparación manual de fichas y partituras", "1,0 a 1,5 h por semana", "Beneficio 1 (se usa 1,0 h)"],
        ["Papelería: fotocopias y cuadernos de pentagrama", "$ 600.000 por aula y año", "Beneficio 2"],
        ["Niños con teclado o xilófono propio en el aula", "Menos del 15 %", "Contexto"],
        ["Tiempo de clase en explicación teórica", "60 % a 70 %", "Proceso actual"],
        ["Pérdida de atención en lectura teórica pasiva", "A los 10 a 12 min", "Duración de la sesión"],
        ["Abandono en el primer semestre", "Superior al 55 %", "Contexto"],
        ["Línea base del grupo de control: discriminación de notas; respuesta motriz; retención a cuatro semanas",
         "42,91 ± 7,56 sobre 100; 5,48 ± 0,92 s; menos del 40 %", "Referencia del piloto"],
    ]
    h.append(tabla("Caracterización de aulas de Montería y Cereté según el estudio previo",
                   ["Observación", "Cifra reportada", "Uso en este documento"], filas,
                   "Datos de Equipo 13 (2026), no verificados de forma independiente.",
                   anchos=["50%", "28%", "22%"], clase="chica larga", ref="campo"))
    h.append(H2("Brecha tecnológica"))
    h.append(P(
        "La <em>brecha tecnológica</em> se entiende como la distancia entre lo que requiere la práctica musical infantil y lo "
        f"que el contexto regional permite sostener. Tiene tres componentes medibles: conectividad, por la diferencia de {n(BRECHA, 1)} "
        f"puntos en hogares con internet; equipamiento, porque solo el {pct(DANE['pers_comp_cor'])} de las personas de Córdoba "
        "usó un computador en 2024; y proceso, porque la evaluación en el aula es manual y no deja registro por nota. El "
        "prototipo responde con procesamiento local, requisitos de hardware mínimos (computador y cámara web) y registro "
        "automático de cada intento."))
    return "".join(h)


# ============================================================ literatura
RESENAS = {
    "203": ("Revisión de tecnologías de inteligencia artificial en educación infantil temprana.",
            "Panorama general; no trata señas ni música."),
    "002": ("Análisis de contenido de estudios de realidad aumentada en educación musical.",
            "Requiere instrumento o dispositivo de realidad aumentada."),
    "186": ("Revisión del aprendizaje en porciones breves; respalda actividades cortas.", "Revisión conceptual, sin niños."),
    "161": ("Experimento con 234 estudiantes sobre apps móviles y carga de trabajo en educación musical.",
            "Universitarios; sin reconocimiento de gestos."),
    "081": ("Instrumento validado por expertos para evaluar apps musicales.", "No cubre visión artificial."),
    "075": ("Rutas de aprendizaje musical con aprendizaje por refuerzo profundo.", "Requiere mucho entrenamiento; poco interpretable."),
    "032": ("Evaluación adaptativa basada en aprendizaje por refuerzo.", "Sin entrada por señas ni procesamiento local."),
    "077": ("Planificación de rutas de aprendizaje con red neuronal profunda.", "Necesita muchos datos por alumno."),
    "044": ("Sistema adaptativo sensible a emociones.", "Entrada afectiva, no gestual."),
    "046": ("Computación afectiva en educación musical preescolar (120 niños).", "Infraestructura de cómputo pesada."),
    "038": ("Retroalimentación con IA en piano (240 estudiantes).", "Universitarios; requiere piano."),
    "144": ("Detección del teclado de piano en video con aprendizaje profundo.", "La entrada es un instrumento, no señas."),
    "164": ("Interacción adaptativa en la enseñanza musical con refuerzo profundo.", "Sin entrada gestual."),
    "129": ("Evaluación multimodal de la enseñanza musical (audio, video y texto).", "Arquitectura dependiente de servicios."),
    "220": ("Generación de ejercicios de lectura ajustados a la dificultad.", "Piano y partitura."),
}


def literatura() -> str:
    h = [H1("Revisión de la literatura")]
    h.append(P(
        "La búsqueda partió de la matriz bibliográfica del proyecto, con 189 documentos únicos clasificados por su relación "
        "con el sistema. Se seleccionaron 15 artículos de relación alta o media, publicados entre 2023 y 2026, con DOI. "
        "Cada DOI se contrastó con la interfaz de Crossref (título, año, autores y revista) y se comprobó que resuelve en "
        "doi.org; la verificación se repitió el 1 de octubre de 2026. Un artículo sobre la postura en la interpretación del "
        "guzheng se excluyó porque Crossref lo registra con una nota editorial de preocupación. La [[T:matriz]] resume el conjunto."))
    filas = [[cita(r), d, l] for r, (d, l) in RESENAS.items()]
    h.append(tabla("Estudios revisados, aporte al proyecto y límite frente a HSK",
                   ["Estudio", "Aporte", "Límite frente a HSK"], filas,
                   "Síntesis elaborada a partir de los resúmenes y metadatos de cada artículo, no del texto completo. "
                   "IA = inteligencia artificial.",
                   anchos=["20%", "46%", "34%"], clase="chica larga", ref="matriz"))
    h.append(H2("Brecha de investigación"))
    h.append(P(
        "En el conjunto revisado predominan propuestas que adaptan la enseñanza con modelos profundos o de refuerzo, sobre "
        "poblaciones universitarias o de piano, y con entradas como audio, video de un instrumento o señales afectivas. "
        "<em>No se identificó</em> un sistema que combine entrada por señas manuales para nombrar notas, población de 3 a 12 "
        "años, procesamiento local y planificación adaptativa interpretable; esa combinación es la brecha que aborda HSK. "
        "La afirmación se limita a los 15 estudios y no sustituye una revisión sistemática. De la literatura se adoptan "
        f"actividades breves ({cita('186')}), una dificultad objetivo intermedia ({cita('220')}) y una planificación "
        f"explícita en lugar del refuerzo profundo ({cita('075')}; {cita('164')}), cuya necesidad de datos no se ajusta "
        "a un niño que genera pocos intentos por sesión."))
    return "".join(h)


# ============================================================ método
def metodo() -> str:
    h = [H1("Método")]
    h.append(P(
        "El trabajo sigue la estructura de introducción, método, resultados y discusión, IMRyD, adaptada a un proyecto de "
        "ingeniería: el método es un ciclo de diseño, construcción y verificación, y los resultados son mediciones "
        "reproducibles sobre el prototipo. Cada cifra se clasificó como verificada en el código, verificada "
        "con una prueba ejecutada, tomada de una fuente oficial o supuesta; los documentos previos del proyecto que "
        "contradecían el código se corrigieron a favor de este."))
    h.append(P(
        "Las fases fueron cinco: diagnóstico, con los indicadores del DANE, la caracterización de campo y el proceso As-Is "
        "([[T:indic]]; [[T:campo]]; [[F:asis]]); revisión, con la selección de 15 estudios y la verificación de sus DOI "
        "([[T:matriz]]); diseño y construcción, en Python con PySide6, MediaPipe, OpenCV, NumPy, PuLP y SQLite (10.581 "
        "líneas de código y 1.746 de pruebas; [[F:arq]]); verificación, con pruebas automáticas, medición de latencia y "
        "auditoría de integridad de datos ([[T:recon]]; [[T:pruebas]]; [[T:calidad]]); y evaluación financiera, con CAPEX, "
        "OPEX, beneficios, ROI y periodo de recuperación ([[T:plantilla]]; [[T:escen]])."))
    return "".join(h)


# ============================================================ prototipo
def prototipo() -> str:
    t = BENCH
    h = [H1("Arquitectura de gestión tecnológica y prototipo")]
    h.append(H2("Arquitectura en capas"))
    h.append(P(
        "El sistema se organiza en cinco capas que solo dependen de las inferiores ([[F:arq]]), y un bus de eventos permite "
        "que las superiores reaccionen sin acoplarse. Ninguna pantalla importa MediaPipe, ningún componente de visión conoce "
        "las notas musicales y el evaluador no dibuja; esa separación permite ejecutar las pruebas sin cámara y sin ventana."))
    h.append(H2("Reconocimiento de señas"))
    h.append(P(
        "La versión 1 concatenaba las coordenadas de ambas manos (126 componentes) y aceptaba la señal más parecida por "
        "similitud coseno si superaba 0,65; sobre la calibración real, ese criterio disparaba una nota en el 100 % de las "
        "posturas que no eran seña. La versión 2.0 usa un descriptor geométrico invariante. Sean p<sub>0</sub>, …, "
        "p<sub>20</sub> ∈ ℝ³ los 21 puntos que entrega <em>MediaPipe Hands</em> para una mano (Zhang et al., 2020); la "
        "escala σ es la distancia de la muñeca al nudillo medio y la curvatura κ de cada dedo, con articulaciones (a, b, c, d), "
        "es una razón de longitudes, invariante a escala, traslación y rotación:"))
    h.append(ecuacion("σ = ‖p<sub>9</sub> − p<sub>0</sub>‖ ,&nbsp;&nbsp; κ = clip( ( ‖p<sub>d</sub> − p<sub>a</sub>‖ / "
                      "(‖p<sub>b</sub> − p<sub>a</sub>‖ + ‖p<sub>c</sub> − p<sub>b</sub>‖ + ‖p<sub>d</sub> − p<sub>c</sub>‖) − 0,35 ) / 0,65 , 0, 1 )"))
    h.append(figura("Arquitectura en cinco capas de HandSingKids7", svg_inline("arquitectura_capas"),
                    "Nombres de módulos tomados del paquete <em>handsingkids</em> de la versión 2.0.", ref="arq"))
    h.append(P(
        f"Cada mano aporta 58 valores (curvatura, apertura entre dedos, distancias del pulgar, normal de la palma, dirección "
        f"y forma normalizada) y con las dos manos se añaden 4 magnitudes relativas: el descriptor tiene {t['dim_descriptor']} "
        "componentes. La comparación es una distancia ponderada por bloques g, y la confianza se reparte con una función "
        "<em>softmax</em> cuya temperatura T se ajusta a la separación entre las señas del niño:"))
    h.append(ecuacion("d(a,b) = √( Σ<sub>g</sub> w<sub>g</sub> · (1/|g|) Σ<sub>i∈g</sub> (a<sub>i</sub> − b<sub>i</sub>)² / Σ<sub>g</sub> w<sub>g</sub> )"))
    h.append(ecuacion("P(c | x) = exp(−(d<sub>c</sub> − d<sub>mín</sub>)/T) / Σ<sub>k</sub> exp(−(d<sub>k</sub> − d<sub>mín</sub>)/T) ,&nbsp;&nbsp; T = clip( ½ · mín<sub>a≠b</sub> d(a,b) , 0,05 , 0,20 )"))
    h.append(P(
        "Una seña se acepta si d<sub>mejor</sub> ≤ 0,95, P<sub>mejor</sub> ≥ 0,55 y P<sub>mejor</sub> − P<sub>segunda</sub> ≥ 0,08; "
        "la tercera condición evita decidir entre dos señas empatadas. Un estabilizador temporal exige 0,45 s entre "
        "confirmaciones y, para repetir la misma nota, que la mano se suelte durante 6 fotogramas; la cámara opera a 24 "
        "fotogramas por segundo. La [[T:recon]] muestra el efecto: el método nuevo cede algo de sensibilidad con ruido alto "
        "porque se abstiene, y a cambio rechaza 92 de cada 100 posturas que no son seña."))
    h.append(tabla("Desempeño del reconocimiento sobre la calibración real con escala, giro y ruido simulados",
                   ["Condición", "Versión 2.0", "Versión 1"],
                   [["Señas válidas, ruido σ = 0,00", "100,0 %", "100,0 %"], ["Señas válidas, ruido σ = 0,03", "100,0 %", "100,0 %"],
                    ["Señas válidas, ruido σ = 0,06", "96,9 %", "100,0 %"], ["Señas válidas, ruido σ = 0,09", "86,0 %", "100,0 %"],
                    ["Posturas que no son seña (n = 640): notas disparadas por error", "8,0 %", "100,0 %"]],
                   "Resultados de <em>tests/test_vision.py</em>: escala entre 0,8 y 1,25, giro de ±18° por mano y ruido gaussiano "
                   "proporcional al tamaño de la mano. La calibración es de una sola persona, por lo que la muestra es limitada.",
                   anchos=["60%", "20%", "20%"], clase="chica", ref="recon"))
    h.append(P(
        f"El descriptor y el clasificador tardan en promedio {n(t['total_ms']['media'], 1)} ms por fotograma (percentil 95: "
        f"{n(t['total_ms']['p95'], 1)} ms; {n(t['n_fotogramas'])} fotogramas). La medición excluye la captura de la cámara y "
        "la inferencia de MediaPipe, por lo que no es la latencia de extremo a extremo, que no se ha medido."))
    h.append(H2("Gemelo digital y repaso espaciado"))
    h.append(P(
        "El <em>gemelo digital</em> del aprendiz es su estado de aprendizaje por habilidad: dominio, precisión, consistencia, "
        "velocidad, retención y próximo repaso. El dominio M<sub>s</sub> no es una suma: la retención R<sub>s</sub> multiplica "
        "al desempeño, de modo que una habilidad sin práctica pierde dominio. Con λ = 0,65, γ = 0,40, w<sub>p</sub> = 0,55, "
        "w<sub>c</sub> = 0,25 y w<sub>v</sub> = 0,20:"))
    h.append(ecuacion("M<sub>s</sub> = ( λ + (1 − λ) R<sub>s</sub><sup>γ</sup> ) · ( w<sub>p</sub> P<sub>s</sub> + w<sub>c</sub> C<sub>s</sub> + w<sub>v</sub> V<sub>s</sub> ) ,&nbsp;&nbsp; R<sub>s</sub> = exp(−Δt / τ<sub>s</sub>)"))
    h.append(P(
        "La precisión usa suavizado bayesiano, P<sub>s</sub> = (aciertos + 1)/(intentos + 4); la velocidad se normaliza "
        "con un tiempo de referencia por edad (5.200, 4.000 y 3.200 ms para 3 a 5, 6 a 8 y 9 a 12 años). Una habilidad se "
        "considera dominada con M<sub>s</sub> ≥ 0,80 y al menos seis intentos. El repaso adapta el algoritmo SM-2 a una "
        "calidad continua: si la precisión de la actividad es menor que 0,6, el intervalo vuelve a un día."))
    h.append(H2("Motor adaptativo y planificación de la sesión"))
    h.append(P(
        "El motor adaptativo aplica reglas explícitas en orden: descanso si la fatiga F ≥ 1; ayuda escalonada si hay fallos "
        "consecutivos y la precisión es menor que 55 %; juego si F ≥ 0,7; repaso si hay repasos vencidos; subida de "
        "dificultad si la precisión llega a 88 %; y, en otro caso, refuerzo o mantenimiento. La selección de actividades "
        "de la sesión es el único componente formulado como problema de optimización: un programa lineal entero mixto, "
        "MILP, que maximiza la ganancia de aprendizaje g<sub>i</sub>, la urgencia de repaso r<sub>i</sub> y la motivación "
        "m<sub>i</sub> y penaliza la fatiga f<sub>i</sub>:"))
    h.append(ecuacion("máx Σ<sub>i∈A</sub> ( 1,00 g<sub>i</sub> + 0,70 r<sub>i</sub> + 0,35 m<sub>i</sub> − 0,55 f<sub>i</sub> ) x<sub>i</sub> ,&nbsp;&nbsp; x<sub>i</sub> ∈ {0, 1}"))
    h.append(P(
        "Las restricciones son siete: tiempo total, número exacto de actividades, prerrequisitos, al menos una actividad "
        "lúdica, dificultad media menor o igual a 0,72, no más de dos actividades por habilidad y al menos un repaso vencido "
        "si existe. La probabilidad de éxito de cada actividad la estima una función logística que, con 40 intentos o más "
        "del niño, se reajusta por regresión logística sobre sus propios datos. El problema se resuelve con el solucionador "
        f"CBC mediante PuLP en {n(MILP['min'] / 1000, 2)} a {n(MILP['max'] / 1000, 1)} s por sesión con {MILP['candidatas']} "
        "candidatas, y una enumeración exhaustiva devolvió el mismo óptimo; las constantes provienen de la literatura y de "
        "decisiones de diseño, no de un estudio con niños."))
    h.append(H2("Estado funcional del prototipo"))
    h.append(P(
        "La versión 2.0 tiene 14 pantallas: bienvenida, perfiles, creación de perfil, inicio, mapa de aventura con 7 niveles, "
        "calibración, progreso, Zona de Padres, ajustes, modo libre, ejercicio, resultados, canciones y ritmo ([[F:caps]]). "
        "El catálogo incluye 14 habilidades, 63 actividades y 17 logros, con estrellas, monedas y racha de días como "
        "elementos de <em>gamificación</em>. Las 8 suites de pruebas pasan; una de ellas solo en ejecución individual ([[T:pruebas]]). El nivel de madurez tecnológica, "
        "<em>Technology Readiness Level</em>, TRL, es 4: componentes validados en laboratorio, sin pruebas con niños."))
    duo = ('<div class="duo"><div>' + img("05_aventura.png", alt="Mapa de aventura") + "</div><div>"
           + img("11_ejercicio.png", alt="Ejercicio con retroalimentación") + "</div></div>")
    h.append(figura("Mapa de aventura (izquierda) y ejercicio guiado (derecha)", duo,
                    "Capturas de la versión 2.0 con un perfil de prueba. En el ejercicio, el fondo es un cuadro de prueba y los "
                    "esqueletos son los 21 puntos por mano del detector.", ref="caps"))
    filas = [[f"<em>{k}</em>", v["comprueba"], v["resultado"]] for k, v in PRUEBAS["archivos"].items()]
    h.append(tabla("Suites de pruebas automáticas y resultado de su ejecución", ["Archivo", "Qué comprueba", "Resultado"], filas,
                   PRUEBAS.get("nota", ""), anchos=["20%", "54%", "26%"], clase="chica larga", ref="pruebas"))
    h.append(H2("Trazabilidad con los objetivos"))
    filas = [
        ["OE1", "Indicadores del DANE; 15 estudios con DOI verificado", "Cumplido; caracterización de campo secundaria"],
        ["OE2", "Visión, gemelo digital, repaso espaciado, planificador MILP, 14 pantallas, base SQLite local",
         "Funcional en banco de pruebas (TRL 4)"],
        ["OE2", "Gobernanza: 11 tablas, sin imágenes en disco ni red", "Parcial: 4 de 8 reglas de integridad impuestas"],
        ["OE3", f"Banco de reconocimiento; {n(BENCH['total_ms']['media'], 1)} ms por fotograma; equivalencia MILP", "Cumplido en banco, sin niños"],
        ["OE3", "Modelo financiero con seis escenarios y supuestos rotulados", "Cumplido; supuestos por validar en un piloto"],
    ]
    h.append(tabla("Trazabilidad entre objetivos específicos, componentes y estado", ["Objetivo", "Componente o evidencia", "Estado"],
                   filas, anchos=["12%", "56%", "32%"], clase="chica", ref="traza"))
    return "".join(h)


# ============================================================ BPMN
def bpmn() -> str:
    h = [H1("Modelado de procesos de negocio en BPMN 2.0")]
    h.append(P(
        "El proceso modelado es la enseñanza de una nota y el seguimiento de su aprendizaje. Los diagramas usan <em>pools</em> "
        "por participante y <em>swimlanes</em> por rol; compuertas exclusivas (X), paralelas (+) e inclusivas (O) con sus "
        "condiciones rotuladas; eventos de inicio, intermedios de temporizador y de mensaje, y de fin; flujos de secuencia "
        "con línea continua y flujos de mensaje con línea punteada. El modelo <em>As-Is</em> ([[F:asis]]) describe la clase "
        "habitual según la caracterización de campo; el <em>To-Be</em> ([[F:tobe]]) se construyó a partir del código del prototipo."))
    h.append(P(
        "En el To-Be, la compuerta paralela refleja que el sonido y el dibujo de la nota no esperan a la evaluación, y la "
        "inclusiva activa siempre la actualización del dominio y, según el caso, las estrellas y la apertura de habilidades. "
        "El temporizador de un fotograma (unos 42 ms a 24 fotogramas por segundo) sustituye la espera de la corrección "
        "individual. La [[T:compar]], después de las figuras, contrasta ambos procesos punto por punto; las capacidades del To-Be están verificadas "
        "en el prototipo, pero su efecto en el aula debe medirse en un piloto."))
    h.append(figura("Proceso actual (As-Is): enseñanza de una nota en el aula de música", svg_inline("bpmn_as_is"),
                    "Marcas rojas: (1) actividad manual con sobrecosto, nivelación de 1,0 a 1,5 h semanales y $ 600.000 anuales "
                    "de papelería por aula (Equipo 13, 2026); (2) cuello de botella, atención de uno a muchos; (3) reproceso, la "
                    "demostración se repite sin diagnóstico del error; (4) registro manual no agregable; (5) redundancia y "
                    "retraso, el avance anotado se vuelve a comunicar de forma verbal; (6) tiempo muerto, el olvido entre "
                    "clases no se mide ni se programa.", ancha=True, ref="asis"))
    h.append(figura("Proceso propuesto (To-Be): sesión de práctica con Hand Sing Kids", svg_inline("bpmn_to_be"),
                    "Tareas amarillas: ejecutadas por el sistema. F = fatiga; d, P y margen = distancia, probabilidad y margen del "
                    "clasificador. Los intentos se guardan al cerrar cada actividad.", ancha=True, ref="tobe"))
    filas = [
        ["1 Nivelación manual", "1,0 a 1,5 h por semana; $ 600.000 de papelería al año", "Planificación automática de la sesión (MILP) y material en pantalla", "Horas de nivelación; gasto de papelería"],
        ["2 Atención de uno a muchos", "Respuesta motriz de referencia: 5,48 s", f"Reconocimiento en cada fotograma ({n(BENCH['total_ms']['media'], 1)} ms de cómputo)", "Tiempo de respuesta"],
        ["3 Reproceso sin diagnóstico", "Se repite la demostración", "Matriz de confusiones por nota y ayuda escalonada", "Intentos hasta el acierto"],
        ["4 Registro manual", "Cuaderno del docente", "Cada intento se guarda con nota esperada, detectada, confianza y reacción", "Intentos registrados (verificado: 100 %)"],
        ["5 Informe tardío", "Verbal o por mensaje", "Zona de Padres bajo demanda", "Consultas por semana"],
        ["6 Sin repaso programado", "Retención inferior al 40 % a cuatro semanas", "Repaso espaciado con fecha por habilidad", "Retención a cuatro semanas"],
    ]
    h.append(tabla("Cuellos de botella del proceso actual y su tratamiento en el proceso propuesto",
                   ["Problema (As-Is)", "Evidencia de campo", "Capacidad del To-Be", "Indicador del piloto"], filas,
                   "Evidencia de campo de Equipo 13 (2026), no verificada.", anchos=["20%", "26%", "32%", "22%"], clase="chica larga", ref="compar"))
    return "".join(h)


# ============================================================ DFD
def dfd() -> str:
    from diagramas_dfd import BALANCE
    h = [H1("Diagramas de flujo de datos")]
    h.append(P(
        "Los diagramas siguen la notación de Yourdon y DeMarco: círculos para procesos, rectángulos para entidades externas, "
        "rectángulos abiertos para almacenes de datos y flechas rotuladas para los flujos. El nivel 0 ([[F:dfd0]]) delimita el "
        "sistema; el nivel 1 ([[F:dfd1]]) lo descompone en siete procesos; y el nivel 2 ([[F:dfd2]]) detalla el proceso crítico, "
        "la planificación adaptativa, que concentra el procesamiento algorítmico y la mayoría de lecturas de almacenes. Los almacenes D1 a D6 son tablas o archivos reales (véase Gobernanza de Datos)."))
    h.append(figura("DFD nivel 0: diagrama de contexto", '<div style="width:80%;margin:0 auto">' + svg_inline("dfd_nivel0") + "</div>",
                    "Sin entidades externas en la nube.", ref="dfd0"))
    h.append(P(
        "El <em>balanceo</em> exige que los flujos que cruzan la frontera de un proceso reaparezcan en su descomposición. "
        "La [[T:balance]] lo comprueba: los cinco flujos del nivel 0 se reparten sin pérdida ni adición en el nivel 1, y los "
        "siete flujos de la frontera del proceso 5.0 reaparecen con el mismo nombre en el nivel 2."))
    filas = []
    for nv, d in BALANCE.items():
        filas.append([f"<em>{nv}</em>", ""])
        filas += [[p, "; ".join(hh)] for p, hh in d.items()]
    h.append(tabla("Comprobación del balanceo entre niveles", ["Flujo en el nivel padre", "Flujos en el nivel hijo"],
                   filas, anchos=["48%", "52%"], clase="chica larga", ref="balance"))
    h.append(figura("DFD nivel 1: descomposición en siete procesos", svg_inline("dfd_nivel1"),
                    "D4 aparece dos veces por legibilidad; la línea vertical adicional marca la copia.", ancha=True, ref="dfd1"))
    h.append(figura("DFD nivel 2: explosión del proceso 5.0, planificar la sesión adaptativa", svg_inline("dfd_nivel2"),
                    "En gris, los procesos y almacenes vecinos del nivel 1; el proceso 6.0 se dibuja a ambos lados por legibilidad.",
                    ancha=True, ref="dfd2"))
    return "".join(h)


# ============================================================ gobernanza
REGLAS = {
    "profiles": "Nombre de 2 a 18 caracteres y edad de 3 a 12 (interfaz); calibrated en {0, 1}",
    "skills": "Dificultad en [0, 1]; prerrequisitos como lista JSON",
    "skill_state": "Estado en {bloqueada, introducida, en_practica, dominada, consolidada}; dominio, precisión, "
                   "consistencia, velocidad y retención en [0, 1]",
    "activities": "Tipo en {ejercicio, juego, cancion, evaluacion, repaso}; dificultad en [0, 1]",
    "sessions": "ended_at nulo mientras la sesión está abierta; precisión en [0, 100]",
    "attempts": "correct en {0, 1}; confianza en [0, 1]; detected nulo si se agotó el tiempo",
    "activity_results": "Estrellas de 1 a 3 (3 si la precisión llega a 90 %; 2 si llega a 70 %)",
    "rewards": "Una fila por recompensa otorgada",
    "achievements": "Catálogo fijo de 17 logros",
    "profile_achievements": "Un logro por perfil una sola vez (llave compuesta)",
    "meta": "Valor JSON; una fila de predictor por perfil",
}
CARD = {
    "profiles": "Raíz: 1 a N con las tablas del perfil",
    "skills": "1 a N con skill_state",
    "skill_state": "Llave (profile_id, skill_code); N a 1 con profiles y skills",
    "activities": "Referida por código desde attempts y activity_results",
    "sessions": "N a 1 con profiles; 1 a N con attempts y activity_results",
    "attempts": "N a 1 con profiles (cascada) y sessions (nulo al borrar)",
    "activity_results": "N a 1 con profiles (cascada) y sessions (nulo al borrar)",
    "rewards": "N a 1 con profiles (cascada)",
    "achievements": "1 a N con profile_achievements",
    "profile_achievements": "N a 1 con profiles y achievements (cascada)",
    "meta": "Clave y valor, sin relaciones",
}


def gobernanza() -> str:
    res = CAT["_resumen"]
    h = [H1("Gobernanza de datos")]
    h.append(P(
        "El marco toma como referencia el cuerpo de conocimiento DAMA-DMBOK (DAMA International, 2017) en sus áreas de "
        "modelado, calidad, metadatos y seguridad, y distingue lo que el código <em>impone hoy</em> de la <em>política "
        "objetivo</em>. Sus principios son privacidad por diseño (ningún fotograma se escribe en disco y no hay módulos de "
        "red), soberanía de los datos (sin cuentas ni nube) y calidad medible."))
    h.append(H2("Catálogo y diccionario de datos"))
    h.append(P(
        f"El repositorio es SQLite, con {res['tablas']} tablas y {res['columnas']} campos, registro anticipado de escritura "
        "(<em>write-ahead logging</em>, WAL) y llaves foráneas activas. El diccionario de la [[T:dicc]] se extrajo del esquema "
        "real con las instrucciones PRAGMA de SQLite, de modo que no puede diferir del código. Fuera de la base hay dos "
        "almacenes de archivos JSON: las plantillas de calibración y las melodías grabadas en el modo libre. Los almacenes de "
        "los DFD corresponden así: D1, profiles, rewards y profile_achievements; D2, plantillas de cada perfil; D3, sessions, "
        "attempts y activity_results; D4, skill_state; D5, skills, activities y achievements; y D6, la fila del predictor en meta."))
    filas = []
    for t, v in CAT.items():
        if t.startswith("_"):
            continue
        campos = ", ".join(f"{c['nombre']} ({c['tipo'].lower()}{', PK' if c['pk'] else ''}{'' if c['not_null'] or c['pk'] else ', nulo'})"
                           for c in v["columnas"])
        filas.append([f"<em>{t}</em>", campos, CARD[t], REGLAS[t]])
    h.append(tabla("Diccionario de datos del esquema SQLite", ["Entidad", "Atributos (tipo)", "Cardinalidad", "Reglas de validación"],
                   filas, "PK = llave primaria; «nulo» = admite valores nulos; los demás campos son NOT NULL. Las reglas de "
                   "validación las aplican la interfaz y el código de dominio: el esquema no tiene restricciones CHECK.",
                   anchos=["15%", "41%", "20%", "24%"], clase="chica larga", ref="dicc"))
    h.append(H2("Linaje del dato"))
    h.append(P(
        "El linaje ([[F:linaje]]) sigue el dato desde la cámara hasta las decisiones: las etapas 1 a 3 existen solo en la "
        "memoria del proceso, las etapas 4 y 5 en la memoria de la sesión, y desde el cierre de cada actividad el dato es "
        "persistente. El planificador y la Zona de Padres, donde el acudiente o el docente decide qué reforzar, consumen el "
        "estado persistente."))
    h.append(figura("Linaje del dato, de la cámara a la toma de decisiones", svg_inline("linaje_dato"),
                    "Borde punteado: dato efímero, solo en RAM; amarillo claro: dato de sesión; amarillo: dato persistente en el disco "
                    "local. Ningún fotograma se escribe en disco. Elaboración propia a partir del código.",
                    ref="linaje"))
    h.append(H2("Dimensiones de calidad"))
    calidad = [
        ["Completitud", "1 − nulos / esperados en campos críticos", "100 %", "Cumple: NOT NULL impuesto (prueba Q3)"],
        ["Exactitud", "Acierto del reconocimiento con ruido σ = 0,06", "≥ 96 %", "Cumple: 96,9 % ([[T:recon]])"],
        ["Consistencia", "Integridad referencial y rangos de dominio", "100 %", "Parcial: llaves foráneas y cascada impuestas (Q2, Q7); "
         "la base acepta edad 99, confianza 5,0 y dominio −3 (Q4 a Q6)"],
        ["Oportunidad", "Tiempo entre el cierre de la actividad y la actualización del gemelo", "En la misma sesión",
         "Cumple por diseño (escritura síncrona); la latencia de escritura no se midió"],
    ]
    h.append(tabla("Dimensiones de calidad, indicador, umbral y resultado", ["Dimensión", "Indicador", "Umbral", "Resultado"], calidad,
                   f"Pruebas Q1 a Q8 de <em>auditoria_calidad.py</em> sobre la clase Database real: {AUD['cumplen']} de "
                   f"{AUD['total']} reglas impuestas por la base.", anchos=["14%", "32%", "14%", "40%"], clase="chica larga", ref="calidad"))
    h.append(H2("Seguridad y privacidad"))
    h.append(P(
        "Hoy los datos se guardan en la carpeta de datos del usuario del sistema operativo, sin cifrado propio, y la Zona de "
        "Padres se abre con un botón: el control de acceso basado en roles, <em>role-based access control</em>, RBAC, de la "
        "[[T:rbac]] es por ahora una convención de la interfaz. La Ley Estatutaria 1581 de 2012 contiene reglas especiales "
        "para el tratamiento de datos de niños, niñas y adolescentes (Congreso de la República de Colombia, 2012); el "
        "procesamiento local reduce la exposición, pero no exime a la institución de obtener la autorización de los "
        "representantes, y por ello el CAPEX incluye una consulta jurídica."))
    rbac = [
        ["Niño o niña", "Jugar, calibrar y ver su progreso", "Interfaz infantil", "Sin barrera hacia Ajustes ni Zona de Padres"],
        ["Acudiente o docente", "Crear y borrar perfiles, leer informes, cambiar ajustes", "Número de identificación personal, PIN, de 4 dígitos guardado con <em>hash</em> y sal (propuesto)", "Pendiente"],
        ["Motor analítico", "Escribir intentos y estado; leer y escribir el modelo", "Código de la aplicación", "Implementado"],
        ["Cámara", "Entregar fotogramas al detector", "Proceso de la aplicación, sin persistencia", "Implementado"],
    ]
    h.append(tabla("Roles y permisos (RBAC): estado actual y control propuesto", ["Rol", "Permisos", "Autenticación o mecanismo", "Estado"],
                   rbac, anchos=["18%", "30%", "34%", "18%"], clase="chica", ref="rbac"))
    pol = [
        ["Respaldo", "Copia con la interfaz de respaldo en línea de SQLite al iniciar sesión si hay más de 20 intentos nuevos; se conservan las 3 últimas", "No implementado"],
        ["Retención", "Detalle de los últimos 180 días y siempre los últimos 200 intentos de cada niño, que el predictor necesita", "No implementado"],
        ["Eliminación", "Al borrar un perfil, borrar sus filas (ya ocurre por cascada), su plantilla, sus melodías y las copias que lo contengan", "Parcial (Q7, Q8)"],
        ["Integridad", "Migración con 16 restricciones CHECK, probada sin romper las suites de integración y del predictor", "Probada, no aplicada"],
        ["Confidencialidad", "Carpeta accesible solo por el usuario del sistema; cifrado de la base en reposo como opción", "Heredado del sistema"],
    ]
    h.append(tabla("Políticas de respaldo, retención, eliminación y confidencialidad", ["Política", "Regla objetivo", "Estado"], pol,
                   "Los parámetros (20 intentos, 3 copias, 180 días y 200 intentos) son propuestas de diseño.",
                   anchos=["16%", "62%", "22%"], clase="chica", ref="politica"))
    return "".join(h)


# ============================================================ finanzas
def _sens() -> list[tuple[str, float, float]]:
    def roi(**kw):
        p = dict(PAR); p.update(kw)
        return MF.calcular(p)["escenarios"][MF.ESC_BASE]["roi_pct"]
    casos = [("las horas de ingeniería de este corte", "horas_dev_corte2"), ("las horas de nivelación", "horas_nivelacion_sem"),
             ("el gasto de papelería", "papeleria_anual")]
    return [(nm, roi(**{k: PAR[k] * 0.8}), roi(**{k: PAR[k] * 1.2})) for nm, k in casos]


def finanzas() -> str:
    h = [H1("Viabilidad financiera")]
    h.append(P(
        "El modelo sigue la guía del curso: el beneficio neto anual es el beneficio bruto menos los costos operativos, OPEX; "
        "el retorno sobre la inversión, ROI, es el cociente entre ese beneficio y la inversión inicial, CAPEX; y el periodo "
        "de recuperación, <em>payback</em>, es el CAPEX dividido por el beneficio neto mensual:"))
    h.append(ecuacion("ROI = ( Beneficio neto anual / CAPEX ) × 100 % ,&nbsp;&nbsp; Payback (meses) = CAPEX / ( Beneficio neto anual / 12 )"))
    h.append(P(
        "La unidad de análisis es un aula de música, porque los datos de campo se reportan por aula. Cada insumo tiene una "
        "procedencia rotulada en la hoja de cálculo: la tarifa de ingeniería viene de la guía ($ 25.000 a $ 40.000 por hora); "
        "los valores marcados PINT2 vienen del estudio del Equipo 13 (2026), no verificado; los verificables se comprobaron "
        "en el código (no hay nube, interfaz de IA ni red); y los supuestos son estimaciones propias ([[T:costos]])."))
    cap = FIN["capex"]; ox = FIN["opex"]; bn = FIN["beneficios"]
    det_c = {
        "Horas de ingeniería y desarrollo": (f"{PAR['horas_dev_pint2']} h (PINT2) + {PAR['horas_dev_corte2']} h de este corte (supuesto) × {cop(PAR['tarifa_ing'])}", "PINT2, supuesto"),
        "Cámara web, periféricos y soportes": ("Cámara 720p, periféricos y soportes", "PINT2"),
        "Licenciamiento y configuración inicial": ("Software de código abierto; puesta a punto", "PINT2"),
        "Capacitación a docentes": (f"{PAR['horas_capac']} h × {cop(PAR['tarifa_docente'])}", "PINT2"),
        "Consulta jurídica de protección de datos": ("Ley 1581 de 2012, datos de menores", "Supuesto"),
        "Mantenimiento y soporte técnico": ("Corrección de errores y librerías", "PINT2"),
        "Reposición de hardware": ("10 % anual del hardware", "Supuesto"),
        "Energía eléctrica": ("Consumo del equipo en clase", "Supuesto"),
        "Nube, API de IA y conectividad": ("El código no los usa", "Verificable"),
        "Ahorro de tiempo docente en nivelación individual": (f"{n(PAR['horas_nivelacion_sem'], 1)} h/semana × {PAR['semanas']} semanas × {cop(PAR['tarifa_docente'])}", "PINT2"),
        "Reducción del gasto en papelería didáctica": ("Fotocopias y cuadernos por aula", "PINT2"),
    }
    filas = []
    for grupo, dic, tot in (("CAPEX", cap, TOT["capex"]), ("OPEX anual", ox, TOT["opex"]), ("Beneficios brutos anuales", bn, TOT["beneficios"])):
        for k, v in dic.items():
            d, tp = det_c[k]
            filas.append([grupo, k, d, tp, cop(v)])
        filas.append(["", f"Total {grupo}", "", "", cop(tot)])
    h.append(tabla("CAPEX, OPEX y beneficios de un aula, con detalle y procedencia",
                   ["Rubro", "Concepto", "Detalle", "Procedencia", "Valor (COP)"], filas,
                   "PINT2 = Equipo 13 (2026). API = interfaz de programación de aplicaciones.",
                   anchos=["14%", "26%", "34%", "12%", "14%"], clase="chica larga", ref="costos"))
    plant = [
        ["Inversión inicial (CAPEX)", "Desarrollo, hardware, configuración, capacitación y consulta jurídica", cop(TOT["capex"])],
        ["Costos operativos anuales (OPEX)", "Mantenimiento, reposición de hardware y energía; sin nube", cop(TOT["opex"])],
        ["Beneficios brutos anuales", "Ahorro de tiempo docente y de papelería", cop(TOT["beneficios"])],
        ["Beneficio neto anual", "Beneficios brutos − OPEX", cop(B1["beneficio_neto"])],
        ["ROI calculado (año 1)", "(Beneficio neto / CAPEX) × 100", pct(B1["roi_pct"])],
        ["Periodo de retorno (<em>payback</em>)", "CAPEX / beneficio neto mensual", n(B1["payback_meses"], 1) + " meses"],
    ]
    h.append(P(
        f"La [[T:plantilla]] reproduce la plantilla obligatoria de la guía para un aula: beneficio neto de {cop(B1['beneficio_neto'])} "
        f"al año ({cop(B1['beneficio_neto_mensual'])} al mes), ROI de {pct(B1['roi_pct'])} y recuperación en "
        f"{n(B1['payback_meses'], 1)} meses. <em>Un aula aislada no cumple</em> los criterios de la guía para software (ROI de "
        "al menos 30 % y recuperación de hasta 12 meses), y el resultado se informa sin ajustar los supuestos."))
    h.append(tabla("Plantilla financiera del escenario base (un aula)", ["Componente financiero", "Descripción", "Valor"], plant,
                   anchos=["32%", "48%", "20%"], clase="chica larga", ref="plantilla"))
    esc_f = [[k, cop(e["capex"]), cop(e["beneficio_neto"]), pct(e["roi_pct"]), n(e["payback_meses"], 1),
              "Sí" if e["roi_pct"] >= 30 else "No", "Sí" if e["payback_meses"] <= 12 else "No"] for k, e in ESC.items()]
    h.append(P(
        f"La [[T:escen]] presenta seis escenarios. Una institución que adopta el sistema en cuatro aulas, con "
        f"beneficios por aula y un desarrollo que se paga una vez, alcanza un ROI de {pct(INST['roi_pct'])} y recupera la "
        f"inversión en {n(INST['payback_meses'], 1)} meses: cumple el criterio de ROI y se acerca al de 12 meses sin cumplirlo. "
        "La rentabilidad del proyecto proviene, por tanto, de la adopción en varias aulas o instituciones."))
    h.append(tabla("Escenarios frente a los criterios de la guía",
                   ["Escenario", "CAPEX", "Beneficio neto", "ROI año 1", "Payback (meses)", "ROI ≥ 30 %", "Payback ≤ 12"], esc_f,
                   "Conservador: beneficios 25 % menores. Optimista: suma el instrumental que deja de comprarse ($ 1.000.000; PINT2). Institución: cuatro aulas "
                   "(supuesto). Escala: el desarrollo se reparte entre tres instituciones de un aula.",
                   anchos=["30%", "12%", "13%", "10%", "11%", "12%", "12%"], clase="chica larga", ref="escen"))
    s = _sens()
    txt = "; ".join(f"{nm}, de {pct(lo)} a {pct(hi)}" for nm, lo, hi in s)
    h.append(P(
        f"En un análisis de sensibilidad de ±20 % sobre el escenario base, el ROI varía así: {txt}. Ningún cambio de esa "
        "magnitud lleva a un aula aislada al umbral de 30 %; las dos variables de beneficio deben medirse en el piloto."))
    return "".join(h)


# ============================================================ discusión
def discusion() -> str:
    h = [H1("Discusión y conclusiones")]
    h.append(P(
        "El resultado técnico central es el equilibrio entre sensibilidad y especificidad: el método de la versión 1 "
        "reconocía siempre porque respondía siempre, mientras que el descriptor invariante rechaza 92 de cada 100 posturas "
        "que no son seña y conserva un acierto del 96,9 % con ruido moderado. Frente a la literatura revisada, que adapta la "
        "enseñanza con refuerzo profundo, HSK usa reglas explícitas y un MILP que pueden explicarse a un docente y funcionan "
        "con pocos datos por niño, a costa de que sus constantes sean decisiones de diseño. La gobernanza cumple la privacidad "
        "por diseño, pero el PIN de adulto, los respaldos y el borrado completo siguen pendientes. Limitaciones: una sola "
        "calibración, sin pruebas con niños ni medición del efecto pedagógico, y beneficios basados en cifras secundarias."))
    h.append(P(
        "Se concluye que el prototipo reconoce las ocho señas con un descriptor de 120 componentes en "
        f"{n(BENCH['total_ms']['media'], 1)} ms de cómputo por fotograma y adapta la práctica con un gemelo digital y una "
        f"planificación MILP verificada contra la enumeración exacta; que la brecha de conectividad de {n(BRECHA, 1)} puntos "
        "justifica el diseño local; y que un aula aislada no alcanza los criterios financieros de la guía "
        f"({pct(B1['roi_pct'])}; {n(B1['payback_meses'], 1)} meses), mientras que cuatro aulas logran {pct(INST['roi_pct'])} y "
        f"{n(INST['payback_meses'], 1)} meses. El paso siguiente es un piloto cuasi-experimental de ocho semanas, con grupo de "
        "control, que mida discriminación de notas, tiempo de respuesta, retención a cuatro semanas, horas de nivelación y "
        "gasto de papelería, con consentimiento de los representantes y cumplimiento de la Ley 1581 de 2012."))
    return "".join(h)


def referencias() -> str:
    h = [H1("Referencias", salto=True), '<div class="ref">']
    h += [f"<p>{r}</p>" for r in referencias_ordenadas()]
    h.append("</div>")
    return "".join(h)
