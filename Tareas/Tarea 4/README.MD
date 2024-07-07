# Tarea 4

### DISCLAIMER

- La funciones de las Tareas anteriores han sido completamente implementadas, pero no se abarcan en este readme.
- La Tarea 3 fue modificada para tener un nuevo elemento en la barra de navegación.


### Funcionalidades Implementadas

1. **Ver Fotos Productos**

   - Ahora es un nuevo elemento de la barra de navegación, muestra las últimas 20 fotos insertadas en formato 120x120 pixeles
   - Las fotos estan ordenadas de más reciente a más antigua de izquierda a derecha y luego de arriba hacia abajo.
   - Cada número en el círculo azul de cada foto corresponde a los comentarios que tiene esa foto.
   - Clickear una foto nos redirige a la url ```ver-foto/{id}``` de la cual hablamos a continuación.

2. **Ver Foto**

    - Se muestra la foto clickeada en formato 640X480 a la izquierda.
    - Los comentarios de la foto se muestran a la derecha, ordenados de más reciente a más antiguo de arriba hacia abajo.
    - Al final de la página se encuentra un pequeño formulario para añadir un comentario.
    - Al clickear el botón agregar comentario se actualiza automáticamente la página.

### Validación HTML 

   - En la carpeta [public](/public/) se encuentran los HTML generados por Flask para facilitar la validación/correción.


### Notas Adicionales

- Es OBLIGATORIO ejecutar app.py de la carpeta flask para tener las funcionalidades de la tarea 3.
- Es OBLIGATORIO ejecutar la aplicación de Java que se encuentra en tarea4/src/main/java/programacionweb/tarea4 para tener las funcionalidades de la Tarea 4.
- En la carpeta sql se encuentra el código utilizado para crear la tabla comentario. Es MANDATORIO ocupar ese código para crear la tabla, de otra manera, las inserciones de comentarios NO VAN A FUNCIONAR.
