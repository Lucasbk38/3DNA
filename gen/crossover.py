from dna.RotTable import RotTable
from random import randint

class Crossover():
    def __init__(self):
        self.name = "Mean"

    #Takes a population of selected individuals, then crosses them over to make generation_size individuals
    def make_full_population(self, selected_individuals: list[RotTable], num_children: int) -> list[RotTable]:
        n = len(selected_individuals)
        result = []
        #Only the first two parameters of the rotation list need to be crossed over,
        #The rest are fixed, this is reflected in this variable:
        num_params = 2
        for _ in range(num_children):
            parent1 = selected_individuals[randint(0, n - 1)]
            parent2 = selected_individuals[randint(0, n - 1)]

            rot_table_dict = {}
            for k,v in parent1.rot_table.items():
                rot_table_dict[k] = [((parent1[k][i] + parent2[k][i]) / 2) for i in range(num_params)]
                rot_table_dict[k] = [parent1[k][i] for i in range(num_params + 1, len(v))]
            
            result.append(RotTable(rot_table_dict))

        return result        
