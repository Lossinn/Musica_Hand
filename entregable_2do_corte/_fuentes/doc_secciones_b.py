"""Secciones 6 a 11, referencias y anexos del documento."""
from __future__ import annotations

import json
from pathlib import Path

from datos import (BASE, BENCH, CAT, CONS, DANE, ESC, ESCALA, FIN, TOT, cop, n, pct, referencias_ordenadas)
from doc_base import (H1, H2, H3, P, UL, ecuacion, figura, img, svg_inline, tabla)
import modelo_financiero as MF

F = Path(__file__).resolve().parent
AUD = json.loads((F / "auditoria_calidad.json").read_text(encoding="utf-8"))


# =====================================================================
def sec6_bpmn() -> str:
    h = [H1("6. Modelado de procesos de negocio en BPMN 2.0", salto=True)]
    h.append(P(
        "El proceso modelado es la enseñanza de una nota musical y el seguimiento de su aprendizaje en una escuela "
        "de música infantil. Se representa en <em>Business Process Model and Notation</em>, BPMN 2.0, con "
        "<em>pools</em> para cada participante, <em>swimlanes</em> para los roles, compuertas exclusivas (X), "
        "paralelas (+) e inclusivas (O) con condiciones rotuladas, eventos de inicio, intermedios (temporizador y "
        "mensaje) y de fin, flujos de secuencia de línea continua y flujos de mensaje de línea punteada. El modelo "
        "<em>As-Is</em> combina la práctica habitual de una clase grupal con la literatura y "
        "con la caracterización de campo del estudio previo (Sección 2.5), que es una fuente secundaria no verificada; debe validarse con la institución piloto."))
    h.append(figura("Proceso actual (As-Is): enseñanza de una nota en una escuela de música",
                    svg_inline("bpmn_as_is"),
                    "Los círculos rojos marcan los cuellos de botella enumerados al pie. Elaboración propia en BPMN 2.0.",
                    ancha=True, ref="asis"))
    h.append(figura("Proceso propuesto (To-Be): sesión de práctica con Hand Sing Kids", svg_inline("bpmn_to_be"),
                    "Las tareas amarillas las ejecuta el sistema; el flujo sigue el ciclo de una nota del código de "
                    "HandSingKids7. Los intentos se guardan al cerrar cada actividad, no uno a uno.",
                    ancha=True, ref="tobe"))
    h.append(P(
        "El modelo To-Be se construyó a partir del código: los umbrales de aceptación de la seña, la espera de un "
        "fotograma (aproximadamente 42 ms a 24 fotogramas por segundo), el cierre de la actividad que persiste "
        "intentos y resultado, y la compuerta inclusiva que, según el caso, reparte estrellas y logros, actualiza el "
        "dominio y el repaso, y abre habilidades nuevas. La compuerta paralela refleja que el sonido y el dibujo de "
        "la nota no esperan a la evaluación. La [[T:compar]] contrasta ambos procesos."))
    filas = [
        ["Retroalimentación", "El docente observa y corrige a cada niño, uno por uno", "Reconocimiento por cámara en cada fotograma; sonido y dibujo inmediatos"],
        ["Criterio de acierto", "Subjetivo, sin medición de latencia ni confianza", "Regla explícita: d ≤ 0,95, P ≥ 0,55 y margen ≥ 0,08"],
        ["Registro", "Cuaderno del docente", "SQLite local: intentos, resultados y estado por habilidad"],
        ["Repaso", "No se programa; el olvido no se mide", "Repaso espaciado (SM-2 adaptado) con próxima fecha por habilidad"],
        ["Dificultad", "Decisión intuitiva del docente", "Escalera de ayuda y planificación MILP de la sesión"],
        ["Informe al acudiente", "Verbal o por mensaje, tardío y sin detalle por nota", "Zona de Padres bajo demanda: dominio, confusiones, tiempo de reacción"],
    ]
    h.append(tabla("Comparación entre el proceso actual (As-Is) y el propuesto (To-Be)",
                   ["Aspecto", "As-Is", "To-Be"], filas,
                   "Las mejoras del To-Be son capacidades del prototipo; su efecto sobre el aprendizaje no se ha medido.",
                   anchos=["18%", "38%", "44%"], ref="compar"))
    return "".join(h)


# =====================================================================
def sec7_dfd() -> str:
    h = [H1("7. Diagramas de flujo de datos")]
    h.append(P(
        "Los diagramas siguen la notación de Yourdon y DeMarco: círculos para los procesos, rectángulos para las "
        "entidades externas, rectángulos abiertos para los almacenes de datos y flechas para los flujos. El "
        "<em>nivel 0</em> ([[F:dfd0]]) delimita el sistema y sus tres entidades externas; el <em>nivel 1</em> "
        "([[F:dfd1]]) lo descompone en siete procesos; y el <em>nivel 2</em> ([[F:dfd2]]) detalla el proceso crítico, "
        "la planificación adaptativa, que es el que más transacciones tiene con los almacenes."))
    h.append(figura("DFD nivel 0: diagrama de contexto", svg_inline("dfd_nivel0"),
                    "El sistema no tiene entidades externas en la nube: todos los flujos terminan en el equipo local.", ref="dfd0"))
    h.append(figura("DFD nivel 1: descomposición en siete procesos", svg_inline("dfd_nivel1"),
                    "Los almacenes D1 a D6 se corresponden con tablas y archivos reales ([[T:almac]]).", ancha=True, ref="dfd1"))
    h.append(figura("DFD nivel 2: explosión del proceso 5.0, planificar la sesión adaptativa", svg_inline("dfd_nivel2"),
                    "Las figuras grises son vecinos del nivel 1; el proceso 6.0 se dibuja dos veces (entrada y salida).",
                    ancha=True, ref="dfd2"))
    alm = [
        ["D1", "Perfiles y logros", "profiles, rewards, profile_achievements", "SQLite"],
        ["D2", "Plantillas de calibración", "gestos/perfil_&lt;id&gt;.json (21 puntos por mano, tres muestras por nota)", "Archivo JSON por perfil"],
        ["D3", "Intentos y resultados", "sessions, attempts, activity_results", "SQLite"],
        ["D4", "Estado de habilidades", "skill_state", "SQLite"],
        ["D5", "Catálogo de actividades", "skills, activities, achievements", "SQLite (sembrado en el arranque)"],
        ["D6", "Modelo del predictor", "meta (fila <em>predictor_&lt;id&gt;</em>)", "SQLite"],
    ]
    h.append(tabla("Almacenes de datos de los DFD y su soporte físico", ["Código", "Almacén", "Tablas o archivos", "Soporte"], alm,
                   "Además, las melodías grabadas en Modo libre se guardan como <em>melodias/*.json</em>; no intervienen en el "
                   "flujo del planificador y se tratan en la Sección 8.", anchos=["9%", "24%", "47%", "20%"], ref="almac"))
    h.append(H2("7.1 Balanceo entre niveles"))
    h.append(P(
        "El balanceo exige que los flujos que cruzan la frontera de un proceso en un nivel sean los que entran y "
        "salen de sus hijos en el nivel siguiente. La [[T:balance]] lo comprueba para el paso del nivel 0 al 1 y del 1 al "
        "2 (proceso 5.0). Los flujos del nivel 0 se descomponen sin pérdida ni adición en el nivel 1, y los siete "
        "flujos de la frontera del proceso 5.0 aparecen, con los mismos nombres, en el nivel 2."))
    from diagramas_dfd import BALANCE
    filas = []
    for nivel, d in BALANCE.items():
        for padre, hijos in d.items():
            filas.append([nivel, padre, "; ".join(hijos)])
    h.append(tabla("Comprobación de balanceo entre niveles", ["Transición", "Flujo en el nivel padre", "Flujos en el nivel hijo"],
                   filas, anchos=["18%", "38%", "44%"], clase="larga chica", ref="balance"))
    return "".join(h)


