"""Contenido inicial: habilidades, mapa de niveles, banco de actividades y logros.

El banco se genera de forma declarativa para que agregar un nivel nuevo sea
cuestión de añadir una entrada, no de escribir pantallas.
"""

from __future__ import annotations

from ..domain.entities import Achievement, Activity, ActivityKind, PlayMode, Skill
from ..domain.notes import NOTE_CODES, solfa
from .database import Database, get_db
from .repositories import AchievementRepository, ActivityRepository, SkillRepository

SEED_VERSION = "7"

# --------------------------------------------------------------- niveles

LEVELS: list[dict] = [
    {"level": 1, "title": "Las Primeras Manitas",
     "subtitle": "Do, Re y Mi", "icon": "🌱", "color": "mint"},
    {"level": 2, "title": "La Granja de las Palmas",
     "subtitle": "Llegan Fa y Sol", "icon": "🐣", "color": "tangerine"},
    {"level": 3, "title": "El Camino de las Notas",
     "subtitle": "Secuencias", "icon": "🛤️", "color": "sky"},
    {"level": 4, "title": "El Bosque que Recuerda",
     "subtitle": "Memoria musical", "icon": "🌳", "color": "violet"},
    {"level": 5, "title": "El Río del Ritmo",
     "subtitle": "Tiempo y pulso", "icon": "🌊", "color": "bubblegum"},
    {"level": 6, "title": "El Cielo de las Melodías",
     "subtitle": "La, Si y Do agudo", "icon": "☁️", "color": "sun"},
    {"level": 7, "title": "El Gran Concierto",
     "subtitle": "Retos y canciones", "icon": "🎪", "color": "bubblegum"},
]

LEVEL_TITLES = {d["level"]: d["title"] for d in LEVELS}


# ------------------------------------------------------------ habilidades

def build_skills() -> list[Skill]:
    skills: list[Skill] = []
    note_levels = {"DO3": 1, "RE3": 1, "MI3": 1, "FA3": 2, "SOL3": 2,
                   "LA3": 6, "SI3": 6, "DO4": 6}
    prev: str | None = None
    for i, code in enumerate(NOTE_CODES):
        skills.append(Skill(
            code=f"nota_{code}",
            name=f"Seña de {solfa(code)}",
            note_code=code,
            level=note_levels[code],
            difficulty=round(0.10 + 0.07 * i, 3),
            prerequisites=[f"nota_{prev}"] if prev else [],
            order_index=i,
            description=f"Reconocer y ejecutar la seña de {solfa(code)}.",
        ))
        prev = code

    compuestas = [
        ("secuencia_2", "Dos notas seguidas", 3, 0.42,
         ["nota_DO3", "nota_RE3", "nota_MI3"],
         "Encadenar dos señas sin perder el hilo."),
        ("secuencia_3", "Tres notas seguidas", 3, 0.52, ["secuencia_2"],
         "Mantener una secuencia corta de principio a fin."),
        ("memoria_corta", "Recordar la secuencia", 4, 0.60, ["secuencia_3"],
         "Reproducir una secuencia después de que desaparece."),
        ("ritmo_basico", "Seguir el pulso", 5, 0.64, ["secuencia_3"],
         "Ejecutar las señas a tiempo con el pulso."),
        ("melodia_simple", "Tocar una melodía", 6, 0.74,
         ["memoria_corta", "ritmo_basico"],
         "Interpretar una melodía completa."),
        ("reto_libre", "Tocar sin ayuda", 7, 0.86, ["melodia_simple"],
         "Ejecutar sin ver la seña de referencia."),
    ]
    for j, (code, name, lvl, diff, prereq, desc) in enumerate(compuestas):
        skills.append(Skill(code=code, name=name, note_code=None, level=lvl,
                            difficulty=diff, prerequisites=prereq,
                            order_index=100 + j, description=desc))
    return skills


# ------------------------------------------------------------ actividades

