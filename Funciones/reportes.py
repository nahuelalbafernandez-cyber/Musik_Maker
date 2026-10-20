from openpyxl import Workbook
from openpyxl.styles import Font

from Funciones import datos, pantalla, auxiliares


# ==================== REPORTES ====================
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
