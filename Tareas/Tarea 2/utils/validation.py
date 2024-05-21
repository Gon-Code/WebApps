# Imports

import re


# En este archivo se encuentran las funciones validadoras del input


# Verifica que el largo del nombre sea correcto
def validate_username(value,error):
    isValid = False

    if  1 <= len(value) and len(value) <= 80 :
        isValid = True 
    else:
        error += "\n El nombre del productor es demasiado grande"
    return (isValid,error)

# Recibe una lista de strings
# Verifica que se hayan elegido al menos 1 producto y maximo 5
def validate_producto(listaProductos,error):
    isValid = False
    if 1 <= len(listaProductos) and len(listaProductos) <= 5:
        isValid = True
    else:
        error += "\n Debe escoger al menos 1 producto y maximo 5"

    return (isValid,error)

# Verifica que el email este en el formato correcto
def validate_email(value,error):
    isValid = False

    # Expresion regular con la que debe matchear el email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(regex,value):
        isValid = True

    else:
        error += "\n Email ingresado no es valido"
    return  (isValid,error)

# Verifica que el numero de telefono comience con un 9, seguido de 8 numeros
def validate_phoneNumer(value,error):
    isValid = False

    # Expresion regular con la que debe matchear el telefono
    regex = r'^9\d{8}'

    if re.fullmatch(regex,value) :
        isValid = True

    else:
        error += "\n El formato del numero de telefono debe ser 9XXXXXXXX"
    
    return (isValid,error)




# Esta funcion llama a todas las funciones validadoras
def validate(input):
    username, productos, phone, email = input
    error = ""

    isUsernameValid, UsernameError = validate_username(username,error)
    isProductoValid, ProductoError = validate_producto(productos,UsernameError)
    isPhoneValid, PhoneError = validate_phoneNumer(phone, ProductoError)
    isEmailValid, EmailError = validate_email(email, PhoneError)


    print("\nMostrando mensaje de error final : ")
    print(EmailError)

    if isUsernameValid and isProductoValid and isPhoneValid and isEmailValid :
        print('Validacion correcta')
        return True

    return EmailError


