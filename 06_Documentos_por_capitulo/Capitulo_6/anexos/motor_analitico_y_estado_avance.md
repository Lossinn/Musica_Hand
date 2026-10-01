# Motor Analítico y Estado de Avance del Software Hand Sing Kids

**Sistema:** Hand Sing Kids (v2.0)  
**Dominio:** Reconocimiento de Visión Artificial, Analítica Adaptativa y Gamificación Musical Infantil  
**Fecha:** Septiembre 2026  

---

## 1. Funcionamiento del Motor Analítico

El **Motor Analítico** de *Hand Sing Kids* es el núcleo computacional y predictivo encargado de transformar flujos continuos de datos sensoriales (visión artificial) en métricas de aprendizaje, diagnósticos de rendimiento psicomotriz/musical y decisiones didácticas adaptativas en tiempo real.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ARQUITECTURA DEL MOTOR ANALÍTICO                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

  [ ENTRADA SENSORIAL ]
  Cámara Web (RGB @ 30 FPS) ──► MediaPipe Hands (21 Landmarks x 2 Manos = 42 Puntos 3D)
                                            │
                                            ▼
  [ NORMALIZACIÓN Y PREPROCESAMIENTO ]
  Invarianza Euclidiana ──────► Traslación a Muñeca / Escalamiento MCP-Muñeca / Rotación 2D
                                            │
                                            ▼
  [ EXTRACCIÓN DE CARACTERÍSTICAS ]
  Vector Físico y Angular ────► Vector numérico $\vec{v} \in \mathbb{R}^{38}$ (Ángulos articulares, distancias interdigitales)
                                            │
                                            ▼
  [ CLASIFICACIÓN Y ESTABILIZACIÓN ]
  Similitud Cosina + Filtro ──► Comparación contra plantillas calibradas (k-NN / Cosine)
                                Filtro de Histéresis Temporal ($N=3$ frames, Debounce, Cooldown)
                                            │
                                            ▼
  [ EVALUACIÓN MUSICAL Y REGISTRO ]
  Comparador de Secuencia ────► Acierto/Fallo, Latencia de Reacción ($T_{reacción}$ ms), Calidad Gestual
                                            │
                                            ▼
  [ GEMELO DIGITAL DEL APRENDIZ (Digital Twin) ]
  Modelo de 4 Dimensiones ───► Dominio $\mu_s$, Precisión $P_s$, Consistencia $C_s$, Velocidad $V_s$
  Curva de Olvido (Ebbinghaus)► Retención $R_s(t) = \exp(- \Delta t / S_s)$
                                            │
                                            ▼
  [ MOTOR DE DECISIÓN Y OPTIMIZACIÓN ]
  MasteryPredictor (Logística)► Probabilidad de éxito $p_i = \sigma(\vec{w} \cdot \vec{x} + b)$
  MILP / Branch-and-Bound ────► $\max \sum (\alpha_1 g_i + \alpha_2 r_i + \alpha_3 m_i - \alpha_4 f_i) x_i$
                                            │
                                            ▼
  [ SALIDAS, ALERTAS Y RETROALIMENTACIÓN ]
  Dashboard Padres / UI Niño ─► Alertas de Fatiga, Confusión Gestual, Adaptación de Dificultad
