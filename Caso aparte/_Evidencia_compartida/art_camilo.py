"""Artículo — primer autor: Camilo Esteban Alvarez Durán. Hilo: la variabilidad de la fracción dosificada limita el cumplimiento; el DOE 2^3 puede medirla."""
import sys
from nucleo import *

b = R["base"]; mp = R["mapa_resumen"]; vv = R["variabilidad_vs_dosis"]; rho = R["spearman_neto"]; pot = R["potencia_DOE"]
N = m(R["reproduccion"]["N"]); pr = PR
dif = vv["cumple_fraccion_fija_pct"] - vv["cumple_fraccion_variable_pct"]

TITULO_ES = ("Sensibilidad y robustez de un clorificador pasivo de PVC con derivación: simulación Monte Carlo y diseño factorial 2³ "
             "para su validación experimental")
TITULO_EN = ("Sensitivity and robustness of a passive PVC bypass chlorinator: Monte Carlo simulation and a 2³ factorial design "
             "for its experimental validation")
RES_ES = ("Los clorificadores pasivos prometen desinfectar sin electricidad, pero su desempeño real depende de qué tan estable sea la dosis que entregan. "
          "Este trabajo analiza la robustez de un clorificador de PVC con derivación, pensado para la vereda El Vidrial (Montería), y define cómo validarlo. "
          f"Con {N} escenarios de Monte Carlo y nueve variables de entrada se calculó la correlación de Spearman con el cloro neto y se evaluó cuánto del incumplimiento "
          f"se debe a la media de la dosis y cuánto a su variabilidad. Las variables dominantes fueron la fracción derivada (ρ = {f(rho['frac']['rho'], 2)}) y la demanda de cloro "
          f"(ρ = {f(rho['demanda']['rho'], 2)}); el caudal, el tiempo de contacto, la temperatura, el pH y la turbidez tuvieron |ρ| ≤ 0,03. En el mejor punto del mapa de cumplimiento, "
          f"fijar la fracción derivada en su media elevó el cumplimiento de {f(vv['cumple_fraccion_variable_pct'], 1)} % a {f(vv['cumple_fraccion_fija_pct'], 1)} %. "
          "Se propone un diseño factorial 2³ con tres réplicas (24 corridas aleatorizadas) que, con la desviación entre réplicas de 0,10 mg/L, detecta diferencias de "
          f"{f(pot[2]['delta_min_mgL'], 2)} mg/L con potencia de 80 %. No hay mediciones validadas: las distribuciones son supuestos y el nivel de madurez es TRL 3.")
RES_EN = ("Passive chlorinators promise to disinfect water without electricity, but their real performance depends on how stable the dose they deliver is. "
          "This paper analyses the robustness of a PVC bypass chlorinator designed for El Vidrial, a rural community in Montería, and defines how to validate it. "
          f"With {N} Monte Carlo scenarios and nine input variables, the Spearman correlation with net chlorine was computed and the share of non-compliance due to the mean "
          f"dose versus its variability was assessed. The dominant variables were the bypass fraction (ρ = {f(rho['frac']['rho'], 2)}) and chlorine demand (ρ = {f(rho['demanda']['rho'], 2)}); "
          f"flow, contact time, temperature, pH and turbidity had |ρ| ≤ 0.03. At the best point of the compliance map, fixing the bypass fraction at its mean raised compliance from "
          f"{f(vv['cumple_fraccion_variable_pct'], 1)} % to {f(vv['cumple_fraccion_fija_pct'], 1)} %. A 2³ factorial design with three replicates (24 randomized runs) is proposed that, with a replicate "
          f"standard deviation of 0.10 mg/L, detects differences of {f(pot[2]['delta_min_mgL'], 2)} mg/L with 80 % power. There are no validated measurements: the distributions are assumptions and the readiness level is TRL 3.")
KW_ES = "cloración pasiva; análisis de sensibilidad; simulación Monte Carlo; diseño de experimentos; robustez; agua rural; Montería"
KW_EN = "passive chlorination; sensitivity analysis; Monte Carlo simulation; design of experiments; robustness; rural water; Montería"

