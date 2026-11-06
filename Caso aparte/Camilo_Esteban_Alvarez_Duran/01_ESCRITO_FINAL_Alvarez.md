# ESCRITO FINAL — Camilo Esteban Alvarez Durán
**Tu hilo:** La variabilidad de la fracción derivada, no solo la media de la dosis, limita el cumplimiento; el factorial 2³ de 24 corridas puede medirla.

---
## ESCRITO FINAL 1 — Preprint para transcribir a mano
**Sensibilidad y robustez de un clorificador pasivo de PVC: simulación y diseño factorial 2³**

**Resumen.** Un clorificador pasivo no tiene sensor ni control: lo que importa es qué tan estable es su dosis. Analizamos la robustez de nuestro clorificador de PVC con 1.000 escenarios de Monte Carlo y nueve variables. La fracción derivada y la demanda de cloro dominaron la sensibilidad. Fijar la fracción en su media subió el cumplimiento de 44,5 % a 70,9 %. Diseñamos un factorial 2³ de 24 corridas aleatorizadas para validarlo. No hay mediciones validadas.

**1. Problema y brecha.** En El Vidrial (Montería) no hay desinfección continua. Los estudios de campo muestran que la variabilidad es el problema: en Ghana hubo grandes fluctuaciones del cloro con el método pasivo; en un clorador modificado de las Islas Vírgenes la desviación fue de 0,5 a 0,8 mg/L, tan ancha como nuestra ventana de 0,3 mg/L; en un dosificador comercial importó la posición del equipo, no la presión. Nos faltaba saber qué variables controlan el cloro en nuestro diseño y cómo validarlo.

**2. Búsqueda (PRISMA).** OpenAlex, 6 de noviembre de 2026. Identificados 328; ventana 2020–2026: 164; con DOI, artículo, inglés o español: 123; con título sobre cloración: 38; excluidos al leer el resumen: 25; incluidos: 13, más 10 fuentes de norma y método. Total 23.

**3. Modelo y diseño.** C_r = máx[ (α·C_c − D)·e^(−k·t) / (f_T·f_pH·f_tu·f_Q) , 0 ].   Sensibilidad: correlación de Spearman entre cada entrada y α·C_c − D.   Factorial 2³: A = caudal (0,5 y 1,5 L/s), B = válvula de derivación (25 y 75 %), C = pastillas (1 y 2).   Y_ijkl = μ + A_i + B_j + C_k + (AB) + (AC) + (BC) + (ABC) + ε.   Diferencia mínima detectable: δ = 2·f·σ, con potencia 80 % y 16 gl del error.

**4. Hallazgos y discusión.** Spearman: fracción derivada 0,65; demanda −0,63; cloro de cámara 0,31; las demás variables |ρ| ≤ 0,03. En el mejor punto del mapa el cumplimiento fue 44,6 %; con la fracción fija, 70,9 %: la variabilidad cuesta 26 puntos. Con σ = 0,10 mg/L, el diseño 2³ detecta diferencias de 0,12 mg/L (f = 0,61). Recomendamos fijar la posición de las válvulas, por ejemplo con topes u orificio calibrado, y medir α por aforo.

**5. Límites.** Distribuciones supuestas; factores de T, pH, turbidez y Q no ajustados a datos; Spearman no captura interacciones; σ = 0,10 es una hipótesis. Hay diez registros de septiembre de 2026 con caudales consistentes, pero no confirmamos su procedencia y no los usamos. TRL 3.

---
## ESCRITO FINAL 2 — Resumen y abstract

(ver recuadro 2 en el .docx)

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Sensibilidad y robustez de un clorificador pasivo de PVC con derivación: simulación Monte Carlo y diseño factorial 2³ para su validación experimental

[Título art] Sensitivity and robustness of a passive PVC bypass chlorinator: Monte Carlo simulation and a 2³ factorial design for its experimental validation

[Nombre autores] Camilo Esteban Alvarez-Durán^{1}^{*}, Roxana Elena Muñoz-Rodiño^{2}, Andrea Guzmán-Gómez^{3}, Cristian Javier Cano-Mogollón^{4}

