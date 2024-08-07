from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin
import pymysql
import os
import ast
import hashlib
import shutil
from PIL import Image
from werkzeug.utils import secure_filename
from utils.getters import *
from utils.validation import validate, validate_conf_img, validate_pedido
from utils.save_upload import *
from utils.submit import *


current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script Python actual
source_dir = os.path.abspath(os.path.join(current_dir, 'static', 'preupload')) # Directorio de preuploads
destination_dir = os.path.abspath(os.path.join(current_dir, 'static', 'upload')) # Directorio de uploads


UPLOAD_FOLDER = 'static/uploads'


app = Flask(__name__)
CORS(app)
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
@app.route('/submittingform-producto',methods=['POST','GET'])
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

    # QUERIES

    # INSERTAR EN LA TABLA PRODUCTO    
    #Primero obtenemos el id de la comuna
    comuna_id = get_comuna_id(comuna)
    #insertar producto
    sql_producto = "INSERT INTO producto (tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor) VALUES (%s,%s,%s,%s,%s,%s)"
    c.execute(sql_producto,(tipo,descripcion,comuna_id,name,email,telefono))
    conn.commit()



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

    
    # INSERTAR EN LA TABLA FOTO
    
    for file in uploads:
        # Si se enviaron menos de 3 archivos alguno sea nulo
        if file is None:
            continue
        # Ruta de la imagen + nombre del archivo
        source_file_path = os.path.join(source_dir,file)
        # Ruta de de destino de la imagen + nombre del archivo
        destination_file_path = os.path.join(destination_dir, file)
        # Chequeamos si existe el archivo con el nombre de la lista
        if os.path.exists(source_file_path):
            # Mueve el archivo
            shutil.move(source_file_path,destination_file_path)

        # Añadimos a la base de datos
        imagen = Image.open(destination_file_path)
        # Guardamos las imagenes en los 3 tamaños
        resize(imagen,file)
        # Guarda las imagenes en 2 tamanos en Java
        save_java(imagen,file)
        sql_foto = "INSERT INTO foto (ruta_archivo, nombre_archivo, producto_id) VALUES (%s,%s,%s)"
        path = os.path.join(app.config['UPLOAD_FOLDER'],file)
        c.execute(sql_foto,(path,file,producto_id))
        conn.commit()
        
    # Borramos todos los archivos, pues ya movimos los importantes
    for file in os.listdir(source_dir):
        # Ruta del archivo actual del directorio
        file_path = os.path.join(source_dir,file)
        # Si existe el archivo, lo elimina
        os.remove(file_path)
        
    return render_template('index.html')     


@app.route('/ver_productos/<int:newPage>',methods=['GET'])
def ver_productos(newPage):
    # Seteamos los limites de los elementos de acuerdo al numero de la pagina
    limit_inf = ( newPage - 1 ) * 5
    limit_sup = newPage * 5
    # Cada vez que se llama a esta funcion tenemos que pedir 5 productos para mostrar en pantalla
    productos = get_last_products(limit_inf,limit_sup) # Esta es una tupla con las 5 ultimas filas de la tabla producto
    productos_length = len(productos)
    # Precalculamos la siguiente lista de productos, si la lista esta vacia entonces le avisamos al template 
    # De esta manera no habra boton de siguiente pagina
    ThisIsTheLastPage = False
    productos_2 = get_last_products(limit_inf+5,limit_sup+5)
    if productos_2 == ():
        ThisIsTheLastPage = True
    
    # Listas que llenaremos
    lista_productos = []
    comunas = []
    regiones = []
    uploads = []
    # File routes
    small = []
    medium = []
    large = []
    
    # Iteramos sobre los 5 productos (envios de productores)
    for x in productos :
        # el [0] entrega el id, asi que iteraremos por ellos
        # es una lista con listas de productos
        list = get_productos(x[0])
        lista_productos.append(list)
        
        # Obtenemos la comuna y la region
        comuna,region = get_comuna_region(x[3])
        comunas.append(comuna)
        regiones.append(region)
        # Obtenemos las rutas a las imagenes de cada envio de productor
        route = get_files(x[0])[0]
        uploads.append(route)
        small.append('small/'+route)
        medium.append('medium/'+route)
        large.append('large/'+route)


    return render_template('ver-productos.html',productos=productos,lista_productos=lista_productos,comunas=comunas,regiones=regiones,uploads=uploads,
                           small=small,medium=medium,large=large,newPage=newPage,ThisIsTheLastPage=ThisIsTheLastPage,productos_length=productos_length)


# Esta funcion es llamada cuando se clikea una fila relacionada a un producto
# Despliega la informacion completa del producto
@app.route('/detalle_producto/<int:producto_id>')
def detalle_producto(producto_id):
    
    # Obtener datos del producto
    sql = "SELECT id, tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor FROM producto WHERE id=%s"
    c.execute(sql,(producto_id,))
    producto = c.fetchone()
    
    lista_productos = get_productos(producto_id)
    comuna, region = get_comuna_region(producto[3])
    
    # Obtenemos su foto
    filename = get_files(producto_id)[0]
    path = 'medium/'+filename
    path_large = 'large/'+filename
    return render_template('informacion-producto.html', producto_id=producto_id,producto=producto,lista_productos=lista_productos,comuna=comuna,region=region,path=path,path_large=path_large)

