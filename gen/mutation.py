from dna.RotTable import RotTable, rotTableConfig
from abc import ABC, abstractmethod
import numpy as np



class Mutation(ABC):
    @abstractmethod
    def mutateValue (self, e: float) -> float:
        pass

    def mutate(self, individu: RotTable) -> RotTable:
        return RotTable({ k: [e if e >= 2 else np.clip(self.mutateValue(e), dinuc[i] - dinuc[3 + i], dinuc[i] + dinuc[3 + i]) for i, e in enumerate(individu.rot_table[k])] for k, dinuc in individu.rot_table.items() })
    
    def mutate_population(self, population: list[RotTable]):
        return [self.mutate(individu) for individu in population]
    

class GaussianAdditiveMutation(Mutation):
    def __init__(self, sigma=1.) -> None:
        super().__init__()

        self.sigma = sigma

    def mutateValue(self, e: float) -> float:
        return e + np.random.normal(0, self.sigma)
    
class GaussianMultiplicativeMutation(Mutation):
    def __init__(self, sigma=1.) -> None:
        super().__init__()

        self.sigma = sigma

    def mutateValue(self, e: float) -> float:
        return e * np.exp(np.random.normal(0, self.sigma))