from dna import RotTable
from fitness import Fitness
from crossover import Crossover
from mutation import Mutation
from selection import Selection
from dna.Traj3D import Traj3D
from math import inf
from random import uniform
from json import load as json_load
import matplotlib.pyplot as plt

def random_rot_table():
    rotTableConfig: dict[str, list[float]] = json_load(open('./dna/table.json'))
    random_rot_table = {[uniform(nuc[0] - nuc[4],nuc[0] + nuc[4]),uniform(nuc[1] - nuc[5],nuc[1] + nuc[5]),nuc[2]] for nuc in rotTableConfig}
    return(random_rot_table)


def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, selection_method: str, benchmark = False):
    fitness = Fitness()
    crossover = Crossover()
    mutation = Mutation()
    selection = Selection()

    traj3d = Traj3D(False)

    if benchmark: #if we want to plot the result
        best_indiv = []
    #Taken from dna.__main__
    # Read file
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    # Formatting
    seq = ''.join(lineList[1:])

    #make init generation
    currentGeneration = [random_rot_table() for i in range(generation_size)]
    eval = [0 for _ in range(generation_size)]

    for g in range(num_generations):
        for i in range(generation_size):
            eval[i] = fitness.evaluate(currentGeneration[i], traj3d, seq)
            if benchmark:
                best_indiv.append(max(eval))
        
        selected = selection.select(currentGeneration, selection_method)
        crossed = crossover.make_full_population(selected, generation_size - len(selected))
        mutated = mutation.mutate_population(selected)

        currentGeneration = crossed + mutated
    

    best_fitness = inf
    best_individual_index = 0
    for i in range(generation_size):
        f = fitness.evaluate(currentGeneration[i], traj3d, seq)
        if f < best_fitness:
            best_fitness = f
            best_individual_index = i

    if benchmark:
        plt.plot(list(range(num_generations)),best_indiv,label = f'{selection_method}')
    return currentGeneration[best_individual_index], best_fitness

def benchmark_selection_method(num_generations: int, generation_size: int, seq_filename: str):
    selection = Selection()
    for method in selection.method():
        genetic_algorithm(num_generations,generation_size,seq_filename,method)
    plt.legend()
    plt.show()