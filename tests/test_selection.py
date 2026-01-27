import unittest
import numpy as np
from gen.selection import Elitism, TournamentSelection, RouletteSelection, RankSelection, TournamentWithHopeSelection
from dna.RotTable import RotTable
from dna.Traj3D import Traj3D
from gen.fitness import Fitness
import random 

class TestSelectionContract(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        np.random.seed(42)

        self.population_size = 20
        self.keep_rate = 0.5

        self.individus = [RotTable.random() for _ in range(self.population_size)]
        self.traj = Traj3D()
        self.fitness_eval = Fitness()
        self.seq = "ATGCATGC"

        self.fitness = [self.fitness_eval.evaluate(ind, self.traj, self.seq) for ind in self.individus]

        self.selectors = [Elitism(), TournamentSelection(), RouletteSelection(), RankSelection(), TournamentWithHopeSelection()]

    def test_size_of_selection(self):
        """La taille retournée doit respecter keepRate"""
        expected = int(self.keep_rate * self.population_size)

        for selector in self.selectors:
            selected = selector.select(self.keep_rate, self.individus, self.fitness)
            self.assertEqual(len(selected), expected)

    def test_indices_are_valid(self):
        """Les indices retournés doivent être valides"""
        for selector in self.selectors:
            selected = selector.select(self.keep_rate, self.individus, self.fitness)
            for i in selected:
                self.assertIsInstance(i, int)
                self.assertGreaterEqual(i, 0)
                self.assertLess(i, self.population_size)

    def test_best_individual_is_always_selected(self):
        """Le meilleur individu est toujours sélectionné (contrat explicite)"""
        best_index = max(range(self.population_size), key=lambda i: self.fitness[i])

        for selector in self.selectors:
            selected = selector.select(self.keep_rate, self.individus, self.fitness)
            self.assertIn(best_index, selected)




if __name__ == "__main__":
    unittest.main()

