from Core import funciones as core

def buscarUsuario(datos, nombre_usuario):
    """Devuelve el usuario si existe, o None si no existe."""
    for usuario in datos["usuarios"]:
        if usuario["usuario"] == nombre_usuario:
            return usuario
    return None

def registro():
    datos = core.leerDatos()

    print("\n--- REGISTRO ---")
    nombre_usuario = input("Elegí un nombre de usuario: ").strip()

    # Validaciones básicas
    if nombre_usuario == "":
        print("El nombre de usuario no puede estar vacío.")
        return None

    if buscarUsuario(datos, nombre_usuario) is not None:
        print("Ese nombre de usuario ya existe, probá con otro.")
        return None

    contraseña = input("Elegí una contraseña: ").strip()
    repetir = input("Repetí la contraseña: ").strip()

    if contraseña == "":
        print("La contraseña no puede estar vacía.")
        return None

    if contraseña != repetir:
        print("Las contraseñas no coinciden.")
        return None

    # Armamos el usuario nuevo y lo agregamos a la lista
    nuevo_usuario = {
        "usuario": nombre_usuario,
        "contraseña": contraseña,
        "bandas_favoritas": []
    }
    datos["usuarios"].append(nuevo_usuario)
    core.guardarDatos(datos)

    print("Usuario registrado con éxito.")
    return nombre_usuario

def login():
    datos = core.leerDatos()

    print("\n--- LOGIN ---")
    intentos = 3

    while intentos > 0:
        nombre_usuario = input("Ingresar el nombre de usuario: ").strip()
        contraseña = input("Ingresar contraseña: ").strip()

        usuario = buscarUsuario(datos, nombre_usuario)

        if usuario is not None and usuario["contraseña"] == contraseña:
            print("Bienvenido/a, " + nombre_usuario + "!")
            return nombre_usuario

        intentos = intentos - 1
        print("Usuario o contraseña incorrectos. Te quedan " + str(intentos) + " intentos.")

    print("Te quedaste sin intentos.")
    return None