# Hand Sing Kids: documento técnico

**Versión 2.0 — septiembre de 2026**

---

## 1. Planteamiento

La primera versión del proyecto resolvía el problema de forma directa: la cámara
entregaba los puntos de la mano, esos puntos se comparaban con una plantilla
guardada y, si el parecido superaba un umbral, se daba la nota por reconocida.
Funciona como demostración, pero tiene dos límites que impiden construir encima.

El primero es de reconocimiento. Comparar coordenadas crudas arrastra toda la
variabilidad de la escena: la distancia del niño a la cámara, la inclinación de
la muñeca, el tamaño de su mano. El segundo es de arquitectura. Con la cámara, la
lógica musical, el puntaje y el dibujo en un mismo archivo de 1.740 líneas, cada
cambio obliga a tocar todo.

Este documento describe cómo se resolvieron ambos y deja escritas las
formulaciones que sostienen la parte adaptativa.

---

## 2. Arquitectura

El sistema se organiza en cinco capas que solo se comunican hacia abajo, y un bus
de eventos que permite que las de arriba se enteren de lo que pasa sin depender
de las de abajo.

```
                    ┌───────────────────────────┐
                    │        INTERFAZ           │   pantallas y componentes
                    ├───────────────────────────┤
                    │       APLICACIÓN          │   contexto, navegación, sesión
                    ├───────────────────────────┤
                    │         DOMINIO           │   entidades, notas, evaluación
                    ├───────────────────────────┤
                    │      INTELIGENCIA         │   dominio, adaptación, MILP
                    ├───────────────────────────┤
                    │     INFRAESTRUCTURA       │   cámara, audio, SQLite
                    └───────────────────────────┘
```

El ciclo completo de una nota:

```
  cámara → detector → descriptor → clasificador → estabilizador
                                                        │
                                              gesto confirmado
                                                        │
                                            motor musical (suena)
                                                        │
                                       evaluador (¿era la esperada?)
                                                        │
                            ┌───────────────────────────┴─────────────┐
                            ▼                                         ▼
                   retroalimentación                            registro
                            │                                         │
                            └───────────────────┬─────────────────────┘
                                                ▼
                                    motor de dominio (gemelo digital)
                                                ▼
                            motor adaptativo  →  optimizador  →  siguiente
```

Ninguna pantalla importa MediaPipe. Ninguna pieza de visión sabe qué es una
nota musical. El evaluador no sabe dibujar. Esa separación es lo que permite que
las pruebas de la sección 9 se ejecuten sin cámara y sin ventana.

---

## 3. Reconocimiento de señas

### 3.1 El problema del método anterior

La versión 1 concatenaba las coordenadas de las dos manos en un vector de 126
componentes y usaba similitud coseno contra una plantilla por nota, aceptando el
mejor candidato si superaba 0,65.

Al aplicar ese procedimiento sobre el archivo de calibración real del proyecto
(`pentagrama_calibrado.json`, ocho señas), la matriz de similitudes entre notas
distintas da lo siguiente:

|        | DO3 | RE3 | MI3 | FA3 | SOL3 | LA3 | SI3 | DO4 |
|--------|-----|-----|-----|-----|------|-----|-----|-----|
| **DO3**  | 1,000 | 0,021 | 0,407 | 0,502 | 0,304 | 0,704 | 0,077 | −0,018 |
| **RE3**  | 0,021 | 1,000 | 0,848 | 0,637 | 0,797 | 0,338 | 0,856 | 0,865 |
| **MI3**  | 0,407 | 0,848 | 1,000 | 0,866 | 0,888 | 0,732 | 0,718 | 0,690 |
| **FA3**  | 0,502 | 0,637 | 0,866 | 1,000 | 0,669 | 0,671 | 0,466 | 0,447 |
| **SOL3** | 0,304 | 0,797 | 0,888 | 0,669 | 1,000 | 0,723 | 0,669 | 0,605 |
| **LA3**  | 0,704 | 0,338 | 0,732 | 0,671 | 0,723 | 1,000 | 0,269 | 0,197 |
| **SI3**  | 0,077 | 0,856 | 0,718 | 0,466 | 0,669 | 0,269 | 1,000 | 0,902 |
| **DO4**  | −0,018 | 0,865 | 0,690 | 0,447 | 0,605 | 0,197 | 0,902 | 1,000 |

De los 56 pares de notas distintas, **30 superan el umbral de aceptación de
0,65**. Si y DO agudo llegan a 0,902. Esto no significa que el clasificador elija
mal entre ocho opciones —el máximo suele caer en la correcta—, sino algo más
grave: cualquier postura intermedia, o las manos en reposo, también superan el
umbral y disparan una nota. El umbral no filtra nada.

La medición de la sección 3.5 lo confirma: el método de la versión 1 emite una
nota en el **100 %** de las posturas que no son ninguna seña.

### 3.2 Descriptor invariante

En lugar de comparar coordenadas, cada mano se describe con magnitudes
geométricas que no cambian cuando el niño se acerca, se aleja o gira la muñeca.

Sean $p_0, \dots, p_{20} \in \mathbb{R}^3$ los puntos de una mano, con $p_0$ la
muñeca. Se define la escala de referencia como la distancia de la muñeca al
nudillo del dedo medio:

$$
\sigma = \lVert p_9 - p_0 \rVert
$$

**Curvatura de cada dedo.** Para el dedo con cadena de articulaciones
$(a, b, c, d)$:

$$
\kappa = \operatorname{clip}\!\left(
\frac{\dfrac{\lVert p_d - p_a \rVert}{\lVert p_b - p_a\rVert + \lVert p_c - p_b\rVert + \lVert p_d - p_c\rVert} - 0{,}35}{0{,}65},\; 0,\; 1 \right)
$$

Un dedo extendido da $\kappa \approx 1$; uno cerrado, $\kappa \approx 0$. Es
invariante a escala, traslación y rotación por construcción, porque solo usa
razones entre longitudes.

**Apertura entre dedos contiguos.** Con $u_i$ el vector unitario del dedo $i$
desde su nudillo hasta su yema:

$$
\alpha_i = \frac{1}{\pi}\arccos\big(\langle u_i, u_{i+1}\rangle\big),
\qquad i = 1,\dots,4
$$

**Distancia del pulgar a cada yema**, normalizada por la escala de la mano.
Distingue las configuraciones cerradas en forma de anillo:

$$
\tau_j = \frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j} - p_4\rVert}{\sigma},\;0,\;3\right)
$$

**Normal del plano de la palma.** Separa palma arriba, palma abajo y palma de
canto, que en las señas de altura es información esencial:

$$
n = \frac{(p_5 - p_0) \times (p_{17} - p_0)}{\lVert (p_5 - p_0) \times (p_{17} - p_0) \rVert}
$$

**Dirección de la mano** en el plano de la imagen:

$$
d = \frac{(p_9 - p_0)_{xy}}{\lVert (p_9 - p_0)_{xy} \rVert}
$$

**Forma normalizada.** Los veinte puntos restantes, trasladados a la muñeca,
divididos por $\sigma$ y girados un ángulo $\alpha = -\tfrac{\pi}{2} - \arctan2(d_y, d_x)$
para que la mano quede apuntando hacia arriba. Aporta 40 números.

Cada mano queda descrita por 58 valores. Con las dos manos se añaden cuatro
magnitudes relativas —desplazamiento de una muñeca respecto de la otra en
unidades de $\sigma$, distancia entre ellas y alineación de sus direcciones— y el
descriptor completo tiene **120 componentes**.

> **Nota de compatibilidad.** Las calibraciones de la versión 1 guardan cada mano
> ya centrada en su propia muñeca, de modo que la geometría *entre* manos se
> perdió. El sistema lo detecta (ambas muñecas en el origen) y desactiva ese
> bloque al comparar, en lugar de producir distancias falsas. Por eso una
> calibración antigua se puede importar y sigue funcionando.

### 3.3 Distancia por bloques

Comparar los 120 números con una distancia euclídea corriente dejaría que los 40
de la forma dominaran sobre los 5 de la curvatura. Cada bloque $g$ se compara por
separado, se promedia dentro del bloque y se pondera:

$$
d(a,b) = \sqrt{ \frac{1}{\sum_g w_g} \sum_g w_g \cdot \frac{1}{|g|} \sum_{i \in g} (a_i - b_i)^2 }
$$

con pesos $w$: curvatura 3,0; forma 2,6; distancias del pulgar 2,0; dirección
2,0; geometría entre manos 1,6; normal de la palma 1,4; apertura 1,2.

### 3.4 Clasificación y confianza

Cada nota guarda hasta tres muestras. La distancia de una postura a una nota es
la menor de sus muestras:

$$
d_c = \min_{s \in S_c} d(x, s)
$$

La confianza se obtiene repartiendo probabilidad entre las notas:

$$
P(c \mid x) = \frac{\exp\!\big(-(d_c - d_{\min})/T\big)}{\sum_k \exp\!\big(-(d_k - d_{\min})/T\big)}
$$

