# Tarea 3

### DISCLAIMER

- Las funciones de la TAREA 2 han sido completamente implementadas, pero no se abarcan en este readme.

### **Estructura del Directorio:**

```bash
Tarea 3
├── app.py     
├── static
│   ├── css    / Archivos css
│   ├── img    / Imagenes de la pagina principal
│   ├── js     / Archivos JavaScript
│   ....       / Todas las otras carpetas son para manejar los archivos del formulario de los productos
├── templates  / Plantillas HTML
├── test       / Test para las funciones auxiliares
├── utils      / Funciones auxiliares
├── public     / HTML usados para las validaciones
└── database   / Archivos sql provistos del enunciado

```
### Funcionalidades Implementadas

1. **Agregar Pedido**

   - La página ahora funciona con Flask gracias a la función ``` agregar_pedido ```.
   - Al presionar el botón agregar producto(s), se envía un POST method, el cual genera una validación de los datos del usuario.
        - Si los Datos son validados de manera correcta, se muestra un mensaje de confirmación a través de un modal.
        - Si los Datos NO son validados, se muestra un mensaje con los errores en el formulario a través de un modal.
   - Es importante destacar que las validaciones son realizadas en Python .Todas las funciones validadoras se encuentran en el archivo
   `validation.py`
   - Cuando el usuario envía sus datos son almacenados en la base de datos gracias a la función ```submittingform_pedido``` , la cual también
   redirige al usuario a la página principal.

2. **Ver Pedido**

   - La página ahora funciona con Flask gracias a la función ` ver_pedidos `.
   - La función ` ver_pedidos `:
      - Necesita un parámetro llamado newPage, el cual indica el número de la página a desplegar.
      - Si la siguiente página no tiene pedidos que mostrar se esconde el botón de "Página siguiente".
      - El botón de "Página Anterior" redirige a la misma página si está en la primera página.
   
3. **Información Pedido**
   - Si se hace click en una fila, se genera una llamada a la función `detalle_pedido`.
   - Dependiendo de la fila en la que se clickee, se añade un parámetro distinto a la función `detalle_pedido`, el cual siempre es la id del pedido
   correspondiente.
   - `detalle_pedido` genera una query a la base de datos para obtener toda la información del pedido.

4. **Estadísticas**
   - La página funciona con Flask gracias a la función `stats`.
   - Al cargar el html, se utiliza una promesa usando fetch, la cual llama a la función `get-stats-data`.
   - `get-stats-data` obtiene la información necesaria desde la base de datos para desplegar los gráficos y los entrega en formato ".json".
   - La implementación del fetch como de los gráficos se encuentran en el archivo `stats.js`.

### Validación HTML 

   - En la carpeta [public](/public/) se encuentran los HTML generados por Flask para facilitar la validación/correción.


### Notas Adicionales

- En la mayoría de funciones, se utilizan funciones auxiliares para generar un código más limpio.
- Las funciones auxiliares se encuentran en la carpeta utils y se dividen principalmente en 3 archivos :
   - `getters.py` : Funciones que obtienen datos desde la Base de Datos.
   - ``submit.py ``: Funciones que insertan datos en la Base de Datos.
   - ``validation.py``: Funciones que validan el input del usuario.
