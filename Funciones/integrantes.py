from Funciones import datos, pantalla, auxiliares

# ==================== AGREGAR INTEGRANTES ====================
def agregarIntegrante():
    bandas = datos.leerDatos("bandas")
    integrantes = datos.leerDatos("integrantes")

    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    # Elegimos a qué banda pertenece el integrante
    banda = auxiliares.elegirElemento(
        bandas,
        "¿A qué banda pertenece el integrante?"
    )

    if banda is None:
        return

    # Pedimos el nombre
    nombre = pantalla.pedirTexto(
        "Agregar integrante",
        "Nombre del integrante:"
    )

    if nombre is None:
        return

    if nombre == "":
        pantalla.error("El nombre no puede estar vacío.")
        return

    # Pedimos el instrumento
    instrumento = pantalla.pedirTexto(
        "Agregar integrante",
        "¿Qué instrumento toca?"
    )

    if instrumento is None:
        return

    if instrumento == "":
        pantalla.error("El instrumento no puede estar vacío.")
        return

    # Creamos el nuevo integrante
    nuevo_integrante = {
        "id": auxiliares.nuevoId(integrantes),
        "nombre": nombre,
        "instrumento": instrumento,
        "banda_id": banda["id"]
    }

    integrantes.append(nuevo_integrante)

    # Guardamos en el archivo JSON
    datos.guardarDatos("integrantes", integrantes)

    pantalla.avisar(
        nombre + " fue agregado a " + banda["nombre"] + "."
    )