La temperatura $T$ no es fija: se ajusta a la separación real entre las señas del
niño concreto. Si sus señas quedaron parecidas, una temperatura alta repartiría
la probabilidad entre varias y el sistema nunca decidiría:

$$
T = \operatorname{clip}\!\left(\tfrac{1}{2}\min_{a \neq b} d(a,b),\; 0{,}05,\; 0{,}20\right)
$$

Una seña se acepta solo si cumple las tres condiciones:

$$
d_{\text{best}} \le 0{,}95
\qquad
P_{\text{best}} \ge 0{,}55
\qquad
P_{\text{best}} - P_{\text{second}} \ge 0{,}08
$$

La tercera es la que faltaba en la versión 1: cuando dos señas empatan, el
sistema **no decide**. Es preferible pedir al niño que repita el gesto que hacer
sonar una nota que no quiso tocar.

### 3.5 Estabilización temporal

A 24 fotogramas por segundo, un clasificador sin filtro produciría una nota cada
40 milisegundos y mover la mano de Do a Sol dispararía toda la escala intermedia.

Se mantiene una ventana deslizante de $N$ lecturas (de fábrica, $N = 1$: la
nota se confirma en el mismo fotograma en que se reconoce, sin ninguna
espera — ver la sección 11.5.1 sobre por qué se bajó de $N=8$ a $N=1$ y qué
se dejó de exigir al hacerlo). Una nota se confirma cuando:

1. aparece en al menos $\max(1, \operatorname{round}(0{,}62\,N))$ posiciones de la ventana,
2. la confianza media de esas lecturas alcanza el umbral,
3. han pasado al menos 0,45 s desde la confirmación anterior,
4. y, si es la misma nota que la última, el niño la **soltó** antes: al menos dos
   fotogramas consecutivos con una lectura distinta.

La cuarta condición es la que permite tocar «Do Do Do» sin que mantener la mano
quieta produzca una ráfaga; no depende de $N$, así que sigue vigente incluso con
la confirmación instantánea de fábrica. Con $N > 1$ (ajustable en Ajustes,
"Tiempo de sostener la seña"), la primera condición vuelve a exigir varias
lecturas seguidas, y ahí sí tiene sentido mostrar en pantalla cuánto falta —
que es lo que hacía el anillo que se llenaba durante el ejercicio antes de
quitarse (sección 11.5.1).

### 3.6 Resultados

Sobre la calibración real del proyecto, con perturbaciones que imitan la
variación cotidiana (escala entre 0,8 y 1,25; giro independiente por mano de
±18°; ruido gaussiano proporcional al tamaño de la mano):

**A. Señas válidas — porcentaje de aciertos**

| Ruido σ | Método nuevo | Método v1 |
|---------|--------------|-----------|
| 0,00 | 100,0 % | 100,0 % |
| 0,03 | 100,0 % | 100,0 % |
| 0,06 | 96,9 % | 100,0 % |
| 0,09 | 86,0 % | 100,0 % |

**B. Posturas que no son ninguna seña — notas disparadas por error**
*(transiciones a mitad de camino entre dos señas, y combinaciones de mano
izquierda de una seña con mano derecha de otra; n = 640)*

| Método nuevo | Método v1 |
|--------------|-----------|
| **8,0 %** | **100,0 %** |

La lectura correcta de estas dos tablas es conjunta. El método de la versión 1
tiene sensibilidad perfecta y especificidad nula: acierta siempre porque siempre
responde algo. El método nuevo sacrifica algo de sensibilidad con ruido alto
—casos en los que se abstiene— a cambio de rechazar doce de cada trece posturas
que no son una seña. Para esta aplicación el intercambio es el correcto: una nota
que suena sin que el niño la haya pedido rompe el juego, mientras que una nota
que tarda un fotograma más en confirmarse no se nota, porque el voto de la
ventana la recupera.

Reproducible con `python tests/test_vision.py`.

---

## 4. Modelo de dominio

Una habilidad no se considera dominada por acertar una vez. El dominio se define
como el desempeño demostrado, moderado por cuánto se recuerda:

$$
\mathcal{M}_s = \Big(\lambda + (1-\lambda)\,R_s^{\gamma}\Big)\Big(w_p P_s + w_c C_s + w_v V_s\Big)
$$

con $w_p = 0{,}55$, $w_c = 0{,}25$, $w_v = 0{,}20$, $\lambda = 0{,}65$ y
$\gamma = 0{,}40$.

**Por qué la retención multiplica y no suma.** En una primera formulación la
retención entraba como un cuarto sumando con peso 0,20. El problema apareció al
probarlo: un mes sin practicar bajaba el dominio como mucho 0,20 y una habilidad
olvidada seguía figurando como dominada. Multiplicando, el desuso prolongado sí
la degrada; el término $\lambda$ impide que el dominio se desplome a cero por
faltar unos días y borre todo lo aprendido.

**Precisión**, con suavizado bayesiano:

$$
P_s = \frac{h_s + \alpha}{n_s + \alpha + \beta}, \qquad \alpha = 1,\ \beta = 3
$$

Sin práctica alguna vale 0,25: el sistema parte de la duda. Cuatro aciertos de
cuatro dan 0,625, no 1.

**Consistencia** sobre los últimos $k \le K = 8$ intentos $y_1,\dots,y_k \in \{0,1\}$:

$$
C_s = \bar{y}_k \left(1 - \frac{\text{cambios}}{k-1}\right) \min\!\left(1, \frac{k}{K}\right)
$$

donde «cambios» cuenta las transiciones entre acierto y fallo. Alternar es la
firma de quien todavía no sabe, y el último factor evita que cuatro aciertos
seguidos pesen igual que ocho.

**Velocidad**, respecto a un tiempo de referencia propio de la franja de edad
($t_{\text{ref}}$ = 5.200 ms de 3 a 5 años, 4.000 ms de 6 a 8, 3.200 ms de 9 a 12;
$t_{\min}$ = 700 ms):

$$
V_s = \operatorname{clip}\!\left(\frac{t_{\text{ref}} - \bar{t}_s}{t_{\text{ref}} - t_{\min}},\; 0,\; 1\right)
$$

**Retención**, con olvido exponencial desde la última práctica, en días:

$$
R_s = \exp\!\left(-\frac{\Delta t}{\tau_s}\right),
\qquad
\tau_s = \tau_0\,\varepsilon_s\,(0{,}6 + \mathcal{M}_s^{-}),
\qquad \tau_0 = 1{,}8
$$

$\mathcal{M}_s^{-}$ es el dominio calculado en la actualización anterior. Usar el
previo y no el actual es lo que evita una definición circular.

### 4.1 Estados de una habilidad

```
  🔒 bloqueada → 👀 introducida → 🟡 en práctica → 🟢 dominada → ⭐ consolidada
                                        ↑                │
                                        └────────────────┘
                                      si el dominio cae por debajo de 0,70
```

El paso a *dominada* exige $\mathcal{M}_s \ge 0{,}80$ **y** al menos seis
intentos; a *consolidada*, $\mathcal{M}_s \ge 0{,}92$ y doce intentos. Una sesión
perfecta de cuatro intentos da un dominio cercano a 0,68: bien, pero todavía no.

---

## 5. Repaso espaciado

Adaptación del esquema SM-2 a una escala de calidad continua $q \in [0,1]$,
tomada de la precisión de la actividad:

$$
\varepsilon \leftarrow \operatorname{clip}\big(\varepsilon + 0{,}1 - (1-q)\,(0{,}8 + (1-q)),\; 1{,}3,\; 2{,}8\big)
$$

$$
I \leftarrow
\begin{cases}
1 & \text{si } q < 0{,}6 \\[4pt]
\max(1,\ I \cdot \varepsilon) & \text{en caso contrario}
\end{cases}
$$

$$
\text{siguiente repaso} = t_{\text{ahora}} + I \cdot 86400
$$

El primer repaso cae al día siguiente; a partir de ahí el intervalo crece en
proporción a lo bien que va la habilidad, y un mal repaso lo devuelve a un día.

---

## 6. Motor adaptativo por reglas

El motor recibe un retrato del momento —dominio por habilidad, precisión de la
última actividad, fallos consecutivos, fatiga estimada y repasos vencidos— y
devuelve una decisión, no una pantalla.

La fatiga se estima combinando cuánto lleva jugado y cuánto tiempo:

$$
F = \operatorname{clip}\!\left(\tfrac{1}{2}\cdot\frac{n}{N} + \tfrac{1}{2}\cdot\frac{t}{T}\right)
$$

El orden de las reglas importa, porque la primera que se cumple decide:

1. $F \ge 1$ → **descansar**. Cerrar en alto vale más que insistir.
2. Fallos consecutivos y precisión por debajo de 55 % → **escalera de ayuda**.
3. $F \ge 0{,}7$ y las dos últimas no fueron juegos → **jugar**.
4. Hay repasos vencidos → **repasar** el de menor dominio.
5. Precisión ≥ 88 % y hay una habilidad lista para abrirse → **introducir**;
   si no, **subir** dificultad.