autores = encabezado("Alvarez", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

# ------------------------------------------------------------------ 1. Introducción
H1("Introducción")
H2("Más importante que la media es la estabilidad")
T("Un clorificador pasivo no tiene sensor ni lazo de control. Una vez calibrado, entrega la dosis que le permiten su hidráulica y su pastilla, y esa dosis cambia con el caudal, "
  "con la temperatura, con el desgaste del producto y con la posición de las válvulas. Por eso su desempeño no se resume en un promedio: lo que decide si el agua queda protegida "
  "es la proporción del tiempo en que el cloro residual libre permanece dentro de un rango estrecho. La Resolución 2115 de 2007 fija ese rango en 0,3 a 2,0 mg/L {c:res2115}, "
  "y la guía de la Organización Mundial de la Salud recomienda un residual que proteja frente a la recontaminación {c:oms}.")
T("Los estudios de campo muestran que la variabilidad es el problema real. Un clorador local de bajo costo instalado en Guatemala redujo la contaminación fecal, "
  "pero solo 24 % de las muestras de grifo alcanzó 0,2 mg/L {c:guatemala}. En Ghana, 685 mediciones en dos redes mostraron grandes fluctuaciones del cloro, en especial con el método pasivo, "
  "que el pH, la temperatura, la conductividad y la turbidez no explicaron del todo {c:ghana}. En Honduras, los problemas técnicos explicaron 26 % de los lapsos sin cloro, y los errores ocasionales y habituales "
  "de las juntas de agua, 24 y 15 % {c:honduras}. En ensayos de laboratorio con un dosificador comercial en línea, la presión no modificó el cloro residual, pero la posición "
  "del dispositivo sí {c:aquatabs}, y un sistema doméstico con clorador de piscina modificado tuvo desviaciones estándar de 0,5 a 0,8 mg/L {c:usvi}. Esa desviación es del tamaño de la ventana "
  "objetivo completa.")
H2("Lo que ya se sabe y lo que falta")
T("La búsqueda bibliográfica reproducible (sección 2.6, Figura 1) dejó " + str(pr["incluidos_busqueda"]) + " estudios sobre cloración pasiva o en línea en contextos de bajos recursos. Los "
  "ensayos y evaluaciones de campo informan cuánto baja la contaminación microbiológica {c:nepal,odisha,etiopia,pickering}, y los trabajos económicos, si hay demanda de pago por el servicio "
  "{c:dhaka,venturi}. El mercado potencial de estos dispositivos es enorme {c:mercado}, y la evidencia agregada indica que clorar reduce la diarrea infantil {c:arnold,clasen}, en un contexto de carga de enfermedad "
  "aún alta {c:wolf,amrose}. En los resúmenes revisados no se encontró una descomposición de cuánta variabilidad del cloro viene de cada fuente. Esa descomposición es la que permite decidir qué controlar. Algunos "
  "trabajos comparan dispositivos entre sí {c:uganda}; falta hacerlo con un diseño propio antes de construirlo en serie.")
figura(["prisma.png"], 9.5, "Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.")
H2("Objetivo")
T("El objetivo es doble: (i) identificar, con simulación, qué variables controlan el cloro residual del clorificador de PVC y cuánto pesa la variabilidad de la dosis frente a su media; y "
  "(ii) diseñar el experimento que permita validar esos hallazgos con una potencia estadística conocida de antemano.")

# ------------------------------------------------------------------ 2. Métodos
H1("Métodos")
H2("Dispositivo y variables controlables")
T("El clorificador usa tubería de PVC de 1 y 2 pulgadas. Una Tee divide el flujo; un ramal de derivación con válvula de bola lleva la fracción $1-\\alpha$ y el otro pasa por una cámara de 2 pulgadas de "
  "0,50 m con pastillas de tricloro al 90 % y válvulas de entrada y salida (Figura 2). Tres válvulas fijan la fracción $\\alpha$ de caudal que pasa por la cámara. El caudal de diseño es de 0,2 a 2,5 L/s con "
  "carga de 1,5 a 5,0 m. Las variables que el operador puede mover son la apertura de las válvulas y la carga de pastillas; el resto (caudal, temperatura, pH, turbidez, demanda) las impone la fuente.")
figura(["esquema.png"], 14.0, "Figura 2. Clorificador pasivo con derivación; las tres válvulas (V_bp, V_in, V_out) controlan la fracción α.")
H2("Modelo y simulación")
T("El residual libre se calcula con el balance de masa del proyecto, donde $C_c$ es el cloro de cámara, $\\alpha$ la fracción derivada, $D$ la demanda, $k$ el decaimiento, $t$ el tiempo de contacto y los $f$ "
  "factores de temperatura, pH, turbidez y caudal:")
ecuacion("res", r"C_r=\max\!\left(\frac{(\alpha\,C_c-D)\,e^{-kt}}{f_T\,f_{pH}\,f_{tu}\,f_Q},\,0\right)")
T("Se simularon " + N + " escenarios con la semilla 42 y las distribuciones del cuaderno del proyecto, que son supuestos y no mediciones: caudal normal (1,0; 0,25) L/s, tiempo de contacto normal (20; 4) min, "
  "cloro de cámara normal (1,2; 0,3) mg/L, demanda normal (0,65; 0,18) mg/L, fracción beta(2,5; 5,5), decaimiento normal (0,035; 0,010) por minuto, temperatura normal (28; 3) °C, pH normal (7,2; 0,4) y turbidez gamma(2,2; 0,6) NTU. "
  "La reproducción coincidió con el archivo original (diferencia máxima " + f(R['reproduccion']['max_diferencia_vs_csv_del_notebook'], 1) + ").")
H2("Análisis de sensibilidad y de variabilidad")
T("La sensibilidad se midió con la correlación de rangos de Spearman entre cada variable de entrada y el cloro neto $\\alpha C_c-D$, antes de recortar a cero, porque el residual recortado es continuo solo en "
  "una parte de los escenarios. Para separar la media de la variabilidad se buscó, en el mapa de cumplimiento (escala de dosis de 0,5 a 6 y demanda media de 0,05 a 1,0 mg/L, con 20.000 escenarios por celda), el punto con mayor "
  "cumplimiento y se repitió el cálculo con la fracción derivada fija en su media. Las proporciones llevan intervalos de Wilson {c:wilson}.")
H2("Diseño experimental propuesto")
T("El plan del proyecto es un factorial completo $2^3$ con tres réplicas, 24 corridas, y tres factores: caudal $A$ (0,5 y 1,5 L/s), apertura de la válvula de derivación $B$ (25 y 75 %) y carga de pastillas $C$ (una o dos). "
  "La respuesta es el cloro residual libre por DPD. Las 24 corridas se aleatorizaron con semilla 2026 (hoja de ejecución adjunta). El modelo de análisis de varianza es:")
ecuacion("anova", r"Y_{ijkl}=\mu+A_i+B_j+C_k+(AB)_{ij}+(AC)_{ik}+(BC)_{jk}+(ABC)_{ijk}+\varepsilon_{ijkl}")
T("Los supuestos se revisarían con Shapiro–Wilk y Levene. La potencia para un efecto principal con $N=24$ y 16 grados de libertad del error se obtuvo de la distribución F no central con parámetro $\\lambda=Nf^{2}$, "
  "donde $f$ es el tamaño de efecto de Cohen; la diferencia mínima detectable entre niveles es:")
ecuacion("delta", r"\delta_{\min}=2\,f\,\sigma,\qquad 1-\beta=1-F_{1,16,\lambda}\!\left(F_{0{,}95;1,16}\right)\ge 0{,}80")
H2("Auditoría de los registros existentes")
T("El repositorio contiene un formato de captura con diez registros de septiembre de 2026. Se verificó que el caudal calculado como volumen entre tiempo coincide con el registrado y que la categoría "
  "de cloración corresponde al rango definido. No se usaron como resultado porque su procedencia no pudo confirmarse.")
H2("Búsqueda bibliográfica")
T("La búsqueda en OpenAlex del 6 de noviembre de 2026 (ecuación en prisma_cifras.json) consideró artículos de 2020 a 2026 con DOI. El cribado exigió que el título tratara de cloración; la elegibilidad se evaluó sobre "
  "título y resumen. El flujo sigue PRISMA 2020 {c:prisma}. La lectura de texto completo queda pendiente.")

# ------------------------------------------------------------------ 3. Resultados
H1("Resultados")
H2("Qué variables controlan el cloro neto")
T(f"La Tabla 1 y la Figura 3 muestran que dos variables concentran la sensibilidad: la fracción derivada (ρ = {f(rho['frac']['rho'], 2)}) y la demanda (ρ = {f(rho['demanda']['rho'], 2)}), con una "
  f"contribución menor del cloro de cámara (ρ = {f(rho['C0']['rho'], 2)}). El caudal, el tiempo de contacto, la constante de decaimiento, la temperatura, el pH y la turbidez no superaron |ρ| = 0,03. "
  "Esto no significa que esas variables carezcan de efecto físico: en el modelo actúan como factores multiplicativos de pocos puntos porcentuales y tienen poca dispersión comparada con la de la dosis.")
nombres = {"frac": "Fracción derivada α", "demanda": "Demanda de cloro", "C0": "Cloro de cámara", "Q": "Caudal", "t": "Tiempo de contacto", "k": "Decaimiento", "T": "Temperatura", "pH": "pH", "turb": "Turbidez"}
filas = [[nombres[k], f(rho[k]["rho"], 2), "< 0,001" if rho[k]["p"] < 0.001 else f(rho[k]["p"], 2)] for k in sorted(rho, key=lambda x: -abs(rho[x]["rho"]))]
tabla("Tabla 1. Correlación de Spearman entre cada variable de entrada y el cloro neto (n = 1000)", ["Variable", "ρ", "Valor p"], filas,
      "Fuente: elaboración propia, estudio_clorificador.py.", [6.0, 3.0, 3.0])
figura(["spearman.png"], 8.0, "Figura 3. Correlación de Spearman con el cloro neto antes de recortar a cero.")
H2("Media frente a variabilidad")
T(f"En el cuaderno original, {f(b['sub'] / 10, 1)} % de los escenarios quedó por debajo de 0,2 mg/L y solo {f(b['adecuada'] / 10, 1)} % en el rango. En el mejor punto del mapa (Figura 4), con una demanda de "
  f"{f(mp['en_demanda'], 2)} mg/L y una dosis {f(mp['en_escala'], 2)} veces la del cuaderno, el cumplimiento fue de {f(mp['max_cumplimiento_pct'], 1)} %. Con la fracción derivada fija en su media y el resto sin cambios, "
  f"el cumplimiento subió a {f(vv['cumple_fraccion_fija_pct'], 1)} %: la variabilidad de la fracción, por sí sola, cuesta {f(dif, 1)} puntos porcentuales. Ninguna celda del mapa alcanzó 90 %.")
figura(["mapa_cumplimiento.png"], 11.0, "Figura 4. Cumplimiento simulado según la escala de la dosis y la demanda media; la estrella marca los supuestos del cuaderno.")
H2("Potencia del diseño 2³")
T("Con 24 corridas y 16 grados de libertad del error, la potencia de 80 % se alcanza con un tamaño de efecto $f=0{,}61$. Eso corresponde a las diferencias mínimas detectables de la Tabla 2, según la desviación entre réplicas.")
tabla("Tabla 2. Diferencia mínima detectable entre niveles de un factor, con potencia de 80 % y α = 0,05",
      ["Desviación entre réplicas σ (mg/L)", "Tamaño de efecto f", "Diferencia mínima δ (mg/L)"],
      [[f(p["sigma_mgL"], 2), f(p["f"], 2), f(p["delta_min_mgL"], 3)] for p in pot],
      "Fuente: elaboración propia con la distribución F no central.", [6.0, 4.0, 5.0])
H2("Registros existentes")
T("Los diez registros cumplieron la verificación interna: el caudal recalculado coincide con el registrado y las categorías corresponden al rango. Cinco tienen cloro; cuatro de ellos quedan entre 0,2 y 0,5 mg/L y uno, con dos "
  "pastillas, en 0,72 mg/L. Al no poder confirmarse su procedencia, no se incluyen en el análisis; si el equipo confirma que son mediciones de laboratorio, serían la primera evidencia contra la cual comparar la simulación.")

# ------------------------------------------------------------------ 4. Discusión
H1("Discusión")
T("Dos hallazgos orientan el trabajo experimental. El primero es que la fracción derivada, la única variable que el operador controla de forma directa, es también la que más pesa y la que más varía en el "
  "modelo. Fijarla con precisión, por ejemplo con válvulas con tope y marca de posición o con un orificio calibrado en lugar de una válvula de bola, rinde más que afinar la dosis media. Es coherente con lo "
  "observado en laboratorio: la posición del dispositivo importó más que la presión {c:aquatabs}. El segundo es que la variabilidad se paga en cumplimiento: 26 puntos porcentuales en el mejor punto del mapa.")
T("La comparación con estudios de campo debe leerse con cautela. Una desviación estándar de 0,5 a 0,8 mg/L en un clorador modificado {c:usvi} es mayor que la ventana de 0,3 mg/L del diseño, y en Ghana, aunque el método "
  "pasivo terminó con 100 % de las mediciones en el rango de 0,2 a 2,0 mg/L tras cinco meses, hubo grandes fluctuaciones intermedias {c:ghana}. La norma colombiana admite un rango más ancho (0,3–2,0 mg/L) que el "
  "objetivo del proyecto; con ese rango, la tolerancia a la variabilidad sería mucho mayor y el diseño tendría margen. Además, en los dispositivos que se desempeñan bien, el soporte técnico recurrente parece "
  "importar tanto como el aparato {c:honduras,odisha}.")
T("Limitaciones. Las distribuciones son supuestos; los factores de temperatura, pH, turbidez y caudal no están ajustados a datos; la correlación de Spearman mide asociación monótona y no efectos de interacción; y la "
  "desviación entre réplicas de 0,10 mg/L del análisis de potencia es una hipótesis hasta que se mida. La hoja de aleatorización y el diseño 2³ ya están listos; lo que falta es ejecutarlos.")

# ------------------------------------------------------------------ 5. Conclusiones
H1("Conclusiones")
T(f"En la simulación, la fracción derivada y la demanda de cloro explican casi toda la sensibilidad del cloro neto. Fijar la fracción derivada eleva el cumplimiento de {f(vv['cumple_fraccion_variable_pct'], 1)} % a "
  f"{f(vv['cumple_fraccion_fija_pct'], 1)} % en el mejor punto del mapa. El diseño factorial 2³ con 24 corridas es suficiente para detectar diferencias de {f(pot[2]['delta_min_mgL'], 2)} mg/L si la desviación entre réplicas es de 0,10 mg/L. "
  "El prototipo permanece en TRL 3; el paso siguiente es ejecutar las 24 corridas con la hoja aleatorizada.")
H1("Recomendaciones")
T("(1) Ejecutar el factorial 2³ con la hoja de aleatorización y estimar la desviación entre réplicas con las primeras corridas. (2) Medir la fracción derivada por aforo volumétrico en cada posición de válvula. "
  "(3) Probar un dispositivo de fijación de la posición de las válvulas. (4) Medir la demanda del agua antes de cada serie. (5) Confirmar la procedencia de los diez registros de septiembre.")
declaraciones("La hoja de aleatorización de las 24 corridas está en DOE_hoja_aleatorizacion.csv.")
cierre(autores, TITULO_ES, "Sensibilidad y robustez de un clorificador pasivo de PVC", Path(sys.argv[1]))
Path(sys.argv[1]).with_suffix(".txt").write_text("\n\n".join(f"[{e}] {t}" for e, t in LOG), encoding="utf-8")
