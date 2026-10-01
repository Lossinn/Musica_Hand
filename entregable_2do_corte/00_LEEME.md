# Entregable del segundo corte — Hand Sing Kids v2.0

Gestión Tecnológica (8830 0064 0) · UPB Seccional Montería · 2026-2 · Actualizado el 1 de octubre de 2026.

## Estructura

```
entregable_2do_corte/
├── 00_LEEME.md                                   este archivo
├── 01_FALTANTE_POR_CORROBORAR_O_AJUSTAR.md       pendientes del equipo (interno, no va en el .zip)
├── entrega_teams/                                lo que se sube a Teams
│   ├── 01_Documento_EBT_GestionTecnologica_Equipo_XX.pdf
│   ├── 03_Poster_Cientifico_90x120_Equipo_XX.pdf
│   ├── 04_Modelo_Financiero_ROI_Equipo_XX.xlsx
│   └── GT_Corte2_Equipo_XX_HandSingKids.zip
├── recursos/
│   ├── assets/          logos (UPB, HIS, SILOGE), fondos, capturas, fuentes, QR
│   ├── diagramas/       BPMN As-Is/To-Be, DFD 0-1-2, árbol de problemas, flujo de caja
│   ├── identidad_visual/ 3 conceptos de logotipo (SVG + PNG 300 DPI), paleta y guía
│   └── _previews/       vistas previas (no van en el .zip)
└── _fuentes/            scripts que regeneran todo y datos de verificación
```

El archivo `02_Modelado_BPMN_DFD_Gobernanza` va insertado en el documento (secciones 6 a 8), como permite la instrucción.

## Contenido de la entrega

| Archivo | Qué es |
| --- | --- |
| `01_Documento_…pdf` | Documento EBT en APA 7 (31 páginas): diagnóstico, literatura, método, prototipo, BPMN 2.0, DFD 0-1-2, gobernanza DAMA-DMBOK, finanzas, discusión y referencias |
| `03_Poster_…pdf` | Póster vertical 900 × 1200 mm (vectorial, QR funcional) con logos UPB, HIS y SILOGE en la identidad del evento HIS |
| `04_Modelo_Financiero_…xlsx` | Supuestos rotulados por procedencia, CAPEX, OPEX, beneficios, seis escenarios y flujo acumulado, con fórmulas |

## Qué cambió al analizar el estudio del Equipo 13 (PINT2)

- **Se aprovechó** (rotulado como fuente secundaria no verificada): caracterización de campo en aulas de Montería y Cereté y su aritmética financiera (reproducida y correcta).
- **Se añadió** (por la rúbrica): caracterización de campo, gamificación, TRL (se declara **TRL 4**), trazabilidad de objetivos, leyenda BPMN, cuantificación As-Is/To-Be, protocolo de piloto, migración CHECK probada (Anexo D) y contraste con el estudio (Anexo E).
- **No se heredó** (no coincide con el código o no existe): Streamlit/Gemini/SimPy/SciPy, 30 fps, vector de 38 componentes, solver en 38 ms, p < 0,0001 y d = 4,929, y 5 referencias con DOI inexistente o incorrecto.
- **Finanzas**: un aula tiene CAPEX $ 7.370.000, ROI 18,9 % y recuperación en 63,4 meses (**no cumple** la guía). Institución con 4 aulas: 71,4 % y 16,8 meses.

## Pendientes

Ver [01_FALTANTE_POR_CORROBORAR_O_AJUSTAR.md](01_FALTANTE_POR_CORROBORAR_O_AJUSTAR.md).

## Verificación (resumen)

- 8 de 8 suites del proyecto pasan; MILP y enumeración coinciden con CBC (PuLP 2.9.0); 16 restricciones CHECK probadas sin romper la integración.
- Descriptor y clasificador: 2,3 ms por fotograma; solver: 0,13 a 1,8 s por sesión; latencia de extremo a extremo no medida.
- DANE: Córdoba 47,2 % de hogares con internet frente a 65,6 % nacional (valores de Córdoba leídos de gráficos).
- 15 referencias con DOI verificados en Crossref y doi.org.
