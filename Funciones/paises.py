from Funciones import datos, pantalla, auxiliares

# ==================== LISTADO ====================
def mostrarPaises():
    paises = datos.leerDatos("paises")
    bandas = datos.leerDatos("bandas")
    integrantes = datos.leerDatos("integrantes")

    if len(paises) == 0:
        pantalla.avisar("No hay países cargados.")
        return

    lineas = []
    for pais in paises:
        cantidad_bandas = auxiliares.contarRelacionados(bandas, "pais_id", pais["id"])
        cantidad_integrantes = auxiliares.contarRelacionados(integrantes, "pais_id", pais["id"])
        lineas.append(pais["nombre"] + " - Bandas: " + str(cantidad_bandas) + " - Integrantes: " + str(cantidad_integrantes))
    pantalla.mostrarLista("Todos los países", lineas)

def pedirPais(pregunta):
    """Pide un país por nombre y devuelve su id, o None si no se eligió ninguno."""
    paises = datos.leerDatos("paises")
    pais = auxiliares.elegirPorNombre(paises, "País", pregunta)
    if pais is None:
        return None
    return pais["id"]

# ==================== ABM PAÍSES ====================
def agregarPais():
    paises = datos.leerDatos("paises")

    nombre = pantalla.pedirTexto("Agregar país", "Nombre del país:")
    if nombre is None:
        return
    if nombre == "":
        pantalla.error("El nombre no puede estar vacío.")
        return
    if auxiliares.existeNombre(paises, nombre):
        pantalla.error("Ese país ya existe.")
        return

    nuevo_pais = {"id": auxiliares.nuevoId(paises), "nombre": nombre}
    paises.append(nuevo_pais)
    datos.guardarDatos("paises", paises)
    pantalla.avisar("País agregado.")

def editarPais():
    paises = datos.leerDatos("paises")
    if len(paises) == 0:
        pantalla.avisar("No hay países cargados.")
        return

    # Son muchos países, así que se busca por nombre en vez de mostrar toda la lista
    pais = auxiliares.elegirPorNombre(paises, "Editar país", "¿Qué país querés editar?")
    if pais is None:
        return

    nombre_nuevo = pantalla.pedirTexto("Editar país", "Nuevo nombre para \"" + pais["nombre"] + "\":")
    if nombre_nuevo is None:
        return
    if nombre_nuevo == "":
        pantalla.error("El nombre no puede estar vacío.")
        return

    # Si solo cambian mayúsculas o tildes del mismo país, no es un repetido
    es_el_mismo = auxiliares.normalizar(nombre_nuevo) == auxiliares.normalizar(pais["nombre"])
    if not es_el_mismo and auxiliares.existeNombre(paises, nombre_nuevo):
        pantalla.error("Ya existe un país con ese nombre.")
        return

    pais["nombre"] = nombre_nuevo
    datos.guardarDatos("paises", paises)
    pantalla.avisar("País editado.")

def eliminarPais():
    paises = datos.leerDatos("paises")
    bandas = datos.leerDatos("bandas")
    integrantes = datos.leerDatos("integrantes")
    if len(paises) == 0:
        pantalla.avisar("No hay países cargados.")
        return

    pais = auxiliares.elegirPorNombre(paises, "Eliminar país", "¿Qué país querés eliminar?")
    if pais is None:
        return

    # Si alguna banda o integrante lo usa no se puede borrar
    cantidad_bandas = auxiliares.contarRelacionados(bandas, "pais_id", pais["id"])
    cantidad_integrantes = auxiliares.contarRelacionados(integrantes, "pais_id", pais["id"])
    if cantidad_bandas > 0 or cantidad_integrantes > 0:
        pantalla.error("No se puede eliminar " + pais["nombre"] + ": lo usan " + str(cantidad_bandas) + " banda/s y " + str(cantidad_integrantes) + " integrante/s.")
        return

    if not pantalla.confirmar("¿Seguro que querés eliminar " + pais["nombre"] + "?"):
        pantalla.avisar("No se eliminó nada.")
        return

    paises.remove(pais)
    datos.guardarDatos("paises", paises)
    pantalla.avisar("País eliminado.")