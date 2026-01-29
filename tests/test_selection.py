import unittest
import numpy as np
from gen.selection import ElitismSelection, TournamentSelection, RouletteSelection, RankSelection, TournamentWithHopeSelection
from dna.RotTable import RotTable
from dna.Traj3D import Traj3D
from gen.fitness import FitnessNorm2Last
import random 

class TestSelectionContract(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        np.random.seed(42)

        self.population_size = 20
        self.keep_rate = 0.5

        self.individus = [RotTable.random() for _ in range(self.population_size)]
        self.traj = Traj3D()
        self.fitness_eval = FitnessNorm2Last()
        self.seq = "ATGCATGC"

        self.fitness = [self.fitness_eval.evaluate(ind, self.traj, self.seq) for ind in self.individus]

        self.selectors = [ElitismSelection(), TournamentSelection(), RouletteSelection(), RankSelection(), TournamentWithHopeSelection()]

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
        """Le meilleur individu est toujours sélectionné"""
        best_index = max(range(self.population_size), key=lambda i: self.fitness[i])

        for selector in self.selectors:
            selected = selector.select(self.keep_rate, self.individus, self.fitness)
            self.assertIn(best_index, selected)

class TestElitismSelection(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        np.random.seed(0)
        self.individus = [RotTable.random() for _ in range(10)]
        self.fitness: list[float] = list(range(10))  # fitness (positive mais pas grave)

    def test_elitism_selects_exact_best(self):
        """Teste si élitisme sélectionne les meilleurs"""
        selector = ElitismSelection()
        selected = selector.select(0.5, self.individus, self.fitness)

        expected = [9, 8, 7, 6, 5]
        self.assertEqual(set(selected), set(expected))

class TestTournamentSelection(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        np.random.seed(0)
        self.individus = [RotTable.random() for _ in range(10)]
        self.fitness: list[float] = list(range(10))  # fitness (positive mais pas grave)

    def test_tournament_favors_best(self, k_best=2):
        """
        Teste si la sélection par tournoi favorise le k-ième meilleur individu
        par rapport au pire.
        
        k_best=1 -> meilleur
        k_best=2 -> deuxième meilleur
        """
        selector = TournamentSelection()

        # Trier les indices par fitness décroissante
        sorted_indices = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=True)

        # Identifier le k-ième meilleur et le pire
        target = sorted_indices[k_best - 1]  # k_best=2 Le deuxième meilleur
        worst = sorted_indices[-1]           # pire

        count_target = 0
        count_worst = 0
        repetitions = 300

        for _ in range(repetitions):
            selected = selector.select(0.5, self.individus, self.fitness)
            if target in selected:
                count_target += 1
            if worst in selected:
                count_worst += 1

        self.assertGreater(count_target, count_worst)

class TestRouletteSelection(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        np.random.seed(0)
        self.individus = [RotTable.random() for _ in range(10)]
        self.fitness: list[float] = list(range(10))  # fitness (positive mais pas grave)

    def test_roulette_favors_best(self, k_best=2):
        """Teste que le k ème individu a plus de chance d'être choisi que le pire"""
        selector = RouletteSelection()

        # Trier les indices par fitness décroissante
        sorted_indices = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=True)

        # Identifier le k-ième meilleur et le pire
        target = sorted_indices[k_best - 1]  # k_best=2 Le deuxième meilleur
        worst = sorted_indices[-1]           # pire

        count_target = 0
        count_worst = 0
        repetitions = 100000

        for _ in range(repetitions):
            selected = selector.select(0.5, self.individus, self.fitness)
            if target in selected:
                count_target += 1
            if worst in selected:
                count_worst += 1

        self.assertGreater(count_target, count_worst)

class TestRankSelection(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        np.random.seed(0)
        self.individus = [RotTable.random() for _ in range(10)]
        self.fitness: list[float] = list(range(10))  # fitness (positive mais pas grave)

    def test_rank_favors_best(self, k_best=2):
        """Teste que le k ème individu a plus de chance d'être choisi que le pire"""
        selector = RankSelection()

        # Trier les indices par fitness décroissante
        sorted_indices = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=True)

        # Identifier le k-ième meilleur et le pire
        target = sorted_indices[k_best - 1]  # k_best=2 Le deuxième meilleur
        worst = sorted_indices[-1]           # pire

        count_target = 0
        count_worst = 0
        repetitions = 300

        for _ in range(repetitions):
            selected = selector.select(0.5, self.individus, self.fitness)
            if target in selected:
                count_target += 1
            if worst in selected:
                count_worst += 1

        self.assertGreater(count_target, count_worst)

class TestTournamentWithHopeSelection(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        np.random.seed(0)
        self.individus = [RotTable.random() for _ in range(10)]
        self.fitness: list[float] = list(range(10))  # fitness (positive mais pas grave)

    def test_tournament_with_hope_allows_worst(self):
        """Teste si le pire peut être choisi parfois"""
        selector = TournamentWithHopeSelection(hopeProbability=0.5) # Probabilité élevé pour éviter de faire trop d'itérations

        worst = min(range(len(self.fitness)), key=lambda i: self.fitness[i])

        found = False
        for _ in range(300):
            selected = selector.select(0.5, self.individus, self.fitness)
            if worst in selected:
                found = True
                break

        self.assertTrue(found, "Le pire doit parfois être sélectionné avec l'espoir")








if __name__ == "__main__":
    unittest.main()

