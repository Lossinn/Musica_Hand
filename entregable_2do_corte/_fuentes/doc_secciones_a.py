"""Secciones 1 a 5 del documento: introducción, diagnóstico, literatura, metodología y prototipo."""
from __future__ import annotations

import json
from pathlib import Path

from datos import BASE, BENCH, CAT, CONS, DANE, ESCALA, TOT, cita, cop, n, pct
from doc_base import (H1, H2, H3, P, UL, ecuacion, figura, img, svg_inline, tabla)

F = Path(__file__).resolve().parent
PRUEBAS = json.loads((F / "pruebas.json").read_text(encoding="utf-8")) if (F / "pruebas.json").exists() else {}


# =====================================================================
def sec1_introduccion() -> str:
    h = [H1("1. Introducción", salto=True)]
    h.append(P(
        "Hand Sing Kids, HSK, es una aplicación de escritorio que enseña las ocho notas del solfeo, de DO3 a DO4, "
        "a niños de 3 a 12 años mediante señas de las manos que una cámara reconoce. Cada seña se convierte en una "
        "nota, la nota se evalúa y el resultado modifica lo que la aplicación propone a continuación. Todo el "
        "procesamiento ocurre en el equipo del usuario: no hay conexión a internet, no se graba video y no se envía "
        "ningún dato a servidores (Sección 5)."))
    h.append(P(
        "El proyecto se presenta como <em>Empresa de Base Tecnológica</em>, EBT, en la asignatura Gestión Tecnológica, "
        "GT, de la Facultad de Ingeniería Industrial de la Universidad Pontificia Bolivariana, Seccional Montería. "
        "Este documento consolida la ingeniería de detalle del segundo corte: el diagnóstico de la brecha tecnológica "
        "regional, la arquitectura del prototipo funcional mínimo, <em>Minimum Viable Product</em>, MVP, el modelado de "
        "procesos de negocio en <em>Business Process Model and Notation</em>, BPMN 2.0, los diagramas de flujo de "
        "datos, DFD, el marco de gobernanza de datos y la evaluación financiera."))
    h.append(P(
        "Una característica del documento es que cada cifra técnica se verificó contra el código de la versión 2.0, "
        "contra pruebas ejecutables o contra una fuente oficial citada, y las discrepancias halladas entre "
        "documentos previos se resolvieron en favor del código (Anexo A). Las cifras financieras, en cambio, dependen "
        "de supuestos explícitos que todavía no provienen de un estudio de campo y se marcan como tales."))
    h.append(H2("1.1 Planteamiento del problema"))
    h.append(P(
        "El aprendizaje de las notas musicales exige retroalimentación inmediata y repaso a intervalos adecuados. En "
        "un aula, un docente atiende a muchos niños a la vez, evalúa de forma manual y no conserva un registro por "
        "nota que permita decidir qué reforzar. La [[F:arbol]] resume el árbol de problemas: el problema central, sus "
        "efectos y sus causas. La causa asociada a la conectividad se apoya en un dato oficial: en 2024 solo el "
        f"{n(DANE['hog_internet_cor'], 1)} % de los hogares de Córdoba tenía conexión a internet, frente al "
        f"{n(DANE['hog_internet_nal'], 1)} % nacional (Sección 2)."))
    h.append(figura("Árbol de problemas de la educación de notas musicales en niños de Montería",
                    svg_inline("arbol_problemas"),
                    "Elaboración propia. La causa 3 proviene de la ENTIC Hogares 2024 (DANE, 2025); las causas 1 y 2 "
                    "describen el proceso actual modelado en la Sección 6; la causa 4 es la brecha hallada en la "
                    "revisión de la Sección 3.", ref="arbol"))
    h.append(H2("1.2 Pregunta de investigación y objetivos"))
    h.append(P(
        "La pregunta que orienta el proyecto es la siguiente: ¿en qué medida un sistema que reconoce señas manuales y "
        "planifica de forma adaptativa la práctica, todo en el equipo del usuario, puede ofrecer retroalimentación "
        "individual inmediata y un registro objetivo del dominio de las notas musicales en niños de 3 a 12 años de "
        "Montería?"))
    h.append(P("El objetivo general es <em>diseñar, construir y verificar técnicamente</em> un prototipo de aplicación "
               "que reconozca señas manuales de las ocho notas del solfeo y adapte la práctica de cada niño, y "
               "evaluar su viabilidad financiera para una institución de educación musical de Montería. Los objetivos "
               "específicos, ordenados de diagnóstico a evaluación, son:"))
    h.append(UL([
        "diagnosticar la brecha tecnológica regional con indicadores oficiales y revisar la literatura reciente "
        "sobre tecnología en la educación musical;",
        "diseñar y construir el prototipo: reconocimiento de señas, gemelo digital del aprendiz, planificación "
        "adaptativa y gobernanza de datos local;",
        "verificar el desempeño técnico del prototipo y estimar el retorno de la inversión con supuestos "
        "explícitos que puedan contrastarse en un piloto."]))
    h.append(H2("1.3 Justificación y Objetivos de Desarrollo Sostenible"))
    h.append(P(
        "El proyecto contribuye a los Objetivos de Desarrollo Sostenible, ODS, número 4 (educación de calidad), por "
        "ofrecer práctica individualizada con seguimiento; número 9 (industria, innovación e infraestructura), por "
        "desarrollar tecnología que funciona sin nube en un territorio con conectividad desigual; y número 10 "
        "(reducción de las desigualdades), por diseñarse para equipos de escritorio sin suscripción en línea. La "
        "contribución se plantea como orientación del diseño, no como impacto medido."))
    h.append(H2("1.4 Alcance y estado del proyecto"))
    h.append(P(
        "El alcance de este documento es el prototipo de la versión 2.0, con 14 pantallas implementadas y una suite "
        "de pruebas automáticas (Sección 5.6). Las constantes del modelo pedagógico provienen de la literatura y "
        "del ajuste sobre datos de una sola calibración; <em>no se han validado con niños</em>. Esa validación, "
        "junto con el piloto institucional que confirmaría los supuestos financieros, es la fase siguiente."))
    return "".join(h)


