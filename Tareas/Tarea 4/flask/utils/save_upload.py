import os
import hashlib
from werkzeug.utils import secure_filename
import filetype


current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script Python actual


# Recibe una lista de archivos
# Ya estan validados asi que solo se deben subir
# Retorna una lista con las urls
def save_uploads(files):
    
    # Aqui se guardan los nombres de los archivos 
    uploads = []
    # Se guardan los archivos en una carpeta auxiliar
    for file in files :
        if file == None :
            uploads.append(None)
            continue
       # Generamos nombre al azar para foto
        _filename = hashlib.sha256(
            secure_filename(file.filename) # nombre del archivo
            .encode("utf-8") # encodear a bytes
            ).hexdigest()
        _extension = filetype.guess(file).extension
        img_filename = f"{_filename}.{_extension}"
        #print(f"Nombre del archivo{i} : {img_filename}")
        # Guardamos en el directorio auxiliar
        # Construir la ruta absoluta al directorio de destino
        target_dir = os.path.abspath(os.path.join(current_dir, '..', 'static', 'preupload'))  # Ruta al directorio /static/preupload  
        new_path = os.path.join(target_dir,img_filename)
        # Guardamos el nombre
        uploads.append(img_filename)
        # Guarda la foto
        file.save(new_path)
                    
    # Luego le paso la lista con los nombres de los archivos
    return uploads
    # Submit toma los archivos, los guarda en la carpeta de upload folder
    
    # Y borra lo archivos en la carpeta auxiliar
    
    # Envia los datos a la base de datos 


# Guarda las imagenes en los 3 tamanos distintos
# recibe la imagen y su nombre
def resize(file,filename):
    # Construir la ruta absoluta al directorio de destino
    target_dir_small = os.path.abspath(os.path.join(current_dir, '..', 'static', 'small'))  # Ruta al directorio /static/small 
    target_dir_medium = os.path.abspath(os.path.join(current_dir, '..', 'static', 'medium'))  # Ruta al directorio /static/medium 
    target_dir_large = os.path.abspath(os.path.join(current_dir, '..', 'static', 'large'))  # Ruta al directorio /static/large
    
    path_small = os.path.join(target_dir_small,filename)
    path_medium = os.path.join(target_dir_medium,filename)
    path_large = os.path.join(target_dir_large,filename)
    
    file_small = file.resize((120,120))
    file_medium = file.resize((640,480))
    file_large = file.resize((1280,1024))
    
    file_small.save(path_small)
    file_medium.save(path_medium)
    file_large.save(path_large)    
    
    return 

# Para la Tarea 4 , necesitamos guardar una copia de las fotos en la ruta static de java
# Especificamente en la carpeta /static/small y /static/medium
def save_java(file,filename):
    
    # Construir la ruta absoluta al directorio de destino EN JAVA
    target_dir_small = os.path.abspath(os.path.join(current_dir, '..', '..', 'tarea4', 'src','main',
                                                    'resources', 'static', 'small'))  # Ruta al directorio /static/small
    target_dir_medium = os.path.abspath(os.path.join(current_dir, '..', '..', 'tarea4', 'src','main',
                                                    'resources', 'static', 'medium'))  # Ruta al directorio /static/medium
    
    # Unimos ruta y nombre de archivo
    path_small = os.path.join(target_dir_small,filename)
    path_medium = os.path.join(target_dir_medium,filename)
    
    # Redimensionamos la imagen    
    file_small = file.resize((120,120))
    file_medium = file.resize((640,480))

    # Guarda los archivos
    file_small.save(path_small)
    file_medium.save(path_medium)    
    
    return