"""Artículo único del equipo del clorificador (El Vidrial, Montería) en dos columnas.
Reúne las tres líneas de análisis (balance de masa, sensibilidad y diseño experimental, costo y viabilidad) en un solo texto.
Uso: python -X utf8 ef_clor.py salida.docx"""
import json, math, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GEN = AQUI.parent.parent / "entregables_last" / "generador"
sys.path.insert(0, str(GEN))
import ef_nucleo as EN
from ef_nucleo import construir

# ---- referencias y figuras de este proyecto (no las del otro)
EN.FIG = AQUI / "fig"
EN.REFS = {r["doi"]: r for r in json.loads((AQUI / "refs_crossref.json").read_text(encoding="utf-8")) if r["estado"] == "VERIFICADO"}
EN.CLAVES = {
    "uganda": "10.3362/1756-3488.20-00014", "nepal": "10.1021/acs.est.2c03133", "venturi": "10.1038/s41545-020-00091-1",
    "dhaka": "10.1021/acs.est.1c01308", "mercado": "10.1021/acs.estlett.2c00781", "aquatabs": "10.1061/(asce)ee.1943-7870.0001883",
    "ghana": "10.1371/journal.pwat.0000295", "usvi": "10.1061/(asce)ee.1943-7870.0002063", "honduras": "10.1021/acsestwater.3c00425",
    "kmu": "10.2166/washdev.2024.407", "guatemala": "10.1371/journal.pwat.0000255", "odisha": "10.1371/journal.pwat.0000440",
    "etiopia": "10.1371/journal.pwat.0000575", "amrose": "10.1146/annurev-environ-031411-091819", "arnold": "10.4269/ajtmh.2007.76.354",
    "wolf": "10.1016/S0140-6736(23)00458-0", "clasen": "10.1002/14651858.CD004794.pub3", "powell": "10.1016/S0043-1354(99)00097-4",
    "wilson": "10.1080/01621459.1927.10502953", "pickering": "10.1016/S2214-109X(19)30315-8", "prisma": "10.1136/bmj.n71",
}
NORMAS = {
    "res2115": ("Ministerio de la Protección Social, 2007", "Ministerio de la Protección Social y Ministerio de Ambiente, Vivienda y Desarrollo Territorial (2007). "
                "Resolución 2115 de 2007, por medio de la cual se señalan características, instrumentos básicos y frecuencias del sistema de control y vigilancia para la calidad del agua para consumo humano. Bogotá, Colombia. "
                "https://normograma.invima.gov.co/normograma/compilacion/docs/resolucion_minproteccion_2115_2007.htm", "ministerio"),
    "oms": ("OMS, 2022", "World Health Organization (2022). *Guidelines for Drinking-water Quality: Fourth Edition Incorporating the First and Second Addenda*. Geneva, Switzerland: WHO. "
            "https://www.who.int/publications/i/item/9789240045064", "world"),
}
_cc, _rl, _oa, _ol = EN.cita_corta, EN.ref_larga, EN._orden_alfa, EN._limpiar


def _lim(t):
    s = _ol(t)
    return (s[:1].upper() + s[1:].lower()) if len(s) > 8 and s == s.upper() else s


EN._limpiar = _lim


def cita_corta(c, narrativa=False):
    if c in NORMAS:
        t = NORMAS[c][0]
        return t.replace(", ", " (") + ")" if narrativa else t
    return _cc(c, narrativa)


EN.cita_corta = cita_corta
EN.ref_larga = lambda c: NORMAS[c][1] if c in NORMAS else _rl(c)
EN._orden_alfa = lambda c: NORMAS[c][2] if c in NORMAS else _oa(c)