# =====================================================================
def sec2_diagnostico() -> str:
    h = [H1("2. Diagnóstico cuantitativo y brecha tecnológica")]
    h.append(H2("2.1 Fuentes y método"))
    h.append(P(
        "Los indicadores se tomaron del boletín técnico de la Encuesta de Tecnologías de la Información y las "
        "Comunicaciones en Hogares, ENTIC Hogares, 2024, publicado por el Departamento Administrativo Nacional de "
        "Estadística, DANE, el 1 de agosto de 2025 (DANE, 2025). Los valores departamentales de Córdoba se leyeron "
        "de los gráficos de barras del boletín, que los presentan con un decimal y ordenados de menor a mayor; los "
        "valores nacionales figuran en el texto del boletín. La población de Montería proviene de las proyecciones "
        "del DANE con base en el Censo Nacional de Población y Vivienda 2018, consultadas a través del sitio "
        "Telencuestas, que las reproduce (DANE, s. f.)."))
    h.append(H2("2.2 Indicadores regionales"))
    filas = [
        ["Hogares con conexión a internet", n(DANE["hog_internet_cor"], 1) + " %", n(DANE["hog_internet_nal"], 1) + " %",
         "−" + n(DANE["hog_internet_nal"] - DANE["hog_internet_cor"], 1), "Gráfico 6"],
        ["Personas que usaron computador (escritorio, portátil o tableta)", n(DANE["pers_comp_cor"], 1) + " %",
         n(DANE["pers_comp_nal"], 1) + " %", "−" + n(DANE["pers_comp_nal"] - DANE["pers_comp_cor"], 1), "Gráfico 13"],
        ["Personas de 5 años o más que usaron internet", n(DANE["pers_int_cor"], 1) + " %",
         n(DANE["pers_int_nal"], 1) + " %", "−" + n(DANE["pers_int_nal"] - DANE["pers_int_cor"], 1), "Gráfico 15"],
        ["Hogares con computador", "sin dato departamental", n(DANE["hog_comp_nal"], 1) + " %", "—", "Gráfico 2"],
    ]
    h.append(P(
        "La [[T:indic]] compara Córdoba con el total nacional. La brecha más marcada es la de hogares con internet: "
        f"{n(DANE['hog_internet_nal'] - DANE['hog_internet_cor'], 1)} puntos porcentuales por debajo del promedio del "
        f"país. Dicho de otro modo, en {n(100 - DANE['hog_internet_cor'], 1)} de cada 100 hogares de Córdoba no hay "
        "conexión a internet, de modo que una solución educativa que dependa de la nube excluye a más de la mitad de "
        "los hogares del departamento."))
    h.append(tabla("Indicadores de acceso a tecnologías de la información, Córdoba y total nacional, 2024",
                   ["Indicador", "Córdoba", "Nacional", "Brecha (p. p.)", "Fuente"], filas,
                   "Fuente: DANE (2025), ENTIC Hogares 2024. Los valores de Córdoba se leyeron de los gráficos "
                   "departamentales; p. p. = puntos porcentuales. A nivel nacional, el " +
                   n(DANE["hog_internet_cab"], 1) + " % de los hogares de las cabeceras tenía internet frente al " +
                   n(DANE["hog_internet_rur"], 1) + " % de los centros poblados y el rural disperso.",
                   anchos=["38%", "14%", "14%", "16%", "18%"], ref="indic"))
    h.append(H2("2.3 Población objetivo"))
    tot = DANE["mon_5_9"] + DANE["mon_10_14"]
    h.append(P(
        f"La población proyectada de Montería para 2026 es de {n(DANE['mon_total'])} habitantes. El proyecto atiende a "
        f"niños de 3 a 12 años, un intervalo que los grupos quinquenales del DANE no reproducen; como aproximación, "
        f"los grupos de 5 a 9 años ({n(DANE['mon_5_9'])}) y de 10 a 14 años ({n(DANE['mon_10_14'])}) suman "
        f"{n(tot)} niños, equivalentes al {n(tot / DANE['mon_total'] * 100, 1)} % de la población del municipio. "
        "Esta cifra acota el universo potencial y no debe confundirse con la demanda: el número de instituciones de "
        "educación musical de Montería y su matrícula no se encontraron en fuentes oficiales verificables, por lo "
        "que el modelo financiero parte de un aula de música (Sección 9)."))
    h.append(H2("2.4 Brecha tecnológica"))
    h.append(P(
        "La <em>brecha tecnológica</em> (<em>technology gap</em>) se define aquí como la distancia entre lo que la "
        "práctica musical infantil requiere y lo que el contexto regional permite sostener. Tiene tres componentes "
        "verificables. El primero es de conectividad: la diferencia de "
        f"{n(DANE['hog_internet_nal'] - DANE['hog_internet_cor'], 1)} puntos en hogares con internet. El segundo es de "
        f"equipamiento: solo el {n(DANE['pers_comp_cor'], 1)} % de las personas de Córdoba usó un computador en 2024, y "
        f"a escala nacional solo el {n(DANE['hog_comp_nal'], 1)} % de los hogares posee uno, lo que acota la "
        "práctica en casa. El tercero es de proceso: según el modelo As-Is de la Sección 6 y la caracterización de la Sección 2.5, la evaluación es manual y "
        "no deja registro por nota. El prototipo responde al primer componente procesando todo de forma local, al "
        "segundo requiriendo únicamente un computador y una cámara web, y al tercero con un registro objetivo por "
        "intento."))
    return "".join(h)


