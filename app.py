from flask import Flask
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = '3209139823928139'

#configurar carpeta donde se van a guardar las fotos de los productos
app.config["UPLOAD_FOLDER"]="./static/imagenes/"

#uri conexión local
uri="mongodb://localhost:27017/"
#uri remota (aquí cada uno obtiene de acuerdo a su base de datos remota)
#remplazan <db_username> Y <db_password> en la cadena obtenida
uri="mongodb+srv://santiagomera051:<santiagomera123>@cluster0.fdx1n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

miConexion = MongoClient(uri)


#crear base datos
baseDatos = miConexion["Nuevonegocio"]

#crear la colección
productos = baseDatos["Nuevos_productos"]

#crear la coleccion
usuarios = baseDatos["Nuevos_usuarios"]

if __name__=="__main__":
    from controladores.productoController import *
    from controladores.usuarioController import *
    app.run(port=5000, debug=True)