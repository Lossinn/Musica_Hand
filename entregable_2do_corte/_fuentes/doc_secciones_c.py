"""Secciones nuevas o reescritas tras el análisis del estudio PINT2 (Equipo 13)."""
from __future__ import annotations

import json
import math
from pathlib import Path

import modelo_financiero as MF
from datos import BASE, BENCH, DANE, FIN, TOT, ESC, cop, n, pct
from doc_base import H1, H2, H3, P, UL, ecuacion, figura, svg_inline, tabla

F = Path(__file__).resolve().parent
CHK = json.loads((F / "ddl_checks.json").read_text(encoding="utf-8"))
CON = json.loads((F / "contraste_pint2.json").read_text(encoding="utf-8"))
DOI13 = json.loads((F / "doi_estudio_pint2.json").read_text(encoding="utf-8"))
SQL = (F / "propuesta_check.sql").read_text(encoding="utf-8")
K = {k: v for k, v in ESC.items()}
CONS, B1, OPT, INST, ESCA, MAX = (K[x] for x in (MF.ESC_CONS, MF.ESC_BASE, MF.ESC_OPT, MF.ESC_INST, MF.ESC_ESCALA, MF.ESC_MAX))


# ====================================================================== 2
def sec2_campo() -> str:
    h = [H2("2.5 Caracterización de campo reportada por un estudio previo")]
    h.append(P(
        "El Equipo 13 de la asignatura Proyecto Integrador II documentó, en un estudio previo del mismo proyecto "
        "(Equipo 13, 2026), una caracterización de campo en aulas de instituciones de Montería y Cereté, que adapta el "
        "recorrido en planta (<em>Gemba Walk</em>) al contexto escolar. La [[T:campo]] resume sus cifras. Se usan como "
        "<em>fuente secundaria interna</em>: el texto no documenta el tamaño de la muestra ni los instrumentos de "
        "medición, y este equipo no pudo verificarlas de forma independiente. Por esa razón se emplean para "
        "dimensionar el modelo financiero, donde se marcan como «PINT2», y no para sustentar conclusiones sobre el "
        "efecto del sistema."))
    filas = [
        ["Acceso a instrumento", "Niños con teclado o xilófono propio en el aula", "Menos del 15 %", "Contexto"],
        ["Tiempo de clase", "Parte de la clase dedicada a explicaciones teóricas abstractas", "60 % a 70 %", "Contexto; proceso As-Is"],
        ["Nivelación docente", "Preparación manual de fichas y partituras para ritmos dispares", "1,0 a 1,5 h por semana", "Beneficio B1 (se usa 1,0 h)"],
        ["Papelería", "Fotocopias y cuadernos de caligrafía musical", "$ 600.000 por aula y año", "Beneficio B2"],
        ["Abandono temprano", "Desinterés y deserción en el primer semestre", "Superior al 55 %", "Contexto; no se monetiza"],
        ["Atención sostenida", "Pérdida del foco en lectura teórica pasiva", "A los 10 a 12 minutos", "Respalda sesiones de 8 minutos"],
        ["Línea base de desempeño", "Grupo de control con instrucción tradicional: discriminación de notas, tiempo de respuesta motriz y retención a cuatro semanas",
         "42,91 ± 7,56 de 100; 5,48 ± 0,92 s; menos del 40 %", "Referencia del piloto (Sección 10.3)"],
    ]
    h.append(tabla("Caracterización de campo en aulas de Montería y Cereté, según el estudio del Equipo 13", ["Factor", "Observación", "Cifra reportada", "Uso aquí"], filas,
                   "Fuente: Equipo 13 (2026). Valores no verificados por este equipo. El tiempo de respuesta de 5,48 s es del orden del "
                   "tiempo de referencia de 5.200 ms que el modelo de dominio usa para niños de 3 a 5 años (Sección 5.3), y la sesión "
                   "de 8 minutos del motor adaptativo es menor que el intervalo de atención que ese estudio reporta.",
                   anchos=["16%", "36%", "24%", "24%"], clase="chica", ref="campo"))
    return "".join(h)


