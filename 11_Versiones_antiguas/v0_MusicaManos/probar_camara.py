import cv2

def encontrar_camaras():
    """
    Revisa los puertos de cámara uno por uno y muestra la imagen de las que encuentra.
    """
    print("Buscando cámaras conectadas...")
    print("Presiona 'N' para probar el siguiente puerto.")
    print("Presiona 'Q' para salir.")

    index = 0
    while index < 10:  # Prueba los primeros 10 puertos, que es más que suficiente
        cap = cv2.VideoCapture(index)

        if cap.isOpened():
            print(f"✅ ¡Cámara encontrada en el puerto {index}!")

            # Muestra la imagen de la cámara encontrada
            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"❌ No se pudo leer el frame de la cámara en el puerto {index}.")
                    break

                # Muestra el número de puerto en la ventana
                cv2.putText(frame, f"Puerto: {index}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Presiona 'N' para siguiente, 'Q' para salir", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.imshow('Probador de Camaras', frame)

                # Espera a que el usuario presione una tecla
                key = cv2.waitKey(1) & 0xFF
                if key == ord('n'): # 'n' para la siguiente
                    break 
                if key == ord('q'): # 'q' para salir
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Saliendo del probador.")
                    return

            cap.release()
        else:
            print(f"-- No se encontró cámara en el puerto {index}.")

        index += 1

    cv2.destroyAllWindows()
    print("\nBúsqueda finalizada.")

if __name__ == "__main__":
    encontrar_camaras()