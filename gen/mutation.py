from dna.RotTable import RotTable, rotTableConfig
from abc import ABC, abstractmethod
import numpy as np

class Mutation(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def mutateValue (self, e: float, delta: float, logFit: float) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def mutate(self, individu: RotTable, fitness: float) -> RotTable:
        rot_table_dict = {}
        logFit = np.log10(-fitness)

        for k, dinuc in individu.rot_table.items():
            rot_table_dict[k] = []
            for i, e in enumerate(dinuc):
                if e >= 2:
                    rot_table_dict[k].append(e)
                else:
                    center = rotTableConfig[k][i]
                    delta = rotTableConfig[k][3 + i]
                    mutated_value = self.mutateValue(e, delta, logFit)
                    rot_table_dict[k].append(float(np.clip(mutated_value, center - delta, center + delta)))

        return RotTable(rot_table_dict)
    
    def mutate_population(self, population: list[RotTable], fitnesses: list[float]):
        return [self.mutate(individu, fitness) for individu, fitness in zip(population, fitnesses)]
    

class ThresholdMutator(Mutation):
    def __init__(self, mutator: Mutation, mutation_probability = 0.1) -> None:
        super().__init__()

        self.mutator = mutator
        self.mutation_probability = mutation_probability

    def __str__(self) -> str:
        return f"T($p = {self.mutation_probability:.2f}$, {self.mutator})"
    
    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return self.mutator.mutateValue(e, delta, logFit) if np.random.random() <= self.mutation_probability else e

    
class GaussianMutator(Mutation):
    name = ""

    def __init__(self, sigma=1.) -> None:
        self.sigma = sigma

    def __str__(self) -> str:
        return f"{self.name}, $\\sigma = {self.sigma:.2f}$"
    
    def gaussian (self):
        return np.random.normal(0, self.sigma)
    
class GaussianAdditiveMutation(GaussianMutator):
    name = "G+"

    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return e + self.gaussian()

class GaussianAdditiveDeltaMutation(GaussianMutator):
    name = "G+$\\Delta$"

    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return e + self.gaussian() * delta
    
class GaussianMultiplicativeMutation(GaussianMutator):
    name = "G*"

    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return e * np.exp(self.gaussian())
    

class GaussianAdditiveDeltaLog10FitnessAnnealedMutation(GaussianMutator):
    name = "G+$\\DeltaF$"

    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return e + self.gaussian() * delta * logFit
    
class SimulatedAnnealingMutation(Mutation):
    """We lower the chance of mutation as the simulation goes on"""
    def __init__(self, mutator: Mutation, key: str, alpha = 1.) -> None:
        super().__init__()

        self.key = key
        self.alpha = alpha
        self.mutator = mutator

    def __str__(self) -> str:
        return f"SA({ self.mutator }, ${self.key}={self.alpha:.3f}^t$)"
    
    def mutate_population(self, population: list[RotTable], fitnesses: list[float]):
        mutated = super().mutate_population(population, fitnesses)

        setattr(self.mutator, self.key, getattr(self.mutator, self.key) * self.alpha)

        return mutated
    
    def mutateValue(self, e: float, delta: float, logFit: float) -> float:
        return self.mutator.mutateValue(e, delta, logFit)