# =====================================================================
RESENAS = {
    "203": ("Revisión de tecnologías de inteligencia artificial en educación infantil temprana (robots, aprendizaje "
            "profundo), con perspectiva histórica y obras representativas.",
            "Encuadra la IA en la infancia temprana.", "Panorama general; no trata señas ni música."),
    "002": ("Análisis de contenido de estudios de realidad aumentada en educación musical en Web of Science y Scopus "
            "(2006 a 2020); predominan piano y guitarra para principiantes.",
            "Indica que la tecnología visual acelera y vuelve más agradable el aprendizaje.",
            "Requiere instrumento físico o dispositivo de realidad aumentada."),
    "186": ("Revisión exploratoria del aprendizaje en porciones breves (<em>bite-sized learning</em>) en educación y "
            "disciplinas afines; reduce la carga cognitiva.",
            "Respalda las actividades cortas de HSK (del orden de 25 s).", "Revisión conceptual; sin niños."),
    "161": ("Estudio experimental con 234 estudiantes de Grado de Primaria sobre apps móviles y carga de trabajo "
            "(NASA-TLX) en Educación Musical.",
            "Método para medir la carga percibida.", "Universitarios y teléfonos; sin reconocimiento de gestos."),
    "081": ("Instrumento para evaluar apps móviles musicales, validado por juicio de expertos.",
            "Criterios de calidad aplicables a HSK.", "Evalúa apps de móvil; no cubre visión artificial."),
    "075": ("Aprendizaje por refuerzo profundo con proceso de decisión de Markov, estado multidimensional del alumno y "
            "recompensa dual (desempeño y afecto); resultados simulados y en pilotos controlados.",
            "Formula la ruta de aprendizaje como decisión secuencial.",
            "Requiere modelado multimodal y entrenamiento; poco interpretable."),
    "032": ("Marco de evaluación adaptativa basado en aprendizaje por refuerzo para educación musical personalizada.",
            "Evaluación adaptativa y retroalimentación oportuna.", "Sin entrada por señas ni enfoque local."),
    "077": ("Modelo de planificación y optimización de rutas de aprendizaje con red neuronal profunda y mecanismo de "
            "atención, para alumnos novatos a avanzados.",
            "Personalización del ritmo y el estilo.", "Modelo profundo; requiere muchos datos por alumno."),
    "044": ("Sistema adaptativo consciente de emociones con aprendizaje automático para educación musical.",
            "Incorpora el estado afectivo a la adaptación.", "Emociones multimodales; no aplica a señas."),
    "046": ("Computación afectiva en educación musical preescolar con arquitectura de mezcla de expertos y campos de "
            "radiancia neuronal; 120 niños de preescolar.",
            "Población infantil y medición afectiva.", "Reconstrucción de escenas; infraestructura pesada."),
    "038": ("Retroalimentación con IA en piano: 240 estudiantes de primer año; exactitud técnica y autonomía.",
            "Retroalimentación automática mejora la exactitud.", "Universitarios; requiere piano."),
    "144": ("Detección del teclado de piano en video con aprendizaje profundo, para transcripción musical.",
            "Visión por computador como entrada musical.", "Entrada: video de piano; no son señas."),
    "164": ("Aprendizaje por refuerzo profundo en la interacción de la enseñanza musical, con adaptación a cada "
            "estudiante en tiempo real.",
            "Adaptación dinámica de la interacción.", "Sin entrada gestual ni restricciones de tiempo."),
    "129": ("Sistema multimodal de evaluación de la enseñanza musical con aprendizaje por refuerzo profundo y "
            "generación aumentada por recuperación (audio, video, partitura y texto).",
            "Evaluación multimodal adaptativa.", "Arquitectura pesada, dependiente de servicios."),
    "220": ("Generación de ejercicios de lectura a primera vista ajustados a la dificultad del estudiante.",
            "Dificultad ajustada, afín al generador procedural de HSK.", "Piano y lectura de partitura."),
}