```

---

### 1.1 Procesamiento de Entradas (Pipeline de Visión Artificial)

1. **Captura y Extracción de Landmarks:**  
   Se captura el flujo de video a 30 FPS. El detector extrae 21 puntos clave tridimensionales $(x, y, z)$ por mano.
2. **Normalización e Invarianza Espacial:**  
   Para evitar que la distancia del niño a la cámara, el tamaño anatómico de sus manos o la inclinación de la postura alteren la clasificación:
   - **Centrado:** Se traslada el origen de coordenadas $(0,0,0)$ a la muñeca (landmark 0).
   - **Escalado:** Se divide por la distancia euclidiana entre la muñeca y el nudillo del dedo medio (MCP 9).
   - **Alineación planar:** Se proyecta y normaliza el vector director del plano de la palma.
3. **Construcción del Vector de Características ($\vec{v} \in \mathbb{R}^{38}$):**  
   Se calculan 15 ángulos de flexión articular interdigital, 10 distancias clave normalizadas entre puntas de dedos (apertura), 8 orientaciones espaciales y 5 factores de profundidad relativa.
4. **Clasificación y Estabilización Temporal:**  
   - Se calcula la distancia euclidiana/similitud angular frente a las plantillas registradas durante la calibración personalizada del usuario.
   - **Estabilizador con histéresis:** Para evitar activaciones erráticas en el tránsito de una seña a otra, se exige la confirmación persistente del gesto durante un umbral mínimo de frames consecutivos ($N=3$), aplicando un estado de *debounce* y desacople (*release*) antes de admitir repeticiones.

---

### 1.2 Lógica Algorítmica y Modelo Matemático

El motor analítico combina tres capas de modelado formal:

#### A. Modelo de Dominio de Habilidad (Gemelo Digital)

Cada nota/seña $s$ tiene un vector de estado dinámico que modela la destreza del usuario:
$$\mu_s = 0{,}40 \cdot P_s + 0{,}25 \cdot C_s + 0{,}20 \cdot V_s + 0{,}15 \cdot R_s$$
Donde:

- **$P_s$ (Precisión):** Tasa de aciertos ponderada por la dificultad del contexto.
- **$C_s$ (Consistencia):** Varianza inversa del rendimiento en los últimos $K$ intentos.
- **$V_s$ (Velocidad):** Normalización de la velocidad de reacción frente al umbral neuromotriz infantil esperado ($400\,\text{ms} \le T \le 2500\,\text{ms}$).
- **$R_s$ (Retención con Memoria Espaciada):** Implementación de la curva de Ebbinghaus / SM-2:
  $$R_s(\Delta t) = \exp\left(-\frac{\Delta t}{S_s}\right)$$
  Donde $\Delta t$ es el tiempo transcurrido sin práctica y $S_s$ es la estabilidad del intervalo mnemotécnico.

#### B. Modelo Predictivo de Rendimiento (`MasteryPredictor`)

- **Fase Fría ($N < 40$ intentos):** Función sigmoide logística paramétrica:
  $$p_i = \frac{1}{1 + \exp\left(-k (\bar{\mu} - \text{dif}_i)\right)}$$
- **Fase Calibrada ($N \ge 40$ intentos):** Regresión logística adaptativa entrenada en el dispositivo mediante Descenso de Gradiente estocástico sobre variables individuales:
  $$z = w_1 \cdot \text{precisión\_nota} + w_2 \cdot \text{dificultad} + w_3 \cdot \Delta t_{\text{última}} + b$$
  $$p_i = \sigma(z) = \frac{1}{1 + e^{-z}}$$

#### C. Optimizador de Rutas de Aprendizaje (MILP / Branch-and-Bound)

Selecciona la combinación óptima de actividades $x_i \in \{0, 1\}$ resolviendo un problema de Programación Lineal Entera Mixta (Mixed-Integer Linear Programming):
$$\max \sum_{i \in A} \big(\alpha_1 g_i + \alpha_2 r_i + \alpha_3 m_i - \alpha_4 f_i\big) x_i$$
Sujeto a:

- **Restricción de tiempo:** $\sum d_i x_i \le T_{\text{presupuesto}}$
- **Restricción de tamaño:** $\sum x_i = K$
- **Prerrequisitos:** $x_i \le a_i$ (bloquea actividades si sus notas base no están consolidadas)
- **Carga cognitiva y fatiga:** $\sum \text{dif}_i x_i \le \delta_{\max} K$
- **Garantía lúdica y repaso:** Inclusión obligatoria de repasos vencidos ($r_i$) y actividades lúdicas motivacionales ($m_i$).

---

### 1.3 Generación de Soluciones, Acciones y Alertas

El motor evalúa periódicamente el contexto y dispara las siguientes acciones estructuradas:

| Tipo de Evento / Disparador | Condición Lógica Algorítmica | Solución / Alerta Generada | Acción en el Software |
| --- | --- | --- | --- |
| **Alerta de Fatiga Infantil** | $F_{\text{estimada}} = 0{,}5\frac{n}{N} + 0{,}5\frac{t}{T} \ge 0{,}85$ | `ALERT_FATIGUE_LIMIT` | Pausa dinámica recomendada, reducción del ritmo y cierre sugerido de sesión. |
| **Frustración / Fallos Consecutivos** | 3 intentos consecutivos con acierto $< 60\%$ | `ACTION_SCAFFOLD_EASE` | Escalera de andamiaje: reduce tempo (BPM), acorta secuencia y activa pistas visuales. |
| **Confusión Gestual Detectada** | $\frac{\text{confusiones}(s_a, s_b)}{\text{intentos}(s_a)} \ge 0{,}30$ | `DIAGNOSTIC_GESTURE_CONFUSION` | Genera ejercicio discriminativo de contraste entre $s_a$ y $s_b$; alerta en Zona de Padres. |
| **Repaso Espaciado Vencido** | $t_{\text{actual}} \ge \text{due\_at}(s)$ | `TRIGGER_SPACED_REVIEW` | Inserta automáticamente la seña en la ruta diaria para prevenir degradación de memoria. |
| **Desbloqueo de Nueva Habilidad** | $\forall p \in \text{prereqs}(s): \mu_p \ge 0{,}80$ | `EVENT_SKILL_UNLOCKED` | Notificación de logro, desbloqueo en el mapa y presentación de nueva nota. |

---

## 2. Estado de Avance: Módulos Operativos y Funcionales

El software cuenta con una arquitectura completamente desacoplada y validada mediante suites de pruebas automatizadas unitarias, de integración y de renderizado visual. A continuación se presentan las evidencias e ilustraciones técnicas de los módulos que se encuentran **100% operativos**.

---

### 2.1 Módulo de Bienvenida y Gestión de Perfiles

Permite la administración de perfiles infantiles con selección de avatares, seguimiento de estrellas, monedas y rachas diarias con aislamiento local de datos.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  MÓDULO DE PERFILES Y BIENVENIDA (OPERATIVO)                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│     👋 ¡HOLA! ¿QUIÉN VA A JUGAR HOY?                                                        │
│                                                                                             │
│     ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐                    │
│     │      🦎 Leo      │    │     🦜 Maya      │    │    ➕ NUEVO      │                    │
│     │    Nivel 3 • ⭐ 24│    │    Nivel 1 • ⭐ 5 │    │      PERFIL      │                    │
│     │ [ CONTINUAR > ]  │    │ [ CONTINUAR > ]  │    │   [ CREAR ]      │                    │
│     └──────────────────┘    └──────────────────┘    └──────────────────┘                    │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Captura de referencia:** `docs/capturas/01_splash.png`, `02_perfiles.png`, `03_crear_perfil.png`
- **Funcionalidad:** Carga de estado desde SQLite, cálculo de rachas diarias y configuración de sesión.

---

### 2.2 Módulo de Calibración Personalizada e Invariante

Sistema interactivo de visión artificial que captura y genera las plantillas biométricas adaptadas a las manos del niño para cada una de las 8 notas musicales (DO3 a DO4).

- **Captura de referencia:** `docs/capturas/06_calibracion.png`
- **Funcionalidad:**
  - Detección en vivo con MediaPipe.
  - Comprobación visual de postura (3 muestras consecutivas estables por seña).
  - Almacenamiento seguro en archivo de descriptores vectoriales.

---

### 2.3 Módulo de Mapa de Aventura y Enrutamiento Inteligente

Renderiza la ruta de aprendizaje generada dinámicamente por el optimizador MILP, marcando actividades fijas y actividades adaptativas generadas en tiempo real.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  MAPA DE AVENTURA Y GENERACIÓN DE RUTAS (OPERATIVO)                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│   (⭐ Nivel 1: DO) ──► (⭐ Nivel 2: RE) ──► [🤖 Reto Generado] ──► (🔒 Nivel 3: MI)        │
│          ▲                                                                                  │
│          └─────────── Ruta recomendada por el Optimizador MILP ────────────┘                │
│                                                                                             │
│   [ Continuar Aventura ]               [ Modo Canciones ]              [ Modo Libre ]       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Captura de referencia:** `docs/capturas/04_inicio.png`, `05_aventura.png`
- **Funcionalidad:** Enrutamiento algorítmico, cálculo de tiempo disponible y progresión de niveles.

---

### 2.4 Módulo de Ejecución de Ejercicios y Feedback en Vivo

Espacio de interacción en tiempo real donde el niño realiza las señas frente a la cámara.

- **Captura de referencia:** `docs/capturas/11_ejercicio.png`, `10_modo_libre.png`
- **Funcionalidad:**
  - Pipeline de clasificación con latencia $< 35\,\text{ms}$.
  - Síntesis de audio polifónico/nota correspondiente mediante motor de sonido local.
  - Indicador visual inmediato de acierto, racha y puntaje acumulado.

---

### 2.5 Módulo de Ritmo y Canciones (Línea de Impacto)

Mecánica de juego rítmico musical en la que las notas se desplazan hacia una línea de impacto temporal.

- **Captura de referencia:** `docs/capturas/13_canciones.png`, `14_ritmo.png`
- **Funcionalidad:**
  - Control de tempo dinámico (Tortuga 🐢, Normal, Liebre 🐇).
  - Tolerancia temporal ajustable según la edad y precisión del niño.
  - Multiplicadores de combo y evaluación de precisión métrica.

---

### 2.6 Módulo de Resultados y Diagnóstico Adaptativo

Al finalizar cada actividad, presenta el desglose pedagógico y las decisiones tomadas por el agente de inteligencia artificial.

- **Captura de referencia:** `docs/capturas/12_resultados.png`
- **Funcionalidad:**
  - Resumen de precisión, ritmo y calidad postural.
  - Registro inmediato en la base de datos de intentos.
  - Re-entrenamiento automático en segundo plano del modelo cuando se cumplen las condiciones de volumen de muestras.

---

### 2.7 Módulo de Analítica para Padres y Educadores (Zona de Padres)

Panel de control con visualización analítica del gemelo digital del aprendiz.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  ZONA DE PADRES / PANEL DE CONTROL ANALÍTICO (OPERATIVO)                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  DOMINIO POR HABILIDAD:                                                                     │
│  DO [████████████████████] 100% (Consolidado)   RE [████████████░░░░░░] 68% (En práctica)   │
│  MI [████████░░░░░░░░░░░░] 42% (Introducido)    FA [░░░░░░░░░░░░░░░░░░]  0% (Bloqueado)     │
│                                                                                             │
│  DIAGNÓSTICO PSICOMOTRIZ:                                                                   │
│  • Tiempo medio de reacción: 740 ms (Excelente agilidad)                                    │
│  • Confusión recurrente detectada: RE ↔ MI (Solución: Se programó ejercicio de contraste)   │
│  • Retención proyectada: 94% (Próximo repaso sugerido: en 2 días)                           │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Captura de referencia:** `docs/capturas/07_progreso.png`, `08_padres.png`, `09_ajustes.png`
- **Funcionalidad:** Desglose del gemelo digital, matrices de confusión intergestual, reporte de tiempos de reacción y recomendaciones personalizadas.

---

## 3. Matriz de Estado de Integración de Componentes

| Componente de Software | Módulo Tecnológico | Estado Operativo | Cobertura de Pruebas |
| --- | --- | --- | --- |
| **Extractor de Landmarks** | `handsingkids.vision.detector` | **100% Operativo** | Validado con video y stream real |
| **Normalizador Invariante** | `handsingkids.vision.features` | **100% Operativo** | Invarianza geométrica demostrada |
| **Filtro de Histéresis** | `handsingkids.vision.stabilizer` | **100% Operativo** | Cero disparos accidentales |
| **Clasificador Angular** | `handsingkids.vision.classifier` | **100% Operativo** | $k\text{-NN} / \text{Cosine}$ funcional |
| **Gemelo Digital** | `handsingkids.intelligence.digital_twin` | **100% Operativo** | Curvas de Ebbinghaus operativas |
| **Estimador Logístico** | `handsingkids.intelligence.predictor` | **100% Operativo** | Gradiente estocástico local activo |
| **Optimizador MILP** | `handsingkids.intelligence.optimizer` | **100% Operativo** | PuLP CBC + Fallback Exacto |
| **Base de Datos Local** | `handsingkids.data.database` | **100% Operativo** | SQLite WAL sin dependencias cloud |
| **Interfaz Gráfica (UI)** | `handsingkids.ui.screens` | **100% Operativo** | 14 pantallas integradas y activas |
