import unittest
import numpy as np
from gen.selection import Elitism, TournamentSelection, RouletteSelection, RankSelection, TournamentWithHopeSelection
from dna.RotTable import RotTable
from dna.Traj3D import Traj3D
from gen.fitness import Fitness


class TestSelection(unittest.TestCase):
    """Test les 4 stratégies de SÉLECTION d'un algorithme génétique.
    La sélection choisit les MEILLEURS individus pour les reproduire.
    On teste que chaque sélection retourne la bonne moitié de la population."""

    def setUp(self):
        """Crée une population de test avec des fitness réelles."""
        np.random.seed(42)
        
        self.population_size = 10
        
        # Crée 10 individus différents
        self.individus = [RotTable.random() for _ in range(self.population_size)]
        self.traj = Traj3D()
        self.fitness_evaluator = Fitness()
        test_seq = "ATGCATGC"  # Séquence ADN test
        
        self.fitness = [self.fitness_evaluator.evaluate(ind, self.traj, test_seq) for ind in self.individus]
        
        # On sélectionne la moitié de la population
        self.expected_size = self.population_size // 2

    def test_elitism_selects_best_individuals(self):
        """Test de l'élitisme"""
        selector = Elitism()
        selected = selector.select(1/2, self.individus, self.fitness)
        
        # Vérification 1: Taille correcte
        self.assertEqual(len(selected), self.expected_size)
        
        # Vérification 2: Les meilleurs sont bien là
        best_individuals = sorted(zip(self.individus, self.fitness), key=lambda x: x[1], reverse=True)[:self.expected_size]
        best_set = {ind for ind, _ in best_individuals}
        
        self.assertEqual(set(selected), best_set, "L'élitisme doit retourner exactement les meilleurs")

    def test_tournament_favors_best(self):
        """Test du tournoi"""
        selector = TournamentSelection()
        selected = selector.select(1/2, self.individus, self.fitness)
        
        # Vérification 1: Taille correcte et individus valides
        self.assertEqual(len(selected), self.expected_size)
        for ind in selected:
            self.assertIn(ind, self.individus)
        
        # Vérification 2: Le meilleur doit être sélectionné plus souvent
        # indices triés du plus grand au plus petit
        sorted_indices = np.argsort(self.fitness)[::-1]

        # meilleur individu
        best_individual = self.individus[sorted_indices[0]]

        # deuxième meilleur
        second_best_individual = self.individus[sorted_indices[1]]

        # Le pire individu
        worst_individual = self.individus[np.argmin(self.fitness)]
        
        count_best = 0
        count_second_best = 0
        count_worst = 0
        repetitions = 100
        
        for _ in range(repetitions):
            selected = selector.select(1/2, self.individus, self.fitness)
            if best_individual in selected:
                count_best += 1
            if worst_individual in selected:
                count_worst += 1
            if second_best_individual in selected:
                count_second_best += 1
        
        # Le meilleur doit toujours être sélectionné.
        # Les meilleurs ont plus de chances d'être sélectionnés
        self.assertGreater(count_second_best, count_worst, f"Le meilleur doit être sélectionné plus souvent ({count_best} vs {count_worst})")
        self.assertEqual(count_best, repetitions)

    def test_roulette_probabilistic_selection(self):
        """Test de la roulette"""

        selector = RouletteSelection()
        selected = selector.select(1/2, self.individus, self.fitness)
        
        # Vérification 1: Taille correcte et individus valides
        self.assertEqual(len(selected), self.expected_size)
        for ind in selected:
            self.assertIn(ind, self.individus)
        
        # Vérification 2: Les meilleurs ont plus de chances
       # indices triés du plus grand au plus petit
        sorted_indices = np.argsort(self.fitness)[::-1]

        # meilleur individu
        best_individual = self.individus[sorted_indices[0]]

        # deuxième meilleur
        second_best_individual = self.individus[sorted_indices[1]]

        # Le pire individu
        worst_individual = self.individus[np.argmin(self.fitness)]
        
        count_best = 0
        count_second_best = 0
        count_worst = 0
        repetitions = 100
        
        for _ in range(repetitions):
            selected = selector.select(1/2, self.individus, self.fitness)
            if best_individual in selected:
                count_best += 1
            if worst_individual in selected:
                count_worst += 1
            if second_best_individual in selected:
                count_second_best += 1
        
        # Le meilleur doit toujours être sélectionné.
        # Les meilleurs ont plus de chances d'être sélectionnés
        self.assertGreater(count_second_best, count_worst, f"Roulette: Le meilleur doit avoir plus de chances ({count_best} vs {count_worst})")
        self.assertEqual(count_best, repetitions)

    def test_rank_based_selection(self):
        """Test du rang"""

        selector = RankSelection()
        selected = selector.select(1/2, self.individus, self.fitness)
        
        # Vérification 1: Taille correcte et individus valides
        self.assertEqual(len(selected), self.expected_size)
        for ind in selected:
            self.assertIn(ind, self.individus)
        
        # Vérification 2: Les meilleurs ont plus de chances
        # indices triés du plus grand au plus petit
        sorted_indices = np.argsort(self.fitness)[::-1]

        # meilleur individu
        best_individual = self.individus[sorted_indices[0]]

        # deuxième meilleur
        second_best_individual = self.individus[sorted_indices[1]]
        
        # Le pire individu
        worst_individual = self.individus[np.argmin(self.fitness)]
        
        count_best = 0
        count_second_best = 0
        count_worst = 0
        repetitions = 100
        
        for _ in range(repetitions):
            selected = selector.select(1/2, self.individus, self.fitness)
            if best_individual in selected:
                count_best += 1
            if worst_individual in selected:
                count_worst += 1
            if second_best_individual in selected:
                count_second_best += 1
        
        # Le meilleur doit toujours être sélectionné.
        # Les meilleurs ont plus de chances d'être sélectionnés
        self.assertGreater(count_second_best, count_worst, f"Rang: Le meilleur doit être sélectionné plus souvent ({count_best} vs {count_worst})")
        self.assertEqual(count_best, repetitions)

    def test_tournament_with_hope(self):
        """Test du tournoi avec espoir"""
        selector = TournamentWithHopeSelection()
        selected = selector.select(1/2, self.individus, self.fitness)
        
        # Vérification 1: Taille correcte et individus valides
        self.assertEqual(len(selected), self.expected_size)
        for ind in selected:
            self.assertIn(ind, self.individus)
        
        # Vérification 2: Le meilleur doit être sélectionné plus souvent

        # indices triés du plus grand au plus petit
        sorted_indices = np.argsort(self.fitness)[::-1]

        # meilleur individu
        best_individual = self.individus[sorted_indices[0]]

        # deuxième meilleur
        second_best_individual = self.individus[sorted_indices[1]]

        # Le pire individu
        worst_individual = self.individus[np.argmin(self.fitness)]
        
        count_best = 0
        count_second_best = 0
        count_worst = 0
        repetitions = 100
        
        for _ in range(repetitions):
            selected = selector.select(1/2, self.individus, self.fitness)
            if best_individual in selected:
                count_best += 1
            if worst_individual in selected:
                count_worst += 1
            if second_best_individual in selected:
                count_second_best += 1
        
        # Le meilleur doit toujours être sélectionné.
        # Les meilleurs ont plus de chances d'être sélectionnés
        self.assertGreater(count_second_best, count_worst, f"Le meilleur doit être sélectionné plus souvent ({count_best} vs {count_worst})")
        self.assertEqual(count_best, repetitions)



if __name__ == "__main__":
    unittest.main()

