import json

def login():
    with open("bandas.json", "r") as archivo:
        datos = json.load(archivo)

    correcto = False

    while not correcto:
        usuario = input("Ingresar el nombre de usuario: ")
        contraseña = input("Ingresar contraseña: ")

        for usuario_guardado in datos["usuarios"]:
            if usuario in usuario_guardado:
                if usuario_guardado[usuario] == contraseña:
                    correcto = True

        if correcto:
            print("Usuario y contraseña correctos")
        else:
            print("Usuario o contraseña incorrectos")

    return correcto

login()