def _note_skills(seq: list[str]) -> list[str]:
    return sorted({f"nota_{c}" for c in seq})


def estimate_difficulty(seq: list[str], mode: PlayMode, hints: bool,
                        tempo: int) -> float:
    """Dificultad estimada de una actividad.

    Combina longitud, variedad de notas, amplitud del salto interválico, modo de
    juego, ayuda visual y tempo; se recorta al intervalo [0, 1]. Pública porque
    también la usa `learning.generator` para las actividades que arma sobre la
    marcha, y así ambas fuentes de contenido se miden con la misma regla.
    """
    from ..domain.notes import sequence_span
    n = len(seq)
    variety = len(set(seq))
    span = sequence_span(seq)
    mode_w = {PlayMode.GUIDED: 0.0, PlayMode.MEMORY: 0.18, PlayMode.SPEED: 0.14,
              PlayMode.MELODY: 0.10, PlayMode.CHALLENGE: 0.22, PlayMode.FREE: 0.0}
    d = (0.030 * n + 0.045 * variety + 0.030 * span
         + mode_w[mode] + (0.0 if hints else 0.12)
         + max(0.0, (tempo - 70) / 240.0))
    return round(min(1.0, max(0.05, d)), 3)


# Alias retrocompatible: el resto de este módulo seguía llamando a _difficulty.
_difficulty = estimate_difficulty


def _activity(code: str, kind: ActivityKind, title: str, level: int,
              seq: list[str], *, mode: PlayMode = PlayMode.GUIDED,
              skills: list[str] | None = None, tempo: int = 70,
              hints: bool = True, reps: int = 1, icon: str = "🎵",
              desc: str = "", tolerance_ms: int = 2500) -> Activity:
    sk = list(skills) if skills else _note_skills(seq)
    return Activity(
        code=code, kind=kind, title=title, level=level,
        difficulty=_difficulty(seq, mode, hints, tempo),
        skill_codes=sk, sequence=seq, mode=mode, tempo_bpm=tempo,
        duration_s=max(25, int(len(seq) * reps * (60.0 / tempo) * 2.2) + 12),
        hints=hints, repetitions=reps, description=desc, icon=icon,
        tolerance_ms=tolerance_ms)