^{1} Autor 1: Camilo Esteban Alvarez-Durán - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: camilo.alvarezd@upb.edu.co

^{2} Autor 2: Roxana Elena Muñoz-Rodiño - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: roxana.munoz@upb.edu.co

^{3} Autor 3: Andrea Guzmán-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andrea.guzmang@upb.edu.co

^{4} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^{*} Autor de correspondencia: Camilo Esteban Alvarez-Durán (camilo.alvarezd@upb.edu.co).

**Resumen:

Los clorificadores pasivos prometen desinfectar sin electricidad, pero su desempeño real depende de qué tan estable sea la dosis que entregan. Este trabajo analiza la robustez de un clorificador de PVC con derivación, pensado para la vereda El Vidrial (Montería), y define cómo validarlo. Con 1.000 escenarios de Monte Carlo y nueve variables de entrada se calculó la correlación de Spearman con el cloro neto y se evaluó cuánto del incumplimiento se debe a la media de la dosis y cuánto a su variabilidad. Las variables dominantes fueron la fracción derivada (ρ = 0,65) y la demanda de cloro (ρ = -0,63); el caudal, el tiempo de contacto, la temperatura, el pH y la turbidez tuvieron |ρ| ≤ 0,03. En el mejor punto del mapa de cumplimiento, fijar la fracción derivada en su media elevó el cumplimiento de 44,5 % a 70,9 %. Se propone un diseño factorial 2³ con tres réplicas (24 corridas aleatorizadas) que, con la desviación entre réplicas de 0,10 mg/L, detecta diferencias de 0,12 mg/L con potencia de 80 %. No hay mediciones validadas: las distribuciones son supuestos y el nivel de madurez es TRL 3.

**Palabras clave:

cloración pasiva; análisis de sensibilidad; simulación Monte Carlo; diseño de experimentos; robustez; agua rural; Montería

**Abstract:

Passive chlorinators promise to disinfect water without electricity, but their real performance depends on how stable the dose they deliver is. This paper analyses the robustness of a PVC bypass chlorinator designed for El Vidrial, a rural community in Montería, and defines how to validate it. With 1.000 Monte Carlo scenarios and nine input variables, the Spearman correlation with net chlorine was computed and the share of non-compliance due to the mean dose versus its variability was assessed. The dominant variables were the bypass fraction (ρ = 0,65) and chlorine demand (ρ = -0,63); flow, contact time, temperature, pH and turbidity had |ρ| ≤ 0.03. At the best point of the compliance map, fixing the bypass fraction at its mean raised compliance from 44,5 % to 70,9 %. A 2³ factorial design with three replicates (24 randomized runs) is proposed that, with a replicate standard deviation of 0.10 mg/L, detects differences of 0,12 mg/L with 80 % power. There are no validated measurements: the distributions are assumptions and the readiness level is TRL 3.

**Keywords:

passive chlorination; sensitivity analysis; Monte Carlo simulation; design of experiments; robustness; rural water; Montería

# Introducción

## Más importante que la media es la estabilidad

Un clorificador pasivo no tiene sensor ni lazo de control. Una vez calibrado, entrega la dosis que le permiten su hidráulica y su pastilla, y esa dosis cambia con el caudal, con la temperatura, con el desgaste del producto y con la posición de las válvulas. Por eso su desempeño no se resume en un promedio: lo que decide si el agua queda protegida es la proporción del tiempo en que el cloro residual libre permanece dentro de un rango estrecho. La Resolución 2115 de 2007 fija ese rango en 0,3 a 2,0 mg/L {c:res2115}, y la guía de la Organización Mundial de la Salud recomienda un residual que proteja frente a la recontaminación {c:oms}.

Los estudios de campo muestran que la variabilidad es el problema real. Un clorador local de bajo costo instalado en Guatemala redujo la contaminación fecal, pero solo 24 % de las muestras de grifo alcanzó 0,2 mg/L {c:guatemala}. En Ghana, 685 mediciones en dos redes mostraron grandes fluctuaciones del cloro, en especial con el método pasivo, que el pH, la temperatura, la conductividad y la turbidez no explicaron del todo {c:ghana}. En Honduras, los problemas técnicos explicaron 26 % de los lapsos sin cloro, y los errores ocasionales y habituales de las juntas de agua, 24 y 15 % {c:honduras}. En ensayos de laboratorio con un dosificador comercial en línea, la presión no modificó el cloro residual, pero la posición del dispositivo sí {c:aquatabs}, y un sistema doméstico con clorador de piscina modificado tuvo desviaciones estándar de 0,5 a 0,8 mg/L {c:usvi}. Esa desviación es del tamaño de la ventana objetivo completa.

