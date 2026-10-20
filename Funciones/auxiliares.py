import difflib

from Funciones import pantalla


# ==================== AUXILIARES ====================
# Sirven para cualquier lista que tenga "id" y "nombre" (bandas, paises, tablaturas, etc.)

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


def nuevoId(lista):
    """Devuelve el id para un elemento nuevo: el más grande que haya + 1."""
    id_nuevo = 1
    for elemento in lista:
        if elemento["id"] >= id_nuevo:
            id_nuevo = elemento["id"] + 1
    return id_nuevo


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


def elegirElemento(lista, titulo):
    """Muestra los nombres de la lista en una ventanita para elegir uno.
    Devuelve el elemento elegido, o None si no se eligió nada."""
    nombres = []
    for elemento in lista:
        nombres.append(elemento["nombre"])

    nombre_elegido = pantalla.elegirDeLista(titulo, nombres)
    if nombre_elegido is None:
        return None

    for elemento in lista:
        if elemento["nombre"] == nombre_elegido:
            return elemento
    return None


def elegirPorNombre(lista, titulo, pregunta):
    """Pide un nombre, lo busca en la lista y devuelve el elemento elegido, o None.
    Si hay varios resultados, los muestra en una lista para elegir uno."""
    texto = pantalla.pedirTexto(titulo, pregunta)
    if texto is None:
        return None
    if texto == "":
        pantalla.error("No escribiste nada.")
        return None

    resultados = buscarPorNombre(lista, texto)

    if len(resultados) == 0:
        pantalla.error("No se encontró nada con ese nombre.")
        return None

    # Si encontró uno solo, es ese
    if len(resultados) == 1:
        return resultados[0]

    # Si encontró varios, el usuario elige uno de la lista
    return elegirElemento(resultados, "Se encontraron varios, elegí uno")
