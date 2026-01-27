from dna.RotTable import RotTable
import random
import numpy as np
from abc import ABC, abstractmethod

class Selection(ABC):
    @abstractmethod
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Elitism(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Elitism"

    # Sélection par elimination des plus faibles
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:

        # Trier les individus par fitness décroissante
        individus_sorted = sorted(range(len(individus)), key=lambda i: fitness[i], reverse=True)
        
        # Garder la moitié des meilleurs
        half = len(individus_sorted) // 2
        return [individus[i] for i in individus_sorted[:half]]

class Tournament(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Tournament"
        
    # Sélection par tournoi
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        selected: list[RotTable] = []
        size_of_selection = len(individus) // 2 - 1

        for _ in range(size_of_selection):
            # Choisir 2 individus au hasard
            p1 = random.randint(0, len(individus) - 1)
            p2 = random.randint(0, len(individus) - 1)
            # Prendre le meilleur du tournoi
            if fitness[p1] > fitness[p2]:
                selected.append(individus[p1])
            else:
                selected.append(individus[p2])

        return [individus[max(range(len(individus)), key=lambda i: fitness[i])]] + selected


class Roulette(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Roulette"
    
    # Sélection par roulette
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        expFitness = np.exp(np.array(fitness) / 100)
        indices = np.random.choice(len(individus), len(individus)//2 - 1, p=expFitness / expFitness.sum())

        return [individus[max(range(len(individus)), key=lambda i: fitness[i])]] + [individus[i] for i in indices]


class Rank(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Rank"
    
    # Sélection par rang
    def select(self, individus: list[RotTable], fitness: list[float]):
        selected: list[RotTable] = []
        size_of_selection = len(individus) // 2 - 1

        # Trier les individus par fitness croissante (le pire en premier)
        individus_sorted = sorted(range(len(individus)), key=lambda i: fitness[i])

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
                    selected.append(individus[ind])
                    break

        return [individus[max(range(len(individus)), key=lambda i: fitness[i])]] + selected
    
class Tournament_with_hope(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Tournament"
        
    # Sélection par tournoi
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        selected: list[RotTable] = []
        size_of_selection = len(individus) // 2 - 1

        for _ in range(size_of_selection):
            # Choisir 2 individus au hasard
            p1 = random.randint(0, len(individus) - 1)
            p2 = random.randint(0, len(individus) - 1)
            # Prendre le meilleur du tournoi mais le pire a une chance
            p = random.uniform(0, 1)
            if p < 10**(-3):
                if fitness[p1] > fitness[p2]:
                    selected.append(individus[p2])
                else:
                    selected.append(individus[p2])
            # Tournoi normal
            else:
                if fitness[p1] > fitness[p2]:
                    selected.append(individus[p1])
                else:
                    selected.append(individus[p2])

        return [individus[max(range(len(individus)), key=lambda i: fitness[i])]] + selected
