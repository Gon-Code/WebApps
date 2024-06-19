import pymysql
from PIL import Image

# En este archivo creamos queries para insertar productos y pedidos

# Conexion a base de datos
conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host = 'localhost',
    charset = 'utf8'
)

c = conn.cursor()


# Inserta un pedido en la tabla pedido
def submitPedido(tipo,descripcion,comuna_id,nombre,email,telefono):
    
    sql = "INSERT INTO pedido (tipo, descripcion, comuna_id, nombre_comprador, email_comprador, celular_comprador) VALUES (%s,%s,%s,%s,%s,%s)"
    c.execute(sql,(tipo,descripcion,comuna_id,nombre,email,telefono))
    conn.commit()
        
    
    return

# Inserta los productos de un pedido en la tabala pedido_verdura_fruta
def submitPedido_Verdura_Fruta(pedido_id,tipo_verdura_fruta_id):
    
    sql = "INSERT INTO pedido_verdura_fruta (tipo_verdura_fruta_id, pedido_id) VALUES (%s,%s)"
    c.execute(sql,(tipo_verdura_fruta_id,pedido_id))
    conn.commit()
    
    return

# Entrega el ultimo id insertado
def get_last_id():
    
    sql = "SELECT LAST_INSERT_ID()"
    c.execute(sql)
    resultado = c.fetchone()
    
    return resultado