# =====================================================================
DESC = {
    "profiles.id": "Identificador del perfil", "profiles.name": "Nombre de pila o alias del niño",
    "profiles.age": "Edad en años (la interfaz limita a 3-12)", "profiles.avatar": "Clave del personaje gráfico",
    "profiles.created_at": "Fecha de alta (época Unix)", "profiles.last_seen_at": "Última visita (época Unix)",
    "profiles.stars": "Estrellas acumuladas", "profiles.coins": "Monedas acumuladas",
    "profiles.streak_days": "Días consecutivos de práctica", "profiles.last_play_date": "Última fecha de juego (ISO)",
    "profiles.calibrated": "Calibración completada (0 o 1)",
    "skills.code": "Código de la habilidad", "skills.name": "Nombre", "skills.note_code": "Nota asociada, si aplica",
    "skills.level": "Nivel del mapa (1 a 7)", "skills.difficulty": "Dificultad intrínseca [0, 1]",
    "skills.prerequisites": "Habilidades previas (lista JSON)", "skills.order_index": "Orden de presentación",
    "skills.description": "Descripción pedagógica",
    "skill_state.profile_id": "Perfil (llave foránea)", "skill_state.skill_code": "Habilidad (llave foránea)",
    "skill_state.status": "bloqueada, introducida, en_practica, dominada o consolidada",
    "skill_state.mastery": "Dominio M<sub>s</sub> [0, 1]", "skill_state.precision_v": "Precisión suavizada P<sub>s</sub>",
    "skill_state.consistency": "Consistencia C<sub>s</sub>", "skill_state.speed": "Velocidad V<sub>s</sub>",
    "skill_state.retention": "Retención R<sub>s</sub> al actualizar", "skill_state.attempts": "Intentos acumulados",
    "skill_state.hits": "Aciertos acumulados", "skill_state.mean_reaction_ms": "Reacción media (ms)",
    "skill_state.last_practice_at": "Última práctica (época Unix)", "skill_state.due_at": "Próximo repaso (época Unix)",
    "skill_state.ease": "Factor de facilidad ε del repaso", "skill_state.interval_days": "Intervalo de repaso I (días)",
    "activities.code": "Código de la actividad", "activities.kind": "Tipo (ejercicio, repaso, juego, canción, evaluación)",
    "activities.title": "Título", "activities.level": "Nivel del mapa", "activities.difficulty": "Dificultad [0, 1]",
    "activities.skill_codes": "Habilidades que toca (lista JSON)", "activities.sequence": "Secuencia de notas (lista JSON)",
    "activities.mode": "Modo (guiado, etc.)", "activities.tempo_bpm": "Tempo en pulsos por minuto",
    "activities.duration_s": "Duración estimada (s)", "activities.hints": "Ayudas visuales (0 o 1)",
    "activities.repetitions": "Repeticiones", "activities.description": "Descripción", "activities.icon": "Ícono",
    "activities.tolerance_ms": "Tolerancia temporal (ms)",
    "sessions.id": "Identificador de la sesión", "sessions.profile_id": "Perfil (llave foránea)",
    "sessions.started_at": "Inicio (época Unix)", "sessions.ended_at": "Fin (época Unix), nulo si sigue abierta",
    "sessions.activities_done": "Actividades completadas", "sessions.accuracy": "Precisión de la sesión (%)",
    "attempts.id": "Identificador del intento", "attempts.profile_id": "Perfil (llave foránea)",
    "attempts.session_id": "Sesión (llave foránea, nula si se borra)", "attempts.activity_code": "Actividad",
    "attempts.step_index": "Posición del paso", "attempts.expected": "Nota esperada", "attempts.detected": "Nota detectada, nula si expiró el tiempo",
    "attempts.confidence": "Confianza del clasificador [0, 1]", "attempts.correct": "Acierto (0 o 1)",
    "attempts.reaction_ms": "Tiempo de reacción (ms)", "attempts.attempt_number": "Número de intento en el paso",
    "attempts.at": "Momento del intento (época Unix)",
    "activity_results.id": "Identificador del resultado", "activity_results.profile_id": "Perfil (llave foránea)",
    "activity_results.session_id": "Sesión (llave foránea)", "activity_results.activity_code": "Actividad",
    "activity_results.accuracy": "Precisión (%)", "activity_results.rhythm": "Puntaje de ritmo",
    "activity_results.gesture_quality": "Calidad del gesto", "activity_results.stars": "Estrellas (0 a 3)",
    "activity_results.score": "Puntaje", "activity_results.max_combo": "Mayor racha de aciertos",
    "activity_results.duration_s": "Duración (s)", "activity_results.steps_total": "Pasos totales",
    "activity_results.steps_correct": "Pasos acertados", "activity_results.at": "Momento (época Unix)",
    "rewards.id": "Identificador", "rewards.profile_id": "Perfil (llave foránea)", "rewards.kind": "Tipo de recompensa",
    "rewards.code": "Código", "rewards.label": "Texto mostrado", "rewards.icon": "Ícono", "rewards.at": "Momento (época Unix)",
    "achievements.code": "Código del logro", "achievements.title": "Título", "achievements.description": "Descripción",
    "achievements.icon": "Ícono",
    "profile_achievements.profile_id": "Perfil (llave foránea)", "profile_achievements.code": "Logro (llave foránea)",
    "profile_achievements.at": "Momento en que se obtuvo",
    "meta.key": "Clave (por ejemplo, predictor_&lt;id&gt;)", "meta.value": "Valor (JSON del modelo u otros ajustes)",
}


