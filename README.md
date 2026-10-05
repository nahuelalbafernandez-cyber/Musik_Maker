# Musik_Maker

## Resumen

La idea para nuestro proyecto se debe a nuestro gran gusto por la música, de ahí nace nuestro interés en combinar ambos gustos y armar este programa sobre organización musical.

Con esto el usuario va a poder crear su cuenta y poder buscar y seleccionar canciones de sus artistas favoritos, donde tendrá sus tablaturas e información de la canción y alojarlas en su perfil.

El problema que queremos resolver es tener una forma simple de organizar la información de nuestras canciones favoritas y así el usuario pueda tener todo lo que necesita de una canción en un mismo lugar. Algo muy útil para músicos o fanáticos que buscan aprender sobre sus artistas favoritos.

Nuestra motivación principal para este proyecto fue compartir gustos musicales.

## Módulos

El programa está dividido en varios módulos:

- CORE: es el núcleo del proyecto. Tiene el main.py, que es el archivo que se ejecuta y donde están los menús, y el funciones.py con las funciones principales que usa todo el programa (leer y guardar los datos, el buscador, etc). También está el base_de_datos.json, que funciona como base de datos con las bandas, los países y los usuarios.
- REGISTRATION: tiene la lógica del registro y el login del usuario. Cuando alguien se registra se guarda directamente en el base_de_datos.json y al loguearse se chequea contra eso.
- ABMS: tiene el alta, baja y modificación de las bandas. Cada banda tiene su nombre y el país de donde es.
- REPORTES: tiene todo lo relacionado a generar reportes. Por ahora se puede descargar un Excel con todas las bandas de un país.

## Cómo ejecutarlo

Primero instalamos las librerías necesarias:

```
pip install -r requirements.txt
```

Después, parados en la carpeta principal del proyecto:

```
python -m Core.main
```

## Qué se puede hacer por ahora

- Registrarse e iniciar sesión.
- Ver todas las bandas.
- Buscar una banda por nombre. No hace falta escribirla exacta, si ponés una parte del nombre o te equivocás en alguna letra igual te la encuentra.
- Agregar, editar y eliminar bandas.
- Descargar un reporte en Excel con las bandas de un país (se guarda en la carpeta Reportes).

## Integrantes
- Alba Fernández, Nahuel Uriel
- Rosas Sandillú, Julián Exequiel