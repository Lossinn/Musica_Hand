# 🎨 Plantilla de Contenido para Póster Científico Oficial (90 x 120 cm)
### Universidad Pontificia Bolivariana — Seccional Montería
**Facultad de Ingeniería Industrial // Grupo de Investigación SILOGE // Hub Industrial Solution (HIS)**  
**Periodo Académico:** 2026-2 &nbsp;|&nbsp; **Docente:** M.Sc. Cristian Javier Cano Mogollón  

---

> [!IMPORTANT]
> **ESPECIFICACIONES TÉCNICAS DE IDENTIDAD VISUAL HIS (MEMORIAS HIS 2025-2026)**
> - **Dimensiones Oficiales:** **90 cm de ancho $\times$ 120 cm de alto** (Orientación Vertical / Portrait).
> - **Fondo Oficial:** Textura de Cartón Corrugado (`assets/backgrounds/fondoCorrugado.jpg`) con capa sutil de papel kraft translúcido al 94% y marca de agua central HIS al 5%.
> - **Paleta de Colores Industrial HIS (`config/styles.tex`):**
>   - `HISYellow` (`#FFCC00`): Amarillo Industrial de alto contraste para acentos, títulos y tarjetas KPI.
>   - `HISBlack` (`#141414`): Negro Industrial Mate para marcos, textos de títulos y cabeceras.
>   - `SoftGray` (`#F5F5F5`) & `DarkGray` (`#404040`): Fondos de tarjetas y subtítulos.
> - **Tipografía:** Sans-serif técnica industrial (`Helvetica`, `Inter`, `Montserrat` con títulos en mayúsculas negrita sostenida).
> - **Logotipos Obligatorios en Cabecera:**
>   1. Escudo Oficial UPB / 30 Años (`assets/logos/upb_30a.png` o `logo_upb.png`) a la izquierda.
>   2. Logo Oficial HIS — Hub de Soluciones Industriales (`assets/logos/logo_his.png`) al centro/derecha.
>   3. Logo Semillero SILOGE (`assets/logos/logo_siloge.jpeg`) a la derecha.
> - **Herramientas de Maquetación Aceptadas:**
>   - Plantilla HTML5/CSS3 interactiva provista (`plantilla_poster_cientifico.html`), imprimible directamente desde Google Chrome / Edge con `Cmd + P` o `Ctrl + P` (Configuración: Tamaño 900x1200 mm, Márgenes Ninguno, Guardar como PDF).
>   - PowerPoint / Canva / Illustrator / InDesign configurando el lienzo en **90 cm $\times$ 120 cm** con los activos de la subcarpeta `assets/`.

---

## 📋 Estructura de Contenido del Póster (Sección por Sección)

A continuación se detalla la información que cada equipo debe preparar y sintetizar:

### 1. Cabecera Institucional
* **Título del Proyecto:** Estructurado según la fórmula canónica de ingeniería:  
  `[Acción/Variable Independiente] + [Efecto/Variable Dependiente] + [Población/Empresa] + [Montería/Córdoba] + [2026]`  
  *(Ejemplo: Optimización de Rutas de Recolección de Biomasa mediante Algoritmos Genéticos en Cereté, Córdoba, 2026).*
* **Subtítulo:** Enfoque tecnológico o metodológico principal.
* **Integrantes del Equipo:** Nombres y apellidos completos, código de estudiante y correos institucionales.
* **Docente Asesor:** M.Sc. Cristian Javier Cano Mogollón.
* **Filiación:** Facultad de Ingeniería Industrial, Semillero SILOGE, Universidad Pontificia Bolivariana Seccional Montería.

---

### 2. Columna Izquierda: Contexto, Problema y Fundamentación Científica
* **2.1 Problemática Regional & Justificación:**
  - Diagnóstico cuantitativo de la situación actual en la empresa o sector asignado de Montería/Córdoba.
  - Causas raíz y efectos directos (sustentados en el Árbol de Problemas MML).
  - Objetivos de Desarrollo Sostenible (ODS) directamente impactados (ej. ODS 9: Industria, Innovación e Infraestructura; ODS 12: Producción y Consumo Responsables).
