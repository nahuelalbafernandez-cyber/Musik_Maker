from Funciones import datos, pantalla, auxiliares, generos as modulo_generos, paises as modulo_paises

# ==================== MOSTRAR Y BUSCAR ====================
def textoBanda(banda, paises, generos):
    """Arma el texto para mostrar una banda, ej: "The Beatles (Reino Unido) - Rock"."""
    nombre_pais = auxiliares.nombrePorId(paises, banda["pais_id"], "sin país")
    # Usamos .get() porque las bandas viejas todavía no tienen género
    nombre_genero = auxiliares.nombrePorId(generos, banda.get("genero_id"), "sin género")
    return banda["nombre"] + " (" + nombre_pais + ") - " + nombre_genero

def mostrarBandas():
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")
    generos = datos.leerDatos("generos")

    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    lineas = []
    for banda in bandas:
        lineas.append(textoBanda(banda, paises, generos))
    pantalla.mostrarLista("Todas las bandas", lineas)

def buscarBanda():
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")
    generos = datos.leerDatos("generos")

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
        lineas.append(textoBanda(banda, paises, generos))
    pantalla.mostrarLista("Resultados de la búsqueda", lineas)

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

    pais_id = modulo_paises.pedirPais("¿De qué país es la banda?")
    if pais_id is None:
        return

    genero_id = modulo_generos.pedirGenero()
    if genero_id is None:
        return

    nueva_banda = {"id": auxiliares.nuevoId(bandas), "nombre": nombre, "pais_id": pais_id, "genero_id": genero_id}
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
    if nombre_nuevo != "":
        # Si solo cambian mayúsculas o tildes de la misma banda, no es un repetido
        es_la_misma = auxiliares.normalizar(nombre_nuevo) == auxiliares.normalizar(banda["nombre"])
        if not es_la_misma and auxiliares.existeNombre(bandas, nombre_nuevo):
            pantalla.error("Ya existe una banda con ese nombre.")
            return
        banda["nombre"] = nombre_nuevo

    # País: si se responde que no, queda el que estaba
    if pantalla.confirmar("¿Querés cambiar el país?"):
        pais_id = modulo_paises.pedirPais("¿De qué país es la banda?")
        if pais_id is None:
            return
        banda["pais_id"] = pais_id

    # Género: si se responde que no, queda el que estaba
    if pantalla.confirmar("¿Querés cambiar el género?"):
        genero_id = modulo_generos.pedirGenero()
        if genero_id is None:
            return
        banda["genero_id"] = genero_id

    datos.guardarDatos("bandas", bandas)
    pantalla.avisar("Banda editada.")

def eliminarBanda():
    bandas = datos.leerDatos("bandas")
    tablaturas = datos.leerDatos("tablaturas")
    integrantes = datos.leerDatos("integrantes")
    usuarios = datos.leerDatos("usuarios")
    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    banda = auxiliares.elegirElemento(bandas, "¿Qué banda querés eliminar?")
    if banda is None:
        return

    cantidad_integrantes = auxiliares.contarRelacionados(integrantes, "banda_id", banda["id"])
    cantidad_tablaturas = auxiliares.contarRelacionados(tablaturas, "banda_id", banda["id"])

    # Contamos cuántos usuarios la tienen en favoritas
    cantidad_usuarios = 0
    for usuario in usuarios:
        if banda["id"] in usuario["bandas_favoritas"]:
            cantidad_usuarios = cantidad_usuarios + 1

    # Si la banda tiene algo adentro, avisamos qué se va a borrar con ella
    pregunta = "¿Seguro que querés eliminar " + banda["nombre"] + "?"
    if cantidad_integrantes > 0 or cantidad_tablaturas > 0 or cantidad_usuarios > 0:
        pregunta = "¡Ojo! " + banda["nombre"] + " tiene " + str(cantidad_integrantes) + " integrante/s y " + str(cantidad_tablaturas) + " tablatura/s, y está en favoritas de " + str(cantidad_usuarios) + " usuario/s.\nSi la eliminás, también se borra todo eso. ¿Querés eliminarla igual?"

    if not pantalla.confirmar(pregunta):
        pantalla.avisar("No se eliminó nada.")
        return

    # Sacamos la banda
    bandas.remove(banda)

    # Nos quedamos solo con las tablaturas que NO son de esa banda
    tablaturas_que_quedan = []
    for tablatura in tablaturas:
        if tablatura["banda_id"] != banda["id"]:
            tablaturas_que_quedan.append(tablatura)

    # Lo mismo con los integrantes
    integrantes_que_quedan = []
    for integrante in integrantes:
        if integrante["banda_id"] != banda["id"]:
            integrantes_que_quedan.append(integrante)

    # Y la sacamos de las favoritas de todos los usuarios
    for usuario in usuarios:
        if banda["id"] in usuario["bandas_favoritas"]:
            usuario["bandas_favoritas"].remove(banda["id"])

    datos.guardarDatos("bandas", bandas)
    datos.guardarDatos("tablaturas", tablaturas_que_quedan)
    datos.guardarDatos("integrantes", integrantes_que_quedan)
    datos.guardarDatos("usuarios", usuarios)
    pantalla.avisar("Banda eliminada.")