from dna.RotTable import RotTable
from random import randint

class Crossover():
    def __init__(self):
        self.name = "Mean"

    #Takes a population of selected individuals, then crosses them over to make generation_size individuals
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int) -> list[RotTable]:
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
