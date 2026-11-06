# Diseño de Experimentos Estadísticos (DOE) y Plan de Validación

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación**: `03_Protocolos_y_Ensayos_Laboratorio/Diseño_de_Experimentos_Estadisticos_DOE.md`

---

## 1. Definición del Arreglo Experimental

Para validar cuantitativamente el desempeño del prototipo clorificador en PVC, se implementa un **Diseño Factorial Completo $2^3$ con 3 Réplicas** ($2^3 \times 3 = 24$ corridas experimentales en total).

### Factores Evaluados y Niveles (Variables Independientes):

| Factor | Variable | Nivel Bajo ($-1$) | Nivel Alto ($+1$) | Unidad |
| :---: | :--- | :---: | :---: | :---: |
| **A** | Caudal de Entrada ($Q$) | $0.5$ (Bajo) | $1.5$ (Alto) | L/s |
| **B** | Apertura Válvula Bypass ($V_{\text{bp}}$) | $25\%$ (Restringido) | $75\%$ (Abierto) | $\%$ |
| **C** | Carga de Cloro en Cámara | 1 Pastilla | 2 Pastillas | Unidades |

### Variable de Respuesta (Dependiente):
- **$Y_1 = C_{\text{res}}$**: Concentración de Cloro Residual Libre ($\text{mg/L}$) medida a la salida por el método DPD.
- **$Y_2 = \Delta P$**: Pérdida de carga hidráulica / caída de presión ($\text{m.c.a.}$).

---

## 2. Matriz del Diseño Factorial $2^3$

| Corrida | Factor A ($Q$) | Factor B ($V_{\text{bp}}$) | Factor C (Pastillas) | Configuración Experimental |
| :---: | :---: | :---: | :---: | :--- |
| 1 | $-1$ | $-1$ | $-1$ | $Q=0.5 \text{ L/s}$, $V_{\text{bp}}=25\%$, 1 Pastilla |
| 2 | $+1$ | $-1$ | $-1$ | $Q=1.5 \text{ L/s}$, $V_{\text{bp}}=25\%$, 1 Pastilla |
| 3 | $-1$ | $+1$ | $-1$ | $Q=0.5 \text{ L/s}$, $V_{\text{bp}}=75\%$, 1 Pastilla |
| 4 | $+1$ | $+1$ | $-1$ | $Q=1.5 \text{ L/s}$, $V_{\text{bp}}=75\%$, 1 Pastilla |
| 5 | $-1$ | $-1$ | $+1$ | $Q=0.5 \text{ L/s}$, $V_{\text{bp}}=25\%$, 2 Pastillas |
| 6 | $+1$ | $-1$ | $+1$ | $Q=1.5 \text{ L/s}$, $V_{\text{bp}}=25\%$, 2 Pastillas |
| 7 | $-1$ | $+1$ | $+1$ | $Q=0.5 \text{ L/s}$, $V_{\text{bp}}=75\%$, 2 Pastillas |
| 8 | $+1$ | $+1$ | $+1$ | $Q=1.5 \text{ L/s}$, $V_{\text{bp}}=75\%$, 2 Pastillas |

*Cada combinación se ejecuta en 3 réplicas aleatorizadas (Semana 2).*

---

## 3. Pruebas Estadísticas de Hipótesis

### 3.1 Pruebas de Supuestos
1. **Prueba de Normalidad de Residuos**: Prueba de Shapiro-Wilk ($\alpha = 0.05$). Hipótesis nula $H_0$: Los residuos siguen una distribución normal.
2. **Prueba de Homocedasticidad**: Prueba de Levene / Bartlett para igualdad de varianzas.

### 3.2 Análisis de Varianza (ANOVA de 3 Vías)
Se evalúa el efecto principal de cada factor y las interacciones ($A \times B$, $A \times C$, $B \times C$, $A \times B \times C$).
- **Criterio de Significación**: Valor $p < 0.05$ indica que el factor o interacción afecta significativamente la concentración de cloro residual libre.

### 3.3 Prueba t de Student para Muestra Única (Verificación Normativa)
Se prueba si el valor medio experimental $\mu_{C_{\text{res}}}$ es significativamente conforme con el rango normativo de la Resolución 2115:

$$H_0: \mu_{C_{\text{res}}} = 0.35 \text{ mg/L} \quad \text{vs.} \quad H_1: \mu_{C_{\text{res}}} \ne 0.35 \text{ mg/L}$$

---

## 4. Comparación con Simulación Monte Carlo

Los datos recolectados en laboratorio se contrastarán mediante la prueba de Chi-cuadrado / Kolmogorov-Smirnov frente a los $1,000$ escenarios simulados en el archivo `montecarlo_clorificador.ipynb` para ajustar los coeficientes de aceleración por temperatura ($T_{\text{factor}}$) y turbidez ($turb_{\text{factor}}$).