# ====================================================================== 5
def sec5_extra() -> str:
    h = [H2("5.8 Gamificación y experiencia infantil")]
    h.append(P(
        "La <em>gamificación</em> es la incorporación de mecánicas de juego a una tarea de aprendizaje. En HSK se "
        "implementa con elementos verificados en el código: siete niveles temáticos (de «Las primeras manitas» a «El gran "
        "concierto»), 14 habilidades y un catálogo sembrado de 63 actividades (19 canciones, 26 ejercicios, 8 repasos, "
        "6 juegos y 4 evaluaciones); 17 logros; estrellas por actividad (3 si la precisión alcanza el 90 %, 2 si alcanza "
        "el 70 % y 1 en otro caso) que solo se suman cuando mejoran el récord de esa actividad; monedas (5 por estrella y "
        "10 adicionales con precisión de 90 % o más); racha de días consecutivos; puntaje por rapidez de respuesta "
        "(perfecto hasta 1.400 ms, 100 puntos; bien hasta 2.600 ms, 70; vale, 50) con multiplicador de combo; y una "
        "mascota que acompaña la calibración y los ejercicios. El diseño de la interfaz sigue la lógica de pantallas "
        "cortas, lenguaje de segunda persona y color de alto contraste. Su efecto sobre la motivación no se ha medido; se "
        "propone medirlo en el piloto (Sección 10.3)."))
    h.append(H2("5.9 Madurez tecnológica"))
    h.append(P(
        "La escala de niveles de madurez tecnológica, <em>Technology Readiness Level</em>, TRL, va de 1 a 9. El nivel 4 "
        "corresponde a la validación de componentes en laboratorio y el nivel 5 a la validación en un entorno relevante. "
        "La evidencia de este documento (pruebas automáticas, un banco con la calibración de una persona y capturas de "
        "pantalla) sitúa a HSK en el <em>TRL 4</em>. El estudio previo declara un TRL 5; esa declaración requeriría "
        "pruebas en aula con niños y con cámaras y luz reales, que no constan en ninguno de los dos documentos."))
    h.append(H2("5.10 Trazabilidad entre objetivos, componentes y estado"))
    filas = [
        ["OE1. Diagnosticar la brecha y revisar la literatura", "Sección 2 y Sección 3", "Indicadores DANE; 15 estudios con DOI verificado", "Cumplido; la caracterización de campo es secundaria"],
        ["OE2. Construir el prototipo", "Visión (descriptor, clasificador, estabilizador); gemelo digital; repaso espaciado; planificador MILP; 14 pantallas; SQLite local", "8 de 8 suites; capturas 01 a 14", "Funcional en banco de pruebas (TRL 4)"],
        ["OE2. Gobernanza local", "Esquema de 11 tablas; sin imágenes en disco; sin red", "Auditoría de integridad (4 de 8 reglas impuestas)", "Parcial: brechas B1 a B8 (Sección 8.6)"],
        ["OE3. Verificar el desempeño", "Banco de reconocimiento; latencia; equivalencia MILP y enumeración", "[[T:recon]]; 2,3 ms por fotograma", "Cumplido en banco; sin pruebas con niños"],
        ["OE3. Estimar el retorno", "Modelo con seis escenarios y supuestos rotulados", "Hoja de cálculo verificada", "Cumplido; supuestos por validar en el piloto"],
    ]
    h.append(tabla("Trazabilidad de los objetivos específicos", ["Objetivo", "Componente", "Evidencia", "Estado"], filas,
                   "OE = objetivo específico (Sección 1.2).", anchos=["26%", "32%", "22%", "20%"], clase="chica", ref="trazabilidad"))
    return "".join(h)


# ====================================================================== 6
def sec6_extra() -> str:
    h = [H2("6.1 Leyenda de la notación")]
    leyenda = [
        ["Pool y swimlane", "Rectángulo con banda lateral; los carriles se dividen por rol: docente, niño, acudiente, visión, evaluación y planificación"],
        ["Tarea de usuario / de servicio", "Rectángulo redondeado con ícono de persona (tarea humana) o de engranaje (tarea del sistema); en el To-Be las del sistema van en amarillo"],
        ["Compuerta exclusiva (X)", "Un solo camino según una condición rotulada, por ejemplo ¿Seña aceptada?"],
        ["Compuerta paralela (+)", "Los caminos de salida se ejecutan a la vez: sonido y registro no se esperan entre sí"],
        ["Compuerta inclusiva (O)", "Se activan uno o varios caminos según sus condiciones: siempre actualizar dominio; estrellas si corresponde; abrir habilidades si hay prerrequisitos"],
        ["Eventos", "Círculo simple de inicio, círculo grueso de fin, doble círculo con reloj (intermedio de temporizador) y círculo con sobre (mensaje)"],
        ["Flujos", "Línea continua de secuencia; línea punteada con círculo inicial y punta abierta de mensaje entre participantes"],
        ["Cuello de botella", "Círculo rojo numerado en el As-Is con su explicación al pie de la figura"],
    ]
    h.append(tabla("Elementos BPMN 2.0 utilizados", ["Elemento", "Uso en los modelos"], leyenda, anchos=["26%", "74%"], clase="chica"))
    h.append(H2("6.2 Cierre de brechas de proceso: métricas del As-Is y del To-Be"))
    h.append(P(
        "El criterio de evaluación del modelado exige demostrar la eliminación de cuellos de botella, reprocesos y "
        "tiempos muertos. La [[T:brechas_proc]] relaciona cada cuello de botella con la métrica de campo reportada, la "
        "capacidad del prototipo que lo aborda y la forma de medir el efecto. Solo las capacidades están verificadas; los "
        "efectos sobre el aula se miden en el piloto."))
    filas = [
        ["1 Atención de uno a muchos; espera de la corrección individual", "Tiempo de respuesta motriz de referencia: 5,48 s por estímulo (PINT2)", f"Reconocimiento en cada fotograma: {n(BENCH['total_ms']['media'], 1)} ms de cómputo y una espera de unos 42 ms por fotograma", "Tiempo de respuesta y proporción de intentos corregidos al instante"],
        ["2 Registro manual sin datos agregables", "Cuaderno del docente", "Cada intento se guarda con nota esperada, nota detectada, confianza y reacción", "Porcentaje de intentos registrados (verificado: 100 %)"],
        ["3 Nivelación individual manual", "1,0 a 1,5 h por semana (PINT2)", "Planificación automática de la sesión con restricciones (0,13 a 1,8 s por sesión en el banco)", "Horas docentes de nivelación por semana"],
        ["4 Papelería de teoría pasiva", "$ 600.000 por aula y año (PINT2)", "Fichas, secuencias y canciones en pantalla", "Gasto anual de papelería"],
        ["5 Sin repaso programado; olvido entre clases", "Retención inferior al 40 % a cuatro semanas (PINT2)", "Repaso espaciado con fecha por habilidad", "Retención a cuatro semanas"],
        ["6 Informe tardío y sin detalle al acudiente", "Informe verbal o por mensaje", "Zona de Padres bajo demanda con dominio, confusiones y reacción", "Consultas por semana y comprensión del informe"],
    ]
    h.append(tabla("Cuellos de botella del proceso actual y su cierre en el proceso propuesto",
                   ["Cuello de botella (As-Is)", "Métrica de campo", "Capacidad del To-Be", "Cómo se mide el efecto"], filas,
                   "PINT2 = estudio del Equipo 13 (2026), no verificado. La latencia es la medición propia de la Sección 5.2.",
                   anchos=["24%", "22%", "30%", "24%"], clase="chica", ref="brechas_proc"))
    return "".join(h)