* **2.2 Objetivos & Pregunta Central de Investigación:**
  - Pregunta formal de investigación.
  - Objetivo General (verbo en infinitivo accionable).
  - 3 Objetivos Específicos jerarquizados (Diagnóstico $\to$ Modelado/Desarrollo $\to$ Validación/Evaluación).
* **2.3 Estado del Arte & Matriz Bibliométrica:**
  - Mapeo de literatura en **Scopus, Web of Science o PubMed** (mínimo 12-15 artículos, 2021-2026).
  - Enlaces **DOI activos y verificados**.
  - Identificación explícita de la **Brecha de Investigación (*Research Gap*)**.

---

### 3. Columna Central: Arquitectura Técnica, Procesos & Gobernanza
* **3.1 Modelado de Procesos (BPMN / Árbol de Objetivos):**
  - Diagrama de flujo bajo estándar BPMN 2.0 (carriles de responsabilidad *swimlanes*, compuertas lógicas y eventos).
  - Transición del proceso actual (*As-Is*) al proceso tecnificado (*To-Be*).
* **3.2 Diagramas de Flujos de Datos (DFD):**
  - DFD Nivel 0 (Contexto del sistema, fuentes y consumidores externos).
  - DFD Nivel 1 (Subsistemas de ingesta, procesamiento, optimización y visualización).
* **3.3 Gobernanza de Datos (Data Governance):**
  - Diccionario de variables críticas y tipos de datos.
  - Linaje del dato (*Data Lineage* desde el origen hasta el cuadro de mando).
  - Protocolos de calidad (completitud, consistencia, exactitud) y seguridad de la información.

---

### 4. Columna Derecha: Desarrollo/Interfaces, Análisis Financiero (ROI) y Proyección
* **4.1 Desarrollo Tecnológico & Interfaces:**
  - Evidencia visual del desarrollo realizado (mockups de alta fidelidad, capturas del aplicativo web en Streamlit/FastHTML, arquitectura del prototipo maker o gemelo digital).
  - Explicación de cómo este desarrollo conduce directamente al cumplimiento de los objetivos específicos.
* **4.2 Retorno de Inversión (ROI) y Factibilidad Financiera:**
  - Cuadro de costos de inversión inicial (**CAPEX**) y costos operativos (**OPEX**).
  - Cuantificación de ahorros operativos / beneficios económicos anuales generados.
  - **Tarjeta Destacada de KPI:**
    - Porcentaje de ROI Calculado: $\text{ROI} = \frac{\text{Beneficio Neto}}{\text{CAPEX}} \times 100\%$
    - Periodo de Recuperación de la Inversión (*Payback Period* en meses).
* **4.3 Resultados Preliminares & Proyección de Impacto:**
  - Reducción esperada en tiempos de ciclo, costos de merma o incremento de productividad.
  - Viabilidad de escalabilidad regional.
* **4.4 Código QR Interactivo:**
  - Enlace dinámico hacia el video de demostración, repositorio de código (GitHub) o memoria técnica en la plataforma ZERO.

---

## 📐 Consejos Visuales para la Maquetación
1. **Regla del 40 - 30 - 30:** 40% elementos visuales (diagramas, interfaces, gráficos), 30% espacio en blanco / descanso visual, 30% texto técnico conciso.
2. **Jerarquía Tipográfica:** Los títulos deben leerse cómodamente a 2 metros de distancia; el texto de cuerpo a 1 metro.
3. **Imágenes en Alta Resolución:** No usar capturas de pantalla pixeladas. Los diagramas deben exportarse en formato SVG o PNG a 300 DPI.
4. **Cero Párrafos Extensos:** Emplear listas de viñetas estructuradas y tarjetas tipo KPI para destacar métricas clave.
