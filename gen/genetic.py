from gen.fitness import Fitness
from gen.crossover import Crossover, MeanCrossover, FitnessWeightedMeanCrossover
from gen.mutation import GaussianAdditiveMutation, GaussianMultiplicativeMutation, GaussianAdditiveDeltaMutation, Mutation, SimulatedAnnealingMutation, ThresholdMutator
from gen.selection import Roulette, Rank, Tournament, Elitism, Selection
from math import inf
import statistics
from dna.Traj3D import Traj3D
import matplotlib.pyplot as plt
from dna.RotTable import RotTable
import numpy as np
from dna.RotTable import defaultRotTable
from json import dump as json_dump

def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, selection: Selection, crossover: Crossover, mutation: Mutation, benchmark = False, visualisation = False, comparison = False):
    fitness = Fitness()
    traj3d = Traj3D(visualisation)

    #Taken from dna.__main__
    # Read file
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    # Formatting
    seq = ''.join(lineList[1:])

    #make init generation
    currentGeneration = [RotTable.random() for i in range(generation_size)]
    eval = [0. for _ in range(generation_size)]

    
    list_best_fitness = []
    for g in range(num_generations):
        best_fitness = -inf
        for i in range(generation_size):
            eval[i] = fitness.evaluate(currentGeneration[i], traj3d, seq)

            if(benchmark and best_fitness < eval[i]):
                best_fitness = eval[i]

        if(benchmark):
            avg = sum(eval) / len(eval)
            sd = np.sqrt(sum([e ** 2 for e in eval]) / len(eval) - avg ** 2)
            print(f"generation: {g}, best fitness: {best_fitness}, med: {statistics.median(eval)}, avg: {avg}, sd: {sd}")
            list_best_fitness.append(best_fitness)
        selected = selection.select(currentGeneration, eval)
        crossed = crossover.make_full_population(selected, generation_size - len(selected), eval)
        mutated = mutation.mutate_population(crossed, g)

        currentGeneration = selected + mutated
    

    best_fitness = -inf
    best_individual_index = 0
    for i in range(generation_size):
        f = fitness.evaluate(currentGeneration[i], traj3d, seq)
        if f > best_fitness:
            best_fitness = f
            best_individual_index = i
    
    if benchmark and not visualisation:
        print(f"last generation, best fitness: {best_fitness}")
        plt.plot(range(num_generations), np.log10(-np.array(list_best_fitness)), label=f"Sélection: {selection} et Mutation: {mutation} ")

    if visualisation:
        traj3d.compute(seq,currentGeneration[best_individual_index],True)
        traj3d.draw()
    if comparison:
        fit = Fitness()
        traj = Traj3D(True)
        print(f"Before modifying the rotation table the last point had a norm of : {fit.evaluate(RotTable(defaultRotTable),traj,seq)}")
        traj.compute(seq,RotTable(defaultRotTable),True)
        traj.draw()
    
    return currentGeneration[best_individual_index], best_fitness

def benchmark(
    num_generations: int,
    generation_size: int,
    seq_filename: str,
    selections: list[Selection] = [ Elitism(), Roulette(), Rank(), Tournament() ],
    mutations: list[Mutation] = [ GaussianAdditiveMutation(), GaussianMultiplicativeMutation() ],
    crossovers: list[Crossover] = [ MeanCrossover() ]
):
    best_fitness = inf
    best_rottable = None
    for selection in selections:
        for mutation in mutations:
            for crossover in crossovers:
                print(f"{str(selection)} and {str(mutation)}")
                rottable, score = genetic_algorithm(num_generations,generation_size,seq_filename, selection, crossover, mutation, True, False)
                if score < best_fitness:
                    best_rottable, best_fitness = rottable, score
    plt.legend(loc = 1, prop={ 'size': 6 })
    plt.xlabel("Génération n")
    plt.ylabel("Norme du dernier point de la trajectoire pour le meilleur individu de la génération (échelle logarithmique)")
    plt.show()
    with open(f"best_rottable_{seq_filename}", 'w') as file:
            json_dump(best_rottable.rot_table, file)


def benchmark_sigma_tuning(num_generations: int, generation_size: int, seq_filename: str):
    for random_var in np.linspace(-0.4,-0.2,10):
        sigma = 10**random_var
        mutation = GaussianAdditiveDeltaMutation(sigma)
        selection = Roulette()
        crossover = MeanCrossover()
        genetic_algorithm(num_generations,generation_size,seq_filename, selection, crossover, mutation, True)
    plt.legend(loc = 1)
    plt.show()