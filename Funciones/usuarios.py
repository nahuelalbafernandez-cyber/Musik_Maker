from Funciones import datos, pantalla


# ==================== USUARIOS ====================
def buscarUsuario(usuarios, nombre_usuario):
    """Devuelve el usuario si existe, o None si no existe."""
    for usuario in usuarios:
        if usuario["usuario"] == nombre_usuario:
            return usuario
    return None


def registro():
    usuarios = datos.leerDatos("usuarios")

    nombre_usuario = pantalla.pedirTexto("Registro", "Elegí un nombre de usuario:")
    if nombre_usuario is None:
        return None

    # Validaciones básicas
    if nombre_usuario == "":
        pantalla.error("El nombre de usuario no puede estar vacío.")
        return None

    if buscarUsuario(usuarios, nombre_usuario) is not None:
        pantalla.error("Ese nombre de usuario ya existe, probá con otro.")
        return None

    contraseña = pantalla.pedirTexto("Registro", "Elegí una contraseña:", oculto=True)
    if contraseña is None:
        return None
    repetir = pantalla.pedirTexto("Registro", "Repetí la contraseña:", oculto=True)
    if repetir is None:
        return None

    if contraseña == "":
        pantalla.error("La contraseña no puede estar vacía.")
        return None

    if contraseña != repetir:
        pantalla.error("Las contraseñas no coinciden.")
        return None

    # Armamos el usuario nuevo y lo agregamos a la lista
    nuevo_usuario = {
        "usuario": nombre_usuario,
        "contraseña": contraseña,
        "bandas_favoritas": []
    }
    usuarios.append(nuevo_usuario)
    datos.guardarDatos("usuarios", usuarios)

    pantalla.avisar("Usuario registrado con éxito.")
    return nombre_usuario


def login():
    usuarios = datos.leerDatos("usuarios")
    intentos = 3

    while intentos > 0:
        nombre_usuario = pantalla.pedirTexto("Iniciar sesión", "Nombre de usuario:")
        if nombre_usuario is None:
            return None
        contraseña = pantalla.pedirTexto("Iniciar sesión", "Contraseña:", oculto=True)
        if contraseña is None:
            return None

        usuario = buscarUsuario(usuarios, nombre_usuario)

        if usuario is not None and usuario["contraseña"] == contraseña:
            pantalla.avisar("¡Bienvenido/a, " + nombre_usuario + "!")
            return nombre_usuario

        intentos = intentos - 1
        if intentos > 0:
            pantalla.error("Usuario o contraseña incorrectos. Te quedan " + str(intentos) + " intentos.")

    pantalla.error("Te quedaste sin intentos.")
    return None
