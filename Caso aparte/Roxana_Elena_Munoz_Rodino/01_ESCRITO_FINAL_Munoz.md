# ESCRITO FINAL — Roxana Elena Muñoz Rodiño
**Tu hilo:** La demanda de cloro como restricción de diseño: con un balance de masa, el clorificador necesita una dosis en la mezcla de unos 1,7 mg/L y el diseño supuesto entrega 0,39 mg/L.

---
## ESCRITO FINAL 1 — Preprint para transcribir a mano
**Balance de masa y demanda de cloro en un clorificador pasivo de PVC para El Vidrial, Montería**

**Resumen.** Diseñamos un clorificador pasivo de PVC que divide el caudal, pasa una fracción por una cámara con pastillas de tricloro al 90 % y recombina las corrientes. Costó 159.991 COP en materiales. Con un balance de masa calculamos cuánta dosis necesita para dejar entre 0,2 y 0,5 mg/L de cloro libre y simulamos 1.000 escenarios. Con los supuestos del equipo, solo el 1,0 % de los escenarios queda en el rango. La demanda de cloro debe medirse antes de calibrar. No hay validación experimental.

**1. Problema y brecha.** En El Vidrial, vereda rural de Montería, las familias usan fuentes de agua sin tratamiento adecuado. La Resolución 2115 de 2007 pide entre 0,3 y 2,0 mg/L de cloro residual libre y dice que la dosis debe salir de pruebas de demanda. Nuestro diseño tenía un rango propio de 0,2 a 0,5 mg/L, pero no una prueba de demanda. En la literatura, los cloradores pasivos reducen E. coli, pero su dosis varía mucho: en Guatemala solo el 24 % de los grifos llegó a 0,2 mg/L y en Ghana las fluctuaciones apuntaron a cambios en la demanda.

**2. Búsqueda (PRISMA).** Buscamos en OpenAlex el 6 de noviembre de 2026, artículos de 2020 a 2026. Identificados: 328 (164 en la ventana). Con DOI, artículo e idioma: 123. Cribado por título (debe tratar de cloración): 38. Evaluados por título y resumen: 38; excluidos 25. Incluidos: 13. Más 10 fuentes de norma, guías y método: 23 en total.

**3. Modelo.** Q_t = Q_b + Q_c ;  α = Q_c / Q_t.   Cámara: C_c = k_m·A_s·C_sat / (Q_c + k_m·A_s).   Mezcla: C_s = α·C_c.   Residual: C_r = máx[ (C_s − D)·e^(−k·t) / (f_T·f_pH·f_tu·f_Q) , 0 ].   Dosis requerida: C_s,mín = D + C*·Φ, con Φ = e^(kt)·f_T·f_pH·f_tu·f_Q.   D = demanda, k = decaimiento, t = tiempo de contacto, C* = residual meta (0,4 mg/L).

**4. Hallazgos y discusión.** Con los valores medios supuestos, Φ ≈ 2,64 y la mezcla debe entregar 1,71 mg/L, pero el modelo entrega 0,39 mg/L, 4,4 veces menos. De 1.000 escenarios, 990 (99,0 %) quedaron por debajo de 0,2 mg/L y 10 (1,0 %) en el rango. En el mapa de cumplimiento, el máximo fue 44,6 %, y ninguna celda llegó a 90 %. Con α = 0,2 la cámara debería tener 8,5 mg/L. Conclusión: antes de calibrar las válvulas hay que medir la demanda de El Vidrial.

**5. Límites.** Las distribuciones son supuestos nuestros, sin medición; el rango 0,2–0,5 es más estrecho que el de la norma; los diez registros de septiembre de 2026 no se usaron porque no confirmamos su procedencia. El prototipo está en TRL 3. Siguiente paso: medir la demanda y la tasa de disolución de la pastilla.

---
## ESCRITO FINAL 2 — Resumen y abstract

(ver recuadro 2 en el .docx)

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Balance de masa y demanda de cloro en un clorificador pasivo por derivación en PVC: simulación de cumplimiento para una vereda rural de Montería, Córdoba

[Título art] Mass balance and chlorine demand in a passive PVC bypass chlorinator: compliance simulation for a rural community in Montería, Córdoba

