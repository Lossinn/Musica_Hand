"""Ruta de Aprendizaje Musical — versión legible por máquina.

Fuente de verdad del CONTENIDO (qué notas y qué ritmos están desbloqueados y en
qué orden). El texto explicativo vive en `docs/01_ruta_aprendizaje_musical.md` y
**debe** mantenerse sincronizado con este módulo.

Lo consumen:
    game.py                -> qué actividad presentar
    adaptive/optimizer.py  -> dominio de decisión del MILP
    adaptive/environment.py-> avance de currículo (acción introducir_nueva_nota)
    adaptive/predictor.py  -> features (etapa, nota_idx)
    editor de canciones    -> paleta de notas/figuras por modo

Principio (§0 del doc): salvo la Etapa 1 (que establece la base), cada etapa
introduce **una sola** dificultad nueva fuerte: o una nota, o una figura
rítmica que subdivide el pulso. Nunca las dos a la vez.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config

# ─────────────────────────────────────────────────────────────────────────────
# 1. Correspondencia gesto → nota
# ─────────────────────────────────────────────────────────────────────────────
# Heredado de la versión anterior (MusicaManos):
#   · Cada NOTA es una SEÑA DE DOS MANOS que el niño calibra (no un nº de dedos).
#   · El reconocedor compara la pose en vivo contra las plantillas calibradas
#     por similitud coseno (umbral config.GESTURE_SIMILARITY_THRESHOLD) y
#     devuelve la nota de la plantilla más parecida.
#   · El "gesto" que sale del reconocedor YA es el nombre de la nota → identidad.
# Ver recognizer.GestureRecognizer y calibration.Calibrator.
GESTO_NOTA: dict[str, str] = {n: n for n in config.NOTAS}

# Cierre de octava: DO en registro agudo (8.ª seña, DO4).
DO_AGUDO = "DO4"
NOTAS_EXTENDIDAS: tuple[str, ...] = config.NOTAS          # ya incluye DO4

# Orden pedagógico de aparición de las notas (Kodály: sol-mi primero; fa y si
# —los semitonos— al final).
ORDEN_NOTAS: tuple[str, ...] = ("SOL3", "MI3", "LA3", "DO3", "RE3", "FA3", "SI3", DO_AGUDO)

# Color de apoyo por nota (PROVISIONAL — botonera de la imagen de referencia).
# El color es una ayuda que se retira gradualmente, no una propiedad permanente.
COLOR_NOTA: dict[str, str] = {
    "DO3": "#E24A4A",    # rojo / coral
    "RE3": "#F2913D",    # naranja
    "MI3": "#F2D13D",    # amarillo
    "FA3": "#5FBF6A",    # verde
    "SOL3": "#3DBFB0",   # turquesa
    "LA3": "#4A78E2",    # azul
    "SI3": "#8A5FE2",    # morado
    DO_AGUDO: "#F26DA8",  # rosa
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. Vocabulario rítmico
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Figura:
    """Figura rítmica con nombre infantil (sílaba tipo Kodály)."""

    nombre: str
    silaba: str
    pulsos: float          # duración en pulsos de negra
    simbolo: str           # etiqueta corta para la UI
    subdivide: bool        # ¿mete más de un evento por pulso? (dificultad fuerte)


NEGRA = Figura("negra", "ta", 1.0, "negra", False)
SILENCIO_NEGRA = Figura("silencio_negra", "sh", 1.0, "silencio", False)
DOS_CORCHEAS = Figura("dos_corcheas", "ti-ti", 1.0, "corcheas", True)
BLANCA = Figura("blanca", "ta-a", 2.0, "blanca", False)
REDONDA = Figura("redonda", "ta-a-a-a", 4.0, "redonda", False)
NEGRA_PUNTILLO_CORCHEA = Figura("negra_puntillo_corchea", "ta—i-ti", 2.0, "puntillo", True)
SEMICORCHEAS = Figura("cuatro_semicorcheas", "ti-ri-ti-ri", 1.0, "semicorcheas", True)

TODAS_LAS_FIGURAS: tuple[Figura, ...] = (
    NEGRA, SILENCIO_NEGRA, DOS_CORCHEAS, BLANCA, REDONDA,
    NEGRA_PUNTILLO_CORCHEA, SEMICORCHEAS,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Rangos de parámetros continuos que mueve la IA (doc §6 / Entregable 2 §11)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RangoDificultad:
    """Rango [min, max] de cada parámetro continuo dentro de una etapa.

    La IA (predictor + MILP + DQN) elige el valor puntual; el currículo solo
    acota. Los rangos se interpolan suavemente entre etapas (interpolar_rango).
    """

    bpm: tuple[int, int] = (60, 80)
    n_eventos: tuple[int, int] = (4, 6)
    densidad: tuple[float, float] = (1.0, 1.0)       # eventos por pulso
    p_lectura: tuple[float, float] = (0.0, 0.0)      # proporción lectura a 1.ª vista
    p_salto: tuple[float, float] = (0.0, 0.0)        # saltos vs. grados conjuntos
    tol_ms: tuple[int, int] = (180, 250)             # ventana de acierto de tiempo
    ayudas: tuple[int, int] = (3, 3)                 # nº de apoyos visuales (0 = ninguno)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Etapas
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Etapa:
    """Hito de contenido. NO es un nivel de dificultad fijo: acota qué está
    desbloqueado; la dificultad real la ajusta `adaptive/` de forma continua."""

    id: int
    nombre: str
    lema: str
    puntua: bool                         # Etapa 0 (calibración) no puntúa
    pilar: str                           # "base" | "notas" | "ritmo" | "consolida" | "infinito"
    notas_nuevas: tuple[str, ...]
    notas_activas: tuple[str, ...]       # acumulado (todas las disponibles aquí)
    figuras_nuevas: tuple[Figura, ...]
    figuras_activas: tuple[Figura, ...]  # acumulado
    compases: tuple[str, ...]
    dinamicas: tuple[str, ...]           # subconjunto de config.DINAMICAS
    objetivos_notas: tuple[str, ...]
    objetivos_ritmos: tuple[str, ...]
    progresion: str                     # cómo sube respecto a la etapa previa
    consolidacion: str                  # qué del nivel previo se afianza aquí
    apoyos_visuales: str
    repertorio: tuple[str, ...]
    rango: RangoDificultad = field(default_factory=RangoDificultad)


def _acumular(pares: list[tuple]) -> list[tuple]:
    """Para cada posición, devuelve la unión acumulada con las anteriores."""
    notas: list[str] = []
    figuras: list[Figura] = []
    out = []
    for notas_nuevas, figuras_nuevas in pares:
        for n in notas_nuevas:
            if n not in notas:
                notas.append(n)
        for f in figuras_nuevas:
            if f not in figuras:
                figuras.append(f)
        out.append((tuple(notas), tuple(figuras)))
    return out


# (notas_nuevas, figuras_nuevas) por etapa, en orden. La ruta ALTERNA
# nota / ritmo salvo la Etapa 1 (base) y las de consolidación.
_NUEVAS = [
    ((), ()),                                    # 0  calibración
    (("SOL3", "MI3"), (NEGRA,)),                 # 1  base: 2 notas + pulso
    (("LA3",), ()),                             # 2  nota
    ((), (SILENCIO_NEGRA,)),                     # 3  ritmo (no subdivide)
    (("DO3", "RE3"), ()),                        # 4  nota
    ((), (DOS_CORCHEAS,)),                       # 5  ritmo (subdivide)
    (("FA3", "SI3"), ()),                        # 6  nota: escala de 7 completa
    ((), (BLANCA, REDONDA)),                     # 7  ritmo (no subdivide)
    ((DO_AGUDO,), ()),                           # 8  nota: octava (DO4)
    ((), (NEGRA_PUNTILLO_CORCHEA,)),             # 9  ritmo (subdivide) + anacrusa
    ((), (SEMICORCHEAS,)),                       # 10 ritmo (subdivide) + 3/4
    ((), ()),                                    # 11 consolidación / repertorio
    ((), ()),                                    # 12 modo infinito
]
_ACUM = _acumular(_NUEVAS)


CURRICULUM: tuple[Etapa, ...] = (
    Etapa(
        id=0, nombre="Conoce tus manos", lema="Vamos a calibrar",
        puntua=False, pilar="base",
        notas_nuevas=(), notas_activas=(),
        figuras_nuevas=(), figuras_activas=(),
        compases=("4/4",), dinamicas=("tutorial",),
        objetivos_notas=("Imitar el gesto del personaje para cada nota que usará la Etapa 1 (mín. SOL y MI).",),
        objetivos_ritmos=("Sentir un pulso lento siguiéndolo con la mano. Sin evaluación.",),
        progresion="No aplica: se repite hasta que la calibración es estable.",
        consolidacion="—",
        apoyos_visuales="Máximos: el personaje demuestra, texto corto, color y sonido.",
        repertorio=(),
        rango=RangoDificultad(bpm=(50, 60), n_eventos=(2, 4), tol_ms=(400, 400), ayudas=(3, 3)),
    ),
    Etapa(
        id=1, nombre="Dos sonidos", lema="SOL y MI",
        puntua=True, pilar="base",
        notas_nuevas=("SOL3", "MI3"), notas_activas=_ACUM[1][0],
        figuras_nuevas=(NEGRA,), figuras_activas=_ACUM[1][1],
        compases=("4/4",), dinamicas=("tutorial", "reaccion"),
        objetivos_notas=(
            "Reconocer y producir SOL y MI (tercera menor, 'el canto del cucú').",
            "Distinguir agudo (SOL) de grave (MI). Sin pentagrama: burbujas de color.",
        ),
        objetivos_ritmos=(
            "Pulso constante.",
            "Negra (ta) = 1 pulso. Imitar patrones de 4 negras.",
            "Compás 4/4 como 'una caja de 4'.",
        ),
        progresion="Desde 2 gestos a ~60 BPM hasta secuencias de 4-6 notas a ~80 BPM; ventana ±250→±180 ms.",
        consolidacion="Los gestos calibrados en la Etapa 0.",
        apoyos_visuales="Color + nombre hablado + personaje que modela cada nota.",
        repertorio=("Motivos de 2 notas ('cu-cú')", "Llamada-respuesta con el personaje"),
        rango=RangoDificultad(bpm=(60, 80), n_eventos=(4, 6), tol_ms=(180, 250), ayudas=(3, 3)),
    ),
    Etapa(
        id=2, nombre="Tres sonidos", lema="Llega LA y el pentagrama",
        puntua=True, pilar="notas",
        notas_nuevas=("LA3",), notas_activas=_ACUM[2][0],
        figuras_nuevas=(), figuras_activas=_ACUM[2][1],
        compases=("4/4",), dinamicas=("tutorial", "reaccion", "libre"),
        objetivos_notas=(
            "Añadir LA. Melodías SOL-MI-LA.",
            "Introducir el pentagrama: líneas y espacios; SOL en la 2.ª línea como ancla.",
        ),
        objetivos_ritmos=(
            "Sin figura nueva: se afianza la negra y el pulso mientras la atención va a la nota nueva.",
        ),
        progresion="+1 nota; primera lectura en pentagrama (con color detrás, luego sin él); 5-8 eventos.",
        consolidacion="SOL y MI ahora se leen en pentagrama, no solo por color; pulso estable de la Etapa 1.",
        apoyos_visuales="Color desvaneciéndose (~50 % del tiempo); nombre de nota bajo demanda.",
        repertorio=("Canciones de 3 notas de ámbito corto", "Ostinatos"),
        rango=RangoDificultad(bpm=(66, 88), n_eventos=(5, 8), p_lectura=(0.2, 0.5),
                              tol_ms=(160, 220), ayudas=(2, 3)),
    ),
    Etapa(
        id=3, nombre="El silencio también suena", lema="Silencio de negra: sh",
        puntua=True, pilar="ritmo",
        notas_nuevas=(), notas_activas=_ACUM[3][0],
        figuras_nuevas=(SILENCIO_NEGRA,), figuras_activas=_ACUM[3][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=("Consolidar SOL-MI-LA; frases de hasta 8 notas; primeros saltos MI↔LA (4.ª).",),
        objetivos_ritmos=(
            "Silencio de negra (sh) = 1 pulso de mano quieta.",
            "Patrones de 4 tiempos con exactamente 1 silencio. Reforzar 4/4.",
        ),
        progresion="Primera figura de reposo: hay que 'no hacer' en el momento justo.",
        consolidacion="Lectura en pentagrama de SOL-MI-LA; pulso.",
        apoyos_visuales="Metrónomo visual (el personaje balancea); color solo bajo demanda.",
        repertorio=("Ostinatos con silencio", "Preguntas y respuestas rítmicas"),
        rango=RangoDificultad(bpm=(70, 92), n_eventos=(6, 10), p_lectura=(0.4, 0.7),
                              p_salto=(0.0, 0.2), tol_ms=(150, 200), ayudas=(1, 2)),
    ),
    Etapa(
        id=4, nombre="La escalera baja", lema="DO y RE graves",
        puntua=True, pilar="notas",
        notas_nuevas=("DO3", "RE3"), notas_activas=_ACUM[4][0],
        figuras_nuevas=(), figuras_activas=_ACUM[4][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=(
            "Añadir DO y RE (registro grave). Pentacordo DO-RE-MI-FA-SOL (aún sin FA).",
            "DO en 1.ª línea adicional inferior ('nota con sombrero').",
            "Grados conjuntos ascendentes y descendentes DO→SOL.",
        ),
        objetivos_ritmos=("Sin figura nueva: negra y silencio se combinan libremente.",),
        progresion="+2 notas; ámbito de 5 notas; el tricordio pasa a ser el centro de un rango mayor.",
        consolidacion="Silencio de negra; lectura líneas/espacios.",
        apoyos_visuales="Color solo bajo demanda; nombres ocultos por defecto.",
        repertorio=("Arroz con leche (fragmento)", "Melodías de pentacordo"),
        rango=RangoDificultad(bpm=(76, 100), n_eventos=(6, 12), p_lectura=(0.6, 0.85),
                              p_salto=(0.05, 0.25), tol_ms=(140, 190), ayudas=(0, 2)),
    ),
    Etapa(
        id=5, nombre="El eco del ritmo", lema="Corcheas: ti-ti",
        puntua=True, pilar="ritmo",
        notas_nuevas=(), notas_activas=_ACUM[5][0],
        figuras_nuevas=(DOS_CORCHEAS,), figuras_activas=_ACUM[5][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=("Consolidar el pentacordo DO-RE-MI-FA-SOL con frases de 8-10 notas.",),
        objetivos_ritmos=(
            "Dos corcheas (ti-ti) = 1 pulso: dos gestos en un tiempo.",
            "Combinar ta, sh y ti-ti en patrones de 4 tiempos.",
            "Dinámica 'rítmico': eco (el personaje toca, el niño repite).",
        ),
        progresion="Primera subdivisión del pulso; densidad rítmica variable; tempo hasta ~104 BPM.",
        consolidacion="Pentacordo DO→SOL; silencio de negra.",
        apoyos_visuales="Color solo en notas nuevas del patrón; metrónomo visual.",
        repertorio=("Rimas y juegos de palmas transcritos a gesto",),
        rango=RangoDificultad(bpm=(84, 104), n_eventos=(8, 14), densidad=(1.0, 2.0),
                              p_lectura=(0.6, 0.9), p_salto=(0.1, 0.3), tol_ms=(120, 170), ayudas=(0, 1)),
    ),
    Etapa(
        id=6, nombre="La escala completa", lema="Llegan FA y SI",
        puntua=True, pilar="notas",
        notas_nuevas=("FA3", "SI3"), notas_activas=_ACUM[6][0],
        figuras_nuevas=(), figuras_activas=_ACUM[6][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=(
            "Añadir FA y SI (los semitonos) → escala diatónica completa "
            "DO-RE-MI-FA-SOL-LA-SI, ascendente y descendente.",
            "Noción de grado de la escala (1.º = DO, 'reposo'). Todos los gestos calibrados en uso.",
        ),
        objetivos_ritmos=("Sin figura nueva: ta / sh / ti-ti se combinan sobre la escala completa.",),
        progresion="Rango completo de 7; los semitonos MI-FA y SI-DO exigen precisión de gesto fina.",
        consolidacion="Corcheas; pentacordo; lectura fluida.",
        apoyos_visuales="Mínimos: ayuda solo tras un error.",
        repertorio=("Escalas cantadas", "Estrellita (Twinkle) — primera frase"),
        rango=RangoDificultad(bpm=(88, 112), n_eventos=(8, 16), densidad=(1.0, 2.0),
                              p_lectura=(0.8, 1.0), p_salto=(0.15, 0.35), tol_ms=(110, 160), ayudas=(0, 1)),
    ),
    Etapa(
        id=7, nombre="Notas que duran", lema="Blanca y redonda",
        puntua=True, pilar="ritmo",
        notas_nuevas=(), notas_activas=_ACUM[7][0],
        figuras_nuevas=(BLANCA, REDONDA), figuras_activas=_ACUM[7][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=("Consolidar la escala de 7 con frases de 10-14 notas y cadencia en DO.",),
        objetivos_ritmos=(
            "Blanca (ta-a) = 2 pulsos; redonda solo para cerrar frase.",
            "Mezclar negra, corchea, silencio y blanca. Sostener la atención sin repetir el gesto.",
        ),
        progresion="Duraciones largas: el reto es esperar sin volver a tocar.",
        consolidacion="Escala de 7; corcheas.",
        apoyos_visuales="Ninguno por defecto.",
        repertorio=("Arroz con leche (completa)", "Melodías con finales largos"),
        rango=RangoDificultad(bpm=(84, 116), n_eventos=(10, 18), densidad=(1.0, 2.0),
                              p_lectura=(0.9, 1.0), p_salto=(0.15, 0.4), tol_ms=(105, 150), ayudas=(0, 0)),
    ),
    Etapa(
        id=8, nombre="La octava", lema="DO agudo: el mismo nombre, más alto",
        puntua=True, pilar="notas",
        notas_nuevas=(DO_AGUDO,), notas_activas=_ACUM[8][0],
        figuras_nuevas=(), figuras_activas=_ACUM[8][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=(
            "DO agudo (8.ª tecla). Concepto de octava.",
            "Saltos melódicos de 3.ª, 5.ª y 8.ª además de grados conjuntos.",
        ),
        objetivos_ritmos=("Sin figura nueva: todo el vocabulario rítmico hasta aquí.",),
        progresion="Ámbito de octava (8 sonidos); los saltos exigen mayor precisión de gesto.",
        consolidacion="Escala de 7; blanca y redonda.",
        apoyos_visuales="Ninguno; una 'pista' cuesta una estrella.",
        repertorio=("Estrellita (completa)", "Melodías con salto de octava"),
        rango=RangoDificultad(bpm=(88, 120), n_eventos=(10, 20), densidad=(1.0, 2.2),
                              p_lectura=(0.95, 1.0), p_salto=(0.2, 0.45), tol_ms=(100, 140), ayudas=(0, 0)),
    ),
    Etapa(
        id=9, nombre="Ritmos con puntillo", lema="ta—i-ti y arrancar antes del 1",
        puntua=True, pilar="ritmo",
        notas_nuevas=(), notas_activas=_ACUM[9][0],
        figuras_nuevas=(NEGRA_PUNTILLO_CORCHEA,), figuras_activas=_ACUM[9][1],
        compases=("4/4",), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=("Consolidar la octava con frases de 12-18 notas.",),
        objetivos_ritmos=(
            "Negra con puntillo + corchea (ta—i-ti): ritmo 'cojo'.",
            "Anacrusa: empezar antes del primer tiempo.",
        ),
        progresion="Ritmos irregulares y arranques a contratiempo.",
        consolidacion="Octava completa; subdivisión en corcheas.",
        apoyos_visuales="Ninguno.",
        repertorio=("Cumpleaños feliz (con anacrusa)", "Melodías con puntillo"),
        rango=RangoDificultad(bpm=(90, 124), n_eventos=(12, 22), densidad=(1.2, 2.3),
                              p_lectura=(1.0, 1.0), p_salto=(0.2, 0.45), tol_ms=(95, 130), ayudas=(0, 0)),
    ),
    Etapa(
        id=10, nombre="Vals y carreras", lema="3/4 y semicorcheas",
        puntua=True, pilar="ritmo",
        notas_nuevas=(), notas_activas=_ACUM[10][0],
        figuras_nuevas=(SEMICORCHEAS,), figuras_activas=_ACUM[10][1],
        compases=("4/4", "3/4"), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=("Consolidar la octava en dos compases distintos.",),
        objetivos_ritmos=(
            "Cuatro semicorcheas (ti-ri-ti-ri) en contextos simples.",
            "Compás de 3/4 (vals) junto al 4/4; cambiar de compás en una sesión.",
        ),
        progresion="Subdivisión más fina y un compás ternario nuevo.",
        consolidacion="Puntillo; anacrusa; octava.",
        apoyos_visuales="Ninguno.",
        repertorio=("Valses cortos", "Cumpleaños feliz (completa)"),
        rango=RangoDificultad(bpm=(96, 132), n_eventos=(14, 24), densidad=(1.5, 2.5),
                              p_lectura=(1.0, 1.0), p_salto=(0.2, 0.5), tol_ms=(95, 125), ayudas=(0, 0)),
    ),
    Etapa(
        id=11, nombre="Canciones completas", lema="Toca de principio a fin",
        puntua=True, pilar="consolida",
        notas_nuevas=(), notas_activas=_ACUM[11][0],
        figuras_nuevas=(), figuras_activas=_ACUM[11][1],
        compases=("4/4", "3/4"), dinamicas=("ritmico", "reaccion", "libre"),
        objetivos_notas=(
            "Piezas reales que usan toda la octava: Estrellita, Arroz con leche, Cumpleaños feliz.",
            "Frase musical y cadencia (reposo en DO). Memorizar una canción entera.",
        ),
        objetivos_ritmos=(
            "Combinación libre de todo lo anterior.",
            "Tempo variable (lento / andante / rápido) según la pieza.",
            "Mantener el tempo durante 16-24 notas sin arrastrarse ni acelerar.",
        ),
        progresion="Longitud (piezas completas), memoria y estabilidad de tempo sobre toda la pieza.",
        consolidacion="Todo lo anterior.",
        apoyos_visuales="Ninguno; modo 'concierto'.",
        repertorio=("Estrellita", "Arroz con leche", "Cumpleaños feliz", "Banco ampliable en assets/music/"),
        rango=RangoDificultad(bpm=(80, 132), n_eventos=(16, 24), densidad=(1.0, 2.5),
                              p_lectura=(1.0, 1.0), p_salto=(0.2, 0.5), tol_ms=(90, 120), ayudas=(0, 0)),
    ),
    Etapa(
        id=12, nombre="Modo Infinito", lema="Crea tus canciones",
        puntua=True, pilar="infinito",
        notas_nuevas=(), notas_activas=_ACUM[12][0],
        figuras_nuevas=(), figuras_activas=_ACUM[12][1],
        compases=("4/4", "3/4"), dinamicas=config.DINAMICAS,
        objetivos_notas=("No entra contenido nuevo. La IA combina solo lo que el niño domina.",),
        objetivos_ritmos=(
            "No entra contenido nuevo. La IA mueve tempo, densidad, longitud, saltos, "
            "proporción de lectura, tolerancia, apoyos y compás de forma continua.",
        ),
        progresion="Definida por adaptive/ (predictor + MILP + DQN). Sin final: reto en la zona de desarrollo próximo.",
        consolidacion="El modo infinito es consolidación permanente.",
        apoyos_visuales="Los que decida la IA (rango 0-3).",
        repertorio=("Editor: modo Nivel X (paleta restringida) y modo Libre (paleta completa, grabar y guardar)",),
        rango=RangoDificultad(bpm=(60, 132), n_eventos=(4, 32), densidad=(1.0, 2.5),
                              p_lectura=(0.0, 1.0), p_salto=(0.0, 0.5), tol_ms=(90, 250), ayudas=(0, 3)),
    ),
)

N_ETAPAS = len(CURRICULUM)           # ajustable: editar CURRICULUM y este valor sigue

# ─────────────────────────────────────────────────────────────────────────────
# 5. Reglas de avance entre etapas (doc §4). Parámetros, no números mágicos.
# ─────────────────────────────────────────────────────────────────────────────
VENTANA_AVANCE = 12                  # nº de actividades recientes a evaluar
UMBRALES_AVANCE = {
    "precision_min": 0.85,           # P_t
    "error_max": 0.15,               # E_t
    "timing_ok_min": 0.80,           # aciertos de tiempo dentro de ventana
    "tendencias_ok": ("estable", "mejorando"),
}

# Repertorio de la imagen de referencia (tarjetas "Canciones").
CANCIONES_BASE = ("Estrellita", "Arroz con leche", "Cumpleaños feliz")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Helpers de consulta
# ─────────────────────────────────────────────────────────────────────────────
def etapa(n: int) -> Etapa:
    """Devuelve la Etapa de id `n` (0..N_ETAPAS-1). Satura en los extremos."""
    n = max(0, min(n, N_ETAPAS - 1))
    return CURRICULUM[n]


def notas_disponibles(etapa_id: int) -> tuple[str, ...]:
    """Notas que la etapa permite usar (acumulado hasta esa etapa)."""
    return etapa(etapa_id).notas_activas


def figuras_disponibles(etapa_id: int) -> tuple[Figura, ...]:
    """Figuras rítmicas que la etapa permite usar (acumulado)."""
    return etapa(etapa_id).figuras_activas


def paleta_editor(etapa_id: int, modo: str = "nivel") -> dict:
    """Paleta para el editor de canciones.

    modo == "nivel": solo lo desbloqueado hasta `etapa_id`.
    modo == "libre": todo el vocabulario.
    """
    if modo == "libre":
        return {"notas": NOTAS_EXTENDIDAS, "figuras": TODAS_LAS_FIGURAS,
                "compases": ("4/4", "3/4")}
    e = etapa(etapa_id)
    return {"notas": e.notas_activas, "figuras": e.figuras_activas, "compases": e.compases}


def puede_avanzar(metricas: dict) -> bool:
    """Aplica UMBRALES_AVANCE a un dict con claves precision, error_rate,
    timing_ok_rate y tendencia (calculadas sobre las últimas VENTANA_AVANCE
    actividades). Devuelve True si la etapa siguiente debe desbloquearse."""
    u = UMBRALES_AVANCE
    return (
        metricas.get("precision", 0.0) >= u["precision_min"]
        and metricas.get("error_rate", 1.0) <= u["error_max"]
        and metricas.get("timing_ok_rate", 0.0) >= u["timing_ok_min"]
        and metricas.get("tendencia", "empeorando") in u["tendencias_ok"]
    )


def interpolar_rango(etapa_id: int, progreso: float) -> RangoDificultad:
    """Interpola los rangos entre la etapa actual y la siguiente según
    `progreso` in [0, 1] dentro de la etapa. Transición suave de dificultad
    sin saltos al cambiar de etapa (doc §0.3)."""
    a = etapa(etapa_id).rango
    b = etapa(etapa_id + 1).rango
    p = max(0.0, min(progreso, 1.0))

    def lerp_par(pa, pb):
        lo = pa[0] + (pb[0] - pa[0]) * p
        hi = pa[1] + (pb[1] - pa[1]) * p
        return (type(pa[0])(lo), type(pa[1])(hi))

    return RangoDificultad(
        bpm=lerp_par(a.bpm, b.bpm),
        n_eventos=lerp_par(a.n_eventos, b.n_eventos),
        densidad=lerp_par(a.densidad, b.densidad),
        p_lectura=lerp_par(a.p_lectura, b.p_lectura),
        p_salto=lerp_par(a.p_salto, b.p_salto),
        tol_ms=lerp_par(a.tol_ms, b.tol_ms),
        ayudas=lerp_par(a.ayudas, b.ayudas),
    )
