# Guía Práctica: Lista de Chequeo, Equipos y Captura de Datos de Laboratorio

**Proyecto**: Prototipo Clorificador de Agua en PVC para la Comunidad El Vidrial.  
**Ubicación de Archivo**: `04_Toma_de_Datos_y_Seguimiento/Guia_Lista_de_Chequeo_y_Variables_Laboratorio.md`  
**Entidad**: Universidad Pontificia Bolivariana (UPB) - Semillero SILOGÍ

---

## 🧰 1. Lista de Chequeo (Checklist Pre-Ensayo)

Antes de iniciar cualquier jornada de pruebas en el laboratorio, asegúrate de contar con todos los elementos de la siguiente lista:

### A. Equipos e Hidráulica
- [ ] **Prototipo Físico en PVC**: Prototipo completo con sus 3 válvulas de bola de 1" y la cámara de 2".
- [ ] **Tanque Alimentador**: Tanque graduado de 100 L a 250 L colocado en altura ($1.5 \text{ m} \text{ a } 2.5 \text{ m}$ por gravedad).
- [ ] **Manguera / Conexión de 1"**: Acople flexible para conectar la descarga del tanque a la entrada del prototipo.
- [ ] **Cinta Teflón**: Para asegurar el sello del tapón roscado de 2" y evitar fugas de agua.

### B. Instrumentos de Medición de Caudal
- [ ] **Probeta Graduada de 1,000 mL (1 Litro)**: Limpia y sin residuos.
- [ ] **Cronómetro Digital**: Con precisión de $0.01 \text{ s}$.

### C. Reactivos e Instrumentos Químicos
- [ ] **Fotómetro Digital / Colorímetro para Cloro Libre**: Con sus celdas de vidrio de 10 mL.
- [ ] **Reactivo DPD No. 1**: Sachets/sobres o tabletas para cuantificación de Cloro Residual Libre.
- [ ] **Pastillas de Cloro Commercial**: Tricloro al 90% o Hipoclorito de Calcio (diámetro 1" o 2").
- [ ] **pHmetro Digital / Tiras Indicadoras**: Previamente calibrado con soluciones amortiguadoras pH 4.0 y 7.0.
- [ ] **Termómetro Digital de Laboratorio**.
- [ ] **Turbidímetro Digital**: Con celda óptica de lectura.
- [ ] **Paño de Microfibra Óptico**: Para limpiar las celdas de vidrio del fotómetro sin rayarlas ni dejar huellas dactilares.

### D. Registro de Datos
- [ ] **Hoja de Registro / Laptop**: Formato CSV cargado o impresión física de la tabla de bitácora.

---

## 📊 2. Tabla Estandarizada de Captura de Datos

Para cada corrida o ensayo ejecutado, se deben registrar cuantitativamente las siguientes **13 variables**:

| No. | Categoría | Variable a Registrar | Símbolo / Unidad | Instrumento o Método de Medición |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Identificación | ID del Ensayo / Corrida | Consecutivo (`#1, #2...`) | Registro correlativo |
| **2** | Identificación | Fecha y Hora Exacta | `YYYY-MM-DD HH:MM` | Reloj / Celular |
| **3** | Identificación | Número de Réplica | `Réplica 1, 2 o 3` | Diseño de experimentos (DOE) |
| **4** | **Configuración** | Posición Válvula Bypass | $\%V_{\text{bp}}$ ($\%$) | Graduación manual llave superior 1" ($25\%, 50\%, 75\%, 100\%$) |
| **5** | **Configuración** | Posición Válvula Entrada/Salida | $\%V_{\text{in}}, \%V_{\text{out}}$ ($\%$) | Graduación manual llaves verticales 1" ($50\%, 100\%$) |
| **6** | **Configuración** | Carga de Cloro en Cámara | $M_{\text{cloro}}$ (Pastillas) | Conteo físico al recargar (1 o 2 pastillas) |
| **7** | **Agua Cruda** | Temperatura del Agua | $T$ (${}^\circ\text{C}$) | Termómetro digital de laboratorio |
| **8** | **Agua Cruda** | pH Inicial del Agua | $\text{pH}$ (Unidades) | pHmetro digital |
| **9** | **Agua Cruda** | Turbidez Inicial del Agua | $\text{Turb}$ (NTU) | Turbidímetro óptico |
| **10**| **Resultado** | Tiempo Aforo Volumétrico | $t$ (segundos) | Cronómetro digital (tiempo para llenar 1.0 Litro) |
| **11**| **Resultado** | Caudal Calculado | $Q$ (L/s) | Fórmula: $Q = 1.0 / t$ |
| **12**| **Resultado** | **Cloro Residual Libre** | **$C_{\text{res}}$ (mg/L)** | **Fotómetro digital + Reactivo DPD No. 1** |
| **13**| **Resultado** | Estado de Cloración | *Categoría* | *Subclorada* ($<0.2$) / *Adecuada* ($0.2-0.5$) / *Sobreclorada* ($>0.5$) |

---

## 📝 3. Ejemplo Práctico de Registro Diario

```text
ID Ensayo: #1
Fecha: 2026-09-21 09:30 AM | Réplica: 1
Válvula Bypass: 50% | Válvulas Cámara: 100% | Carga Cloro: 1 Pastilla
Temperatura: 28.5 °C | pH: 7.2 | Turbidez: 0.5 NTU
Tiempo de Aforo: 2.45 s (para 1.0 L) --> Caudal Q = 0.408 L/s
Cloro Libre DPD: 0.38 mg/L
Estado: ADECUADA (Cumple Resolución 2115 de 2007)
```

---

## 🔬 4. Resumen Rápido del Protocolo de Muestreo

1. **Estabilización (2 min)**: Dejar fluir el agua a través del prototipo durante 2 minutos antes de tomar la muestra para eliminar burbujas y estabilizar la mezcla.
2. **Medición de Caudal**: Llenar la probeta de $1,000 \text{ mL}$ midiendo el tiempo exacto con el cronómetro.
3. **Muestra para DPD**:
   - Enjuagar la celda de vidrio 3 veces con el agua tratada.
   - Llenar hasta la marca de $10 \text{ mL}$.
   - Agregar 1 sachet de **DPD No. 1** y agitar suavemente por inversión durante 10-15 s.
   - Limpiar el vidrio por fuera con el paño de microfibra.
   - Leer en el fotómetro **antes de 1 minuto** (a los 20-30 s).
4. **Verificación Normativa**:
   - **$C_{\text{res}} < 0.20 \text{ mg/L}$**: Subclorada (Riesgo biológico).
   - **$0.20 \le C_{\text{res}} \le 0.50 \text{ mg/L}$**: **Adecuada / Óptima** (Cumple norma).
   - **$C_{\text{res}} > 0.50 \text{ mg/L}$**: Sobreclorada (Riesgo de mal sabor y subproductos).
