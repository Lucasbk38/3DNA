from gen.fitness import Fitness, FitnessNorm2Last, FitnessNorm2AvgLast2
from gen.crossover import Crossover, MeanCrossover, FitnessWeightedMeanCrossover
from gen.mutation import GaussianAdditiveMutation, GaussianMultiplicativeMutation, GaussianAdditiveDeltaMutation, Mutation, SimulatedAnnealingMutation, ThresholdMutation, GaussianAdditiveDeltaLog10FitnessAnnealedMutation
from gen.selection import RouletteSelection, RankSelection, TournamentSelection, ElitismSelection, Selection, TournamentWithHopeSelection
from math import inf
import statistics
from dna.Traj3D import Traj3D
import matplotlib.pyplot as plt
from typing import Callable
from dna.RotTable import RotTable
import numpy as np
from dna.RotTable import defaultRotTable
from json import dump as json_dump
from json import load as json_load
import os

def genetic_algorithm(num_generations: int, generation_size: int, keepRate: float, duplicateRate: float, saltRate: float, seq_filename: str, selection: Selection, crossover: Crossover, mutation: Mutation, fitness: Fitness, init_gen = RotTable.random, benchmark = False, visualisation = False, comparison = False):
    traj3d = Traj3D(visualisation)

    #Taken from dna.__main__
    # Read file
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    # Formatting
    seq = ''.join(lineList[1:])

    #make init generation
    currentGeneration = [init_gen() for i in range(generation_size)]
    eval = [0. for _ in range(generation_size)]

    
    list_best_fitness = []
    list_medians = []
    list_avg = []
    list_std = []
    for g in range(num_generations):
        best_fitness = -inf
        for i in range(generation_size):
            eval[i] = fitness.evaluate(currentGeneration[i], traj3d, seq)

            if(benchmark and best_fitness < eval[i]):
                best_fitness = eval[i]

        if(benchmark):
            avg = statistics.mean(eval)
            std = statistics.stdev(eval)
            med = statistics.median(eval)

            list_medians.append(med)
            list_avg.append(avg)
            list_std.append(std)

            list_best_fitness.append(best_fitness)
            print(f"generation: {g}, best fitness: {best_fitness}, med: {med}, avg: {avg}, sd: {std}")
        selectedIndices = selection.select(keepRate, currentGeneration, eval)
        selected = [currentGeneration[i] for i in selectedIndices]
        mutated: list[RotTable] = []

        for _ in range(int(generation_size * duplicateRate)):
            i: int = np.random.choice(selectedIndices)
            mutated.append(mutation.mutate(currentGeneration[i], eval[i]))

        kept = selected + mutated + [RotTable.random() for _ in range(int(generation_size * saltRate))]

        crossed = crossover.make_full_population(kept, generation_size - len(kept), eval)
        mutatedChildren = mutation.mutate_population(crossed, eval)

        currentGeneration = kept + mutatedChildren
    

    best_fitness = -inf
    best_individual_index = 0
    for i in range(generation_size):
        f = fitness.evaluate(currentGeneration[i], traj3d, seq)
        if f > best_fitness:
            best_fitness = f
            best_individual_index = i

    # plt.plot(range(num_generations), -5 * np.log10(-np.array(list_avg)), label=f"Avg - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
    # plt.plot(range(num_generations), -5 * np.log10(np.array(list_std)), label=f"Std - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
    # plt.plot(range(num_generations), -5 * np.log10(-np.array(list_medians)), label=f"Med - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")

    if visualisation:
        traj3d.compute(seq,currentGeneration[best_individual_index],True)
        traj3d.draw()
    if comparison:
        traj = Traj3D(True)
        print(f"Before modifying the rotation table the last point had a norm of : {fitness.evaluate(RotTable(defaultRotTable),traj,seq)}")
        traj.compute(seq,RotTable(defaultRotTable),True)
        traj.draw()
    
    return currentGeneration[best_individual_index], best_fitness, list_best_fitness

def benchmark(
    num_generations: int,
    generation_size: int,
    keepRate: float,
    duplicateRate: float,
    saltRate: float,
    seq_filename: str,
    selections: list[Selection] = [ ElitismSelection(), RouletteSelection(), RankSelection(), TournamentSelection() ],
    mutations: list[Mutation] = [ GaussianAdditiveMutation(), GaussianMultiplicativeMutation() ],
    crossovers: list[Crossover] = [ MeanCrossover() ],
    fitnesses: list[Fitness] = [ FitnessNorm2Last() ],
    init_gen=RotTable.random,
    round = 1
):
    best_fitness = -inf
    best_rottable = None
    
    for selection in selections:
        for mutation in mutations:
            for crossover in crossovers:
                for fitness in fitnesses:
                    print(f"{selection}, {crossover} and {mutation}")

                    list_best_fitness_log_avg = np.array([0] * num_generations)

                    for _ in range(round):
                        rottable, score, list_best_fitness = genetic_algorithm(num_generations, generation_size, keepRate, duplicateRate, saltRate, seq_filename, selection, crossover, mutation, fitness, init_gen, True, False)
                        list_best_fitness_log_avg = list_best_fitness_log_avg + np.log(-np.array(list_best_fitness))
                        if score > best_fitness:
                            best_rottable, best_fitness = rottable, score

                    plt.plot(range(num_generations), list_best_fitness_log_avg / round, label=f"Avg log best - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
                    
    plt.legend(loc = 3, prop={ 'size': 6 })
    plt.xlabel("Génération n")
    plt.ylabel("Evaluation du meilleur individu de la génération (échelle logarithmique)")
    plt.savefig('fig.png')
    plt.show()
    dir = "gen"
    with open(seq_filename, 'r', encoding='utf-8') as file:
        seq = file.read()
    nb_nucleotide = len(seq)
    fichier = os.path.join(dir, f"{nb_nucleotide}nucleotide_{best_fitness}.json")
    with open(fichier, 'w') as file:
                best_rottable.rot_table["score"] = [best_fitness]
                json_dump(best_rottable.rot_table,file,indent = 4)
