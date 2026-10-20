# Ejecutar desde la carpeta raíz del proyecto con:  python main.py

from Funciones import datos, pantalla, usuarios, bandas, tablaturas, reportes


# Usuario que inició sesión (None = nadie)
usuario_actual = None


# ==================== ACCIONES DE INICIO Y SESIÓN ====================
def iniciarSesion():
    global usuario_actual
    usuario = usuarios.login()
    if usuario is not None:
        usuario_actual = usuario
        mostrarMenu("principal")


def cerrarSesion():
    global usuario_actual
    usuario_actual = None
    pantalla.avisar("Sesión cerrada.")
    mostrarMenu("inicio")


def salir():
    pantalla.ventana.destroy()


# ==================== ACCIONES ====================
# En db_menus.json cada botón tiene una "accion" (un texto).
# Este diccionario dice qué función se ejecuta para cada texto.
ACCIONES = {
    "iniciar_sesion": iniciarSesion,
    "registrarse": usuarios.registro,
    "salir": salir,
    "cerrar_sesion": cerrarSesion,
    "buscar_banda": bandas.buscarBanda,
    "ver_bandas": bandas.mostrarBandas,
    "agregar_banda": bandas.agregarBanda,
    "editar_banda": bandas.editarBanda,
    "eliminar_banda": bandas.eliminarBanda,
    "ver_tablaturas": tablaturas.mostrarTablaturas,
    "agregar_tablatura": tablaturas.agregarTablatura,
    "reporte_bandas_por_pais": reportes.reporteBandasPorPais
}


# ==================== MENÚS DINÁMICOS ====================
def elegirOpcion(opcion):
    """Se ejecuta cuando se toca un botón del menú."""
    # Si la opción lleva a otro menú, lo mostramos
    if "submenu" in opcion:
        mostrarMenu(opcion["submenu"])
        return

    # Si no, buscamos la función de esa acción y la ejecutamos
    nombre_accion = opcion["accion"]
    if nombre_accion not in ACCIONES:
        pantalla.error("La acción \"" + nombre_accion + "\" no existe.")
        return
    funcion = ACCIONES[nombre_accion]
    funcion()


def crearBoton(opcion):
    """Crea el botón de una opción. Cada botón llama a elegirOpcion con SU opción."""
    pantalla.boton(opcion["texto"], lambda: elegirOpcion(opcion))


def mostrarMenu(nombre_menu):
    """Lee el menú desde db_menus.json y dibuja un botón por cada opción."""
    menus = datos.leerDatos("menus")
    menu = menus[nombre_menu]

    pantalla.limpiarVentana()
    pantalla.titulo(menu["titulo"])

    if usuario_actual is not None:
        pantalla.subtitulo("Usuario: " + usuario_actual)
    else:
        pantalla.subtitulo("Tu biblioteca de bandas y tablaturas")

    for opcion in menu["opciones"]:
        crearBoton(opcion)


# ==================== PROGRAMA PRINCIPAL ====================
mostrarMenu("inicio")
pantalla.ventana.mainloop()
