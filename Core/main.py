# Ejecutar desde la carpeta raíz del proyecto con:  python -m Core.main

from Core import funciones as core
from Registration import funciones as registration
from ABMs import funciones as abms
from Reportes import funciones as reportes


def menuInicio():
    while True:
        print("\n===== MUSIK MAKER =====")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            usuario = registration.login()
            if usuario is not None:
                menuUsuario(usuario)
        elif opcion == "2":
            registration.registro()
        elif opcion == "3":
            print("Chau!")
            break
        else:
            print("Opción inválida.")


def menuUsuario(usuario):
    while True:
        print("\n--- Menú de " + usuario + " ---")
        print("1. Buscar banda")
        print("2. Ver todas las bandas")
        print("3. Agregar banda")
        print("4. Editar banda")
        print("5. Eliminar banda")
        print("6. Reporte: bandas por país")
        print("7. Cerrar sesión")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            core.buscarBanda()
        elif opcion == "2":
            core.mostrarBandas()
        elif opcion == "3":
            abms.agregarBanda()
        elif opcion == "4":
            abms.editarBanda()
        elif opcion == "5":
            abms.eliminarBanda()
        elif opcion == "6":
            reportes.reporteBandasPorPais()
        elif opcion == "7":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")


menuInicio()