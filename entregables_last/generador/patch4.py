def sub(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (path, a[:70])
        s = s.replace(a, b, 1)
    open(path, "w", encoding="utf-8").write(s)


T = "Cada cifra de este trabajo puede rastrearse hasta el script, el archivo o el cálculo que la produce, como se resume en el cuadro siguiente."
nuevos = {
    "petro": "Cada cifra puede rastrearse hasta el archivo y el script que la generan, según el cuadro siguiente.",
    "negrete": "El origen de cada cifra se resume a continuación: o es un archivo de resultados o es un cálculo con las ecuaciones del código.",
    "carrascal": "Se indica a continuación de dónde sale cada cifra, sea un archivo del repositorio o un cálculo con las ecuaciones del modelo.",
    "quintana": "El cuadro siguiente indica el archivo, el script o el cálculo del que sale cada cifra.",
    "vitola": "Para que quien lea pueda comprobar los números, el cuadro siguiente remite cada cifra a su fuente.",
    "pemberty": "La trazabilidad de las cifras se resume así: cada una remite a un script, un archivo o un cálculo.",
    "guerra": "Aplicando la regla propuesta, cada cifra remite a su origen en el cuadro siguiente.",
}
for k, v in nuevos.items():
    sub(f"ef_{k}.py", [(T, v)])
sub("ef_petro.py", [("Las mediciones se hicieron en un solo equipo con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21. No se registraron las características del procesador ni de la memoria.",
                     "El entorno fue un único equipo con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21; no quedó registrado el procesador ni la memoria.")])
sub("ef_guerra.py", [("Las mediciones se hicieron en un **un solo equipo** con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21; no se registraron las características del procesador."
                      if False else "Las mediciones se hicieron en **un solo equipo** con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21; no se registraron las características del procesador.",
                      "Todo se midió en **un equipo** con Windows 11 y Python 3.12.10 (NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21), sin registro de su procesador.")])
sub("ef_pemberty.py", [("Las mediciones se hicieron en **un solo equipo** con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0; **no** se evaluó macOS ni otras versiones de Python.",
                        "El entorno fue **un solo equipo** con Windows 11 y estas versiones: Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0. **No** se evaluó macOS ni otras versiones de Python.")])
print("ok")
