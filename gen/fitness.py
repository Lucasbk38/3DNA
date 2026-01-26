from dna.Traj3D import Traj3D
from dna.RotTable import RotTable
import numpy as np

class Fitness():
    def __init__(self):
        pass

    def __str__(self) -> str:
        return "$-norm_2$"

    def evaluate(self, rot_table: RotTable, traj: Traj3D, seq: str):
        new_seq = seq + seq[0]
        assert new_seq[0] == new_seq[-1]

        return float(-np.linalg.norm(traj.compute(new_seq, rot_table), 2)) # Euclidean norm of the last point of the DNA (we search to minimize it)
