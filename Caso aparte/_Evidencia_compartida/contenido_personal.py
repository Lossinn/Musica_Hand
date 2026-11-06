"""Textos individuales (ESCRITO FINAL del preprint a mano, guion de defensa y notas) de cada integrante."""

PERSONAS = {
    "Muñoz": {
        "carpeta": "Roxana_Elena_Munoz_Rodino",
        "nombre": "Roxana Elena Muñoz Rodiño",
        "correo": "roxana.munoz@upb.edu.co",
        "id": "000525435",
        "art": "art_roxana",
        "sufijo": "Munoz",
        "titulo_corto": "Balance de masa y demanda de cloro en un clorificador pasivo de PVC",
        "hilo": "La demanda de cloro como restricción de diseño: con un balance de masa, el clorificador necesita una dosis en la mezcla de unos 1,7 mg/L y el diseño supuesto entrega 0,39 mg/L.",
        "preprint": {
            "titulo": "Balance de masa y demanda de cloro en un clorificador pasivo de PVC para El Vidrial, Montería",
            "secciones": [
                ("Resumen", "Diseñamos un clorificador pasivo de PVC que divide el caudal, pasa una fracción por una cámara con pastillas de tricloro al 90 % y recombina las corrientes. "
                 "Costó 159.991 COP en materiales. Con un balance de masa calculamos cuánta dosis necesita para dejar entre 0,2 y 0,5 mg/L de cloro libre y simulamos 1.000 escenarios. "
                 "Con los supuestos del equipo, solo el 1,0 % de los escenarios queda en el rango. La demanda de cloro debe medirse antes de calibrar. No hay validación experimental."),
                ("1. Problema y brecha", "En El Vidrial, vereda rural de Montería, las familias usan fuentes de agua sin tratamiento adecuado. La Resolución 2115 de 2007 pide entre 0,3 y 2,0 mg/L de cloro "
                 "residual libre y dice que la dosis debe salir de pruebas de demanda. Nuestro diseño tenía un rango propio de 0,2 a 0,5 mg/L, pero no una prueba de demanda. En la literatura, los "
                 "cloradores pasivos reducen E. coli, pero su dosis varía mucho: en Guatemala solo el 24 % de los grifos llegó a 0,2 mg/L y en Ghana las fluctuaciones apuntaron a cambios en la demanda."),
                ("2. Búsqueda (PRISMA)", "Buscamos en OpenAlex el 6 de noviembre de 2026, artículos de 2020 a 2026. Identificados: 328 (164 en la ventana). Con DOI, artículo e idioma: 123. "
                 "Cribado por título (debe tratar de cloración): 38. Evaluados por título y resumen: 38; excluidos 25. Incluidos: 13. Más 10 fuentes de norma, guías y método: 23 en total."),
                ("3. Modelo", "Q_t = Q_b + Q_c ;  α = Q_c / Q_t.   Cámara: C_c = k_m·A_s·C_sat / (Q_c + k_m·A_s).   Mezcla: C_s = α·C_c.   "
                 "Residual: C_r = máx[ (C_s − D)·e^(−k·t) / (f_T·f_pH·f_tu·f_Q) , 0 ].   Dosis requerida: C_s,mín = D + C*·Φ, con Φ = e^(kt)·f_T·f_pH·f_tu·f_Q.   "
                 "D = demanda, k = decaimiento, t = tiempo de contacto, C* = residual meta (0,4 mg/L)."),
                ("4. Hallazgos y discusión", "Con los valores medios supuestos, Φ ≈ 2,64 y la mezcla debe entregar 1,71 mg/L, pero el modelo entrega 0,39 mg/L, 4,4 veces menos. De 1.000 escenarios, 990 "
                 "(99,0 %) quedaron por debajo de 0,2 mg/L y 10 (1,0 %) en el rango. En el mapa de cumplimiento, el máximo fue 44,6 %, y ninguna celda llegó a 90 %. Con α = 0,2 la cámara debería "
                 "tener 8,5 mg/L. Conclusión: antes de calibrar las válvulas hay que medir la demanda de El Vidrial."),
                ("5. Límites", "Las distribuciones son supuestos nuestros, sin medición; el rango 0,2–0,5 es más estrecho que el de la norma; los diez registros de septiembre de 2026 no se usaron "
                 "porque no confirmamos su procedencia. El prototipo está en TRL 3. Siguiente paso: medir la demanda y la tasa de disolución de la pastilla."),
            ],
        },
        "defensa": [
            ("¿Por qué dices que el diseño no cumple si no hay mediciones?", "No digo que el diseño falle en la realidad. Digo que, con los supuestos del propio proyecto (demanda 0,65 mg/L, cámara de 1,2 mg/L), el balance de masa da una dosis efectiva de 0,39 mg/L frente a 1,71 requeridos. La conclusión es condicional y por eso el aporte es el criterio: medir la demanda."),
            ("¿Qué es Φ y de dónde sale?", "Es el factor que junta el decaimiento (e^kt) y los factores de temperatura, pH, turbidez y caudal del modelo del proyecto. Con k = 0,035/min, t = 20 min, T = 28 °C y turbidez media 1,32 NTU, vale 2,64."),
            ("¿Por qué la norma dice 0,3–2,0 y el proyecto 0,2–0,5?", "La Resolución 2115 (art. 9) fija 0,3–2,0 mg/L en la red; 0,2–0,5 es el rango propio del diseño. Su límite inferior queda por debajo del mínimo legal: lo señalamos como limitación."),
            ("¿Cómo se hizo la búsqueda y cuántos artículos leyeron?", "Búsqueda reproducible en OpenAlex con ecuación guardada; cribado por título y evaluación por título y resumen. La lectura de texto completo de los 13 incluidos es una tarea pendiente que debes hacer antes de defender."),
            ("¿Qué sigue?", "Medir demanda de cloro por fuente, medir la tasa de disolución de la pastilla y ejecutar el factorial 2³ ya diseñado."),
        ],
    },
    "Alvarez": {
        "carpeta": "Camilo_Esteban_Alvarez_Duran",
        "nombre": "Camilo Esteban Alvarez Durán",
        "correo": "camilo.alvarezd@upb.edu.co",
        "id": "000503488",
        "art": "art_camilo",
        "sufijo": "Alvarez",
        "titulo_corto": "Sensibilidad y robustez de un clorificador pasivo de PVC",
        "hilo": "La variabilidad de la fracción derivada, no solo la media de la dosis, limita el cumplimiento; el factorial 2³ de 24 corridas puede medirla.",
        "preprint": {
            "titulo": "Sensibilidad y robustez de un clorificador pasivo de PVC: simulación y diseño factorial 2³",
            "secciones": [
                ("Resumen", "Un clorificador pasivo no tiene sensor ni control: lo que importa es qué tan estable es su dosis. Analizamos la robustez de nuestro clorificador de PVC con 1.000 escenarios "
                 "de Monte Carlo y nueve variables. La fracción derivada y la demanda de cloro dominaron la sensibilidad. Fijar la fracción en su media subió el cumplimiento de 44,5 % a 70,9 %. "
                 "Diseñamos un factorial 2³ de 24 corridas aleatorizadas para validarlo. No hay mediciones validadas."),
                ("1. Problema y brecha", "En El Vidrial (Montería) no hay desinfección continua. Los estudios de campo muestran que la variabilidad es el problema: en Ghana hubo grandes fluctuaciones del cloro "
                 "con el método pasivo; en un clorador modificado de las Islas Vírgenes la desviación fue de 0,5 a 0,8 mg/L, tan ancha como nuestra ventana de 0,3 mg/L; en un dosificador comercial "
                 "importó la posición del equipo, no la presión. Nos faltaba saber qué variables controlan el cloro en nuestro diseño y cómo validarlo."),
                ("2. Búsqueda (PRISMA)", "OpenAlex, 6 de noviembre de 2026. Identificados 328; ventana 2020–2026: 164; con DOI, artículo, inglés o español: 123; con título sobre cloración: 38; "
                 "excluidos al leer el resumen: 25; incluidos: 13, más 10 fuentes de norma y método. Total 23."),
                ("3. Modelo y diseño", "C_r = máx[ (α·C_c − D)·e^(−k·t) / (f_T·f_pH·f_tu·f_Q) , 0 ].   Sensibilidad: correlación de Spearman entre cada entrada y α·C_c − D.   "
                 "Factorial 2³: A = caudal (0,5 y 1,5 L/s), B = válvula de derivación (25 y 75 %), C = pastillas (1 y 2).   Y_ijkl = μ + A_i + B_j + C_k + (AB) + (AC) + (BC) + (ABC) + ε.   "
                 "Diferencia mínima detectable: δ = 2·f·σ, con potencia 80 % y 16 gl del error."),
                ("4. Hallazgos y discusión", "Spearman: fracción derivada 0,65; demanda −0,63; cloro de cámara 0,31; las demás variables |ρ| ≤ 0,03. En el mejor punto del mapa el cumplimiento fue 44,6 %; "
                 "con la fracción fija, 70,9 %: la variabilidad cuesta 26 puntos. Con σ = 0,10 mg/L, el diseño 2³ detecta diferencias de 0,12 mg/L (f = 0,61). Recomendamos fijar la posición de las "
                 "válvulas, por ejemplo con topes u orificio calibrado, y medir α por aforo."),
                ("5. Límites", "Distribuciones supuestas; factores de T, pH, turbidez y Q no ajustados a datos; Spearman no captura interacciones; σ = 0,10 es una hipótesis. Hay diez registros de "
                 "septiembre de 2026 con caudales consistentes, pero no confirmamos su procedencia y no los usamos. TRL 3."),
            ],
        },
        "defensa": [
            ("¿Por qué Spearman y no regresión?", "Las relaciones son monótonas pero no lineales (exponenciales y productos). Spearman mide asociación monótona y no exige linealidad; lo aplicamos al cloro neto antes de recortar a cero, que es continuo."),
            ("¿Cómo calculaste la potencia del diseño?", "Con la F no central: λ = N·f² con N = 24, 16 gl del error y F crítico al 5 %. Potencia 80 % se logra con f = 0,61, lo que da δ = 2·f·σ; con σ = 0,10 mg/L, δ = 0,12 mg/L. σ es hipótesis hasta medirla."),
            ("¿Por qué la fracción fija sube el cumplimiento a 70,9 %?", "Porque en el cuaderno la fracción es beta(2,5; 5,5), con desviación grande. Al fijarla en su media se elimina esa fuente de dispersión, y queda la del cloro de cámara y la demanda."),
            ("¿Los diez registros de septiembre de 2026?", "El caudal recalculado coincide y las categorías corresponden al rango. Pero no se confirmó su procedencia; no se usan como resultado. Si el equipo confirma que son mediciones, serían la primera evidencia contra la simulación."),
            ("¿Qué harías primero en el laboratorio?", "Aforo volumétrico de la fracción derivada en cada posición de válvula y las primeras corridas del factorial para estimar σ."),
        ],
    },
    "Guzmán": {
        "carpeta": "Andrea_Guzman_Gomez",
        "nombre": "Andrea Guzmán Gómez",
        "correo": "andrea.guzmang@upb.edu.co",
        "id": "000511622",
        "art": "art_andrea",
        "sufijo": "Guzman",
        "titulo_corto": "Costo, consumo de cloro y operación de un clorificador pasivo de PVC",
        "hilo": "El costo bajo es condición necesaria pero no suficiente: viabilidad económica, consumo de insumos y condiciones sociotécnicas, condicionadas al desempeño técnico.",
        "preprint": {
            "titulo": "Costo, consumo de cloro y operación de un clorificador pasivo de bajo costo para una comunidad rural de Montería",
            "secciones": [
                ("Resumen", "Un dispositivo barato no resuelve el acceso al agua segura si no se sostiene ni entrega la dosis necesaria. Evaluamos la viabilidad preliminar de nuestro clorificador de PVC "
                 "(159.991 COP en materiales). Calculamos el consumo de pastillas por balance de masa, el costo del cloro por m³ y el tiempo de recuperación según cuántos hogares compartan "
                 "una unidad. Los beneficios son supuestos, no mediciones. La simulación técnica solo cumple en 1,0 % de los escenarios."),
                ("1. Problema y brecha", "Las plantas compactas y los dosificadores con bomba no están al alcance de las juntas de agua rurales. La cloración pasiva se propone como alternativa. Los estudios "
                 "sobre costos y adopción muestran que el cloro es barato (Nepal: 0,06–0,09 USD por m³), pero que hay menor demanda de pago en hogares pobres (Dhaka) y que el soporte técnico "
                 "(Honduras) y el conocimiento de uso (Kenia, Malawi, Uganda) pesan tanto como el aparato."),
                ("2. Búsqueda (PRISMA)", "OpenAlex, 6 de noviembre de 2026: 328 registros identificados; 164 en 2020–2026; 123 con DOI, artículo, inglés o español; 38 con título sobre cloración; "
                 "25 excluidos al leer el resumen; 13 incluidos. Más 10 fuentes de norma y método. Total 23."),
                ("3. Modelo", "Masa de cloro: M_Cl = d·Q·86.400 / 1.000 [g/día].   Pastillas: M_TCCA = M_Cl / 0,90.   Recuperación: T_R = I / (n·B − O).   VPN = −I + Σ (n·B − O)/(1 + r)^t, t = 1…12.   "
                 "I = 159.991; B = 25.000 COP/mes por hogar (supuesto); O = 15.000 COP/mes; r = 0,8 % mensual; n = hogares que comparten la unidad."),
                ("4. Hallazgos y discusión", "Costo teórico del cloro: 6,7 a 17,5 COP por m³ (disolución ideal; 1 kg ≈ 15.000 COP): es un piso, porque en Nepal costó más de diez veces. Con un hogar, la "
                 "recuperación es de 16,0 meses y el VPN a 12 meses es −46.005 COP; con 2 hogares, 4,6 meses; con 3, 2,7; con 10, 0,7. Conviene verlo como infraestructura comunal. Pero con "
                 "99,0 % de escenarios por debajo de 0,2 mg/L, el ahorro solo se materializa si el dispositivo funciona."),
                ("5. Límites", "El beneficio mensual, el precio y la masa de las pastillas no están medidos; el VPN del documento del proyecto (96.800 COP) no se reprodujo; no se midió aceptación comunitaria. "
                 "TRL 3. Siguiente paso: medir consumo real, presupuestar visitas técnicas y encuestar gasto en agua y salud."),
            ],
        },
        "defensa": [
            ("¿Por qué una unidad con un solo hogar no se recupera en menos de 12 meses?", "Porque el beneficio supuesto (25.000 COP/mes) menos el costo operativo (15.000) deja 10.000 COP/mes; 159.991/10.000 = 16 meses. Compartida por dos o más hogares, baja de cinco meses."),
            ("¿De dónde sale el costo de 6,7–17,5 COP por m³?", "Del balance de masa: dosis (0,4 o 1,05 mg/L) / 0,90 de cloro disponible = g de pastilla por m³, por 15 COP/g. Es el mínimo estequiométrico; el gasto real será mayor, como mostró Nepal."),
            ("¿Por qué no usaron el ROI de 361 % del 2.º corte?", "Porque dependía de 60 familias, 10 unidades y beneficios por 44,5 millones COP sin respaldo medido en el repositorio. Aquí solo usamos datos del presupuesto y del documento final de PI-I, con la cifra del VPN recalculada."),
            ("¿Cómo se relaciona el costo con la simulación?", "El ahorro económico supone agua protegida. Con 1,0 % de escenarios en el rango, el beneficio no está garantizado: por eso decimos que el costo bajo es necesario pero no suficiente."),
            ("¿Qué falta medir?", "Consumo real de pastillas, precio y masa por paquete, gasto de hogares en agua y salud, y aceptación comunitaria."),
        ],
    },
}
