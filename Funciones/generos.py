from Funciones import datos, pantalla, auxiliares

# ==================== LISTADO ====================
def mostrarGeneros():
    generos = datos.leerDatos("generos")
    bandas = datos.leerDatos("bandas")

    if len(generos) == 0:
        pantalla.avisar("No hay géneros cargados.")
        return

    lineas = []
    for genero in generos:
        cantidad = auxiliares.contarRelacionados(bandas, "genero_id", genero["id"])
        lineas.append(genero["nombre"] + " - Bandas: " + str(cantidad))
    pantalla.mostrarLista("Todos los géneros", lineas)

def pedirGenero():
    """Muestra los géneros para elegir uno y devuelve su id, o None si no se eligió ninguno."""
    generos = datos.leerDatos("generos")
    if len(generos) == 0:
        pantalla.error("Primero tenés que cargar algún género.")
        return None

    genero = auxiliares.elegirElemento(generos, "¿De qué género es la banda?")
    if genero is None:
        return None
    return genero["id"]

# ==================== ABM GÉNEROS ====================
def agregarGenero():
    generos = datos.leerDatos("generos")

    nombre = pantalla.pedirTexto("Agregar género", "Nombre del género:")
    if nombre is None:
        return
    if nombre == "":
        pantalla.error("El nombre no puede estar vacío.")
        return
    if auxiliares.existeNombre(generos, nombre):
        pantalla.error("Ese género ya existe.")
        return

    nuevo_genero = {"id": auxiliares.nuevoId(generos), "nombre": nombre}
    generos.append(nuevo_genero)
    datos.guardarDatos("generos", generos)
    pantalla.avisar("Género agregado.")

def editarGenero():
    generos = datos.leerDatos("generos")
    if len(generos) == 0:
        pantalla.avisar("No hay géneros cargados.")
        return

    genero = auxiliares.elegirElemento(generos, "¿Qué género querés editar?")
    if genero is None:
        return

    nombre_nuevo = pantalla.pedirTexto("Editar género", "Nuevo nombre para \"" + genero["nombre"] + "\":")
    if nombre_nuevo is None:
        return
    if nombre_nuevo == "":
        pantalla.error("El nombre no puede estar vacío.")
        return

    # Si solo cambian mayúsculas o tildes del mismo género, no es un repetido
    es_el_mismo = auxiliares.normalizar(nombre_nuevo) == auxiliares.normalizar(genero["nombre"])
    if not es_el_mismo and auxiliares.existeNombre(generos, nombre_nuevo):
        pantalla.error("Ya existe un género con ese nombre.")
        return

    genero["nombre"] = nombre_nuevo
    datos.guardarDatos("generos", generos)
    pantalla.avisar("Género editado.")

def eliminarGenero():
    generos = datos.leerDatos("generos")
    bandas = datos.leerDatos("bandas")
    if len(generos) == 0:
        pantalla.avisar("No hay géneros cargados.")
        return

    genero = auxiliares.elegirElemento(generos, "¿Qué género querés eliminar?")
    if genero is None:
        return

    # Si alguna banda lo usa no se puede borrar, porque quedaría sin género
    cantidad = auxiliares.contarRelacionados(bandas, "genero_id", genero["id"])
    if cantidad > 0:
        pantalla.error("No se puede eliminar " + genero["nombre"] + ": lo usan " + str(cantidad) + " banda/s.")
        return

    if not pantalla.confirmar("¿Seguro que querés eliminar " + genero["nombre"] + "?"):
        pantalla.avisar("No se eliminó nada.")
        return

    generos.remove(genero)
    datos.guardarDatos("generos", generos)
    pantalla.avisar("Género eliminado.")