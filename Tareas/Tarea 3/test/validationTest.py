import unittest
from utils.validation import *

class TestvalidationFunctions(unittest.TestCase):
    
    # Test validate username function 
    def test_validateUsername(self):
        longName = "A" * 81
        error = ""
        self.assertTrue(validate_username("Gonzalo",error)[0])
        self.assertFalse(validate_email("h",error)[0])
        self.assertFalse(validate_username(longName,error)[0])

    # Test validate producto function
    def test_validateProducto(self):
        productos = ["1","2","3","4","5","6","7"]
        error = ""
        self.assertTrue(validate_producto(productos[:1],error)[0])
        self.assertTrue(validate_producto(productos[:5],error)[0])
        self.assertFalse(validate_producto([],error)[0])
        self.assertFalse(validate_producto(productos,error)[0])

    # Test validate Email function
    def test_validateEmail(self):
        error = ""
        self.assertTrue(validate_email("juanitoperez@hotmail.com",error)[0])
        self.assertFalse(validate_email("estonoesuncorreo.com",error)[0])
    
    # Test validate Phone function
    def test_validatePhone(self):
        error = ""
        self.assertTrue(validate_phone_number("988888888",error)[0])
        self.assertFalse(validate_phone_number("1",error)[0])
        self.assertFalse(validate_phone_number("123456789",error)[0])


        
if __name__ == '__main__':
    unittest.main()
