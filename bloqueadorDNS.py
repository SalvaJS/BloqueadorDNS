import os
import ctypes
import sys

# Comprobar si la aplicación se ha abierto con permisos de administrador.
try:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
except:
    is_admin = False
if not is_admin:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

ficheroHost = os.path.join(os.environ['SystemRoot'], 'System32/drivers/etc', 'hosts')
ficheroHostRollBack = os.path.join(os.environ['SystemRoot'], 'System32/drivers/etc', 'hosts.rollback')

def copiaRollBack():
    with open(ficheroHost, 'r') as hosts:
        contenidoHosts = hosts.read()
    with open(ficheroHostRollBack, 'w') as hostsRollBack:
        hostsRollBack.write(contenidoHosts)

print("---------- Bienvenido al programa para bloquear o desbloquear nombres de dominio ----------")
print()
while(True):
    print("---------------------------------------------------------------")
    print("Escribe uno de los siguientes números para realizar una acción:")
    print(" 1)   Mostrar los DNS bloqueados.")
    print(" 2)   Bloquear DNS.")
    print(" 3)   Desbloquear DNS.")
    opcion = input("Ingresar valor: ")

    if opcion == '1':
        print()
        print("Lista de DNS bloqueados:")
        with open(ficheroHost, 'r') as hosts:
            contenido = ""
            linea = hosts.readline()
            while linea:
                linea = linea.split()
                if len(linea) > 0 and linea[0] == '127.0.0.1':
                    contenido += f'- {linea[1]}\n' 
                linea = hosts.readline()
            print(contenido)
        print()
        input("Pulsa enter para volver al menú.")
    elif opcion == '2':
        print()
        print("Escribe los nombres de dominio que desea bloquear. Si quiere añadir varios a las lista, puede escribirlos separadas por espacio o uno a uno. Para volver al menú escribe 'salir'.")
        entrada = input()
        copiaRollBack()
        while 'salir' not in entrada.lower():
            entrada = entrada.split()
            with open(ficheroHost, 'a') as hosts:
                for dns in entrada:
                    hosts.write(f'\n127.0.0.1 {dns}')
            print("Se han bloqueado los DNS correctamente. Puede añadir más o escribir 'salir' para volver al menú:")
            entrada = input()
    elif opcion == '3':
        print()
        print("Escribe los nombres de dominio que desea desbloquear. Si quiere eliminar varios de la lista, puede escribirlos separadas por espacio o uno a uno. Para volver al menú escribe 'salir'.")
        entrada = input()
        copiaRollBack()
        while 'salir' not in entrada.lower():
            entrada = entrada.split()
            esta = False
            for dns in entrada:
                with open(ficheroHost, 'r') as hosts:
                    contenidoHosts = hosts.readlines()
                with open(ficheroHost, 'w') as hosts:
                    for linea in contenidoHosts:
                        lineaList = linea.split()
                        if len(lineaList) >= 2 and lineaList[1] == dns:
                            esta = True
                        else:
                            hosts.write(linea)
            if esta == False:
                print(f"El DNS {dns} no se encuentra en la lista. Puede añadir más o escribir 'salir' para volver al menú:")
            else:
                print("Se han eliminado de la lista los DNS correctamente. Puede añadir más o escribir 'salir' para volver al menú:")
            entrada = input()
                


