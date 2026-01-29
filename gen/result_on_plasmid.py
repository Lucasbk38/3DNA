from json import load as json_load
from dna.Traj3D import *
from gen.fitness import *

def any_rottable_result(rottable_filename : str,seq_filename: str):
    rottable = json_load(open(rottable_filename))
    fit = FitnessNorm2Last()
    traj = Traj3D(True)
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    seq = ''.join(lineList[1:])
    print(fit.evaluate(RotTable(rottable),traj,seq))
    traj.draw()

def best_rottable_8k():
    any_rottable_result("gen/best_rottable8k.json","data/plasmid_8k.fasta")


def best_rottable_180k():
    any_rottable_result("gen/best_rottable180k.json","data/plasmid_180k.fasta")