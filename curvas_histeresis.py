import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image

sns.set_theme(style="darkgrid")

# Rutas relativas al script
base_dir     = Path(__file__).parent
txt_dir      = base_dir / "txt"
png_dir      = base_dir / "png"
results_dir  = base_dir / "Resultados"

results_dir.mkdir(exist_ok=True)  # Crea la carpeta Resultados si no existe

# Etiqueta para extraer el valor variable del nombre del archivo
lbl   = "mp"
s_var = "$mp$"

for archivo in txt_dir.iterdir():
    if archivo.suffix != ".txt":
        continue

    fname = archivo.stem                          # ej: 1PA0.4B6R1mp10
    idx   = fname.find(lbl)

    if idx == -1:
        print(f"⚠️  No se encontró '{lbl}' en {fname}, saltando...")
        continue

    var = fname[idx + len(lbl):]                  # ej: "10"

    # Leer datos
    df = pd.read_table(archivo, sep="\t", header=None)
    df = df.set_axis(["hx", "hy", "mx", "my", "E"], axis=1)

    # Buscar imagen .png correspondiente
    png_path = png_dir / (fname + ".png")

    fig, axes = plt.subplots(2, 1, figsize=(5, 10))

    # Panel inferior: imagen del potencial (si existe)
    if png_path.exists():
        im = Image.open(png_path)
        new_w = int(im.size[0] * 0.7)
        new_h = int(im.size[1] * 0.7)
        im_resized = im.resize((new_w, new_h))
        fig.figimage(im_resized, xo=-25, yo=55)
        axes[1].set_xticks([])
        axes[1].set_yticks([])
    else:
        axes[1].text(0.5, 0.5, "Imagen no encontrada",
                     ha="center", va="center", transform=axes[1].transAxes)
        print(f"⚠️  No se encontró imagen para {fname}")

    # Panel superior: curva de histéresis
    axes[0].plot(df["hy"], df["my"], linestyle="-", alpha=1,
                 label=f"{s_var}={var}")
    axes[0].set_xlabel("$h_y$")
    axes[0].set_ylabel("$M/M_s$")
    axes[0].annotate(text=f"{s_var}={var}", xy=(-4, 0.9))
    axes[0].set_xlim((-4, 4))

    # Guardar en Resultados/
    output = results_dir / f"mp{var}.png"
    plt.savefig(output)
    plt.close(fig)
    print(f"✅ Curva guardada: {output.name}")

plt.close("all")
print("✅ Código finalizado con éxito")