# Melodías: dos piezas de dominio público y cuatro composiciones propias
# pensadas para la tesitura de ocho notas de la aplicación.
SONGS: list[tuple[str, str, list[str], int, str]] = [
    ("cancion_estrellita", "Estrellita, ¿dónde estás?",
     ["DO3", "DO3", "SOL3", "SOL3", "LA3", "LA3", "SOL3",
      "FA3", "FA3", "MI3", "MI3", "RE3", "RE3", "DO3"], 66, "⭐"),
    ("cancion_corderito", "Mi corderito",
     ["MI3", "RE3", "DO3", "RE3", "MI3", "MI3", "MI3",
      "RE3", "RE3", "RE3", "MI3", "SOL3", "SOL3"], 72, "🐑"),
    ("cancion_iguana", "Kiki, la Iguana",
     ["SOL3", "MI3", "SOL3", "MI3", "FA3", "RE3", "MI3", "DO3"], 78, "🦎"),
    ("cancion_rio", "El Río del Sinú",
     ["DO3", "MI3", "SOL3", "MI3", "FA3", "LA3", "SOL3", "MI3", "DO3"], 70, "🌊"),
    ("cancion_campanas", "Las Campanas del Bosque",
     ["SOL3", "SOL3", "LA3", "SI3", "DO4", "SI3", "LA3", "SOL3"], 74, "🔔"),
    ("cancion_concierto", "El Gran Concierto",
     ["DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4",
      "SI3", "LA3", "SOL3", "FA3", "MI3", "RE3", "DO3"], 80, "🎪"),
    # ---- Repertorio ampliado del módulo "Canciones" ----------------------
    # Trece melodías infantiles y tradicionales, simplificadas a las ocho
    # notas que reconoce la aplicación (una escala mayor natural: no hay
    # semitonos alterados). Son composiciones populares de dominio público o
    # folclore; aquí solo se codifica la línea melódica en do-re-mi, nunca la
    # letra. "Martinillo" es la versión en español de la ronda tradicional
    # francesa "Frère Jacques": el descenso final "din don dan" se adaptó a
    # Do4-Sol3-Do3 (un Do más un Sol más bajo, no disponibles en este rango,
    # se reemplazan por la octava completa disponible) para conservar el
    # efecto de campana sin salirse de las ocho notas de la aplicación.
    ("cancion_pollitos", "Los Pollitos",
     ["MI3", "MI3", "MI3", "DO3", "RE3", "MI3", "FA3", "FA3",
      "FA3", "RE3", "MI3", "FA3", "SOL3", "MI3", "DO3"], 70, "🐥"),
    ("cancion_cucu", "Cucú Cantaba la Rana",
     ["SOL3", "MI3", "SOL3", "MI3", "SOL3", "MI3", "FA3", "RE3",
      "SOL3", "MI3", "SOL3", "MI3", "DO3"], 76, "🐸"),
    ("cancion_aserrin", "Aserrín Aserrán",
     ["MI3", "MI3", "RE3", "DO3", "MI3", "MI3", "RE3", "DO3",
      "SOL3", "FA3", "MI3", "RE3", "DO3"], 68, "🪵"),
    ("cancion_pinpon", "Pin Pón",
     ["DO3", "MI3", "SOL3", "SOL3", "FA3", "MI3", "RE3", "DO3",
      "MI3", "SOL3", "DO4", "SOL3", "MI3", "DO3"], 74, "🪆"),
    ("cancion_arroz", "Arroz con Leche",
     ["DO4", "SI3", "LA3", "SOL3", "SOL3", "LA3", "SOL3", "FA3",
      "MI3", "RE3", "DO3", "RE3", "MI3", "FA3", "SOL3"], 76, "🍚"),
    ("cancion_anton", "Antón Pirulero",
     ["SOL3", "SOL3", "MI3", "SOL3", "LA3", "SOL3", "FA3", "MI3",
      "RE3", "DO3", "RE3", "MI3", "FA3", "SOL3"], 78, "🎩"),
    ("cancion_cumpleanos", "Cumpleaños Feliz",
     ["DO3", "DO3", "RE3", "DO3", "FA3", "MI3",
      "DO3", "DO3", "RE3", "DO3", "SOL3", "FA3"], 104, "🎂"),
    ("cancion_vaca", "Tengo una Vaca Lechera",
     ["DO4", "DO4", "SI3", "LA3", "SOL3", "LA3", "SI3", "DO4",
      "SOL3", "LA3", "SI3", "DO4", "SI3", "LA3", "SOL3", "MI3"], 84, "🐄"),
    ("cancion_mambru", "Mambrú se Fue a la Guerra",
     ["MI3", "MI3", "MI3", "DO3", "RE3", "MI3", "FA3", "MI3",
      "RE3", "DO3", "RE3", "MI3", "SOL3", "MI3", "RE3", "DO3"], 72, "⚔️"),
    ("cancion_cucaracha", "La Cucaracha",
     ["DO3", "MI3", "SOL3", "DO4", "SOL3", "MI3", "DO3", "RE3",
      "MI3", "FA3", "SOL3", "FA3", "MI3", "RE3", "DO3"], 88, "🪳"),
    ("cancion_nochedepaz", "Noche de Paz",
     ["SOL3", "LA3", "SOL3", "MI3", "SOL3", "LA3", "SOL3", "MI3",
      "SI3", "DO4", "SI3", "LA3", "SOL3", "LA3", "SI3", "DO4"], 60, "✨"),
    ("cancion_alegria", "Himno de la Alegría",
     ["MI3", "MI3", "FA3", "SOL3", "SOL3", "FA3", "MI3", "RE3",
      "DO3", "DO3", "RE3", "MI3", "MI3", "RE3", "RE3"], 92, "🎼"),
    ("cancion_martinillo", "Martinillo",
     ["DO3", "RE3", "MI3", "DO3", "DO3", "RE3", "MI3", "DO3",
      "MI3", "FA3", "SOL3", "MI3", "FA3", "SOL3",
      "SOL3", "LA3", "SOL3", "FA3", "MI3", "DO3",
      "SOL3", "LA3", "SOL3", "FA3", "MI3", "DO3",
      "DO4", "SOL3", "DO3", "DO4", "SOL3", "DO3"], 88, "🛎️"),
]