6. Hay una debilidad clara → **reforzar** con un ejercicio dirigido.
7. En otro caso → **mantener**.

### 6.1 La escalera de ayuda

Cuando algo va mal, repetir lo mismo más veces no ayuda. Cada peldaño retira una
exigencia distinta, en este orden:

| Peldaño | Qué se retira | Tempo | Longitud | Ayuda visual |
|---------|---------------|-------|----------|--------------|
| 1 | tiempo | ×0,80 | igual | igual |
| 2 | longitud | ×0,80 | ×0,6 | igual |
| 3 | memoria | ×0,75 | ×0,6 | siempre visible |
| 4 | secuencia | ×0,75 | ×0,5 | siempre visible, nota aislada |

### 6.2 Ejercicios dirigidos

Cuando el problema es una nota concreta, no se repite esa nota sola: se intercala
con una que el niño ya domina.

```
Debilidad: Mi          Ancla: Do (dominada)
Secuencia generada:    Mi  Do  Mi  Do  Mi  Mi
```

Alternar obliga a **distinguir** las dos señas, que es justo lo que falla cuando
se confunden. La secuencia cierra con la nota débil para que la última impresión
sea esa.

---

## 7. Selección de la sesión como problema de optimización

### 7.1 Formulación

**Conjuntos.** $A$ actividades candidatas; $S$ habilidades; $S_i$ las que toca la
actividad $i$; $G$ las lúdicas; $R$ los repasos vencidos.

**Variable.** $x_i \in \{0,1\}$, vale 1 si la actividad entra en la sesión.

**Parámetros derivados del gemelo digital.** Probabilidad estimada de éxito,
logística sobre la holgura entre lo que el niño domina y lo que la actividad
exige:

$$
\bar{\mu}_i = \frac{1}{|S_i|}\sum_{s \in S_i}\mu_s,
\qquad
p_i = \frac{1}{1 + e^{-k(\bar{\mu}_i - \text{dif}_i)}},\quad k = 6
$$

Factor de dificultad deseable. El aprendizaje no es máximo donde todo sale bien
ni donde nada sale; se concentra alrededor de $p^\ast = 0{,}75$:

$$
\eta_i = \exp\!\left(-\frac{(p_i - p^\ast)^2}{2\sigma_p^2}\right), \qquad \sigma_p = 0{,}18
$$

Ganancia de aprendizaje, urgencia de repaso, motivación y fatiga inducida:

$$
g_i = \eta_i \cdot \frac{\sum_{s \in S_i}(1 - \mu_s)}{\sqrt{|S_i|}}
\qquad
r_i = \frac{1}{|S_i|}\sum_{s \in S_i} \operatorname{clip}\!\left(\frac{t - \text{due}_s}{3\,\text{días}}, 0, 1\right)
$$

$$
m_i = \beta(\text{tipo}_i) + \nu_i
\qquad
f_i = \frac{d_i}{D}\,(0{,}5 + \text{dif}_i)
$$

donde $\nu_i$ es la novedad (0,25 si no se jugó hace poco) y $\beta$ la
bonificación por tipo: juego 0,85; canción 0,70; ejercicio 0,30; repaso 0,25;
evaluación 0,10.

**Función objetivo:**

$$
\max \sum_{i \in A} \big(\alpha_1 g_i + \alpha_2 r_i + \alpha_3 m_i - \alpha_4 f_i\big)\, x_i
$$

con $\alpha_1 = 1{,}00$, $\alpha_2 = 0{,}70$, $\alpha_3 = 0{,}35$, $\alpha_4 = 0{,}55$.

**Restricciones:**

$$
\begin{aligned}
\text{(1) tiempo:}\quad & \sum_{i \in A} d_i x_i \le T \\
\text{(2) tamaño:}\quad & \sum_{i \in A} x_i = K \\
\text{(3) prerrequisitos:}\quad & x_i \le a_i \\
\text{(4) actividad lúdica:}\quad & \sum_{i \in G} x_i \ge 1 \quad \text{si } K \ge 3 \\
\text{(5) dificultad media:}\quad & \sum_{i \in A} \text{dif}_i\, x_i \le \delta_{\max} K, \quad \delta_{\max} = 0{,}72 \\
\text{(6) no insistir:}\quad & \sum_{i\,:\,s \in S_i} x_i \le 2 \quad \forall s \in S \\
\text{(7) repasos vencidos:}\quad & \sum_{i \in R} x_i \ge 1 \quad \text{si } R \neq \emptyset
\end{aligned}
$$

La restricción (3) es la que impide proponer una actividad que dependa de una
seña todavía bloqueada; $a_i$ vale 1 solo si ninguna habilidad de $S_i$ está en
estado *bloqueada*.

### 7.2 Resolución en tres niveles

El solucionador CBC que trae PuLP para macOS está compilado para Intel; en un Mac
con Apple Silicon requiere Rosetta 2, que no siempre está instalado. Por eso la
resolución tiene tres niveles y el sistema informa cuál usó:

1. **MILP con CBC** a través de PuLP.
2. **Enumeración exhaustiva**, si CBC no está disponible. Con un catálogo de 24
   candidatas y $K = 4$ son $\binom{24}{4} = 10{.}626$ combinaciones: milisegundos,
   y el resultado es el **óptimo exacto**, no una aproximación. Se aplica mientras
   $\binom{|A|}{K} \le 4\times10^5$.
3. **Heurística voraz**, solo si el catálogo creciera lo suficiente como para que
   la enumeración deje de ser viable.

Comprobación sobre datos reales del proyecto: ambos métodos devuelven el mismo
valor objetivo (3,101) y el mismo conjunto de actividades, lo que valida la
enumeración como respaldo del solucionador.

---

## 8. Gemelo digital del aprendiz

El gemelo es la representación del estado de aprendizaje en un momento dado.
No es una tabla más: es lo que consumen el motor adaptativo, el optimizador y la
Zona de Padres, cada uno traduciéndolo a su registro.

```
                        GEMELO DIGITAL
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   Por habilidad         Conducta              Evolución
        │                     │                     │
   dominio               confusiones           minutos/semana
   precisión             tiempo de reacción    actividades
   consistencia          intentos              tendencia
   velocidad
   retención
   días sin practicar
   próximo repaso
```

Al construirlo se aplica el olvido acumulado desde la última práctica, de modo
que consultar el progreso después de dos semanas muestra el estado real y no el
que quedó congelado en la última sesión.

---

## 9. Verificación

| Archivo | Qué comprueba |
|---|---|
| `tests/test_vision.py` | Identidad, invariancia a escala y giro, y la comparación cuantitativa con el método de la versión 1 |
| `tests/test_stabilizer.py` | Que una transición no dispare las notas del camino, que la mano quieta no produzca ráfagas y que sí se pueda repetir una nota tras soltarla |
| `tests/test_mastery.py` | Que una sesión perfecta no baste para dominar, que el intervalo de repaso crezca y se reinicie, y que el olvido degrade una habilidad |
| `tests/test_optimizer.py` | Que se cumplan las restricciones, que MILP y enumeración coincidan, y que la selección cambie con el perfil |
| `tests/capturas.py` | Que las doce pantallas se construyan sin errores, generando una imagen de cada una |

Dos errores reales se encontraron por esta vía y no por inspección: el
estabilizador reiniciaba el contador de «soltar» en cuanto la nota reaparecía, de
modo que nunca se podía repetir la misma nota dos veces; y entrar a recalibrar
borraba las plantillas en memoria antes de capturar nada, así que salir a mitad
de camino dejaba al niño sin señas.

---

## 10. Límites de esta versión

Conviene decirlo sin rodeos, porque marca hasta dónde se puede afirmar algo:

- **El modelo entrenado es simple a propósito.** Desde la sección 11.2,
  `MasteryPredictor.fit()` sí ajusta una regresión logística de tres variables
  sobre los intentos reales de cada niño (nunca datos sintéticos), pero sigue
  siendo un modelo lineal de tres coeficientes, no una red neuronal ni nada
  que necesite más datos de los que un niño genera jugando unos minutos. Se
  activa solo con `MIN_SAMPLES = 40` intentos propios porque un ajuste con
  menos generaliza peor que la fórmula fija — no porque el modelo en sí
  necesite más.
- **No hay aprendizaje por refuerzo.** El motor adaptativo es un conjunto de
  reglas explícitas. Trabaja sobre el mismo objeto `Context` que consumiría un
  agente, de modo que sustituirlo no obliga a tocar nada más.
- **Las constantes no están validadas empíricamente.** Los pesos del dominio, el
  umbral de 0,80, $p^\ast = 0{,}75$ y los coeficientes del objetivo provienen de
  la literatura y del ajuste sobre los datos disponibles, no de un estudio con
  niños. Es la primera cosa que habría que medir.
- **El reconocimiento se probó con una sola calibración.** Ocho señas de una
  persona. Los porcentajes de la sección 3.6 son consistentes, pero la muestra es
  la que es.
