from Funciones import datos, pantalla, auxiliares


# ==================== MOSTRAR Y BUSCAR ====================
def textoBanda(banda, paises):
    """Arma el texto para mostrar una banda, ej: "The Beatles (Reino Unido)"."""
    pais = auxiliares.buscarPorId(paises, banda["pais_id"])
    nombre_pais = "sin país"
    if pais is not None:
        nombre_pais = pais["nombre"]
    return banda["nombre"] + " (" + nombre_pais + ")"


def mostrarBandas():
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")

    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    lineas = []
    for banda in bandas:
        lineas.append(textoBanda(banda, paises))
    pantalla.mostrarLista("Todas las bandas", lineas)


def buscarBanda():
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")

    texto = pantalla.pedirTexto("Buscar banda", "¿Qué banda buscás?")
    if texto is None:
        return
    if texto == "":
        pantalla.error("No escribiste nada.")
        return

    resultados = auxiliares.buscarPorNombre(bandas, texto)

    if len(resultados) == 0:
        pantalla.error("No se encontró ninguna banda.")
        return

    lineas = []
    for banda in resultados:
        lineas.append(textoBanda(banda, paises))
    pantalla.mostrarLista("Resultados de la búsqueda", lineas)


def pedirPais():
    """Pide un país por nombre y devuelve su id, o None si no se eligió ninguno."""
    paises = datos.leerDatos("paises")
    pais = auxiliares.elegirPorNombre(paises, "País", "¿De qué país es la banda?")
    if pais is None:
        return None
    return pais["id"]


# ==================== ABM BANDAS ====================
def agregarBanda():
    bandas = datos.leerDatos("bandas")

    nombre = pantalla.pedirTexto("Agregar banda", "Nombre de la banda:")
    if nombre is None:
        return
    if nombre == "":
        pantalla.error("El nombre no puede estar vacío.")
        return
    if auxiliares.existeNombre(bandas, nombre):
        pantalla.error("Esa banda ya existe.")
        return

    pais_id = pedirPais()
    if pais_id is None:
        return

    nueva_banda = {
        "id": auxiliares.nuevoId(bandas),
        "nombre": nombre,
        "pais_id": pais_id
    }
    bandas.append(nueva_banda)
    datos.guardarDatos("bandas", bandas)
    pantalla.avisar("Banda agregada.")


def editarBanda():
    bandas = datos.leerDatos("bandas")
    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    banda = auxiliares.elegirElemento(bandas, "¿Qué banda querés editar?")
    if banda is None:
        return

    # Nombre: si se deja vacío, queda el que estaba
    nombre_nuevo = pantalla.pedirTexto("Editar banda", "Nuevo nombre (dejalo vacío para mantener \"" + banda["nombre"] + "\"):")
    if nombre_nuevo is None:
        return
    if nombre_nuevo != "" and auxiliares.normalizar(nombre_nuevo) != auxiliares.normalizar(banda["nombre"]):
        if auxiliares.existeNombre(bandas, nombre_nuevo):
            pantalla.error("Ya existe una banda con ese nombre.")
            return
        banda["nombre"] = nombre_nuevo

    # País: si se responde que no, queda el que estaba
    if pantalla.confirmar("¿Querés cambiar el país?"):
        pais_id = pedirPais()
        if pais_id is None:
            return
        banda["pais_id"] = pais_id

    datos.guardarDatos("bandas", bandas)
    pantalla.avisar("Banda editada.")


def eliminarBanda():
    bandas = datos.leerDatos("bandas")
    tablaturas = datos.leerDatos("tablaturas")
    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    banda = auxiliares.elegirElemento(bandas, "¿Qué banda querés eliminar?")
    if banda is None:
        return

    if not pantalla.confirmar("¿Seguro que querés eliminar " + banda["nombre"] + "?\nTambién se borran sus tablaturas."):
        pantalla.avisar("No se eliminó nada.")
        return

    # Sacamos la banda
    bandas.remove(banda)

    # Nos quedamos solo con las tablaturas que NO son de esa banda
    tablaturas_que_quedan = []
    for tablatura in tablaturas:
        if tablatura["banda_id"] != banda["id"]:
            tablaturas_que_quedan.append(tablatura)

    datos.guardarDatos("bandas", bandas)
    datos.guardarDatos("tablaturas", tablaturas_que_quedan)
    pantalla.avisar("Banda eliminada.")
