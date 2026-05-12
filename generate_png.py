import os
from pathlib import Path
from PIL import Image
# Ajusta el número de versión según el que instalaste
os.environ["PATH"] += r";C:\Program Files\gs\gs10.07.0\bin"

# Rutas relativas al script
base_dir = Path(__file__).parent
eps_dir  = base_dir / "eps"
png_dir  = base_dir / "png"

png_dir.mkdir(exist_ok=True)  # Crea la carpeta png si no existe

print(f"Convirtiendo archivos en: {eps_dir}")

for file in eps_dir.iterdir():
    if file.suffix == ".eps":
        output = png_dir / (file.stem + ".png")
        print(f"Convirtiendo {file.name}  →  {output.name}")
        with Image.open(file) as img:
            img = img.convert("RGB")
            img.save(output, "PNG")

print("✅ Conversión finalizada con éxito")