from dna.RotTable import RotTable, rotTableConfig
from typing import Callable
from abc import ABC, abstractmethod
import numpy as np



class Mutation(ABC):
    @abstractmethod
    def mutateValue (self, e: float, delta: float) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def mutate(self, individu: RotTable) -> RotTable:
        return RotTable({ k: [e if e >= 2 else float(np.clip( \
            self.mutateValue(e, rotTableConfig[k][3 + i]), rotTableConfig[k][i] - rotTableConfig[k][3 + i], \
            rotTableConfig[k][i] + rotTableConfig[k][3 + i])) for i, e in enumerate(dinuc)] \
            for k, dinuc in individu.rot_table.items() })
    
    def mutate_population(self, population: list[RotTable]):
        return [self.mutate(individu) for individu in population]
    

class GaussianMutation(Mutation):
    name = ""

    def __init__(self, sigma=1.) -> None:
        super().__init__()

        self.sigma = sigma

    def __str__(self) -> str:
        return f"{self.name}, $\\sigma = {self.sigma}$"
    
    def gaussian (self):
        return np.random.normal(0, self.sigma)
    
class GaussianAdditiveMutation(GaussianMutation):
    name = "G+"

    def mutateValue(self, e: float, delta: float) -> float:
        return e + self.gaussian()

class GaussianAdditiveDeltaMutation(GaussianMutation):
    name = "G+$\\Delta$"

    def mutateValue(self, e: float, delta: float) -> float:
        return e + self.gaussian() * delta
    
class GaussianMultiplicativeMutation(GaussianMutation):
    name = "G*"

    def mutateValue(self, e: float, delta: float) -> float:
        return e * np.exp(self.gaussian())
    
class SimulatedAnnealingMutation(Mutation):
    def __init__(self, mutationClass) -> None:
        super().__init__()

        self.mutationClass = mutationClass

    def __str__(self) -> str:
        return f"SA({ self.mutationClass.name })"
    
    def mutateValue(self, *args) -> float:
        return self.mutationClass().mutateValue(*args)