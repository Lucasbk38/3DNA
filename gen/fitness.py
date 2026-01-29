from abc import ABC, abstractmethod
from dna.Traj3D import Traj3D
from dna.RotTable import RotTable
import numpy as np



class Fitness(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, rot_table: RotTable, traj: Traj3D, seq: str) -> float:
        pass
    

class FitnessNorm2Last(Fitness):
    def __init__(self):
        pass

    def __str__(self) -> str:
        return "$-{\\sigma||\\cdot||}_2$"

    def evaluate(self, rot_table: RotTable, traj: Traj3D, seq: str):
        [x] = list(traj.compute(seq + seq[:1], rot_table))

        return float(-np.linalg.norm(x, 2) / 2) # Minus euclidean norm of the last point of the DNA (we search to minimize it)
    

class FitnessNorm2AvgLast2(Fitness):
    def __init__(self):
        pass

    def __str__(self) -> str:
        return "$-{\\sigma||\\cdot||}_2/2$"

    def evaluate(self, rot_table: RotTable, traj: Traj3D, seq: str):
        [a, b, c] = list(traj.compute(seq + seq[:2], rot_table, values=[1, -2, -1]))

        d1 = np.linalg.norm(b, 2)
        d2 = np.linalg.norm(a - c, 2)

        return float(-(d1 + d2) / 2) # Minus euclidean norm of the last point of the DNA (we search to minimize it)
    