def build_activities() -> list[Activity]:
    A: list[Activity] = []
    E, G, S, V, R = (ActivityKind.EXERCISE, ActivityKind.GAME, ActivityKind.SONG,
                     ActivityKind.ASSESSMENT, ActivityKind.REVIEW)

    # ---- Nivel 1: familiarización con Do, Re y Mi -----------------------
    for code in ("DO3", "RE3", "MI3"):
        s = solfa(code)
        A.append(_activity(f"n1_{code}_intro", E, f"Conoce a {s}", 1,
                           [code] * 4, tempo=60, icon="👋",
                           desc=f"Repite la seña de {s} cuatro veces."))
    A.append(_activity("n1_do_re", E, "Do y Re bailan", 1,
                       ["DO3", "RE3", "DO3", "RE3"], tempo=64, icon="💃"))
    A.append(_activity("n1_do_mi", E, "Do y Mi saltan", 1,
                       ["DO3", "MI3", "DO3", "MI3"], tempo=64, icon="🦘"))
    A.append(_activity("n1_trio", E, "Las tres amigas", 1,
                       ["DO3", "RE3", "MI3", "RE3"], tempo=66, icon="🌈"))
    A.append(_activity("n1_juego_burbujas", G, "Burbujas Musicales", 1,
                       ["DO3", "MI3", "RE3", "MI3", "DO3"], tempo=70, icon="🫧",
                       desc="Revienta la burbuja haciendo la seña correcta."))
    A.append(_activity("n1_eval", V, "¿Ya las conoces?", 1,
                       ["MI3", "DO3", "RE3", "MI3", "RE3", "DO3"],
                       mode=PlayMode.CHALLENGE, hints=False, tempo=68, icon="🎯"))

    # ---- Nivel 2: llegan Fa y Sol ---------------------------------------
    for code in ("FA3", "SOL3"):
        s = solfa(code)
        A.append(_activity(f"n2_{code}_intro", E, f"Conoce a {s}", 2,
                           [code] * 4, tempo=62, icon="👋"))
    A.append(_activity("n2_mi_fa", E, "Mi y Fa se saludan", 2,
                       ["MI3", "FA3", "MI3", "FA3"], tempo=66, icon="🤝"))
    A.append(_activity("n2_fa_sol", E, "Fa y Sol se columpian", 2,
                       ["FA3", "SOL3", "FA3", "SOL3"], tempo=66, icon="🎠"))
    A.append(_activity("n2_cinco", E, "Las cinco primeras", 2,
                       ["DO3", "RE3", "MI3", "FA3", "SOL3"], tempo=70, icon="🖐️"))
    A.append(_activity("n2_juego_granja", G, "La Granja de las Palmas", 2,
                       ["SOL3", "MI3", "FA3", "RE3", "DO3"], tempo=72, icon="🐔"))
    A.append(_activity("n2_eval", V, "Reto de la granja", 2,
                       ["SOL3", "DO3", "FA3", "MI3", "RE3", "SOL3"],
                       mode=PlayMode.CHALLENGE, hints=False, tempo=72, icon="🎯"))

    # ---- Nivel 3: secuencias --------------------------------------------
    seqs3 = [("n3_sube", "Subiendo la escalera", ["DO3", "RE3", "MI3"], "🪜"),
             ("n3_baja", "Bajando la escalera", ["MI3", "RE3", "DO3"], "🛝"),
             ("n3_ida_vuelta", "Ida y vuelta", ["DO3", "MI3", "SOL3", "MI3", "DO3"], "🔁"),
             ("n3_zigzag", "Zigzag musical", ["DO3", "MI3", "RE3", "FA3", "MI3"], "⚡")]
    for code, title, seq, icon in seqs3:
        A.append(_activity(code, E, title, 3, seq, tempo=72, icon=icon,
                           skills=_note_skills(seq) + ["secuencia_2", "secuencia_3"]))
    A.append(_activity("n3_juego_camino", G, "El Camino de Piedritas", 3,
                       ["DO3", "RE3", "MI3", "FA3", "SOL3", "FA3", "MI3"],
                       tempo=76, icon="🪨",
                       skills=_note_skills(["DO3", "SOL3"]) + ["secuencia_3"]))
    A.append(_activity("n3_eval", V, "Camino sin pistas", 3,
                       ["DO3", "MI3", "SOL3", "FA3", "RE3", "DO3"],
                       mode=PlayMode.CHALLENGE, hints=False, tempo=74, icon="🎯",
                       skills=["secuencia_3"]))

    # ---- Nivel 4: memoria -----------------------------------------------
    mem = [("n4_mem2", "Recuerda dos", ["DO3", "SOL3"], "🧠"),
           ("n4_mem3", "Recuerda tres", ["MI3", "DO3", "SOL3"], "🧠"),
           ("n4_mem4", "Recuerda cuatro", ["RE3", "FA3", "DO3", "MI3"], "🧠"),
           ("n4_mem5", "Recuerda cinco", ["SOL3", "MI3", "DO3", "FA3", "RE3"], "🧠")]
    for code, title, seq, icon in mem:
        A.append(_activity(code, E, title, 4, seq, mode=PlayMode.MEMORY,
                           tempo=70, icon=icon,
                           skills=_note_skills(seq) + ["memoria_corta"]))
    A.append(_activity("n4_juego_bosque", G, "El Bosque que Recuerda", 4,
                       ["MI3", "SOL3", "RE3", "DO3", "FA3", "MI3"],
                       mode=PlayMode.MEMORY, tempo=74, icon="🌳",
                       skills=["memoria_corta"]))

    # ---- Nivel 5: ritmo --------------------------------------------------
    rit = [("n5_pulso_lento", "Pulso tranquilo", ["DO3", "MI3", "SOL3", "MI3"], 60, "🐢"),
           ("n5_pulso_medio", "Pulso alegre", ["DO3", "MI3", "SOL3", "MI3"], 84, "🐇"),
           ("n5_pulso_rapido", "Pulso veloz", ["DO3", "RE3", "MI3", "FA3", "SOL3"], 104, "⚡")]
    for code, title, seq, tempo, icon in rit:
        A.append(_activity(code, E, title, 5, seq, mode=PlayMode.SPEED,
                           tempo=tempo, icon=icon, tolerance_ms=1800,
                           skills=_note_skills(seq) + ["ritmo_basico"]))
    A.append(_activity("n5_juego_rio", G, "El Río del Ritmo", 5,
                       ["SOL3", "SOL3", "MI3", "MI3", "FA3", "RE3", "DO3"],
                       mode=PlayMode.SPEED, tempo=92, icon="🌊",
                       tolerance_ms=1700, skills=["ritmo_basico"]))

    # ---- Nivel 6: melodías y notas agudas --------------------------------
    for code in ("LA3", "SI3", "DO4"):
        s = solfa(code)
        A.append(_activity(f"n6_{code}_intro", E, f"Conoce a {s}", 6,
                           [code] * 4, tempo=64, icon="☁️"))
    A.append(_activity("n6_octava", E, "La octava completa", 6, list(NOTE_CODES),
                       tempo=76, icon="🌈", skills=list(f"nota_{c}" for c in NOTE_CODES)))

    # ---- Canciones y nivel 7 --------------------------------------------
    song_level = {"cancion_estrellita": 3, "cancion_corderito": 3,
                  "cancion_iguana": 4, "cancion_rio": 5,
                  "cancion_campanas": 6, "cancion_concierto": 7,
                  "cancion_pollitos": 3, "cancion_cucu": 3,
                  "cancion_aserrin": 3, "cancion_pinpon": 4,
                  "cancion_arroz": 4, "cancion_anton": 4,
                  "cancion_cumpleanos": 4, "cancion_vaca": 5,
                  "cancion_mambru": 5, "cancion_cucaracha": 5,
                  "cancion_nochedepaz": 6, "cancion_alegria": 7,
                  "cancion_martinillo": 5}
    for code, title, seq, tempo, icon in SONGS:
        lvl = song_level[code]
        A.append(_activity(code, S, title, lvl, seq, mode=PlayMode.MELODY,
                           tempo=tempo, icon=icon,
                           skills=_note_skills(seq) + ["melodia_simple"],
                           desc="Toca la melodía completa con tus manitas."))

    A.append(_activity("n7_reto_final", V, "El Gran Reto", 7,
                       ["DO3", "SOL3", "MI3", "DO4", "LA3", "FA3", "RE3", "SI3"],
                       mode=PlayMode.CHALLENGE, hints=False, tempo=84, icon="🏆",
                       skills=["reto_libre"]))
    A.append(_activity("n7_improvisa", G, "Inventa tu Melodía", 7, [],
                       mode=PlayMode.FREE, tempo=70, icon="🎹",
                       skills=["reto_libre"],
                       desc="Modo libre: toca las notas que quieras y guárdalas."))

    # ---- Repasos generados por nota --------------------------------------
    niveles_nota = {"DO3": 1, "RE3": 1, "MI3": 1, "FA3": 2, "SOL3": 2,
                    "LA3": 6, "SI3": 6, "DO4": 6}
    for code in NOTE_CODES:
        s = solfa(code)
        A.append(_activity(f"repaso_{code}", R, f"Repaso de {s}",
                           niveles_nota[code], [code, code, code], tempo=64,
                           icon="🔄",
                           desc=f"Un repaso corto para no olvidar {s}."))
    return A


