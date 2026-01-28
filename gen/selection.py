from dna.RotTable import RotTable
import random
import numpy as np
from abc import ABC, abstractmethod

class Selection(ABC):
    @abstractmethod
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]) -> list[int]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class ElitismSelection(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Elitism"

    # Sélection par elimination des plus faibles
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]) -> list[int]:

        # Trier les indices des individus par fitness décroissante
        individus_sorted = sorted(range(len(individus)), key=lambda i: fitness[i], reverse=True)
        
        # Garder les indices correspondants aux meilleurs individus (le nombre de places est défini par le keepRate)
        return individus_sorted[:int(keepRate * len(individus))]

class TournamentSelection(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Tournament"
        
    # Sélection par tournoi
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]) -> list[int]:
        selected: list[int] = []
        size_of_selection = int(keepRate * len(individus)) - 1

        for _ in range(size_of_selection):
            # Choisir l'indice de 2 individus au hasard
            p1 = random.randint(0, len(individus) - 1)
            p2 = random.randint(0, len(individus) - 1)
            # Prendre l'indice de l'individu avec le meilleur score au tournoi
            if fitness[p1] > fitness[p2]:
                selected.append(p1)
            else:
                selected.append(p2)

        return [max(range(len(individus)), key=lambda i: fitness[i])] + selected


class RouletteSelection(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Roulette"
    
    # Sélection par roulette
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]) -> list[int]:
        expFitness = np.exp(np.array(fitness) / 100)
        
        # Sélectionner les indices des individus par roulette avec un nombre de places défini par le keepRate
        indices = np.random.choice(len(individus), int(keepRate * len(individus)) - 1, p=expFitness / expFitness.sum())

        # Conversion en int
        indices = [int(i) for i in indices]

        return [max(range(len(individus)), key=lambda i: fitness[i])] + list(indices)


class RankSelection(Selection):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Rank"
    
    # Sélection par rang
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]):
        selected: list[int] = []
        size_of_selection = int(keepRate * len(individus)) - 1

        # Trier les indices des individus selon leur score (le pire en premier)
        individus_sorted = sorted(range(len(individus)), key=lambda i: fitness[i])

        # Attribuer un rang à chaque individu (1 = pire, N = meilleur)
        N = len(individus_sorted)
        ranks = list(range(1, N + 1))  # [1, 2, ..., N]

        # Somme des rangs
        sum_of_ranks = sum(ranks)

        # Sélectionner les indices des individus par roulette basée sur les rangs (nombre de places défini par le keepRate)
        for _ in range(size_of_selection):
            r = random.uniform(0, sum_of_ranks)
            cumul = 0
            for ind, rank in zip(individus_sorted, ranks):
                cumul += rank
                if cumul >= r:
                    selected.append(ind)
                    break

        return [max(range(len(individus)), key=lambda i: fitness[i])] + selected
    
class TournamentWithHopeSelection(Selection):
    def __init__(self, hopeProbability = 0.001):
        super().__init__()
        self.hopeProbability = hopeProbability

    def __str__(self) -> str:
        return f"TwH($hp={self.hopeProbability}$)"
        
    # Sélection par tournoi
    def select(self, keepRate: float, individus: list[RotTable], fitness: list[float]) -> list[int]:
        selected: list[int] = []
        size_of_selection = int(keepRate * len(individus)) - 1

        for _ in range(size_of_selection):
            # Choisir les indices de 2 individus au hasard
            p1 = random.randint(0, len(individus) - 1)
            p2 = random.randint(0, len(individus) - 1)
            # Prendre l'indice du meilleur du tournoi mais le pire peut avoir une chance
            p = random.uniform(0, 1)
            if p < self.hopeProbability:
                if fitness[p1] > fitness[p2]:
                    selected.append(p2)
                else:
                    selected.append(p2)
            # Tournoi normal
            else:
                if fitness[p1] > fitness[p2]:
                    selected.append(p1)
                else:
                    selected.append(p2)

        return [max(range(len(individus)), key=lambda i: fitness[i])] + selected
