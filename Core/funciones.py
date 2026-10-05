import json
import difflib


# ==================== BASE DE DATOS ====================
def leerDatos():
    """Abre el JSON y devuelve todo su contenido como un diccionario."""
    with open("Core/base_de_datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


def guardarDatos(datos):
    """Sobrescribe el JSON con los datos nuevos."""
    with open("Core/base_de_datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# ==================== AUXILIARES ====================
# Sirven para cualquier lista del JSON que tenga "id" y "nombre" (bandas, paises, etc.)

def normalizar(texto):
    """Pasa a minúsculas y saca las tildes, así "Perú" y "peru" se consideran iguales."""
    texto = texto.lower()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i")
    texto = texto.replace("ó", "o").replace("ú", "u").replace("ü", "u")
    return texto


def buscarPorId(lista, id_buscado):
    """Devuelve el elemento con ese id, o None si no existe."""
    for elemento in lista:
        if elemento["id"] == id_buscado:
            return elemento
    return None


def existeNombre(lista, nombre):
    """True si ya hay un elemento con ese nombre (sin importar mayúsculas)."""
    for elemento in lista:
        if normalizar(elemento["nombre"]) == normalizar(nombre):
            return True
    return False


def buscarPorNombre(lista, texto):
    """Busca en la lista por nombre y devuelve una lista con los resultados.
    1) Si hay uno con el nombre exacto, devuelve solo ese.
    2) Si no, devuelve los que contienen el texto ("rolling" -> The Rolling Stones).
    3) Si no hay ninguno, devuelve los parecidos ("beatels" -> The Beatles)."""
    texto = normalizar(texto)

    # 1) Exacto
    for elemento in lista:
        if normalizar(elemento["nombre"]) == texto:
            return [elemento]

    # 2) Contiene el texto
    encontrados = []
    for elemento in lista:
        if texto in normalizar(elemento["nombre"]):
            encontrados.append(elemento)
    if len(encontrados) > 0:
        return encontrados

    # 3) Parecidos
    nombres = []
    for elemento in lista:
        nombres.append(normalizar(elemento["nombre"]))
    parecidos = difflib.get_close_matches(texto, nombres, n=3, cutoff=0.5)

    for elemento in lista:
        if normalizar(elemento["nombre"]) in parecidos:
            encontrados.append(elemento)
    return encontrados


def elegirPorNombre(lista, pregunta):
    """Pide un nombre, lo busca en la lista y devuelve el elemento elegido, o None.
    Si hay varios resultados, los muestra y pide escribir el nombre completo."""
    texto = input(pregunta).strip()
    if texto == "":
        print("No escribiste nada.")
        return None

    resultados = buscarPorNombre(lista, texto)

    if len(resultados) == 0:
        print("No se encontró nada con ese nombre.")
        return None

    # Si encontró uno solo, es ese
    if len(resultados) == 1:
        return resultados[0]

    # Si encontró varios, hay que elegir escribiendo el nombre completo
    print("Se encontraron varios:")
    for elemento in resultados:
        print("- " + elemento["nombre"])

    nombre = input("Escribí el nombre completo: ").strip()
    for elemento in resultados:
        if normalizar(elemento["nombre"]) == normalizar(nombre):
            return elemento

    print("Ese nombre no está entre las opciones.")
    return None


# ==================== BANDAS ====================
def textoBanda(datos, banda):
    """Arma el texto para mostrar una banda, ej: "- The Beatles (Reino Unido)"."""
    pais = buscarPorId(datos["paises"], banda["pais_id"])
    nombre_pais = "sin país"
    if pais is not None:
        nombre_pais = pais["nombre"]
    return "- " + banda["nombre"] + " (" + nombre_pais + ")"


def mostrarBandas():
    datos = leerDatos()

    if len(datos["bandas"]) == 0:
        print("No hay bandas cargadas.")
        return
    print("\n--- BANDAS ---")
    for banda in datos["bandas"]:
        print(textoBanda(datos, banda))


def buscarBanda():
    datos = leerDatos()
    print("\n--- BUSCAR BANDA ---")
    texto = input("¿Qué banda buscás?: ").strip()
    if texto == "":
        print("No escribiste nada.")
        return

    resultados = buscarPorNombre(datos["bandas"], texto)

    if len(resultados) == 0:
        print("No se encontró ninguna banda.")
        return

    print("Resultados:")
    for banda in resultados:
        print(textoBanda(datos, banda))


# ==================== PAÍSES ====================
def pedirPais(datos):
    """Pide un país por nombre y devuelve su id, o None si no se eligió ninguno."""
    pais = elegirPorNombre(datos["paises"], "País de la banda: ")
    if pais is None:
        return None
    print("País: " + pais["nombre"])
    return pais["id"]