def _restr(c, fks):
    r = []
    if c["pk"]:
        r.append("PK")
    if c["not_null"]:
        r.append("NOT NULL")
    if c["defecto"] is not None:
        r.append(f"por defecto {c['defecto']}")
    for f in fks:
        if f["col"] == c["nombre"]:
            r.append(f"FK → {f['ref_tabla']} ({f['on_delete'].lower()})")
    return ", ".join(r) or "—"


def sec8_gobernanza() -> str:
    h = [H1("8. Gobernanza de datos", salto=True)]
    res = CAT["_resumen"]
    h.append(P(
        "El marco de gobernanza toma como referencia el cuerpo de conocimiento de gestión de datos, DAMA-DMBOK "
        "(DAMA International, 2017), en sus áreas de arquitectura, modelado y almacenamiento, seguridad, calidad y "
        "metadatos. Se distingue en todo el apartado entre lo que el código <em>impone hoy</em>, lo que se "
        "comprobó con una prueba y lo que es <em>política objetivo</em> aún no implementada, porque los documentos "
        "previos describían como existentes varios controles que el código no contiene (Anexo A)."))
    h.append(P(
        "Los principios son tres. <em>Privacidad por diseño</em>: ningún fotograma se escribe en disco y el paquete no "
        "importa módulos de red; solo se conservan coordenadas numéricas de 21 puntos por mano. <em>Soberanía de los "
        "datos</em>: arquitectura <em>local-first</em>, sin cuentas ni nube. <em>Calidad medible</em>: indicadores con "
        "un procedimiento de comprobación (Sección 8.3)."))
    h.append(H2("8.1 Catálogo y diccionario de datos"))
    h.append(P(
        f"El repositorio relacional es SQLite, con {res['tablas']} tablas y {res['columnas']} columnas, en modo de registro "
        "anticipado (<em>write-ahead logging</em>, WAL) y con llaves foráneas activas. El catálogo de la [[T:dicc]] se "
        "extrajo del esquema real mediante las instrucciones <em>PRAGMA</em> de SQLite, por lo que no puede diferir "
        "del código. Las cardinalidades son de uno a muchos desde <em>profiles</em> hacia <em>skill_state</em>, "
        "<em>sessions</em>, <em>attempts</em>, <em>activity_results</em>, <em>rewards</em> y <em>profile_achievements</em>; "
        "<em>skills</em> se relaciona con <em>skill_state</em> y <em>achievements</em> con <em>profile_achievements</em>."))
    filas = []
    for t, v in CAT.items():
        if t.startswith("_"):
            continue
        for c in v["columnas"]:
            filas.append([f"<em>{t}</em>", c["nombre"], c["tipo"], _restr(c, v["fks"]), DESC.get(f"{t}.{c['nombre']}", "")])
    h.append(tabla("Diccionario de datos del esquema SQLite de HandSingKids7",
                   ["Tabla", "Campo", "Tipo", "Restricciones impuestas", "Descripción"], filas,
                   f"Fuente: <em>catalogo_datos.py</em>. Las reglas de dominio (edad entre 3 y 12, intervalos [0, 1], "
                   f"valores binarios) <em>no</em> están impuestas por la base: el esquema no contiene ninguna restricción "
                   f"CHECK ({res['check_constraints']}). Esas reglas se aplican en la interfaz y en el código de dominio.",
                   anchos=["14%", "15%", "9%", "28%", "34%"], clase="larga chica", ref="dicc"))
    h.append(P(
        "Fuera de la base existen dos almacenes de archivos: <em>gestos/perfil_&lt;id&gt;.json</em>, con las "
        "coordenadas de las muestras de calibración de cada niño, y <em>melodias/*.json</em>, con las melodías grabadas "
        "en Modo libre, que incluyen el nombre del perfil, la lista de notas y los intervalos. Ninguno de los dos "
        "aparecía en los documentos previos."))
    h.append(H2("8.2 Linaje del dato"))
    h.append(P(
        "El linaje ([[F:linaje]]) describe el recorrido de los datos desde la cámara hasta el informe. Las etapas 1 a 3 "
        "son efímeras y viven solo en la memoria del proceso; las etapas 4 y 5 existen en la memoria de la sesión; "
        "a partir del cierre de cada actividad (etapa 6) el dato es persistente. La [[T:traza]] resume la "
        "trazabilidad con su clasificación de seguridad."))
    h.append(figura("Linaje del dato, de la cámara al informe para adultos", svg_inline("linaje_dato"),
                    "Elaboración propia a partir del código (<em>vision</em>, <em>learning.session_flow</em> y <em>data</em>).",
                    ancha=True, ref="linaje"))
    lin = [
        ["1 Captura", "Fotogramas de la cámara", "Video RGB", "Fotograma en memoria", "RAM", "Efímero"],
        ["2 Detección", "MediaPipe Hands", "Fotograma", "21 puntos 3D por mano", "RAM", "Efímero"],
        ["3 Descriptor", "Normalización e invariancia", "21 puntos por mano", "Vector de 120 componentes", "RAM", "Efímero"],
        ["4 Clasificación", "Distancia por bloques, softmax y estabilizador", "Vector y plantillas", "Nota y confianza", "Memoria de la sesión", "De sesión"],
        ["5 Evaluación", "Comparación con la nota esperada y medición de la reacción", "Nota y marca de tiempo", "Acierto, latencia", "Memoria de la actividad", "De sesión"],
        ["6 Cierre de actividad", "Persistencia de intentos y resultado", "Intentos de la actividad", "Filas de <em>attempts</em> y <em>activity_results</em>", "SQLite", "Persistente"],
        ["7 Gemelo y predictor", "Dominio, retención, repaso y reajuste del modelo", "Historial del perfil", "<em>skill_state</em>; fila de <em>meta</em>", "SQLite", "Persistente"],
        ["8 Consumo", "Planificación de la sesión; consulta de la Zona de Padres", "Estado por habilidad", "Ruta del día; informe", "Interfaz local", "Por consulta"],
    ]
    h.append(tabla("Trazabilidad extremo a extremo", ["Etapa", "Transformación", "Entrada", "Salida", "Ubicación", "Retención"], lin,
                   anchos=["12%", "26%", "14%", "20%", "16%", "12%"], clase="chica", ref="traza"))
    h.append(H2("8.3 Calidad del dato"))
    h.append(P(
        "La [[T:calidad]] define cuatro dimensiones de calidad con su indicador, su umbral y el estado de verificación. "
        "Los umbrales de completitud y consistencia son <em>objetivos</em>; el estado indica qué parte la base impone "
        "hoy. Para obtener evidencia se ejecutó una auditoría de integridad sobre la clase <em>Database</em> real "
        "([[T:audit]])."))
    calidad = [
        ["Completitud", "Campos críticos no nulos: 1 − nulos/esperados", "100 % en llaves y medidas",
         "Impuesta por NOT NULL en los campos críticos (prueba Q3)"],
        ["Exactitud", "Acierto del reconocimiento; error de tiempo", "Acierto ≥ 96 % con ruido 0,06; confianza ≥ 0,55",
         "Medida en Tabla 4. Los tiempos usan el reloj del sistema (<em>time.time()</em>), no un contador de alta resolución; el error de tiempo no se midió"],
        ["Consistencia", "Registros con integridad referencial / total", "100 %",
         "Referencial impuesta (Q2, Q7). Rangos de dominio no impuestos (Q4, Q5, Q6)"],
        ["Oportunidad", "Latencia entre el intento y la actualización del gemelo", "Actualización al cerrar la actividad",
         "Las escrituras son síncronas con confirmación por sentencia y bloqueo por hilo; la latencia de persistencia no se midió"],
    ]
    h.append(tabla("Dimensiones, indicadores y estado de verificación", ["Dimensión", "Indicador", "Umbral", "Estado"], calidad,
                   anchos=["14%", "30%", "24%", "32%"], clase="chica", ref="calidad"))
    aud = [[r["id"], r["regla"], "Sí" if r["cumple"] else "No", r["detalle"]] for r in AUD["resultados"]]
    h.append(tabla("Auditoría de integridad sobre el esquema real",
                   ["Prueba", "Regla", "¿Impuesta?", "Evidencia"], aud,
                   f"Ejecutada con <em>auditoria_calidad.py</em>: {AUD['cumplen']} de {AUD['total']} reglas impuestas. "
                   "Q4 a Q6 muestran que la base acepta valores fuera de rango; Q8 que el borrado del perfil no elimina "
                   "los archivos JSON.", anchos=["8%", "40%", "10%", "42%"], clase="chica", ref="audit"))
    h.append(H2("8.4 Seguridad, privacidad y control de acceso"))
    h.append(P(
        "Estado verificado: el paquete no escribe imágenes ni video en disco, no importa módulos de red, guarda los "
        "datos en la carpeta de datos del usuario del sistema operativo (en Windows, <em>%APPDATA%\\Hand Sing Kids</em>; en "
        "macOS, <em>~/Library/Application Support/Hand Sing Kids</em>; en Linux, <em>~/.local/share/Hand Sing Kids</em>) y "
        "no cifra ni cambia los permisos de los archivos, de modo que la protección es la del perfil del usuario del "
        "sistema. La Zona de Padres se abre con un botón, sin autenticación: los roles de la [[T:rbac]] son, por ahora, "
        "una convención de la interfaz y no un control."))
    rbac = [
        ["Niño o niña", "Jugar, calibrar, ver su progreso en la interfaz infantil", "Interfaz infantil", "Parcial: no hay barrera hacia la Zona de Padres ni hacia Ajustes", "Protección con PIN de adulto"],
        ["Padre, madre o docente", "Crear y borrar perfiles, leer informes, cambiar ajustes", "Botón «Zona de padres» y «Ajustes»", "Pendiente: sin autenticación", "PIN de adulto de 4 dígitos, guardado con <em>hash</em> y sal"],
        ["Motor analítico", "Escribir intentos y estado, leer y escribir el modelo", "Código de la aplicación", "Implementado", "—"],
        ["Cámara", "Entregar fotogramas al detector", "Proceso de la aplicación", "Implementado: sin persistencia", "—"],
    ]
    h.append(tabla("Control de acceso basado en roles, RBAC: estado actual y propuesta",
                   ["Rol", "Capacidad prevista", "Mecanismo actual", "Estado", "Propuesta"], rbac,
                   "RBAC = <em>role-based access control</em>. El PIN es una propuesta; no existe en el código.",
                   anchos=["14%", "26%", "16%", "24%", "20%"], clase="chica", ref="rbac"))
    h.append(P(
        "En cuanto a la normativa, la Ley Estatutaria 1581 de 2012 dicta las disposiciones generales para la "
        "protección de datos personales en Colombia y contiene reglas especiales para el tratamiento de datos de "
        "niños, niñas y adolescentes (Congreso de la República, 2012). El procesamiento local reduce la exposición, "
        "pero no exime a la institución que use HSK de obtener la autorización de los representantes para registrar "
        "el nombre, la edad y el desempeño de un menor. Por esa razón se presupuestó una consulta jurídica en el "
        "CAPEX (Sección 9). Este documento no constituye asesoría legal."))
    h.append(H2("8.5 Respaldo y ciclo de vida: política objetivo"))
    h.append(P(
        "El código actual <em>no</em> implementa respaldos, compactación ni purga. La [[T:politica]] fija la política "
        "objetivo con parámetros comprobables. Un punto crítico es que la compactación de intentos antiguos en "
        "agregados destruiría los datos que <em>MasteryPredictor</em> necesita para reajustarse; por eso se "
        "conservan siempre los intentos más recientes de cada niño."))
    pol = [
        ["Respaldo", "Copia de la base con la API de respaldo en línea de SQLite al iniciar la sesión si hay más de 20 intentos nuevos; se rotan las últimas 3 copias", "No implementado"],
        ["Conservación activa", "Intentos de los últimos 180 días disponibles con todo detalle, y siempre los últimos 200 intentos del niño para el predictor", "No implementado"],
        ["Agregación", "Los intentos más antiguos se resumen en métricas semanales por habilidad, sin tocar los 200 más recientes", "No implementado"],
        ["Eliminación", "Al borrar un perfil, eliminar sus filas (ya ocurre por cascada), su archivo <em>gestos/perfil_&lt;id&gt;.json</em>, sus melodías y las copias de respaldo que lo contengan", "Parcial: solo la cascada en la base (Q7, Q8)"],
        ["Permisos", "Carpeta de datos accesible solo por el usuario; en Windows, la lista de control de acceso del perfil del usuario", "Heredado del sistema operativo"],
    ]
    h.append(tabla("Política de respaldo, retención y eliminación", ["Elemento", "Política objetivo", "Estado"], pol,
                   "Los parámetros (20 intentos, 3 copias, 180 días, 200 intentos) son propuestas de diseño.",
                   anchos=["16%", "60%", "24%"], clase="chica", ref="politica"))
    h.append(H2("8.6 Plan de cierre de brechas"))
    brechas = [
        ["B1", "Añadir restricciones CHECK (edad 3 a 12; valores en [0, 1]; binarios en {0, 1}) mediante migración", "Alta", "Bajo"],
        ["B2", "Eliminar plantillas y melodías al borrar un perfil", "Alta", "Bajo"],
        ["B3", "PIN de adulto para la Zona de Padres y Ajustes", "Alta", "Medio"],
        ["B4", "Respaldo automático con rotación de 3 copias", "Media", "Medio"],
        ["B5", "Política de agregación que conserve los intentos del predictor", "Media", "Medio"],
        ["B6", "Medir la latencia de extremo a extremo y la de persistencia", "Media", "Bajo"],
        ["B7", "Fijar <em>pulp==2.9.0</em> (con PuLP 4.0.0 no hubo solucionadores disponibles) y hacer que la prueba de equivalencia MILP falle, en lugar de omitirse, cuando falte CBC", "Media", "Bajo"],
        ["B8", "Cifrado de la base en reposo (opcional)", "Baja", "Alto"],
    ]
    h.append(tabla("Brechas de gobernanza detectadas y acciones propuestas", ["Id", "Acción", "Prioridad", "Esfuerzo"], brechas,
                   anchos=["7%", "69%", "12%", "12%"], clase="chica", ref="brechas"))
    return "".join(h)


