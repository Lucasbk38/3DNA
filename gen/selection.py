from dna.RotTable import RotTable
import random
import numpy as np
from abc import ABC, abstractmethod

class Selection(ABC):
    @abstractmethod
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        pass

class Elitism(Selection):
    # Sélection par elimination des plus faibles
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:

        # Trier les individus par fitness décroissante
        individus_sorted = sorted(range(len(individus)), key=lambda i: fitness[i], reverse=True)
        
        # Garder la moitié des meilleurs
        half = len(individus_sorted) // 2
        return [individus[i] for i in individus_sorted[:half]]

class Tournament(Selection):
    # Sélection par tournoi
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        selected = []
        size_of_selection = len(individus) // 2

        for _ in range(size_of_selection):
            # Choisir 2 individus au hasard
            p1 = random.randint(0, len(individus) - 1)
            p2 = random.randint(0, len(individus) - 1)
            # Prendre le meilleur du tournoi
            if fitness[p1] > fitness[p2]:
                selected.append(individus[p1])
            else:
                selected.append(individus[p2])

        return selected


class Roulette(Selection):
    # Sélection par roulette
    def select(self, individus: list[RotTable], fitness: list[float]) -> list[RotTable]:
        expFitness = np.exp(fitness)
        indices = np.random.choice(len(individus), len(individus)//2, p=expFitness / expFitness.sum())

        return [individus[i] for i in indices]


class Rank(Selection):
    # Sélection par rang
    def selection(self, individus: list[RotTable], fitness: list[float]):
        
        selected = []
        size_of_selection = len(individus) // 2

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

        return selected
