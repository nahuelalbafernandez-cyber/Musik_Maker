from openpyxl import Workbook
from openpyxl.styles import Font

from Core import funciones as core


# ==================== REPORTES ====================
def reporteBandasPorPais():
    datos = core.leerDatos()
    print("\n--- REPORTE: BANDAS POR PAÍS ---")

    pais = core.elegirPorNombre(datos["paises"], "¿De qué país?: ")
    if pais is None:
        return

    # Juntamos las bandas de ese país
    bandas_del_pais = []
    for banda in datos["bandas"]:
        if banda["pais_id"] == pais["id"]:
            bandas_del_pais.append(banda)

    if len(bandas_del_pais) == 0:
        print("No hay bandas de " + pais["nombre"] + ".")
        return

    # Mostramos en pantalla
    print("Bandas de " + pais["nombre"] + ":")
    for banda in bandas_del_pais:
        print("- " + banda["nombre"])

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

    print("Reporte descargado en: " + nombre_archivo)