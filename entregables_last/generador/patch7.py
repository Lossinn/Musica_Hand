s = open("art_unico.py", encoding="utf-8").read()


def cambiar(inicio, fin, nuevo):
    global s
    a = s.index(inicio); b = s.index(fin, a) + len(fin)
    s = s[:a] + nuevo + s[b:]


cambiar('T("El gemelo digital del aprendiz es', 'Lo consumen el motor adaptativo, el optimizador y la zona de padres.")',
        'T("Con el nombre de gemelo digital del aprendiz llamamos a la fotografía del estado de aprendizaje de un niño en un instante. Tiene tres caras. Una por habilidad, con el dominio, la precisión, la consistencia, la velocidad, la retención, los días sin practicar y la fecha del próximo repaso. '
        'Otra de conducta, con las notas que confunde, su tiempo de reacción y el número de intentos. Y una de evolución, con los minutos por semana, las actividades hechas y la tendencia. '
        'Cada vez que se consulta, el modelo descuenta primero el olvido acumulado desde la última práctica, así que quien mira el progreso dos semanas después ve el estado real y no el de la última sesión. Del gemelo se alimentan el motor adaptativo, el optimizador y la zona de padres.")')
cambiar('T("Dos errores reales se encontraron por esta vía', 'dejaba al niño sin señas.")',
        'T("Las pruebas sirvieron para algo más que confirmar lo esperado: dos fallos reales salieron de ellas y no de revisar el código a ojo. En el estabilizador, el contador de suelta volvía a cero apenas la nota reaparecía, y por eso un niño nunca podía repetir la misma nota. '
        'En la recalibración, entrar a la pantalla vaciaba las plantillas de la memoria antes de capturar nada, de manera que quien salía a mitad de camino se quedaba sin sus señas.")')
cambiar('T("El motor adaptativo recibe un retrato del momento', 'el tiempo $t$ sobre un máximo $T_s$:")',
        'T("El motor adaptativo no dibuja pantallas; toma una decisión. Para ello mira cómo está el niño en ese momento: el dominio de cada habilidad, la precisión de la última actividad, los fallos seguidos, los repasos vencidos y una estimación de fatiga que mezcla cuánto ha jugado (actividades $n$ sobre un máximo $N$) y cuánto tiempo lleva (tiempo $t$ sobre un máximo $T_s$):")')
cambiar('T("La primera versión comparaba las coordenadas crudas', 'Esa separación permite ejecutar las pruebas sin cámara y sin ventana.")',
        'T("Nuestra primera versión era directa: tomaba los puntos que entregaba la cámara, los comparaba con una plantilla guardada y daba la nota por buena si el parecido pasaba de un umbral. Servía para una demostración, pero cargaba con toda la variabilidad de la escena (qué tan lejos está el niño, cuánto inclina la muñeca, qué tan grande es su mano) '
        'y concentraba la cámara, la música, el puntaje y el dibujo en un único archivo de 1.740 líneas, donde cualquier cambio obligaba a tocar todo. La versión que evaluamos reparte el trabajo en cinco capas que solo se comunican hacia abajo, con un bus de eventos para que las de arriba sepan qué ocurre sin depender de las de abajo (Figura 2). '
        'Ninguna pantalla importa MediaPipe, ninguna pieza de visión sabe qué es una nota y el evaluador no sabe dibujar. Gracias a eso las pruebas corren sin cámara y sin ventana.")')
open("art_unico.py", "w", encoding="utf-8").write(s)
print("ok")
