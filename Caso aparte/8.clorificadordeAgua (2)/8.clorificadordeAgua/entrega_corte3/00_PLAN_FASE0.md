# Plan Fase 0 — Clorificador de agua (Corte 3, Gestión Tecnológica)

Fecha: 6 de noviembre de 2026. Estado: **esperando decisiones del equipo antes de redactar**.
Se asume que las reglas del corte son las mismas del proyecto Hand Sing Kids (rúbrica, ZIP de cinco archivos, Turnitin ≤ 20 %, docente como co-autor).

## 1. Qué existe (leído completo)
| Insumo | Estado |
|---|---|
| Diseño del prototipo PVC (BOM $159.991 COP, bypass + cámara 2", 3 válvulas) y modelo de mezcla | Completo, en `01_Documentacion_Tecnica/` |
| Protocolos (aforo, DPD), DOE factorial 2³ × 3 réplicas (24 corridas), plan de 2 semanas | Redactados. **No hay evidencia de que se hayan ejecutado** |
| Bitácora (26-ene a 8-may-2026) | Registra compra (13-abr), ensamblaje (15-abr) y ajustes (24-abr). **No registra mediciones** |
| Documento final de Proyecto Integrador I | Dice textualmente que el proyecto «se encuentra en fase de construcción y preparación experimental» y que el capítulo 6 son «resultados esperados teóricos» |
| Simulación Monte Carlo (1.000 escenarios, notebook y CSV) | Existe; usa distribuciones **supuestas** (no medidas) |
| `Formato_Captura_Datos_Ensayos.csv` | 10 filas fechadas 21-29 sep 2026. **Procedencia sin confirmar** (la guía muestra un «ejemplo» con cifras distintas) |
| Entrega del 2.º corte (68 KB) | Presente |
| Preprint manuscrito, cifras PRISMA, escaneos | **No están** |

## 2. Hallazgos que cambian el enfoque (no los resuelvo por mi cuenta)
1. **No hay resultados experimentales verificables.** El artículo solo podría ser de diseño + modelo analítico + simulación, declarado como tal. Si las 10 filas del CSV son mediciones reales, se pueden usar como datos preliminares; si son ilustrativas, no.
2. **La simulación Monte Carlo, tal como está programada, no respalda el diseño.** En el CSV: 990 de 1.000 escenarios «Subclorada» y solo 10 «Adecuada»; cloro residual medio 0,011 mg/L; 838 escenarios en 0,00. La causa está en los parámetros supuestos (demanda de cloro media 0,65 mg/L frente a una dosis efectiva media de C₀·f ≈ 0,3 mg/L). Hay que decidir si se reporta tal cual (es un hallazgo honesto: con esos supuestos el diseño no cumple) o se recalibra con datos medidos.
3. **El documento del 2.º corte contiene afirmaciones sin respaldo en este repositorio:** plataforma «HydroVidrial Analytics» (Streamlit/PostgreSQL/Supabase) sin código aquí; TRL 5 del software con «sesiones de usabilidad con la JAC»; ROI 361,2 % y payback 3,3 meses (de supuestos); 85 % de familias con pozos, 680 habitantes y 140 familias; ocho de 15 referencias marcadas «verificar DOI por el equipo» (p. ej. «Nejm Editorial Team»). No las usaré sin verificación.
3b. Hay referencias con DOI/volumen inconsistentes entre el documento del 2.º corte y el documento final (p. ej. Bain et al. 2023, Clasen 2023).
4. **El rango normativo se contradice entre documentos:** 0,2–0,5 mg/L (prototipo y DOE) frente a 0,3–2,0 mg/L (documento del 2.º corte). La Resolución 2115 fija 0,3–2,0 mg/L en la red; 0,2–0,5 es un rango objetivo propio. Hay que escoger y citar la fuente.
5. **Autoría inconsistente.** Proyecto Integrador I y CI: seis estudiantes (Correa, González, Guzmán, Pérez, Soto, Vidal). Entrega del 2.º corte de Gestión Tecnológica: tres (Roxana Muñoz, Andrea Guzmán Gómez, Camilo Esteban Alvarez). Solo Andrea Guzmán aparece en ambas.
6. Código de asignatura: 8830 0064 0 en la entrega del 2.º corte; 8830 0048 0 en los documentos del Corte 3.
7. Discrepancias menores: tarro de soldadura 1/16 gal (presupuesto) vs 1/4 gal (2.º corte); recarga de «1 o 2 pastillas de 1" o 2"» en una cámara de 2" de 0,5 m sin masa definida (la matriz habla de 20–40 g).

## 3. Qué haré, en cuanto confirmen
Mismo proceso del otro proyecto, dentro de esta carpeta (`entrega_corte3/`): pruebas y análisis reproducibles (re-ejecutar la simulación, análisis de sensibilidad, intervalos de confianza, ANOVA solo si hay datos reales), selección y verificación de revista, referencias verificadas en Crossref, artículo en la plantilla oficial, prefiltro de similitud, paquete de envío y ZIP con marcadores PENDIENTE (preprint, Turnitin, constancia de envío).

## 4. Decisiones que necesito
1. ¿Quiénes son los autores y en qué orden? (¿los tres del 2.º corte o los seis del Proyecto Integrador?) ¿Cuántas versiones/personas entregan?
2. ¿Las 10 filas del CSV son mediciones reales de laboratorio? ¿Existe otra evidencia (fotos, bitácora de laboratorio, hojas de Excel) de los ensayos?
3. ¿Aceptan que el artículo sea de diseño, modelo y simulación, con el hallazgo de que la simulación actual da subcloración, y que el prototipo no esté validado experimentalmente?
4. ¿Mantienen la fecha límite del 6 de noviembre? ¿Misma revista (Revista UIS Ingenierías)?
