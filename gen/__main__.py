from gen.genetic import *
from gen.result_on_plasmid import any_rottable_result

# genetic_algorithm(15,30,"data/plasmid_8k.fasta",Roulette(),GaussianAdditiveDeltaMutation(5),True,True,True)

# np.random.seed()


benchmark(
    2048, 64,
    1/8, 1/8, 1/64,
    "data/plasmid_8k.fasta",
    [ TournamentWithHopeSelection(hopeProbability=.01) ],
    [
        # ThresholdMutation(SimulatedAnnealingMutation(GaussianAdditiveDeltaMutation(sigma=1), key="sigma", alpha=.995), mutation_probability=.2),
        ThresholdMutation(SimulatedAnnealingMutation(GaussianAdditiveDeltaLog10FitnessAnnealedMutation(sigma=10), key="sigma", alpha=.998), mutation_probability=.2)
    ],
    [ FitnessWeightedMeanCrossover() ],
    round=2
)

# any_rottable_result('1-9.json', 'data/plasmid_8k.fasta')