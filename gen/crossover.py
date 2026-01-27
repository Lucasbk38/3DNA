from dna.RotTable import RotTable
from random import randint, random
from abc import ABC, abstractmethod

class Crossover(ABC):
    @abstractmethod
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int, fitness: list[float]) -> list[RotTable]:
        pass

class MeanCrossover(Crossover):
    #Takes a population of selected individuals, then crosses them over to make generation_size individuals
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int, fitness: list[float]) -> list[RotTable]:
        n = len(selected_individuals)
        result = []
        for _ in range(num_children):
            parent1 = selected_individuals[randint(0, n - 1)]
            parent2 = selected_individuals[randint(0, n - 1)]

            rot_table_dict = {}
            for k,v in parent1.rot_table.items():
                rot_table_dict[k] = [((parent1.rot_table[k][i] + parent2.rot_table[k][i]) / 2) for i in range(len(v))]
            
            result.append(RotTable(rot_table_dict))

        return result 

class FitnessWeightedMeanCrossover(Crossover):
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int, fitness: list[float]) -> list[RotTable]:
        n = len(selected_individuals)
        result = []
        for _ in range(num_children):
            parent_index1 = randint(0, n - 1)
            parent_index2 = randint(0, n - 1)
            parent1 = selected_individuals[parent_index1]
            parent2 = selected_individuals[parent_index2]

            rot_table_dict = {}
            for k,v in parent1.rot_table.items():
                #On multiplie par la fitenss de l'autre parent car plus grande est la fitness en valeur absolute,
                #plus elle est mauvaise (car la fitness est négative)
                rot_table_dict[k] = [(parent1.rot_table[k][i] * fitness[parent_index2] + parent2.rot_table[k][i] * fitness[parent_index1]) \
                                      / (fitness[parent_index1] + fitness[parent_index2]) for i in range(len(v))]
            
            result.append(RotTable(rot_table_dict))

        return result
    
class ChooseBetweenParentsCrossover(Crossover):
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int, fitness: list[float]) -> list[RotTable]:
        n = len(selected_individuals)
        result = []
        for _ in range(num_children):
            parent1 = selected_individuals[randint(0, n - 1)]
            parent2 = selected_individuals[randint(0, n - 1)]

            rot_table_dict = {}
            for k,v in parent1.rot_table.items():
                rot_table_dict[k] = []
                for i in range(len(v)):
                    p = random()
                    if p <= 0.5:
                        rot_table_dict[k].append(parent1.rot_table[k][i])
                    else:
                        rot_table_dict[k].append(parent2.rot_table[k][i])

            
            result.append(RotTable(rot_table_dict))

        return result