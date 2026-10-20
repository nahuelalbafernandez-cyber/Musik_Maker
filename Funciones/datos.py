import json


# ==================== BASE DE DATOS ====================
# Cada "tabla" es un archivo distinto dentro de la carpeta db:
#   leerDatos("bandas")  ->  abre db/db_bandas.json
#   leerDatos("paises")  ->  abre db/db_paises.json
#   leerDatos("menus")   ->  abre db/db_menus.json   (y así con todos)

def rutaArchivo(nombre):
    """Arma la ruta del archivo, ej: "bandas" -> "db/db_bandas.json"."""
    return "db/db_" + nombre + ".json"


def leerDatos(nombre):
    """Abre el JSON de esa tabla y devuelve su contenido."""
    with open(rutaArchivo(nombre), "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


def guardarDatos(nombre, datos):
    """Sobrescribe el JSON de esa tabla con los datos nuevos."""
    with open(rutaArchivo(nombre), "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