# =====================================================================
def _sens() -> list[list[str]]:
    base = FIN["parametros"]
    filas = []
    def roi(**kw):
        p = dict(base); p.update(kw)
        return MF.calcular(p)["escenarios"]["Base (1 institución)"]["roi_pct"]
    r0 = roi()
    casos = [
        ("Horas docentes ahorradas por semana", "horas_ahorro_sem"),
        ("Reducción de deserción (puntos)", "desercion_sistema"),
        ("Familias que contratan práctica en casa", "familias_pct"),
        ("Horas de ingeniería y desarrollo", "horas_dev"),
        ("Costo hora docente", "tarifa_docente"),
    ]
    for nombre, k in casos:
        v = base[k]
        if k == "desercion_sistema":
            bajo = roi(desercion_sistema=base["desercion_base"] - (base["desercion_base"] - v) * 0.8)
            alto = roi(desercion_sistema=base["desercion_base"] - (base["desercion_base"] - v) * 1.2)
        else:
            bajo, alto = roi(**{k: v * 0.8}), roi(**{k: v * 1.2})
        filas.append([nombre, pct(bajo), pct(r0), pct(alto), n(abs(alto - bajo), 1) + " p. p."])
    return sorted(filas, key=lambda f: -float(f[4].split()[0].replace(",", ".")))


