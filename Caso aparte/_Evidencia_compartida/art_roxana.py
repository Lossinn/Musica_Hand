"""Artículo — primera autora: Roxana Elena Muñoz Rodiño. Hilo: la demanda de cloro como restricción de diseño (balance de masa)."""
import math, sys
from nucleo import *

b = R["base"]; mp = R["mapa_resumen"]; pr = PR
phi = math.exp(0.035 * 20) * math.exp(0.03 * 3) * (1 + 0.15 * 1.32)
req = (0.65 + 0.4 * phi)          # mg/L requeridos en la mezcla para dejar 0,4 mg/L con los valores medios supuestos
N = m(R["reproduccion"]["N"])

TITULO_ES = ("Balance de masa y demanda de cloro en un clorificador pasivo por derivación en PVC: simulación de cumplimiento "
             "para una vereda rural de Montería, Córdoba")
TITULO_EN = ("Mass balance and chlorine demand in a passive PVC bypass chlorinator: compliance simulation for a rural "
             "community in Montería, Córdoba")
RES_ES = ("El Vidrial, vereda rural de Montería, no cuenta con una desinfección continua y verificable del agua que consume. Se presenta el "
          "diseño de un clorificador pasivo de PVC que divide el caudal, hace pasar una fracción por una cámara con pastillas de tricloro al 90 % "
          "y recombina las corrientes, con un costo de materiales de 159.991 COP. El objetivo fue establecer, con un balance de masa, cuánta dosis "
          "necesita el dispositivo para dejar entre 0,2 y 0,5 mg/L de cloro libre y comprobar si el diseño la entrega bajo los supuestos del "
          f"equipo. Se simularon {N} escenarios de Monte Carlo con caudal, temperatura, pH, turbidez, demanda y fracción derivada "
          f"variables. La dosis efectiva media fue de {f(b['dosis_efectiva_media'], 2)} mg/L frente a una demanda media supuesta de {f(b['demanda_media'], 2)} mg/L; "
          f"solo {f(b['adecuada'] / 10, 1)} % de los escenarios quedó en el rango (IC 95 %: {f(b['ic_adecuada'][0], 1)} a {f(b['ic_adecuada'][1], 1)} %) y "
          f"{f(b['sub'] / 10, 1)} % quedó por debajo. Un mapa de cumplimiento mostró que bajar la demanda o subir la dosis no basta por sí solo: el máximo "
          f"fue de {f(mp['max_cumplimiento_pct'], 1)} %. Se concluye que la demanda de cloro debe medirse antes de calibrar el dispositivo, como lo exige la "
          "Resolución 2115 de 2007. No hay validación experimental: las distribuciones son supuestos del equipo y el nivel de madurez es TRL 3.")
RES_EN = ("El Vidrial, a rural community in Montería, lacks continuous and verifiable drinking-water disinfection. This paper presents a passive PVC "
          "chlorinator that splits the flow, sends a fraction through a chamber with 90 % trichloroisocyanuric acid tablets and recombines the streams, "
          "at a materials cost of 159,991 COP. The aim was to establish, through a mass balance, how much dose the device needs to leave 0.2 to 0.5 mg/L "
          f"of free chlorine and to test whether the design delivers it under the team's assumptions. {N} Monte Carlo scenarios were "
          "simulated with variable flow, temperature, pH, turbidity, chlorine demand and bypass fraction. The mean effective dose was "
          f"{f(b['dosis_efectiva_media'], 2)} mg/L against an assumed mean demand of {f(b['demanda_media'], 2)} mg/L; only {f(b['adecuada'] / 10, 1)} % of scenarios fell inside the "
          f"range (95 % CI {f(b['ic_adecuada'][0], 1)} to {f(b['ic_adecuada'][1], 1)} %) and {f(b['sub'] / 10, 1)} % fell below it. A compliance map showed that neither lowering the demand "
          f"nor raising the dose is enough on its own: the maximum was {f(mp['max_cumplimiento_pct'], 1)} %. Chlorine demand should be measured before the device is "
          "calibrated, as Colombian regulation requires. There is no experimental validation: the distributions are team assumptions and the readiness level is TRL 3.")
KW_ES = "desinfección del agua; cloración pasiva; demanda de cloro; balance de masa; simulación Monte Carlo; agua rural; Montería"
KW_EN = "water disinfection; passive chlorination; chlorine demand; mass balance; Monte Carlo simulation; rural water; Montería"

