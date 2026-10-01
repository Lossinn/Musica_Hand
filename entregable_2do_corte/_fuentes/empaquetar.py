"""Genera entrega_teams/GT_Corte2_Equipo_XX_HandSingKids.zip con los archivos que pide la instrucción.

01 documento, 03 póster y 04 modelo financiero. El 02 (BPMN, DFD y gobernanza) va insertado en el documento,
como permite la instrucción. Los recursos y los scripts de regeneración quedan en el repositorio, no en el .zip.
"""
import zipfile
from pathlib import Path

out = Path(__file__).resolve().parents[1] / "entrega_teams"
z = out / "GT_Corte2_Equipo_XX_HandSingKids.zip"
z.unlink(missing_ok=True)
archivos = ["01_Documento_EBT_GestionTecnologica_Equipo_XX.pdf", "03_Poster_Cientifico_90x120_Equipo_XX.pdf",
            "04_Modelo_Financiero_ROI_Equipo_XX.xlsx"]
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
    for a in archivos:
        f.write(out / a, a)
print(round(z.stat().st_size / 1e6, 1), "MB:", ", ".join(archivos))
