from Funciones import datos, pantalla, auxiliares, usuarios as modulo_usuarios, bandas as modulo_bandas

# ==================== FAVORITAS ====================
# Cada usuario guarda en "bandas_favoritas" los id de sus bandas.
# Estas funciones reciben el nombre del usuario que inició sesión.

def bandasFavoritas(usuario, bandas):
    """Devuelve la lista de bandas que ese usuario tiene como favoritas."""
    favoritas = []
    for banda_id in usuario["bandas_favoritas"]:
        banda = auxiliares.buscarPorId(bandas, banda_id)
        if banda is not None:
            favoritas.append(banda)
    return favoritas

def mostrarFavoritas(nombre_usuario):
    usuarios = datos.leerDatos("usuarios")
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")
    generos = datos.leerDatos("generos")

    usuario = modulo_usuarios.buscarUsuario(usuarios, nombre_usuario)
    favoritas = bandasFavoritas(usuario, bandas)

    if len(favoritas) == 0:
        pantalla.avisar("Todavía no tenés bandas favoritas.")
        return

    lineas = []
    for banda in favoritas:
        lineas.append(modulo_bandas.textoBanda(banda, paises, generos))
    pantalla.mostrarLista("Mis favoritas", lineas)

def agregarFavorita(nombre_usuario):
    usuarios = datos.leerDatos("usuarios")
    bandas = datos.leerDatos("bandas")

    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    usuario = modulo_usuarios.buscarUsuario(usuarios, nombre_usuario)

    # Solo ofrecemos las bandas que todavía no son favoritas
    disponibles = []
    for banda in bandas:
        if banda["id"] not in usuario["bandas_favoritas"]:
            disponibles.append(banda)

    if len(disponibles) == 0:
        pantalla.avisar("Ya tenés todas las bandas en favoritas.")
        return

    banda = auxiliares.elegirElemento(disponibles, "¿Qué banda querés agregar a favoritas?")
    if banda is None:
        return

    usuario["bandas_favoritas"].append(banda["id"])
    datos.guardarDatos("usuarios", usuarios)
    pantalla.avisar(banda["nombre"] + " se agregó a tus favoritas.")

def quitarFavorita(nombre_usuario):
    usuarios = datos.leerDatos("usuarios")
    bandas = datos.leerDatos("bandas")

    usuario = modulo_usuarios.buscarUsuario(usuarios, nombre_usuario)
    favoritas = bandasFavoritas(usuario, bandas)

    if len(favoritas) == 0:
        pantalla.avisar("Todavía no tenés bandas favoritas.")
        return

    banda = auxiliares.elegirElemento(favoritas, "¿Qué banda querés quitar de favoritas?")
    if banda is None:
        return

    usuario["bandas_favoritas"].remove(banda["id"])
    datos.guardarDatos("usuarios", usuarios)
    pantalla.avisar(banda["nombre"] + " se quitó de tus favoritas.")