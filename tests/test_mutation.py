import unittest
import numpy as np
from dna.RotTable import RotTable, rotTableConfig
from gen.mutation import GaussianAdditiveMutation, GaussianAdditiveDeltaMutation, GaussianMultiplicativeMutation, SimulatedAnnealingMutation, ThresholdMutation, GaussianAdditiveDeltaLog10FitnessAnnealedMutation
from dna.Traj3D import Traj3D
from gen.fitness import Fitness

class TestMutations(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)

        # Crée un individu de test
        self.individu = RotTable.random()
        
        # Crée une petite popu de test
        self.population = [RotTable.random() for _ in range(3)]
        self.fitnesses = [-1.0 for _ in self.population]


        self.base_mutator = GaussianAdditiveMutation(sigma=0.1)
        self.sa_mutator = SimulatedAnnealingMutation(mutation=self.base_mutator, key="sigma", alpha=0.5)

    def test_values_above_threshold_are_not_mutated(self):
        """Conservation des valeurs supérieures ou égale à 2"""
        for k in self.individu.rot_table:
            self.individu.rot_table[k][0] = 2.5

        mutator = GaussianAdditiveMutation(sigma=10.0)
        mutated = mutator.mutate(self.individu, fitness=-1.0)

        for k in mutated.rot_table:
            self.assertEqual(mutated.rot_table[k][0], self.individu.rot_table[k][0])

    def test_mutation_does_not_modify_original_individu(self):
        """Vérifie que c'est nouveau qui apparaît"""
        original = self.individu
        mutator = GaussianAdditiveMutation(sigma=1.0)

        mutated = mutator.mutate(original, fitness=-1.0)

        self.assertIsNot(original, mutated)
        self.assertNotEqual(original.rot_table, mutated.rot_table)

    def test_mutate_population_preserves_size(self):
        """Préserve la taille"""
        mutator = GaussianAdditiveMutation()
        mutated_pop = mutator.mutate_population(self.population, self.fitnesses)

        self.assertEqual(len(mutated_pop), len(self.population))

    def test_mutations_GAM(self):
        """Teste que les mutations de type GaussianAdditive respectent les intervalles de valeurs"""
        mutated_individu = GaussianAdditiveMutation().mutate(self.individu, -1)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)

    def test_mutations_GADM(self):
        """Teste que les mutations de type GaussianAdditiveDelta respectent les intervalles de valeurs"""
        mutated_individu = GaussianAdditiveDeltaMutation().mutate(self.individu, -1)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)
    
    def test_mutations_GADLogM(self):
        """Teste que les mutations de type GaussianAdditiveDeltaLog10FitnessAnnealed respectent les intervalles de valeurs"""
        mutated_individu = GaussianAdditiveDeltaLog10FitnessAnnealedMutation().mutate(self.individu, -1)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)

    def test_mutations_GMM(self):
        """Teste que les mutations de type GaussianMultiplicative respectent les intervalles de valeurs"""
        mutated_individu = GaussianMultiplicativeMutation().mutate(self.individu, -1)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)


    def test_alpha_decay(self):
        """Teste que le paramètre sigma diminue correctement avec le facteur alpha à chaque appel"""
        initial_sigma = self.base_mutator.sigma
        alpha = self.sa_mutator.alpha

        # Premier appel
        pop1 = self.sa_mutator.mutate_population(self.population, self.fitnesses)
        self.assertAlmostEqual(self.base_mutator.sigma, initial_sigma * alpha)

        # Deuxième appel
        pop2 = self.sa_mutator.mutate_population(self.population, self.fitnesses)
        self.assertAlmostEqual(self.base_mutator.sigma, initial_sigma * alpha * alpha)

        # Vérifier que les individus retournés sont valides
        for p in pop1 + pop2:
            self.assertIsInstance(p, RotTable)

    def test_threshold_mutator_zero_probability(self):
        """Teste que l'individu ne change pas"""
        base = GaussianAdditiveMutation(sigma=10.0)
        threshold = ThresholdMutation(base, mutation_probability=0.0)

        mutated = threshold.mutate(self.individu, fitness=-1.0)

        self.assertEqual(mutated.rot_table, self.individu.rot_table)

    def test_threshold_mutator_full_probability(self):
        """Teste que l'individu mute toujours"""
        np.random.seed(0)
        base = GaussianAdditiveMutation(sigma=1.0)
        threshold = ThresholdMutation(base, mutation_probability=1.0)

        mutated = threshold.mutate(self.individu, fitness=-1.0)

        self.assertNotEqual(mutated.rot_table, self.individu.rot_table)




if __name__ == "__main__":
    unittest.main()

    
