from dna.RotTable import RotTable, rotTableConfig
from abc import ABC, abstractmethod
import numpy as np
from random import random

class Mutation(ABC):
    def __init__(self, mutation_probability: float) -> None:
        super().__init__()
        self.mutation_probability = mutation_probability

    @abstractmethod
    def mutateValue (self, e: float, delta: float) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def mutate(self, individu: RotTable) -> RotTable:
        rot_table_dict = {}

        for k, dinuc in individu.rot_table.items():
            rot_table_dict[k] = []
            for i, e in enumerate(dinuc):
                if e >= 2:
                    rot_table_dict[k].append(e)
                else:
                    p = random()

                    if p <= self.mutation_probability:
                        center = rotTableConfig[k][i]
                        delta = rotTableConfig[k][3 + i]
                        mutated_value = self.mutateValue(e, delta)
                        rot_table_dict[k].append(float(np.clip(mutated_value, center - delta, center + delta)))
                    else:
                        rot_table_dict[k].append(e)

        return RotTable(rot_table_dict)
    
    def mutate_population(self, population: list[RotTable]):
        return [self.mutate(individu) for individu in population]
    

class GaussianMutation(Mutation):
    name = ""

    def __init__(self, mutation_probability: float = 0.1, sigma=1.) -> None:
        super().__init__(mutation_probability)

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
    def __init__(self, mutationClass, mutation_probability= 0.1) -> None:
        super().__init__(mutation_probability)

        self.mutationClass = mutationClass

    def __str__(self) -> str:
        return f"SA({ self.mutationClass.name })"
    
    def mutateValue(self, e: float, delta: float) -> float:
        return self.mutationClass(1).mutateValue(e, delta)