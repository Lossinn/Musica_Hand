# Diagrama SIPOC y Arquitectura del Sistema Clorificador

**Proyecto**: Diseños y Prototipado de un Clorificador de Agua de Bajo Costo para Zonas Rurales de Montería.  
**Ubicación**: `01_Documentacion_Tecnica/Diagramas_SIPOC_y_Arquitectura_Sistema.md`

---

## 1. Diagrama SIPOC (Suppliers, Inputs, Process, Outputs, Customers)

```text
+----------------------+--------------------+---------------------+--------------------+--------------------+
| SUPPLIERS            | INPUTS             | PROCESS             | OUTPUTS            | CUSTOMERS          |
| (Proveedores)        | (Entradas)         | (Proceso)           | (Salidas)          | (Clientes)         |
+----------------------+--------------------+---------------------+--------------------+--------------------+
| 1. Fuente Hídrica    | - Agua sin tratar  | 1. Bifurcación del  | - Agua tratada con | 1. Población rural |
|    (Pozo/Río El      |   (Caudal Q, pH,   |    flujo en Tee 1"  |   cloro residual   |    de El Vidrial   |
|    Vidrial).         |   turbidez).       |    (Bypass / Cámara)|   entre 0.2 y 0.5  |    (Hogares).      |
|                      |                    |                     |   mg/L.            |                    |
| 2. Proveedor Químico | - Pastillas de     | 2. Contacto pasivo  |                    | 2. Junta de Acción |
|    (Tricloro / Hipo).|   cloro (TCCA/Hipo)|    y disolución de  | - Reducción del    |    Comunal /       |
|                      |                    |    cloro en 2".     |   100% en Colif.   |    Acueducto rural.|
| 3. Proveedor de      | - Presión por      |                     |   Totales / E.coli.|                    |
|    Materiales PVC    |   gravedad (cabeza | 3. Control de       |                    | 3. Comité de       |
|    (Pavco/Ferretería)|   hidráulica H).   |    apertura de      | - Agua sin sabor a |    Salud Pública.  |
|                      |                    |    3 válvulas 1".   |   sobrecloración.  |                    |
| 4. Laboratorio UPB   | - Kit DPD y        |                     |                    |                    |
|    (Equipos de       |   fotómetro de     | 4. Mezcla final y   |                    |                    |
|    medición).        |   cloro libre.     |    desinfección.    |                    |                    |
+----------------------+--------------------+---------------------+--------------------+--------------------+
```

---

## 2. Mapa de Variables del Sistema

```text
                                VARIABLES DEL SISTEMA
                                          |
        +---------------------------------+---------------------------------+
        |                                                                   |
  VARIABLES CONTROLABLES (Entradas)                               VARIABLES DEPENDIENTES (Respuestas)
  - Apertura Válvula Bypass (% V_bp)                               - Cloro residual libre (C_res, mg/L)
  - Apertura Válvula Entrada Cámara (% V_in)                        - Caudal de salida tratada (Q_total, L/s)
  - Apertura Válvula Salida Cámara (% V_out)                        - Inactivación microbiológica (%)
  - Número de pastillas en cámara (M_cloro)                         - Pérdida de carga hidráulica (h_L, m)
  - Tiempo de contacto previo a consumo (t_contacto)
        |
        +---------------------------------+
                                          |
                          VARIABLES NO CONTROLABLES (Perturbaciones)
                          - Presión del tanque elevado por gravedad (H_cabeza)
                          - Temperatura ambiental y del agua (T, °C)
                          - Turbidez inicial del agua cruda (Turb, NTU)
                          - Demanda química e inorgánica de cloro (D_demanda)
                          - pH inicial del agua cruda
```
