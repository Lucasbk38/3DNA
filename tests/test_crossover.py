from gen.crossover import Crossover, MeanCrossover, FitnessWeightedMeanCrossover, ChooseBetweenParentsCrossover
from dna.RotTable import RotTable
from random import randint
from gen.fitness import Fitness
from dna.Traj3D import Traj3D
import unittest

class TestCrossover(unittest.TestCase):

    def setUp(self):
        self.crossoverM = MeanCrossover()
        self.crossoverFWM = FitnessWeightedMeanCrossover()
        self.crossoverCBP = ChooseBetweenParentsCrossover()

        self.table_example = [RotTable().random() for _ in range(10)] #Default rot table
        self.traj = Traj3D()
        self.fitness_evaluator = Fitness()
        test_seq = "ATGCATGC"
        self.fitness = [self.fitness_evaluator.evaluate(ind, self.traj, test_seq) for ind in self.table_example]
        self.n = randint(0,len(self.table_example))
    
    def test_size(self):
        """Vérification de la taille de la population"""
        population_FWM = self.crossoverFWM.make_full_population(self.table_example,self.n, self.fitness)
        population_CBP = self.crossoverCBP.make_full_population(self.table_example,self.n, self.fitness)
        population_M = self.crossoverM.make_full_population(self.table_example,self.n, self.fitness)
        assert len(population_FWM) == self.n
        assert len(population_M) == self.n
        assert len(population_CBP) == self.n

    def test_empty_list(self):
         """Vérifie que la population est vide"""
         assert self.crossoverFWM.make_full_population([],0, []) == []
         assert self.crossoverM.make_full_population([],0, []) == []
         assert self.crossoverCBP.make_full_population([],0, []) == []

if __name__ == '__main__':
    unittest.main()

    