def sec9_financiero() -> str:
    h = [H1("9. Viabilidad financiera", salto=True)]
    h.append(P(
        "El modelo sigue la guía metodológica del curso. El beneficio neto anual es el beneficio bruto menos los "
        "costos operativos, <em>OPEX</em>; el retorno sobre la inversión, <em>ROI</em>, es el cociente entre el "
        "beneficio neto anual y la inversión inicial, <em>CAPEX</em>; y el periodo de recuperación, <em>payback</em>, "
        "es el CAPEX dividido por el beneficio neto mensual:"))
    h.append(ecuacion("ROI = ( Beneficio neto anual / CAPEX ) × 100 % ,&nbsp;&nbsp; Payback (meses) = CAPEX / ( Beneficio neto anual / 12 )"))
    h.append(P(
        "La unidad de análisis es una institución de educación musical de Montería con 60 niños de 3 a 12 años. "
        "Como no se dispone de datos de campo, todos los insumos distintos de la tarifa de ingeniería, tomada del "
        "rango de la guía, son <em>supuestos</em> explícitos que un piloto debe contrastar; están resaltados en la hoja de "
        "cálculo y se enumeran en el Anexo C. Las cifras de este apartado son las de esa hoja, generadas desde una "
        "única fuente para que el documento, el póster y la hoja coincidan."))
    cap = [[k, cop(v)] for k, v in FIN["capex"].items()] + [["Total CAPEX (I<sub>0</sub>)", cop(TOT["capex"])]]
    h.append(H2("9.1 Inversión inicial (CAPEX)"))
    h.append(P(
        "El CAPEX se compone en su mayor parte de las horas de ingeniería del equipo (80 % del total). "
        "El licenciamiento es cero porque las dependencias son de código abierto según la licencia que declara cada "
        "proyecto (MediaPipe y OpenCV, Apache 2.0; PySide6, LGPL; PuLP, MIT; NumPy, BSD); conviene confirmarlo al "
        "empaquetar la aplicación."))
    h.append(tabla("CAPEX por componente", ["Componente", "Valor (COP)"], cap,
                   "Horas de ingeniería: 360 h × $ 30.000. Cámaras: 6 × $ 130.000. Soportes: 6 × $ 45.000. "
                   "Capacitación: 8 h de facilitador más 3 docentes × 8 h × $ 35.000. Consulta jurídica: $ 600.000.",
                   anchos=["70%", "30%"], clase="chica"))
    h.append(H2("9.2 Costos operativos (OPEX) y beneficios"))
    ox = [[k, cop(v)] for k, v in FIN["opex"].items()] + [["Total OPEX anual", cop(TOT["opex"])]]
    h.append(tabla("OPEX anual por componente", ["Componente", "Valor anual (COP)"], ox,
                   "El costo de nube es cero porque el procesamiento es local; no hay servidores ni interfaces de programación de pago.",
                   anchos=["70%", "30%"], clase="chica"))
    bn = [[k, cop(v)] for k, v in FIN["beneficios"].items()] + [["Total beneficios brutos anuales", cop(TOT["beneficios"])]]
    h.append(P(
        "Los beneficios se cuantifican con las categorías de la guía. El ahorro de horas docentes resulta de 3 h por "
        "semana × 38 semanas × $ 35.000. La menor deserción supone que, con el sistema, la deserción anual baja del "
        f"25 % al 15 %, es decir, {n(FIN['desertores_retenidos'], 0)} de los 60 niños permanecen, con una cuota mensual de "
        "$ 110.000 durante 6 meses. Los ingresos por licencias de práctica en casa suponen que el 20 % de las familias "
        "paga $ 12.000 al mes durante 9 meses; se fijó en 20 % porque solo el "
        f"{n(DANE['hog_comp_nal'], 1)} % de los hogares del país posee computador (Sección 2)."))
    h.append(tabla("Beneficios brutos anuales cuantificados", ["Beneficio", "Valor anual (COP)"], bn,
                   "La deserción base del 25 %, su reducción de 10 puntos y la cuota son supuestos; no hay datos de la "
                   "institución que los respalden todavía.", anchos=["70%", "30%"], clase="chica"))
    h.append(H2("9.3 Indicadores de retorno"))
    plant = [
        ["Inversión inicial (CAPEX)", "Desarrollo, hardware, prototipado, capacitación y consulta jurídica", cop(TOT["capex"])],
        ["Costos operativos anuales (OPEX)", "Soporte, reposición de cámaras y energía; sin nube", cop(TOT["opex"])],
        ["Beneficios brutos anuales", "Ahorro de horas docentes, deserción evitada y licencias", cop(TOT["beneficios"])],
        ["Beneficio neto anual", "Beneficios brutos − OPEX", cop(BASE["beneficio_neto"])],
        ["ROI calculado (año 1)", "(Beneficio neto / CAPEX) × 100", pct(BASE["roi_pct"])],
        ["Periodo de retorno (payback)", "CAPEX / beneficio neto mensual", n(BASE["payback_meses"], 1) + " meses"],
    ]
    h.append(P(
        f"La [[T:plantilla]] reproduce la plantilla obligatoria de la guía para el escenario base. El beneficio neto anual es "
        f"{cop(BASE['beneficio_neto'])}, que equivale a {cop(BASE['beneficio_neto_mensual'])} por mes; el ROI es de "
        f"{pct(BASE['roi_pct'])} y el periodo de recuperación, de {n(BASE['payback_meses'], 1)} meses."))
    h.append(tabla("Plantilla financiera del escenario base (una institución)", ["Componente financiero", "Descripción", "Valor"], plant,
                   anchos=["30%", "48%", "22%"], clase="chica", ref="plantilla"))
    esc_f = []
    for k, e in ESC.items():
        esc_f.append([k, cop(e["capex"]), cop(e["beneficio_neto"]), pct(e["roi_pct"]), n(e["payback_meses"], 1) + " meses",
                      "Sí" if e["roi_pct"] >= 30 else "No", "Sí" if e["payback_meses"] <= 12 else "No"])
    h.append(P(
        "Los criterios de la guía para proyectos de software son un ROI de al menos 30 % en el primer año y un periodo "
        "de recuperación de hasta 12 meses. La [[T:escen]] muestra que el ROI cumple en los tres escenarios, pero "
        "el payback solo cumple cuando el costo de desarrollo se reparte entre tres instituciones. En el escenario base "
        f"el payback de {n(BASE['payback_meses'], 1)} meses <em>no cumple</em> el criterio de 12 meses: es un resultado "
        "que se informa tal cual, sin ajustar los supuestos para que cumpla."))
    h.append(tabla("Escenarios frente a los criterios de la guía",
                   ["Escenario", "CAPEX", "Beneficio neto", "ROI año 1", "Payback", "ROI ≥ 30 %", "Payback ≤ 12 m"], esc_f,
                   "Conservador: beneficios 25 % menores. Escala: el costo de desarrollo se reparte entre tres instituciones, "
                   "cada una con los mismos beneficios.", anchos=["30%", "13%", "14%", "11%", "12%", "10%", "10%"], clase="chica", ref="escen"))
    h.append(figura("Posición acumulada de caja por escenario", svg_inline("flujo_caja_acumulado"),
                    "Posición = −CAPEX + mes × beneficio neto mensual. Los puntos marcan el mes de recuperación; la línea roja, el límite de 12 meses.", ref="caja"))
    h.append(H2("9.4 Sensibilidad"))
    h.append(P(
        "La [[T:sens]] varía cada supuesto en ±20 % manteniendo los demás. La variable que más mueve el ROI es el "
        "costo de desarrollo (horas de ingeniería), que el equipo conoce y controla. Le siguen las horas docentes "
        "ahorradas y la deserción evitada, que desconoce y dependen del comportamiento de la institución; por eso el "
        "piloto debe medir primero esas dos."))
    h.append(tabla("Sensibilidad del ROI del escenario base a variaciones de ±20 % en un supuesto",
                   ["Supuesto", "ROI con −20 %", "ROI base", "ROI con +20 %", "Rango"], _sens(),
                   "Para la deserción, la variación se aplica a la reducción (10 puntos), no al nivel base.",
                   anchos=["38%", "16%", "14%", "16%", "16%"], clase="chica", ref="sens"))
    return "".join(h)


