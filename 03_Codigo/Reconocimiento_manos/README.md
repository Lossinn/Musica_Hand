# Reconocimiento_manos

Experimentos aislados de visión por computador **antes** de integrarlos al prototipo
(principio §42: cada componente funciona solo, luego se conecta).

Ideas de scripts:
- `01_camara.py` — abrir cámara con OpenCV y mostrar FPS.
- `02_landmarks.py` — MediaPipe Hands: dibujar los 21 landmarks.
- `03_normalizacion.py` — probar características relativas (invariantes a escala/posición).
- `04_calibracion_auto.py` — prototipo de la rutina de calibración automática (Fase 4).

Lo que funcione se migra a `03_Codigo/Prototipo/{vision,calibration,recognizer}.py`.
