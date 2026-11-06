# Protocolo Físico: Medición de Caudal y Pérdidas de Carga Hidráulica

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación**: `03_Protocolos_y_Ensayos_Laboratorio/Protocolo_Fisico_Medicion_Caudal_y_Perdidas.md`

---

## 1. Objetivo del Ensayo Físico

Caracterizar hidráulicamente el prototipo de PVC determinando la curva de caudal ($Q$) frente al grado de apertura de las válvulas ($V_{\text{bp}}, V_{\text{in}}, V_{\text{out}}$) y cuantificando las pérdidas de carga en el circuito.

---

## 2. Equipos y Materiales Requeridos

1. Prototipo físico ensamblado en PVC de 1" y 2".
2. Tanque elevado alimentador de 100 L a 250 L (Cabeza constante de $2.0 \text{ m}$ de altura).
3. Probeta graduada de plástico/vidrio de $1,000 \text{ mL}$ o $2,000 \text{ mL}$ (Precisión $\pm 5 \text{ mL}$).
4. Cronómetro digital con precisión de $0.01 \text{ s}$.
5. Pie de rey / Flexómetro para verificar diámetros internos y alturas hidrostáticas.
6. Manómetros de tubo en U o sensores de presión diferencial a la entrada y salida del prototipo (opcional).

---

## 3. Procedimiento Paso a Paso (Aforo Volumétrico)

1. **Montaje e Inspección Inicial**:
   - Conectar la entrada del prototipo a la tubería de descarga del tanque elevado.
   - Verificar que no existan fugas en las uniones de PVC soldadas ni en las roscas de la cámara de 2".
   - Llenar el tanque alimentador hasta la marca de nivel máximo ($H_0 = 2.0 \text{ m}$).

2. **Ensayo 1: Curva de Apertura de Válvula de Bypass ($V_{\text{bp}}$)**:
   - Mantener las válvulas de la cámara de cloro ($V_{\text{in}}$ y $V_{\text{out}}$) cerradas ($0\%$).
   - Ajustar la válvula de bypass ($V_{\text{bp}}$) en 5 posiciones: $20\%$, $40\%$, $60\%$, $80\%$ y $100\%$ (Totalmente abierta).
   - Para cada posición, colocar la probeta graduada en la descarga de salida y accionar el cronómetro simultáneamente.
   - Capturar el tiempo ($t$) requerido para colectar $1,000 \text{ mL}$ ($1.0 \text{ L}$).
   - Repetir 3 veces cada medición (Triplicado experimental) para obtener la media y desviación estándar.

3. **Ensayo 2: División de Flujo (Bypass vs. Cámara de Contacto)**:
   - Configurar $V_{\text{bp}}$ al $50\%$.
   - Variar $V_{\text{in}}$ y $V_{\text{out}}$ al $25\%$, $50\%$, $75\%$ y $100\%$.
   - Registrar el caudal total $Q_{\text{total}} = \frac{V_{\text{colectado}}}{t}$.

4. **Cálculo Matemático de Caudal**:

$$Q = \frac{V}{t} \quad \left[\text{L/s}\right] \quad \text{o} \quad Q = \frac{V}{t} \cdot 60 \quad \left[\text{L/min}\right]$$

---

## 4. Registro y Criterios de Aceptación

- El coeficiente de variación ($CV = \frac{\sigma}{\mu} \cdot 100\%$) entre réplicas del mismo punto debe ser **menor al 5%**.
- Los datos se registrarán inmediatamente en la matriz de la carpeta `04_Toma_de_Datos_y_Seguimiento/Formato_Captura_Datos_Ensayos.csv`.
