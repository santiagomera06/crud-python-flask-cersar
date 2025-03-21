from flask import Flask, render_template, jsonify, request, redirect, session
import pymongo.errors
from app import app, baseDatos, productos 
from werkzeug.utils import secure_filename 
import os
import pymongo
from bson.objectid import ObjectId

@app.route("/listarProductos", methods=['GET'])
def inicio():
    try:
        #validacion al iniciar secion 
        if  "username" in session:
            listaProductos = productos.find()
            return render_template("listarProductos.html", listaProductos=listaProductos) 
        else:
            mensaje="Debe primero iniciar la sesión"
            return render_template("frmIniciarSesion.html", mensaje=mensaje)
        
    except pymongo.errors as error:
        mensaje=str(error)
        return render_template("listarProductos.html", mensaje=mensaje) 
    

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    try:
        # validacion al crear el incio de secion
        if "username" in session:
            if request.method=="GET":
                producto=None
                return render_template("frmAgregar.html", producto=producto)            
                
            elif(request.method=="POST"):
                codigo = int(request.form['txtCodigo'])
                nombre = request.form['txtNombre']
                precio = int(request.form['txtPrecio'])
                categoria = request.form['cbCategoria']        
                foto = request.files['fileFoto']
                nombreArchivo = secure_filename(foto.filename)
                listaNombreArchivo = nombreArchivo.rsplit('.', 1)
                extension = listaNombreArchivo[1].lower()
                nombreFotoServidor = f"{str(codigo)}.{extension}"
                producto = {
                    "codigo": codigo,
                    "nombre":nombre,
                    "precio":precio,
                    "categoria":categoria,
                    "foto":nombreFotoServidor
                }            
                resultado = productos.insert_one(producto)
                if(resultado.acknowledged):
                    #subir la foto al servidor
                    rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                    foto.save(rutaFoto)                
                    return redirect("/listarProductos")  
        else:
            mensaje="Debe primero iniciar la sesión"
            return render_template("frmIniciarSesion.html", mensaje=mensaje)    
    except pymongo.errors.PyMongoError as error:
       
        mensaje="Ya existe producto con ese código. Modificar"
        return render_template("frmAgregar.html", mensaje=mensaje, producto=producto)
        
        
@app.route("/editar/<string:id>", methods=['GET', 'POST'])
def editar(id):
    try:
        #validacion de sesión creada al iniciar la sesión
        if "username" in session:
            id = ObjectId(id)
            productoAEditar = {"_id": id}
            if request.method=="GET":          
                #consultar los productos por su id
                producto = productos.find_one(productoAEditar)
                if(producto):
                    return render_template("frmEditar.html", producto=producto)
            elif(request.method=="POST"):
                codigo = int(request.form['txtCodigo'])
                nombre = request.form['txtNombre']
                precio = int(request.form['txtPrecio'])
                categoria = request.form['cbCategoria']        
                foto = request.files['fileFoto']
                nombreArchivo = secure_filename(foto.filename)             
                producto = {
                    "_id": str(id),
                    "codigo":codigo,
                    "nombre":nombre,
                    "precio":precio
                }
                
                if nombreArchivo=="":
                    atributosActualizar={
                        "codigo":codigo,
                        "nombre":nombre,
                        "precio":precio,
                        "categoria":categoria
                    }
                    #actualizar el producto cuando no envían foto
                    resultado = productos.update_one(productoAEditar,{'$set': atributosActualizar})
                    if (resultado.modified_count==1):
                        return redirect("/listarProductos")
                else:
                    listaNombreArchivo = nombreArchivo.rsplit('.', 1)
                    extension = listaNombreArchivo[1].lower()
                    nombreFotoServidor = f"{str(codigo)}.{extension}"
                    atributosActualizar={
                        "codigo":codigo,
                        "nombre":nombre,
                        "precio":precio,
                        "categoria":categoria,
                        "foto": nombreFotoServidor
                    }
                    resultado = productos.update_one(productoAEditar,{'$set': atributosActualizar})
                    if (resultado.modified_count==1):
                        #subir la foto
                        rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                        foto.save(rutaFoto)                
                        return redirect("/listarProductos")    
        else:
            mensaje="Debe primero iniciar la sesión"
            return render_template("frmIniciarSesion.html", mensaje=mensaje)           
    except pymongo.errors.PyMongoError as error:
        mensaje=str(error)
        mensaje="Ya existe producto con ese código. Modificar"
        if nombreArchivo=="":
    
            #condulta del producto el cual nos devolveria a la vista para que nos muestre la consulta 
            foto = productos.find_one(productoAEditar)['foto']
            #agregamos al producto el atributo foto
            producto['foto']=foto
        return render_template("frmEditar.html", mensaje=mensaje, producto=producto)
    
@app.route("/eliminar/<string:id>", methods=["GET"])
def eliminar(id):
    """_summary_
        Elimina un producto de acuerdo a su id
    Args:
        id (_type_): ObjectId

    Returns:
        _type_: Redirecciona la vista de listarProductos
    """
    if "username" in session:
        listaProductos=productos.find()
        try:
            if request.method=="GET":
                id=ObjectId(id)
                resultado = productos.delete_one({"_id":id})
                if resultado.deleted_count==1:
                    return redirect("/listarProductos")  
        except pymongo.errors.PyMongoError as error:
            mensaje=str(error)
            mensaje="Problemas de conexión al servidor."       
            return render_template("listarProductos.html", mensaje=mensaje,
                                    listaProductos=listaProductos)
    else:
        mensaje="Debe primero iniciar la sesión"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)    