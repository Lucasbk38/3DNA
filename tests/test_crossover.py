import unittest
import random

from gen.crossover import MeanCrossover, FitnessWeightedMeanCrossover, ChooseBetweenParentsCrossover

from dna.RotTable import RotTable
from gen.fitness import Fitness
from dna.Traj3D import Traj3D


class TestCrossoverBase(unittest.TestCase):
    """Tests généraux valables pour Tous les crossovers"""

    POP_SIZE = 10
    NUM_CHILDREN = 5

    def setUp(self):
        random.seed(42)

        self.crossovers = [MeanCrossover(), FitnessWeightedMeanCrossover(), ChooseBetweenParentsCrossover()]

        self.population = [RotTable().random() for _ in range(self.POP_SIZE)]
        self.traj = Traj3D()
        self.fitness_eval = Fitness()
        self.seq = "ATGCATGC"

        self.fitness = [self.fitness_eval.evaluate(ind, self.traj, self.seq) for ind in self.population]

    def test_population_size(self):
        """La taille de la population générée doit être exactement num_children"""
        for crossover in self.crossovers:
            children = crossover.make_full_population(self.population, self.NUM_CHILDREN,self.fitness)
            self.assertEqual(len(children), self.NUM_CHILDREN)

    def test_empty_population(self):
        """Une population vide ne doit jamais générer d'individus"""
        for crossover in self.crossovers:
            children = crossover.make_full_population([], 0, [])
            self.assertEqual(children, [])

    def test_rot_table_keys_preserved(self):
        """Les enfants doivent avoir exactement les mêmes clés que les parents"""
        parent_keys = set(self.population[0].rot_table.keys())

        for crossover in self.crossovers:
            children = crossover.make_full_population(self.population, 1, self.fitness)
            child_keys = set(children[0].rot_table.keys())
            self.assertEqual(parent_keys, child_keys)

    def test_rot_table_lengths_preserved(self):
        """Les longueurs des listes de rotations doivent être conservées"""
        parent = self.population[0]

        for crossover in self.crossovers:
            child = crossover.make_full_population(self.population, 1, self.fitness)[0]

            for k in parent.rot_table:
                self.assertEqual(len(parent.rot_table[k]), len(child.rot_table[k]))


class TestMeanCrossover(unittest.TestCase):

    def setUp(self):
        random.seed(1)
        self.crossover = MeanCrossover()
        self.parents = [RotTable().random(), RotTable().random()]

    def test_mean_values_are_between_parents(self):
        """Chaque valeur doit être comprise entre les deux parents"""
        child = self.crossover.make_full_population(self.parents, 1, [1.0, 1.0])[0]

        p1, p2 = self.parents

        for k in child.rot_table:
            for i, v in enumerate(child.rot_table[k]):
                self.assertGreaterEqual(v, min(p1.rot_table[k][i], p2.rot_table[k][i]))
                self.assertLessEqual(v, max(p1.rot_table[k][i], p2.rot_table[k][i]))


class TestFitnessWeightedMeanCrossover(unittest.TestCase):

    def setUp(self):
        random.seed(2)
        self.crossover = FitnessWeightedMeanCrossover()
        self.parents = [RotTable().random(), RotTable().random()]
        self.fitness = [-10, -1]  # -1 est le meilleur

    def test_best_fitness_parent_influences_more(self):
        """Le parent avec la fitness la plus proche de 0 doit influencer davantage"""

        parents = [self.parents[0], self.parents[1]]
        child = self.crossover.make_full_population(parents, 1, fitness=self.fitness)[0]
        best, worst = parents[1], parents[0]

        self.assertTrue(all(abs(child.rot_table[k][i] - best.rot_table[k][i]) <= abs(child.rot_table[k][i] - worst.rot_table[k][i]) for k in child.rot_table for i in range(len(child.rot_table[k]))))


class TestChooseBetweenParentsCrossover(unittest.TestCase):
    
    def setUp(self):
        random.seed(3)
        self.crossover = ChooseBetweenParentsCrossover()
        self.parents = [RotTable().random(), RotTable().random()]

    def test_child_values_come_from_parents(self):
        """Chaque valeur doit provenir exactement d'un des deux parents"""
        child = self.crossover.make_full_population(self.parents, 1, [1.0, 1.0])[0]

        p1, p2 = self.parents

        for k in child.rot_table:
            for i, v in enumerate(child.rot_table[k]):
                self.assertIn(v, (p1.rot_table[k][i], p2.rot_table[k][i]))


if __name__ == "__main__":
    unittest.main()
