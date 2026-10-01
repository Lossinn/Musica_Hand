"""Genera el QR del póster. Uso: python generar_qr.py [URL]  (por defecto, el repositorio del proyecto)."""
import sys
from pathlib import Path
import segno
URL = sys.argv[1] if len(sys.argv) > 1 else "https://github.com/Lossinn/Musica_Hand"
out = Path(__file__).resolve().parents[1] / "recursos" / "assets"
qr = segno.make(URL, error="m", micro=False)
qr.save(out / "qr_repositorio.svg", scale=10, dark="#141414", light="#ffffff", border=2)
qr.save(out / "qr_repositorio.png", scale=12, dark="#141414", light="#ffffff", border=2)
# verificación: decodificar el PNG con OpenCV
import cv2
img = cv2.imread(str(out / "qr_repositorio.png"))
val, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
print("URL codificada:", URL); print("decodificada  :", val, "->", "CORRECTO" if val == URL else "ERROR")
