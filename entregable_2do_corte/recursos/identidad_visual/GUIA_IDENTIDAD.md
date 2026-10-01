# Identidad visual de Hand Sing Kids

Tres conceptos de logotipo, todos vectoriales (SVG, con el texto convertido a trazados con Montserrat ExtraBold, sin depender de fuentes instaladas) y exportados a PNG a 300 DPI (`png_300dpi/`).

| Concepto | Idea | Fortalezas | Límites |
|---|---|---|---|
| **A. Mano-nota** | Mano abierta amarilla sobre placa negra, con una corchea en la palma | Comunica señas y música a la vez; formas simples; legible desde 16 px; usa los colores HIS | Mano «alto» puede leerse como «detener» si se muestra sin la corchea |
| **B. Puntos de mano** | Esqueleto de 21 puntos (topología de MediaPipe Hands) dentro de un visor | Refleja la tecnología real del producto | Trazos finos: pierde legibilidad bajo 32 px y la placa negra desaparece sobre fondo oscuro |
| **C. Nota-dedo** | Corchea cuya plica es un índice y cuya cabeza es un puño; arcos de movimiento | Amigable para niños; alto contraste; legible a 16 px | La referencia a «manos» es más sutil |

**Recomendación: concepto A** como logotipo principal (mejor equilibrio entre claridad, escala y coherencia con la paleta industrial de HIS). El concepto C queda como alternativa infantil (por ejemplo, ícono de la aplicación) y el B como ilustración técnica. El documento y el póster usan el A.

## Paleta
Amarillo `#FFCC00`, negro `#141414`, gris claro `#F5F5F5`, gris oscuro `#404040` y verde azulado `#1FA99B` (acento de la interfaz de la aplicación). Razones de contraste WCAG 2.1: negro sobre amarillo 12,18:1; blanco sobre negro 18,42:1; gris oscuro sobre blanco 10,37:1. **El verde azulado sobre blanco solo alcanza 2,91:1**: usarlo únicamente en elementos gráficos, nunca en texto. Ver `paleta_y_contraste.png`.

## Tipografía
Montserrat (títulos en mayúsculas, peso 800) y Helvetica/Arial para diagramas y texto corrido. Fuente incluida en `../assets/fonts/` (licencia SIL Open Font License).

## Uso
- Zona de respeto: al menos la mitad de la altura de la mano alrededor del ícono.
- Tamaño mínimo: 16 px el ícono; 120 px de ancho el logotipo horizontal.
- Sobre fondo oscuro, usar `concepto_*_horizontal_oscuro.svg` (y el ícono A o C, que conservan contraste).
- No estirar, girar ni cambiar los colores del ícono.

## Archivos
`concepto_{A,B,C}_icono.svg`, `concepto_{A,B,C}_horizontal.svg`, `concepto_{A,B,C}_horizontal_oscuro.svg`, `png_300dpi/*.png` (íconos de 2400 px = 8 in; horizontales de 3280 px), `comparativa_conceptos.png`, `escalas_legibilidad.png`, `paleta_y_contraste.png`.

Nota: los logotipos de UPB, HIS y SILOGE son de sus instituciones y se usan tal como se entregaron; el escudo de la UPB **no se entregó** y el póster tiene un marco rotulado para insertarlo.
