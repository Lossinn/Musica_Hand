"""Inserta un apartado «Trazabilidad de las cifras» antes de las conclusiones de cada escrito final."""
ANCLA = '    e.sec("Conclusiones")'
BLOQUES = {
    "ef_petro.py": [["Aciertos por nivel de ruido", "resultados_vision.json (evidencia_vision.py, semilla 11)"], ["Notas falsas y desglose", "resultados_vision.json (semilla 23)"], ["Estabilidad con 30 semillas", "resultados_vision.json"],
                    ["Separabilidad y latencia", "resultados_vision.json; matriz_similitud"], ["Sensibilidad de umbrales", "sensibilidad_umbrales.json (sensibilidad_umbrales.py)"], ["Pruebas del repositorio", "salida_pruebas.txt"]],
    "ef_negrete.py": [["Ventana de acierto por tempo", "Cálculo con la ecuación del código (este documento)"], ["Sensibilidad del piso", "Cálculo con la ecuación del código (este documento)"], ["Latencia", "resultados_vision.json"],
                      ["Notas falsas", "resultados_vision.json"], ["Constantes del motor temporal", "Código del repositorio (estabilizador y canciones)"], ["Piso de 380 ms", "Documentación técnica del proyecto"]],
    "ef_carrascal.py": [["Constantes del dominio y del repaso", "Código del repositorio (módulos de dominio y repaso)"], ["78 % del predictor", "Prueba unitaria del predictor (salida_pruebas.txt)"], ["Dominio según $R$ y $S$", "Cálculo con la ecuación del dominio (este documento)"],
                        ["Umbrales de retención y días", "Cálculo con supuestos explícitos (este documento)"], ["Baterías de dominio y predictor", "salida_pruebas.txt"]],
    "ef_quintana.py": [["40 ms y valor 2,9524", "Prueba del optimizador (salida_pruebas.txt)"], ["Pesos y restricciones", "Código del repositorio (optimizador)"], ["Instancia ilustrativa y escenarios", "quintana_demo.json (quintana_demo.py)"],
                       ["Curvas $p_i$ y $\\eta_i$", "Cálculo con las ecuaciones del modelo (este documento)"], ["Umbral de enumeración $4\\times10^{5}$", "Código del repositorio"]],
    "ef_vitola.py": [["Evidencia técnica", "resultados_vision.json; salida_pruebas.txt"], ["Población de Montería", "DANE, proyecciones municipales 2020–2035"], ["Tamaño de muestra", "Fórmula normal para dos grupos (este documento)"],
                     ["Latencia parcial", "resultados_vision.json"], ["Referencias", "verificacion_referencias.csv (Crossref y DataCite)"]],
    "ef_pemberty.py": [["62 módulos y 10.581 líneas", "Medición del repositorio, 5 de noviembre de 2026"], ["Ocho baterías sin fallos", "salida_pruebas.txt"], ["Mediciones del reconocedor", "resultados_vision.json"],
                       ["Versiones del entorno", "Registro de la evaluación"], ["Referencias", "verificacion_referencias.csv"]],
    "ef_guerra.py": [["8 % de notas falsas y 30 semillas", "resultados_vision.json"], ["Latencia", "resultados_vision.json"], ["40 ms del optimizador", "salida_pruebas.txt"], ["Dependencia del umbral de confianza", "sensibilidad_umbrales.json"],
                     ["Cifras reportadas", "Documentación y documentos previos del proyecto"], ["Discrepancias", "Revisión del código y la documentación"]],
}
for archivo, filas in BLOQUES.items():
    s = open(archivo, encoding="utf-8").read()
    assert ANCLA in s and "Trazabilidad de las cifras" not in s, archivo
    texto = ('    e.sub("Trazabilidad de las cifras")\n'
             '    e.P("Cada cifra de este trabajo puede rastrearse hasta el script, el archivo o el cálculo que la produce, como se resume en el cuadro siguiente.")\n'
             f'    e.tabla("traza", "Origen de las cifras principales.", ["Cifra", "Origen"], {filas!r}, [3.4, 5.1], size=8)\n\n')
    s = s.replace(ANCLA, texto + ANCLA, 1)
    open(archivo, "w", encoding="utf-8").write(s)
print("ok")