# ====================================================================== 9
def _sens() -> list[list[str]]:
    base = FIN["parametros"]

    def roi(**kw):
        p = dict(base); p.update(kw)
        return MF.calcular(p)["escenarios"][MF.ESC_BASE]["roi_pct"]
    r0 = roi()
    casos = [("Horas de nivelación docente por semana", "horas_nivelacion_sem"), ("Gasto anual de papelería", "papeleria_anual"),
             ("Horas de ingeniería de este corte", "horas_dev_corte2"), ("Costo hora docente", "tarifa_docente"),
             ("Costo del kit de hardware", "hardware_kit")]
    filas = []
    for nombre, k in casos:
        lo, hi = roi(**{k: base[k] * 0.8}), roi(**{k: base[k] * 1.2})
        filas.append([nombre, pct(lo), pct(r0), pct(hi), n(abs(hi - lo), 1) + " p. p."])
    return sorted(filas, key=lambda f: -float(f[4].split()[0].replace(",", ".")))


def sec9_financiero() -> str:
    p = FIN["parametros"]
    h = [H1("9. Viabilidad financiera", salto=True)]
    h.append(P(
        "El modelo sigue la guía metodológica del curso. El beneficio neto anual es el beneficio bruto menos los costos "
        "operativos, <em>OPEX</em>; el retorno sobre la inversión, <em>ROI</em>, es el cociente entre el beneficio neto "
        "anual y la inversión inicial, <em>CAPEX</em>; y el periodo de recuperación, <em>payback</em>, es el CAPEX "
        "dividido por el beneficio neto mensual:"))
    h.append(ecuacion("ROI = ( Beneficio neto anual / CAPEX ) × 100 % ,&nbsp;&nbsp; Payback (meses) = CAPEX / ( Beneficio neto anual / 12 )"))
    h.append(H2("9.1 Unidad de análisis y procedencia de los insumos"))
    h.append(P(
        "La unidad de análisis es <em>un aula de música</em> de una institución educativa de Montería o Cereté, porque "
        "los datos de campo disponibles se reportan por aula. Cada insumo tiene una procedencia explícita, que la hoja de "
        "cálculo rotula en la columna «Tipo»: la tarifa de ingeniería proviene de la guía; los valores «PINT2» provienen del "
        "estudio de campo del Equipo 13, que es una fuente secundaria no verificada; los «verificables» se comprobaron "
        "en el código (el sistema no usa nube, ni interfaz de programación de IA, ni red); y los «supuestos» son "
        "estimaciones propias. Respecto del estudio previo, el modelo elimina los ingresos por cuotas y licencias, que "
        "no tenían respaldo en el contexto de aulas escolares, y los costos de nube, de tokens de IA y de conectividad, "
        "que el código no genera."))
    h.append(H2("9.2 Inversión inicial (CAPEX)"))
    cap = [[k, cop(v)] for k, v in FIN["capex"].items()] + [["Total CAPEX (I<sub>0</sub>)", cop(TOT["capex"])]]
    h.append(P(
        f"El CAPEX es de {cop(TOT['capex'])}. Las horas de ingeniería son el {n(FIN['capex']['Horas de ingeniería y desarrollo'] / TOT['capex'] * 100, 0)} % del total: "
        f"{p['horas_dev_pint2']} h reportadas por el estudio previo más {p['horas_dev_corte2']} h estimadas para este corte, a "
        f"{cop(p['tarifa_ing'])} por hora, dentro del rango de la guía. El licenciamiento es cero porque las dependencias son de "
        "código abierto según la licencia que declara cada proyecto (MediaPipe y OpenCV, Apache 2.0; PySide6, LGPL; "
        "PuLP, MIT; NumPy, BSD); conviene confirmarlo al empaquetar la aplicación."))
    h.append(tabla("CAPEX por componente (un aula)", ["Componente", "Valor (COP)"], cap,
                   "Capacitación: 4 h × $ 30.000. Cámara, periféricos y soportes: $ 300.000 + $ 150.000 (PINT2). Configuración inicial: $ 200.000 (PINT2). "
                   "Consulta jurídica: $ 600.000 (supuesto, Ley 1581 de 2012).", anchos=["70%", "30%"], clase="chica"))
    h.append(H2("9.3 Costos operativos (OPEX) y beneficios"))
    ox = [[k, cop(v)] for k, v in FIN["opex"].items()] + [["Total OPEX anual", cop(TOT["opex"])]]
    h.append(tabla("OPEX anual por componente", ["Componente", "Valor anual (COP)"], ox,
                   "No hay costos de nube, de interfaz de IA ni de conectividad porque el código no los usa (verificado). El estudio previo presupuestaba $ 780.000 por esos conceptos.",
                   anchos=["70%", "30%"], clase="chica"))
    bn = [[k, cop(v)] for k, v in FIN["beneficios"].items()] + [["Total beneficios brutos anuales", cop(TOT["beneficios"])]]
    h.append(P(
        f"Los beneficios se limitan a los dos que tienen cifra de campo: el ahorro de tiempo docente, de "
        f"{n(p['horas_nivelacion_sem'], 1)} h por semana durante {p['semanas']} semanas a {cop(p['tarifa_docente'])} por hora, y la reducción del "
        f"gasto en papelería, de {cop(p['papeleria_anual'])} por aula. Se usó el mínimo del intervalo reportado de nivelación "
        "(1,0 a 1,5 h). El instrumental que no se adquiere ($ 1.000.000 en el estudio previo) se excluye del escenario base "
        "porque la aplicación no reemplaza a un instrumento y su efecto es discutible; solo se incluye en el escenario optimista. "
        "No se monetiza la deserción: en aulas escolares públicas no hay cuota que se pierda."))
    h.append(tabla("Beneficios brutos anuales cuantificados (un aula)", ["Beneficio", "Valor anual (COP)"], bn,
                   "Ambos valores son «PINT2»: no verificados por este equipo. El piloto debe medirlos.", anchos=["70%", "30%"], clase="chica"))
    h.append(H2("9.4 Indicadores de retorno"))
    plant = [
        ["Inversión inicial (CAPEX)", "Desarrollo, hardware, configuración, capacitación y consulta jurídica", cop(TOT["capex"])],
        ["Costos operativos anuales (OPEX)", "Soporte, reposición de hardware y energía; sin nube", cop(TOT["opex"])],
        ["Beneficios brutos anuales", "Ahorro de tiempo docente y de papelería", cop(TOT["beneficios"])],
        ["Beneficio neto anual", "Beneficios brutos − OPEX", cop(B1["beneficio_neto"])],
        ["ROI calculado (año 1)", "(Beneficio neto / CAPEX) × 100", pct(B1["roi_pct"])],
        ["Periodo de retorno (payback)", "CAPEX / beneficio neto mensual", n(B1["payback_meses"], 1) + " meses"],
    ]
    h.append(P(
        f"La [[T:plantilla]] reproduce la plantilla obligatoria de la guía para el escenario base de un aula. El beneficio neto anual es "
        f"{cop(B1['beneficio_neto'])}, equivalente a {cop(B1['beneficio_neto_mensual'])} por mes; el ROI es de {pct(B1['roi_pct'])} y el periodo de "
        f"recuperación, de {n(B1['payback_meses'], 1)} meses. <em>El escenario base no cumple</em> ninguno de los dos criterios de la guía para "
        "proyectos de software (ROI de al menos 30 % y recuperación de hasta 12 meses): se informa tal cual."))
    h.append(tabla("Plantilla financiera del escenario base (un aula de música)", ["Componente financiero", "Descripción", "Valor"], plant,
                   anchos=["30%", "48%", "22%"], clase="chica", ref="plantilla"))
    esc_f = []
    for k, e in ESC.items():
        esc_f.append([k, cop(e["capex"]), cop(e["beneficio_neto"]), pct(e["roi_pct"]), n(e["payback_meses"], 1) + " m",
                      "Sí" if e["roi_pct"] >= 30 else "No", "Sí" if e["payback_meses"] <= 12 else "No"])
    h.append(P(
        f"La [[T:escen]] presenta seis escenarios. Una institución que adopte el sistema en cuatro aulas, con beneficios que se escalan "
        f"por aula y un desarrollo que se paga una sola vez, alcanza un ROI de {pct(INST['roi_pct'])} y un periodo de recuperación de "
        f"{n(INST['payback_meses'], 1)} meses: cumple el criterio de ROI y se acerca, sin cumplirlo, al de 12 meses. Ningún escenario con un solo aula "
        "cumple el payback; el que reparte el desarrollo entre tres instituciones llega a "
        f"{n(ESCA['payback_meses'], 1)} meses. La conclusión financiera es que el sistema se justifica por adopción en <em>varias aulas</em> o "
        "<em>varias instituciones</em>, no por un aula aislada."))
    h.append(tabla("Escenarios frente a los criterios de la guía",
                   ["Escenario", "CAPEX", "Beneficio neto", "ROI año 1", "Payback", "ROI ≥ 30 %", "Payback ≤ 12 m"], esc_f,
                   "Conservador: beneficios 25 % menores. Optimista: suma el instrumental evitado ($ 1.000.000). Institución: cuatro aulas "
                   "(supuesto). Escala: el desarrollo se reparte entre tres instituciones, de un aula cada una.",
                   anchos=["30%", "13%", "13%", "11%", "11%", "11%", "11%"], clase="chica", ref="escen"))
    h.append(figura("Posición acumulada de caja por escenario", svg_inline("flujo_caja_acumulado"),
                    "Posición = −CAPEX + mes × beneficio neto mensual. Los puntos marcan el mes de recuperación; la línea roja, el límite de 12 meses.", ref="caja"))
    h.append(H2("9.5 Sensibilidad"))
    h.append(P(
        "La [[T:sens]] varía cada supuesto en ±20 % del escenario base. La variable que más mueve el ROI es el costo de "
        "desarrollo, que el equipo conoce y controla; le siguen las dos variables de beneficio de campo, que dependen de la "
        "institución y deben medirse en el piloto."))
    h.append(tabla("Sensibilidad del ROI del escenario base a variaciones de ±20 % en un supuesto",
                   ["Supuesto", "ROI con −20 %", "ROI base", "ROI con +20 %", "Rango"], _sens(), anchos=["38%", "16%", "14%", "16%", "16%"], clase="chica", ref="sens"))
    h.append(H2("9.6 Comparación con el modelo del estudio previo"))
    cmp_ = [
        ["CAPEX", "$ 4.370.000", cop(TOT["capex"]), "+80 h de este corte ($ 2.400.000) y consulta jurídica ($ 600.000)"],
        ["OPEX anual", "$ 1.080.000", cop(TOT["opex"]), "Sin nube, tokens de IA ni conectividad (el código no los usa); se añaden reposición y energía"],
        ["Beneficios brutos", "$ 2.800.000", cop(TOT["beneficios"]), "El instrumental evitado ($ 1.000.000) pasa al escenario optimista"],
        ["Beneficio neto", "$ 1.720.000", cop(B1["beneficio_neto"]), "Efecto combinado"],
        ["ROI año 1", "39,36 %", pct(B1["roi_pct"]), "Menor beneficio y mayor CAPEX"],
        ["Payback", "30,5 meses", n(B1["payback_meses"], 1) + " meses", "Menor beneficio y mayor CAPEX"],
    ]
    h.append(P(
        "La aritmética del estudio previo se reprodujo y es correcta: 3,6 + 0,3 + 0,15 + 0,2 + 0,12 = 4,37 millones de CAPEX; "
        "ROI de 39,36 % y payback de 30,5 meses. Las diferencias de la [[T:cmp13]] no son errores de ese estudio sino decisiones de "
        "modelación: este documento incorpora el costo del trabajo de este corte, no cuenta costos que el código no genera y "
        "separa el beneficio discutible."))
    h.append(tabla("Modelo financiero del estudio previo frente a este documento", ["Concepto", "Estudio del Equipo 13", "Este documento", "Motivo de la diferencia"], cmp_,
                   anchos=["16%", "20%", "20%", "44%"], clase="chica", ref="cmp13"))
    return "".join(h)