[Nombre autores] Roxana Elena Muñoz-Rodiño^1^*, Camilo Esteban Alvarez-Durán^2, Andrea Guzmán-Gómez^3, Cristian Javier Cano-Mogollón^4

^1 Autor 1: Roxana Elena Muñoz-Rodiño - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: roxana.munoz@upb.edu.co

^2 Autor 2: Camilo Esteban Alvarez-Durán - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: camilo.alvarezd@upb.edu.co

^3 Autor 3: Andrea Guzmán-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andrea.guzmang@upb.edu.co

^4 Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^* Autor de correspondencia: Roxana Elena Muñoz-Rodiño (roxana.munoz@upb.edu.co).

**Resumen:

El Vidrial, vereda rural de Montería, no cuenta con una desinfección continua y verificable del agua que consume. Se presenta el diseño de un clorificador pasivo de PVC que divide el caudal, hace pasar una fracción por una cámara con pastillas de tricloro al 90 % y recombina las corrientes, con un costo de materiales de 159.991 COP. El objetivo fue establecer, con un balance de masa, cuánta dosis necesita el dispositivo para dejar entre 0,2 y 0,5 mg/L de cloro libre y comprobar si el diseño la entrega bajo los supuestos del equipo. Se simularon 1.000 escenarios de Monte Carlo con caudal, temperatura, pH, turbidez, demanda y fracción derivada variables. La dosis efectiva media fue de 0,39 mg/L frente a una demanda media supuesta de 0,65 mg/L; solo 1,0 % de los escenarios quedó en el rango (IC 95 %: 0,5 a 1,8 %) y 99,0 % quedó por debajo. Un mapa de cumplimiento mostró que bajar la demanda o subir la dosis no basta por sí solo: el máximo fue de 44,6 %. Se concluye que la demanda de cloro debe medirse antes de calibrar el dispositivo, como lo exige la Resolución 2115 de 2007. No hay validación experimental: las distribuciones son supuestos del equipo y el nivel de madurez es TRL 3.

**Palabras clave:

desinfección del agua; cloración pasiva; demanda de cloro; balance de masa; simulación Monte Carlo; agua rural; Montería

**Abstract:

El Vidrial, a rural community in Montería, lacks continuous and verifiable drinking-water disinfection. This paper presents a passive PVC chlorinator that splits the flow, sends a fraction through a chamber with 90 % trichloroisocyanuric acid tablets and recombines the streams, at a materials cost of 159,991 COP. The aim was to establish, through a mass balance, how much dose the device needs to leave 0.2 to 0.5 mg/L of free chlorine and to test whether the design delivers it under the team's assumptions. 1.000 Monte Carlo scenarios were simulated with variable flow, temperature, pH, turbidity, chlorine demand and bypass fraction. The mean effective dose was 0,39 mg/L against an assumed mean demand of 0,65 mg/L; only 1,0 % of scenarios fell inside the range (95 % CI 0,5 to 1,8 %) and 99,0 % fell below it. A compliance map showed that neither lowering the demand nor raising the dose is enough on its own: the maximum was 44,6 %. Chlorine demand should be measured before the device is calibrated, as Colombian regulation requires. There is no experimental validation: the distributions are team assumptions and the readiness level is TRL 3.

**Keywords:

water disinfection; passive chlorination; chlorine demand; mass balance; Monte Carlo simulation; rural water; Montería

# Introducción

## El problema de dosificar sin conocer la demanda

Desinfectar con cloro parece una operación sencilla: se agrega una cantidad de producto y se espera. En la práctica, el cloro que se agrega se reparte entre lo que oxida la materia orgánica y los metales disueltos, lo que decae con el tiempo y la temperatura, y lo que queda como residual libre, que es lo único que protege el agua después. Si la dosis no supera la demanda, el residual es cero aunque se haya vertido producto. La Resolución 2115 de 2007 pide que el cloro residual libre esté entre 0,3 y 2,0 mg/L en cualquier punto de la red y dice, además, que la dosis debe resultar de pruebas frecuentes de demanda [1]. Las guías de la Organización Mundial de la Salud van en la misma dirección [2]. Un dispositivo que no parte de la demanda del agua que trata está calibrado a ciegas.

