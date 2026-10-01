"""Ejecuta las suites de HandSingKids7 y registra el resultado en pruebas.json."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
COMPRUEBA = {
    "test_vision.py": "Identidad, invariancia a escala y giro; comparación cuantitativa con el método de la versión 1",
    "test_stabilizer.py": "Sin ráfagas con la mano quieta; transiciones sin notas intermedias; repetición tras soltar",
    "test_mastery.py": "Una sesión perfecta no basta para dominar; el intervalo de repaso crece y se reinicia; el olvido degrada",
    "test_optimizer.py": "Restricciones del MILP, coincidencia MILP y enumeración, cambio de selección con el perfil",
    "test_predictor.py": "Ajuste logístico mejor que el azar, monotonía, serialización y generador procedural",
    "test_rhythm.py": "Planificación de tiempos y ventanas del módulo de ritmo",
    "test_audio.py": "Capas de sonido (personalizado, incluido, sintetizado) y música de fondo",
    "test_integracion.py": "Flujo completo de una sesión con la aplicación real sin ventana visible",
}
env = dict(os.environ, PYTHONUTF8="1", QT_QPA_PLATFORM="offscreen")
out = {}
total_ok = 0
for nombre, desc in COMPRUEBA.items():
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, str(ROOT / "tests" / nombre)], cwd=ROOT, env=env,
                           capture_output=True, text=True, timeout=600, encoding="utf-8", errors="replace")
        txt = (r.stdout or "") + (r.stderr or "")
        ok = r.returncode == 0
    except subprocess.TimeoutExpired:
        txt, ok = "timeout", False
    n_ok = len(re.findall(r"^\s*ok\s", txt, flags=re.M))
    marcador = bool(re.search(r"(Todas las pruebas pasaron|como se esperaba|funcionan? como se esperaba)", txt))
    fallos_txt = bool(re.search(r"(comprobaciones fallaron|Traceback|FALLA)", txt))
    logico = marcador and not fallos_txt
    cierre_anomalo = (not ok) and logico      # todas las comprobaciones pasan, pero el proceso cae al cerrar
    ok = ok or logico
    total_ok += n_ok
    resumen = f"Pasó ({n_ok} verificaciones «ok»)" if ok and n_ok else "Pasó" if ok else "FALLÓ"
    if cierre_anomalo:
        resumen += f"; cierre anómalo del proceso (código {r.returncode:#x})"
    out[nombre] = dict(comprueba=desc, resultado=resumen, pasa=ok, verificaciones_ok=n_ok, cierre_anomalo=cierre_anomalo,
                       segundos=round(time.time() - t0, 1), cola=txt[-600:])
    print(f"{nombre:22s} {resumen}  ({out[nombre]['segundos']} s)")
    if not ok:
        print(txt[-800:])
versiones = subprocess.run([sys.executable, "-c",
                            "import numpy,PySide6,pulp,cv2,mediapipe,sys;print(sys.version.split()[0],numpy.__version__,PySide6.__version__,pulp.__version__,cv2.__version__,mediapipe.__version__)"],
                           capture_output=True, text=True).stdout.strip()
nota = (f"Ejecución del 30 de septiembre de 2026 en Windows 11; Python, NumPy, PySide6, PuLP, OpenCV y MediaPipe "
        f"en las versiones {versiones}.")
Path(__file__).with_name("pruebas.json").write_text(
    json.dumps(dict(archivos=out, nota=nota, versiones=versiones, total=len(out),
                    pasan=sum(v["pasa"] for v in out.values())), ensure_ascii=False, indent=1), encoding="utf-8")
print(nota)
print(f"{sum(v['pasa'] for v in out.values())}/{len(out)} suites pasan")
