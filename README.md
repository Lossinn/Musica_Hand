# Hand Sing Music

Plataforma inteligente de **aprendizaje musical adaptativo** para niños de 3 a 12 años.
Usa **visión computacional** para reconocer la interacción gestual del estudiante, registra y
analiza su desempeño con modelos de IA, emplea **optimización matemática (MILP)** para
seleccionar actividades y usa **aprendizaje por refuerzo** y un **gemelo digital** para mejorar
progresivamente la adaptación del proceso de aprendizaje.

> Proyecto de Ingeniería Industrial: no es solo una app, es el diseño y evaluación de un *sistema*.

---

## Principio rector

**Primero hacemos funcionar perfectamente cada componente; después los conectamos.**
No romper lo que ya funciona. Mejorar por módulos, probar cada cambio, integrar, validar.

El trabajo actual se concentra en la **calibración automática**, manteniendo las notas, formas,
ubicaciones y dinámica de interacción que ya funcionan.

---

## Pipeline conceptual

```
Niño → Cámara → Visión computacional → Reconocimiento de gesto → Nota musical
     → Evaluación → Perfil del niño → Adaptación → Nueva actividad
```

| Componente            | Pregunta que responde                                         |
|-----------------------|--------------------------------------------------------------|
| Visión computacional  | ¿Qué hizo el niño?                                            |
| Datos / Perfil        | ¿Cómo le fue?                                                 |
| Machine Learning      | ¿Cómo probablemente responderá?                               |
| MILP (PuLP)           | ¿Qué combinación de actividades conviene?                     |
| DQN (RL)              | ¿Qué decisión adaptativa produce mejores resultados?          |
| Gemelo digital        | ¿Qué pasaría si aplicamos esa estrategia?                     |

---

## Estructura del repositorio

```
musica_hand/
├── 01_Agente_de_IA/            Notas / configuración del agente de IA de apoyo
├── 02_Base_de_investigacion/   Documentos, matriz bibliográfica, teorías, modelos
├── 03_Codigo/                  Código fuente
│   ├── Prototipo/              Aplicación principal (Python) — ver 03_Codigo/README.md
│   ├── Reconocimiento_manos/   Experimentos aislados de visión/MediaPipe
│   └── Musica/                 Experimentos de audio / teoría musical
├── 04_Datos/                   Datasets, exportes de sesiones, resultados
├── 05_Documento_base/          Necesidad, Problema, Objetivos, Justificación
├── 06_Documentos_por_capitulo/ Capítulos 1–4 del documento
├── 07_Ecuaciones_booleanas/    Ecuaciones de búsqueda (BDC, Scopus, Pruebas)
├── 08_Investigacion/           Búsquedas, antecedentes, estado del arte, APA
├── 09_Imagenes/                Figuras y diagramas
├── 10_Errores/                 Registro de errores y su resolución
└── 11_Versiones_antiguas/      Snapshots de versiones previas
```

---

## Fases del proyecto

| Fase | Descripción                              | Estado        |
|-----:|-----------------------------------------|---------------|
| 1    | Aplicación musical básica               | Base          |
| 2    | Reconocimiento de gestos                | Base          |
| 3    | Calibración                             | Base          |
| 4    | **Calibración automática**              | **En curso**  |
| 5    | Registro de resultados                  | Pendiente     |
| 6    | Perfil individual del niño              | Pendiente     |
| 7    | Modelo matemático MILP                  | Pendiente     |
| 8    | Modelo predictivo TensorFlow/Keras      | Pendiente     |
| 9    | Gemelo digital                          | Pendiente     |
| 10   | Entorno Gymnasium                       | Pendiente     |
| 11   | DQN con Stable-Baselines3               | Pendiente     |
| 12   | Integración completa                    | Pendiente     |
| 13   | Dashboard en Streamlit                  | Pendiente     |
| 14   | Validación experimental                 | Pendiente     |

---

## Puesta en marcha (código)

```powershell
# desde musica_hand/
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python 03_Codigo/Prototipo/main.py
```

`requirements.txt` contiene solo el stack mínimo (Fases 1–4).
`requirements-full.txt` lista el stack completo por fases, para añadir cuando corresponda.