El Vidrial es una vereda rural de Montería, Córdoba, cuyas familias, según la caracterización preliminar del proyecto, usan fuentes de agua sin tratamiento adecuado o métodos informales de potabilización. El contexto no es excepcional: la carga de enfermedad atribuible al agua insegura y al saneamiento deficiente sigue siendo alta [3], y revisiones y ensayos muestran que clorar en el punto de uso o de recolección reduce la diarrea infantil [4]–[6]. Entre las opciones de bajo costo, la cloración pasiva, es decir, la que no requiere electricidad ni una acción diaria del usuario, se considera una vía para ampliar el acceso [7], [8].

## Qué muestra la literatura reciente

Se hizo una búsqueda reproducible en OpenAlex (sección 2.4). De 328 registros se retuvieron 13 estudios sobre cloración pasiva, en línea o con dosificadores en contextos de bajos recursos (Figura 1). Sus resultados dependen mucho de qué tan bien se ajusta la dosis a las condiciones locales. En seis sistemas de agua por gravedad de Nepal, la cloración pasiva bajó la presencia de E. coli en los grifos de más de 80 % a 7 % en un año [9]. En Guatemala, un clorador local de bajo costo redujo la contaminación fecal, pero solo 24 % de las muestras de grifo alcanzó el mínimo de 0,2 mg/L [10]. En Ghana, el cloro libre estuvo en el rango de 0,2 a 2,0 mg/L en 86 % de las mediciones con el método pasivo y en 71 % con el manual, y las fluctuaciones observadas no quedaron explicadas por el pH, la temperatura, la conductividad ni la turbidez; los autores señalan cambios en la demanda de cloro como posible causa [11]. En Uganda, siete dispositivos sin electricidad se compararon por consistencia de dosis y solo uno, el clorador en T, alcanzó la dosis correcta con probabilidad de 90 % [12]. El patrón se repite: el dispositivo funciona cuando su dosis se ajusta a la fuente, y falla cuando no. Otros estudios aportan el contexto de adopción y costo [13]–[20].

*Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.

*Tabla 1. Desempeño de la dosificación reportado por estudios de cloración pasiva o en línea

*Fuente: elaboración propia a partir de los resúmenes de las referencias citadas.

## Objetivo y aporte

El objetivo es responder una pregunta previa a cualquier prueba de campo: con los supuestos del propio proyecto, ¿cuánta dosis necesita el clorificador de PVC para dejar entre 0,2 y 0,5 mg/L, y la entrega el diseño? El aporte es un balance de masa que enlaza la geometría del dispositivo con la demanda del agua, una simulación que cuantifica el desajuste y un criterio de diseño verificable: medir la demanda antes de calibrar.

# Métodos

## Dispositivo

El clorificador se construye con tubería y accesorios de PVC a presión de 1 y 2 pulgadas y funciona por gravedad con una carga de 1,5 a 5,0 m. Una Tee de 1 pulgada divide el caudal en un ramal de derivación con una válvula de bola y un ramal que pasa por una cámara de 2 pulgadas y 0,50 m con pastillas de tricloro al 90 %, con válvulas de entrada y de salida; una segunda Tee recombina las corrientes (Figura 2). El caudal de diseño es de 0,2 a 2,5 L/s. Los materiales suman 159.991 COP según el presupuesto del proyecto. La apertura relativa de las tres válvulas fija la fracción que pasa por la cámara.

*Figura 2. Esquema del clorificador pasivo con derivación (Q_cámara = α·Q_total).

## Balance de masa

El caudal total se reparte entre derivación y cámara, y la fracción que pasa por la cámara es alpha:

La disolución de la pastilla sigue una ley de transferencia de masa tipo Noyes–Whitney, con coeficiente k_m, área expuesta A_s y solubilidad de saturación C_sat. La concentración en la cámara y, al recombinar con agua sin cloro, la concentración en la mezcla son:

El cloro residual libre resulta de restar la demanda D y de aplicar el decaimiento de primer orden, con constante k y tiempo de contacto t, y los factores de temperatura, pH, turbidez y caudal que calibró el equipo en su simulación:

con f_T=e^0,03(T-25), f_pH=1+0,06 |pH-7,2|, f_tu=1+0,15 NTU y f_Q=1+0,08 (Q-1). Estos factores son del modelo del proyecto y no están ajustados a mediciones; la dependencia de la cinética con la temperatura y la composición del agua es conocida [21]. Si se quiere un residual objetivo C^* y se llama Φ=e^ktf_Tf_pHf_tuf_Q al factor de pérdida, la mezcla debe entregar al menos:

