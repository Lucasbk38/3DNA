from gen.crossover import Crossover
from dna.RotTable import RotTable
from random import randint
import unittest

class TestCrossover(unittest.TestCase):

    def setUp(self):
        self.crossover = Crossover()
        self.table_example = RotTable() #Default rot table
        self.n = randint(0,len(self.table_example.getTable()))
    
    def test_size(self):
        """Vérification de la taille de la population"""
        population = self.crossover.make_full_population(self.table_example.getTable(),self.n)
        assert len(population) == self.n

    def test_empty_list(self):
         """Vérifie que la population est vide"""
         assert self.crossover.make_full_population([],0) == []

if __name__ == '__main__':
    unittest.main()

    



