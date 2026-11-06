# Cronograma y Guía Paso a Paso: 2 Semanas de Ensayos en Laboratorio

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación**: `03_Protocolos_y_Ensayos_Laboratorio/Plan_Paso_a_Paso_2_Semanas_Laboratorio.md`  
**Duración Total**: 14 Días Calendario (2 Semanas intensivas).

---

## 📅 SEMANA 1: Puesta a Punto Hidráulica y Calibración Físico-Química

### **Día 1 (Lunes): Verificación Estructural y Prueba de Hermeticidad**
- **Objetivo**: Garantizar que el prototipo ensamblado en PVC no presente fugas ni desprendimientos.
- **Acciones**:
  1. Instalar el prototipo en el banco de pruebas de hidráulica.
  2. Conectar la tubería de entrada al tanque alimentador a una cabeza hidrostática de $2.0 \text{ m}$.
  3. Llenar el sistema con agua sin cloración y mantener la presión durante $30 \text{ minutos}$.
  4. Inspeccionar visualmente las uniones soldadas de 1" y 2", codos y válvulas.
  5. Registrar en la bitácora la aprobación de hermeticidad.

### **Día 2 (Martes): Calibración Volumétrica del Caudal ($Q$) vs. Apertura Válvula Bypass**
- **Objetivo**: Establecer la curva de calibración hidráulica del prototipo.
- **Acciones**:
  1. Fijar las válvulas de cámara en $0\%$ (cerradas).
  2. Variar la válvula de bypass ($V_{\text{bp}}$) en 5 posiciones: $20\%$, $40\%$, $60\%$, $80\%$, $100\%$.
  3. Ejecutar 3 aforos volumétricos por posición utilizando probeta de $1,000 \text{ mL}$ y cronómetro.
  4. Calcular el caudal medio $Q$ en $\text{L/s}$ y $\text{L/min}$.
  5. Graficar $Q$ vs. $\%$ Apertura de Válvula.

### **Día 3 (Miércoles): Caracterización de Pérdidas de Carga y Caída de Presión**
- **Objetivo**: Medir la resistencia hidráulica del bypass y cámara de 2".
- **Acciones**:
  1. Abrir las válvulas de cámara $V_{\text{in}}$ y $V_{\text{out}}$ al $50\%$.
  2. Variar el nivel del tanque alimentador desde $2.5 \text{ m}$ hasta $1.0 \text{ m}$ para simular la vaciada del tanque en la comunidad rural.
  3. Medir la variación del caudal de descarga.
  4. Identificar el caudal crítico mínimo de operación.

### **Día 4 (Jueves): Línea Base de Calidad de Agua de Prueba y Blancos DPD**
- **Objetivo**: Calibrar el medidor DPD y caracterizar el agua bruta de laboratorio.
- **Acciones**:
  1. Preparar 50 L de agua de ensayo en el tanque alimentador.
  2. Medir pH, Temperatura y Turbidez inicial.
  3. Realizar 5 mediciones de blanco con Reactivo DPD No. 1 para verificar lectura en $0.00 \text{ mg/L}$.

### **Día 5 (Viernes): Primer Ensayo de Cloración Continua (Línea Base 1 Pastilla)**
- **Objetivo**: Evaluar la disolución pasiva inicial de la pastilla de cloro.
- **Acciones**:
  1. Insertar 1 pastilla de Tricloro de 1" o 2" en la cámara de 2" de PVC.
  2. Fijar $V_{\text{bp}} = 50\%$, $V_{\text{in}} = 50\%$, $V_{\text{out}} = 50\%$.
  3. Iniciar el flujo de agua y tomar muestras a la salida a los $5, 10, 15, 30 \text{ y } 60 \text{ minutos}$.
  4. Medir cloro residual libre por DPD. Ver si se encuentra en el rango objetivo ($0.2 - 0.5 \text{ mg/L}$).

---

## 📅 SEMANA 2: Diseño de Experimentos Factorial (DOE) y Análisis Estadístico

### **Día 6 (Lunes): Preparación del Diseño Factorial $2^3$**
- **Objetivo**: Configurar las condiciones experimentales del DOE.
- **Acciones**:
  1. Preparar la hoja de aleatorización de las 24 corridas (8 tratamientos $\times$ 3 réplicas).
  2. Reinstalar la instrumentación y verificar la cantidad de pastillas de cloro comercial disponibles.

### **Día 7 (Martes): Ejecución de Réplica 1 del DOE (Corridas 1 a 8)**
- **Objetivo**: Recolectar el primer bloque de datos experimentales.
- **Acciones**:
  1. Ajustar los factores según la matriz del DOE (Caudal $Q$, Válvula Bypass $V_{\text{bp}}$, Pastillas).
  2. Para cada corrida, estabilizar el sistema por $3 \text{ minutos}$ y tomar muestra de $10 \text{ mL}$.
  3. Aplicar reactivo DPD No. 1 y registrar $C_{\text{res}}$ en la hoja CSV.

### **Día 8 (Miércoles): Ejecución de Réplicas 2 y 3 del DOE (Corridas 9 a 24)**
- **Objetivo**: Completar las réplicas del diseño factorial.
- **Acciones**:
  1. Ejecutar las réplicas restantes en orden totalmente aleatorizado.
  2. Medir y registrar la temperatura del agua en cada corrida para efectuar correcciones cinéticas.

### **Día 9 (Jueves): Pruebas de Sensibilidad a la Turbidez (Perturbación Exógena)**
- **Objetivo**: Simular el agua de río con turbidez elevada (Temporada de lluvias).
- **Acciones**:
  1. Adicionar caolín o arcilla sintética al tanque para ajustar la turbidez a $5.0 \text{ NTU}$ y $10.0 \text{ NTU}$.
  2. Medir el consumo extra de cloro por demanda orgánica y el impacto en $C_{\text{res}}$.

### **Día 10 (Viernes): Procesamiento Estadístico (ANOVA, Shapiro-Wilk y Prueba t)**
- **Objetivo**: Analizar cuantitativamente los resultados.
- **Acciones**:
  1. Cargar el archivo CSV en Python o Excel.
  2. Ejecutar la prueba de Shapiro-Wilk para comprobar la normalidad de residuos.
  3. Correr el ANOVA de 3 vías y determinar los factores estadísticamente significativos ($p < 0.05$).
  4. Realizar la prueba t para verificar cumplimiento del intervalo $[0.2, 0.5] \text{ mg/L}$.

### **Día 11 a 14 (Fin de Semana y Cierre): Validación vs. Monte Carlo e Informe Final**
- **Objetivo**: Consolidación final y documentación.
- **Acciones**:
  1. Comparar la distribución empírica de $C_{\text{res}}$ con el histograma generado por la simulación Monte Carlo (`montecarlo_clorificador.ipynb`).
  2. Completar la bitácora del proyecto y redactar el capítulo de resultados del informe final.