# =====================================================================
def sec10_discusion() -> str:
    h = [H1("10. Discusión y conclusiones")]
    h.append(H2("10.1 Discusión"))
    h.append(P(
        "El resultado técnico más relevante es la distinción entre sensibilidad y especificidad. El método heredado de "
        "la versión 1 reconoce siempre porque responde siempre; el descriptor invariante con la regla de tres "
        "condiciones rechaza 92 de cada 100 posturas que no son seña y conserva un acierto del 96,9 % con ruido "
        "moderado. Para un niño, una nota que suena sin haberla pedido rompe el juego más que una nota que tarda un "
        "fotograma más, y el diseño prioriza la primera propiedad."))
    h.append(P(
        "Frente a la literatura revisada, que recurre a modelos de refuerzo profundo o de aprendizaje profundo para "
        "adaptar la enseñanza, HSK adopta una formulación explícita (reglas y MILP) cuyo comportamiento puede "
        "explicarse a un docente y que funciona con pocos datos por niño. La contrapartida es que sus constantes "
        "son decisiones de diseño y no resultados de un ajuste con datos de muchos estudiantes."))
    h.append(P(
        "La gobernanza muestra una brecha entre el diseño y la implementación: el principio de privacidad por diseño se "
        "cumple (no se guardan imágenes y no hay red), pero el control de acceso a la Zona de Padres, los respaldos, "
        "la retención y el borrado completo son pendientes, y la base no impone los rangos de los datos. La [[T:brechas]] "
        "las prioriza."))
    h.append(P(
        "El resultado financiero depende de supuestos. El ROI del escenario base supera el umbral de 30 %, pero el "
        "payback de 23,4 meses queda por encima de 12 meses; el modelo solo cumple ambos criterios si el desarrollo "
        "se reparte entre varias instituciones, lo que es coherente con una EBT que replica el mismo software."))
    h.append(H2("10.2 Amenazas a la validez"))
    h.append(UL([
        "Validez interna: una sola calibración, de una persona, sustenta las cifras de reconocimiento.",
        "Validez externa: no hay pruebas con niños, con manos pequeñas, iluminación variable ni cámaras de baja gama.",
        "Construcción: el efecto pedagógico (aprendizaje, retención) no se ha medido; solo se midió el desempeño técnico.",
        "Financiera: los beneficios descansan en tres supuestos de comportamiento que no se han contrastado.",
        "Bibliográfica: los 15 estudios se sintetizaron a partir de resúmenes y metadatos, no de texto completo."]))
    h.append(H2("10.3 Conclusiones y trabajo siguiente"))
    h.append(P(
        "Se construyó y verificó técnicamente un prototipo que reconoce las ocho señas de las notas con un descriptor de "
        f"120 componentes, en {n(BENCH['total_ms']['media'], 1)} ms de cómputo por fotograma, y que adapta la práctica con un "
        "gemelo digital y una planificación MILP cuya equivalencia con la enumeración exacta se comprobó. Se "
        "diagnosticó una brecha de conectividad de 18,4 puntos porcentuales entre Córdoba y el promedio nacional, que "
        "justifica el diseño local. El modelo financiero, con supuestos explícitos, arroja un ROI de "
        f"{pct(BASE['roi_pct'])} y un payback de {n(BASE['payback_meses'], 1)} meses para una institución, y "
        f"{pct(ESCALA['roi_pct'])} y {n(ESCALA['payback_meses'], 1)} meses con desarrollo compartido."))
    h.append(P("El trabajo siguiente, en orden de prioridad, es: (a) probar el sistema con niños reales y con más de una "
               "calibración; (b) medir en un piloto las horas docentes ahorradas, la deserción y la disposición a "
               "pagar; (c) cerrar las brechas B1 a B3 de gobernanza; (d) medir la latencia de extremo a extremo; y (e) "
               "validar las constantes del modelo pedagógico con los datos que la aplicación ya registra."))
    return "".join(h)


