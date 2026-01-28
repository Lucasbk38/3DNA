from gen.fitness import Fitness
from gen.crossover import Crossover, MeanCrossover, FitnessWeightedMeanCrossover
from gen.mutation import GaussianAdditiveMutation, GaussianMultiplicativeMutation, GaussianAdditiveDeltaMutation, Mutation, SimulatedAnnealingMutation, ThresholdMutation, GaussianAdditiveDeltaLog10FitnessAnnealedMutation
from gen.selection import RouletteSelection, RankSelection, TournamentSelection, Elitism, Selection, TournamentWithHopeSelection
from math import inf
import statistics
from dna.Traj3D import Traj3D
import matplotlib.pyplot as plt
from dna.RotTable import RotTable
import numpy as np
from dna.RotTable import defaultRotTable
from json import dump as json_dump
from json import load as json_load

def genetic_algorithm(num_generations: int, generation_size: int, keepRate: float, duplicateRate: float, seq_filename: str, selection: Selection, crossover: Crossover, mutation: Mutation, benchmark = False, visualisation = False, comparison = False):
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

        kept = selected + mutated

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
    
    if benchmark and not visualisation:
        print(f"last generation, best fitness: {best_fitness}")
        plt.plot(range(num_generations), np.log10(-np.array(list_best_fitness)), label=f"Avg - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
        plt.plot(range(num_generations), -5 * np.log10(-np.array(list_avg)), label=f"Avg - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
        plt.plot(range(num_generations), -5 * np.log10(np.array(list_std)), label=f"Std - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")
        # plt.plot(range(num_generations), -5 * np.log10(-np.array(list_medians)), label=f"Med - Sélection: {selection}; Mutation: {mutation}; Crossover: {crossover}")

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
    keepRate: float,
    duplicateRate: float,
    seq_filename: str,
    selections: list[Selection] = [ Elitism(), RouletteSelection(), RankSelection(), TournamentSelection() ],
    mutations: list[Mutation] = [ GaussianAdditiveMutation(), GaussianMultiplicativeMutation() ],
    crossovers: list[Crossover] = [ MeanCrossover() ]
):
    best_fitness = inf
    best_rottable = None
    
    for selection in selections:
        for mutation in mutations:
            for crossover in crossovers:
                print(f"{str(selection)} and {str(mutation)}")
                rottable, score = genetic_algorithm(num_generations, generation_size, keepRate, duplicateRate, seq_filename, selection, crossover, mutation, True, False)
                if score < best_fitness:
                    best_rottable, best_fitness = rottable, score
    plt.legend(loc = 3, prop={ 'size': 6 })
    plt.xlabel("Génération n")
    plt.ylabel("Evaluation du meilleur individu de la génération (échelle logarithmique)")
    plt.savefig('fig.png')
    plt.show()
    if seq_filename == "data/plasmid_8k.fasta":
        rotTableref = json_load(open('gen/best_rottable8k.json'))
        if best_fitness > rotTableref["score"]:
            with open("gen/best_rottable8k.json", 'w') as file:
                best_rottable.rot_table["score"] = best_fitness
                json_dump(best_rottable.rot_table, file, indent = 4)
    if seq_filename == "data/plasmid_180k.fasta":
        rotTableref = json_load(open('gen/best_rottable180k.json'))
        if best_fitness > rotTableref["score"]:
            with open("gen/best_rottable180k.json", 'w') as file:
                best_rottable.rot_table["score"] = best_fitness
                json_dump(best_rottable.rot_table, file, indent = 4)