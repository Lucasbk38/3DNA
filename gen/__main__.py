from fitness import Fitness
from crossover import Crossover
from mutation import GaussianMultiplicativeMutation
from selection import Selection
from dna.Traj3D import Traj3D
from math import inf

def random_rot_table():
    pass


def genetic_algorithm(num_generations: int, generation_size: int, seq_filename: str, benchmark: bool):
    fitness = Fitness()
    crossover = Crossover()
    mutation = GaussianMultiplicativeMutation()
    selection = Selection()

    traj3d = Traj3D(False)

    #Taken from dna.__main__
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    seq = ''.join(lineList[1:])

    #make init generation
    currentGeneration = [random_rot_table() for i in range(generation_size)]
    eval = [0 for _ in range(generation_size)]

    for g in range(num_generations):
        best_fitness = inf
        for i in range(generation_size):
            eval[i] = fitness.evaluate(currentGeneration[i], traj3d, seq)

            if(benchmark and best_fitness > eval[i]):
                best_fitness = eval[i]

        if(benchmark):
            print(f"best fitness: {best_fitness} at generation {i}")
        
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
    
    if(benchmark):
        print(f"best fitness: {best_fitness} at last generation")

    return currentGeneration[best_individual_index], best_fitness