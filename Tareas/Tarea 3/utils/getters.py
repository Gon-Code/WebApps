import pymysql
from PIL import Image

# En este archivo creamos algunas funciones para obtener los productos y las comunas
# Conexion a base de datos

conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host = 'localhost',
    charset = 'utf8'
)

c = conn.cursor()

# get_producto entrega un diccionaro con 2 llaves, fruta y verdura
# Cada llave tiene una lista con todos sus productos correspondientes 
def get_producto():

    
    dict = { "fruta" : [],
              "verdura" : []
              }

    # Obtenemos las frutas y las guardamos
    sql_frutas = "SELECT nombre FROM tipo_verdura_fruta WHERE id BETWEEN 1 AND 37 ORDER BY nombre ASC"
    c.execute(sql_frutas)
    resultado_frutas = c.fetchall()
    lista_frutas = [x[0] for x in resultado_frutas]

    dict["fruta"] = lista_frutas

    # Obtenemos las verduras y las guardamos
    sql_verduras = "SELECT nombre FROM tipo_verdura_fruta WHERE id BETWEEN 38 AND 64 ORDER BY nombre ASC"
    c.execute(sql_verduras)
    resultado_verduras = c.fetchall()
    lista_verduras = [x[0] for x in resultado_verduras]

    dict["verdura"] = lista_verduras

    return dict

# get_regiones Entrega una lista con las regiones  
def get_regiones():
    
    #Primero obtenemos las regiones con una query
    sql_regiones = "SELECT nombre FROM region ORDER BY id"
    c.execute(sql_regiones)
    resultado_regiones = c.fetchall()
    lista_regiones = [x[0] for x in resultado_regiones]
    return lista_regiones

# get_comunas Entrega una lista con las comunas correspondiente a la region ingresada
def get_comunas(region):

    #Primero obtenemos las comunas con una query
    sql = "SELECT nombre FROM comuna WHERE region_id = (SELECT id FROM region WHERE nombre = %s) ORDER BY nombre"
    c.execute(sql,(region,))
    comunas = c.fetchall()
    lista_comunas = [x[0] for x in comunas]
    return lista_comunas


# get_comuna_id Entrega el id (llave) de la comuna ingresada
def get_comuna_id(comuna):
    
    # Query
    sql = "SELECT id FROM comuna WHERE nombre = %s"
    # Obtenemos una 1-tupla 
    c.execute(sql,(comuna,))
    id = c.fetchone()
    
    return id[0]

# get_fruta_verdura_id Entrega el id (llave)
def get_fruta_verdura_id(name):
    
    # Query
    sql = "SELECT id FROM tipo_verdura_fruta WHERE nombre = %s"
    c.execute(sql,(name,))
    id = c.fetchone()
    
    return id[0]

# Recibe 2 parametros : x y , estos delimitan un rango
# Entrega una lista con productos, desde el x hasta y 
def get_last_products(inf,sup):
    # Query
    sql = "SELECT id, tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor FROM producto ORDER BY id DESC LIMIT %s, %s"
    c.execute(sql,(inf,sup,))
    list = c.fetchall()
    
    return list

# Recibe una id (la de la tabla producto )
# Entrega una lista con las frutas o verduras, asociadas a esa id
def get_productos(id):
    # Query 
    sql = "SELECT TVF.nombre FROM tipo_verdura_fruta TVF, producto_verdura_fruta PVF WHERE TVF.id=PVF.tipo_verdura_fruta_id AND PVF.producto_id=%s "
    c.execute(sql,(id,))
    list = c.fetchall()
    new_list = []
    for x in list : 
        new_list.append(x[0])

    return new_list

# Recibe el id de una comuna
# Entrega el nombre de una comuna y su region correspondiente
def get_comuna_region(id_comuna):
    # Query 
    sql = "SELECT COM.nombre, REG.nombre FROM comuna COM, region REG  WHERE COM.region_id=REG.id AND COM.id=%s"
    c.execute(sql,(id_comuna,))
    list = c.fetchall()[0]
    comuna = list[0]
    region = list[1]
    
    return comuna,region

# Recibe un parametro, el id el producto
# Entrega una lista con las rutas de las imagenes
# enlazadas a un producto
def get_files(id):
    sql = "SELECT nombre_archivo FROM foto WHERE producto_id=%s"
    c.execute(sql,(id,))
    list = c.fetchall()[0]

    return list


# Recibe 2 parametros : x y , estos delimitan un rango
# Entrega una lista con pedidos, desde el x hasta y 
def get_last_pedidos(inf,sup):
    # Query
    sql = "SELECT id, tipo, descripcion, comuna_id, nombre_comprador, email_comprador, celular_comprador FROM pedido ORDER BY id DESC LIMIT %s, %s"
    c.execute(sql,(inf,sup,))
    list = c.fetchall()
    
    return list

# Recibe una id (la de la tabla pedido)
# Entrega una lista con las frutas o verduras, asociadas a esa id
def get_productos_from_pedido(id):
    # Query 
    sql = "SELECT TVF.nombre FROM tipo_verdura_fruta TVF, pedido_verdura_fruta PVF WHERE TVF.id=PVF.tipo_verdura_fruta_id AND PVF.pedido_id=%s "
    c.execute(sql,(id,))
    list = c.fetchall()
    new_list = []
    for x in list : 
        new_list.append(x[0])

    return new_list

# Entrega la informacion necesaria para el primero grafico
# Entrega una tabla con productos (frutas o verduras) y la cantidad de veces que estan en la base de datos
def get_data_1():
    
    sql = """SELECT tvf.nombre,
             COUNT(*) AS cantidad_productos
             FROM pedido_verdura_fruta pvf
             INNER JOIN tipo_verdura_fruta tvf ON  pvf.tipo_verdura_fruta_id = tvf.id 
             GROUP BY tvf.nombre 
             ORDER BY cantidad_productos DESC"""
    c.execute(sql)
    list = c.fetchall()
    print(list)
    return list

# Entrega la informacion necesaria para el segundo grafico
# Entrega cantidad de pedidos por comuna
def get_data_2():
    
    sql = """SELECT COM.nombre, 
             COUNT(*) AS Cantidad_pedidos 
             FROM comuna COM  
             INNER JOIN pedido PE ON COM.id = PE.comuna_id 
             GROUP BY COM.nombre"""
    c.execute(sql)
    list = c.fetchall()
    print(list)
    return list