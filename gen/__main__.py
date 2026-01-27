from gen.genetic import *

genetic_algorithm(15, 200, "data/plasmid_8k.fasta", Roulette(), Mean(), GaussianAdditiveDeltaMutation(5), True, True, True)