# =====================================================================
def referencias() -> str:
    h = [H1("Referencias", salto=True), '<div class="ref">']
    for r in referencias_ordenadas():
        h.append(f"<p>{r}</p>")
    h.append("</div>")
    return "".join(h)


def anexos() -> str:
    h = [H1("Anexo A. Verificación de datos", salto=True)]
    h.append(P(
        "La tabla contrasta las cifras de los documentos previos (capítulo de gobernanza y documento del motor "
        "analítico) con el valor verificado y su evidencia. Las filas 1 a 10 son discrepancias entre documentos que ya "
        "estaban anotadas; las restantes son hallazgos nuevos de esta verificación."))
    t = BENCH
    filas = [
        ["1", "Dimensión del descriptor", "38", "120 = 2 × 58 + 4", "<em>features.py</em>; medido: 120"],
        ["2", "Clasificador", "k-NN o coseno", "Distancia por bloques y <em>softmax</em> con temperatura adaptativa", "<em>classifier.py</em>"],
        ["3", "Estabilizador", "N = 3; «cero disparos accidentales»", "Ventana 1; liberación 6; 8,0 % de notas por error", "<em>config.py</em>; test_vision"],
        ["4", "Fórmula de dominio", "Suma 0,40·P + 0,25·C + 0,20·V + 0,15·R", "Producto (λ + (1 − λ)R<sup>γ</sup>)(0,55P + 0,25C + 0,20V)", "<em>mastery.py</em>"],
        ["5", "Velocidad", "400 a 2.500 ms", "Referencia por edad (5.200, 4.000, 3.200 ms); mínimo 700 ms", "<em>mastery.py</em>"],
        ["6", "Fotogramas por segundo", "30", "24 de forma predeterminada", "<em>config.py</em> (target_fps)"],
        ["7", "Exactitud temporal", "«&lt; 35 ms» y «&lt; 5 ms» (contradictorios)", f"Descriptor + clasificador: {n(t['total_ms']['media'], 1)} ms de media, p95 {n(t['total_ms']['p95'], 1)} ms; extremo a extremo no medido", "<em>bench_latencia.py</em>"],
        ["8", "Fatiga y frustración", "F ≥ 0,85; acierto &lt; 60 % en 3 intentos", "Descansar si F ≥ 1; jugar si F ≥ 0,7; ayuda si precisión &lt; 55 %", "<em>adaptation.py</em>"],
        ["9", "Ajuste del predictor", "Gradiente estocástico", "Por lotes: 300 épocas, tasa 0,35; mínimo 40 intentos; cada 20", "<em>predictor.py</em>"],
        ["10", "Módulos", "<em>handsingkids.intelligence.*</em> para todo", "Reparto entre <em>intelligence</em> y <em>learning</em>", "Árbol de directorios"],
        ["11", "Restricciones CHECK", "Presentes en todas las tablas", "Ninguna (0)", "Auditoría Q4 a Q6"],
        ["12", "Carpeta de datos", "<em>~/.handsingkids/</em>", "Por sistema operativo: carpeta «Hand Sing Kids» de datos del usuario", "<em>config.py</em>"],
        ["13", "Permisos 0600/0700", "Aplicados", "No hay cambios de permisos; se hereda el perfil del sistema", "Búsqueda en el código"],
        ["14", "Respaldo automático y purga", "Descritos como vigentes", "No implementados", "Búsqueda en el código"],
        ["15", "Derecho al olvido", "Cascada borra todo", "Cascada en la base (Q7); quedan <em>gestos/perfil_&lt;id&gt;.json</em> y <em>melodias/*.json</em> (Q8)", "Auditoría"],
        ["16", "RBAC", "Matriz de roles vigente", "Sin autenticación: la Zona de Padres se abre con un botón", "<em>home.py</em>"],
        ["17", "«WAL con escrituras asíncronas»", "Asíncronas y no bloqueantes", "WAL sí; escrituras síncronas con bloqueo por hilo", "<em>database.py</em>"],
        ["18", "Tiempo de reacción", "<em>time.perf_counter()</em>", "<em>time.time()</em>", "<em>evaluation.py</em>"],
        ["19", "Estado «100 % operativo»", "Todos los módulos", "14 pantallas construidas y 8 de 8 suites que pasan; sin pruebas con niños", "<em>pruebas.json</em>"],
        ["20", "Solucionador MILP", "CBC mediante PuLP", "Con PuLP 4.0.0 no hay solucionadores; con 2.9.0 sí. La prueba de equivalencia se omite sin CBC", "<em>listSolvers</em>; test_optimizer"],
    ]
    h.append(tabla("Datos verificados y correcciones respecto de los documentos previos",
                   ["N.º", "Tema", "Documento previo", "Valor verificado", "Evidencia"], filas,
                   "La prueba de equivalencia MILP y enumeración devolvió, con CBC disponible, el mismo objetivo (3,3798) y las mismas "
                   "cuatro actividades sobre 24 candidatas.", anchos=["5%", "17%", "22%", "36%", "20%"], clase="larga chica"))
    h.append(H1("Anexo B. Reproducibilidad"))
    h.append(P("Todos los insumos de este documento se regeneran con los <em>scripts</em> de la carpeta <em>_fuentes</em>:"))
    h.append(UL([
        "<em>verificar_doi.py</em>: metadatos de Crossref de los 15 DOI (resultado en <em>doi_verificados.json</em>);",
        "<em>bench_latencia.py</em>: latencia del descriptor y el clasificador (<em>bench_latencia.json</em>);",
        "<em>catalogo_datos.py</em>: diccionario de datos desde el esquema real;",
        "<em>auditoria_calidad.py</em>: pruebas de integridad sobre la base de datos;",
        "<em>ejecutar_pruebas.py</em>: las ocho suites del proyecto (<em>pruebas.json</em>);",
        "<em>modelo_financiero.py</em>: cifras, hoja de cálculo y gráfico de caja;",
        "<em>diagramas_bpmn.py</em>, <em>diagramas_dfd.py</em>, <em>diagramas_otros.py</em> y <em>logos.py</em>: figuras vectoriales;",
        "<em>construir_todo.py</em>: documento y póster en PDF."]))
    h.append(H1("Anexo C. Supuestos del modelo financiero"))
    p = FIN["parametros"]
    sup = [
        ["Horas de ingeniería y desarrollo", f"{p['horas_dev']} h", "Estimación del equipo; validar con la bitácora"],
        ["Tarifa de ingeniería", cop(p["tarifa_ing"]) + " / h", "Dentro del rango de la guía ($ 25.000 a $ 40.000)"],
        ["Precio de una cámara web", cop(p["precio_camara"]), "Validar con cotización"],
        ["Costo hora docente con cargas", cop(p["tarifa_docente"]) + " / h", "Validar con la nómina de la institución"],
        ["Horas docentes ahorradas por semana", f"{p['horas_ahorro_sem']} h", "Medir en un piloto"],
        ["Deserción anual sin y con el sistema", f"{pct(p['desercion_base'] * 100, 0)} y {pct(p['desercion_sistema'] * 100, 0)}", "Validar con registros de la institución y medir en un piloto"],
        ["Cuota mensual por niño", cop(p["cuota_mensual"]), "Validar con la institución"],
        ["Familias que contratan práctica en casa", pct(p["familias_pct"] * 100, 0), "Acotada por la tenencia de computador (DANE)"],
        ["Niños atendidos", f"{p['ninos']}", "Unidad de análisis"],
    ]
    h.append(tabla("Supuestos principales del modelo", ["Supuesto", "Valor", "Nota"], sup,
                   "La lista completa, con su tipo (supuesto, verificable o de la guía), está en la hoja <em>Supuestos</em> de "
                   "<em>04_Modelo_Financiero_ROI_Equipo_XX.xlsx</em>.", anchos=["38%", "22%", "40%"], clase="chica"))
    return "".join(h)
