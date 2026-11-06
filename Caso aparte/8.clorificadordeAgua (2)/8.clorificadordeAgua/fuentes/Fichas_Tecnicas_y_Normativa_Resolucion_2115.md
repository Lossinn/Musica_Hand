# Resumen Normativo y Fichas Técnicas del Sistema de Cloración

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial, Montería.  
**Ubicación de Archivo**: `fuentes/Fichas_Tecnicas_y_Normativa_Resolucion_2115.md`

---

## 1. Normativa Sanitaria Colombiana: Resolución 2115 de 2007

La **Resolución 2115 de 2007** dictada conjuntamente por el Ministerio de la Protección Social y el Ministerio de Ambiente, Vivienda y Desarrollo Territorial regula las características químicas, físicas y microbiológicas del agua para consumo humano en Colombia.

### Parámetros Clave para el Prototipo:

| Parámetro | Unidad | Rango Aceptable (Norma) | Valor Objetivo en Prototipo | Justificación Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **Cloro Residual Libre ($C_{\text{res}}$)** | mg/L | $0.2 \text{ a } 2.0 \text{ mg/L}$ | **$0.2 \text{ a } 0.5 \text{ mg/L}$** | Garantiza desinfección efectiva previniendo la formación de trihalometanos (THMs) y sabores/olores desagradables. |
| **Turbidez** | NTU | $\le 2.0 \text{ NTU}$ | $\le 1.0 \text{ NTU}$ | Alta turbidez interfiere con la acción del cloro por apantallamiento de microbios. |
| **pH** | Unidad pH | $6.5 \text{ a } 9.0$ | $6.8 \text{ a } 7.5$ | El ácido hipocloroso ($\text{HOCl}$, forma desinfectante más activa) predomina a $\text{pH} < 7.5$. |
| **Color Aparente** | UPC | $\le 15 \text{ UPC}$ | $\le 5 \text{ UPC}$ | Aceptabilidad estética por parte de la comunidad. |
| **Coliformes Totales / E. coli** | UFC/100 mL | $0 \text{ UFC/100 mL}$ | $0 \text{ UFC/100 mL}$ | Inactivación microbiológica total exigida por ley. |

---

## 2. Ficha Técnica del Prototipo en PVC

### Materiales y Componentes Físicos

1. **Cámara de Dosificación (Pastillas)**:
   - **Tubería**: PVC Presión RDE 21 / Schedule 40 de 2 pulgadas (diámetro nominal).
   - **Accesorios**: 1 Tee de presión 2", 1 Codo de presión 2", 1 Conector macho 2" para recarga.
   - **Bujes de Reducción**: 2 Bujes PVC de $2" \times 1"$.

2. **Línea de Bypass y Regulación de Flujo**:
   - **Tubería de Bypass**: PVC Presión RDE 21 / Schedule 40 de 1 pulgada (longitud total $1.30 \text{ m}$).
   - **Válvulas de Control**: 3 Válvulas / Llaves de bola PVC de 1 pulgada.
     - *Válvula 1 ($V_{\text{bp}}$)*: Controla el flujo por la tubería de bypass directa.
     - *Válvula 2 ($V_{\text{in}}$)*: Regula la entrada de agua a la cámara de pastillas de 2".
     - *Válvula 3 ($V_{\text{out}}$)*: Regula la salida de la corriente concentrada con cloro hacia la mezcla principal.
   - **Accesorios adicionales**: 2 Tees PVC 1", 1 Tapón PVC 1", Soldadura líquida para PVC y limpiador.

3. **Pastillas de Cloro Utilizadas**:
   - **Composición**: Tricloro-s-triazinatriona ($\text{C}_3\text{Cl}_3\text{N}_3\text{O}_3$, TCCA) al 90% de cloro disponible, o Hipoclorito de Calcio ($\text{Ca(ClO)}_2$) al 65-70%.
   - **Mecanismo de Desinfección**: Disolución pasiva por contacto con el flujo derivado a través de la cámara de 2".

---

## 3. Cinética de Cloración y Química del Proceso

La reacción de disolución y formación de ácido hipocloroso ($\text{HOCl}$) y ion hipoclorito ($\text{OCl}^-$) en agua es:

$$\text{HOCl} \rightleftharpoons \text{H}^+ + \text{OCl}^- \quad (pK_a \approx 7.53 \text{ a } 25^\circ\text{C})$$

A $\text{pH} = 7.2$, el **$68\%$** del cloro libre se encuentra como $\text{HOCl}$ (potente germicida, 80 veces más eficaz que el $\text{OCl}^-$).

La concentración final de cloro residual libre en la mezcla ($C_{\text{mezcla}}$) se modela mediante el balance de masa hidráulico:

$$C_{\text{mezcla}} = \frac{Q_{\text{cámara}} \cdot C_{\text{cámara}} + Q_{\text{bypass}} \cdot C_{\text{entrada}}}{Q_{\text{total}}}$$

donde:
- $Q_{\text{total}} = Q_{\text{cámara}} + Q_{\text{bypass}}$
- $C_{\text{cámara}}$ depende de la tasa de erosión de la pastilla de cloro y del tiempo de residencia hidráulica en la cámara de 2".
