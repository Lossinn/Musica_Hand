"""Ensambla el ZIP del curso. Uso: python -X utf8 empaquetar.py [NN]   (por defecto 'NN')
Copia los archivos con nombres canónicos. Si existen los reales (Preprint, Turnitin, Constancia) en entrega_final/,
los usa; si no, incluye el marcador PENDIENTE con el nombre exacto."""
import shutil, sys, zipfile
from pathlib import Path
NN = sys.argv[1] if len(sys.argv) > 1 else "NN"
VER = sys.argv[2] if len(sys.argv) > 2 else ""   # versión: Pemberty / Carrascal
B = Path(__file__).resolve().parents[1]
out = B / ("entrega_final" + ("_" + VER if VER else "")); out.mkdir(exist_ok=True)
fuentes = {
    f"Preprint_Manuscrito_Equipo{NN}.pdf": B / "soporte/PENDIENTE_Preprint_Manuscrito_EquipoNN.pdf",
    f"Certificado_Turnitin_Equipo{NN}.pdf": B / "soporte/PENDIENTE_Certificado_Turnitin_EquipoNN.pdf",
    f"Ficha_Revista_Indexada_Equipo{NN}.pdf": B / "soporte/Ficha_Revista_Indexada_EquipoNN.pdf",
    f"Articulo_Maquetado_Equipo{NN}.pdf": B / f"articulo/Articulo_Maquetado_EquipoNN{'_' + VER if VER else ''}.pdf",
    f"Constancia_Envio_Revista_Equipo{NN}.pdf": B / "soporte/PENDIENTE_Constancia_Envio_Revista_EquipoNN.pdf",
}
zpath = out / f"02_GT_Corte3_CierreProyecto_Equipo{NN}.zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for nombre, src in fuentes.items():
        real = out / "reales" / nombre
        z.write(real if real.exists() else src, nombre)
print("ZIP:", zpath); print([i.filename for i in zipfile.ZipFile(zpath).infolist()])
