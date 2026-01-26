from individu import Individu
from dna.Traj3D import Traj3D
import numpy as np

class Fitness():
    def __init__(self):
        pass

    def evaluate(self, rot_table: Individu, traj: Traj3D, seq: str) -> float:
        new_seq = seq + seq[0]
        assert(new_seq[0] == new_seq [-1])

        return np.linalg.norm(traj.compute(new_seq,rot_table),2) #Norm of the last point of the DNA (we search to minimize it)