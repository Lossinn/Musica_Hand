import re
s = open("art_unico.py", encoding="utf-8").read()

# 1) título más corto
i = s.index("TITULO_ES = ("); j = s.index("RES_ES = (")
s = s[:i] + '''TITULO_ES = ("Hand Sing Kids: señas de las manos, aprendizaje adaptativo y selección de actividades para enseñar música a niños. "
             "Diseño, evaluación de laboratorio y camino hacia el aula en Montería")
TITULO_EN = ("Hand Sing Kids: hand signs, adaptive learning and activity selection to teach music to children. "
             "Design, laboratory evaluation and the road to the classroom in Montería")

''' + s[j:]

# 2) resúmenes más cortos
i = s.index("RES_ES = ("); j = s.index("KW_ES = ")
nuevo = '''RES_ES = ("Aprender música con las manos es una práctica antigua, pero llevarla a una aplicación obliga a resolver a la vez tres problemas: reconocer cuándo el niño hizo de verdad una seña, estimar lo que sabe y decidir qué debe practicar después. "
          "Este artículo presenta Hand Sing Kids, una aplicación de escritorio en Python que asigna una seña de las dos manos a cada nota de Do3 a Do4 y funciona con cámara y base local, sin internet. "
          "El reconocedor describe cada postura con un vector de 120 componentes invariante al tamaño, la posición y el giro de la mano y acepta una nota solo si la distancia, la confianza y el margen lo permiten; el modelo de aprendizaje combina precisión, consistencia, velocidad y retención con repaso espaciado; "
          "y la sesión se elige con un problema entero mixto que tiene respaldo exacto. De 189 documentos únicos reunidos, 87 resultaron aprovechables y solo ocho trataban la música infantil. "
          f"En laboratorio, con una calibración de una persona y perturbaciones simuladas, el reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, y ante 640 posturas que no son seña el método disparó una nota por error en {f(FPG['pct'])} % de los casos, frente a 100 % del método inicial. "
          "No hubo pruebas con niños: el nivel de madurez es TRL 4 y el efecto sobre el aprendizaje en Montería y Córdoba se plantea como hipótesis, con un plan de piloto.")
RES_EN = ("Learning music with the hands is an old practice, but taking it to an application means solving three problems at once: recognizing when a child really made a sign, estimating what the child knows and deciding what to practise next. "
          "This paper presents Hand Sing Kids, a desktop application in Python that assigns a two-handed sign to each note from C3 to C4 and works with a camera and a local database, with no internet. "
          "The recognizer describes each posture with a 120-component vector invariant to hand size, position and rotation and accepts a note only if distance, confidence and margin allow it; the learning model combines accuracy, consistency, speed and retention with spaced repetition; "
          "and the session is chosen with a mixed-integer problem that has an exact fallback. Of 189 unique documents gathered, 87 proved useful and only eight dealt with children's music. "
          f"In the laboratory, with a single-person calibration and simulated perturbations, recognition was {f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09, and over 640 non-sign postures the method fired a wrong note in {f(FPG['pct'])} % of cases, against 100 % for the initial method. "
          "No tests with children were done: the readiness level is TRL 4 and the effect on learning in Montería and Córdoba is stated as a hypothesis, with a pilot plan.")
'''
s = s[:i] + nuevo + s[j:]

# 3) quitar figuras 5, 7 y 8 y renumerar
def quitar(inicio):
    global s
    a = s.index(inicio); b = s.index("\n", a)
    s = s[:a] + s[b + 1:]
quitar('figura(["umbral_confianza.png"]')
quitar('figura(["ventana_tempo.png"]')
quitar('figura(["dominio_retencion.png"]')
reemplazos = [
    ("El umbral de confianza es la perilla que mueve el compromiso (Figura 5): con 0,35", "El umbral de confianza es la perilla que mueve el compromiso: con 0,35"),
    ("que sí cambian de una seña a otra (Figura 6).", "que sí cambian de una seña a otra (Figura 5)."),
    ("y deja 276 ms antes y 204 ms después de la línea (Figura 7). ", "y deja 276 ms antes y 204 ms después de la línea. "),
    ("{f(r_um(0.85, 0.7), 2)} (Figura 8). En días", "{f(r_um(0.85, 0.7), 2)}. En días"),
    ('"Figura 6. Matrices 8 × 8', '"Figura 5. Matrices 8 × 8'),
    ('[2.6, 8.6, 1.0, 1.0])', '[2.6, 7.9, 1.3, 1.4])'),
]
for a, b in reemplazos:
    assert a in s, a[:60]
    s = s.replace(a, b, 1)
open("art_unico.py", "w", encoding="utf-8").write(s)
print("ok")
