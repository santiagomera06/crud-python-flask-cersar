# **Aplicación Web en Python que realiza las tareas del CRUD a una base de datos MongoDB**

**Base de Datos**
Nombre de la base de datos 
**Nuevonegocio**
La base de datos contiene una colección principal llamada **Nuevos_productos** con los siguientes atributos:
- **codigo**: Entero y con indice único. Código del producto
- **nombre**: String, nombre del producto
- **precio**: Entero, precio del producto
- **categoria**: String, categoría del producto
- **foto**: String, contiene el nombre del archivo como se guarda en el servidor.

La otra colección es **Nuevos_usuarios** que contiene los usuarios permitidos para ingresar a la aplicación. Tiene los siguientes atributos:
- **username**: String, valor único.
- **password**: String, con la contraseña del usuario.

**Características:**
La aplicación utiliza el framework **Flask** y la librería **Pymongo** quien es la que me permite conectarme a la base de datos.
De acuerdo a lo anterior debemos instalar las librerías mencionadas.
- **pip install Flask pymongo**

El ejercicio realiza una conexión de manera local, si queremos conectarnos de manera remota debemos ingresar a mongo atlas crear la base de datos y obtener
la cadena de conexión de acuerdo a las indicaciones dadas en el mismo sitio.

