"""Artículo — primera autora: Andrea Guzmán Gómez. Hilo: el bajo costo es necesario pero no suficiente; viabilidad, consumo de insumos y condiciones sociotécnicas."""
import sys
from nucleo import *

b = R["base"]; pr = PR; mp = R["mapa_resumen"]
N = m(R["reproduccion"]["N"])
pb = C["payback_por_hogares_compartidos"]
cm3 = C["costo_cloro_por_m3_ideal"]

TITULO_ES = ("Costo, consumo de cloro y condiciones de operación de un clorificador pasivo de bajo costo en PVC para una comunidad rural "
             "de Montería: análisis de viabilidad preliminar")
TITULO_EN = ("Cost, chlorine consumption and operating conditions of a low-cost passive PVC chlorinator for a rural community in "
             "Montería: preliminary feasibility analysis")
RES_ES = ("Un dispositivo barato no resuelve el acceso al agua segura si no se sostiene en el tiempo ni entrega la dosis necesaria. Se evalúa la viabilidad preliminar de un clorificador "
          "pasivo de PVC para la vereda El Vidrial, en Montería, con materiales de 159.991 COP. Con la lista de materiales y el presupuesto del proyecto se calculó el consumo de pastillas de tricloro al 90 % "
          "por balance de masa, el costo del cloro por metro cúbico y el tiempo de recuperación según cuántos hogares compartan una unidad, y se contrastaron con evidencia de cloración pasiva en otros países. "
          f"El costo teórico del cloro fue de {f(cm3['0.4']['COP_por_m3'], 1)} a {f(cm3['1.05']['COP_por_m3'], 1)} COP por metro cúbico con disolución ideal. Con un beneficio supuesto de 25.000 COP mensuales por hogar y un costo "
          f"operativo de 15.000 COP al mes, una unidad usada por un solo hogar se recupera en {f(C['payback_meses_1hogar_neto'], 1)} meses y su valor presente neto a 12 meses es negativo; compartida por tres hogares, en "
          f"{f(pb['3'], 1)} meses. Sin embargo, la simulación técnica del proyecto indica que solo {f(b['adecuada'] / 10, 1)} % de los escenarios llega al rango de 0,2 a 0,5 mg/L, de modo que el costo bajo es una condición "
          "necesaria pero no suficiente. Los beneficios son supuestos, no mediciones, y el nivel de madurez es TRL 3.")
RES_EN = ("A cheap device does not deliver safe water if it cannot be sustained over time or does not provide the required dose. The preliminary feasibility of a passive PVC chlorinator for El Vidrial, a rural "
          "community in Montería, is assessed, with materials costing 159,991 COP. Using the project's bill of materials and budget, the consumption of 90 % trichloroisocyanuric acid tablets was calculated by mass balance, "
          "together with the chlorine cost per cubic metre and the payback period as a function of how many households share a unit, and these were contrasted with evidence on passive chlorination elsewhere. "
          f"The theoretical chlorine cost was {f(cm3['0.4']['COP_por_m3'], 1)} to {f(cm3['1.05']['COP_por_m3'], 1)} COP per cubic metre under ideal dissolution. With an assumed benefit of 25,000 COP per household per month and an operating cost "
          f"of 15,000 COP per month, a unit used by one household pays back in {f(C['payback_meses_1hogar_neto'], 1)} months and its 12-month net present value is negative; shared by three households, in {f(pb['3'], 1)} months. "
          f"However, the project's technical simulation shows that only {f(b['adecuada'] / 10, 1)} % of scenarios reach 0.2 to 0.5 mg/L, so low cost is necessary but not sufficient. Benefits are assumptions, not measurements, "
          "and the readiness level is TRL 3.")
KW_ES = "cloración pasiva; viabilidad económica; costo de operación; tiempo de recuperación; adopción comunitaria; agua rural; Montería"
KW_EN = "passive chlorination; economic feasibility; operating cost; payback period; community adoption; rural water; Montería"