# ====================================================================== 10
def _n_muestra(d: float, alfa_z=1.959964, pot_z=0.841621) -> int:
    return math.ceil(2 * (alfa_z + pot_z) ** 2 / d ** 2) + 1


def sec10_discusion() -> str:
    h = [H1("10. Discusión y conclusiones")]
    h.append(H2("10.1 Discusión"))
    h.append(P(
        "El resultado técnico más relevante es la distinción entre sensibilidad y especificidad. El método heredado de la versión 1 "
        "reconoce siempre porque responde siempre; el descriptor invariante con la regla de tres condiciones rechaza 92 de cada 100 "
        "posturas que no son seña y conserva un acierto del 96,9 % con ruido moderado. Para un niño, una nota que suena sin haberla "
        "pedido rompe el juego más que una nota que tarda un fotograma más, y el diseño prioriza la primera propiedad."))
    h.append(P(
        "Frente a la literatura revisada, que recurre a modelos de refuerzo profundo o de aprendizaje profundo para adaptar la enseñanza, "
        "HSK adopta una formulación explícita (reglas y MILP) cuyo comportamiento puede explicarse a un docente y que funciona con pocos "
        "datos por niño. La contrapartida es que sus constantes son decisiones de diseño y no resultados de un ajuste con muchos estudiantes."))
    h.append(P(
        "La gobernanza muestra una brecha entre el diseño y la implementación: el principio de privacidad por diseño se cumple (no se "
        "guardan imágenes y no hay red), pero el control de acceso a la Zona de Padres, los respaldos, la retención y el borrado completo son "
        "pendientes, y la base no impone los rangos de los datos. El Anexo D prueba una migración con 16 restricciones CHECK que no rompe la "
        "aplicación, y la [[T:brechas]] prioriza el resto."))
    h.append(P(
        f"En lo financiero, el aula aislada no se paga en el plazo que pide la guía ({pct(B1['roi_pct'])} y {n(B1['payback_meses'], 1)} meses), "
        f"porque el desarrollo pesa el {n(FIN['capex']['Horas de ingeniería y desarrollo'] / TOT['capex'] * 100, 0)} % del CAPEX y los únicos beneficios con cifra de campo son "
        f"{cop(TOT['beneficios'])} anuales. Con cuatro aulas en una institución el ROI es de {pct(INST['roi_pct'])} y el payback de "
        f"{n(INST['payback_meses'], 1)} meses. Esto es coherente con una EBT que replica el mismo software: la rentabilidad proviene de la "
        "escala, no del aula individual."))
    h.append(H2("10.2 Amenazas a la validez"))
    h.append(UL([
        "Validez interna: una sola calibración, de una persona, sustenta las cifras de reconocimiento.",
        "Validez externa: no hay pruebas con niños, con manos pequeñas, iluminación variable ni cámaras de baja gama.",
        "Construcción: el efecto pedagógico (aprendizaje, retención, motivación) no se ha medido; solo el desempeño técnico.",
        "Financiera: los beneficios descansan en dos cifras de campo secundarias y no verificadas, y en el número de aulas.",
        "Bibliográfica: los 15 estudios se sintetizaron a partir de resúmenes y metadatos, no de texto completo."]))
    h.append(H2("10.3 Protocolo de validación en piloto"))
    h.append(P(
        "El piloto convierte los supuestos en datos. Se propone un diseño cuasi-experimental con dos grupos de aulas de la misma institución: "
        "un grupo de control con la instrucción habitual y un grupo experimental con HSK, durante ocho semanas y con una medición de retención "
        "a las cuatro semanas siguientes. Las variables son el puntaje de discriminación de notas (0 a 100), el tiempo de respuesta motriz, la "
        "retención de las notas, las horas docentes de nivelación por semana, el gasto de papelería, la deserción y una escala de motivación "
        f"infantil. Con un nivel de significancia de 0,05 y una potencia de 0,80, una prueba <em>t</em> bilateral requiere unos {_n_muestra(0.8)} niños por "
        f"grupo para detectar un efecto grande (<em>d</em> de Cohen igual a 0,8) y unos {_n_muestra(0.5)} por grupo para un efecto mediano (0,5); el cálculo usa la "
        "aproximación normal. El análisis comparará los grupos con la prueba <em>t</em> de Welch o con la de Mann-Whitney según la normalidad, y "
        "reportará el tamaño del efecto con su intervalo de confianza. La línea base reportada por el estudio previo "
        "(42,91 de 100; 5,48 s; retención inferior al 40 %) sirve como referencia, no como resultado. Antes de empezar se requiere el consentimiento "
        "informado de los representantes, el asentimiento de los niños y el cumplimiento de la Ley 1581 de 2012."))
    h.append(H2("10.4 Conclusiones y trabajo siguiente"))
    h.append(P(
        "Se construyó y verificó técnicamente un prototipo que reconoce las ocho señas de las notas con un descriptor de 120 componentes, en "
        f"{n(BENCH['total_ms']['media'], 1)} ms de cómputo por fotograma, y que adapta la práctica con un gemelo digital y una planificación MILP cuya equivalencia con "
        "la enumeración exacta se comprobó. Se diagnosticó una brecha de conectividad de 18,4 puntos porcentuales entre Córdoba y el promedio nacional, que "
        "justifica el diseño local. Se contrastó el estudio previo con el código y se corrigieron sus cifras técnicas y su modelo económico. "
        f"El modelo financiero, con insumos rotulados por procedencia, arroja para un aula un ROI de {pct(B1['roi_pct'])} y un payback de "
        f"{n(B1['payback_meses'], 1)} meses, y para una institución con cuatro aulas, {pct(INST['roi_pct'])} y {n(INST['payback_meses'], 1)} meses."))
    h.append(P(
        "El trabajo siguiente, en orden de prioridad, es: (a) ejecutar el piloto de la Sección 10.3; (b) cerrar las brechas B1 a B3 de gobernanza; "
        "(c) medir la latencia de extremo a extremo; (d) probar con más de una calibración y con niños; y (e) validar las constantes del modelo pedagógico."))
    return "".join(h)


