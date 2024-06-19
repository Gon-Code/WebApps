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
        limite_sup = 1
        self.assertEquals(len(get_last_products(limite_inf,limite_sup)),1)

    # Testing getter for get_productos
    def test_get_productos(self):
        id = 116
        self.assertEquals(len(get_productos(id)),5)

    # Testing getter for get_comuna_region
    def test_get_comuna_region(self):
        id = 80109
        self.assertEquals(get_comuna_region(id),("Coihueco","Región del Ñuble"))

    # Testing getter for get_files
    def test_get_files(self):
        id = 111
        self.assertEquals(get_files(id)[0],'b66b67c33ff0e4cb51fdc5915eeecafa9a74448f18f94d4cd802d70c5ce4b385.jpg')

    # Testing getter for get_productos_from_pedido
    def test_get_productos_from_pedido(self):
        id = 6
        self.assertEquals(len(get_productos_from_pedido(id)),3)

    # Testing getter for get_Data_1
    def test_get_data_1(self):
        self.assertEquals(get_data_1(),3)

    # Testing getter for get_Data_2
    def test_get_data_2(self):
        self.assertEquals(get_data_2(),3)





if __name__ == '__main__':
    unittest.main()