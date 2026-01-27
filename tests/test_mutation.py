import unittest
import numpy as np
from dna.RotTable import RotTable, rotTableConfig
from gen.mutation import GaussianAdditiveMutation, GaussianAdditiveDeltaMutation, GaussianMultiplicativeMutation, Mutation

class TestMutations(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.individu = RotTable.random()

    def test_mutations_GAM(self):
        
        mutated_individu = GaussianAdditiveMutation().mutate(self.individu)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)

    def test_mutations_GADM(self):
        
        mutated_individu = GaussianAdditiveDeltaMutation().mutate(self.individu)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)

    def test_mutations_GMM(self):
        
        mutated_individu = GaussianMultiplicativeMutation().mutate(self.individu)
        for k, dinuc in mutated_individu.rot_table.items():
            for i, val in enumerate(dinuc):
                if self.individu.rot_table[k][i] >= 2:
                    self.assertEqual(val, self.individu.rot_table[k][i])
                else:
                    min_val = rotTableConfig[k][i] - rotTableConfig[k][3 + i]
                    max_val = rotTableConfig[k][i] + rotTableConfig[k][3 + i]
                    self.assertTrue(min_val <= val <= max_val)

if __name__ == "__main__":
    unittest.main()
