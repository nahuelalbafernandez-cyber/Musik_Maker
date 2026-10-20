from Funciones import datos, pantalla, auxiliares


# ==================== TABLATURAS ====================
def mostrarTablaturas():
    tablaturas = datos.leerDatos("tablaturas")
    bandas = datos.leerDatos("bandas")

    if len(tablaturas) == 0:
        pantalla.avisar("No hay tablaturas cargadas.")
        return

    lineas = []
    for tablatura in tablaturas:
        banda = auxiliares.buscarPorId(bandas, tablatura["banda_id"])
        nombre_banda = "sin banda"
        if banda is not None:
            nombre_banda = banda["nombre"]
        lineas.append(tablatura["nombre"] + " - " + nombre_banda)
        lineas.append("     " + tablatura["link"])
    pantalla.mostrarLista("Tablaturas", lineas)


def agregarTablatura():
    tablaturas = datos.leerDatos("tablaturas")
    bandas = datos.leerDatos("bandas")

    if len(bandas) == 0:
        pantalla.error("Primero tenés que cargar alguna banda.")
        return

    nombre = pantalla.pedirTexto("Agregar tablatura", "Nombre de la tablatura:")
    if nombre is None:
        return
    if nombre == "":
        pantalla.error("No se ingresó un nombre válido.")
        return
    if auxiliares.existeNombre(tablaturas, nombre):
        pantalla.error("Esa tablatura ya existe.")
        return

    link = pantalla.pedirTexto("Agregar tablatura", "Link de la tablatura:")
    if link is None:
        return
    if link == "":
        pantalla.error("No se ingresó ningún link.")
        return

    banda = auxiliares.elegirElemento(bandas, "¿De qué banda es?")
    if banda is None:
        return

    nueva_tablatura = {
        "id": auxiliares.nuevoId(tablaturas),
        "nombre": nombre,
        "link": link,
        "banda_id": banda["id"]
    }
    tablaturas.append(nueva_tablatura)
    datos.guardarDatos("tablaturas", tablaturas)
    pantalla.avisar("Tablatura agregada.")