# Esta funcion carga el template de agregar-pedido 
# El formulario es identico a agregar-producto pero sin imagenes
@app.route('/agregar-pedido', methods=['GET', 'POST'])
def agregar_pedido():
    
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

        # Datos para validar
        input_data = (name, productos_seleccionados, telefono, email)
        validation_result = validate_pedido(input_data)

        # Retorna True si son validos
        if validation_result is True:
            
            confirm_message = "Confirma el envío del formulario"
            # Guardar las fotos aqui
            
            return render_template('agregar-pedido.html', 
                                   productos=productos, 
                                   regiones=regiones, 
                                   comunas_por_region=comunas_por_region, 
                                   confirm_message=confirm_message,
                                   error_message='',
                                   productos_seleccionados=productos_seleccionados,
                                   form_data=request.form)
            
        
        return render_template('agregar-pedido.html', 
                               productos=productos, 
                               regiones=regiones, 
                               comunas_por_region=comunas_por_region, 
                               error_message=validation_result,
                               productos_seleccionados=productos_seleccionados,
                               form_data=request.form)
    
    return render_template('agregar-pedido.html', 
                           productos=productos, 
                           regiones=regiones, 
                           comunas_por_region=comunas_por_region,
                           error_message='',
                           productos_seleccionados=[],
                           form_data = request.form)


# Esta funcion va a enviar los archivos a la base de datos
@app.route('/submittingform-pedido',methods=['POST','GET'])
def submittingform_pedido():

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

    # QUERIES

    # INSERTAR EN LA TABLA PEDIDO
     
    #Primero obtenemos el id de la comuna
    comuna_id = get_comuna_id(comuna)
    
    #INSERTAR PEDIDO
    submitPedido(tipo,descripcion,comuna_id,name,email,telefono)

    # INSERTAR EN LA TABLA PEDIDO_FRUTA_VERDURA
    # En esta tabla insertamos la lista de productos, y necesitamos el id del pedido de la tabla producto primero
    # Obtenemos el pedido_id    
    pedido_id = get_last_id()
    
    # Iteramos sobre la lista, cada producto implica una entrada en la tabla producto_fruta_verdura
    for producto in productos :   
        # Obtenemos la id de cada producto
        id = get_fruta_verdura_id(producto)
        submitPedido_Verdura_Fruta(pedido_id,id)
        
    return render_template('index.html')     



@app.route('/ver_pedidos/<int:newPage>',methods=['GET'])
def ver_pedidos(newPage):
    # Seteamos los limites de los elementos de acuerdo al numero de la pagina
    limit_inf = ( newPage - 1 ) * 5
    limit_sup = newPage * 5
    # Cada vez que se llama a esta funcion tenemos que pedir 5 productos para mostrar en pantalla
    pedidos = get_last_pedidos(limit_inf,limit_sup) # Esta es una tupla con las 5 ultimas filas de la tabla producto
    pedidos_length = len(pedidos)
    
    # Precalculamos la siguiente lista de productos, si la lista esta vacia entonces le avisamos al template 
    # De esta manera no habra boton de siguiente pagina
    ThisIsTheLastPage = False
    pedidos_2 = get_last_pedidos(limit_inf+5,limit_sup+5)
    if pedidos_2 == ():
        ThisIsTheLastPage = True
    
    # En estas listas se guardaran productos de cada pedido, comuna y region, respectivamente
    lista_productos = []
    comunas = []
    regiones = []
    
    # Iteramos sobre los 5 pedidos 
    for x in pedidos :
        # el [0] entrega el id, asi que iteraremos por ellos
        # es una lista con listas de productos
        list = get_productos_from_pedido(x[0])
        lista_productos.append(list)
        
        # Obtenemos la comuna y la region
        comuna,region = get_comuna_region(x[3])
        comunas.append(comuna)
        regiones.append(region)


    return render_template('ver-pedidos.html',pedidos=pedidos,lista_productos=lista_productos,comunas=comunas,regiones=regiones,
                           newPage=newPage,ThisIsTheLastPage=ThisIsTheLastPage,pedidos_length=pedidos_length)


@app.route('/detalle_pedido/<int:pedido_id>')
def detalle_pedido(pedido_id):
    
    # Obtener datos del producto
    sql = "SELECT id, tipo, descripcion, comuna_id, nombre_comprador, email_comprador, celular_comprador FROM pedido WHERE id=%s"
    c.execute(sql,(pedido_id,))
    pedido = c.fetchone()
    
    lista_productos = get_productos_from_pedido(pedido_id)
    comuna, region = get_comuna_region(pedido[3])
    
    return render_template('informacion-pedido.html', pedido_id=pedido_id,pedido=pedido,lista_productos=lista_productos,comuna=comuna,region=region)


@app.route('/stats')
def stats():
    
    return render_template('stats.html')
    


@app.route("/get-stats-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_stats_data():
    
    # Obtenemos la info para los graficos
    products_data = get_data_1()
    cities_data = get_data_2()

    
    return jsonify({
        "products_data": products_data,
        "cities_data": cities_data
    })
    
 
if __name__ == '__main__':
    app.run(debug=True,port=8007)
