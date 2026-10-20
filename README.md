# Musik_Maker

## Resumen

La idea para nuestro proyecto se debe a nuestro gran gusto por la música, de ahí nace nuestro interés en combinar ambos gustos y armar este programa sobre organización musical.

Con esto el usuario va a poder crear su cuenta y poder buscar y seleccionar canciones de sus artistas favoritos, donde tendrá sus tablaturas e información de la canción y alojarlas en su perfil.

El problema que queremos resolver es tener una forma simple de organizar la información de nuestras canciones favoritas y así el usuario pueda tener todo lo que necesita de una canción en un mismo lugar. Algo muy útil para músicos o fanáticos que buscan aprender sobre sus artistas favoritos.

Nuestra motivación principal para este proyecto fue compartir gustos musicales.

## Estructura del proyecto

```
MusikMaker/
├── main.py              → archivo que se ejecuta, arma los menús
├── Funciones/           → todas las funciones del programa, un archivo por tema
│   ├── datos.py
│   ├── pantalla.py
│   ├── auxiliares.py
│   ├── usuarios.py
│   ├── bandas.py
│   ├── tablaturas.py
│   └── reportes.py
├── db/                  → base de datos, un archivo JSON por tabla
│   ├── db_bandas.json
│   ├── db_paises.json
│   ├── db_tablaturas.json
│   ├── db_usuarios.json
│   └── db_menus.json
└── Reportes/            → acá se guardan los Excel que genera el programa
```

## Módulos

Todas las funciones están centralizadas en la carpeta `Funciones`, separadas por tema:

- **datos.py**: Lee y guarda los archivos de la base de datos.
- **pantalla.py**: Todo lo de la interfaz gráfica con tkinter.
- **auxiliares.py**: Funciones que sirven para cualquier lista.
- **usuarios.py**: El registro y el login.
- **bandas.py**: Todo sobre las bandas.
- **tablaturas.py**: Todo sobre las tablaturas.
- **reportes.py**: Todo lo relacionado a generar reportes en excel.

## Base de datos

Las bases de datos están modularizadas por cada tema en la carpeta db.

## Menús dinámicos

Los menús no están escritos en el código, se leen desde `db_menus.json`. Cada menú tiene un título y una lista de opciones, y cada opción hace una de dos cosas:

- `"submenu"`: lleva a otro menú.
- `"accion"`: ejecuta una función del programa.

Los menús quedan organizados así:

- **Inicio**: Iniciar sesión, Registrarse, Salir.
- **Menú principal**: Bandas, Tablaturas, Reportes, Cerrar sesión.
  - **Bandas**: Buscar banda, Ver todas las bandas, Agregar banda, Editar banda, Eliminar banda, Volver.
  - **Tablaturas**: Ver tablaturas, Agregar tablatura, Volver.
  - **Reportes**: Bandas por país (Excel), Volver.

## Cómo ejecutarlo

Primero instalamos las librerías necesarias:

```
pip install -r requirements.txt
```

Después, parados en la carpeta principal del proyecto:

```
python main.py
```

## Qué se puede hacer por ahora

- Registrarse e iniciar sesión (con 3 intentos para la contraseña).
- Ver todas las bandas.
- Buscar una banda por nombre. No hace falta escribirla exacta, si ponés una parte del nombre o te equivocás en alguna letra igual te la encuentra.
- Agregar, editar y eliminar bandas. Al eliminar una banda también se borran sus tablaturas.
- Ver todas las tablaturas con su banda y su link.
- Agregar tablaturas.
- Descargar un reporte en Excel con las bandas de un país (se guarda en la carpeta Reportes).

## Integrantes
- Alba Fernández, Nahuel Uriel
- Rosas Sandillú, Julián Exequiel