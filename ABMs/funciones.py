from Core import funciones as core


# ==================== ABM BANDAS ====================
def agregarBanda():
    datos = core.leerDatos()
    print("\n--- AGREGAR BANDA ---")
    nombre = input("Nombre de la banda: ").strip()

    if nombre == "":
        print("El nombre no puede estar vacío.")
        return
    if core.existeNombre(datos["bandas"], nombre):
        print("Esa banda ya existe.")
        return

    pais_id = core.pedirPais(datos)
    if pais_id is None:
        return

    # El id nuevo es el más grande que haya + 1
    id_nuevo = 1
    for banda in datos["bandas"]:
        if banda["id"] >= id_nuevo:
            id_nuevo = banda["id"] + 1

    nueva_banda = {
        "id": id_nuevo,
        "nombre": nombre,
        "pais_id": pais_id
    }
    datos["bandas"].append(nueva_banda)
    core.guardarDatos(datos)
    print("Banda agregada.")


def editarBanda():
    datos = core.leerDatos()
    print("\n--- EDITAR BANDA ---")
    core.mostrarBandas()
    banda = core.elegirPorNombre(datos["bandas"], "¿Qué banda querés editar?: ")
    if banda is None:
        return

    # Nombre: si se deja vacío, queda el que estaba
    nombre_nuevo = input("Nuevo nombre (Enter para dejar \"" + banda["nombre"] + "\"): ").strip()
    if nombre_nuevo != "" and core.normalizar(nombre_nuevo) != core.normalizar(banda["nombre"]):
        if core.existeNombre(datos["bandas"], nombre_nuevo):
            print("Ya existe una banda con ese nombre.")
            return
        banda["nombre"] = nombre_nuevo

    # País: si se responde que no, queda el que estaba
    cambiar_pais = input("¿Cambiar el país? (s/n): ").strip().lower()
    if cambiar_pais == "s":
        pais_id = core.pedirPais(datos)
        if pais_id is None:
            return
        banda["pais_id"] = pais_id

    core.guardarDatos(datos)
    print("Banda editada.")


def eliminarBanda():
    datos = core.leerDatos()
    print("\n--- ELIMINAR BANDA ---")
    core.mostrarBandas()
    banda = core.elegirPorNombre(datos["bandas"], "¿Qué banda querés eliminar?: ")
    if banda is None:
        return

    confirmar = input("¿Seguro que querés eliminar " + banda["nombre"] + "? (s/n): ").strip().lower()
    if confirmar != "s":
        print("No se eliminó nada.")
        return

    datos["bandas"].remove(banda)
    core.guardarDatos(datos)
    print("Banda eliminada.")

def pedirbanda(datos):
    """Pide una banda por nombre y devuelve su id, o None si no se eligió ninguno."""
    banda = core.elegirPorNombre(datos["bandas"], "banda: ")
    if banda is None:
        return None
    print("Banda: " + banda["nombre"])
    return banda["id"]

def  agregartablaturas():
     datos = core.leerDatos()
     print("\n--- AGREGAR TABLATURA---")
     nombre = input("Nombre de la tablatura").strip()
     if nombre =="":
         print("No se ingresó un nombre válido")
         return
     
     if core.existeNombre(datos["tablaturas"], nombre):
         print("Esa tablatura ya existe.")
         return
     
     link = input("link de la tablatura")
     if link =="":
          print("No se ingresó ningun link")
          return
     
     banda_id = pedirbanda(datos)
     if banda_id is None:
         return
     
     id_nuevo = 1
     for tablatura in datos["tablaturas"]:
         if tablatura["id"] >= id_nuevo:
                     id_nuevo = tablatura["id"] + 1

     nueva_tablatura = {
            "id": id_nuevo,
            "nombre": nombre,
            "link": link,
            "banda_id": banda_id
     }
     datos["tablaturas"].append(nueva_tablatura)
     core.guardarDatos(datos)
     print("Tablatura Agregada.")
 