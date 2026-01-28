from json import load as json_load
from dna.Traj3D import *
from gen.fitness import *

def best_rottable_8k():
    best_rottable8k = json_load("gen/best_rottable8k.json")
    del best_rottable8k["score"]
    fit = Fitness()
    traj = Traj3D()
    lineList = [line.rstrip('\n') for line in open("data/plasmid_8k.fasta")]
    seq = ''.join(lineList[1:])
    return fit.evaluate(RotTable(best_rottable8k),traj,seq)

def best_rottable_180k():
    best_rottable180k = json_load("gen/best_rottable180k.json")
    del best_rottable180k["score"]
    fit = Fitness()
    traj = Traj3D()
    lineList = [line.rstrip('\n') for line in open("data/plasmid_180k.fasta")]
    seq = ''.join(lineList[1:])
    return fit.evaluate(RotTable(best_rottable180k),traj,seq)

def any_rottable_result(rottable_filename : str,seq_filename: str):
    rottable = json_load(rottable_filename)
    fit = Fitness()
    traj = Traj3D()
    lineList = [line.rstrip('\n') for line in open(seq_filename)]
    seq = ''.join(lineList[1:])
    return fit.evaluate(RotTable(rottable),traj,seq)