## Lo que ya se sabe y lo que falta

La búsqueda bibliográfica reproducible (sección 2.6, Figura 1) dejó 13 estudios sobre cloración pasiva o en línea en contextos de bajos recursos. Los ensayos y evaluaciones de campo informan cuánto baja la contaminación microbiológica {c:nepal,odisha,etiopia,pickering}, y los trabajos económicos, si hay demanda de pago por el servicio {c:dhaka,venturi}. El mercado potencial de estos dispositivos es enorme {c:mercado}, y la evidencia agregada indica que clorar reduce la diarrea infantil {c:arnold,clasen}, en un contexto de carga de enfermedad aún alta {c:wolf,amrose}. En los resúmenes revisados no se encontró una descomposición de cuánta variabilidad del cloro viene de cada fuente. Esa descomposición es la que permite decidir qué controlar. Algunos trabajos comparan dispositivos entre sí {c:uganda}; falta hacerlo con un diseño propio antes de construirlo en serie.

*Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.

## Objetivo

El objetivo es doble: (i) identificar, con simulación, qué variables controlan el cloro residual del clorificador de PVC y cuánto pesa la variabilidad de la dosis frente a su media; y (ii) diseñar el experimento que permita validar esos hallazgos con una potencia estadística conocida de antemano.

# Métodos

## Dispositivo y variables controlables

El clorificador usa tubería de PVC de 1 y 2 pulgadas. Una Tee divide el flujo; un ramal de derivación con válvula de bola lleva la fracción $1-\alpha$ y el otro pasa por una cámara de 2 pulgadas de 0,50 m con pastillas de tricloro al 90 % y válvulas de entrada y salida (Figura 2). Tres válvulas fijan la fracción $\alpha$ de caudal que pasa por la cámara. El caudal de diseño es de 0,2 a 2,5 L/s con carga de 1,5 a 5,0 m. Las variables que el operador puede mover son la apertura de las válvulas y la carga de pastillas; el resto (caudal, temperatura, pH, turbidez, demanda) las impone la fuente.

*Figura 2. Clorificador pasivo con derivación; las tres válvulas (V_bp, V_in, V_out) controlan la fracción α.

## Modelo y simulación

El residual libre se calcula con el balance de masa del proyecto, donde $C_c$ es el cloro de cámara, $\alpha$ la fracción derivada, $D$ la demanda, $k$ el decaimiento, $t$ el tiempo de contacto y los $f$ factores de temperatura, pH, turbidez y caudal; la cinética del decaimiento depende de esas condiciones {c:powell}:

Se simularon 1.000 escenarios con la semilla 42 y las distribuciones del cuaderno del proyecto, que son supuestos y no mediciones: caudal normal (1,0; 0,25) L/s, tiempo de contacto normal (20; 4) min, cloro de cámara normal (1,2; 0,3) mg/L, demanda normal (0,65; 0,18) mg/L, fracción beta(2,5; 5,5), decaimiento normal (0,035; 0,010) por minuto, temperatura normal (28; 3) °C, pH normal (7,2; 0,4) y turbidez gamma(2,2; 0,6) NTU. La reproducción coincidió con el archivo original (diferencia máxima 0,0).

## Análisis de sensibilidad y de variabilidad

La sensibilidad se midió con la correlación de rangos de Spearman entre cada variable de entrada y el cloro neto $\alpha C_c-D$, antes de recortar a cero, porque el residual recortado es continuo solo en una parte de los escenarios. Para separar la media de la variabilidad se buscó, en el mapa de cumplimiento (escala de dosis de 0,5 a 6 y demanda media de 0,05 a 1,0 mg/L, con 20.000 escenarios por celda), el punto con mayor cumplimiento y se repitió el cálculo con la fracción derivada fija en su media. Las proporciones llevan intervalos de Wilson {c:wilson}.

