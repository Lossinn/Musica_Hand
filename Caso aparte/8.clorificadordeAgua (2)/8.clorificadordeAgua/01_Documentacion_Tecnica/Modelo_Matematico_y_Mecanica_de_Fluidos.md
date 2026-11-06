# Modelo Matemático y Mecánica de Fluidos Aplicada al Clorificador

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación**: `01_Documentacion_Tecnica/Modelo_Matematico_y_Mecanica_de_Fluidos.md`

---

## 1. Conservación de Masa e Hidráulica del Bypass

El flujo volumétrico total $Q_{\text{total}}$ que atraviesa el prototipo se divide en dos ramales en paralelo:

$$Q_{\text{total}} = Q_{\text{bypass}} + Q_{\text{cámara}}$$

Por la ecuación de energía de Bernoulli con pérdidas de carga entre los nodos de división y mezcla:

$$h_{L, \text{bypass}} = h_{L, \text{cámara}}$$

donde las pérdidas de carga hidráulica $h_L$ se componen de pérdidas mayores por fricción ($h_f$) y pérdidas menores por accesorios ($h_m$):

$$h_L = f \cdot \frac{L}{D} \cdot \frac{v^2}{2g} + \sum K_m \cdot \frac{v^2}{2g}$$

- $K_m$ para válvulas de bola 1": varía desde $K \approx 0.05$ (100% abierta) hasta $K \to \infty$ (cerrada).
- La relación de división del caudal $\alpha = \frac{Q_{\text{cámara}}}{Q_{\text{total}}}$ es modulada directamente ajustando las aperturas relativas de las 3 válvulas.

---

## 2. Cinética de Disolución y Masa de Cloro Libreado

La tasa de transferencia de masa de cloro desde la pastilla sólida a la fase líquida en la cámara de 2" se rige por la ley de difusión/erosión de Noyes-Whitney / Nernst-Bruner:

$$\frac{dM_{\text{cloro}}}{dt} = k_d \cdot A_s \cdot (C_{\text{sat}} - C_{\text{cámara}})$$

donde:
- $k_d$: Coeficiente global de transferencia de masa por erosión hidráulica ($\text{m/s}$), el cual escala proporcionalmente con la velocidad local $v_{\text{cámara}} = \frac{Q_{\text{cámara}}}{A_{\text{cámara}}}$.
- $A_s$: Área superficial expuesta de las pastillas sólidas ($\text{m}^2$).
- $C_{\text{sat}}$: Solubilidad de saturación del Tricloro/Hipoclorito ($\text{mg/L}$).

Concentración de cloro en la cámara de contacto:

$$C_{\text{cámara}} = \frac{\frac{dM_{\text{cloro}}}{dt}}{Q_{\text{cámara}}} = \frac{k_d \cdot A_s \cdot C_{\text{sat}}}{Q_{\text{cámara}} + k_d \cdot A_s}$$

---

## 3. Balance de Mezcla y Concentración Residual Final

Al recombinarse los flujos en el nodo de mezcla final:

$$C_{\text{salida}} = \frac{Q_{\text{cámara}} \cdot C_{\text{cámara}} + Q_{\text{bypass}} \cdot C_{\text{entrada}}}{Q_{\text{total}}}$$

Considerando que el agua bruta de pozo/río carece de cloro libre ($C_{\text{entrada}} = 0$), la ecuación se simplifica a:

$$C_{\text{salida}} = \alpha \cdot C_{\text{cámara}} = \frac{Q_{\text{cámara}}}{Q_{\text{total}}} \cdot C_{\text{cámara}}$$

### Ecuación de Corrección por Demanda y Factores Ambientales:

Para determinar el cloro residual neto disponible $C_{\text{res}}$ tras reaccionar con la materia orgánica e inorgánica ($D_{\text{demanda}}$):

$$C_{\text{res}} = \max\left( \frac{(C_{\text{salida}} - D_{\text{demanda}}) \cdot e^{-k_{\text{decay}} \cdot t_{\text{contacto}}}}{f_T \cdot f_{\text{pH}} \cdot f_{\text{turb}}}, 0 \right)$$

donde los factores de penalización calibrados en el modelo Monte Carlo son:
- $f_T = e^{0.03 \cdot (T - 25)}$ (Efecto de la temperatura en ${}^\circ\text{C}$).
- $f_{\text{pH}} = 1 + 0.06 \cdot |\text{pH} - 7.2|$ (Desviación del pH óptimo).
- $f_{\text{turb}} = 1 + 0.15 \cdot \text{Turbidez (NTU)}$ (Consumo por sólidos suspendidos).

---

## 4. Función Objetivo de Optimización

El objetivo técnico de operación del prototipo es minimizar la desviación cuadrática respecto al valor meta de $0.4 \text{ mg/L}$ de cloro residual libre:

$$\min_{V_{\text{bp}}, V_{\text{in}}, V_{\text{out}}} J = \sum_{i=1}^{N} \left( C_{\text{res}, i} - 0.4 \right)^2$$

Sujeto a las restricciones:
1. $0.2 \text{ mg/L} \le C_{\text{res}} \le 0.5 \text{ mg/L}$
2. $Q_{\text{min}} \le Q_{\text{total}} \le Q_{\text{max}}$
3. $\text{Turbidez} \le 2.0 \text{ NTU}$
