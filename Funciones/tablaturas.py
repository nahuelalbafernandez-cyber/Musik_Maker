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
        nombre_banda = auxiliares.nombrePorId(bandas, tablatura["banda_id"], "sin banda")
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

    nueva_tablatura = {"id": auxiliares.nuevoId(tablaturas), "nombre": nombre, "link": link, "banda_id": banda["id"]}
    tablaturas.append(nueva_tablatura)
    datos.guardarDatos("tablaturas", tablaturas)
    pantalla.avisar("Tablatura agregada.")


def editarTablatura():
    tablaturas = datos.leerDatos("tablaturas")
    bandas = datos.leerDatos("bandas")
    if len(tablaturas) == 0:
        pantalla.avisar("No hay tablaturas cargadas.")
        return

    tablatura = auxiliares.elegirElemento(tablaturas, "¿Qué tablatura querés editar?")
    if tablatura is None:
        return

    # Nombre: si se deja vacío, queda el que estaba
    nombre_nuevo = pantalla.pedirTexto("Editar tablatura", "Nuevo nombre (dejalo vacío para mantener \"" + tablatura["nombre"] + "\"):")
    if nombre_nuevo is None:
        return
    if nombre_nuevo != "":
        es_el_mismo = auxiliares.normalizar(nombre_nuevo) == auxiliares.normalizar(tablatura["nombre"])
        if not es_el_mismo and auxiliares.existeNombre(tablaturas, nombre_nuevo):
            pantalla.error("Ya existe una tablatura con ese nombre.")
            return
        tablatura["nombre"] = nombre_nuevo

    # Link: si se deja vacío, queda el que estaba
    link_nuevo = pantalla.pedirTexto("Editar tablatura", "Nuevo link (dejalo vacío para mantener el actual):")
    if link_nuevo is None:
        return
    if link_nuevo != "":
        tablatura["link"] = link_nuevo

    # Banda: si se responde que no, queda la que estaba
    if pantalla.confirmar("¿Querés cambiar la banda?"):
        banda = auxiliares.elegirElemento(bandas, "¿De qué banda es?")
        if banda is None:
            return
        tablatura["banda_id"] = banda["id"]

    datos.guardarDatos("tablaturas", tablaturas)
    pantalla.avisar("Tablatura editada.")

def eliminarTablatura():
    tablaturas = datos.leerDatos("tablaturas")
    if len(tablaturas) == 0:
        pantalla.avisar("No hay tablaturas cargadas.")
        return

    tablatura = auxiliares.elegirElemento(tablaturas, "¿Qué tablatura querés eliminar?")
    if tablatura is None:
        return

    if not pantalla.confirmar("¿Seguro que querés eliminar " + tablatura["nombre"] + "?"):
        pantalla.avisar("No se eliminó nada.")
        return

    tablaturas.remove(tablatura)
    datos.guardarDatos("tablaturas", tablaturas)
    pantalla.avisar("Tablatura eliminada.")