## Simulación

Se reprodujo el cuaderno Monte Carlo del proyecto con la misma semilla (42) y 1.000 escenarios. Las distribuciones son supuestos del equipo: caudal normal de media 1,0 L/s; tiempo de contacto de 20 min; cloro en cámara de 1,2 mg/L; demanda de 0,65 mg/L; fracción derivada beta(2,5; 5,5); constante de decaimiento de 0,035 por minuto; temperatura de 28 °C; pH de 7,2 y turbidez gamma. La reproducción coincidió con el archivo del cuaderno (diferencia máxima 0,0). El rango objetivo es de 0,2 a 0,5 mg/L, con meta de 0,4. Los intervalos de proporciones son de Wilson [22]. Para el mapa de cumplimiento se multiplicó la dosis efectiva por una escala de 0,5 a 6 y se varió la demanda media de 0,05 a 1,0 mg/L, con 20.000 escenarios por celda.

## Búsqueda bibliográfica

La búsqueda se hizo en OpenAlex el 6 de noviembre de 2026 con la ecuación guardada en prisma_cifras.json, en título y resumen, artículos de 2020 a 2026 en inglés o español con DOI. El cribado exigió que el título tratara de cloración; la elegibilidad se evaluó sobre título y resumen con tres criterios (agua de consumo, dispositivo pasivo o dosificador, contexto de bajos recursos). El flujo sigue la guía PRISMA 2020 [23] y se muestra en la Figura 1. No es una revisión sistemática completa: la lectura de texto completo queda pendiente.

# Resultados

## Qué dosis necesita el diseño

Con los valores medios supuestos, el factor de pérdida es Φapprox 2,64. Para dejar 0,4 mg/L con una demanda de 0,65 mg/L, la mezcla debe entregar C_s^mínapprox 1,71 mg/L, según la ecuación (5). La dosis efectiva media del modelo es C_0alpha=0,39 mg/L, es decir, 4,4 veces menos. La dosis efectiva supera a la demanda en solo 16,2 % de los escenarios.

La concentración que debe tener la cámara depende de cuánta agua pasa por ella. Con la mezcla requerida, una fracción alpha=0,2 exige una cámara de 8,5 mg/L y alpha=0,5, de 3,4 mg/L (Tabla 2). Con una cámara que apenas disuelva 1,2 mg/L, como supone la simulación, ninguna fracción razonable alcanza la mezcla requerida.

*Tabla 2. Concentración de cámara necesaria según la fracción derivada

*Fuente: cálculo propio con la ecuación (5) y los valores medios supuestos; la tercera columna usa D = 0.

## Cumplimiento simulado

De los 1.000 escenarios, 990 (99,0 %; IC 95 %: 98,2 a 99,5 %) quedaron por debajo de 0,2 mg/L, 10 (1,0 %; IC 95 %: 0,5 a 1,8 %) en el rango y ninguno por encima. El residual medio fue de 0,011 mg/L, el máximo de 0,30 mg/L y 838 escenarios dieron 0,00 (Figura 3). Solo 1 escenario alcanzó 0,3 mg/L, el mínimo de la Resolución 2115.

*Figura 3. Distribución del cloro residual simulado (n = 1000) y rango objetivo.

## Mapa de cumplimiento

Al barrer la escala de la dosis y la demanda media (Figura 4), el máximo de cumplimiento fue de 44,6 %, con una demanda de 0,05 mg/L y una dosis 2,75 veces la del cuaderno. Ninguna de las 460 celdas llegó a 90 %. Aun con demanda casi nula, la variabilidad de la fracción derivada y del cloro de cámara impide que el residual caiga de forma sostenida dentro de un rango de 0,3 mg/L de ancho.

*Figura 4. Escenarios dentro de 0,2–0,5 mg/L según la escala de la dosis y la demanda media; la estrella marca los supuestos del cuaderno.

# Discusión