- **Dos manos obligatorias.** Sigue el esquema de la versión 1. El descriptor
  admite una sola mano, pero no se ha probado con señas de una mano.
- **Las melodías tradicionales del catálogo son simplificaciones, no
  transcripciones exactas** (sección 11.3.6): se ajustaron a las ocho notas
  naturales que reconoce la aplicación, sin verificación por alguien con
  formación musical formal.
- **Falta el archivo de música de fondo** (sección 11.4.1): el mecanismo de
  las tres capas de sonido y la confinación a las pantallas principales ya
  están implementados y probados, pero sin `musica_fondo.wav` esas pantallas
  quedan en silencio — no es un error, es el estado normal hasta que se
  agregue.
- **El reconocimiento instantáneo (sección 11.5.1) acepta el mismo 8 % de
  falsos positivos en posturas de transición que ya tenía el descriptor por
  sí solo**, medido en `tests/test_vision.py` sin ningún estabilizador de por
  medio. Antes, la votación de varios fotogramas reducía ese margen todavía
  más a cambio de una espera perceptible; ahora se prioriza la respuesta
  inmediata sobre ese margen adicional. Sigue siendo mucho mejor que el 100 %
  de la versión 1, pero conviene decirlo sin rodeos: es un cambio de
  compromiso, no una mejora en ambos sentidos a la vez. Una familia que note
  más notas por error que antes tiene el control "Tiempo de sostener la
  seña" en Ajustes para recuperar margen, a costa de volver a introducir esa
  espera.

---

## 11. Trabajo posterior

En orden de rendimiento por esfuerzo:

1. **Probar con niños reales.** Sin eso, todo lo demás es especulación.
2. **Validar las constantes** con los datos que la aplicación ya recoge,
   incluidas las del propio `MasteryPredictor` (sección 11.2): con más
   perfiles activos convendría revisar si tres variables bastan o si el
   modelo debería crecer.
3. ~~Modelo predictivo de dominio entrenado sobre la tabla `attempts`~~ — ver
   sección 11.2: implementado, en uso, entrenado con datos reales de cada niño.
4. **Aprendizaje por refuerzo** sobre el contexto ya definido. El predictor de
   la sección 11.2 sigue siendo aprendizaje supervisado, no RL: no elige
   acciones para maximizar una recompensa futura, solo estima una
   probabilidad puntual que el optimizador consume.
5. **Señas de una mano** siguiendo el método Curwen-Kodály, que tiene respaldo
   pedagógico y no exige calibración individual.
6. **Informe para el docente**, con varios niños a la vez.

---

## 11.1 Anexo: ajustes posteriores a la primera entrega

Tras la entrega inicial se incorporaron siete ajustes solicitados, todos
compatibles con la arquitectura ya descrita (no se tocó ninguna capa fuera de
la estrictamente responsable de cada cambio) y verificados contra las cinco
suites de prueba existentes más `capturas.py`.

1. **Sonido de acierto solo al completar.** `ExerciseScreen._on_feedback`
   dejó de invocar `AudioEngine.correct()` en cada nota; la respuesta visual
   (destello, marca de la burbuja, mensaje) se conserva nota a nota, pero el
   sonido de logro suena una única vez, al terminar la actividad
   (`_on_finished`, que ya disparaba `star()`/`applause()`).
2. **Nombre de la mascota.** La iguana pasó de "Iguana Maraquita" a **Kiki**:
   un nombre propio corto, fácil de pronunciar para un niño de tres años y que
   no describe simplemente el instrumento que sostiene.
3. **Seña de referencia animada.** `HandSignView` conserva el esquema
   derivado de la calibración real del niño —eso es lo que garantiza que la
   ayuda coincide con lo que el reconocedor espera ver— pero ahora respira
   (leve oscilación de escala), tiene un halo de color que pulsa detrás de la
   mano y un brillo que recorre las puntas de los dedos en bucle. No se
   generaron ilustraciones externas: no hay banco de imágenes de gestos en el
   proyecto, y sustituir el esquema por arte ilustrado por nota sería un
   proyecto de generación de contenido aparte, no un ajuste de esta iteración.
4. **Duración y silencios.** `Activity.duration_s` (ya existente) se muestra
   ahora en las tarjetas de actividad (`AdventureScreen`) y en el encabezado
   del ejercicio. En el modo libre (`FreePlayScreen`) se agregó un cronómetro
   visible desde la primera nota y un botón "Silencio" que inserta la marca
   `SILENCE` (`domain.notes`) en la melodía; `MusicEngine.play_sequence` la
   respeta como una pausa audible y `Staff` la dibuja como un signo de
   silencio, no como una nota.
5. **Ubicación de las melodías guardadas.** Sin cambios de código: ya se
   guardan en `melodias/<perfil>_<timestamp>.json` dentro de la carpeta de
   datos (ahora ese archivo incluye también `duracion_seg`).
