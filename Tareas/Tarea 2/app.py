from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
import ast
import hashlib
import shutil
from werkzeug.utils import secure_filename
from utils.getters import get_producto, get_regiones, get_comunas, get_comuna_id, get_fruta_verdura_id
from utils.validation import validate, validate_conf_img
from utils.save_upload import save_uploads

current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script Python actual
source_dir = os.path.abspath(os.path.join(current_dir, 'static', 'preupload')) # Directorio de preuploads
destination_dir = os.path.abspath(os.path.join(current_dir, 'static', 'upload')) # Directorio de uploads

UPLOAD_FOLDER = 'static/uploads'


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Añade una clave secreta para las sesiones de Flask


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGHT'] = 16 * 1024 * 1024

# Conexion a base de datos
conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host='localhost',
    charset='utf8'
)
c = conn.cursor()

@app.errorhandler(413)
def request_entity_too_large(error):
    return "File exceeds the maximun file size allowed",413

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
            print(type(file))
            print(file.filename)
            if file and file.filename != '':
                fotos.append(file)
            else:
                fotos.append(None)
        
        # Datos para validar
        input_data = (name, productos_seleccionados,fotos, telefono, email)
        validation_result = validate(input_data)

        # Retorna True si son validos
        if validation_result is True:
            # Guarda las fotos porque al recargar la pagina se pierde la informacion del usuario, las fotos no se pueden recargar
            uploads = save_uploads(fotos)
            confirm_message = "Confirma el envío del formulario"
            # Guardar las fotos aqui
            
            return render_template('agregar-producto.html', 
                                   productos=productos, 
                                   regiones=regiones, 
                                   comunas_por_region=comunas_por_region, 
                                   confirm_message=confirm_message,
                                   error_message='',
                                   uploads=uploads,
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
                           form_data = request.form)


# Esta funcion va a enviar los archivos a la base de datos
@app.route('/',methods=['POST','GET'])
def submittingform():

    #Primero obtenemos los datos del formulario
    form = request.form
    
    tipo = form['tipo']
    productos = ast.literal_eval(form['producto_selector']) # Viene como str asi que lo formateamos a una lista
    uploads = ast.literal_eval(form['uploads']) # Viene como str asi que lo formateamos a una lista
    descripcion = form['descripcion']
    region = form['region_selector']
    comuna = form['comunas']
    name = form['name']
    email = form['email']
    telefono = form['phone']
    
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
    print("ESTAMOS MOVIENDO ARCHIVOS ")
    
    for file in uploads:
        print(file)
        # Ruta de la imagen + nombre del archivo
        source_file_path = os.path.join(source_dir,file)
        # Ruta de de destino de la imagen + nombre del archivo
        destination_file_path = os.path.join(destination_dir, file)
        
        # Chequeamos si existe el archivo con el nombre de la lista
        if os.path.exists(source_file_path):
            # Mueve el archivo
            shutil.move(source_file_path,destination_file_path)

        # Añadimos a la base de datos
        sql_foto = "INSERT INTO foto (ruta_archivo, nombre_archivo, producto_id) VALUES (%s,%s,%s)"
        path = os.path.join(app.config['UPLOAD_FOLDER'],file)
        c.execute(sql_foto,(path,file,producto_id))
        conn.commit()
        
    print("ESTAMOS ELIMINANDO ARCHIVOS")
    # Borramos todos los archivos, pues ya movimos los importantes
    for file in os.listdir(source_dir):
        # Ruta del archivo actual del directorio
        file_path = os.path.join(source_dir,file)
        # Si existe el archivo, lo elimina
        os.remove(file_path)
        


    
    
    
    '''
        # Añadimos a la base de datos
        sql_foto = "INSERT INTO foto (ruta_archivo, nombre_archivo, producto_id) VALUES (%s,%s,%s)"
        c.execute(sql_foto,(app.config['UPLOAD_FOLDER'],img_filename,producto_id))
        conn.commit()
        print(result)   
    '''
    
    return render_template('index.html')     
            
if __name__ == '__main__':
    app.run(debug=True)