def f(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def m(x):
    return f"{int(round(x)):,}".replace(",", ".")


R = json.loads((AQUI / "resultados_estudio.json").read_text(encoding="utf-8"))
C = json.loads((AQUI / "resultados_complemento.json").read_text(encoding="utf-8"))
PR = json.loads((AQUI / "prisma_cifras.json").read_text(encoding="utf-8"))
b = R["base"]; mp = R["mapa_resumen"]; vv = R["variabilidad_vs_dosis"]; rho = R["spearman_neto"]; pot = R["potencia_DOE"]
pb = C["payback_por_hogares_compartidos"]; cm3 = C["costo_cloro_por_m3_ideal"]
N = m(R["reproduccion"]["N"]); pr = PR
dif = vv["cumple_fraccion_fija_pct"] - vv["cumple_fraccion_variable_pct"]
phi = math.exp(0.035 * 20) * math.exp(0.03 * 3) * (1 + 0.15 * 1.32)
req = 0.65 + 0.4 * phi

TITULO_ES = ("Clorificador pasivo de PVC con derivación para una vereda rural de Montería: balance de masa, sensibilidad, "
             "diseño experimental y viabilidad económica")
TITULO_EN = ("Passive PVC bypass chlorinator for a rural community in Montería: mass balance, sensitivity, "
             "experimental design and economic viability")
RES_ES = ("El Vidrial, vereda rural de Montería, no cuenta con una desinfección continua y verificable del agua que consume. Este artículo reúne el análisis de un clorificador pasivo de PVC que divide el caudal, hace pasar una fracción por una cámara con pastillas de tricloro al 90 % y recombina las corrientes, con materiales por 159.991 COP. "
          f"Con un balance de masa y {N} escenarios de Monte Carlo se estudian tres preguntas: cuánta dosis necesita el dispositivo para dejar entre 0,2 y 0,5 mg/L de cloro libre, qué variables controlan el resultado y cuánto cuesta y en cuánto tiempo se recupera la inversión. "
          f"La dosis efectiva media fue de {f(b['dosis_efectiva_media'], 2)} mg/L frente a una demanda media supuesta de {f(b['demanda_media'], 2)} mg/L, y solo {f(b['adecuada'] / 10, 1)} % de los escenarios quedó en el rango. "
          f"La fracción derivada (ρ = {f(rho['frac']['rho'], 2)}) y la demanda (ρ = {f(rho['demanda']['rho'], 2)}) concentran la sensibilidad; fijar la fracción derivada elevó el cumplimiento del mejor punto del mapa de {f(vv['cumple_fraccion_variable_pct'], 1)} % a {f(vv['cumple_fraccion_fija_pct'], 1)} %. "
          f"El cloro teórico cuesta de {f(cm3['0.4']['COP_por_m3'], 1)} a {f(cm3['1.05']['COP_por_m3'], 1)} COP por m³ y una unidad compartida por tres hogares se recupera en {f(pb['3'], 1)} meses con los supuestos del proyecto. "
          "Se propone un diseño factorial 2³ de 24 corridas aleatorizadas para validar los resultados. Las distribuciones son supuestos del equipo y no hay validación experimental: el nivel de madurez es TRL 3.")
RES_EN = ("El Vidrial, a rural community in Montería, lacks continuous and verifiable drinking-water disinfection. This paper brings together the analysis of a passive PVC chlorinator that splits the flow, sends a fraction through a chamber with 90 % trichloroisocyanuric acid tablets and recombines the streams, with materials costing 159,991 COP. "
          f"With a mass balance and {N} Monte Carlo scenarios, three questions are studied: how much dose the device needs to leave 0.2 to 0.5 mg/L of free chlorine, which variables control the outcome, and what it costs and how long the investment takes to pay back. "
          f"The mean effective dose was {f(b['dosis_efectiva_media'], 2)} mg/L against an assumed mean demand of {f(b['demanda_media'], 2)} mg/L, and only {f(b['adecuada'] / 10, 1)} % of scenarios fell inside the range. "
          f"The bypass fraction (ρ = {f(rho['frac']['rho'], 2)}) and the demand (ρ = {f(rho['demanda']['rho'], 2)}) concentrate the sensitivity; fixing the bypass fraction raised compliance at the best point of the map from {f(vv['cumple_fraccion_variable_pct'], 1)} % to {f(vv['cumple_fraccion_fija_pct'], 1)} %. "
          f"Ideal chlorine costs {f(cm3['0.4']['COP_por_m3'], 1)} to {f(cm3['1.05']['COP_por_m3'], 1)} COP per m³ and a unit shared by three households pays back in {f(pb['3'], 1)} months under the project's assumptions. "
          "A 2³ factorial design of 24 randomized runs is proposed to validate the results. The distributions are team assumptions and there is no experimental validation: the readiness level is TRL 3.")
KW_ES = "desinfección del agua; cloración pasiva; balance de masa; simulación Monte Carlo; diseño de experimentos; agua rural; Montería"
KW_EN = "water disinfection; passive chlorination; mass balance; Monte Carlo simulation; design of experiments; rural water; Montería"

CUERPO = r'''
H1("Introducción")
H2("El problema de dosificar sin conocer la demanda")
T("Desinfectar con cloro parece una operación sencilla: se agrega una cantidad de producto y se espera. En la práctica, el cloro que se agrega se reparte entre lo que oxida la materia orgánica y los metales disueltos, lo que decae con el tiempo y la temperatura, y lo que queda como residual libre, que es lo único que protege el agua después. "
  "Si la dosis no supera la demanda, el residual es cero aunque se haya vertido producto. La Resolución 2115 de 2007 pide que el cloro residual libre esté entre 0,3 y 2,0 mg/L en cualquier punto de la red y dice, además, que la dosis debe resultar de pruebas frecuentes de demanda {cite:res2115}. "
  "Las guías de la Organización Mundial de la Salud van en la misma dirección {cite:oms}. Un dispositivo que no parte de la demanda del agua que trata está calibrado a ciegas.")
T("Un clorificador pasivo, además, no tiene sensor ni lazo de control. Una vez calibrado, entrega la dosis que le permiten su hidráulica y su pastilla, y esa dosis cambia con el caudal, con la temperatura, con el desgaste del producto y con la posición de las válvulas. Por eso su desempeño no se resume en un promedio: "
  "lo que decide si el agua queda protegida es la proporción del tiempo en que el cloro residual libre permanece dentro de un rango estrecho.")
T("El Vidrial es una vereda rural de Montería, Córdoba, cuyas familias, según la caracterización preliminar del proyecto, usan fuentes de agua sin tratamiento adecuado o métodos informales de potabilización. El contexto no es excepcional: la carga de enfermedad atribuible al agua insegura y al saneamiento deficiente sigue siendo alta {cite:wolf}, "
  "y revisiones y ensayos muestran que clorar en el punto de uso o de recolección reduce la diarrea infantil {cite:arnold,clasen,pickering}. Entre las opciones de bajo costo, la cloración pasiva, es decir, la que no requiere electricidad ni una acción diaria del usuario, se considera una vía para ampliar el acceso {cite:amrose,mercado}. "
  "El proyecto construyó un diseño de PVC por gravedad con derivación y cámara de pastillas, cuyos materiales cuestan 159.991 COP.")
H2("Qué muestra la literatura reciente")
T("Se hizo una búsqueda reproducible en OpenAlex (sección 2.7). De " + m(pr["identificados_total"]) + " registros se retuvieron " + str(pr["incluidos_busqueda"]) + " estudios sobre cloración pasiva, en línea o con dosificadores en contextos de bajos recursos (Figura 1). "
  "Sus resultados dependen mucho de qué tan bien se ajusta la dosis a las condiciones locales. En seis sistemas de agua por gravedad de Nepal, la cloración pasiva bajó la presencia de E. coli en los grifos de más de 80 % a 7 % en un año {cite:nepal}. "
  "En Guatemala, un clorador local de bajo costo redujo la contaminación fecal, pero solo 24 % de las muestras de grifo alcanzó el mínimo de 0,2 mg/L {cite:guatemala}. En Ghana, el cloro libre estuvo en el rango de 0,2 a 2,0 mg/L en 86 % de las mediciones con el método pasivo y en 71 % con el manual, "
  "y las fluctuaciones observadas no quedaron explicadas por el pH, la temperatura, la conductividad ni la turbidez; los autores señalan cambios en la demanda de cloro como posible causa {cite:ghana}. En Uganda, siete dispositivos sin electricidad se compararon por consistencia de dosis y solo uno, el clorador en T, alcanzó la dosis correcta con probabilidad de 90 % {cite:uganda}. "
  "El patrón se repite: el dispositivo funciona cuando su dosis se ajusta a la fuente, y falla cuando no.")
figura(["prisma.png"], 8.3, "Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.")
T("La variabilidad es el otro problema de campo. En Ghana, 685 mediciones en dos redes mostraron grandes fluctuaciones del cloro, en especial con el método pasivo {cite:ghana}. En Honduras, los problemas técnicos explicaron 26 % de los lapsos sin cloro, y los errores ocasionales y habituales de las juntas de agua, 24 y 15 % {cite:honduras}. "
  "En ensayos de laboratorio con un dosificador comercial en línea, la presión no modificó el cloro residual, pero la posición del dispositivo sí {cite:aquatabs}, y un sistema doméstico con clorador de piscina modificado tuvo desviaciones estándar de 0,5 a 0,8 mg/L {cite:usvi}. Esa desviación es del tamaño de la ventana objetivo completa.")
T("Los datos económicos y de adopción son menos abundantes que los técnicos, pero consistentes. En sistemas por gravedad de Nepal, el cloro costó entre 0,06 y 0,09 USD por metro cúbico tratado {cite:nepal}. En Dhaka, 196 propietarios de viviendas de alquiler mostraron una demanda efectiva por cloración en línea comparable a la de otros productos, pero menor en las viviendas de ingresos bajos {cite:dhaka}. "
  "En Kisumu, Kenia, 27 % de los kioscos de agua a los que se ofreció un dosificador Venturi se comprometió con un paquete de servicio {cite:venturi}. En Kenia, Malawi y Uganda, el conocimiento del uso correcto del dosificador y la promoción comunitaria se asociaron con tener cloro residual {cite:kmu}, y en Etiopía la fragilidad de las cadenas de suministro llevó a probar un clorador con producción in situ {cite:etiopia}.")
tabla("Tabla 1. Desempeño y sostenibilidad reportados por estudios de cloración pasiva o en línea",
      ["Contexto", "Refs.", "Medida reportada", "Lectura para este diseño"],
      [["Guatemala, clorador local", "{cite:guatemala}", "24 % de grifos con al menos 0,2 mg/L", "Un diseño barato puede reducir E. coli y aun así dosificar poco"],
       ["Ghana, pasivo y manual", "{cite:ghana}", "86 % y 71 % en 0,2–2,0 mg/L", "Las fluctuaciones apuntan a la demanda cambiante"],
       ["Uganda, siete dispositivos", "{cite:uganda}", "Dosis correcta: 90 % (en T) a 40 % (balde)", "La consistencia depende del diseño hidráulico"],
       ["Honduras, juntas de agua", "{cite:honduras}", "77 % de muestras con al menos 0,2 mg/L", "El apoyo técnico explica gran parte de los aciertos"],
       ["Nepal, sistemas por gravedad", "{cite:nepal}", "E. coli en grifos: de más de 80 % a 7 %", "Cloro a 0,06–0,09 USD por m³ tratado"]],
      "Fuente: elaboración propia a partir de los resúmenes de las referencias citadas.", [3.4, 3.4, 4.6, 5.6])
H2("Objetivo y aportes")
T("El objetivo es responder, con los supuestos del propio proyecto y antes de cualquier prueba de campo, tres preguntas: cuánta dosis necesita el clorificador de PVC para dejar entre 0,2 y 0,5 mg/L y si el diseño la entrega; qué variables controlan el cloro residual y cuánto pesa la variabilidad frente a la media; y cuánto cuesta el dispositivo y en cuánto tiempo se recupera la inversión. "
  "Los aportes son un balance de masa que enlaza la geometría del dispositivo con la demanda del agua, una simulación que cuantifica el desajuste, un diseño factorial 2³ con su análisis de potencia para validar el prototipo y un cálculo de costo y recuperación que no separa la economía de la eficacia.")

H1("Métodos")
H2("Dispositivo")
T("El clorificador se construye con tubería y accesorios de PVC a presión de 1 y 2 pulgadas y funciona por gravedad con una carga de 1,5 a 5,0 m. Una Tee de 1 pulgada divide el caudal en un ramal de derivación con una válvula de bola y un ramal que pasa por una cámara de 2 pulgadas y 0,50 m con pastillas de tricloro al 90 %, con válvulas de entrada y de salida; una segunda Tee recombina las corrientes (Figura 2). "
  "El caudal de diseño es de 0,2 a 2,5 L/s. La apertura relativa de las tres válvulas fija la fracción $\\alpha$ del caudal que pasa por la cámara. Lo que el operador puede mover es esa apertura y la carga de pastillas; el caudal, la temperatura, el pH, la turbidez y la demanda las impone la fuente.")
figura(["esquema.png"], 14.0, "Figura 2. Esquema del clorificador pasivo con derivación; las tres válvulas fijan la fracción α (Q_cámara = α·Q_total).")
H2("Balance de masa")
T("El caudal total se reparte entre derivación y cámara, y la fracción que pasa por la cámara es $\\alpha$:")
ecuacion("div", r"Q_t=Q_b+Q_c,\qquad \alpha=\frac{Q_c}{Q_t}")
T("La disolución de la pastilla sigue una ley de transferencia de masa tipo Noyes–Whitney, con coeficiente $k_m$, área expuesta $A_s$ y solubilidad de saturación $C_{sat}$. La concentración en la cámara y, al recombinar con agua sin cloro, la concentración en la mezcla son:")
ecuacion("cam", r"C_c=\frac{k_m A_s C_{sat}}{Q_c+k_m A_s}")
ecuacion("mez", r"C_s=\alpha\,C_c")
T("El cloro residual libre resulta de restar la demanda $D$ y de aplicar el decaimiento de primer orden, con constante $k$ y tiempo de contacto $t$, y los factores de temperatura, pH, turbidez y caudal que calibró el equipo en su simulación:")
ecuacion("res", r"C_r=\max\!\left(\frac{(C_s-D)\,e^{-kt}}{f_T\,f_{pH}\,f_{tu}\,f_Q},\,0\right)")
T("con $f_T=e^{0{,}03(T-25)}$, $f_{pH}=1+0{,}06\\,|pH-7{,}2|$, $f_{tu}=1+0{,}15\\,\\mathrm{NTU}$ y $f_Q=1+0{,}08\\,(Q-1)$. Estos factores son del modelo del proyecto y no están ajustados a mediciones; la dependencia de la cinética con la temperatura y la composición del agua es conocida {cite:powell}. "
  "Si se quiere un residual objetivo $C^{*}$ y se llama $\\Phi=e^{kt}f_Tf_{pH}f_{tu}f_Q$ al factor de pérdida, la mezcla debe entregar al menos:")
ecuacion("req", r"C_s^{\min}=D+C^{*}\,\Phi")
H2("Simulación")
T("Se reprodujo el cuaderno Monte Carlo del proyecto con la misma semilla (42) y " + N + " escenarios. Las distribuciones son supuestos del equipo: caudal normal (1,0; 0,25) L/s, tiempo de contacto normal (20; 4) min, cloro de cámara normal (1,2; 0,3) mg/L, demanda normal (0,65; 0,18) mg/L, fracción derivada beta(2,5; 5,5), decaimiento normal (0,035; 0,010) por minuto, temperatura normal (28; 3) °C, pH normal (7,2; 0,4) y turbidez gamma(2,2; 0,6) NTU. "
  "La reproducción coincidió con el archivo del cuaderno (diferencia máxima " + f(R['reproduccion']['max_diferencia_vs_csv_del_notebook'], 1) + "). El rango objetivo es de 0,2 a 0,5 mg/L, con meta de 0,4, y los intervalos de proporciones son de Wilson {cite:wilson}. "
  "Para el mapa de cumplimiento se multiplicó la dosis efectiva por una escala de 0,5 a 6 y se varió la demanda media de 0,05 a 1,0 mg/L, con 20.000 escenarios por celda.")
H2("Sensibilidad y variabilidad")
T("La sensibilidad se midió con la correlación de rangos de Spearman entre cada variable de entrada y el cloro neto $\\alpha C_c-D$, antes de recortar a cero, porque el residual recortado es continuo solo en una parte de los escenarios. Para separar la media de la variabilidad se buscó, en el mapa de cumplimiento, el punto con mayor cumplimiento y se repitió el cálculo con la fracción derivada fija en su media.")
H2("Diseño experimental")
T("El plan de validación es un factorial completo $2^3$ con tres réplicas, 24 corridas, y tres factores: caudal $A$ (0,5 y 1,5 L/s), apertura de la válvula de derivación $B$ (25 y 75 %) y carga de pastillas $C$ (una o dos). La respuesta es el cloro residual libre por DPD. Las 24 corridas se aleatorizaron con semilla 2026 (hoja de ejecución en DOE_hoja_aleatorizacion.csv). El modelo de análisis de varianza es:")
ecuacion("anova", r"Y_{ijkl}=\mu+A_i+B_j+C_k+(AB)_{ij}+(AC)_{ik}+(BC)_{jk}+(ABC)_{ijk}+\varepsilon_{ijkl}")
T("Los supuestos se revisarían con Shapiro–Wilk y Levene. La potencia para un efecto principal con $N=24$ y 16 grados de libertad del error se obtuvo de la distribución F no central con parámetro $\\lambda=Nf^{2}$, donde $f$ es el tamaño de efecto de Cohen; la diferencia mínima detectable entre niveles es:")
ecuacion("delta", r"\delta_{\min}=2\,f\,\sigma,\qquad 1-\beta=1-F_{1,16,\lambda}\!\left(F_{0{,}95;1,16}\right)\ge 0{,}80")
H2("Consumo de cloro y viabilidad económica")
T("Para una dosis $d$ en mg/L y un caudal $Q$ en L/s, la masa de cloro por día y la masa de pastillas de tricloro al 90 % de cloro disponible son:")
ecuacion("masa", r"M_{\mathrm{Cl}}=\frac{d\,Q\,86\,400}{1000}\ [\mathrm{g/d}],\qquad M_{\mathrm{TCCA}}=\frac{M_{\mathrm{Cl}}}{0{,}90}")
T("Se evaluaron dos dosis: 0,4 mg/L, solo el residual meta, y 1,05 mg/L, que suma la demanda media supuesta de 0,65 mg/L. El cálculo supone disolución ideal y no incluye pérdidas por disolución irregular. El precio del cloro se tomó de la ficha del proyecto: un paquete de 15.000 COP, que se trata como 1 kg. "
  "Con la inversión $I$ (159.991 COP), el beneficio mensual supuesto $B$ por hogar (25.000 COP, del documento del proyecto), el costo operativo mensual $O$ (15.000 COP, de la ficha de costos) y $n$ hogares que comparten la unidad, el tiempo de recuperación simple y el valor presente neto a 12 meses con tasa mensual $r=0{,}8\\ \\%$ son:")
ecuacion("payback", r"T_R=\frac{I}{nB-O},\qquad \mathrm{VPN}=-I+\sum_{t=1}^{12}\frac{nB-O}{(1+r)^t}")
T("El beneficio de 25.000 COP es un supuesto del proyecto que agrupa ahorro en compra de agua y en gastos de salud; se ofrece el cálculo como análisis de sensibilidad y no como pronóstico.")
H2("Búsqueda bibliográfica")
T("La búsqueda se hizo en OpenAlex el 6 de noviembre de 2026 con la ecuación guardada en prisma_cifras.json, en título y resumen, artículos de 2020 a 2026 en inglés o español con DOI. El cribado exigió que el título tratara de cloración; la elegibilidad se evaluó sobre título y resumen con tres criterios (agua de consumo, dispositivo pasivo o dosificador, contexto de bajos recursos). "
  "El flujo sigue la guía PRISMA 2020 {cite:prisma} y se muestra en la Figura 1. Es una revisión de alcance y no una revisión sistemática completa.")

H1("Resultados")
H2("Qué dosis necesita el diseño")
T(f"Con los valores medios supuestos, el factor de pérdida es $\\Phi\\approx {f(phi, 2)}$. Para dejar 0,4 mg/L con una demanda de 0,65 mg/L, la mezcla debe entregar $C_s^{{\\min}}\\approx {f(req, 2)}$ mg/L, según la ecuación {{E_REQ}}. La dosis efectiva media del modelo es $C_0\\alpha={f(b['dosis_efectiva_media'], 2)}$ mg/L, es decir, "
  f"{f(req / b['dosis_efectiva_media'], 1)} veces menos. La dosis efectiva supera a la demanda en solo {f(100 * b['p_dosis_mayor_demanda'], 1)} % de los escenarios.")
T("La concentración que debe tener la cámara depende de cuánta agua pasa por ella. Con la mezcla requerida, una fracción $\\alpha=0{,}2$ exige una cámara de "
  f"{f(req / 0.2, 1)} mg/L y $\\alpha=0{{,}}5$, de {f(req / 0.5, 1)} mg/L (Tabla 2). Con una cámara que apenas disuelva 1,2 mg/L, como supone la simulación, ninguna fracción razonable alcanza la mezcla requerida.")
tabla("Tabla 2. Concentración de cámara necesaria según la fracción derivada",
      ["Fracción α", "Cámara para dejar 0,4 mg/L (mg/L)", "Cámara si no hubiera demanda (mg/L)"],
      [[f(a, 2), f(req / a, 1), f(0.4 * phi / a, 1)] for a in (0.05, 0.1, 0.2, 0.3, 0.5)],
      "Fuente: cálculo propio con la mezcla requerida y los valores medios supuestos; la tercera columna usa D = 0.", [3.0, 6.0, 6.0])
H2("Cumplimiento simulado")
T(f"De los {N} escenarios, {b['sub']} ({f(b['sub'] / 10, 1)} %; IC 95 %: {f(b['ic_sub'][0], 1)} a {f(b['ic_sub'][1], 1)} %) quedaron por debajo de 0,2 mg/L, {b['adecuada']} ({f(b['adecuada'] / 10, 1)} %; IC 95 %: {f(b['ic_adecuada'][0], 1)} a {f(b['ic_adecuada'][1], 1)} %) en el rango y ninguno por encima. "
  f"El residual medio fue de {f(b['media'], 3)} mg/L, el máximo de {f(b['max'], 2)} mg/L y {b['ceros']} escenarios dieron 0,00 (Figura 3). Solo {C['escenarios_ge_0_3']} escenario alcanzó 0,3 mg/L, el mínimo de la Resolución 2115.")
figura(["hist_cloro.png"], 8.3, "Figura 3. Distribución del cloro residual simulado (n = 1000) y rango objetivo.")
H2("Mapa de cumplimiento")
T(f"Al barrer la escala de la dosis y la demanda media (Figura 4), el máximo de cumplimiento fue de {f(mp['max_cumplimiento_pct'], 1)} %, con una demanda de {f(mp['en_demanda'], 2)} mg/L y una dosis {f(mp['en_escala'], 2)} veces la del cuaderno. Ninguna de las {mp['celdas_totales']} celdas llegó a 90 %. "
  "Aun con demanda casi nula, la variabilidad de la fracción derivada y del cloro de cámara impide que el residual caiga de forma sostenida dentro de un rango de 0,3 mg/L de ancho.")
figura(["mapa_cumplimiento.png"], 8.3, "Figura 4. Escenarios dentro de 0,2–0,5 mg/L según la escala de la dosis y la demanda media; la estrella marca los supuestos del cuaderno.")
H2("Qué variables controlan el cloro neto")
T(f"La Tabla 3 y la Figura 5 muestran que dos variables concentran la sensibilidad: la fracción derivada (ρ = {f(rho['frac']['rho'], 2)}) y la demanda (ρ = {f(rho['demanda']['rho'], 2)}), con una contribución menor del cloro de cámara (ρ = {f(rho['C0']['rho'], 2)}). "
  "El caudal, el tiempo de contacto, la constante de decaimiento, la temperatura, el pH y la turbidez no superaron |ρ| = 0,03. Esto no significa que esas variables carezcan de efecto físico: en el modelo actúan como factores multiplicativos de pocos puntos porcentuales y tienen poca dispersión comparada con la de la dosis.")
nombres = {"frac": "Fracción derivada α", "demanda": "Demanda de cloro", "C0": "Cloro de cámara", "Q": "Caudal", "t": "Tiempo de contacto", "k": "Decaimiento", "T": "Temperatura", "pH": "pH", "turb": "Turbidez"}
filas = [[nombres[k], f(rho[k]["rho"], 2), "< 0,001" if rho[k]["p"] < 0.001 else f(rho[k]["p"], 2)] for k in sorted(rho, key=lambda x: -abs(rho[x]["rho"]))]
tabla("Tabla 3. Correlación de Spearman entre cada variable de entrada y el cloro neto (n = 1000)", ["Variable", "ρ", "Valor p"], filas,
      "Fuente: elaboración propia, estudio_clorificador.py.", [6.0, 3.0, 3.0])
figura(["spearman.png"], 8.3, "Figura 5. Correlación de Spearman con el cloro neto antes de recortar a cero.")
H2("Media frente a variabilidad")
T(f"En el cuaderno original, {f(b['sub'] / 10, 1)} % de los escenarios quedó por debajo de 0,2 mg/L y solo {f(b['adecuada'] / 10, 1)} % en el rango. En el mejor punto del mapa, con una demanda de {f(mp['en_demanda'], 2)} mg/L y una dosis {f(mp['en_escala'], 2)} veces la del cuaderno, el cumplimiento fue de {f(mp['max_cumplimiento_pct'], 1)} %. "
  f"Con la fracción derivada fija en su media y el resto sin cambios, el cumplimiento subió a {f(vv['cumple_fraccion_fija_pct'], 1)} %: la variabilidad de la fracción, por sí sola, cuesta {f(dif, 1)} puntos porcentuales.")
H2("Potencia del diseño 2³")
T("Con 24 corridas y 16 grados de libertad del error, la potencia de 80 % se alcanza con un tamaño de efecto $f=0{,}61$. Eso corresponde a las diferencias mínimas detectables de la Tabla 4, según la desviación entre réplicas.")
tabla("Tabla 4. Diferencia mínima detectable entre niveles de un factor, con potencia de 80 % y α = 0,05",
      ["Desviación entre réplicas σ (mg/L)", "Tamaño de efecto f", "Diferencia mínima δ (mg/L)"],
      [[f(p["sigma_mgL"], 2), f(p["f"], 2), f(p["delta_min_mgL"], 3)] for p in pot],
      "Fuente: elaboración propia con la distribución F no central.", [6.0, 4.0, 5.0])
H2("Costo de materiales")
tabla("Tabla 5. Presupuesto de materiales del prototipo (COP)",
      ["Ítem", "Cant.", "Valor unitario", "Valor total"],
      [["Tee de presión de 2\"", "1", "17.000", "17.000"], ["Codo de presión de 2\"", "1", "13.300", "13.300"], ["Adaptador macho de 2\"", "1", "6.700", "6.700"],
       ["Bujes de reducción 2\" × 1\"", "2", "6.300", "12.600"], ["Válvulas de bola de 1\"", "3", "14.900", "44.700"], ["Tee de presión de 1\"", "2", "1.600", "3.200"],
       ["Tubo de 1\" (1,30 m)", "1,3 m", "6.455", "8.391"], ["Tubo de 2\" (0,50 m)", "0,5 m", "23.400", "11.700"], ["Tapón de 1\"", "1", "1.400", "1.400"],
       ["Soldadura líquida", "1", "26.000", "26.000"], ["Pastillas de cloro (paquete)", "1", "15.000", "15.000"], ["**Total**", "", "", "**159.991**"]],
      "Fuente: presupuesto y costos del prototipo, proyecto del equipo.", [5.6, 1.8, 3.0, 3.0])
T("Las tres válvulas de bola son 28 % del total y la soldadura y las pastillas, 26 %. El resto es tubería y accesorios. El costo de 159.991 COP es del orden de 40 USD según el propio documento del proyecto, frente a un rango de 1,2 a 4,5 millones de COP para cloradores comerciales de inyección eléctrica citado en la misma ficha.")
H2("Consumo de cloro y costo por metro cúbico")
filas = [[f(r["Q_Ls"], 1), f(r["dosis_mgL"], 2), f(r["cloro_g_dia"], 1), f(r["TCCA90_g_dia"], 1), f(r["TCCA90_kg_mes_24h"], 2)] for r in R["consumo"]]
tabla("Tabla 6. Consumo teórico de cloro y de pastillas de tricloro al 90 % si el sistema opera 24 horas",
      ["Q (L/s)", "Dosis (mg/L)", "Cloro (g/día)", "Pastillas (g/día)", "Pastillas (kg/mes)"], filas,
      "Fuente: elaboración propia con la ecuación de la masa de cloro; disolución ideal.", [2.0, 2.4, 2.8, 3.0, 3.0])
T(f"Un kilogramo de pastillas alcanza para {m(R['alcance_1kg_TCCA90_m3']['dosis_1_05'])} m³ con 1,05 mg/L y para {m(R['alcance_1kg_TCCA90_m3']['dosis_0_4'])} m³ con 0,4 mg/L. Con un precio de 15.000 COP por kilogramo, el costo teórico del cloro es de "
  f"{f(cm3['1.05']['COP_por_m3'], 1)} COP por m³ con 1,05 mg/L y de {f(cm3['0.4']['COP_por_m3'], 1)} COP por m³ con 0,4 mg/L. En Nepal, el cloro costó de 0,06 a 0,09 USD por m³ {{cite:nepal}}; con el tipo de cambio implícito del proyecto (159.991 COP, unos 40 USD), eso equivale a unos 240–360 COP por m³, más de diez veces el valor ideal. "
  "El cálculo estequiométrico es, por tanto, un piso y no una estimación del gasto real.")
H2("Tiempo de recuperación")
T(f"Con los supuestos del proyecto, una unidad usada por un solo hogar tiene un beneficio mensual bruto de 25.000 COP y se recupera en {f(C['payback_meses_1hogar_bruto'], 1)} meses; descontando el costo operativo de 15.000 COP, el tiempo sube a {f(C['payback_meses_1hogar_neto'], 1)} meses y el valor presente neto a 12 meses es de {m(C['vpn_12m_neto_de_opex_1hogar'])} COP, es decir, negativo. "
  f"Compartida por dos hogares, la recuperación baja a {f(pb['2'], 1)} meses; por tres, a {f(pb['3'], 1)}; y por diez, a {f(pb['10'], 1)} (Figura 6). Sin restar el costo operativo, el valor presente neto a 12 meses es de {m(C['vpn_12m_solo_beneficio'])} COP, calculado con una tasa mensual de 0,8 %.")
figura(["payback.png"], 8.3, "Figura 6. Tiempo de recuperación simple según el número de hogares que comparten una unidad (beneficio supuesto de 25.000 COP/mes por hogar).")
H2("Costo bajo frente a desempeño técnico")
T(f"La simulación dio {f(b['adecuada'] / 10, 1)} % de escenarios en el rango de 0,2 a 0,5 mg/L y {f(b['sub'] / 10, 1)} % por debajo. Si esos supuestos se confirmaran, el ahorro estimado no se materializaría, porque el agua no quedaría protegida. Por eso la viabilidad económica solo tiene sentido condicionada a que la calibración funcione.")

H1("Discusión")
T("El resultado central no es que el dispositivo falle, sino que el diseño no puede juzgarse sin conocer la demanda. Con los supuestos del equipo, la dosis queda a una fracción de lo necesario, y subirla lo suficiente exige una cámara muy concentrada que una pastilla en erosión pasiva difícilmente sostiene. "
  "Esto coincide con la experiencia de campo: en Ghana las fluctuaciones del cloro no se explicaron por las variables fisicoquímicas medidas y se atribuyeron a cambios en la demanda {cite:ghana}; en Guatemala, un dispositivo barato mejoró la calidad microbiológica pero dosificó poco {cite:guatemala}; y en Uganda el dispositivo que acertó con mayor frecuencia fue el de mejor diseño hidráulico {cite:uganda}.")
T("La segunda lectura es que la fracción derivada, la única variable que el operador controla de forma directa, es también la que más pesa y la que más varía en el modelo. Fijarla con precisión, por ejemplo con válvulas con tope y marca de posición o con un orificio calibrado en lugar de una válvula de bola, rinde más que afinar la dosis media. "
  f"Es coherente con lo observado en laboratorio: la posición del dispositivo importó más que la presión {{cite:aquatabs}}. Y la variabilidad se paga en cumplimiento: {f(dif, 0)} puntos porcentuales en el mejor punto del mapa.")
T("Hay una consecuencia práctica. La Resolución 2115 ya pide que la dosis salga de pruebas de demanda {cite:res2115}, y el protocolo del proyecto mide cloro por DPD pero no define una prueba de demanda previa. Incorporarla, aunque sea con una dosis de ensayo en un recipiente, convierte la calibración de las válvulas en un procedimiento y no en un tanteo. "
  "Además, la presencia de partículas y materia orgánica en un agua de pozo o de río debería justificar una etapa previa de reducción de turbidez, algo que las guías recomiendan para que la desinfección sea eficaz {cite:oms}.")
T("En cuanto a los costos, el material es el menor de ellos. Lo que decide la sostenibilidad es lo que rodea al dispositivo: el suministro de pastillas, la capacitación y las visitas técnicas. En Honduras, la frecuencia de las visitas técnicas fue el mejor predictor del éxito {cite:honduras}; en Kenia, Malawi y Uganda lo fue el conocimiento del uso correcto {cite:kmu}. "
  "Ninguna de esas partidas está en el presupuesto de 159.991 COP, y deberían aparecer en un presupuesto de operación del piloto. Compartir la unidad cambia el resultado: con un hogar, la recuperación es de unos 16 meses con el costo operativo supuesto; con dos o más, baja de cinco meses. "
  "Eso sugiere que el diseño tiene sentido como infraestructura comunal, a cargo de la junta de acción comunal, y no como equipo doméstico; la evidencia de Dhaka apunta en el mismo sentido, porque los hogares de bajos ingresos tienen menos capacidad de pago y podrían necesitar subsidios {cite:dhaka}.")
T("Hay límites que conviene tener presentes. Las distribuciones, en particular la demanda de 0,65 mg/L y el cloro de cámara de 1,2 mg/L, son supuestos sin medición; si la demanda real fuera de 0,1 a 0,2 mg/L, el cuadro cambiaría. Los factores de temperatura, pH, turbidez y caudal no están ajustados a datos, y la correlación de Spearman mide asociación monótona y no efectos de interacción. "
  "La desviación entre réplicas de 0,10 mg/L del análisis de potencia es una hipótesis hasta que se mida, y el beneficio mensual de 25.000 COP es un supuesto del proyecto. El rango de diseño (0,2–0,5 mg/L) es más estrecho que el de la norma (0,3–2,0 mg/L) y su límite inferior queda por debajo del mínimo normativo; con el rango legal, la tolerancia a la variabilidad sería mucho mayor y el diseño tendría margen.")

H1("Conclusiones")
T(f"Con los supuestos actuales, el clorificador de PVC no alcanza el rango objetivo: {f(b['adecuada'] / 10, 1)} % de los escenarios simulados cumple y la dosis efectiva media es {f(req / b['dosis_efectiva_media'], 1)} veces inferior a la requerida. El balance de masa permite decir cuánto falta y por qué, sin ensayos costosos. "
  f"La fracción derivada y la demanda de cloro explican casi toda la sensibilidad del cloro neto, y fijar la fracción derivada eleva el cumplimiento del mejor punto del mapa de {f(vv['cumple_fraccion_variable_pct'], 1)} % a {f(vv['cumple_fraccion_fija_pct'], 1)} %. "
  f"El dispositivo cuesta 159.991 COP en materiales y su cloro teórico entre {f(cm3['0.4']['COP_por_m3'], 1)} y {f(cm3['1.05']['COP_por_m3'], 1)} COP por m³; una unidad para un solo hogar se recupera en {f(C['payback_meses_1hogar_neto'], 1)} meses y compartida por tres, en {f(pb['3'], 1)}, siempre que la calibración funcione. "
  f"El diseño factorial 2³ de 24 corridas detecta diferencias de {f(pot[2]['delta_min_mgL'], 2)} mg/L si la desviación entre réplicas es de 0,10 mg/L. El prototipo está en TRL 3: concepto y modelo analítico, sin validación experimental.")
H1("Recomendaciones")
T("Antes de una prueba en la vereda, recomendamos medir la demanda de cloro de cada fuente y determinar la tasa de disolución de la pastilla con el protocolo de aforo y DPD ya redactado. Después, ejecutar el factorial 2³ con la hoja de aleatorización, medir la fracción derivada por aforo volumétrico en cada posición de válvula y probar un dispositivo que fije la posición de las válvulas. "
  "También conviene evaluar un pretratamiento de turbidez, reconsiderar el rango objetivo frente al 0,3–2,0 mg/L de la norma, presupuestar la capacitación y las visitas técnicas, reemplazar el beneficio supuesto por una encuesta de gasto en agua y salud y evaluar el modelo de unidad comunal.")
'''


def contenido(e):
    def adapt(t):
        return t.replace("{E_REQ}", "{eq:req}")

    n_t = [0]
    ns = dict(f=f, m=m, R=R, C=C, PR=PR, b=b, mp=mp, vv=vv, rho=rho, pot=pot, pb=pb, cm3=cm3, N=N, pr=pr, dif=dif, phi=phi, req=req, math=math)

    def H1(t): e.sec(t)
    def H2(t, *a): e.sub(t)
    def T(t): e.P(adapt(t))
    def ecuacion(k, l): e.eq(k, l)

    def tabla(titulo, cab_, filas, fuente_, anchos):
        n_t[0] += 1
        cap = re.sub(r"^Tabla \d+\.\s*", "", titulo)
        e.tabla(f"t{n_t[0]}", cap, cab_, filas, anchos, size=8.5 if len(cab_) >= 4 else 9)
        e.nota(fuente_)

    def figura(archivos, ancho, pie):
        cap = re.sub(r"^Figura \d+\.\s*", "", pie)
        ancha = ancho > 8.3
        e.figura(f"f{e.n_fig + 1}", archivos, cap, ancho if ancha else min(ancho, 8.3), ancha=ancha)

    ns.update(dict(H1=H1, H2=H2, T=T, ecuacion=ecuacion, tabla=tabla, figura=figura))
    autores = ["Roxana Elena Muñoz-Rodiño, Camilo Esteban Alvarez-Durán", "Andrea Guzmán-Gómez, Cristian Javier Cano-Mogollón"]
    afil = ["Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia · Asignatura Gestión Tecnológica",
            "Cristian Javier Cano-Mogollón: Docente Titular, Facultad de Ingeniería Industrial; Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE); Hub Industrial Solution (HIS) · cristian.cano@upb.edu.co"]
    e.titulo_bloque([TITULO_ES, TITULO_EN], autores, afil, RES_ES, KW_ES, RES_EN, KW_EN)
    exec(compile(CUERPO, "cuerpo", "exec"), ns)
    e.sec_sin_numero("Declaraciones")
    e.P("**Ética y consentimiento.** El estudio es un análisis con modelos y simulación; no incluyó personas ni se recogieron datos de hogares. Una prueba con la comunidad pasará antes por revisión ética y consentimiento informado.", sangria=False)
    e.P("**Datos y código.** Los scripts de simulación, la búsqueda bibliográfica, el análisis de potencia y las salidas numéricas (estudio_clorificador.py, complemento.py, busqueda_prisma.py, resultados_estudio.json, prisma_cifras.json, verificacion_referencias.csv) se entregan junto con este artículo.", sangria=False)
    e.P("**Uso de herramientas de inteligencia artificial.** Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar la reproducción de la simulación, la búsqueda bibliográfica, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.", sangria=False)
    e.referencias(extras=[])


if __name__ == "__main__":
    ruta = Path(sys.argv[1]); ruta.parent.mkdir(parents=True, exist_ok=True)
    e = construir(contenido, ruta)
    print("guardado", ruta.name, "| tablas", e.n_tab, "| figuras", e.n_fig, "| ecuaciones", e.n_eq, "| refs", len(set(e.citadas)))
