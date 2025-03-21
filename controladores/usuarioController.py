from flask import Flask, render_template, jsonify, request, redirect, session
import pymongo.errors  
from app import app, baseDatos, usuarios  
from werkzeug.utils import secure_filename  
import os 
import pymongo  
from bson.objectid import ObjectId 

@app.route("/")
def iniciar():
    """
    Función que maneja la ruta raíz ("/").
    
    Recibe la petición del cliente para mostrar la interfaz de inicio de sesión.
    
    Returns:
        Renderiza la plantilla "IniciarSesion.html" que contiene el formulario de inicio de sesión.
    """
    return render_template("IniciarSesion.html")

@app.route("/iniciarSesion", methods=['POST'])
def iniciarSesion():
    """
    Función que maneja el inicio de sesión de un usuario.
    
    Recibe las credenciales del usuario desde un formulario y verifica su autenticidad en la base de datos.
    
    Returns:
        - Redirecciona a la página de listado de productos si las credenciales son correctas.
        - Si las credenciales son incorrectas, vuelve a renderizar el formulario de inicio de sesión con un mensaje de error.
    """
    try:
        if request.method == "POST":
            # Obtiene el usuario y contraseña ingresados en el formulario
            username = request.form["txtUsername"]
            password = request.form["txtPassword"]
            
            # Busca en la base de datos un usuario con las credenciales proporcionadas
            usuario = usuarios.find_one({"username": username, "password": password})
            
            if usuario is not None:
                # Si el usuario existe, se almacena en la sesión y se redirige a la página de productos
                session['username'] = username
                return redirect("/listarProductos")
            else:
                # Si las credenciales son incorrectas, se muestra un mensaje de error
                mensaje = "Credenciales no válidas. Verifique"
                return render_template("IniciarSesion.html", mensaje=mensaje)
        else:
            # Si el método no es POST, se muestra un mensaje indicando que se debe usar el formulario
            mensaje = "Debe primero ingresar sus credenciales desde el formulario"
            return render_template("IniciarSesion.html", mensaje=mensaje)
    except pymongo.errors.PyMongoError as error:
        # Captura errores relacionados con la base de datos y los muestra como mensaje
        mensaje = str(error)
        return render_template("IniciarSesion.html", mensaje=mensaje)

@app.route("/salir", methods=['GET'])
def salir():
    """
    Función que maneja el cierre de sesión.
    
    Elimina las variables de sesión existentes y redirige al formulario de inicio de sesión.
    
    Returns:
        Renderiza el formulario de inicio de sesión con un mensaje de confirmación.
    """
    session.clear()  # Elimina todas las variables de sesión
    mensaje = "Ha cerrado la sesión de manera exitosa..."
    return render_template("IniciarSesion.html", mensaje=mensaje)