# ====================================================================== anexos
def anexos() -> str:
    t = BENCH
    h = [H1("Anexo A. Verificación de datos", salto=True)]
    h.append(P(
        "La tabla contrasta las cifras de los documentos previos del proyecto (capítulo de gobernanza y documento del motor analítico) con el valor "
        "verificado y su evidencia. Las afirmaciones del estudio del Equipo 13 se tratan por separado en el Anexo E."))
    filas = [
        ["1", "Dimensión del descriptor", "38", "120 = 2 × 58 + 4", "<em>features.py</em>; medido: 120"],
        ["2", "Clasificador", "k-NN o coseno", "Distancia por bloques y <em>softmax</em> con temperatura adaptativa", "<em>classifier.py</em>"],
        ["3", "Estabilizador", "N = 3; «cero disparos accidentales»", "Ventana 1; liberación 6; 8,0 % de notas por error", "<em>config.py</em>; test_vision"],
        ["4", "Fórmula de dominio", "Suma 0,40·P + 0,25·C + 0,20·V + 0,15·R", "Producto (λ + (1 − λ)R<sup>γ</sup>)(0,55P + 0,25C + 0,20V)", "<em>mastery.py</em>"],
        ["5", "Velocidad", "400 a 2.500 ms", "Referencia por edad (5.200, 4.000, 3.200 ms); mínimo 700 ms", "<em>mastery.py</em>"],
        ["6", "Fotogramas por segundo", "30", f"{CON['target_fps_defecto']} de forma predeterminada", "<em>config.py</em>"],
        ["7", "Exactitud temporal", "«&lt; 35 ms» y «&lt; 5 ms» (contradictorios)", f"Descriptor + clasificador: {n(t['total_ms']['media'], 1)} ms de media, p95 {n(t['total_ms']['p95'], 1)} ms; extremo a extremo no medido", "<em>bench_latencia.py</em>"],
        ["8", "Fatiga y frustración", "F ≥ 0,85; acierto &lt; 60 % en 3 intentos", "Descansar si F ≥ 1; jugar si F ≥ 0,7; ayuda si precisión &lt; 55 %", "<em>adaptation.py</em>"],
        ["9", "Ajuste del predictor", "Gradiente estocástico", "Por lotes: 300 épocas, tasa 0,35; mínimo 40 intentos; cada 20", "<em>predictor.py</em>"],
        ["10", "Módulos", "<em>handsingkids.intelligence.*</em> para todo", "Reparto entre <em>intelligence</em> y <em>learning</em>", "Árbol de directorios"],
        ["11", "Restricciones CHECK", "Presentes en todas las tablas", "Ninguna (0); migración propuesta y probada en el Anexo D", "Auditoría Q4 a Q6"],
        ["12", "Estados de una habilidad", "bloqueada, practicando, dominada", "bloqueada, introducida, en_practica, dominada, consolidada", "<em>SkillStatus</em>"],
        ["13", "Carpeta de datos", "<em>~/.handsingkids/</em>", "Por sistema operativo: carpeta «Hand Sing Kids» de datos del usuario", "<em>config.py</em>"],
        ["14", "Permisos 0600/0700 y cifrado AES-256", "Aplicados", "No hay cambios de permisos ni cifrado; se hereda el perfil del sistema", "Búsqueda en el código"],
        ["15", "Respaldo automático, purga y anonimización anual", "Descritos como vigentes", "No implementados", "Búsqueda en el código"],
        ["16", "Derecho al olvido", "Cascada borra todo", "Cascada en la base (Q7); quedan <em>gestos/perfil_&lt;id&gt;.json</em> y <em>melodias/*.json</em> (Q8)", "Auditoría"],
        ["17", "RBAC", "Matriz de roles vigente", "Sin autenticación: la Zona de Padres se abre con un botón", "<em>home.py</em>"],
        ["18", "«WAL con escrituras asíncronas»", "Asíncronas y no bloqueantes", "WAL sí; escrituras síncronas con bloqueo por hilo", "<em>database.py</em>"],
        ["19", "Tiempo de reacción", "<em>time.perf_counter()</em>", "<em>time.time()</em>", "<em>evaluation.py</em>"],
        ["20", "Estado «100 % operativo»", "Todos los módulos", "14 pantallas construidas y 8 de 8 suites que pasan; TRL 4; sin pruebas con niños", "<em>pruebas.json</em>"],
        ["21", "Solucionador MILP", "CBC mediante PuLP", "Con PuLP 4.0.0 no hay solucionadores; con 2.9.0 sí. La prueba de equivalencia se omite sin CBC", "<em>listSolvers</em>"],
    ]
    h.append(tabla("Datos verificados y correcciones respecto de los documentos previos", ["N.º", "Tema", "Documento previo", "Valor verificado", "Evidencia"], filas,
                   "La prueba de equivalencia MILP y enumeración devolvió, con CBC disponible, el mismo objetivo (3,3798) y las mismas cuatro actividades sobre 24 candidatas.",
                   anchos=["5%", "17%", "22%", "36%", "20%"], clase="larga chica"))
    h.append(H1("Anexo B. Reproducibilidad"))
    h.append(P("Todos los insumos de este documento se regeneran con los <em>scripts</em> de la carpeta <em>_fuentes</em>:"))
    h.append(UL([
        "<em>verificar_doi.py</em>: metadatos de Crossref de los 15 DOI (<em>doi_verificados.json</em>);",
        "<em>bench_latencia.py</em>: latencia del descriptor y el clasificador;",
        "<em>catalogo_datos.py</em> y <em>auditoria_calidad.py</em>: diccionario de datos y pruebas de integridad desde el esquema real;",
        "<em>ddl_checks.py</em> y <em>probar_check_en_app.py</em>: migración CHECK y su prueba sobre la aplicación;",
        "<em>contraste_pint2.py</em>: contraste con las afirmaciones técnicas del estudio previo;",
        "<em>ejecutar_pruebas.py</em>: las ocho suites del proyecto (<em>pruebas.json</em>);",
        "<em>modelo_financiero.py</em> y <em>verificar_xlsx.py</em>: cifras, hoja de cálculo y su comprobación independiente;",
        "<em>diagramas_*.py</em>, <em>poster_diagramas.py</em> y <em>logos.py</em>: figuras vectoriales;",
        "<em>construir_documento.py</em> y <em>construir_poster.py</em>: documento y póster en PDF."]))
    h.append(H1("Anexo C. Supuestos y procedencia de los insumos financieros"))
    filas = [
        ["Tarifa de ingeniería", cop(p := FIN["parametros"]["tarifa_ing"]) + " / h", "Guía UPB", "Rango 25.000 a 40.000"],
        ["Horas de desarrollo", f"{FIN['parametros']['horas_dev_pint2']} h + {FIN['parametros']['horas_dev_corte2']} h", "PINT2 + supuesto", "Validar con la bitácora"],
        ["Kit de hardware y soportes", cop(FIN["parametros"]["hardware_kit"] + FIN["parametros"]["prototipado"]), "PINT2", "Validar con cotización"],
        ["Costo hora docente", cop(FIN["parametros"]["tarifa_docente"]) + " / h", "PINT2", "Validar con la nómina"],
        ["Nivelación docente", f"{n(FIN['parametros']['horas_nivelacion_sem'], 1)} h por semana", "PINT2", "Reportado: 1,0 a 1,5 h; se usa el mínimo"],
        ["Papelería", cop(FIN["parametros"]["papeleria_anual"]) + " por aula y año", "PINT2", "Medir en el piloto"],
        ["Consulta jurídica", cop(FIN["parametros"]["consulta_juridica"]), "Supuesto", "Cotizar"],
        ["Aulas por institución", str(FIN["parametros"]["aulas_institucion"]), "Supuesto", "Solo en el escenario de institución"],
        ["Nube, IA y conectividad", "$ 0", "Verificable", "El código no los usa"],
    ]
    h.append(tabla("Insumos del modelo y su procedencia", ["Insumo", "Valor", "Tipo", "Nota"], filas,
                   "La lista completa está en la hoja <em>Supuestos</em> de <em>04_Modelo_Financiero_ROI_Equipo_XX.xlsx</em>. PINT2 = estudio del Equipo 13, no verificado.",
                   anchos=["30%", "26%", "18%", "26%"], clase="chica"))
    h.append(H1("Anexo D. Migración propuesta de restricciones CHECK"))
    h.append(P(
        "SQLite no permite añadir restricciones CHECK a una columna existente; la migración recrea las tablas afectadas con las "
        "restricciones y copia los datos. El esquema propuesto añade 16 reglas sobre cuatro tablas y se probó de dos maneras. Primero, con "
        f"casos de inserción: {sum(1 for r in CHK['resultados'] if r['correcto'])} de {len(CHK['resultados'])} se comportaron como se esperaba (la base rechaza edad 99 o 2, "
        "confianza 5,0, <em>correct</em> igual a 7, dominio negativo y un estado que no existe, y acepta los valores válidos). Segundo, "
        "ejecutando la suite de integración y la del predictor con ese esquema en lugar del original, que pasaron."))
    reglas = []
    import re
    for linea in SQL.splitlines():
        if "CHECK" in linea:
            reglas.append(linea.strip().rstrip(","))
    h.append(f'<div class="tabla chica"><p class="cap-num">Código 1</p><p class="cap-tit"><em>Restricciones CHECK añadidas al esquema</em></p>'
             f'<pre style="font-size:8.5pt;line-height:1.25;white-space:pre-wrap;border-top:1.2pt solid #000;border-bottom:1.2pt solid #000;padding:4pt 2pt">'
             + "\n".join(r.replace("<", "&lt;").replace(">", "&gt;") for r in reglas) + "</pre>"
             '<p class="nota"><em>Nota.</em> Extraído de <em>propuesta_check.sql</em>. El estado «en_practica» es el valor real del código; el documento previo usaba «practicando».</p></div>')
    h.append(H1("Anexo E. Contraste con el estudio del Equipo 13"))
    h.append(P(
        "El estudio del Equipo 13 (2026) es un documento técnico del mismo proyecto en un semestre anterior. Aporta la caracterización de campo "
        "(Sección 2.5) y un modelo financiero cuya aritmética es correcta. Sin embargo, varias afirmaciones técnicas no coinciden con el código "
        "que este equipo verificó, y algunas referencias no existen. La [[T:contraste]] lo detalla; el criterio fue conservar lo verificable y "
        "no heredar lo que no puede comprobarse."))
    def doi_estado(k):
        v = DOI13[k][0]
        return v.replace("CROSSREF OK", "existe").replace("DATACITE OK", "existe")
    filas = [
        ["Plataforma: Streamlit o Gradio, SimPy, SciPy y API de Gemini", "El código usa PySide6; no menciona Gemini, SimPy, SciPy, Streamlit ni Gradio, y no figuran en <em>requirements.txt</em>", "No coincide"],
        ["30 fotogramas por segundo", f"Valor predeterminado de {CON['target_fps_defecto']}", "No coincide"],
        ["Vector de 38 dimensiones", "120 componentes (Sección 5.2)", "No coincide"],
        ["Solucionador en 38 ms por asignación", f"{n(CON['solver_milp_cbc_ms']['min'], 0)} a {n(CON['solver_milp_cbc_ms']['max'], 0)} ms por sesión (media {n(CON['solver_milp_cbc_ms']['media'], 0)} ms) con CBC y {n(CON['solver_enumeracion_exacta_ms']['min'], 0)} a {n(CON['solver_enumeracion_exacta_ms']['max'], 0)} ms con enumeración, sobre 24 candidatas", "No coincide"],
        ["Latencia de extremo a extremo menor a 50 ms", "No medida; el cómputo propio es de 2,3 ms por fotograma", "Sin evidencia"],
        ["Precisión superior al 94,2 % y TRL 5", "Medido: 100 %, 96,9 % y 86,0 % según el ruido; sin pruebas en aula, TRL 4", "No verificable"],
        ["Ganancia de desempeño de 69,77 %, p &lt; 0,0001 y <em>d</em> de Cohen de 4,929", "No hay datos, <em>script</em> ni grupos experimentales en el repositorio; un <em>d</em> cercano a 5 es excepcional", "No verificable"],
        ["Modelo MILP con variable x<sub>ijt</sub> de tres índices", "El código usa x<sub>i</sub> y siete restricciones distintas (Sección 5.4)", "No coincide"],
        ["Esquema con CHECK, copia diaria cifrada AES-256 y anonimización anual", "No implementados (Anexo A, filas 11, 14 y 15)", "No coincide"],
        ["Cuatro entidades en el diccionario, estado «practicando»", "11 tablas y 97 campos; estado «en_practica»", "Incompleto"],
        ["Referencia Califano y Cammarata (2026)", "El DOI no existe en Crossref ni en DataCite", "Referencia no hallada"],
        ["Referencia Deng, Wang y Zhang (2026)", "El DOI no existe en Crossref ni en DataCite", "Referencia no hallada"],
        ["Referencia Prasanna y Sundaram (2026)", "El DOI no existe en Crossref ni en DataCite", "Referencia no hallada"],
        ["Referencia Matallaoui et al. (2017)", "El DOI citado resuelve a otro artículo; la matriz del proyecto registra una ponencia de la Conferencia de Hawái sobre Ciencias de Sistemas", "DOI incorrecto"],
        ["Referencia Williams (2013), libro", "El DOI citado no existe; el libro es real pero sin ese DOI", "DOI incorrecto"],
        ["Referencias Lugaresi et al. (2019) y Virtanen et al. (2020)", "Existen y coinciden", "Verificadas"],
        ["Modelo financiero (CAPEX $ 4.370.000; ROI 39,36 %; payback 30,5 meses)", "Aritmética reproducida y correcta (Sección 9.6)", "Verificado"],
        ["Cifras de campo de aulas de Montería y Cereté", "Sin metodología ni muestra documentadas", "No verificado; se usa como fuente secundaria"],
    ]
    h.append(tabla("Afirmaciones del estudio previo frente a la verificación", ["Afirmación del estudio", "Verificación de este equipo", "Resultado"], filas,
                   "Verificación del 30 de septiembre de 2026 con <em>contraste_pint2.py</em>, Crossref y DataCite. Este contraste no cuestiona el valor del estudio como "
                   "antecedente; documenta qué cifras pueden usarse y cuáles no.", anchos=["34%", "50%", "16%"], clase="larga chica", ref="contraste"))
    return "".join(h)
