import pymysql


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
    sql_frutas = "SELECT nombre FROM tipo_verdura_fruta WHERE id BETWEEN 1 AND 37"
    c.execute(sql_frutas)
    resultado_frutas = c.fetchall()
    lista_frutas = [x[0] for x in resultado_frutas]

    dict["fruta"] = lista_frutas

    # Obtenemos las verduras y las guardamos
    sql_verduras = "SELECT nombre FROM tipo_verdura_fruta WHERE id BETWEEN 38 AND 64"
    c.execute(sql_verduras)
    resultado_verduras = c.fetchall()
    lista_verduras = [x[0] for x in resultado_verduras]

    dict["verdura"] = lista_verduras

    return dict

# get_regiones Entrega una lista con las regiones  
def get_regiones():
    
    #Primero obtenemos las regiones con una query
    sql_regiones = "SELECT nombre FROM region "
    c.execute(sql_regiones)
    resultado_regiones = c.fetchall()
    lista_regiones = [x[0] for x in resultado_regiones]
    return lista_regiones

# get_comunas Entrega una lista con las comunas correspondiente a la region ingresada
def get_comunas(region):

    #Primero obtenemos las comunas con una query
    sql = "SELECT nombre FROM comuna WHERE region_id = (SELECT id FROM region WHERE nombre = %s)"
    c.execute(sql,(region,))
    comunas = c.fetchall()
    lista_comunas = [x[0] for x in comunas]
    return lista_comunas



