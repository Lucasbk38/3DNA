from dna import RotTable
from fitness import Fitness
from crossover import Crossover
from mutation import Mutation
from selection import Selection
from dna.Traj3D import Traj3D
from math import inf

def random_rot_table():
    pass


def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, benchmark: bool):
    fitness = Fitness()
    crossover = Crossover()
    mutation = Mutation()
    selection = Selection()

    traj3d = Traj3D(False)

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
        
        selected = selection.select()
        crossed = crossover.make_full_population(selected, generation_size)
        mutated = mutation.mutate_population(crossed)

        currentGeneration = mutated
    

    best_fitness = inf
    best_individual_index = 0
    for i in range(generation_size):
        f = fitness.evaluate(currentGeneration[i], traj3d, seq)
        if f < best_fitness:
            best_fitness = f
            best_individual_index = i

    return currentGeneration[best_individual_index], best_fitness