## Diseño experimental propuesto

El plan del proyecto es un factorial completo $2^3$ con tres réplicas, 24 corridas, y tres factores: caudal $A$ (0,5 y 1,5 L/s), apertura de la válvula de derivación $B$ (25 y 75 %) y carga de pastillas $C$ (una o dos). La respuesta es el cloro residual libre por DPD. Las 24 corridas se aleatorizaron con semilla 2026 (hoja de ejecución adjunta). El modelo de análisis de varianza es:

Los supuestos se revisarían con Shapiro–Wilk y Levene. La potencia para un efecto principal con $N=24$ y 16 grados de libertad del error se obtuvo de la distribución F no central con parámetro $\lambda=Nf^{2}$, donde $f$ es el tamaño de efecto de Cohen; la diferencia mínima detectable entre niveles es:

## Auditoría de los registros existentes

El repositorio contiene un formato de captura con diez registros de septiembre de 2026. Se verificó que el caudal calculado como volumen entre tiempo coincide con el registrado y que la categoría de cloración corresponde al rango definido. No se usaron como resultado porque su procedencia no pudo confirmarse.

## Búsqueda bibliográfica

La búsqueda en OpenAlex del 6 de noviembre de 2026 (ecuación en prisma_cifras.json) consideró artículos de 2020 a 2026 con DOI. El cribado exigió que el título tratara de cloración; la elegibilidad se evaluó sobre título y resumen. El flujo sigue PRISMA 2020 {c:prisma}. La lectura de texto completo queda pendiente.

# Resultados

## Qué variables controlan el cloro neto

La Tabla 1 y la Figura 3 muestran que dos variables concentran la sensibilidad: la fracción derivada (ρ = 0,65) y la demanda (ρ = -0,63), con una contribución menor del cloro de cámara (ρ = 0,31). El caudal, el tiempo de contacto, la constante de decaimiento, la temperatura, el pH y la turbidez no superaron |ρ| = 0,03. Esto no significa que esas variables carezcan de efecto físico: en el modelo actúan como factores multiplicativos de pocos puntos porcentuales y tienen poca dispersión comparada con la de la dosis.

*Tabla 1. Correlación de Spearman entre cada variable de entrada y el cloro neto (n = 1000)

*Fuente: elaboración propia, estudio_clorificador.py.

*Figura 3. Correlación de Spearman con el cloro neto antes de recortar a cero.

## Media frente a variabilidad

En el cuaderno original, 99,0 % de los escenarios quedó por debajo de 0,2 mg/L y solo 1,0 % en el rango. En el mejor punto del mapa (Figura 4), con una demanda de 0,05 mg/L y una dosis 2,75 veces la del cuaderno, el cumplimiento fue de 44,6 %. Con la fracción derivada fija en su media y el resto sin cambios, el cumplimiento subió a 70,9 %: la variabilidad de la fracción, por sí sola, cuesta 26,3 puntos porcentuales. Ninguna celda del mapa alcanzó 90 %.

*Figura 4. Cumplimiento simulado según la escala de la dosis y la demanda media; la estrella marca los supuestos del cuaderno.

## Potencia del diseño 2³

Con 24 corridas y 16 grados de libertad del error, la potencia de 80 % se alcanza con un tamaño de efecto $f=0{,}61$. Eso corresponde a las diferencias mínimas detectables de la Tabla 2, según la desviación entre réplicas.

*Tabla 2. Diferencia mínima detectable entre niveles de un factor, con potencia de 80 % y α = 0,05

*Fuente: elaboración propia con la distribución F no central.

## Registros existentes

Los diez registros cumplieron la verificación interna: el caudal recalculado coincide con el registrado y las categorías corresponden al rango. Cinco tienen cloro; cuatro de ellos quedan entre 0,2 y 0,5 mg/L y uno, con dos pastillas, en 0,72 mg/L. Al no poder confirmarse su procedencia, no se incluyen en el análisis; si el equipo confirma que son mediciones de laboratorio, serían la primera evidencia contra la cual comparar la simulación.

