from pathlib import Path
import subprocess
import sys
from datetime import datetime

archivo_valores = Path("valores.txt")
archivo_entrada = Path("input.txt")
archivo_resultados = Path("resultados.txt")
archivo_edp = Path("Flower.edp")

def leer_valores():
    with open(archivo_valores, "r") as f:
        return [line.strip() for line in f if line.strip()]

def escribir(valor):
    with open(archivo_entrada, "w") as f:
        f.write(f"{valor}\n")

def correr_edp():
    """Corre FreeFem++ y muestra la salida en tiempo real."""
    proceso = subprocess.Popen(
        ["FreeFem++", "-nw", str(archivo_edp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Mezcla stderr con stdout
        text=True,
        bufsize=1  # Line-buffered
    )

    salida_completa = []

    for linea in proceso.stdout:
        linea = linea.rstrip()
        print(f"  [FF++] {linea}")       # Muestra en consola en tiempo real
        sys.stdout.flush()
        salida_completa.append(linea)

    proceso.wait()

    if proceso.returncode != 0:
        print(f"  ⚠️  FreeFem++ terminó con error (código {proceso.returncode})")

    return "\n".join(salida_completa)

def guardar_resultado(valor, salida):
    with open(archivo_resultados, "a") as f:
        f.write(f"a0 = {valor}\n")
        f.write(salida)
        f.write("\n" + "-"*40 + "\n")

def main():
    valores = leer_valores()
    total = len(valores)
    print(f"📋 Se procesarán {total} valor(es): {valores}\n")

    for idx, valor in enumerate(valores, start=1):
        print(f"{'='*50}")
        print(f"▶ [{idx}/{total}] Procesando mp = {valor}  |  {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")

        escribir(valor)
        salida = correr_edp()
        guardar_resultado(valor, salida)

        print(f"✅ Valor {valor} completado.\n")

    print("🎉 Todos los valores fueron procesados.")

if __name__ == "__main__":
    main()