def sec3_literatura() -> str:
    h = [H1("3. Revisión de la literatura")]
    h.append(H2("3.1 Selección y verificación"))
    h.append(P(
        "La búsqueda partió de la matriz bibliográfica del proyecto, con 189 documentos únicos clasificados por su "
        "relación con el sistema (A, núcleo; B, relevante; C, método o contexto; D, marginal). Se seleccionaron 15 "
        "artículos de relación A o B, publicados entre 2023 y 2026, con DOI. Cada DOI se verificó el 30 de septiembre "
        "de 2026 contra la API de Crossref (título, año, autores y revista coinciden con la matriz) y contra "
        "doi.org (los 15 resuelven). Un artículo sobre visión por computador en la interpretación del guzheng se "
        "excluyó porque Crossref lo registra con una nota editorial de preocupación (<em>Expression of Concern</em>)."))
    h.append(H2("3.2 Síntesis"))
    filas = []
    for rid in ["203", "002", "186", "161", "081", "075", "032", "077", "044", "046", "038", "144", "164", "129", "220"]:
        d, ap, lim = RESENAS[rid]
        filas.append([cita(rid), d, ap, lim])
    h.append(P(
        "La [[T:matriz]] resume los 15 estudios. Se agrupan en tres líneas: tecnología y carga cognitiva en educación "
        "musical (realidad aumentada, aprendizaje en porciones breves, apps móviles), adaptación personalizada "
        "(aprendizaje por refuerzo, aprendizaje profundo, emociones) y visión por computador aplicada a la música."))
    h.append(tabla("Matriz de los 15 estudios revisados (2023 a 2026)",
                   ["Estudio", "Descripción", "Aporte a HSK", "Límite frente a HSK"], filas,
                   "Los resúmenes se elaboraron a partir de los metadatos y resúmenes de cada artículo; ninguno se "
                   "leyó en texto completo, por lo que no se extraen conclusiones sobre sus métodos internos.",
                   anchos=["14%", "38%", "24%", "24%"], clase="larga chica", ref="matriz"))
    h.append(H2("3.3 Brecha de investigación"))
    h.append(P(
        "En el conjunto revisado predominan propuestas que adaptan la enseñanza con modelos profundos o de "
        "refuerzo, sobre poblaciones universitarias o de piano, y con entradas como audio, video de instrumento o "
        "señales fisiológicas. <em>No se identificó</em> en él un sistema que combine, al mismo tiempo, cuatro "
        "rasgos: entrada por señas manuales para nombrar notas, población de 3 a 12 años, procesamiento íntegramente "
        "local y planificación adaptativa interpretable. Esa combinación es la brecha que aborda HSK. La afirmación "
        "se limita a los 15 estudios seleccionados; no sustituye una revisión sistemática."))
    h.append(P(
        "De la literatura se toman tres decisiones de diseño: actividades breves, por el respaldo al aprendizaje en "
        f"porciones pequeñas ({cita('186')}); una dificultad objetivo intermedia, afín a la generación de ejercicios "
        f"ajustados al nivel ({cita('220')}); y una planificación formulada de manera explícita y explicable, frente "
        f"a los enfoques de refuerzo profundo ({cita('075')}; {cita('164')}), cuya opacidad y necesidad de datos no "
        "se ajustan a un niño que genera pocos intentos por sesión."))
    return "".join(h)