# Discusión

Dos hallazgos orientan el trabajo experimental. El primero es que la fracción derivada, la única variable que el operador controla de forma directa, es también la que más pesa y la que más varía en el modelo. Fijarla con precisión, por ejemplo con válvulas con tope y marca de posición o con un orificio calibrado en lugar de una válvula de bola, rinde más que afinar la dosis media. Es coherente con lo observado en laboratorio: la posición del dispositivo importó más que la presión {c:aquatabs}. El segundo es que la variabilidad se paga en cumplimiento: 26 puntos porcentuales en el mejor punto del mapa.

La comparación con estudios de campo debe leerse con cautela. Una desviación estándar de 0,5 a 0,8 mg/L en un clorador modificado {c:usvi} es mayor que la ventana de 0,3 mg/L del diseño, y en Ghana, aunque el método pasivo terminó con 100 % de las mediciones en el rango de 0,2 a 2,0 mg/L tras cinco meses, hubo grandes fluctuaciones intermedias {c:ghana}. La norma colombiana admite un rango más ancho (0,3–2,0 mg/L) que el objetivo del proyecto; con ese rango, la tolerancia a la variabilidad sería mucho mayor y el diseño tendría margen. Además, en los dispositivos que se desempeñan bien, el soporte técnico recurrente parece importar tanto como el aparato {c:honduras,odisha}, y en el uso doméstico de dosificadores el conocimiento del procedimiento correcto se asoció con tener cloro residual {c:kmu}.

Limitaciones. Las distribuciones son supuestos; los factores de temperatura, pH, turbidez y caudal no están ajustados a datos; la correlación de Spearman mide asociación monótona y no efectos de interacción; y la desviación entre réplicas de 0,10 mg/L del análisis de potencia es una hipótesis hasta que se mida. La hoja de aleatorización y el diseño 2³ ya están listos; lo que falta es ejecutarlos.

# Conclusiones

En la simulación, la fracción derivada y la demanda de cloro explican casi toda la sensibilidad del cloro neto. Fijar la fracción derivada eleva el cumplimiento de 44,5 % a 70,9 % en el mejor punto del mapa. El diseño factorial 2³ con 24 corridas es suficiente para detectar diferencias de 0,12 mg/L si la desviación entre réplicas es de 0,10 mg/L. El prototipo permanece en TRL 3; el paso siguiente es ejecutar las 24 corridas con la hoja aleatorizada.

# Recomendaciones

(1) Ejecutar el factorial 2³ con la hoja de aleatorización y estimar la desviación entre réplicas con las primeras corridas. (2) Medir la fracción derivada por aforo volumétrico en cada posición de válvula. (3) Probar un dispositivo de fijación de la posición de las válvulas. (4) Medir la demanda del agua antes de cada serie. (5) Confirmar la procedencia de los diez registros de septiembre.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar antes del envío): el primer autor diseñó el análisis de sensibilidad y el plan factorial y programó los cálculos; los otros autores participaron en la investigación bibliográfica y en la revisión crítica; Cristian Javier Cano-Mogollón dirigió el trabajo y editó el manuscrito.

## Declaraciones finales

[Heading 3] Financiación

No se recibió financiación específica para este análisis; los insumos de laboratorio del proyecto figuran en el presupuesto del semillero SILOGE. [Por confirmar.]

[Heading 3] Conflicto de intereses

No hay conflictos de intereses que declarar. [Por confirmar.]

[Heading 3] Consentimiento informado y ética

No aplica, porque no hubo participantes; una prueba con la comunidad pasará antes por revisión ética.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código de la simulación y del análisis, la hoja de aleatorización y los registros de la búsqueda se guardaron junto con el proyecto; la publicación en un repositorio abierto está pendiente. La hoja de aleatorización de las 24 corridas está en DOE_hoja_aleatorizacion.csv.

[Heading 3] Uso de herramientas de inteligencia artificial

Se empleó el asistente Claude (Anthropic) como apoyo en programación, verificación de metadatos de las referencias y redacción preliminar. El equipo comprobó las salidas y asume la autoría del contenido.

**Declarations (English)

