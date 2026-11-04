# Musik_Maker

## Resumen

La idea para nuestro proyecto se debe a nuestro gran gusto por la música, de ahí nace nuestro interés en combinarlo con la programación y armar este programa sobre organización musical.

Con esto el usuario va a poder crear su cuenta, buscar bandas y guardar sus favoritas. De cada banda el programa guarda su país, su género, sus integrantes y sus tablaturas.

El problema que queremos resolver es tener una forma simple de organizar la información de nuestros artistas favoritos, para que el usuario tenga todo en un mismo lugar: quién toca en cada banda, de dónde es y los links a las tablaturas de sus canciones. También puede armar reportes en Excel combinando esa información. Algo muy útil para músicos o fanáticos.

Nuestra motivación principal para este proyecto fue compartir gustos musicales.

## Estructura del proyecto

```
MusikMaker/
├── main.py              → archivo que se ejecuta, arma los menús
├── db/                  → base de datos, un archivo JSON por tabla
│   ├── db_bandas.json
│   ├── db_generos.json
│   ├── db_integrantes.json
│   └── db_menus.json
│   ├── db_paises.json
│   ├── db_tablaturas.json
│   ├── db_usuarios.json
├── Funciones/           → todas las funciones del programa, un archivo por tema
│   ├── auxiliares.py
│   ├── bandas.py
│   ├── datos.py
│   ├── favoritas.py
│   ├── generos.py
│   ├── integrantes.py
│   ├── paises.py
│   ├── pantalla.py
│   └── reportes.py
│   ├── tablaturas.py
│   ├── usuarios.py
└── Reportes/            → acá se guardan los Excel que genera el programa
```

## Módulos

Todas las funciones están centralizadas en la carpeta `Funciones`, separadas por tema:

- **datos.py**: Lee y guarda los archivos de la base de datos.
- **pantalla.py**: Todo lo de la interfaz gráfica con tkinter.
- **auxiliares.py**: Funciones que sirven para cualquier lista.
- **usuarios.py**: El registro y el login.
- **bandas.py**: Todo sobre las bandas.
- **favoritas.py**: Las bandas favoritas de cada usuario.
- **generos.py**: Todo sobre los géneros de música.
- **paises.py**: Todo sobre los países.
- **integrantes.py**: Todo sobre los integrantes de las bandas.
- **tablaturas.py**: Todo sobre las tablaturas.
- **reportes.py**: Todo lo relacionado a generar reportes en excel.

## Base de datos

Las bases de datos están modularizadas por cada tema en la carpeta db.
Las tablas se relacionan guardando el id de la otra tabla:

- Cada **banda** tiene un país (`pais_id`) y un género (`genero_id`).
- Cada **integrante** pertenece a una banda (`banda_id`) y tiene un país (`pais_id`).
- Cada **tablatura** pertenece a una banda (`banda_id`).
- Cada **usuario** guarda los id de sus bandas favoritas (`bandas_favoritas`).

## Menús dinámicos

Los menús no están escritos en el código, se leen desde `db_menus.json`. Cada menú tiene un título y una lista de opciones, y cada opción hace una de dos cosas:

- `"submenu"`: lleva a otro menú.
- `"accion"`: ejecuta una función del programa.

Los menús quedan organizados así:

- **Inicio**: Iniciar sesión, Registrarse, Salir.
- **Menú principal**: Bandas, Mis favoritas, Géneros, Países, Integrantes, Tablaturas, Reportes, Cerrar sesión.
  - **Bandas**: Buscar banda, Ver todas las bandas, Agregar banda, Editar banda, Eliminar banda, Volver.
  - **Mis favoritas**: Ver mis favoritas, Agregar favorita, Quitar favorita, Volver.
  - **Géneros**: Ver todos los géneros, Agregar género, Editar género, Eliminar género, Volver.
  - **Países**: Ver todos los países, Agregar país, Editar país, Eliminar país, Volver.
  - **Integrantes**: Ver todos los integrantes, Agregar integrante, Editar integrante, Eliminar integrante, Volver.
  - **Tablaturas**: Ver tablaturas, Agregar tablatura, Editar tablatura, Eliminar tablatura, Volver.
  - **Reportes**: Bandas por país (Excel), Reporte combinado (Excel), Volver.

## Cómo ejecutarlo

Primero instalamos las librerías necesarias:

```
pip install -r requirements.txt
```

Después, parados en la carpeta principal del proyecto:

```
python main.py
```

## Qué se puede hacer

- Registrarse e iniciar sesión (con 3 intentos para la contraseña).
- Ver todas las bandas con su país y su género.
- Buscar una banda por nombre. No hace falta escribirla exacta, si ponés una parte del nombre o te equivocás en alguna letra igual te la encuentra.
- Agregar, editar y eliminar bandas.
- Marcar bandas como favoritas. Cada usuario tiene las suyas y puede verlas, agregar y quitar.
- Ver, agregar, editar y eliminar géneros de música.
- Ver, agregar, editar y eliminar países.
- Ver, agregar, editar y eliminar integrantes.
- Ver, agregar, editar y eliminar tablaturas.
- Descargar un reporte en Excel con las bandas de un país (se guarda en la carpeta Reportes).
- Armar un reporte combinado: se elige qué sumarle a las bandas (géneros, países, integrantes y tablaturas, en cualquier combinación), se puede filtrar por lo elegido, y el resultado se ve en pantalla y se guarda en Excel en la carpeta Reportes.

## Integrantes
- Alba Fernández, Nahuel Uriel
- Rosas Sandillú, Julián Exequiel