6. **Visibilidad del agente adaptativo — y luego, que de verdad aprenda.**
   Primero se hizo visible `AdaptationEngine` (sección 8) en la pantalla de
   resultados. A partir de una aclaración del usuario ("la idea es que el
   agente adaptativo sí funcione y sea entrenable con los datos... para crear
   la ilusión de que el juego es infinito cambiando todo con el progreso"),
   el alcance creció: `MasteryPredictor.fit()` (antes sin implementar) ahora
   ajusta de verdad una regresión logística sobre los intentos reales de cada
   niño, y un generador procedural (`learning.generator`) produce actividades
   nuevas guiadas por ese modelo, de modo que el catálogo crece con el
   progreso en vez de repetir siempre las mismas ~60 actividades. Ver la
   sección 11.2, añadida para documentar esto con el mismo detalle que el
   resto del sistema.
7. **Sonidos.** Se agregó un mecanismo de reemplazo: cualquier `.wav` que la
   familia deje en `sonidos_personalizados/` (ver README) sustituye al sonido
   sintetizado equivalente, sin tocar código. También se agregó una música de
   bienvenida corta y en bucle (`intro_tune`, en `music/synth.py`), generada
   con las mismas notas de la aplicación. No se recibieron archivos de audio
   nuevos adjuntos a la solicitud original pese a la referencia a ellos; el
   mecanismo de reemplazo queda listo para cuando se adjunten.

---

## 11.2 El Agente Adaptativo entrenable y el catálogo infinito

Esta sección documenta la ampliación del punto 6 del anexo anterior: que el
predictor de dominio se entrene de verdad con los datos de cada niño, y que
ese entrenamiento alimente un generador de contenido que hace crecer el
catálogo con el progreso, en vez de repetir siempre las mismas actividades.

### 11.2.1 Por qué antes no se entrenaba

La primera entrega dejó `MasteryPredictor.fit()` sin implementar a propósito:
al momento de esa entrega no existía ni un solo intento real registrado, y
ajustar un modelo con datos inventados habría dado una falsa sensación de
rigor. La interfaz quedó lista para el día en que existieran datos reales —y
ese día es este: la propia aplicación, jugada, produce esos datos en la tabla
`attempts`.

### 11.2.2 Variables y por qué esas y no otras

El obstáculo de fondo es que `SkillState` guarda el dominio **actual** de
cada habilidad, no su historia: no hay una fotografía de "cuánto dominaba
esta nota justo antes de este intento" para cada fila de `attempts`. Entrenar
sobre el dominio de hoy aplicado a intentos de hace semanas sería una fuga de
información del futuro hacia el pasado.

La solución fue elegir variables que se puedan reconstruir dos veces, de
forma consistente:

- **En entrenamiento**, a partir de la propia tabla `attempts`, recorrida en
  orden cronológico y acumulando solo lo que ya había pasado.
- **En predicción**, a partir del `SkillState` vigente, con la misma fórmula.

Concretamente, para una nota $s$ y un instante $t$:

$$
\text{precision}_s(t) = \frac{h_s(t) + \alpha}{n_s(t) + \alpha + \beta},
\qquad \alpha = 1,\ \beta = 3
$$

donde $h_s(t)$ y $n_s(t)$ son aciertos e intentos de esa nota **antes** de
$t$ — la misma suavización bayesiana de la sección 5 (`learning.mastery.precision`),
así que en entrenamiento y en producción es literalmente la misma cuenta.  El
resto de variables:

$$
\text{dificultad}_i \in [0,1] \quad\text{(la de la actividad, sección 6.4)}
$$

$$
\text{dias\_desde\_ultima}_s(t) = \min\!\Big(14,\ \frac{t - t^{\text{prev}}_s}{86400}\Big)
$$

el tiempo en días desde la práctica anterior de esa nota, recortado a dos
semanas para que una pausa de meses no domine el ajuste.

### 11.2.3 El modelo y su ajuste

Regresión logística de tres variables:

$$
p(\text{acierto} \mid s, i, t) = \sigma\big(w_1\, \text{precision}_s(t) +
w_2\, \text{dificultad}_i + w_3\, \text{dias\_desde\_ultima}_s(t) + b\big)
$$

con $\sigma(z) = 1/(1+e^{-z})$. Los pesos $w_1, w_2, w_3, b$ se ajustan por
descenso de gradiente (300 épocas, tasa 0,35) minimizando la entropía cruzada
sobre las variables estandarizadas, y luego se deshace la estandarización
para guardar los coeficientes sobre la escala original. No se usa ninguna
librería de aprendizaje automático externa: con tres variables y unos pocos
cientos de filas, `numpy` alcanza en milisegundos.

El modelo **no se activa** con menos de `MIN_SAMPLES = 40` intentos propios
del perfil — con menos datos, la fórmula fija de la primera entrega
generaliza mejor que cualquier ajuste. A partir de ahí, se reentrena cada
`RETRAIN_EVERY = 20` intentos nuevos (`learning.session_flow._maybe_retrain`,
llamado al cerrar cada actividad), así que el agente sigue cambiando con el
progreso en vez de congelarse tras el primer ajuste. Los pesos se guardan por
perfil en la tabla `meta` (clave `predictor_<id>`): cada niño tiene su propio
modelo, entrenado solo con sus propios datos, y nunca se mezclan entre
perfiles ni sobreviven a un cambio de niño dentro de la misma instalación.

Para una actividad con varias notas involucradas, la probabilidad de la
actividad completa es el promedio de las probabilidades por nota — la misma
convención que ya usaba la fórmula paramétrica con $\bar\mu$, para que ambos
regímenes se lean en la misma escala.

`SessionOptimizer.score()` recibe el predictor como parámetro opcional: sin
él, o mientras no esté entrenado, usa exactamente la misma fórmula fija de
antes (sección 9); en cuanto se entrena, sus probabilidades reemplazan a la
fórmula sin que cambie ninguna otra parte del optimizador. Es el punto de
extensión que la sección 10 de la primera entrega dejó anunciado.

### 11.2.4 El generador procedural: de dónde sale la sensación de infinito

Sesenta actividades escritas a mano se agotan. `learning.generator` propone,
cada vez que se arma la ruta del día, hasta seis actividades nuevas por
nivel: secuencias de notas elegidas al azar entre las que el niño ya tiene
abiertas, con más peso para las que le cuestan más (las mismas "notas
flojas" que ya usa `AdaptationEngine.weakest`). De cada borrador se generan
tres variantes y se elige la que el Agente Adaptativo predice más cerca de
la dificultad deseable:

$$
i^\ast = \arg\min_i \; \big| p_i - p^\ast \big|, \qquad p^\ast = 0.75
$$

el mismo $p^\ast$ del optimizador (sección 9, Bjork y Bjork, 2011): ni tan
fácil que aburra, ni tan difícil que frustre. Esas candidatas se suman —no
reemplazan— al catálogo fijo antes de puntuar y resolver la sesión; el
optimizador decide como siempre cuáles entran. Solo las que efectivamente
resultan elegidas se guardan en la tabla `activities` (`ActivityRepository.upsert_many`,
llamado desde `AdventureScreen._calcular_ruta`), con un código único
`proc_<hex>`: así el catálogo crece con lo que de verdad se llegó a jugar, y
una actividad generada que quede en la cola de "lo siguiente" se puede
recuperar por su código más tarde, igual que cualquier otra.

### 11.2.5 Lo que esto sigue sin ser

Para que quede tan claro como el resto de este documento: esto es aprendizaje
supervisado sobre un problema de clasificación binaria (acierto/fallo), no
aprendizaje por refuerzo. No hay una política que elija acciones para
maximizar una recompensa futura descontada; hay un modelo que estima una
probabilidad puntual, y esa probabilidad la sigue consumiendo el mismo
optimizador MILP de la sección 9. El punto 4 de la sección 11 (RL) sigue
pendiente, y seguiría siendo el siguiente paso natural si se quisiera que el
propio agente decidiera secuencias de actividades óptimas a largo plazo, en
vez de solo estimar el éxito de la siguiente.

---

## 11.3 El módulo Canciones: la mecánica de nota viajera

A partir del contexto de la versión 0 de la aplicación (monolítica, en Pygame)
se pidió recuperar su minijuego "Notas Rítmicas" —notas que viajan por el
pentagrama hacia una línea de impacto, estilo Guitar Hero, donde solo cuenta
la seña hecha justo cuando la nota cruza esa línea— y aplicarlo a un módulo
nuevo, "Canciones", con la visual ya existente de esta versión (no los
gráficos de la v0) y con más melodías, incluidas las que el niño graba en
Modo Libre.

### 11.3.1 Por qué un módulo aparte, y no cambiar el ejercicio guiado

El ejercicio guiado (`ExerciseScreen` / `ActivityRunner`, sección 6) espera
indefinidamente —hasta `GIVE_UP_AFTER` fallos— a que el niño haga la seña
correcta antes de avanzar. Es la decisión correcta para *aprender* una seña
nueva: no tiene sentido apurar a un niño de tres años que todavía está
formando la mano. Pero no es "tocar una canción": una melodía tiene un pulso,
y tocarla de verdad significa llegar a tiempo a cada nota, no en el orden
correcto sin más. De ahí que la mecánica de nota viajera viva en una pantalla
y un motor aparte (`ui.screens.rhythm`, `learning.rhythm.RhythmRunner`) en vez
de reemplazar al ejercicio guiado: son dos maneras de practicar con objetivos
distintos, y ambas conviven — de hecho, las mismas canciones del catálogo se
pueden tocar desde el mapa de aventura (paso a paso) o desde Canciones (nota
viajera).

### 11.3.2 El reloj en vez de la espera

`RhythmRunner` no espera una seña: calcula por adelantado el instante en que
el centro de cada nota cruza la línea de impacto y compara ese instante con
el reloj de la partida en cada tick (cada `TICK_MS = 30` ms). Con tempo
constante — la opción elegida para este módulo, sin aceleración progresiva
dentro de una misma canción —, el intervalo entre notas consecutivas es
siempre el del compás:

$$
g = \frac{60000}{\text{tempo\_bpm}} \quad \text{(ms)}
$$

y el instante de llegada de la nota $i$ es $a_i = a_{i-1} + g$, con
$a_0 = \text{TRAVEL\_MS}$ (el tiempo de vuelo, 2200 ms, que es cuánto tarda una
nota en cruzar la pantalla desde que aparece — así la primera nota también se
ve venir, no aparece ya sobre la línea).

Una tecla es instantánea; una seña no lo es, porque el estabilizador temporal
de la cámara (sección 3.5) necesita sostenerla un momento para confirmarla.
Exigir el cruce exacto habría sido injusto. Por eso cada nota tiene una
ventana de acierto alrededor de $a_i$, no un instante:

$$
\text{media}_i = \frac{\max\!\big(\text{MIN\_WINDOW},\ \min(\text{tolerance\_ms},\ g \cdot 0.85)\big)}{2}
$$

$$
\text{ventana}_i = \big[\,a_i - 1.15 \cdot \text{media}_i,\ \ a_i + 0.85 \cdot \text{media}_i\,\big]
$$

La ventana es más ancha *antes* de la línea que después, a propósito: un niño
suele empezar a sostener la seña con anticipación, y así el tiempo que tarda
el estabilizador en confirmarla no lo penaliza. `MIN_WINDOW_MS = 380` evita
que una canción muy rápida deje una ventana imposible de acertar.

### 11.3.3 Notas falladas: sigue sin parar

Si una nota cruza su ventana sin que se confirme la seña esperada, se
registra como un intento fallido (`Attempt(correct=False)`) y la partida
sigue de inmediato con la nota siguiente — sin la escalera de ayuda ni el
"vamos a la siguiente" del ejercicio guiado (sección 6.1), y sin detenerse a
esperar. Es la misma sensación que la v0: si no se llegó a tiempo, se perdió
esa nota, y la canción sigue. `tests/test_rhythm.py` verifica exactamente
esto — una nota que deliberadamente nunca se confirma no cuelga la partida.

(La sección 11.7 revisa qué cuenta como "no se llegó a tiempo": desde ese
cambio, una seña equivocada mientras la nota está en juego ya no la falla de
inmediato — solo el cruce completo de la ventana sin acierto lo hace, igual
que en v0.)

### 11.3.4 Compatibilidad con el dominio y el Agente Adaptativo

`RhythmRunner` expone la misma superficie pública que `ActivityRunner` que
consume `learning.session_flow.apply_result()`: `activity`, `attempts`,
`build_result()`, `per_note_summary()`, `steps_correct`, `total_steps`. Una
canción del catálogo jugada con nota viajera actualiza el dominio por nota,
desbloquea logros y alimenta el reentrenamiento del `MasteryPredictor`
(sección 11.2) exactamente igual que un ejercicio guiado — es la misma tabla
`attempts`, sin ninguna ruta especial.

Una melodía grabada en Modo Libre usa el mismo motor solo para puntuar en
pantalla (estrellas, puntaje, precisión): nunca llega a `apply_result()`. Es
una decisión explícita, no un descuido — una improvisación del niño no debe
mezclarse con la práctica que el sistema usa para medir dominio real.

### 11.3.5 "A mi ritmo" frente a "tempo fijo"

Desde esta versión, `FreePlayScreen` guarda además el intervalo real, en
milisegundos, entre cada nota grabada y la anterior (`data.melodies`,
campo `gaps_ms`); las melodías guardadas antes de este cambio no lo tienen, y
se reconstruye un promedio a partir de la duración total
(`melodies.estimated_gaps_ms`). "A mi ritmo" pasa esos intervalos reales a
`RhythmRunner`, recortados a $[\text{GAP\_MIN\_MS}, \text{GAP\_MAX\_MS}] =
[220, 4000]$ ms para que una pausa larga accidental durante la grabación no
deje la partida esperando; "tempo fijo" la toca a un pulso constante
(84 bpm), como cualquier canción del catálogo.

### 11.3.6 El catálogo ampliado

Se agregaron doce melodías tradicionales e infantiles al catálogo (de seis a
dieciocho), transcritas de forma simplificada a las ocho notas naturales que
reconoce la aplicación — sin alteraciones cromáticas, porque el instrumento
no las tiene. Son simplificaciones pensadas para que la línea melódica se
reconozca y sea jugable en este rango, no transcripciones musicológicas
exactas; conviene revisarlas con alguien con formación musical formal si
llegan a usarse fuera de este contexto pedagógico. Una de las doce es el tema
de la "Oda a la alegría" de Beethoven (dominio público); las once restantes
son melodías tradicionales y de folclore infantil, de las que aquí solo se
codifica la línea de notas, nunca la letra.

### 11.3.7 Las ilustraciones de gestos

La burbuja que viaja hacia la línea de impacto puede mostrar una ilustración
genérica de la seña en vez de solo su color y su nombre cantado
(`ui.widgets.gesture_images`); es un añadido opcional, no algo que dependa de
la calibración de cada niño — el dibujo que sí depende de la calibración de
cada niño sigue viviendo aparte, en `HandSignView`. Las ocho ilustraciones
(una por nota, de Do3 a Do4) ya están incluidas en
`handsingkids/ui/assets/gestos/`; si en algún momento faltara alguna, la
burbuja simplemente se ve como las burbujas de nota que ya existían en el
resto de la aplicación — nada se rompe por no tenerla.

---

## 11.4 Las tres capas de sonido y la música de fondo fuera del juego

Petición del usuario tras entregar sus propias grabaciones de las ocho notas:
que el sonido de cada nota deje de ser el timbre sintético y use esas
grabaciones, y que cualquier música de fondo quede fuera de las pantallas
donde la cámara evalúa gestos, para no competir con el sonido de la nota que
el niño necesita escuchar con claridad.

### 11.4.1 Prioridad entre sonidos

`music.audio.AudioEngine` ya distinguía dos niveles: lo sintetizado en el
primer arranque (`music.synth`) y lo que una familia deja en
`sonidos_personalizados/` (`core.config.custom_audio_dir`). Se intercaló un
tercer nivel intermedio, `core.config.bundled_audio_dir`
(`handsingkids/ui/assets/audio/`): sonidos reales incluidos con la propia
aplicación, con prioridad sobre el sintetizado pero por debajo de lo que la
familia deje. La resolución de cada nombre de sonido queda, de mayor a menor
prioridad:

$$\text{personalizado}(n) \;\succ\; \text{incluido}(n) \;\succ\; \text{sintetizado}(n)$$

Se usa el primero de los tres que exista en disco para el nombre $n$
(`nota_DO3`, `musica_fondo`, etc.); si ninguno existe salvo el sintetizado,
la aplicación sigue funcionando exactamente como antes de este cambio. La
capa incluida no está limitada a reemplazar nombres que ya existían: un
archivo `<nombre>.wav` nuevo en esa carpeta introduce un sonido reproducible
aunque `music.synth` nunca lo haya generado — es el caso de `musica_fondo`,
que no tiene equivalente sintetizado.

Las ocho notas (`nota_DO3.wav` … `nota_DO4.wav`) ya están incluidas en
`handsingkids/ui/assets/audio/`, convertidas a PCM de 16 bits mono a 44.100
Hz para mantener la misma latencia de reproducción que el resto de sonidos
generados. Falta `musica_fondo.wav`: el usuario mencionó un archivo para la
música de fondo, pero no llegó a adjuntarse — sin él, las pantallas
principales quedan en silencio (comportamiento normal, no un error) hasta que
se agregue.

### 11.4.2 Confinar la música de fondo a las pantallas principales

La decisión de dónde suena la música de fondo se centralizó en un solo punto,
`MainWindow.navigate()` (`app.py`), en vez de repetirla pantalla por
pantalla: al terminar cada navegación, `_actualizar_musica_de_fondo(nombre)`
apaga la música si la pantalla de destino es una de las que activan la
cámara para evaluar gestos (`calibration`, `exercise`, `freeplay`, `rhythm`),
y la enciende — o la deja sonando, si ya sonaba — en cualquier otra. La
pantalla de bienvenida queda excluida de esta regla porque administra su
propia música (`musica_inicio`) al entrar y salir.

`AudioEngine.play_music()` se hizo idempotente respecto al nombre de la
pista: llamarlo dos veces seguidas con el mismo nombre no reinicia la
reproducción desde el principio. Esto es lo que permite invocar la función
en cada cambio de pantalla entre pantallas principales (por ejemplo, mapa →
inicio → progreso) sin que la música de fondo dé un salto audible en cada
una — solo se reinicia de verdad al volver de una pantalla con cámara activa.

---

## 11.5 Reconocimiento instantáneo, silencio en las señas equivocadas de Canciones y Martinillo

Tres pedidos del usuario tras probar el módulo Canciones: que la nota se
reconozca en cuanto se hace, sin ninguna "barra de aceptación" en toda la
aplicación; que en Canciones solo suene la nota correcta, no cualquier seña
que el niño haga; y que se agregue "Martinillo" al catálogo.

### 11.5.1 De ocho fotogramas a uno: qué es en realidad la "barra de aceptación"

El anillo que se llenaba sobre la cámara (`CameraView.set_ring`, dibujado en
`_draw_ring`) no era decorativo: representaba `GestureStabilizer.progress`,
la fracción de la ventana deslizante que ya coincide con la lectura actual.
Con la configuración de fábrica anterior (`window_frames = 8`,
`agreement_ratio = 0{,}62`), hacían falta

$$\text{necesarios} = \max(2, \operatorname{round}(0{,}62 \times 8)) = 5$$

fotogramas de acuerdo antes de confirmar una nota — a unos 24 cuadros por
segundo, poco menos de un cuarto de segundo. Es lo que el usuario percibía
como una espera y pedía quitar.

La solución no fue eliminar el estabilizador (`vision.stabilizer`), sino
llevar su ventana a un solo fotograma. Con `window = 1`, la propiedad
`current` de `GestureStabilizer` ya no vota entre varias lecturas: el
`deque` tiene como máximo un elemento, así que "la lectura más votada de la
ventana" es, sencillamente, la lectura de ese fotograma. Y con
`needed = max(1, \operatorname{round}(agreement \times 1)) = 1$, una sola
lectura que supere `confidence_threshold` ya confirma la nota. El resultado
es que el estabilizador deja de aportar filtrado temporal por votación, pero
conserva sus otras dos funciones — el periodo refractario
(`refractory_s`) y la exigencia de "soltar" antes de repetir la misma nota
(`release_frames`) — que no dependen del tamaño de la ventana.

¿Es esto razonable? La respuesta ya estaba medida en `tests/test_vision.py`:
`benchmark_falsos_positivos` mide el descriptor y el clasificador solos, sin
ningún estabilizador de por medio, y ya arrojaba un 8 % de falsos positivos
sobre posturas de transición y manos cruzadas (frente al 100 % de la
versión 1). Ese 8 % es, en la práctica, el precio de la instantaneidad — y
es exactamente lo que se paga ahora, porque quitar la votación multifotograma
no cambia el número: solo deja de pedir, además, que la postura ambigua se
sostenga varias veces seguidas para colarse.

La ventana sigue siendo ajustable (`VisionSettings.window_frames`, control
"Tiempo de sostener la seña" en Ajustes, ahora con rango de 1 a 16 en vez de
4 a 16): una familia que necesite más margen para un niño en particular
puede subirla, y recupera el comportamiento de votación multifotograma de
antes. El techo de "al menos 2 votos" (`max(2, ...)`) se cambió a "al menos
1" (`max(1, ...)`) en las dos fórmulas del estabilizador (`progress` y
`push`) precisamente para permitir `window = 1`; con cualquier `window ≥ 2`
configurado a mano, el comportamiento es idéntico al de antes.

El anillo de aceptación se quitó de las tres pantallas de juego (`exercise`,
`rhythm`, `freeplay`) — ya no había ningún progreso real que dibujar, y
mostrarlo habría sido, como mucho, un parpadeo entre vacío y lleno en cada
fotograma. La pantalla de calibración conserva su propio anillo, que es un
uso distinto (una cuenta regresiva de varios segundos por muestra, no una
confirmación de gesto) y no se tocó.

### 11.5.2 Silencio en las señas equivocadas, dentro de Canciones

Antes de este cambio, `RhythmScreen._on_confirmed` reproducía la nota
reconocida incondicionalmente (`ctx.music.trigger(nota, confianza)`) y
después, por separado, le preguntaba al motor (`RhythmRunner.submit`) si
había sido un acierto. El niño, entonces, escuchaba cualquier seña que
hiciera, correcta o no.

`RhythmRunner.submit()` ya devolvía si la seña coincidía con la nota activa
en ese instante (`n.code == nota`, con `_nota_activa()` decidiendo cuál nota,
si alguna, está dentro de su ventana de acierto ahora mismo). El cambio fue
invertir el orden y condicionar el sonido a ese resultado:

```python
if self.runner.submit(nota, confianza):
    self.ctx.music.trigger(nota, confianza)
```

Con esto, una seña que no es la nota activa —sea porque es la nota
equivocada, sea porque no hay ninguna nota dentro de su ventana en ese
momento— se sigue registrando (para el puntaje y el intento, exactamente
igual que antes), pero no suena. El único sonido que un niño escucha dentro
de Canciones es el de haber acertado, lo cual, además, refuerza la
mecánica: el sonido pasa a ser la confirmación del acierto en vez de un eco
de cualquier movimiento de manos. Este cambio se limitó a Canciones, tal
como lo pidió el usuario — el ejercicio guiado sigue sonando cualquier nota
reconocida, que es parte de su propósito exploratorio.

("no cuenta" pasó, en la sección 11.7, de "falla la nota en silencio" a
"la nota sigue pendiente en silencio, y se puede reintentar" — el silencio
en la seña equivocada descrito aquí no cambió, pero sí lo que le pasa a la
nota después de ese silencio.)

### 11.5.3 Martinillo

Se agregó "Martinillo" al catálogo (`cancion_martinillo`, nivel 5, 88 bpm),
la versión en español de la ronda tradicional francesa "Frère Jacques"
("¿Fray Santiago?" en algunas regiones). Es dominio público, como el resto
del repertorio tradicional ya incorporado. Su forma —dos frases cortas
repetidas dos veces y un remate— la hace, en la práctica, más fácil de lo
que sus 32 notas sugieren, porque buena parte es la misma frase que vuelve.

El remate tradicional ("din don dan") baja de la tónica a una quinta más
grave y de ahí a la tónica de la octava inferior — dos notas que no existen
en el rango de la aplicación (Do3 a Do4, sin octava más grave). Se adaptó
como Do4–Sol3–Do3: la tónica aguda, la dominante intermedia y la tónica
grave disponibles, que conserva el efecto de campana descendente sin salirse
de las ocho notas reconocidas. Como con el resto del catálogo ampliado
(sección 11.3.6), solo se codifica la línea melódica, nunca la letra.

---

## 11.6 El sonido que se repetía solo, el tiempo elegible en Canciones y las ilustraciones en toda la aplicación

Tres pedidos del usuario después de probar la "Sexta iteración": que el
sonido dejara de duplicarse, que Canciones no fuera tan exigente y se
pudiera elegir el tiempo porque "está muy rápido", y que las ilustraciones
de las señas se usaran en toda la aplicación, no solo en las burbujas
viajeras de Canciones.

### 11.6.1 Por qué se duplicaba el sonido: el efecto secundario de `window = 1`

El diagnóstico no estaba en el motor musical (`MusicEngine.trigger` llama a
`AudioEngine.play_note` una sola vez por evento) ni en el bus de eventos
(`Event.GESTURE_CONFIRMED` tiene un único emisor en `vision.service` y una
única suscripción por pantalla): ambos se revisaron y son consistentes. El
problema estaba un nivel más abajo, en una consecuencia no anticipada de la
sección 11.5.1.

`GestureStabilizer` distingue dos mecanismos independientes del tamaño de la
ventana: el periodo refractario (`refractory_s`, bloquea cualquier
confirmación un rato tras la anterior) y el "soltar" (`release_frames`,
exige que la lectura deje de coincidir con la última nota confirmada durante
varios fotogramas seguidos antes de permitir que esa misma nota vuelva a
sonar). Con `window_frames = 8`, una lectura perdida de la cámara durante
uno o dos fotogramas —MediaPipe pierde el contorno de la mano un instante,
incluso con la mano perfectamente quieta— no bastaba para que `current`
(la lectura más votada de la ventana) cambiara: el resto de fotogramas del
`deque` seguían pesando. Con `window_frames = 1` (el valor de fábrica desde
la sección 11.5), ya no hay ningún voto que amortigüe ese parpadeo: cada
fotograma se juzga solo.

`release_frames` venía en 2 desde antes de este cambio, un valor pensado
para una ventana de 6 u 8 fotogramas, donde dos fotogramas de ruido eran
poco frecuentes. Con `window_frames = 1`, dos fotogramas de parpadeo bastan
para que `_release_count` llegue a 2, se marque `_released = True`, y el
fotograma siguiente —la misma nota, sin que el niño soltara la seña ni
hiciera nada distinto— vuelva a confirmar, con `needed = 1` voto exigido a
esa ventana de tamaño 1. El resultado es dos eventos `GESTURE_CONFIRMED`
genuinos y separados para la misma nota sostenida, cada uno con su propio
`MusicEngine.trigger()`: el sonido no se duplicaba dentro de una sola
reproducción, sino que la nota sonaba dos veces porque el estabilizador la
confirmó dos veces.

La corrección fue subir `release_frames` de 2 a 6, tanto en
`GestureStabilizer.__init__` como en `VisionSettings.release_frames`. Seis
fotogramas de lectura distinta (o ausente) ya no los produce un parpadeo
típico del rastreo, pero siguen siendo bastante menos de un segundo — un
niño que de verdad baja la mano o cambia de seña sigue pudiendo repetir la
misma nota sin sentir espera. `tests/test_stabilizer.py` añade
`test_parpadeo_breve_no_duplica_la_nota_sostenida`, que reproduce ambos
casos con la configuración de fábrica: dos fotogramas de ruido no repiten
la nota, seis fotogramas de soltar de verdad sí.

### 11.6.2 Tiempo elegible en Canciones, y ventanas menos estrictas para todos

`RhythmRunner` ahora acepta `tempo_factor` (por defecto 1,0), que se aplica
al intervalo entre notas antes de calcular su ventana de acierto — tanto a
tempo constante como con tiempos grabados ("a mi ritmo"):

$$\text{intervalo efectivo} = \frac{\text{intervalo planificado}}{\text{tempo\_factor}}$$

Tres valores predefinidos (`TEMPO_FACTORS`): 🐢 lento (0,72), normal (1,0) y
🐇 rápido (1,15). Como la ventana de acierto de cada nota está acotada por
lo ancho que sea su propio intervalo (`half = min(tolerance\_ms, gap \times
0{,}85) / 2`), elegir un tempo más lento no solo separa más las notas en el
tiempo: también ensancha, de forma proporcional, cuánto margen hay para
confirmar cada una. La pantalla Canciones (`ui.screens.songs.SongRow`)
agrega dos botones pequeños (🐢/🐇) junto a "Jugar" en cada canción del
catálogo, que abren la partida con ese factor ya elegido.

Independientemente del tempo elegido, la ventana mínima
(`MIN_WINDOW_MS`) y el tramo "bien" (`TIER_GOOD_MS`) subieron de 380 a
480 ms, y el tramo "perfecto" (`TIER_PERFECT_MS`) de 180 a 200 ms: con el
reconocimiento instantáneo de la sección 11.5, el niño ya no tiene el
margen adicional que daba la vieja votación multifotograma, así que la
ventana se ensancha un poco para todos, no solo para quien elija tempo
lento. `tests/test_rhythm.py` añade
`test_factor_de_tempo_afloja_la_velocidad_y_la_ventana`, que comprueba que
lento > normal > rápido tanto en el intervalo entre notas como en el ancho
de la ventana.

### 11.6.3 Las ilustraciones de gestos, en cualquier burbuja de nota

Las ilustraciones genéricas (`ui.widgets.gesture_images.gesture_pixmap`) ya
se usaban en las burbujas viajeras de Canciones (`TravelingNoteTrack`,
sección 11.3.7) pero en ningún otro lugar: `NoteBubble`
(`ui.widgets.notes`), el círculo compartido que además dibuja la pista del
ejercicio guiado, la fila de referencia de Modo libre y la fila de notas de
la Calibración, seguía mostrando solo el color y el nombre cantado.

El cambio fue mover el mismo patrón de dibujo (recortar un `QPainterPath`
circular y pintar el `QPixmap` dentro) a `NoteBubble.paintEvent`, con la
misma regla de nunca romper nada si falta la imagen: se usa la ilustración
si existe y la nota está pendiente o es la actual; una vez juzgada
(acertada o fallada), vuelve a mostrarse el color y el nombre, para que ese
resultado se lea sin depender de si hay o no ilustración. Como
`NoteBubble` es una única clase compartida por las tres pantallas, este
cambio las alcanza a todas sin tocar cada una por separado.

Quedan fuera a propósito "Ver la seña" (`HandSignView` en el ejercicio) y
las tarjetas de *Mi progreso*: ahí se dibuja la seña que el propio niño
calibró, redibujada a partir de sus propios puntos de referencia — una
ilustración genérica sería un paso atrás, no una mejora, porque esa vista
existe precisamente para mostrar lo que el reconocedor espera ver *de ese
niño*, no una seña de referencia cualquiera.

---

## 11.7 Canciones calca las reglas de "Notas Rítmicas", no su pantalla ni sus constantes

Pedido del usuario: "vamos a cambiar el modo canción y vamos a calcar notas
rítmicas tal cual, pero con el estilo visual de acá y las nuevas canciones."
Es decir, recuperar la mecánica original de v0 con la mayor fidelidad
posible, sin deshacer ni el estilo visual de esta versión (sección 11.3) ni
el catálogo ampliado (sección 11.3.6) ni las correcciones ya entregadas en
las secciones 11.5 y 11.6.

Para saber qué es "tal cual" de verdad, en vez de suponerlo, se revisó el
código fuente de v0 directamente (`game.py`, `constants.py`, `vision.py` de
esa versión) en busca de tres cosas concretas: la fórmula de puntaje, el
comportamiento ante una seña equivocada y el HUD de juego. Vale la pena
anotar un hallazgo negativo: la documentación de este proyecto había dado
por hecho, en algún momento, que las notas de v0 aceleraban progresivamente
dentro de una misma canción; revisando `NoteSprite` en `game.py`, su
velocidad (`speed = 4`, en píxeles por fotograma) es una constante fija en
todo el archivo — no hay ninguna aceleración, ni por nota ni por canción.
Ese supuesto no se traslada a ningún lado de este cambio porque, en
rigor, nunca existió en v0.

### 11.7.1 Qué se calcó literalmente

**La fórmula de combo** (`ScoreManager.hit()` de v0):

$$\text{multiplicador} = \min\!\Big(1{,}0 + \Big\lfloor\frac{\text{combo}}{10}\Big\rfloor \times 0{,}5,\ 4{,}0\Big)$$

Antes de este cambio, `RhythmRunner._award()` usaba una escalera propia
(cada 5 de racha, +0,25, techo 3,0); ahora usa exactamente la de v0: cada
10 de racha suma +0,5 al multiplicador, con techo en 4,0. Los puntos base
por tramo (`TIER_POINTS = {"perfecto": 100, "bien": 70, "vale": 50}`) ya
coincidían con los de v0 (`Perfect/Good/Ok = 100/70/50`) desde antes de
este cambio, así que no se tocaron. `tests/test_rhythm.py` agrega
`test_formula_de_combo_calca_notas_ritmicas`, que hace correr 25 aciertos
"perfecto" seguidos y compara el puntaje final contra la fórmula de v0
calculada aparte, nota por nota.

**El perdón de la seña equivocada.** En v0, un sprite de nota que colisiona
con la zona de impacto (`hit_zone`) y no coincide con la seña reconocida en
ese instante, simplemente no hace nada: sigue viajando sin sonido, sin
romper la racha y sin marcarse fallada; solo se falla cuando el sprite
termina de cruzar la zona de impacto por completo (`note.rect.right <
hit_zone.left`) sin haber acertado nunca. Antes de este cambio,
`RhythmRunner.submit()` era más estricto que eso: una seña equivocada
mientras una nota estaba en juego resolvía esa nota como fallada de
inmediato (rompía la racha ahí mismo, aunque quedara tiempo en la ventana).
Ahora `submit()` distingue ambos casos: si la seña no es la esperada,
registra el intento (sigue alimentando el dominio por nota y el
`MasteryPredictor`, sección 11.2) pero deja la nota en `PENDING` — el niño
puede volver a intentarla cuantas veces quiera mientras siga dentro de su
ventana de acierto, y solo el cruce completo de esa ventana sin acierto
(`_tick`/`_resolve_miss`, sin cambios) la marca fallada. Una consecuencia
menor, y correcta: una nota ahora puede acumular más de un `Attempt` (uno
por cada intento equivocado, y el último correcto o el de fallo por tiempo)
en vez de exactamente uno; `learning.session_flow.apply_result()` ya
recorría `attempts`/`per_note_summary()` de forma genérica y no asumía una
relación 1 a 1, así que no necesitó ningún cambio.
`tests/test_rhythm.py` amplía `test_solo_suena_la_nota_correcta` para
cubrir justo esto: una seña equivocada no suena y deja la nota `PENDING`;
un reintento con la seña correcta, dentro de la misma ventana, sí suena y
sí la resuelve como acierto.

**El HUD de juicio en vivo.** v0 dibujaba, sobre la pantalla de juego, un
texto de juicio por cada nota ("Perfect"/"Good"/"Ok"/"Miss") con un color
por categoría y una precisión (`accuracy()`) que se recalculaba nota a
nota, no solo al final. `RhythmScreen` agrega una etiqueta central
(`etiqueta_juicio`) que muestra "¡Perfecto!"/"¡Bien!"/"Vale"/"Fallada" con
los colores de esta aplicación (verde menta, azul cielo, naranja mandarina
y rosa chicle, respectivamente, en vez de los colores literales de v0) y se
apaga sola a los 550-700 ms; y un chip nuevo junto al puntaje y la racha
(`chip_precision`) que muestra `RhythmRunner.live_accuracy`, una propiedad
nueva que calcula la precisión solo sobre las notas ya juzgadas hasta ese
momento — el mismo `accuracy()` de v0, adaptado a esta interfaz de chips en
vez de un HUD dibujado a mano.

### 11.7.2 Qué no se calcó, y por qué

**Los umbrales de distancia/tiempo de v0** (12 px = Perfect, 28 px = Good,
a 4 px/fotograma y 60 fps, es decir, aproximadamente 50 ms y 117 ms) no
tienen una traducción directa a este motor: v0 juzga por distancia de un
sprite a una zona fija en píxeles, esta versión por milisegundos respecto a
un instante calculado y escalado por tempo (sección 11.3.2). Forzar esos
mismos milisegundos aquí — mucho más estrictos que los ya ajustados en la
sección 11.6.2 tras la queja explícita de que Canciones "está muy rápido"—
deshacería esa corrección. `TIER_PERFECT_MS`, `TIER_GOOD_MS` y
`MIN_WINDOW_MS` se dejaron como quedaron en la sección 11.6.2.

**La pantalla y el trazado por pentagrama** de v0 (una posición vertical
fija por nota, `NOTE_POSITIONS`) no se adoptaron: la sección 11.3 ya había
decidido, a propósito, una única burbuja viajera en vez de un pentagrama de
ocho carriles, y el pedido de esta iteración pide explícitamente mantener
"el estilo visual de acá".

**El clasificador de gestos de v0** (similitud coseno pura contra un umbral
fijo, sin ningún filtrado temporal) no se recuperó: es estrictamente peor
que el descriptor y clasificador actuales (sección 3, con su comparación
medida en `tests/test_vision.py`), y v0 tampoco tenía ningún mecanismo de
"soltar" (`release_frames`) — adoptarlo tal cual habría reintroducido el
sonido duplicado que la sección 11.6.1 ya diagnosticó y corrigió.

**Los rangos S/A/B/C/D de `evaluate_rank()`** de v0 no se agregaron: el
pedido del usuario no los menciona, y esta versión ya tiene su propio
sistema de estrellas (`RhythmRunner.stars()`, secciones 6 y 11.3.4)
consistente con el resto de la aplicación; se puede revisar más adelante si
se pide explícitamente.

---

## 12. Referencias sugeridas

Estas obras sostienen las decisiones de diseño. Conviene verificar edición y
paginación antes de citarlas en el documento final.

- Bjork, R. A., & Bjork, E. L. (2011). Making things hard on yourself, but in a
  good way: Creating desirable difficulties to enhance learning. En
  *Psychology and the real world*. Worth Publishers.
- Choksy, L. (1999). *The Kodály method I: Comprehensive music education*
  (3.ª ed.). Prentice Hall.
- Ebbinghaus, H. (1885). *Über das Gedächtnis: Untersuchungen zur
  experimentellen Psychologie*. Duncker & Humblot.
- Vygotsky, L. S. (1978). *Mind in society: The development of higher
  psychological processes*. Harvard University Press.
- Woźniak, P. A., & Gorzelańczyk, E. J. (1994). Optimization of repetition
  spacing in the practice of learning. *Acta Neurobiologiae Experimentalis,
  54*(1), 59–62.
- Zhang, F., Bazarevsky, V., Vakunov, A., Tkachenka, A., Sung, G., Chang, C.-L.,
  & Grundmann, M. (2020). MediaPipe Hands: On-device real-time hand tracking.
  *arXiv preprint arXiv:2006.10214*.