Author Contributions: the first author designed the sensitivity analysis and the factorial plan and wrote the code; the other authors took part in the literature search and critical review; C. J. Cano-Mogollón directed the work and edited the manuscript. Funding: no specific funding. No conflicts of interest. Ethics and consent: not applicable. Data and code: available in the project's shared folder.

# References

[1] Ministerio de la Protección Social y Ministerio de Ambiente, Vivienda y Desarrollo Territorial, “Resolución 2115 de 2007, por medio de la cual se señalan características, instrumentos básicos y frecuencias del sistema de control y vigilancia para la calidad del agua para consumo humano,” Bogotá, Colombia, 2007. [Online]. Available: https://normograma.invima.gov.co/normograma/compilacion/docs/resolucion_minproteccion_2115_2007.htm. Accessed: Nov. 6, 2026.

[2] World Health Organization, Guidelines for Drinking-water Quality: Fourth Edition Incorporating the First and Second Addenda. Geneva, Switzerland: WHO, 2022. [Online]. Available: https://www.who.int/publications/i/item/9789240045064. Accessed: Nov. 6, 2026.

[3] J. M. Locher et al., “Assessment of a local and low-cost passive in-line chlorination device in rural Guatemala,” PLOS Water, vol. 3, no. 9, art. e0000255, 2024, doi: 10.1371/journal.pwat.0000255.

[4] C. Delaire et al., “Comparison of passive and manual chlorination in small piped water networks in rural Ghana: Technical performance, ease-of-use, and cost,” PLOS Water, vol. 3, no. 10, art. e0000295, 2024, doi: 10.1371/journal.pwat.0000295.

[5] M. Lindmark, W. Meier, D. Calix, and C. Just, “Performance of Community Water Board-Managed Passive In-Line Chlorinators Supported by a Circuit Rider Program in Rural Honduras,” ACS ES&T Water, vol. 3, no. 12, pp. 4011-4019, 2023, doi: 10.1021/acsestwater.3c00425.

[6] L. E. Voth-Gaeddert and A. Schranck, “Inline Chlorinator for Potable Water Systems in Low-Resource Settings,” Journal of Environmental Engineering, vol. 147, no. 7, art. 06021003, 2021, doi: 10.1061/(asce)ee.1943-7870.0001883.

[7] L. E. Voth-Gaeddert, M. Lemley, K. Brathwaite, A. Schranck, and S. Libbey, “Design and Evaluation of a Household Chlorination System for Treating Cistern Water in the US Virgin Islands,” Journal of Environmental Engineering, vol. 148, no. 11, art. 06022002, 2022, doi: 10.1061/(asce)ee.1943-7870.0002063.

[8] Y. S. Crider et al., “Evaluation of System-Level, Passive Chlorination in Gravity-Fed Piped Water Systems in Rural Nepal,” Environmental Science & Technology, vol. 56, no. 19, pp. 13985-13995, 2022, doi: 10.1021/acs.est.2c03133.

[9] J. Lowe et al., “In-line chlorination for drinking water in rural Odisha, India: A randomized controlled implementation trial,” PLOS Water, vol. 5, no. 4, art. e0000440, 2026, doi: 10.1371/journal.pwat.0000440.

[10] R. Meierhofer et al., “Water quality at the point of consumption and child health after installing in-line chlorination with electrolysis in Ethiopia,” PLOS Water, vol. 5, no. 7, art. e0000575, 2026, doi: 10.1371/journal.pwat.0000575.

[11] A. J. Pickering et al., “Effect of in-line drinking water chlorination at the point of collection on child diarrhoea in urban Bangladesh: a double-blind, cluster-randomised controlled trial,” The Lancet Global Health, vol. 7, no. 9, pp. e1247-e1256, 2019, doi: 10.1016/S2214-109X(19)30315-8.

[12] D. W. Smith et al., “Effective Demand for In-Line Chlorination Bundled with Rental Housing in Dhaka, Bangladesh,” Environmental Science & Technology, vol. 55, no. 18, pp. 12471-12482, 2021, doi: 10.1021/acs.est.1c01308.

