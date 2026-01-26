from fitness import Fitness
from crossover import Crossover
from mutation import GaussianMultiplicativeMutation
from selection import Selection
from dna.Traj3D import Traj3D
from math import inf
import matplotlib.pyplot as plt
from dna.RotTable import RotTable


def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, selection_method: str, benchmark = False):
    fitness = Fitness()
    crossover = Crossover()
    mutation = GaussianMultiplicativeMutation()
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
    currentGeneration = [RotTable.random() for i in range(generation_size)]
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
        genetic_algorithm(num_generations,generation_size,seq_filename,method,True)
    plt.legend()
    plt.show()