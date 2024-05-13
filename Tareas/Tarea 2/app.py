from flask import Flask, render_template
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
    regiones = get_regiones()
    comunas_por_region = {region:get_comunas(region) for region in regiones}
    return render_template('agregar-producto.html',regiones=regiones,comunas_por_region=comunas_por_region)


if __name__ == '__main__' :
    app.run(debug=True)