El resultado central no es que el dispositivo falle, sino que el diseño no puede juzgarse sin conocer la demanda. Con los supuestos del equipo, la dosis queda a una fracción de lo necesario, y subirla lo suficiente exige una cámara muy concentrada que una pastilla en erosión pasiva difícilmente sostiene. Esto coincide con la experiencia de campo: en Ghana las fluctuaciones del cloro no se explicaron por las variables fisicoquímicas medidas y se atribuyeron a cambios en la demanda [11]; en Guatemala, un dispositivo barato mejoró la calidad microbiológica pero dosificó poco [10]; y en Uganda el dispositivo que acertó con mayor frecuencia fue el de mejor diseño hidráulico [12].

Hay una consecuencia práctica. La Resolución 2115 ya pide que la dosis salga de pruebas de demanda [1], y el protocolo del proyecto mide cloro por DPD pero no define una prueba de demanda previa. Incorporarla, aunque sea con una dosis de ensayo en un recipiente, convierte la calibración de las válvulas en un procedimiento y no en un tanteo. Además, la presencia de partículas y materia orgánica en un agua de pozo o de río debería justificar una etapa previa de reducción de turbidez, algo que las guías recomiendan para que la desinfección sea eficaz [2].

Hay tres límites. Primero, las distribuciones, en particular la demanda de 0,65 mg/L y el cloro de cámara de 1,2 mg/L, son supuestos sin medición; si la demanda real fuera de 0,1 a 0,2 mg/L, el cuadro cambiaría. Segundo, el repositorio incluye un formato de captura con diez registros fechados en septiembre de 2026, cinco de ellos con cloro y cuatro dentro del rango, cuya procedencia no pudo confirmarse; no se usaron como resultado, pero su contraste con la simulación indica que los supuestos de demanda y de cámara deben recalibrarse con mediciones. Tercero, el rango de diseño del proyecto (0,2–0,5 mg/L) es más estrecho que el de la norma (0,3–2,0 mg/L) y su límite inferior queda por debajo del mínimo normativo; un diseño que apunte al valor legal tendría más margen.

# Conclusiones

Con los supuestos actuales, el clorificador de PVC no alcanza el rango objetivo: 1,0 % de los escenarios simulados cumple y la dosis efectiva media es 4,4 veces inferior a la requerida. El balance de masa permite decir cuánto falta y por qué, y lo hace sin ensayos costosos. La condición para avanzar es medir la demanda de cloro del agua de El Vidrial y la tasa real de disolución de la pastilla. El prototipo está en TRL 3: concepto y modelo analítico, sin validación experimental.

# Recomendaciones

(1) Medir la demanda de cloro de cada fuente antes de calibrar. (2) Determinar la tasa de disolución de la pastilla con el protocolo de aforo y DPD ya redactado. (3) Evaluar un pretratamiento de turbidez. (4) Reconsiderar el rango objetivo frente al 0,3–2,0 mg/L de la norma. (5) Recalibrar el modelo con los datos del diseño factorial 2³ antes de cualquier prueba en la vereda.

## Contribución de los autores

Contribución de los autores (taxonomía CRediT; por confirmar por el equipo antes del envío): la primera autora concibió el planteamiento del balance de masa, ejecutó la simulación y redactó el borrador; los demás autores aportaron en la curación de datos, la verificación de la bibliografía y la revisión; Cristian Javier Cano-Mogollón supervisó el trabajo y revisó el manuscrito.

## Declaraciones finales

[Heading 3] Financiación