# =====================================================================
def sec4_metodologia() -> str:
    h = [H1("4. Metodología")]
    h.append(P(
        "El trabajo sigue una estructura de introducción, métodos, resultados y discusión, IMRyD, adaptada a un "
        "proyecto de ingeniería: el método es un ciclo de diseño, construcción y verificación, y los resultados son "
        "mediciones reproducibles sobre el prototipo. La [[T:fases]] resume las fases y la evidencia que deja cada una."))
    filas = [
        ["1. Diagnóstico", "Indicadores del DANE y modelo As-Is", "[[T:indic]]; [[F:asis]]", "Fuentes citadas con página y gráfico"],
        ["2. Revisión", "Selección de 15 estudios y verificación de DOI", "[[T:matriz]]; Referencias", "Scripts <em>verificar_doi.py</em> (Crossref y doi.org)"],
        ["3. Diseño", "Arquitectura en capas, modelo de dominio, planificador", "Sección 5", "Código y documento técnico v2.0"],
        ["4. Construcción", "Implementación en Python con PySide6, MediaPipe, OpenCV, NumPy, PuLP y SQLite", "HandSingKids7", f"10.581 líneas en el paquete; 1.746 en pruebas"],
        ["5. Verificación", "Pruebas automáticas, comparación con la versión 1, latencia y auditoría de integridad de datos", "Secciones 5.6 y 8", "<em>bench_latencia.py</em>; <em>auditoria_calidad.py</em>"],
        ["6. Evaluación financiera", "CAPEX, OPEX, beneficios, ROI y periodo de recuperación", "Sección 9", "Hoja de cálculo con fórmulas y supuestos"],
    ]
    h.append(tabla("Fases metodológicas y evidencia asociada", ["Fase", "Actividad", "Producto", "Evidencia"], filas,
                   anchos=["16%", "40%", "18%", "26%"], ref="fases"))
    h.append(H2("4.1 Protocolo de verificación de datos"))
    h.append(P(
        "Cada afirmación cuantitativa se clasificó en una de cuatro categorías: verificada en el código, verificada "
        "por una prueba ejecutada para este documento, tomada de una fuente oficial citada, o supuesto. Los documentos "
        "previos del proyecto (motor analítico y gobernanza de datos) contenían diez discrepancias con el documento "
        "técnico v2.0; todas se resolvieron contra el código y se listan en el Anexo A. Los supuestos se identifican "
        "en la Sección 9 y en la hoja de cálculo."))
    return "".join(h)


# =====================================================================
def _mc(s: str) -> str:
    return f'<span class="nb">{s}</span>'


