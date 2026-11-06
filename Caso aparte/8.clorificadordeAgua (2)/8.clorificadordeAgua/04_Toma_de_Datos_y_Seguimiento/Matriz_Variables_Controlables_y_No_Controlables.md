# Matriz de Seguimiento de Variables del Sistema

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación**: `04_Toma_de_Datos_y_Seguimiento/Matriz_Variables_Controlables_y_No_Controlables.md`

---

## 1. Matriz de Categorización de Variables

| Categoría | Variable | Símbolo | Unidad | Rango de Operación | Instrumento de Medición | Impacto en el Sistema |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Controlable (Independiente)** | Apertura Válvula Bypass | $\%V_{\text{bp}}$ | $\%$ | $0\% - 100\%$ | Regla graduada / Posición manual | Modula la proporción del caudal desviado sin desinfectar. |
| **Controlable (Independiente)** | Apertura Válvulas Cámara | $\%V_{\text{in}}, \%V_{\text{out}}$ | $\%$ | $0\% - 100\%$ | Posición manual | Modula el caudal que contacta con la pastilla de cloro. |
| **Controlable (Independiente)** | Carga de Cloro | $M_{\text{cloro}}$ | Unidades / g | $1 - 2$ pastillas ($20 - 40 \text{ g}$) | Balanza analítica / Recarga física | Define la masa de sólido expuesta a erosión. |
| **Controlable (Independiente)** | Tiempo de Contacto | $t_{\text{contacto}}$ | min | $15 - 60$ min | Cronómetro | Inactivación de patógenos en tanque retenedor. |
| **No Controlable (Perturbación)** | Presión de Cabeza | $H_{\text{cabeza}}$ | m.c.a. | $1.0 - 2.5$ m | Flexómetro / Nivel de tanque | Varía el caudal $Q$ por nivel variable del tanque. |
| **No Controlable (Perturbación)** | Temperatura del Agua | $T$ | ${}^\circ\text{C}$ | $22 - 32 {}^\circ\text{C}$ | Termómetro digital / Multiparámetro | Altera la constante cinética de disolución y decaimiento. |
| **No Controlable (Perturbación)** | Turbidez Inicial | $\text{Turb}$ | NTU | $0.2 - 10.0$ NTU | Turbidímetro óptico | Consume cloro por reacción con materia orgánica. |
| **No Controlable (Perturbación)** | pH Inicial del Agua | $\text{pH}$ | Unidades | $6.5 - 8.2$ | pHmetro de electrodo de vidrio | Desplaza el equilibrio $\text{HOCl} \rightleftharpoons \text{OCl}^-$. |
| **Respuesta (Dependiente)** | Caudal Total | $Q_{\text{total}}$ | L/s | $0.2 - 2.5$ L/s | Probeta graduada y cronómetro | Capacidad de abastecimiento en L/s. |
| **Respuesta (Dependiente)** | Cloro Residual Libre | $C_{\text{res}}$ | mg/L | $0.2 - 0.5$ mg/L | Fotómetro DPD | Cumplimiento normativo y seguridad hídrica. |
