"""Genera entrega_teams/GT_Corte2_Equipo_XX_HandSingKids.zip.

Contiene los tres archivos exigidos (01 documento, 03 póster, 04 modelo financiero; el 02 va insertado en el
documento), más recursos y scripts de regeneración. Excluye los archivos internos del equipo (LEEME, faltantes),
las vistas previas y los temporales.
"""
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "entrega_teams"
z = out / "GT_Corte2_Equipo_XX_HandSingKids.zip"
z.unlink(missing_ok=True)
for p in (root / "_fuentes").glob("parche_*.py"):
    p.unlink()
(root / "_fuentes" / "estudio_pint2.txt").unlink(missing_ok=True)

incluir = [out, root / "recursos", root / "_fuentes"]
excluir = {"_previews", "__pycache__"}
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
    for base in incluir:
        for p in base.rglob("*"):
            if not p.is_file() or p == z or p.name.startswith("~$") or p.suffix == ".zip" or excluir & set(p.parts):
                continue
            f.write(p, p.relative_to(out if base == out else root))
print(round(z.stat().st_size / 1e6, 1), "MB")
