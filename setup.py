import shutil
import subprocess
import sys
import os
import pkg_resources

def instalarPaquete(paquete):
    try:
        pkg_resources.get_distribution("PyInstaller")
        print(f"El paquete '{paquete}' ya está instalado.")
    except pkg_resources.DistributionNotFound:
        print(f"Instalando '{paquete}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

instalarPaquete("pyinstaller")

if not os.path.exists("./Ejecutable"):
    os.mkdir("./Ejecutable")

try:
    print("Instalando la aplicación...")
    subprocess.check_call(["pyinstaller", "--clean", "--onefile", "--distpath", "./Ejecutable", "bloqueadorDNS.py"])
    shutil.rmtree("./build")
    os.remove("./bloqueadorDNS.spec")
    print("Se ha generado el ejecutable correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar PyInstaller: {e}")

input("Pulsa enter para salir.")