# ---------------------------------------------------------------- logros

def build_achievements() -> list[Achievement]:
    items = [
        Achievement("primer_gesto", "¡Primera seña!", "Hiciste tu primera seña musical.", "👋"),
        Achievement("primera_cancion", "Primera canción", "Terminaste una canción completa.", "🎶"),
        Achievement("tres_estrellas", "Estrella dorada", "Conseguiste tres estrellas en una actividad.", "⭐"),
        Achievement("racha_3", "Tres días seguidos", "Jugaste tres días seguidos.", "🔥"),
        Achievement("racha_7", "Una semana entera", "Jugaste siete días seguidos.", "🔥"),
        Achievement("combo_10", "Diez seguidas", "Acertaste diez señas sin fallar.", "⚡"),
        Achievement("octava_completa", "La octava completa", "Tocaste las ocho notas en orden.", "🌈"),
        Achievement("cien_intentos", "Manos incansables", "Hiciste cien señas en total.", "💪"),
        Achievement("compositor", "Compositor", "Guardaste una melodía propia.", "🎹"),
    ]
    for code in NOTE_CODES:
        items.append(Achievement(f"domina_{code}", f"Dominaste {solfa(code)}",
                                 f"Alcanzaste el dominio de la seña de {solfa(code)}.", "🏅"))
    return items


# ---------------------------------------------------------------- siembra

def seed(db: Database | None = None, force: bool = False) -> None:
    db = db or get_db()
    if not force and db.get_meta("seed_version") == SEED_VERSION:
        return
    SkillRepository(db).upsert_many(build_skills())
    ActivityRepository(db).upsert_many(build_activities())
    AchievementRepository(db).upsert_many(build_achievements())
    db.set_meta("seed_version", SEED_VERSION)
