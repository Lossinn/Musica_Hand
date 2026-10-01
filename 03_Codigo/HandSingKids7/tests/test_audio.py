"""Pruebas de las tres capas de sonido (personalizado > incluido con la app >
sintetizado) y de que la música de fondo se apague exactamente en las
pantallas con cámara activa.

Esto corrige la petición del usuario tras entregar sus propias grabaciones de
las ocho notas y sus ilustraciones de gestos: que el sonido de cada nota use
esas grabaciones, y que la música de fondo (todavía pendiente de recibir el
archivo) quede confinada a las pantallas principales, nunca a un modo de
juego con la cámara encendida.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DATOS = Path("/tmp/hsk_test_audio")

fallos: list[str] = []


def comprobar(condicion: bool, mensaje: str) -> None:
    if condicion:
        print(f"  ok   {mensaje}")
    else:
        fallos.append(mensaje)
        print(f"  FALLA {mensaje}")


def test_capas_de_sonido() -> None:
    print("\n1. Prioridad entre sonido personalizado, incluido y sintetizado")
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    if DATOS.exists():
        shutil.rmtree(DATOS)
    from handsingkids.core import config
    config.set_data_dir(DATOS)

    from handsingkids.core.config import AudioSettings, bundled_audio_dir
    from handsingkids.music.audio import AudioEngine

    incluida = bundled_audio_dir()
    comprobar(incluida.is_dir(), "la carpeta de sonidos incluidos existe en el paquete")
    for code in ("DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4"):
        comprobar((incluida / f"nota_{code}.wav").exists(),
                  f"hay una grabación real incluida para {code}")

    ae = AudioEngine(AudioSettings())
    for code in ("DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4"):
        ruta = ae._files.get(f"nota_{code}")
        comprobar(ruta is not None and ruta.parent == incluida,
                  f"nota_{code} usa la grabación incluida, no la sintetizada")
    comprobar(ae._files.get("acierto") is not None and
             "sonidos_personalizados" not in str(ae._files["acierto"]) and
             str(ae._files["acierto"]).endswith(".wav"),
              "un efecto sin grabación incluida (acierto) sigue usando el sintetizado")
    comprobar("musica_fondo" not in ae._files,
              "sin archivo incluido ni personalizado, 'musica_fondo' no está "
              "registrada (play_music() sobre ella no hace nada, no falla)")
    ae.play_music("musica_fondo")   # no debe lanzar excepción aunque no exista
    comprobar(ae._music_fx is None,
              "pedir una música de fondo que no existe no reproduce nada")

    # Una familia deja su propia grabación de una nota: debe ganarle a la
    # incluida con la app.
    from handsingkids.core.config import custom_audio_dir
    propio = custom_audio_dir() / "nota_DO3.wav"
    shutil.copy(incluida / "nota_DO3.wav", propio)
    ae2 = AudioEngine(AudioSettings())
    comprobar(ae2._files.get("nota_DO3") == propio,
              "un sonido personalizado de la familia gana a la grabación incluida")


def test_musica_de_fondo_fuera_del_juego() -> None:
    print("\n2. La música de fondo se apaga en las pantallas con cámara activa")
    from handsingkids.app import PANTALLAS_SIN_MUSICA_DE_FONDO, MainWindow

    for pantalla in ("calibration", "exercise", "freeplay", "rhythm"):
        comprobar(pantalla in PANTALLAS_SIN_MUSICA_DE_FONDO,
                  f"'{pantalla}' es un modo de juego con cámara: sin música de fondo")
    for pantalla in ("home", "adventure", "songs", "progress", "parents",
                     "settings", "results", "profiles", "create_profile"):
        comprobar(pantalla not in PANTALLAS_SIN_MUSICA_DE_FONDO,
                  f"'{pantalla}' es una pantalla principal: sí lleva música de fondo")

    class AudioFalso:
        def __init__(self) -> None:
            self.llamadas: list[str] = []

        def play_music(self, name: str) -> None:
            self.llamadas.append(f"play:{name}")

        def stop_music(self) -> None:
            self.llamadas.append("stop")

    class ContextoFalso:
        def __init__(self) -> None:
            self.audio = AudioFalso()

    class VentanaFalsa:
        def __init__(self) -> None:
            self.ctx = ContextoFalso()

    ventana = VentanaFalsa()
    MainWindow._actualizar_musica_de_fondo(ventana, "splash")
    comprobar(ventana.ctx.audio.llamadas == [],
              "la pantalla de bienvenida administra su propia música: no se toca aquí")

    MainWindow._actualizar_musica_de_fondo(ventana, "home")
    MainWindow._actualizar_musica_de_fondo(ventana, "exercise")
    MainWindow._actualizar_musica_de_fondo(ventana, "results")
    comprobar(ventana.ctx.audio.llamadas ==
             ["play:musica_fondo", "stop", "play:musica_fondo"],
              "prende en pantallas principales, apaga al entrar a jugar, "
              f"vuelve a prender al salir ({ventana.ctx.audio.llamadas})")


def main() -> int:
    test_capas_de_sonido()
    test_musica_de_fondo_fuera_del_juego()
    print()
    if fallos:
        print(f"{len(fallos)} comprobaciones fallaron:")
        for f in fallos:
            print("  ·", f)
        return 1
    print("Las tres capas de sonido y la música de fondo fuera del juego "
         "funcionan como se esperaba.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