def sec5_prototipo() -> str:
    t = BENCH
    h = [H1("5. Arquitectura y prototipo funcional mínimo")]
    h.append(H2("5.1 Arquitectura en capas"))
    h.append(P(
        "El sistema se organiza en cinco capas que solo se comunican hacia abajo ([[F:arq]]), con un bus de eventos "
        "que permite que las capas superiores se enteren de lo que ocurre sin depender de las inferiores. Ninguna "
        "pantalla importa <em>MediaPipe</em>, ninguna pieza de visión sabe qué es una nota musical y el evaluador no "
        "sabe dibujar. Esa separación permite ejecutar las pruebas sin cámara y sin ventana."))
    h.append(figura("Arquitectura en cinco capas de HandSingKids7", svg_inline("arquitectura_capas"),
                    "Nombres de módulos tomados del árbol de directorios del paquete <em>handsingkids</em>.", ref="arq"))
    h.append(H2("5.2 Reconocimiento de señas"))
    h.append(P(
        "La versión 1 concatenaba las coordenadas de ambas manos en un vector de 126 componentes y aceptaba la "
        "mejor coincidencia por similitud coseno si superaba 0,65. Sobre la calibración real del proyecto, 30 de los "
        "56 pares de notas distintas superan ese umbral, de modo que cualquier postura intermedia dispara una nota: "
        "el método emite una nota en el 100 % de las posturas que no son ninguna seña. La versión 2.0 sustituye ese "
        "esquema por un descriptor geométrico invariante."))
    h.append(P(
        "Sean p<sub>0</sub>, …, p<sub>20</sub> ∈ ℝ³ los 21 puntos que entrega <em>MediaPipe Hands</em> para una mano "
        "(Zhang et al., 2020), con p<sub>0</sub> la muñeca. La escala de la mano es la distancia de la muñeca al "
        "nudillo del dedo medio, y la curvatura de cada dedo, con cadena de articulaciones (a, b, c, d), es una "
        "razón entre longitudes y por tanto invariante a escala, traslación y rotación:"))
    h.append(ecuacion("σ = ‖p<sub>9</sub> − p<sub>0</sub>‖ ,&nbsp;&nbsp; κ = clip( ( ‖p<sub>d</sub> − p<sub>a</sub>‖ / "
                      "(‖p<sub>b</sub> − p<sub>a</sub>‖ + ‖p<sub>c</sub> − p<sub>b</sub>‖ + ‖p<sub>d</sub> − p<sub>c</sub>‖) − 0,35 ) / 0,65 , 0, 1 )"))
    h.append(P(
        "Cada mano aporta 58 valores: curvatura de los cinco dedos, apertura entre dedos contiguos, distancia del "
        "pulgar a cada yema, normal del plano de la palma, dirección de la mano y 40 números de forma normalizada. "
        f"Con las dos manos se añaden 4 magnitudes relativas y el descriptor completo tiene {t['dim_descriptor']} "
        "componentes (2 × 58 + 4), cifra comprobada en el código y en la ejecución. Los documentos previos "
        "mencionaban 38 componentes; el valor correcto es 120."))
    h.append(P(
        "La comparación entre dos descriptores es una distancia por bloques: cada bloque <em>g</em> se promedia por "
        "separado y se pondera (curvatura 3,0; forma 2,6; distancias del pulgar 2,0; dirección 2,0; geometría entre "
        "manos 1,6; normal de la palma 1,4; apertura 1,2). La confianza se reparte con una función <em>softmax</em> "
        "cuya temperatura T se ajusta a la separación real entre las señas del niño:"))
    h.append(ecuacion("d(a,b) = √( Σ<sub>g</sub> w<sub>g</sub> · (1/|g|) Σ<sub>i∈g</sub> (a<sub>i</sub> − b<sub>i</sub>)² / Σ<sub>g</sub> w<sub>g</sub> )"))
    h.append(ecuacion("P(c | x) = exp(−(d<sub>c</sub> − d<sub>mín</sub>)/T) / Σ<sub>k</sub> exp(−(d<sub>k</sub> − d<sub>mín</sub>)/T) ,&nbsp;&nbsp; T = clip( ½ · mín<sub>a≠b</sub> d(a,b) , 0,05 , 0,20 )"))
    h.append(P(
        "Una seña se acepta solo si d<sub>mejor</sub> ≤ 0,95, P<sub>mejor</sub> ≥ 0,55 y P<sub>mejor</sub> − "
        "P<sub>segundo</sub> ≥ 0,08. La tercera condición evita decidir cuando dos señas empatan: es preferible "
        "pedir al niño que repita el gesto que hacer sonar una nota que no quiso tocar. Por último, un "
        "<em>estabilizador temporal</em> confirma la nota en el mismo fotograma en que se reconoce (ventana de 1), "
        "exige 0,45 s entre confirmaciones y, si la nota es la misma que la anterior, que el niño la haya soltado "
        "durante al menos 6 fotogramas. La cámara entrega 24 fotogramas por segundo de forma predeterminada."))
    h.append(tabla("Desempeño del reconocimiento sobre la calibración real, con escala, giro y ruido simulados",
                   ["Ruido σ", "Método v2.0 (aciertos en señas válidas)", "Método v1 (aciertos)"],
                   [["0,00", "100,0 %", "100,0 %"], ["0,03", "100,0 %", "100,0 %"], ["0,06", "96,9 %", "100,0 %"],
                    ["0,09", "86,0 %", "100,0 %"],
                    ["Posturas que no son seña (n = 640): notas disparadas por error", "8,0 %", "100,0 %"]],
                   "Resultados de <em>tests/test_vision.py</em>, ejecutado el 30 de septiembre de 2026; escala entre 0,8 y "
                   "1,25, giro independiente por mano de ±18° y ruido gaussiano proporcional al tamaño de la mano. La "
                   "calibración es de una sola persona (ocho señas), por lo que la muestra es limitada.",
                   anchos=["46%", "30%", "24%"], ref="recon"))
    h.append(P(
        "Las dos mitades de la [[T:recon]] deben leerse en conjunto. El método de la versión 1 tiene sensibilidad perfecta "
        "y especificidad nula: acierta siempre porque siempre responde algo. El método nuevo cede algo de "
        "sensibilidad con ruido alto, porque se abstiene, y a cambio rechaza 92 de cada 100 posturas que no son una "
        "seña. Con la confirmación instantánea de fábrica se acepta ese 8,0 % de notas por error; el ajuste "
        "<em>Tiempo de sostener la seña</em> permite recuperar margen a costa de una espera."))
    h.append(P(
        f"La latencia del descriptor y el clasificador, medida sobre {n(t['n_fotogramas'])} fotogramas con ruido y "
        f"escala variables, fue de {n(t['total_ms']['media'], 1)} ms en promedio (descriptor "
        f"{n(t['descriptor_ms']['media'], 1)} ms; clasificador {n(t['clasificador_ms']['media'], 1)} ms), con un "
        f"percentil 95 de {n(t['total_ms']['p95'], 1)} ms y un máximo de {n(t['total_ms']['max'], 1)} ms. La medición "
        "excluye la inferencia de <em>MediaPipe</em> y la captura de la cámara, de modo que no equivale a la latencia "
        "de extremo a extremo; esta no se midió."))
    h.append(H2("5.3 Gemelo digital, dominio y repaso espaciado"))
    h.append(P(
        "El <em>gemelo digital</em> del aprendiz es la representación de su estado de aprendizaje en un momento "
        "dado: por habilidad (dominio, precisión, consistencia, velocidad, retención, días sin practicar, próximo "
        "repaso), conducta (confusiones, tiempo de reacción) y evolución. El dominio de una habilidad <em>s</em> no "
        "es una suma ponderada: la retención multiplica al desempeño, de modo que un mes sin practicar degrada una "
        "habilidad olvidada. Con λ = 0,65, γ = 0,40, w<sub>p</sub> = 0,55, w<sub>c</sub> = 0,25 y w<sub>v</sub> = 0,20:"))
    h.append(ecuacion("M<sub>s</sub> = ( λ + (1 − λ) R<sub>s</sub><sup>γ</sup> ) · ( w<sub>p</sub> P<sub>s</sub> + w<sub>c</sub> C<sub>s</sub> + w<sub>v</sub> V<sub>s</sub> )"))
    h.append(P(
        "La precisión usa un suavizado bayesiano, P<sub>s</sub> = (h<sub>s</sub> + 1)/(n<sub>s</sub> + 4), de modo "
        "que sin práctica vale 0,25 y cuatro aciertos de cuatro dan 0,625. La consistencia penaliza alternar entre "
        "acierto y fallo en los últimos ocho intentos. La velocidad se normaliza frente a un tiempo de referencia "
        "por franja de edad (5.200, 4.000 y 3.200 ms para 3 a 5, 6 a 8 y 9 a 12 años; mínimo 700 ms). La retención "
        "decae de forma exponencial, R<sub>s</sub> = exp(−Δt/τ<sub>s</sub>), con τ<sub>s</sub> = 1,8 · ε<sub>s</sub> · "
        "(0,6 + M<sub>s</sub><sup>−</sup>) días, donde M<sub>s</sub><sup>−</sup> es el dominio de la actualización "
        "anterior. Una habilidad pasa a <em>dominada</em> con M<sub>s</sub> ≥ 0,80 y al menos seis intentos, y a "
        "<em>consolidada</em> con M<sub>s</sub> ≥ 0,92 y doce intentos; una sesión perfecta de cuatro intentos da un "
        "dominio cercano a 0,68, todavía insuficiente."))
    h.append(P(
        "El repaso espaciado adapta el esquema SM-2 a una calidad continua q ∈ [0, 1] tomada de la precisión de la "
        "actividad: ε ← clip(ε + 0,1 − (1 − q)(0,8 + (1 − q)), 1,3, 2,8); el intervalo I se reinicia a un día si "
        "q < 0,6 y en otro caso I ← máx(1, I · ε)."))
    h.append(H2("5.4 Motor adaptativo y planificación de la sesión"))
    h.append(P(
        "El motor adaptativo es un conjunto de reglas explícitas que evalúa, en orden, el retrato del momento y "
        "devuelve una decisión: descansar si la fatiga F ≥ 1, con F = clip(½ · n/N + ½ · t/T); escalera de ayuda si "
        "hay fallos consecutivos y la precisión cae por debajo del 55 %; jugar si F ≥ 0,7; repasar si hay repasos "
        "vencidos; introducir o subir dificultad si la precisión alcanza el 88 %; reforzar una debilidad; y en otro "
        "caso mantener. La escalera de ayuda retira una exigencia distinta en cada peldaño (tiempo, longitud, "
        "memoria y secuencia)."))
    h.append(P(
        "La selección de las actividades de la sesión se formula como un problema de <em>programación lineal entera "
        "mixta</em>, MILP. Este es el único punto en que el documento aplica el término optimización al propio sistema, "
        "porque es el único donde existe una formulación matemática. Para cada actividad candidata <em>i</em> se estima la "
        "probabilidad de éxito p<sub>i</sub> = 1/(1 + e<sup>−k(μ̄<sub>i</sub> − dif<sub>i</sub>)</sup>), con k = 6, y "
        "un factor de dificultad deseable η<sub>i</sub> = exp(−(p<sub>i</sub> − p*)²/(2σ<sub>p</sub>²)), con p* = 0,75 "
        "y σ<sub>p</sub> = 0,18. Con la ganancia de aprendizaje g<sub>i</sub>, la urgencia de repaso r<sub>i</sub>, la "
        "motivación m<sub>i</sub> y la fatiga inducida f<sub>i</sub>:"))
    h.append(ecuacion("máx Σ<sub>i∈A</sub> ( α<sub>1</sub> g<sub>i</sub> + α<sub>2</sub> r<sub>i</sub> + α<sub>3</sub> m<sub>i</sub> − α<sub>4</sub> f<sub>i</sub> ) x<sub>i</sub> ,&nbsp;&nbsp; x<sub>i</sub> ∈ {0, 1}"))
    h.append(P(
        "con α<sub>1</sub> = 1,00, α<sub>2</sub> = 0,70, α<sub>3</sub> = 0,35 y α<sub>4</sub> = 0,55, sujeto a siete "
        "restricciones: tiempo total menor o igual a T, tamaño exacto K, prerrequisitos (x<sub>i</sub> ≤ a<sub>i</sub>), "
        "al menos una actividad lúdica si K ≥ 3, dificultad media menor o igual a 0,72, no más de dos actividades "
        "por habilidad y al menos un repaso vencido si existe. La resolución tiene tres niveles: MILP con el "
        "solucionador CBC mediante PuLP; enumeración exhaustiva, que entrega el óptimo exacto mientras el número de "
        "combinaciones no exceda 400.000 (con 24 candidatas y K = 4 son 10.626); y una heurística voraz de reserva. "
        "La aplicación informa cuál usó. Las constantes provienen de la literatura y de ajustes sobre los datos "
        "disponibles, no de un estudio con niños."))
    h.append(P(
        "Además del planificador, un modelo predictivo, <em>MasteryPredictor</em>, estima la probabilidad de éxito. "
        "Con menos de 40 intentos propios usa la función logística fija; con 40 o más ajusta por descenso de "
        "gradiente por lotes (300 épocas, tasa 0,35) una regresión logística de tres variables (precisión de la "
        "nota, dificultad y tiempo desde la última práctica) sobre los intentos reales de cada niño, y se reajusta "
        "cada 20 intentos nuevos. Los coeficientes se guardan en la tabla <em>meta</em>, una fila por perfil. No es "
        "aprendizaje por refuerzo: estima una probabilidad puntual que el planificador consume."))
    h.append(H2("5.5 Módulos funcionales y estado actual"))
    h.append(P(
        "La aplicación tiene 14 pantallas ([[T:pantallas]]; [[F:caps]]). Todas se construyen sin errores en la prueba de "
        "capturas y se generó una imagen de cada una. Su estado es de <em>implementación verificada en banco de "
        "pruebas</em>: el uso con niños reales no se ha realizado."))
    modulos = [
        ["Bienvenida (<em>splash</em>)", "Pantalla de arranque", "01"],
        ["Perfiles", "Selección de perfil, avatar, estrellas y racha", "02"],
        ["Crear perfil", "Alta con nombre, edad (3 a 12) y avatar", "03"],
        ["Inicio", "Acceso a aventura, canciones, modo libre, progreso y ajustes", "04"],
        ["Aventura", "Mapa de 7 niveles y ruta del día generada por el planificador", "05"],
        ["Calibración", "Tres muestras por nota con comprobación de estabilidad", "06"],
        ["Progreso", "Tarjetas por nota y dominio", "07"],
        ["Zona de padres", "Dominio por habilidad, confusiones y detalle técnico", "08"],
        ["Ajustes", "Umbrales, ventana de estabilización, sonido", "09"],
        ["Modo libre", "Tocar y grabar melodías propias", "10"],
        ["Ejercicio", "Secuencias guiadas con retroalimentación inmediata", "11"],
        ["Resultados", "Precisión, ritmo, estrellas y cambios de dominio", "12"],
        ["Canciones", "19 canciones del catálogo y melodías grabadas", "13"],
        ["Ritmo", "Notas viajeras hacia una línea de impacto", "14"],
    ]
    h.append(tabla("Pantallas de la versión 2.0", ["Pantalla", "Función", "Captura"], modulos,
                   "Capturas en <em>assets/capturas</em>, generadas por <em>tests/capturas.py</em> con datos de un "
                   "perfil de prueba.", anchos=["22%", "64%", "14%"], clase="chica", ref="pantallas"))
    duo = ('<div class="duo"><div>' + img("05_aventura.png", alt="Mapa de aventura") + "</div><div>"
           + img("11_ejercicio.png", alt="Ejercicio con retroalimentación") + "</div></div>")
    h.append(figura("Mapa de aventura (izquierda) y ejercicio guiado (derecha)", duo,
                    "Capturas de la versión 2.0. En el ejercicio, la imagen de fondo es un cuadro de prueba; los "
                    "esqueletos corresponden a los 21 puntos por mano que entrega el detector.", ref="caps"))
    h.append(H2("5.6 Verificación automática"))
    filas = []
    for nombre, info in PRUEBAS.get("archivos", {}).items():
        filas.append([f"<em>{nombre}</em>", info["comprueba"], info["resultado"]])
    if filas:
        h.append(P(
            "La [[T:pruebas]] presenta las pruebas ejecutadas para este documento el 30 de septiembre de 2026. Las pruebas "
            "que dependen de la interfaz se ejecutaron con la plataforma gráfica en modo <em>offscreen</em>."))
        h.append(tabla("Suites de pruebas de HandSingKids7 y resultado de su ejecución",
                       ["Archivo", "Qué comprueba", "Resultado"], filas,
                       PRUEBAS.get("nota", ""), anchos=["20%", "56%", "24%"], clase="chica", ref="pruebas"))
    h.append(P(
        "Dos errores reales se detectaron por esta vía y no por inspección: el estabilizador reiniciaba el contador "
        "de «soltar» en cuanto la nota reaparecía, de modo que nunca se podía repetir la misma nota dos veces; y "
        "entrar a recalibrar borraba las plantillas en memoria antes de capturar nada."))
    h.append(H2("5.7 Límites de esta versión"))
    h.append(UL([
        "El reconocimiento se probó con una sola calibración de ocho señas de una persona.",
        "Las constantes del dominio, del planificador y del predictor no se han validado con niños.",
        "Las dos manos son obligatorias; el descriptor admite una sola mano, pero no se ha probado.",
        "La latencia de extremo a extremo (cámara, detector, interfaz) no se midió.",
        "El aprendizaje es supervisado; no hay aprendizaje por refuerzo.",
        "Las melodías tradicionales del catálogo son simplificaciones ajustadas a las ocho notas naturales, sin "
        "revisión de una persona con formación musical formal."]))
    return "".join(h)
