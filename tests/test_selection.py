import unittest
import random
import numpy as np
from gen.selection import Elitism, Tournament, Roulette, Rank
from dna.RotTable import RotTable
from dna.Traj3D import Traj3D
from gen.fitness import Fitness


class TestSelection(unittest.TestCase):

    def setUp(self):
        # Prépare une population de test
        random.seed(42)
        np.random.seed(42)
        
        self.population_size = 10
        # Créer 10 RotTable
        self.individus = [RotTable().random() for _ in range(self.population_size)]
        
        # Créer 10 fitness en évaluant chaque individu
        self.traj = Traj3D()
        self.fitness_evaluator = Fitness()
        test_seq = "ATGC"
        self.fitness = [self.fitness_evaluator.evaluate(ind, self.traj, test_seq) for ind in self.individus]

        self.expected_size = self.population_size // 2

    def _basic_checks(self, selected):

        self.assertEqual(len(selected), self.expected_size)

        for ind in selected:
            self.assertIn(ind, self.individus)

    def test_elitism(self):
        selector = Elitism()
        selected = selector.select(self.individus, self.fitness)

        self._basic_checks(selected)

    def test_tournament(self):
        selector = Tournament()
        selected = selector.select(self.individus, self.fitness)

        self._basic_checks(selected)

    def test_roulette(self):
        selector = Roulette()
        selected = selector.select(self.individus, self.fitness)

        self._basic_checks(selected)

    def test_rank(self):
        selector = Rank()
        selected = selector.select(self.individus, self.fitness)

        self._basic_checks(selected)


if __name__ == "__main__":
    unittest.main()
