from individu import Individu
from fitness import Fitness
import random

class Selection():
    def __init__(self):
        self.methods = {
            "elitism": self.elitism,
            "roulette": self.roulette,
            "tournament": self.tournament,
            "rank": self.rank
        }
    
    def select(self, individus: list[Individu], method: str) -> list[Individu]:
        if method not in self.methods:
            raise ValueError(f"Méthode de sélection inconnue : {method}")
        return self.methods[method](individus)
        
    # Séléction par rang
    def rank(self, individus: list[Individu]) -> list[Individu]:
        
        selected = []
        size_of_selection = len(individus) // 2

        # Trier les individus par fitness croissante (le pire en premier)
        individus_sorted = sorted(individus, key=lambda ind: ind.fitness)

        # Attribuer un rang à chaque individu (1 = pire, N = meilleur)
        N = len(individus_sorted)
        ranks = list(range(1, N + 1))  # [1, 2, ..., N]

        # Somme des rangs
        sum_of_ranks = sum(ranks)

        for _ in range(size_of_selection):
            r = random.uniform(0, sum_of_ranks)
            cumul = 0
            for ind, rank in zip(individus_sorted, ranks):
                cumul += rank
                if cumul >= r:
                    selected.append(ind)
                    break

        return selected

    # Séléction par tournoi
    def tournament(self, individus: list[Individu]) -> list[Individu]:

        selected = []
        size_of_selection = len(individus) // 2

        for _ in range(size_of_selection):
            # Choisir 2 individus au hasard
            concurrents = random.sample(individus, 2)
            # Prendre le meilleur du tournoi
            gagnant = max(concurrents, key=lambda ind: ind.fitness)
            selected.append(gagnant)

        return selected

    # Séléction par roulette
    def roulette(self, individus: list[Individu]) -> list[Individu]:

        selected = []
        size_of_selection = len(individus) // 2

        # Calculer la somme des fitness
        sum_fitness = sum(ind.fitness for ind in individus)

        for _ in range(size_of_selection):
            # Choisir un individu au hasard
            roulette_choisi = random.uniform(0, sum_fitness)
            cumul_fitness = 0
            for ind in individus:
                cumul_fitness += ind.fitness
                if cumul_fitness >= roulette_choisi:
                    selected.append(ind)
                    break
        return selected


    # Séléction par elimination des plus faibles
    def elitism(self, individus: list[Individu]) -> list[Individu]:

        # Trier les individus par fitness décroissante
        individus_sorted = sorted(individus, key=lambda ind: ind.fitness, reverse=True)
        
        # Garder la moitié des meilleurs
        half = len(individus_sorted) // 2
        return individus_sorted[:half]
