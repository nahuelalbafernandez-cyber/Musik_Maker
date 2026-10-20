import tkinter as tk
from tkinter import messagebox, simpledialog


# ==================== COLORES Y LETRAS ====================
COLOR_FONDO = "#1e1e2e"
COLOR_BOTON = "#313244"
COLOR_BOTON_ACTIVO = "#45475a"
COLOR_TEXTO = "#ffffff"
COLOR_ACENTO = "#f9a826"   # naranja para los títulos

LETRA_TITULO = ("Segoe UI", 22, "bold")
LETRA_SUBTITULO = ("Segoe UI", 11)
LETRA_BOTON = ("Segoe UI", 12)


# ==================== VENTANA PRINCIPAL ====================
# Hay una sola ventana en todo el programa. Los menús se dibujan adentro de ella.
ventana = tk.Tk()
ventana.title("Musik Maker")
ventana.geometry("420x560")
ventana.resizable(False, False)
ventana.configure(bg=COLOR_FONDO)


def limpiarVentana():
    """Borra todo lo que hay en la ventana para dibujar otro menú."""
    for elemento in ventana.winfo_children():
        elemento.destroy()


def titulo(texto):
    etiqueta = tk.Label(ventana, text=texto, font=LETRA_TITULO, bg=COLOR_FONDO, fg=COLOR_ACENTO)
    etiqueta.pack(pady=(40, 5))


def subtitulo(texto):
    etiqueta = tk.Label(ventana, text=texto, font=LETRA_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO)
    etiqueta.pack(pady=(0, 20))


def boton(texto, funcion):
    """Crea un botón ancho que ejecuta "funcion" cuando se hace clic."""
    nuevo_boton = tk.Button(
        ventana,
        text=texto,
        command=funcion,
        font=LETRA_BOTON,
        width=26,
        bg=COLOR_BOTON,
        fg=COLOR_TEXTO,
        activebackground=COLOR_BOTON_ACTIVO,
        activeforeground=COLOR_TEXTO,
        relief="flat",
        cursor="hand2"
    )
    nuevo_boton.pack(pady=6, ipady=6)


# ==================== VENTANITAS (reemplazan a input y print) ====================
def pedirTexto(titulo_ventana, pregunta, oculto=False):
    """Reemplaza a input(). Devuelve lo que escribió el usuario (sin espacios de más).
    Si tocó Cancelar devuelve None. Con oculto=True se ven asteriscos (para contraseñas)."""
    if oculto:
        respuesta = simpledialog.askstring(titulo_ventana, pregunta, show="*", parent=ventana)
    else:
        respuesta = simpledialog.askstring(titulo_ventana, pregunta, parent=ventana)

    if respuesta is None:
        return None
    return respuesta.strip()


def avisar(texto):
    """Reemplaza a print() para mensajes normales."""
    messagebox.showinfo("Musik Maker", texto, parent=ventana)


def error(texto):
    """Muestra un mensaje de error."""
    messagebox.showerror("Musik Maker", texto, parent=ventana)


def confirmar(pregunta):
    """Pregunta Sí / No. Devuelve True si tocó Sí."""
    return messagebox.askyesno("Musik Maker", pregunta, parent=ventana)


def mostrarLista(titulo_ventana, lineas):
    """Abre una ventanita con una lista de textos (ej: todas las bandas)."""
    ventanita = tk.Toplevel(ventana)
    ventanita.title(titulo_ventana)
    ventanita.geometry("480x380")
    ventanita.configure(bg=COLOR_FONDO)

    tk.Label(ventanita, text=titulo_ventana, font=("Segoe UI", 14, "bold"),
             bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(pady=10)

    lista = tk.Listbox(ventanita, font=LETRA_BOTON, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                       relief="flat", highlightthickness=0)
    for linea in lineas:
        lista.insert(tk.END, linea)
    lista.pack(fill="both", expand=True, padx=15)

    tk.Button(ventanita, text="Cerrar", command=ventanita.destroy, font=LETRA_BOTON,
              bg=COLOR_BOTON_ACTIVO, fg=COLOR_TEXTO, relief="flat").pack(pady=10)


def elegirDeLista(titulo_ventana, opciones):
    """Muestra una lista de textos para que el usuario elija uno.
    Devuelve el texto elegido, o None si cerró la ventana sin elegir."""
    ventanita = tk.Toplevel(ventana)
    ventanita.title(titulo_ventana)
    ventanita.geometry("420x380")
    ventanita.configure(bg=COLOR_FONDO)

    # Acá se guarda lo que eligió el usuario (empieza vacío)
    eleccion = tk.StringVar(value="")

    tk.Label(ventanita, text=titulo_ventana, font=("Segoe UI", 13, "bold"),
             bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(pady=10)

    lista = tk.Listbox(ventanita, font=LETRA_BOTON, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                       relief="flat", highlightthickness=0)
    for opcion in opciones:
        lista.insert(tk.END, opcion)
    lista.pack(fill="both", expand=True, padx=15)

    def aceptar():
        seleccion = lista.curselection()   # posición de lo que está marcado
        if len(seleccion) == 0:
            messagebox.showwarning("Musik Maker", "Elegí una opción de la lista.", parent=ventanita)
            return
        eleccion.set(lista.get(seleccion[0]))
        ventanita.destroy()

    tk.Button(ventanita, text="Elegir", command=aceptar, font=LETRA_BOTON,
              bg=COLOR_ACENTO, fg="#000000", relief="flat").pack(pady=10)

    # Doble clic en un elemento también sirve para elegir
    lista.bind("<Double-Button-1>", lambda evento: aceptar())

    # Esperamos a que el usuario elija o cierre la ventanita
    ventanita.grab_set()
    ventana.wait_window(ventanita)

    if eleccion.get() == "":
        return None
    return eleccion.get()