autores = encabezado("Guzmán", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

# ------------------------------------------------------------------ 1. Introducción
H1("Introducción")
H2("Una tecnología pensada para quien no puede pagar otra")
T("En las comunidades rurales dispersas, el costo decide qué tecnología llega. Las plantas compactas y los dosificadores con bomba exigen inversión, energía y personal que las juntas de agua no tienen. "
  "La cloración pasiva, que desinfecta sin electricidad ni una acción diaria del usuario, se propone como una vía más accesible {c:amrose,mercado}, y la evidencia agregada indica que clorar "
  "el agua en el punto de uso reduce la diarrea infantil {c:arnold,clasen}. La carga de enfermedad por agua insegura sigue siendo alta {c:wolf}, y un ensayo aleatorizado de cloración en línea en el punto de "
  "recolección estudió su efecto sobre la diarrea en niños {c:pickering}. Si el dispositivo funciona, su costo bajo lo hace replicable.")
T("El Vidrial es una vereda rural de Montería, Córdoba, cuyos hogares, según la caracterización preliminar del proyecto, usan fuentes sin tratamiento adecuado o métodos informales de potabilización. El proyecto "
  "construyó un diseño de PVC por gravedad con derivación y cámara de pastillas, cuyos materiales cuestan 159.991 COP. La pregunta de este trabajo no es solo cuánto cuesta, sino qué hace falta, además de "
  "ese precio, para que el dispositivo sirva.")
H2("Evidencia sobre costos, demanda y sostenibilidad")
T("La búsqueda bibliográfica reproducible (sección 2.5, Figura 1) retuvo " + str(pr["incluidos_busqueda"]) + " estudios sobre cloración pasiva, en línea o con dosificadores en contextos de bajos recursos. Los datos "
  "económicos y de adopción son menos abundantes que los técnicos, pero consistentes. En sistemas por gravedad de Nepal, el cloro costó entre 0,06 y 0,09 USD por metro cúbico tratado, un valor similar al del "
  "monitoreo {c:nepal}. En Dhaka, 196 propietarios de viviendas de alquiler mostraron una demanda efectiva por cloración en línea comparable a la de otros productos, pero menor en las viviendas de ingresos bajos, "
  "lo que sugiere que llegar a los más pobres exigiría reducir costos, subsidiar o ambos {c:dhaka}. En Kisumu, Kenia, 27 % de los kioscos de agua a los que se ofreció un dosificador Venturi se comprometió con un "
  "paquete de servicio {c:venturi}. En Honduras, la frecuencia de las visitas técnicas se correlacionó con el éxito de la cloración y los problemas técnicos explicaron solo 26 % de los lapsos sin cloro {c:honduras}. "
  "Y en Kenia, Malawi y Uganda, el conocimiento del uso correcto del dosificador y la promoción comunitaria se asociaron con tener cloro residual {c:kmu}. En Etiopía, la dificultad de las cadenas de suministro de "
  "cloro llevó a probar clorador con producción in situ {c:etiopia}.")
figura(["prisma.png"], 9.5, "Figura 1. Flujo de la búsqueda bibliográfica (PRISMA 2020), OpenAlex, 6 de noviembre de 2026.")
tabla("Tabla 1. Factores de sostenibilidad reportados en estudios de cloración pasiva o con dosificadores",
      ["Factor", "Refs.", "Hallazgo reportado", "Implicación para El Vidrial"],
      [["Costo del cloro", cita("nepal"), "0,06–0,09 USD por m³ tratado", "El insumo es barato, pero hay que medirlo en campo"],
       ["Demanda de pago", cita("dhaka,venturi"), "Menor demanda en hogares de bajos ingresos; 27 % de kioscos aceptó el servicio", "Probable necesidad de apoyo comunitario o subsidio"],
       ["Soporte técnico", cita("honduras"), "Visitas técnicas correlacionadas con la cloración efectiva", "Prever visitas periódicas de la universidad o del semillero"],
       ["Uso y conocimiento", cita("kmu"), "Saber usar el dosificador se asoció con tener residual", "Capacitación a la junta y a los hogares"],
       ["Suministro de cloro", cita("etiopia,uganda"), "Cadenas de suministro frágiles; diseños sencillos más fáciles de mantener", "Usar pastillas de venta local"]],
      "Fuente: elaboración propia a partir de los resúmenes de las referencias citadas.", [3.0, 2.4, 6.0, 5.2])
H2("Objetivo")
T("El objetivo es estimar, con los datos del propio proyecto, el costo de materiales, el consumo de cloro y el tiempo de recuperación de un clorificador pasivo de PVC, y discutir bajo qué condiciones "
  "técnicas y sociales ese costo bajo se traduce en agua protegida.")

# ------------------------------------------------------------------ 2. Métodos
H1("Métodos")
H2("Lista de materiales y presupuesto")
T("Se tomó el presupuesto de materiales del proyecto (Tabla 2), con precios unitarios de ferretería. El dispositivo usa tubería y accesorios de PVC a presión de 1 y 2 pulgadas y tres válvulas de bola; la cámara de "
  "2 pulgadas y 0,50 m aloja las pastillas de tricloro al 90 % (Figura 2).")
figura(["esquema.png"], 13.5, "Figura 2. Esquema del clorificador pasivo con derivación (Q_cámara = α·Q_total).")
H2("Consumo de cloro por balance de masa")
T("Para una dosis $d$ en mg/L y un caudal $Q$ en L/s, la masa de cloro por día y la masa de pastillas de tricloro al 90 % de cloro disponible son:")
ecuacion("masa", r"M_{\mathrm{Cl}}=\frac{d\,Q\,86\,400}{1000}\ [\mathrm{g/d}],\qquad M_{\mathrm{TCCA}}=\frac{M_{\mathrm{Cl}}}{0{,}90}")
T("Se evaluaron dos dosis: 0,4 mg/L, solo el residual meta, y 1,05 mg/L, que suma la demanda media supuesta de 0,65 mg/L. El cálculo supone disolución ideal y no incluye pérdidas por "
  "disolución irregular. El precio del cloro se tomó de la ficha del proyecto (un paquete de 15.000 COP; la especificación indica 1 kg).")
H2("Viabilidad económica")
T("Con la inversión $I$ (159.991 COP), el beneficio mensual supuesto $B$ por hogar (25.000 COP, del documento del proyecto), el costo operativo mensual $O$ (15.000 COP, de la ficha de costos) y $n$ hogares que comparten la unidad, "
  "el tiempo de recuperación simple y el valor presente neto a 12 meses con tasa mensual $r=0{,}8\\ \\%$ son:")
ecuacion("payback", r"T_R=\frac{I}{nB-O},\qquad \mathrm{VPN}=-I+\sum_{t=1}^{12}\frac{nB-O}{(1+r)^t}")
T("El beneficio de 25.000 COP es un supuesto del proyecto que agrupa ahorro en compra de agua y en gastos de salud; no fue medido. Se ofrece el cálculo como análisis de sensibilidad, no como pronóstico.")
H2("Contraste con el desempeño técnico")
T("Para no separar costo de eficacia, se incorporaron los resultados de la simulación Monte Carlo del proyecto, reproducida con la semilla 42 y " + N + " escenarios. Sus distribuciones son supuestos del equipo. "
  "Las proporciones llevan intervalos de Wilson {c:wilson}. La búsqueda bibliográfica y el flujo PRISMA 2020 {c:prisma} se describen en prisma_cifras.json; el rango objetivo del proyecto es de 0,2 a 0,5 mg/L, "
  "y la Resolución 2115 de 2007 fija 0,3 a 2,0 mg/L {c:res2115}; las guías de la OMS orientan el residual y el tiempo de contacto {c:oms}; la cinética de decaimiento depende de la temperatura y del agua {c:powell}.")

# ------------------------------------------------------------------ 3. Resultados
H1("Resultados")
H2("Costo de materiales")
tabla("Tabla 2. Presupuesto de materiales del prototipo (COP)",
      ["Ítem", "Cantidad", "Valor unitario", "Valor total"],
      [["Tee de presión de 2\"", "1", "17.000", "17.000"], ["Codo de presión de 2\"", "1", "13.300", "13.300"], ["Adaptador macho de 2\"", "1", "6.700", "6.700"],
       ["Bujes de reducción 2\" × 1\"", "2", "6.300", "12.600"], ["Válvulas de bola de 1\"", "3", "14.900", "44.700"], ["Tee de presión de 1\"", "2", "1.600", "3.200"],
       ["Tubo de 1\" (1,30 m)", "1,3 m", "6.455", "8.391"], ["Tubo de 2\" (0,50 m)", "0,5 m", "23.400", "11.700"], ["Tapón de 1\"", "1", "1.400", "1.400"],
       ["Soldadura líquida", "1", "26.000", "26.000"], ["Pastillas de cloro (paquete)", "1", "15.000", "15.000"], ["**Total**", "", "", "**159.991**"]],
      "Fuente: Presupuesto y costos del prototipo, proyecto del equipo.", [6.0, 2.4, 3.6, 3.6])
T("Las tres válvulas de bola son 28 % del total y la soldadura y las pastillas, 26 %. El resto es tubería y accesorios. El costo de 159.991 COP es del orden de 40 USD según el propio documento del proyecto, "
  "frente a un rango de 1,2 a 4,5 millones de COP para cloradores comerciales de inyección eléctrica citado en la misma ficha; esta comparación no pudo contrastarse con cotizaciones.")
H2("Consumo de cloro y costo por metro cúbico")
filas = [[f(r["Q_Ls"], 1), f(r["dosis_mgL"], 2), f(r["cloro_g_dia"], 1), f(r["TCCA90_g_dia"], 1), f(r["TCCA90_kg_mes_24h"], 2)] for r in R["consumo"]]
tabla("Tabla 3. Consumo teórico de cloro y de pastillas de tricloro al 90 % si el sistema opera 24 horas",
      ["Caudal (L/s)", "Dosis (mg/L)", "Cloro (g/día)", "Pastillas (g/día)", "Pastillas (kg/mes)"], filas,
      "Fuente: elaboración propia con la ecuación (1); disolución ideal.", [2.6, 2.6, 3.0, 3.4, 3.4])
T(f"Un kilogramo de pastillas alcanza para {m(R['alcance_1kg_TCCA90_m3']['dosis_1_05'])} m³ con 1,05 mg/L y para {m(R['alcance_1kg_TCCA90_m3']['dosis_0_4'])} m³ con 0,4 mg/L. Con un precio de 15.000 COP por kilogramo, el costo teórico del cloro es de "
  f"{f(cm3['1.05']['COP_por_m3'], 1)} COP por m³ con 1,05 mg/L y de {f(cm3['0.4']['COP_por_m3'], 1)} COP por m³ con 0,4 mg/L. En Nepal, el cloro costó de 0,06 a 0,09 USD por m³ {{c:nepal}}; con el tipo de cambio implícito del "
  "proyecto (159.991 COP, unos 40 USD), eso equivale a unos 240–360 COP por m³, más de diez veces el valor ideal. El cálculo estequiométrico es, por tanto, un piso y no una estimación del gasto real.")
H2("Tiempo de recuperación")
T(f"Con los supuestos del proyecto, una unidad usada por un solo hogar tiene un beneficio mensual bruto de 25.000 COP y se recupera en {f(C['payback_meses_1hogar_bruto'], 1)} meses; descontando el costo operativo de 15.000 COP, el tiempo sube a "
  f"{f(C['payback_meses_1hogar_neto'], 1)} meses y el valor presente neto a 12 meses es de {m(C['vpn_12m_neto_de_opex_1hogar'])} COP, es decir, negativo. Compartida por dos hogares, la recuperación baja a {f(pb['2'], 1)} meses; por tres, a {f(pb['3'], 1)}; y por diez, a {f(pb['10'], 1)} (Figura 3). "
  f"Sin restar el costo operativo, el valor presente neto a 12 meses es de {m(C['vpn_12m_solo_beneficio'])} COP; el documento del proyecto reporta 96.800 COP y no fue posible reproducir esa cifra con los datos "
  "disponibles, por lo que aquí se usa el cálculo propio.")
figura(["payback.png"], 8.0, "Figura 3. Tiempo de recuperación simple según el número de hogares que comparten una unidad (beneficio supuesto de 25.000 COP/mes por hogar).")
H2("Costo bajo frente a desempeño técnico")
T(f"La simulación del proyecto dio {f(b['adecuada'] / 10, 1)} % de escenarios en el rango de 0,2 a 0,5 mg/L (IC 95 %: {f(b['ic_adecuada'][0], 1)} a {f(b['ic_adecuada'][1], 1)} %) y {f(b['sub'] / 10, 1)} % por debajo. La dosis efectiva media fue de {f(b['dosis_efectiva_media'], 2)} mg/L frente a una demanda media supuesta de {f(b['demanda_media'], 2)} mg/L. "
  "Si esos supuestos se confirmaran, el ahorro estimado no se materializaría, porque el agua no quedaría protegida. Por eso la viabilidad económica de la Tabla 3 y la Figura 3 solo tiene sentido condicionada a que la calibración funcione.")

# ------------------------------------------------------------------ 4. Discusión
H1("Discusión")
T("Tres lecturas se desprenden. La primera es que el material es el menor de los costos. Lo que decide la sostenibilidad es lo que rodea al dispositivo: el suministro de pastillas, la capacitación y las visitas técnicas. "
  "En Honduras, la frecuencia de las visitas técnicas fue el mejor predictor del éxito {c:honduras}; en Kenia, Malawi y Uganda lo fue el conocimiento del uso correcto {c:kmu}. Ninguna de esas partidas está en el "
  "presupuesto de 159.991 COP, y deberían aparecer en un presupuesto de operación del piloto.")
T("La segunda es que compartir la unidad cambia el resultado. Con un hogar, la recuperación es de unos 16 meses con el costo operativo supuesto; con dos o más, baja de cinco meses. Eso sugiere que el diseño tiene sentido "
  "como infraestructura comunal, a cargo de la junta de acción comunal, y no como equipo doméstico. La evidencia de Dhaka apunta en el mismo sentido: los hogares de bajos ingresos tienen menos capacidad de pago por el servicio y podrían necesitar "
  "subsidios {c:dhaka}.")
T("La tercera es la más importante: el costo bajo no basta. La simulación indica que, con los supuestos actuales, el diseño casi nunca llega al rango. En los estudios revisados, el éxito dependió de que la dosis se ajustara a "
  "la fuente, y dispositivos de bajo costo mostraron consistencia desigual {c:guatemala,uganda,ghana}. Las limitaciones son claras: el beneficio mensual es un supuesto, la simulación usa distribuciones no medidas, el "
  "precio de las pastillas y su masa por paquete requieren confirmación, y no se midió la aceptación de la comunidad. Además, el rango de diseño del proyecto (0,2–0,5 mg/L) es más estrecho que el de la norma (0,3–2,0 mg/L).")

# ------------------------------------------------------------------ 5. Conclusiones
H1("Conclusiones")
T(f"El clorificador de PVC cuesta 159.991 COP en materiales y su cloro teórico cuesta entre {f(cm3['0.4']['COP_por_m3'], 1)} y {f(cm3['1.05']['COP_por_m3'], 1)} COP por m³, aunque el gasto real será mayor. Una unidad que sirva a un solo hogar se recupera en "
  f"{f(C['payback_meses_1hogar_neto'], 1)} meses con los supuestos del proyecto; compartida por tres, en {f(pb['3'], 1)}. Pero la viabilidad económica está condicionada a un desempeño técnico que la simulación actual no respalda "
  f"({f(b['adecuada'] / 10, 1)} % de cumplimiento). El prototipo está en TRL 3.")
H1("Recomendaciones")
T("(1) Medir en campo el consumo real de pastillas y confirmar su precio y masa. (2) Presupuestar capacitación y visitas técnicas del piloto. (3) Reemplazar el beneficio supuesto por una encuesta de gasto en agua y salud. "
  "(4) Evaluar el modelo de unidad comunal. (5) Ejecutar la validación técnica antes de cualquier cálculo de retorno a escala.")
declaraciones("Los cálculos económicos están en complemento.py y resultados_complemento.json.")
cierre(autores, TITULO_ES, "Costo, consumo de cloro y operación de un clorificador pasivo de PVC", Path(sys.argv[1]))
Path(sys.argv[1]).with_suffix(".txt").write_text("\n\n".join(f"[{e}] {t}" for e, t in LOG), encoding="utf-8")
