from Funciones import datos, pantalla, auxiliares, paises as modulo_paises

# ==================== MOSTRAR Y ELEGIR ====================
def textoIntegrante(integrante, bandas):
    """Arma el texto para mostrar y elegir un integrante, ej: "Paul McCartney - The Beatles".
    Lleva la banda porque puede haber dos personas con el mismo nombre en bandas distintas."""
    nombre_banda = auxiliares.nombrePorId(bandas, integrante["banda_id"], "sin banda")
    return integrante["nombre"] + " - " + nombre_banda

def mostrarIntegrantes():
    integrantes = datos.leerDatos("integrantes")
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")

    if len(integrantes) == 0:
        pantalla.avisar("No hay integrantes cargados.")
        return

    lineas = []
    for integrante in integrantes:
        # Usamos .get() porque los integrantes viejos todavía no tienen país
        nombre_pais = auxiliares.nombrePorId(paises, integrante.get("pais_id"), "sin país")
        lineas.append(textoIntegrante(integrante, bandas))
        lineas.append("     " + integrante["instrumento"] + " - " + nombre_pais)
    pantalla.mostrarLista("Todos los integrantes", lineas)

def elegirIntegrante(integrantes, bandas, titulo):
    """Muestra los integrantes para elegir uno. Devuelve el elegido, o None."""
    opciones = []
    for integrante in integrantes:
        opciones.append(textoIntegrante(integrante, bandas))

    opcion_elegida = pantalla.elegirDeLista(titulo, opciones)
    if opcion_elegida is None:
        return None

    for integrante in integrantes:
        if textoIntegrante(integrante, bandas) == opcion_elegida:
            return integrante
    return None

def existeEnBanda(integrantes, nombre, banda_id, id_a_ignorar):
    """True si esa banda ya tiene otro integrante con ese nombre.
    id_a_ignorar sirve al editar, para que no se compare con él mismo."""
    for integrante in integrantes:
        mismo_nombre = auxiliares.normalizar(integrante["nombre"]) == auxiliares.normalizar(nombre)
        if mismo_nombre and integrante["banda_id"] == banda_id and integrante["id"] != id_a_ignorar:
            return True
    return False

# ==================== ABM INTEGRANTES ====================
def agregarIntegrante():
    bandas = datos.leerDatos("bandas")
    integrantes = datos.leerDatos("integrantes")
    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    # Elegimos a qué banda pertenece el integrante
    banda = auxiliares.elegirElemento(bandas, "¿A qué banda pertenece el integrante?")
    if banda is None:
        return

    # Pedimos el nombre
    nombre = pantalla.pedirTexto("Agregar integrante", "Nombre del integrante:")
    if nombre is None:
        return
    if nombre == "":
        pantalla.error("El nombre no puede estar vacío.")
        return

    if existeEnBanda(integrantes, nombre, banda["id"], None):
        pantalla.error("Ese integrante ya está en " + banda["nombre"] + ".")
        return

    # Pedimos el instrumento
    instrumento = pantalla.pedirTexto("Agregar integrante", "¿Qué instrumento toca?")
    if instrumento is None:
        return
    if instrumento == "":
        pantalla.error("El instrumento no puede estar vacío.")
        return

    # Pedimos el país
    pais_id = modulo_paises.pedirPais("¿De qué país es el integrante?")

    if pais_id is None:
        return

    # Creamos el nuevo integrante
    nuevo_integrante = {"id": auxiliares.nuevoId(integrantes), "nombre": nombre, "instrumento": instrumento, "banda_id": banda["id"], "pais_id": pais_id}
    integrantes.append(nuevo_integrante)

    # Guardamos en el archivo JSON
    datos.guardarDatos("integrantes", integrantes)
    pantalla.avisar(nombre + " fue agregado a " + banda["nombre"] + ".")

def editarIntegrante():
    integrantes = datos.leerDatos("integrantes")
    bandas = datos.leerDatos("bandas")
    if len(integrantes) == 0:
        pantalla.avisar("No hay integrantes cargados.")
        return

    integrante = elegirIntegrante(integrantes, bandas, "¿Qué integrante querés editar?")
    if integrante is None:
        return

    # Nombre: si se deja vacío, queda el que estaba
    nombre_nuevo = pantalla.pedirTexto("Editar integrante", "Nuevo nombre (dejalo vacío para mantener \"" + integrante["nombre"] + "\"):")
    if nombre_nuevo is None:
        return
    if nombre_nuevo != "":
        integrante["nombre"] = nombre_nuevo

    # Instrumento: si se deja vacío, queda el que estaba
    instrumento_nuevo = pantalla.pedirTexto("Editar integrante", "Nuevo instrumento (dejalo vacío para mantener \"" + integrante["instrumento"] + "\"):")
    if instrumento_nuevo is None:
        return
    if instrumento_nuevo != "":
        integrante["instrumento"] = instrumento_nuevo

    # Banda: si se responde que no, queda la que estaba
    if pantalla.confirmar("¿Querés cambiar la banda?"):
        banda = auxiliares.elegirElemento(bandas, "¿A qué banda pertenece?")
        if banda is None:
            return
        integrante["banda_id"] = banda["id"]

    # País: si se responde que no, queda el que estaba
    if pantalla.confirmar("¿Querés cambiar el país?"):
        pais_id = modulo_paises.pedirPais("¿De qué país es el integrante?")
        if pais_id is None:
            return
        integrante["pais_id"] = pais_id

    # Revisamos al final porque recién acá sabemos el nombre y la banda definitivos
    if existeEnBanda(integrantes, integrante["nombre"], integrante["banda_id"], integrante["id"]):
        pantalla.error("Esa banda ya tiene un integrante con ese nombre.")
        return

    datos.guardarDatos("integrantes", integrantes)
    pantalla.avisar("Integrante editado.")

def eliminarIntegrante():
    integrantes = datos.leerDatos("integrantes")
    bandas = datos.leerDatos("bandas")
    if len(integrantes) == 0:
        pantalla.avisar("No hay integrantes cargados.")
        return

    integrante = elegirIntegrante(integrantes, bandas, "¿Qué integrante querés eliminar?")
    if integrante is None:
        return

    if not pantalla.confirmar("¿Seguro que querés eliminar a " + textoIntegrante(integrante, bandas) + "?"):
        pantalla.avisar("No se eliminó nada.")
        return

    integrantes.remove(integrante)
    datos.guardarDatos("integrantes", integrantes)
    pantalla.avisar("Integrante eliminado.")