[13] J. E. Powers et al., “Design, performance, and demand for a novel in-line chlorine doser to increase safe water access,” npj Clean Water, vol. 4, no. 1, art. 4, 2021, doi: 10.1038/s41545-020-00091-1.

[14] K. Cherukumilli, R. Bain, Y. Chen, and A. J. Pickering, “Estimating the Global Target Market for Passive Chlorination,” Environmental Science & Technology Letters, vol. 10, no. 1, pp. 105-110, 2022, doi: 10.1021/acs.estlett.2c00781.

[15] B. F. Arnold and J. M. Colford, “TREATING WATER WITH CHLORINE AT POINT-OF-USE TO IMPROVE WATER QUALITY AND REDUCE CHILD DIARRHEA IN DEVELOPING COUNTRIES: A SYSTEMATIC REVIEW AND META-ANALYSIS,” The American Journal of Tropical Medicine and Hygiene, vol. 76, no. 2, pp. 354-364, 2007, doi: 10.4269/ajtmh.2007.76.354.

[16] T. F. Clasen et al., “Interventions to improve water quality for preventing diarrhoea,” Cochrane Database of Systematic Reviews, vol. 2015, no. 10, 2015, doi: 10.1002/14651858.CD004794.pub3.

[17] J. Wolf et al., “Burden of disease attributable to unsafe drinking water, sanitation, and hygiene in domestic settings: a global analysis for selected adverse health outcomes,” The Lancet, vol. 401, no. 10393, pp. 2060-2071, 2023, doi: 10.1016/S0140-6736(23)00458-0.

[18] S. Amrose, Z. Burt, and I. Ray, “Safe Drinking Water for Low-Income Regions,” Annual Review of Environment and Resources, vol. 40, no. 1, pp. 203-231, 2015, doi: 10.1146/annurev-environ-031411-091819.

[19] L. D. Lukas Dössegger et al., “Assessment of low-cost, non-electrically powered chlorination devices for gravity-driven membrane water kiosks in eastern Uganda,” Waterlines, vol. 40, no. 2, pp. 92-106, 2021, doi: 10.3362/1756-3488.20-00014.

[20] J. C. Powell, N. B. Hallam, J. R. West, C. F. Forster, and J. Simms, “Factors which control bulk chlorine decay rates,” Water Research, vol. 34, no. 1, pp. 117-126, 2000, doi: 10.1016/S0043-1354(99)00097-4.

[21] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[22] M. J. Page et al., “The PRISMA 2020 statement: an updated guideline for reporting systematic reviews,” BMJ, art. n71, 2021, doi: 10.1136/bmj.n71.

[23] I. Evance et al., “Assessing factors affecting the use of chlorine dispensers for household water treatment in rural Kenya, Malawi, and Uganda,” Journal of Water, Sanitation and Hygiene for Development, vol. 15, no. 1, pp. 84-94, 2024, doi: 10.2166/washdev.2024.407.

---
## Guion de defensa

**¿Por qué Spearman y no regresión?**  
Las relaciones son monótonas pero no lineales (exponenciales y productos). Spearman mide asociación monótona y no exige linealidad; lo aplicamos al cloro neto antes de recortar a cero, que es continuo.

**¿Cómo calculaste la potencia del diseño?**  
Con la F no central: λ = N·f² con N = 24, 16 gl del error y F crítico al 5 %. Potencia 80 % se logra con f = 0,61, lo que da δ = 2·f·σ; con σ = 0,10 mg/L, δ = 0,12 mg/L. σ es hipótesis hasta medirla.

**¿Por qué la fracción fija sube el cumplimiento a 70,9 %?**  
Porque en el cuaderno la fracción es beta(2,5; 5,5), con desviación grande. Al fijarla en su media se elimina esa fuente de dispersión, y queda la del cloro de cámara y la demanda.

**¿Los diez registros de septiembre de 2026?**  
El caudal recalculado coincide y las categorías corresponden al rango. Pero no se confirmó su procedencia; no se usan como resultado. Si el equipo confirma que son mediciones, serían la primera evidencia contra la simulación.

**¿Qué harías primero en el laboratorio?**  
Aforo volumétrico de la fracción derivada en cada posición de válvula y las primeras corridas del factorial para estimar σ.
