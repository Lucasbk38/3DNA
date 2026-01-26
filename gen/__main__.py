from gen.fitness import Fitness
from gen.crossover import Crossover
from gen.mutation import GaussianAdditiveMutation, GaussianMultiplicativeMutation, Mutation
from gen.selection import Roulette, Rank, Tournament, Elitism, Selection
from math import inf
from dna.Traj3D import Traj3D
import matplotlib.pyplot as plt
from dna.RotTable import RotTable
import numpy as np

def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, selection: Selection, mutation: Mutation, benchmark = False):
    fitness = Fitness()
    crossover = Crossover()
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
    eval = [0. for _ in range(generation_size)]

    if benchmark:
        list_best_fitness = []
    for g in range(num_generations):
        best_fitness = -inf
        for i in range(generation_size):
            eval[i] = fitness.evaluate(currentGeneration[i], traj3d, seq)

            if(benchmark and best_fitness < eval[i]):
                best_fitness = eval[i]

        if(benchmark):
            print(f"generation: {g}, best fitness {best_fitness}")
            list_best_fitness.append(best_fitness)
        selected = selection.select(currentGeneration, eval)
        crossed = crossover.make_full_population(selected, generation_size - len(selected))
        mutated = mutation.mutate_population(crossed)

        currentGeneration = selected + mutated
    

    best_fitness = -inf
    best_individual_index = 0
    for i in range(generation_size):
        f = fitness.evaluate(currentGeneration[i], traj3d, seq)
        if f > best_fitness:
            best_fitness = f
            best_individual_index = i
    
    if(benchmark):
        print(f"last generation, best fitness: {best_fitness}")
        plt.plot(range(num_generations),list_best_fitness,label=f"Sélection : {selection} et Mutation : {mutation} ")

    return currentGeneration[best_individual_index], best_fitness

def benchmark_selection_method(num_generations: int, generation_size: int, seq_filename: str):
    selections = { Elitism(), Roulette(), Rank(), Tournament() }
    mutations = { GaussianAdditiveMutation(), GaussianMultiplicativeMutation() }
    for selection in selections:
        for mutation in mutations:            
            genetic_algorithm(num_generations,generation_size,seq_filename, selection, mutation, True)
    plt.legend(loc = 1)
    plt.show()

def benchmark_sigma_tuning(num_generations: int, generation_size: int, seq_filename: str):
    for random_var in np.linspace(-1,1,10):
        sigma = 10**random_var
        mutation = GaussianAdditiveMutation(sigma)
        selection = Roulette()
        genetic_algorithm(num_generations,generation_size,seq_filename, selection, mutation, True)
    plt.legend(loc = 1)
    plt.show()

