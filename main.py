from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.append(str(SRC))

from ui.ventana_principal import lanzar_aplicacion


if __name__ == "__main__":
    lanzar_aplicacion()