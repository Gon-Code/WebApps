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









if __name__ == '__main__':
    unittest.main()