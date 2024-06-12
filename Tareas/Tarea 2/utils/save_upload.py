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
    