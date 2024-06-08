import re

# Funciones validadoras del input

def validate_username(value, error):
    isValid = False
    if 1 <= len(value) <= 80:
        isValid = True
    else:
        error += "El nombre del productor es demasiado grande\n"
    return isValid, error

def validate_producto(listaProductos, error):
    isValid = False
    if 1 <= len(listaProductos) <= 5:
        isValid = True
    else:
        error += "Debe escoger al menos 1 producto y máximo \n"
    return isValid, error

def validate_phone_number(value, error):
    isValid = False
    regex = r'^9\d{8}$'
    if re.fullmatch(regex, value):
        isValid = True
    else:
        error += "El formato del número de teléfono debe ser 9XXXXXXXX\n"
    return isValid, error

def validate_email(value, error):
    isValid = False
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(regex, value):
        isValid = True
    else:
        error += "El email ingresado no es válido\n"
    return isValid, error


def validate(input):
    username, productos, phone, email = input
    error = ""

    isUsernameValid, error = validate_username(username, error)
    isProductoValid, error = validate_producto(productos, error)
    isPhoneValid, error = validate_phone_number(phone, error)
    isEmailValid, error = validate_email(email, error)

    print("\nMostrando mensaje de error final:")
    print(error)

    if isUsernameValid and isProductoValid and isPhoneValid and isEmailValid:
        print('Validación correcta')
        return True

    return error
