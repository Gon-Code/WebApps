from flask import Flask, render_template, request, redirect, url_for
import pymysql 
from utils.getters import *

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

'''
@app.route('/agregar-producto', methods=['POST','GET'])
def agregar_producto():
    error = None

    return render_template('agregar-producto.html')
'''
@app.route('/agregar-producto')
def agregar_producto():
    # Obtenemos los productos
    productos = get_producto()

    # Obtenemos regiones y comunas
    regiones = get_regiones()
    comunas_por_region = {region:get_comunas(region) for region in regiones}
    return render_template('agregar-producto.html',productos=productos,regiones=regiones,comunas_por_region=comunas_por_region)


# Esta funcion agrega los productos a la base de datos
@app.route('/enviando-producto',methods=['POST','GET'])
def add_producto():

    # Obtenemos los datos ingresados por el usuario 
    tipo = request.form['tipo']
    productos = request.form.getlist('producto_selector')
    descripcion = request.form['descripcion']
    # Falta la imagen
    region = request.form['region_selector']
    comuna = request.form['comunas']
    email = request.form['email']
    telefono = request.form['phone']

    print(tipo)
    print(productos)
    print(descripcion)
    print(region)
    print(comuna)
    print(email)
    print(telefono)
    
    return "hola mundo , fin del envio del formulario "

if __name__ == '__main__' :
    app.run(debug=True)