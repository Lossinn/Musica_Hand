import cv2
import time
import sys
import os

# Agregamos la ruta del proyecto a sys.path para poder importar "src"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.vision import MediaPipeHandDetector
from src.rhythm.detector import ClapDetector


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    hand_detector = MediaPipeHandDetector(
        detection_conf=0.65,
        tracking_conf=0.5
    )

    clap_detector = ClapDetector(
        clap_distance=0.12,
        release_distance=0.18,
        cooldown=0.30
    )

    print("====================================")
    print("      PRUEBA DE DETECCIÓN DE RITMO")
    print("====================================")
    print("Haz un aplauso frente a la cámara.")
    print("Presiona ESC para salir.")
    print("")

    start_time = time.time()

    while True:
        success, frame = camera.read()

        if not success:
            print("❌ No se pudo leer la cámara.")
            break

        frame = cv2.flip(frame, 1)

        # OpenCV entrega BGR.
        # MediaPipe necesita RGB.
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        hands_data, frame_rgb = hand_detector.detect_hands(
            frame_rgb,
            draw_landmarks=True
        )
        current_time = time.time()
        elapsed = current_time - start_time

        clap_detected = clap_detector.update(
            hands_data,
            current_time
        )

        if len(hands_data) != 2:
            if hands_data:
                labels = [hand.get("hand_label", "?") for hand in hands_data]
                print(f"⚠️ {elapsed:.3f}s | manos={len(hands_data)} | labels={labels}")
            else:
                print(f"⚠️ {elapsed:.3f}s - MediaPipe detecta 0 mano(s)")

        # Información de pantalla
        cv2.putText(
            frame_rgb,
            f"Manos detectadas: {len(hands_data)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame_rgb,
            f"Tiempo: {elapsed:.2f}s",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        if clap_detected:
            print(
                f"👏 CLAP detectado en "
                f"{elapsed:.3f} segundos"
            )

            cv2.putText(
                frame_rgb,
                "👏 CLAP!",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 255),
                3
            )

        else:
            cv2.putText(
                frame_rgb,
                "Esperando aplauso...",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        # RGB → BGR para mostrar con OpenCV
        frame_display = cv2.cvtColor(
            frame_rgb,
            cv2.COLOR_RGB2BGR
        )

        cv2.imshow(
            "Hand Sing Kids - Prueba Ritmo",
            frame_display
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()