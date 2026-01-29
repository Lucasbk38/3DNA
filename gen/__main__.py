from gen.genetic import *
from gen.result_on_plasmid import any_rottable_result
from gen.mutation import *
# genetic_algorithm(15,30,"data/plasmid_8k.fasta",Roulette(),GaussianAdditiveDeltaMutation(5),True,True,True)

# np.random.seed()


benchmark(
    512, 64,
    1/8, 1/8, 1/64,
    "data/plasmid_8k.fasta",
    [ TournamentWithHopeSelection(hopeProbability=.01) ],
    [
        GaussianAdditiveMutation(1),
        GaussianMultiplicativeMutation(1),
        GaussianAdditiveDeltaMutation(1),
        GaussianAdditiveDeltaLog10FitnessAnnealedMutation(5),
        ThresholdMutation(GaussianAdditiveDeltaMutation(1),0.2),
        ThresholdMutation(GaussianAdditiveDeltaMutation(1),0.1),
        ThresholdMutation(GaussianAdditiveDeltaMutation(1),0.4),
        SimulatedAnnealingMutation(GaussianAdditiveDeltaMutation(sigma=1), key="sigma", alpha=.998),
        SimulatedAnnealingMutation(GaussianAdditiveDeltaMutation(sigma=1), key="sigma", alpha=.98),
        ThresholdMutation(SimulatedAnnealingMutation(GaussianAdditiveDeltaLog10FitnessAnnealedMutation(sigma=10), key="sigma", alpha=.998), mutation_probability=.2)
    ],
    [ FitnessWeightedMeanCrossover() ],
    round=3
)

#any_rottable_result('gen/3-12.json', 'data/plasmid_8k.fasta')
#any_rottable_result('gen/182824nucleotide_-5.264791933376954e-10.json','data/plasmid_180k.fasta')