autores = encabezado("Muñoz", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

# ------------------------------------------------------------------ 1. Introducción
H1("Introducción")
H2("El problema de dosificar sin conocer la demanda")
T("Desinfectar con cloro parece una operación sencilla: se agrega una cantidad de producto y se espera. En la práctica, el cloro que se agrega "
  "se reparte entre lo que oxida la materia orgánica y los metales disueltos, lo que decae con el tiempo y la temperatura, y lo que queda como "
  "residual libre, que es lo único que protege el agua después. Si la dosis no supera la demanda, el residual es cero aunque se haya "
  "vertido producto. La Resolución 2115 de 2007 pide que el cloro residual libre esté entre 0,3 y 2,0 mg/L en cualquier punto de la red y "
  "dice, además, que la dosis debe resultar de pruebas frecuentes de demanda {c:res2115}. Las guías de la Organización Mundial de la Salud "
  "van en la misma dirección {c:oms}. Un dispositivo que no parte de la demanda del agua que trata está calibrado a ciegas.")
T("El Vidrial es una vereda rural de Montería, Córdoba, cuyas familias, según la caracterización preliminar del proyecto, usan fuentes de agua "
  "sin tratamiento adecuado o métodos informales de potabilización. El contexto no es excepcional: la carga de enfermedad atribuible al agua "
  "insegura y al saneamiento deficiente sigue siendo alta {c:wolf}, y revisiones y ensayos muestran que clorar en el punto de uso o de recolección "
  "reduce la diarrea infantil {c:arnold,clasen,pickering}. Entre las opciones de bajo costo, la cloración pasiva, es decir, la que no requiere "
  "electricidad ni una acción diaria del usuario, se considera una vía para ampliar el acceso {c:amrose,mercado}.")
H2("Qué muestra la literatura reciente")
T("Se hizo una búsqueda reproducible en OpenAlex (sección 2.4). De " + m(pr["identificados_total"]) + " registros se retuvieron " + str(pr["incluidos_busqueda"]) +
  " estudios sobre cloración pasiva, en línea o con dosificadores en contextos de bajos recursos (Figura 1). Sus resultados dependen mucho de qué tan "
  "bien se ajusta la dosis a las condiciones locales. En seis sistemas de agua por gravedad de Nepal, la cloración pasiva bajó la presencia de "
  "E. coli en los grifos de más de 80 % a 7 % en un año {c:nepal}. En Guatemala, un clorador local de bajo costo redujo la contaminación fecal, "
  "pero solo 24 % de las muestras de grifo alcanzó el mínimo de 0,2 mg/L {c:guatemala}. En Ghana, el cloro libre estuvo en el rango de 0,2 a 2,0 mg/L en "
  "86 % de las mediciones con el método pasivo y en 71 % con el manual, y las fluctuaciones observadas no quedaron explicadas por el pH, la "
  "temperatura, la conductividad ni la turbidez; los autores señalan cambios en la demanda de cloro como posible causa {c:ghana}. En Uganda, siete "
  "dispositivos sin electricidad se compararon por consistencia de dosis y solo uno, el clorador en T, alcanzó la dosis correcta con probabilidad de 90 % "
  "{c:uganda}. El patrón se repite: el dispositivo funciona cuando su dosis se ajusta a la fuente, y falla cuando no. Otros estudios aportan el contexto de "
  "adopción y costo {c:venturi,dhaka,honduras,kmu,odisha,etiopia,aquatabs,usvi}.")
figura(["prisma.png"], 9.5, "Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.")
tabla("Tabla 1. Desempeño de la dosificación reportado por estudios de cloración pasiva o en línea",
      ["Contexto", "Refs.", "Medida reportada", "Lectura para este diseño"],
      [["Guatemala, clorador local", cita("guatemala"), "24 % de grifos con al menos 0,2 mg/L", "Un diseño barato puede reducir E. coli y aun así dosificar poco"],
       ["Ghana, pasivo y manual", cita("ghana"), "86 % y 71 % en 0,2–2,0 mg/L", "Las fluctuaciones apuntan a la demanda cambiante"],
       ["Uganda, siete dispositivos", cita("uganda"), "Dosis correcta: 90 % (en T) a 40 % (balde)", "La consistencia depende del diseño hidráulico"],
       ["Honduras, juntas de agua", cita("honduras"), "77 % de muestras con al menos 0,2 mg/L", "El apoyo técnico explica gran parte de los aciertos"],
       ["Nepal, sistemas por gravedad", cita("nepal"), "E. coli en grifos: de más de 80 % a 7 %", "Cloro a 0,06–0,09 USD por m³ tratado"]],
      "Fuente: elaboración propia a partir de los resúmenes de las referencias citadas.", [3.6, 2.2, 5.2, 5.6])
H2("Objetivo y aporte")
T("El objetivo es responder una pregunta previa a cualquier prueba de campo: con los supuestos del propio proyecto, ¿cuánta dosis necesita el clorificador "
  "de PVC para dejar entre 0,2 y 0,5 mg/L, y la entrega el diseño? El aporte es un balance de masa que enlaza la geometría del dispositivo con la "
  "demanda del agua, una simulación que cuantifica el desajuste y un criterio de diseño verificable: medir la demanda antes de calibrar.")

# ------------------------------------------------------------------ 2. Métodos
H1("Métodos")
H2("Dispositivo")
T("El clorificador se construye con tubería y accesorios de PVC a presión de 1 y 2 pulgadas y funciona por gravedad con una carga de 1,5 a 5,0 m. Una "
  "Tee de 1 pulgada divide el caudal en un ramal de derivación con una válvula de bola y un ramal que pasa por una cámara de 2 pulgadas y 0,50 m con "
  "pastillas de tricloro al 90 %, con válvulas de entrada y de salida; una segunda Tee recombina las corrientes (Figura 2). El caudal de diseño es de 0,2 a "
  "2,5 L/s. Los materiales suman 159.991 COP según el presupuesto del proyecto. La apertura relativa de las tres válvulas fija la fracción que pasa por la cámara.")
figura(["esquema.png"], 14.5, "Figura 2. Esquema del clorificador pasivo con derivación (Q_cámara = α·Q_total).")
H2("Balance de masa")
T("El caudal total se reparte entre derivación y cámara, y la fracción que pasa por la cámara es $\\alpha$:")
ecuacion("div", r"Q_t=Q_b+Q_c,\qquad \alpha=\frac{Q_c}{Q_t}")
T("La disolución de la pastilla sigue una ley de transferencia de masa tipo Noyes–Whitney, con coeficiente $k_m$, área expuesta $A_s$ y solubilidad de "
  "saturación $C_{sat}$. La concentración en la cámara y, al recombinar con agua sin cloro, la concentración en la mezcla son:")
ecuacion("cam", r"C_c=\frac{k_m A_s C_{sat}}{Q_c+k_m A_s}")
ecuacion("mez", r"C_s=\alpha\,C_c")
T("El cloro residual libre resulta de restar la demanda $D$ y de aplicar el decaimiento de primer orden, con constante $k$ y tiempo de contacto $t$, y "
  "los factores de temperatura, pH, turbidez y caudal que calibró el equipo en su simulación:")
ecuacion("res", r"C_r=\max\!\left(\frac{(C_s-D)\,e^{-kt}}{f_T\,f_{pH}\,f_{tu}\,f_Q},\,0\right)")
T("con $f_T=e^{0{,}03(T-25)}$, $f_{pH}=1+0{,}06\\,|pH-7{,}2|$, $f_{tu}=1+0{,}15\\,\\mathrm{NTU}$ y $f_Q=1+0{,}08\\,(Q-1)$. Estos factores son del modelo del "
  "proyecto y no están ajustados a mediciones; la dependencia de la cinética con la temperatura y la composición del agua es conocida {c:powell}. "
  "Si se quiere un residual objetivo $C^{*}$ y se llama $\\Phi=e^{kt}f_Tf_{pH}f_{tu}f_Q$ al factor de pérdida, la mezcla debe entregar al menos:")
ecuacion("req", r"C_s^{\min}=D+C^{*}\,\Phi")
H2("Simulación")
T("Se reprodujo el cuaderno Monte Carlo del proyecto con la misma semilla (42) y " + N + " escenarios. Las distribuciones son supuestos del equipo: "
  "caudal normal de media 1,0 L/s; tiempo de contacto de 20 min; cloro en cámara de 1,2 mg/L; demanda de 0,65 mg/L; fracción derivada beta(2,5; 5,5); constante de "
  "decaimiento de 0,035 por minuto; temperatura de 28 °C; pH de 7,2 y turbidez gamma. La reproducción coincidió con el archivo del cuaderno (diferencia máxima "
  f"{f(R['reproduccion']['max_diferencia_vs_csv_del_notebook'], 1)}). El rango objetivo es de 0,2 a 0,5 mg/L, con meta de 0,4. Los intervalos de proporciones son de Wilson {{c:wilson}}. "
  "Para el mapa de cumplimiento se multiplicó la dosis efectiva por una escala de 0,5 a 6 y se varió la demanda media de 0,05 a 1,0 mg/L, con 20.000 escenarios por celda.")
H2("Búsqueda bibliográfica")
T("La búsqueda se hizo en OpenAlex el 6 de noviembre de 2026 con la ecuación guardada en prisma_cifras.json, en título y resumen, artículos de 2020 a 2026 en "
  "inglés o español con DOI. El cribado exigió que el título tratara de cloración; la elegibilidad se evaluó sobre título y resumen con tres criterios (agua de consumo, "
  "dispositivo pasivo o dosificador, contexto de bajos recursos). El flujo sigue la guía PRISMA 2020 {c:prisma} y se muestra en la Figura 1. No es una revisión sistemática "
  "completa: la lectura de texto completo queda pendiente.")

# ------------------------------------------------------------------ 3. Resultados
H1("Resultados")
H2("Qué dosis necesita el diseño")
T(f"Con los valores medios supuestos, el factor de pérdida es $\\Phi\\approx {f(phi, 2)}$. Para dejar 0,4 mg/L con una demanda de 0,65 mg/L, la mezcla debe entregar "
  f"$C_s^{{\\min}}\\approx {f(req, 2)}$ mg/L, según la ecuación {{E_REQ}}. La dosis efectiva media del modelo es $C_0\\alpha={f(b['dosis_efectiva_media'], 2)}$ mg/L, es decir, "
  f"{f(req / b['dosis_efectiva_media'], 1)} veces menos. La dosis efectiva supera a la demanda en solo {f(100 * b['p_dosis_mayor_demanda'], 1)} % de los escenarios.")
T("La concentración que debe tener la cámara depende de cuánta agua pasa por ella. Con la mezcla requerida, una fracción $\\alpha=0{,}2$ exige una cámara de "
  f"{f(req / 0.2, 1)} mg/L y $\\alpha=0{{,}}5$, de {f(req / 0.5, 1)} mg/L (Tabla 2). Con una cámara que apenas disuelva 1,2 mg/L, como supone la simulación, ninguna fracción razonable alcanza la mezcla requerida.")
tabla("Tabla 2. Concentración de cámara necesaria según la fracción derivada",
      ["Fracción α", "Cámara para dejar 0,4 mg/L (mg/L)", "Cámara si no hubiera demanda (mg/L)"],
      [[f(a, 2), f(req / a, 1), f(0.4 * phi / a, 1)] for a in (0.05, 0.1, 0.2, 0.3, 0.5)],
      "Fuente: cálculo propio con la ecuación (5) y los valores medios supuestos; la tercera columna usa D = 0.", [3.6, 6.0, 6.0])
H2("Cumplimiento simulado")
T(f"De los {N} escenarios, {b['sub']} ({f(b['sub'] / 10, 1)} %; IC 95 %: {f(b['ic_sub'][0], 1)} a {f(b['ic_sub'][1], 1)} %) quedaron por debajo de 0,2 mg/L, "
  f"{b['adecuada']} ({f(b['adecuada'] / 10, 1)} %; IC 95 %: {f(b['ic_adecuada'][0], 1)} a {f(b['ic_adecuada'][1], 1)} %) en el rango y ninguno por encima. El residual medio fue de "
  f"{f(b['media'], 3)} mg/L, el máximo de {f(b['max'], 2)} mg/L y {b['ceros']} escenarios dieron 0,00 (Figura 3). Solo {C['escenarios_ge_0_3']} escenario alcanzó 0,3 mg/L, el mínimo de la Resolución 2115.")
figura(["hist_cloro.png"], 8.0, "Figura 3. Distribución del cloro residual simulado (n = 1000) y rango objetivo.")
H2("Mapa de cumplimiento")
T(f"Al barrer la escala de la dosis y la demanda media (Figura 4), el máximo de cumplimiento fue de {f(mp['max_cumplimiento_pct'], 1)} %, con una demanda de {f(mp['en_demanda'], 2)} mg/L y una dosis "
  f"{f(mp['en_escala'], 2)} veces la del cuaderno. Ninguna de las {mp['celdas_totales']} celdas llegó a 90 %. Aun con demanda casi nula, la variabilidad de la fracción derivada y del cloro de cámara impide "
  "que el residual caiga de forma sostenida dentro de un rango de 0,3 mg/L de ancho.")
figura(["mapa_cumplimiento.png"], 11.5, "Figura 4. Escenarios dentro de 0,2–0,5 mg/L según la escala de la dosis y la demanda media; la estrella marca los supuestos del cuaderno.")

# ------------------------------------------------------------------ 4. Discusión
H1("Discusión")
T("El resultado central no es que el dispositivo falle, sino que el diseño no puede juzgarse sin conocer la demanda. Con los supuestos del equipo, la dosis queda a una fracción de lo "
  "necesario, y subirla lo suficiente exige una cámara muy concentrada que una pastilla en erosión pasiva difícilmente sostiene. Esto coincide con la experiencia de campo: "
  "en Ghana las fluctuaciones del cloro no se explicaron por las variables fisicoquímicas medidas y se atribuyeron a cambios en la demanda {c:ghana}; en Guatemala, un dispositivo barato "
  "mejoró la calidad microbiológica pero dosificó poco {c:guatemala}; y en Uganda el dispositivo que acertó con mayor frecuencia fue el de mejor diseño hidráulico {c:uganda}.")
T("Hay una consecuencia práctica. La Resolución 2115 ya pide que la dosis salga de pruebas de demanda {c:res2115}, y el protocolo del proyecto mide cloro por DPD pero no define una prueba de "
  "demanda previa. Incorporarla, aunque sea con una dosis de ensayo en un recipiente, convierte la calibración de las válvulas en un procedimiento y no en un tanteo. Además, la presencia de "
  "partículas y materia orgánica en un agua de pozo o de río debería justificar una etapa previa de reducción de turbidez, algo que las guías recomiendan para que la desinfección sea eficaz {c:oms}.")
T("Hay tres límites. Primero, las distribuciones, en particular la demanda de 0,65 mg/L y el cloro de cámara de 1,2 mg/L, son supuestos sin medición; si la demanda real fuera de 0,1 a 0,2 mg/L, el "
  "cuadro cambiaría. Segundo, el repositorio incluye un formato de captura con diez registros fechados en septiembre de 2026, cinco de ellos con cloro y cuatro dentro del rango, cuya procedencia no pudo confirmarse; "
  "no se usaron como resultado, pero su contraste con la simulación indica que los supuestos de demanda y de cámara deben recalibrarse con mediciones. Tercero, el rango de diseño del proyecto (0,2–0,5 mg/L) es más "
  "estrecho que el de la norma (0,3–2,0 mg/L) y su límite inferior queda por debajo del mínimo normativo; un diseño que apunte al valor legal tendría más margen.")

# ------------------------------------------------------------------ 5. Conclusiones
H1("Conclusiones")
T("Con los supuestos actuales, el clorificador de PVC no alcanza el rango objetivo: " + f"{f(b['adecuada'] / 10, 1)} % de los escenarios simulados cumple y la dosis efectiva media es {f(req / b['dosis_efectiva_media'], 1)} veces inferior a la requerida. "
  "El balance de masa permite decir cuánto falta y por qué, y lo hace sin ensayos costosos. La condición para avanzar es medir la demanda de cloro del agua de El Vidrial y la tasa real de disolución de la pastilla. "
  "El prototipo está en TRL 3: concepto y modelo analítico, sin validación experimental.")
H1("Recomendaciones")
T("(1) Medir la demanda de cloro de cada fuente antes de calibrar. (2) Determinar la tasa de disolución de la pastilla con el protocolo de aforo y DPD ya redactado. (3) Evaluar un pretratamiento de turbidez. "
  "(4) Reconsiderar el rango objetivo frente al 0,3–2,0 mg/L de la norma. (5) Recalibrar el modelo con los datos del diseño factorial 2³ antes de cualquier prueba en la vereda.")
declaraciones(v=0)
cierre(autores, TITULO_ES, "Balance de masa y demanda de cloro en un clorificador pasivo de PVC", Path(sys.argv[1]))
Path(sys.argv[1]).with_suffix(".txt").write_text("\n\n".join(f"[{e}] {t}" for e, t in LOG), encoding="utf-8")
