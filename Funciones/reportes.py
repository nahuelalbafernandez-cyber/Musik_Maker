import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from Funciones import datos, pantalla, auxiliares

# ==================== REPORTE: BANDAS POR PAÍS ====================
def reporteBandasPorPais():
    bandas = datos.leerDatos("bandas")
    paises = datos.leerDatos("paises")

    pais = auxiliares.elegirPorNombre(paises, "Reporte", "¿De qué país?")
    if pais is None:
        return

    # Juntamos las bandas de ese país
    bandas_del_pais = []
    for banda in bandas:
        if banda["pais_id"] == pais["id"]:
            bandas_del_pais.append(banda)

    if len(bandas_del_pais) == 0:
        pantalla.avisar("No hay bandas de " + pais["nombre"] + ".")
        return

    # Armamos el Excel
    libro = Workbook()             # el archivo
    hoja = libro.active            # la primera hoja
    hoja.title = "Bandas"

    # Encabezado en negrita
    hoja.append(["Banda", "País"])
    hoja["A1"].font = Font(bold=True)
    hoja["B1"].font = Font(bold=True)

    # Una fila por banda
    for banda in bandas_del_pais:
        hoja.append([banda["nombre"], pais["nombre"]])

    # Ancho de las columnas para que se lean bien
    hoja.column_dimensions["A"].width = 30
    hoja.column_dimensions["B"].width = 20

    nombre_archivo = "Reportes/bandas_" + pais["nombre"].replace(" ", "_") + ".xlsx"
    libro.save(nombre_archivo)

    # Mostramos en pantalla las bandas y dónde quedó el Excel
    lineas = []
    for banda in bandas_del_pais:
        lineas.append(banda["nombre"])
    pantalla.mostrarLista("Bandas de " + pais["nombre"], lineas)
    pantalla.avisar("Reporte descargado en: " + nombre_archivo)

# ==================== REPORTE COMBINADO ====================
def opcionesDeFiltro(elementos, campo, tabla, texto_vacio):
    """Arma las opciones para filtrar: "Todos" y los nombres que realmente se usan.
    Ej: de los 195 países solo ofrece los que tienen alguna banda."""
    nombres = []
    for elemento in elementos:
        nombre = auxiliares.nombrePorId(tabla, elemento.get(campo), texto_vacio)
        if nombre not in nombres:
            nombres.append(nombre)

    nombres.sort(key=auxiliares.normalizar)
    return ["Todos"] + nombres

def textosIntegrantes(banda, integrantes, paises, filtro_pais):
    """Devuelve una lista con los integrantes de la banda.
    Si hay filtro, deja solo los integrantes de ese país."""
    textos = []
    for integrante in integrantes:
        if integrante["banda_id"] == banda["id"]:
            nombre_pais = auxiliares.nombrePorId(paises, integrante.get("pais_id"), "sin país")
            if filtro_pais == "Todos" or filtro_pais == nombre_pais:
                textos.append(integrante["nombre"] + " - " + integrante["instrumento"] + " (" + nombre_pais + ")")
    return textos

def textosTablaturas(banda, tablaturas):
    """Devuelve una lista con las tablaturas de la banda, ej: "Let it Be - https://...". """
    textos = []
    for tablatura in tablaturas:
        if tablatura["banda_id"] == banda["id"]:
            textos.append(tablatura["nombre"] + " - " + tablatura["link"])
    return textos

