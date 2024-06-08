from flask import Flask, render_template, request, redirect, url_for, flash

import pymysql
import os
import ast
from utils.getters import get_producto, get_regiones, get_comunas, get_comuna_id, get_fruta_verdura_id
from utils.validation import validate

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Añade una clave secreta para las sesiones de Flask

# Conexion a base de datos
conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host='localhost',
    charset='utf8'
)
c = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ver-productos')
def ver_productos():
    return render_template('ver-productos.html')

@app.route('/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    
    productos = get_producto()
    regiones = get_regiones()
    comunas_por_region = {region: get_comunas(region) for region in regiones}
    
    if request.method == 'POST':
        # Obtiene los datos ingresados por el usuario
        tipo = request.form['tipo']
        productos_seleccionados = request.form.getlist('producto_selector')
        descripcion = request.form['descripcion']
        region = request.form['region_selector']
        comuna = request.form['comunas']
        name = request.form['name']
        email = request.form['email']
        telefono = request.form['phone']

        # Manejar archivos subidos
        fotos = []
        for i in range(1, 4):
            file = request.files.get(f'myfile{i}')
            if file and file.filename != '':
                # Lee el archivo en binario
                file_data = file.read()
                fotos.append(file_data)
            else:
                fotos.append(None)
                
        # Datos para validar
        input_data = (name, productos_seleccionados, telefono, email)
        validation_result = validate(input_data)

        # Retorna True si son validos
        if validation_result is True:
            confirm_message = "Confirma el envío del formulario"
            return render_template('agregar-producto.html', 
                                   productos=productos, 
                                   regiones=regiones, 
                                   comunas_por_region=comunas_por_region, 
                                   confirm_message=confirm_message,
                                   error_message='',
                                   productos_seleccionados=productos_seleccionados,
                                   form_data=request.form)
            
        
        return render_template('agregar-producto.html', 
                               productos=productos, 
                               regiones=regiones, 
                               comunas_por_region=comunas_por_region, 
                               error_message=validation_result,
                               productos_seleccionados=productos_seleccionados,
                               form_data=request.form)
    
    return render_template('agregar-producto.html', 
                           productos=productos, 
                           regiones=regiones, 
                           comunas_por_region=comunas_por_region,
                           error_message='',
                           productos_seleccionados=[],
                           form_data =request.form)


# Esta funcion va a enviar los archivos a la base de datos
@app.route('/',methods=['POST'])
def submittingform():
    
    #Primero obtenemos los datos del formulario
    form = request.form
    tipo = form['tipo']
    productos = ast.literal_eval(form['producto_selector']) # Viene como str asi que lo formateamos a una lista
    descripcion = form['descripcion']
    region = form['region_selector']
    comuna = form['comunas']
    name = form['name']
    email = form['email']
    telefono = form['phone']
    
    '''
    # Manejar archivos subidos
    fotos = [] # Almacena los archivos
    for i in range(1, 4):
        file = request.files.get(f'myfile{i}')
        if file and file.filename != '':
            # Obtener el nombre del archivo
            filename = secure_filename(file.filename)
            # Guardar el archivo en la carpeta 'img'
            file_path = os.path.join(app.config['img/small'], filename)
            file.save(file_path) # Guarda las fotos
            fotos.append(file_path) # Lista con las rutas de las fotos
        else:
            fotos.append(None) 
    '''
    print(tipo)
    print(productos)
    print(descripcion)
    print(region)
    print(comuna)
    print(name)
    print(email)
    print(telefono)
    
    # QUERIES

    # INSERTAR EN LA TABLA PRODUCTO    
    #Primero obtenemos el id de la comuna
    comuna_id = get_comuna_id(comuna)
    #insertar producto
    sql_producto = "INSERT INTO producto (tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor) VALUES (%s,%s,%s,%s,%s,%s)"
    c.execute(sql_producto,(tipo,descripcion,comuna_id,name,email,telefono))
    conn.commit()
    print("PRODUCTO INSERTADO")


    # INSERTAR EN LA TABLA PRODUCTO_FRUTA_VERDURA
    # En esta tabla insertamos la lista de productos, y necesitamos el id del producto de la tabla producto primero
    # Obtenemos el producto_id
    
    sql_id_producto = "SELECT LAST_INSERT_ID()"   
    c.execute(sql_id_producto) 
    producto_id = c.fetchone()

    # Iteramos sobre la lista, cada producto implica una entrada en la tabla producto_fruta_verdura
    for producto in productos :   
        # Obtenemos la id de cada producto
        id = get_fruta_verdura_id(producto)
        sql_fruta_verdura = "INSERT INTO producto_verdura_fruta (producto_id, tipo_verdura_fruta_id) VALUES (%s,%s)"
        c.execute(sql_fruta_verdura,(producto_id,id))
        conn.commit()
        print("PRODUCTOS INSERTADOS")
        print(f"LAST ID : {producto_id}")
        print(f"ID DEL PRODUCTO : {id} Nombre del producto : {producto}")
        
    print("Todos los productos fueron insertados")
    
    # INSERTAR EN LA TABLA FOTO
    
    return render_template('index.html')     
            
if __name__ == '__main__':
    app.run(debug=True)
