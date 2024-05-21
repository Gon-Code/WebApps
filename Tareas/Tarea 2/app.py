from flask import Flask, render_template, request, redirect, url_for
import pymysql 
from utils.getters import *
from utils.validation import *


app = Flask(__name__)

# Conexion a base de datos

conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host = 'localhost',
    charset = 'utf8'
)

c = conn.cursor()

## ESTO ESTA POR REVISAR

#app.secret_key = "s3cr3t_k3y"

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ver-productos')
def ver_productos():
    return render_template('ver-productos.html')


# En la función agregar_producto
@app.route('/agregar-producto')
def agregar_producto():
    # Obtener los productos y demás datos
    productos = get_producto()
    regiones = get_regiones()
    comunas_por_region = {region: get_comunas(region) for region in regiones}
    
    # Pasar los mensajes de confirmación y error al renderizar la plantilla
    confirm_message = request.args.get('confirm_message')
    error_message = request.args.get('error_message')
    
    return render_template('agregar-producto.html', confirm_message=confirm_message, error_message=error_message, productos=productos, regiones=regiones, comunas_por_region=comunas_por_region)


# Esta funcion agrega los productos a la base de datos
@app.route('/enviando-producto',methods=['POST'])
def add_producto():

    # Obtenemos los datos ingresados por el usuario 
    tipo = request.form['tipo']
    productos = request.form.getlist('producto_selector')
    descripcion = request.form['descripcion']
    # Falta la imagen
    region = request.form['region_selector']
    comuna = request.form['comunas']
    name = request.form['name']
    email = request.form['email']
    telefono = request.form['phone']

    # Debuggin 
    print(tipo)
    print(productos)
    print(descripcion)
    print(region)
    print(comuna)
    print(name)
    print(email)
    print(telefono)

    # Validamos el formulario
    input = (name, productos, telefono, email)
    
    # Obtenemos nuevamente los productos y las regiones para pasarlos al template
    productos = get_producto()
    regiones = get_regiones()
    comunas_por_region = {region: get_comunas(region) for region in regiones}

    if validate(input) == True :

        confirm_message = "Confirma el envío del formulario"
        return render_template('agregar-producto.html', productos=productos, regiones=regiones, comunas_por_region=comunas_por_region, confirm_message=confirm_message)

    # Si la validación es exitosa, mostrar el modal con el mensaje de confirmación

    return render_template('agregar-producto.html', productos=productos, regiones=regiones, comunas_por_region=comunas_por_region, error_message=validate(input))



    
if __name__ == '__main__' :
    app.run(debug=True)