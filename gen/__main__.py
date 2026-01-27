from gen.genetic import *

# genetic_algorithm(15,30,"data/plasmid_8k.fasta",Roulette(),GaussianAdditiveDeltaMutation(5),True,True,True)



benchmark(
    64, 64,
    "data/plasmid_8k.fasta",
    [ Roulette() ],
    [ SimulatedAnnealingMutation(ThresholdMutator(SimulatedAnnealingMutation(GaussianAdditiveDeltaMutation(sigma=10), key="sigma", alpha=.9), mutation_probability=1), key="mutation_probability", alpha=.9) for _ in range(8) ]
)