def guardarExcelCombinado(encabezados, filas):
    """Guarda el reporte en un Excel y devuelve la ruta del archivo."""
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Reporte"

    hoja.append(encabezados)
    for fila in filas:
        hoja.append(fila)

    # Encabezado en negrita y las celdas con saltos de línea bien acomodadas
    for numero_fila, fila in enumerate(hoja.iter_rows(), start=1):
        for celda in fila:
            celda.alignment = Alignment(wrap_text=True, vertical="top")
            if numero_fila == 1:
                celda.font = Font(bold=True)

    # Ancho de cada columna: las de integrantes y tablaturas necesitan más lugar
    letras = "ABCDE"
    for posicion in range(len(encabezados)):
        ancho = 22
        if encabezados[posicion] == "Banda":
            ancho = 38
        if encabezados[posicion] == "Integrantes" or encabezados[posicion] == "Tablaturas":
            ancho = 55
        hoja.column_dimensions[letras[posicion]].width = ancho

    # La fecha y hora en el nombre hacen que no se pise un reporte anterior
    os.makedirs("Reportes", exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = "Reportes/reporte_combinado_" + fecha + ".xlsx"
    libro.save(nombre_archivo)
    return nombre_archivo

def reporteCombinado():
    bandas = datos.leerDatos("bandas")
    generos = datos.leerDatos("generos")
    paises = datos.leerDatos("paises")
    integrantes = datos.leerDatos("integrantes")
    tablaturas = datos.leerDatos("tablaturas")

    if len(bandas) == 0:
        pantalla.avisar("No hay bandas cargadas.")
        return

    # 1) El usuario elige qué quiere combinar
    elegidos = pantalla.elegirVarios("¿Qué querés combinar con las bandas?", ["Géneros", "Países", "Integrantes", "Tablaturas"])
    if elegidos is None:
        return
    usa_generos = "Géneros" in elegidos
    usa_paises = "Países" in elegidos
    usa_integrantes = "Integrantes" in elegidos
    usa_tablaturas = "Tablaturas" in elegidos

    # 2) Por cada cosa elegida puede filtrar, o dejar "Todos"
    filtro_genero = "Todos"
    filtro_pais = "Todos"
    filtro_pais_integrante = "Todos"

    if usa_generos:
        opciones = opcionesDeFiltro(bandas, "genero_id", generos, "sin género")
        filtro_genero = pantalla.elegirDeLista("Filtrar por género", opciones)
        if filtro_genero is None:
            return

    if usa_paises:
        opciones = opcionesDeFiltro(bandas, "pais_id", paises, "sin país")
        filtro_pais = pantalla.elegirDeLista("Filtrar por país de la banda", opciones)
        if filtro_pais is None:
            return

    if usa_integrantes:
        opciones = opcionesDeFiltro(integrantes, "pais_id", paises, "sin país")
        filtro_pais_integrante = pantalla.elegirDeLista("Filtrar por país del integrante", opciones)
        if filtro_pais_integrante is None:
            return

    # 3) Armamos las columnas según lo que se eligió
    encabezados = ["Banda"]
    if usa_generos:
        encabezados.append("Género")
    if usa_paises:
        encabezados.append("País")
    if usa_integrantes:
        encabezados.append("Integrantes")
    if usa_tablaturas:
        encabezados.append("Tablaturas")

    # 4) Recorremos las bandas: filas para el Excel y líneas para la pantalla
    filas = []
    lineas = []
    for banda in bandas:
        nombre_genero = auxiliares.nombrePorId(generos, banda.get("genero_id"), "sin género")
        nombre_pais = auxiliares.nombrePorId(paises, banda["pais_id"], "sin país")
        lista_integrantes = textosIntegrantes(banda, integrantes, paises, filtro_pais_integrante)
        lista_tablaturas = textosTablaturas(banda, tablaturas)

        # Si la banda no cumple algún filtro, pasamos a la siguiente
        if filtro_genero != "Todos" and filtro_genero != nombre_genero:
            continue
        if filtro_pais != "Todos" and filtro_pais != nombre_pais:
            continue
        if filtro_pais_integrante != "Todos" and len(lista_integrantes) == 0:
            continue

        fila = [banda["nombre"]]
        linea = banda["nombre"]
        if usa_generos:
            fila.append(nombre_genero)
            linea = linea + " | " + nombre_genero
        if usa_paises:
            fila.append(nombre_pais)
            linea = linea + " | " + nombre_pais
        lineas.append(linea)

        if usa_integrantes:
            fila.append("\n".join(lista_integrantes))
            for texto in lista_integrantes:
                lineas.append("     " + texto)
        if usa_tablaturas:
            fila.append("\n".join(lista_tablaturas))
            for texto in lista_tablaturas:
                lineas.append("     " + texto)
        filas.append(fila)

    if len(filas) == 0:
        pantalla.avisar("Ninguna banda cumple con esos filtros.")
        return

    # 5) Lo mostramos en pantalla y lo guardamos en Excel
    nombre_archivo = guardarExcelCombinado(encabezados, filas)
    pantalla.mostrarLista("Reporte combinado", lineas)
    pantalla.avisar("Reporte descargado en: " + nombre_archivo)