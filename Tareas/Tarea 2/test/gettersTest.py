import unittest
from utils.getters import *

class TestgettersFunctions(unittest.TestCase):
    
    # Testing getter for Comuna id
    def test_get_comuna_id(self):
        comuna = "Coihueco"
        self.assertEquals(get_comuna_id(comuna),80109)

    # Testing getter for fruta_verdura id
    def test_get_fruta_verdura_id(self):
        name = "Frutilla"
        self.assertEquals(get_fruta_verdura_id(name),3)

    
    # Testing getter for fruta_verdura id
    def test_get_last_product(self):
        limite_inf = 0
        limite_sup = 5
        self.assertEquals(len(get_last_products(limite_inf,limite_sup)),5)

    # Testing getter for get_productos
    def test_get_productos(self):
        id = 97
        self.assertEquals(len(get_productos(id)),4)

    # Testing getter for get_comuna_region
    def test_get_comuna_region(self):
        id = 80109
        self.assertEquals(get_comuna_region(id),("Coihueco","Región del Ñuble"))

    # Testing getter for get_files
    def test_get_files(self):
        id = 111
        self.assertEquals(get_files(id)[0],'b66b67c33ff0e4cb51fdc5915eeecafa9a74448f18f94d4cd802d70c5ce4b385.jpg')







if __name__ == '__main__':
    unittest.main()