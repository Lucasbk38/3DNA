from gen.genetic import *

# genetic_algorithm(15,30,"data/plasmid_8k.fasta",Roulette(),GaussianAdditiveDeltaMutation(5),True,True,True)



benchmark(
    1024, 128,
    "data/plasmid_8k.fasta",
    [ TournamentWithHopeSelection(hopeProbability=.01) ],
    [ ThresholdMutator(SimulatedAnnealingMutation(GaussianAdditiveDeltaMutation(sigma=1), key="sigma", alpha=.99), mutation_probability=.2) for _ in range(1) ],
    [ FitnessWeightedMeanCrossover() ]
)