El presupuesto del proyecto prevé que el semillero SILOGE cubra los insumos de laboratorio (160.000 COP). [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

Los autores declaran que no existen conflictos de intereses. [Por confirmar por el equipo.]

[Heading 3] Consentimiento informado y ética

No aplica: el estudio no incluyó personas. La encuesta comunitaria prevista requerirá consentimiento informado.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

Los scripts de simulación, la búsqueda bibliográfica y las salidas numéricas están en la carpeta de evidencia del proyecto (estudio_clorificador.py, complemento.py, busqueda_prisma.py, resultados_estudio.json, prisma_cifras.json, verificacion_referencias.csv). El repositorio público está por definir. 

[Heading 3] Uso de herramientas de inteligencia artificial

Un asistente de inteligencia artificial (Claude, de Anthropic) apoyó la ejecución de los análisis, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y responden por el texto y por los resultados.

**Declarations (English)

Author Contributions: the first author conceived the mass-balance approach, ran the simulation and drafted the manuscript; the other authors contributed to data curation, literature verification and review; C. J. Cano-Mogollón supervised and reviewed. Funding: laboratory supplies are budgeted by the SILOGE seed group. No conflicts of interest. Informed consent and ethics approval: not applicable. Data and code: shared evidence folder of the project.

# References

[1] Ministerio de la Protección Social y Ministerio de Ambiente, Vivienda y Desarrollo Territorial, “Resolución 2115 de 2007, por medio de la cual se señalan características, instrumentos básicos y frecuencias del sistema de control y vigilancia para la calidad del agua para consumo humano,” Bogotá, Colombia, 2007. [Online]. Available: https://normograma.invima.gov.co/normograma/compilacion/docs/resolucion_minproteccion_2115_2007.htm. Accessed: Nov. 6, 2026.

[2] World Health Organization, Guidelines for Drinking-water Quality: Fourth Edition Incorporating the First and Second Addenda. Geneva, Switzerland: WHO, 2022. [Online]. Available: https://www.who.int/publications/i/item/9789240045064. Accessed: Nov. 6, 2026.

[3] J. Wolf et al., “Burden of disease attributable to unsafe drinking water, sanitation, and hygiene in domestic settings: a global analysis for selected adverse health outcomes,” The Lancet, vol. 401, no. 10393, pp. 2060-2071, 2023, doi: 10.1016/S0140-6736(23)00458-0.

[4] B. F. Arnold and J. M. Colford, “TREATING WATER WITH CHLORINE AT POINT-OF-USE TO IMPROVE WATER QUALITY AND REDUCE CHILD DIARRHEA IN DEVELOPING COUNTRIES: A SYSTEMATIC REVIEW AND META-ANALYSIS,” The American Journal of Tropical Medicine and Hygiene, vol. 76, no. 2, pp. 354-364, 2007, doi: 10.4269/ajtmh.2007.76.354.

[5] T. F. Clasen et al., “Interventions to improve water quality for preventing diarrhoea,” Cochrane Database of Systematic Reviews, vol. 2015, no. 10, 2015, doi: 10.1002/14651858.CD004794.pub3.

[6] A. J. Pickering et al., “Effect of in-line drinking water chlorination at the point of collection on child diarrhoea in urban Bangladesh: a double-blind, cluster-randomised controlled trial,” The Lancet Global Health, vol. 7, no. 9, pp. e1247-e1256, 2019, doi: 10.1016/S2214-109X(19)30315-8.

[7] S. Amrose, Z. Burt, and I. Ray, “Safe Drinking Water for Low-Income Regions,” Annual Review of Environment and Resources, vol. 40, no. 1, pp. 203-231, 2015, doi: 10.1146/annurev-environ-031411-091819.

[8] K. Cherukumilli, R. Bain, Y. Chen, and A. J. Pickering, “Estimating the Global Target Market for Passive Chlorination,” Environmental Science & Technology Letters, vol. 10, no. 1, pp. 105-110, 2022, doi: 10.1021/acs.estlett.2c00781.

[9] Y. S. Crider et al., “Evaluation of System-Level, Passive Chlorination in Gravity-Fed Piped Water Systems in Rural Nepal,” Environmental Science & Technology, vol. 56, no. 19, pp. 13985-13995, 2022, doi: 10.1021/acs.est.2c03133.

[10] J. M. Locher et al., “Assessment of a local and low-cost passive in-line chlorination device in rural Guatemala,” PLOS Water, vol. 3, no. 9, art. e0000255, 2024, doi: 10.1371/journal.pwat.0000255.

[11] C. Delaire et al., “Comparison of passive and manual chlorination in small piped water networks in rural Ghana: Technical performance, ease-of-use, and cost,” PLOS Water, vol. 3, no. 10, art. e0000295, 2024, doi: 10.1371/journal.pwat.0000295.

[12] L. D. Lukas Dössegger et al., “Assessment of low-cost, non-electrically powered chlorination devices for gravity-driven membrane water kiosks in eastern Uganda,” Waterlines, vol. 40, no. 2, pp. 92-106, 2021, doi: 10.3362/1756-3488.20-00014.

[13] J. E. Powers et al., “Design, performance, and demand for a novel in-line chlorine doser to increase safe water access,” npj Clean Water, vol. 4, no. 1, art. 4, 2021, doi: 10.1038/s41545-020-00091-1.

[14] D. W. Smith et al., “Effective Demand for In-Line Chlorination Bundled with Rental Housing in Dhaka, Bangladesh,” Environmental Science & Technology, vol. 55, no. 18, pp. 12471-12482, 2021, doi: 10.1021/acs.est.1c01308.

[15] M. Lindmark, W. Meier, D. Calix, and C. Just, “Performance of Community Water Board-Managed Passive In-Line Chlorinators Supported by a Circuit Rider Program in Rural Honduras,” ACS ES&T Water, vol. 3, no. 12, pp. 4011-4019, 2023, doi: 10.1021/acsestwater.3c00425.

[16] I. Evance et al., “Assessing factors affecting the use of chlorine dispensers for household water treatment in rural Kenya, Malawi, and Uganda,” Journal of Water, Sanitation and Hygiene for Development, vol. 15, no. 1, pp. 84-94, 2024, doi: 10.2166/washdev.2024.407.

[17] J. Lowe et al., “In-line chlorination for drinking water in rural Odisha, India: A randomized controlled implementation trial,” PLOS Water, vol. 5, no. 4, art. e0000440, 2026, doi: 10.1371/journal.pwat.0000440.

[18] R. Meierhofer et al., “Water quality at the point of consumption and child health after installing in-line chlorination with electrolysis in Ethiopia,” PLOS Water, vol. 5, no. 7, art. e0000575, 2026, doi: 10.1371/journal.pwat.0000575.

[19] L. E. Voth-Gaeddert and A. Schranck, “Inline Chlorinator for Potable Water Systems in Low-Resource Settings,” Journal of Environmental Engineering, vol. 147, no. 7, art. 06021003, 2021, doi: 10.1061/(asce)ee.1943-7870.0001883.

[20] L. E. Voth-Gaeddert, M. Lemley, K. Brathwaite, A. Schranck, and S. Libbey, “Design and Evaluation of a Household Chlorination System for Treating Cistern Water in the US Virgin Islands,” Journal of Environmental Engineering, vol. 148, no. 11, art. 06022002, 2022, doi: 10.1061/(asce)ee.1943-7870.0002063.

[21] J. C. Powell, N. B. Hallam, J. R. West, C. F. Forster, and J. Simms, “Factors which control bulk chlorine decay rates,” Water Research, vol. 34, no. 1, pp. 117-126, 2000, doi: 10.1016/S0043-1354(99)00097-4.

[22] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[23] M. J. Page et al., “The PRISMA 2020 statement: an updated guideline for reporting systematic reviews,” BMJ, art. n71, 2021, doi: 10.1136/bmj.n71.

---
## Guion de defensa

**¿Por qué dices que el diseño no cumple si no hay mediciones?**  
No digo que el diseño falle en la realidad. Digo que, con los supuestos del propio proyecto (demanda 0,65 mg/L, cámara de 1,2 mg/L), el balance de masa da una dosis efectiva de 0,39 mg/L frente a 1,71 requeridos. La conclusión es condicional y por eso el aporte es el criterio: medir la demanda.

**¿Qué es Φ y de dónde sale?**  
Es el factor que junta el decaimiento (e^kt) y los factores de temperatura, pH, turbidez y caudal del modelo del proyecto. Con k = 0,035/min, t = 20 min, T = 28 °C y turbidez media 1,32 NTU, vale 2,64.

**¿Por qué la norma dice 0,3–2,0 y el proyecto 0,2–0,5?**  
La Resolución 2115 (art. 9) fija 0,3–2,0 mg/L en la red; 0,2–0,5 es el rango propio del diseño. Su límite inferior queda por debajo del mínimo legal: lo señalamos como limitación.

**¿Cómo se hizo la búsqueda y cuántos artículos leyeron?**  
Búsqueda reproducible en OpenAlex con ecuación guardada; cribado por título y evaluación por título y resumen. La lectura de texto completo de los 13 incluidos es una tarea pendiente que debes hacer antes de defender.

**¿Qué sigue?**  
Medir demanda de cloro por fuente, medir la tasa de disolución de la pastilla y ejecutar el factorial 2³ ya diseñado.
