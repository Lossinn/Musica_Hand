#!/bin/bash
# Arranque de Hand Sing Kids.

cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
    echo "Todavía no está instalado."
    echo "Haz doble clic primero en:  instalar_mac.command"
    read -n 1 -s -r -p "Pulsa una tecla para cerrar."
    exit 1
fi

source .venv/bin/activate
echo "🎵  Abriendo Hand Sing Kids…"
python main.py
CODIGO=$?

if [ $CODIGO -ne 0 ]; then
    echo ""
    echo "La aplicación se cerró con un error (código $CODIGO)."
    echo "Si el problema es la cámara, revisa Ajustes del Sistema →"
    echo "Privacidad y seguridad → Cámara, y activa Terminal."
    read -n 1 -s -r -p "Pulsa una tecla para cerrar."
fi
