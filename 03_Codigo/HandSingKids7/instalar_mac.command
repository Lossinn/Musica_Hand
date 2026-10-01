#!/bin/bash
# Instalador de Hand Sing Kids para macOS.
# Crea un entorno aislado en .venv e instala las dependencias.

cd "$(dirname "$0")" || exit 1

VERDE='\033[0;32m'; ROJO='\033[0;31m'; AMAR='\033[1;33m'; FIN='\033[0m'
echo ""
echo "🎵  Hand Sing Kids — instalación"
echo "───────────────────────────────────────────────"

# --- 1. Buscar un Python compatible -----------------------------------------
# MediaPipe no publica todavía para 3.13, y PySide6 pide 3.10 o superior.
PY=""
for cand in python3.12 python3.11 python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
        V=$("$cand" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
        MAJ=${V%%.*}; MIN=${V##*.}
        if [ "$MAJ" = "3" ] && [ "$MIN" -ge 10 ] && [ "$MIN" -le 12 ] 2>/dev/null; then
            PY="$cand"; break
        fi
    fi
done

if [ -z "$PY" ]; then
    printf "${ROJO}No encontré Python 3.10, 3.11 o 3.12 en este equipo.${FIN}\n"
    echo ""
    echo "Comprueba qué versión tienes con:"
    echo "    python3 --version"
    echo ""
    echo "Si es 3.13 o más nueva, MediaPipe todavía no la soporta. Instala una"
    echo "compatible con Homebrew:"
    echo "    brew install python@3.12"
    echo ""
    read -n 1 -s -r -p "Pulsa una tecla para cerrar."
    exit 1
fi

printf "Python encontrado: ${VERDE}%s${FIN}  (%s)\n" "$($PY --version 2>&1)" "$(command -v $PY)"
echo "Procesador: $(uname -m)"

# --- 2. Entorno aislado ------------------------------------------------------
if [ ! -d ".venv" ]; then
    echo "Creando el entorno aislado…"
    "$PY" -m venv .venv || {
        printf "${ROJO}No se pudo crear el entorno.${FIN}\n"
        read -n 1 -s -r -p "Pulsa una tecla para cerrar."
        exit 1
    }
fi

source .venv/bin/activate
python -m pip install --upgrade pip --quiet

echo "Instalando dependencias (la primera vez puede tardar varios minutos)…"
if ! python -m pip install -r requirements.txt; then
    echo ""
    printf "${ROJO}La instalación falló.${FIN}\n"
    echo "Si el error menciona 'mediapipe', revisa que la versión de Python sea"
    echo "3.10, 3.11 o 3.12 y que haya conexión a internet."
    read -n 1 -s -r -p "Pulsa una tecla para cerrar."
    exit 1
fi

# --- 3. Comprobación ---------------------------------------------------------
echo ""
echo "Comprobando la instalación…"
python - <<'PYCHECK'
import sys
fallos = []
for mod in ("PySide6", "cv2", "mediapipe", "numpy", "pulp"):
    try:
        m = __import__(mod)
        print(f"   ok   {mod} {getattr(m, '__version__', '?')}")
    except Exception as exc:
        fallos.append(f"{mod}: {exc}")
if fallos:
    print("\n   Problemas:")
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
PYCHECK

if [ $? -ne 0 ]; then
    printf "${ROJO}Alguna dependencia no quedó bien instalada.${FIN}\n"
    read -n 1 -s -r -p "Pulsa una tecla para cerrar."
    exit 1
fi

chmod +x iniciar_mac.command 2>/dev/null

echo ""
printf "${VERDE}✅  Todo listo.${FIN}\n"
echo ""
printf "${AMAR}Dos cosas sobre la cámara en macOS:${FIN}\n"
echo "  1. La primera vez, el sistema pedirá permiso de cámara para Terminal."
echo "     Hay que aceptarlo."
echo "  2. Si no aparece el aviso, entra en Ajustes del Sistema →"
echo "     Privacidad y seguridad → Cámara, y activa Terminal."
echo ""
echo "Para abrir la aplicación, haz doble clic en:  iniciar_mac.command"
echo ""
read -n 1 -s -r -p "Pulsa una tecla para cerrar."
