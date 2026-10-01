#!/usr/bin/env python3
"""Diagnóstico de la cámara.

Si Hand Sing Kids no ve la cámara, este script dice por qué sin abrir la
aplicación completa: qué puertos responden, si MediaPipe detecta manos y a qué
velocidad va el equipo.

    python probar_camara.py

Pulsa Q en la ventana para salir, N para probar el siguiente puerto.
"""

from __future__ import annotations

import os
import sys
import time

os.environ.setdefault("GLOG_minloglevel", "2")


def buscar_puertos(cv2, maximo: int = 5) -> list[int]:
    disponibles = []
    print("Buscando cámaras…")
    for i in range(maximo):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ok, frame = cap.read()
            if ok and frame is not None:
                alto, ancho = frame.shape[:2]
                print(f"  ✅ puerto {i}: {ancho}x{alto}")
                disponibles.append(i)
            else:
                print(f"  ⚠️  puerto {i}: abre pero no entrega imagen")
            cap.release()
        else:
            print(f"  —  puerto {i}: sin cámara")
    return disponibles


def main() -> int:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        print(f"Falta una dependencia: {exc}")
        print("Ejecuta primero:  pip install -r requirements.txt")
        return 1

    print("")
    print("🎥  Diagnóstico de cámara — Hand Sing Kids")
    print("──────────────────────────────────────────")
    if sys.platform == "darwin":
        print("En macOS, el permiso de cámara se concede a Terminal:")
        print("Ajustes del Sistema → Privacidad y seguridad → Cámara.")
        print("")

    puertos = buscar_puertos(cv2)
    if not puertos:
        print("")
        print("No se encontró ninguna cámara utilizable.")
        print("Revisa que ninguna otra aplicación la esté usando (Zoom, Meet,")
        print("Photo Booth) y que el permiso esté concedido.")
        return 1

    try:
        from handsingkids.vision.detector import HandDetector
        detector = HandDetector()
        print("\nDetector de manos listo.")
    except Exception as exc:
        print(f"\nNo se pudo cargar MediaPipe: {exc}")
        detector = None

    indice = 0
    while indice < len(puertos):
        puerto = puertos[indice]
        cap = cv2.VideoCapture(puerto)
        print(f"\nMostrando el puerto {puerto}.  Q = salir   N = siguiente")
        marca, cuadros, fps = time.time(), 0, 0.0

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            cuadros += 1
            if time.time() - marca >= 1.0:
                fps = cuadros / (time.time() - marca)
                marca, cuadros = time.time(), 0

            manos = []
            if detector is not None:
                pequeno = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                                     (480, 270))
                manos = detector.detect(np.ascontiguousarray(pequeno))
                alto, ancho = frame.shape[:2]
                for mano in manos:
                    color = (60, 200, 120) if mano["hand_label"] == "Left" \
                        else (60, 200, 255)
                    for punto in mano["landmarks"]:
                        cv2.circle(frame,
                                   (int(punto[0] * ancho), int(punto[1] * alto)),
                                   4, color, -1)

            texto = f"Puerto {puerto}   {fps:.0f} fps   manos: {len(manos)}"
            cv2.putText(frame, texto, (12, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 0), 4)
            cv2.putText(frame, texto, (12, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), 2)
            cv2.imshow("Diagnostico Hand Sing Kids", frame)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                if detector:
                    detector.close()
                print("\nFin del diagnóstico.")
                return 0
            if tecla == ord("n"):
                break

        cap.release()
        indice += 1

    cv2.destroyAllWindows()
    if detector:
        detector.close()
    print("\nSe probaron todos los puertos disponibles.")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
