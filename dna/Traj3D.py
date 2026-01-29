#For drawing
import numpy as np
from numpy.typing import NDArray
from typing import Generator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dna.RotTable import RotTable


dinucleotidesComplementaryMap = {
    "TT": "AA",
    "GG": "CC",
    "TC": "GA",
    "GT": "AC",
    "CT": "AG",
    "TG": "CA",
}


class Traj3D:
    """Represents a 3D trajectory"""

    # Vertical translation (elevation) between two di-nucleotides
    __MATRIX_T = np.array(
        [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -3.38/2],
        [0, 0, 0, 1]]
    )

    def __init__(self, show=False):
        self.__Traj3D = []

        if show:
            self.fig = plt.figure()
            self.ax = plt.axes(projection='3d')

    def getTraj(self) -> list:
        return self.__Traj3D

    def compute(self, dna_seq: str, rot_table: RotTable, values=[-1], saveTraj=False) -> Generator[NDArray[np.float64]]:
        # Matrice cumulant l'ensemble des transformations géométriques engendrées par la séquence d'ADN
        total_matrix = np.eye(4)  # Identity matrix

        # On enregistre la position du premier nucléotide
        self.__Traj3D = [np.array([0.0, 0.0, 0.0, 1.0])]

        matrices_Rz: dict[str, NDArray[np.float64]] = {}
        matrices_Q: dict[str, NDArray[np.float64]] = {}
        dinucleotideMatrices: dict[str, NDArray[np.float64]] = {}

        values = set(e % (len(dna_seq) - 1) for e in values)

        # On parcourt la sequence, nucléotide par nucléotide
        for i in range(len(dna_seq) - 1):
            # On lit le dinucleotide courant
            dinucleotide = dna_seq[i] + dna_seq[i+1]
            # On remplit au fur et à mesure les matrices de rotation
            if dinucleotide not in matrices_Rz:
                matrices_Rz[dinucleotide], matrices_Q[dinucleotide] = \
                    self.__compute_matrices(rot_table, dinucleotide)
                
                dinucleotideMatrices[dinucleotide] = \
                    self.__MATRIX_T \
                    @ matrices_Rz[dinucleotide] \
                    @ matrices_Q[dinucleotide] \
                    @ matrices_Rz[dinucleotide] \
                    @ self.__MATRIX_T

            # On calcule les transformations géométriques
            # selon le dinucleotide courant,
            # et on les ajoute à la matrice totale
            total_matrix = total_matrix @ dinucleotideMatrices[dinucleotide]

            if i in values:
                yield (total_matrix @ self.__Traj3D[0]).T[:3]

            # On calcule la position du nucléotide courant
            # en appliquant toutes les transformations géométriques
            # à la position du premier nucléotide
            if saveTraj:
                self.__Traj3D.append(total_matrix @ self.__Traj3D[0])

    def __compute_matrices(self, rot_table: RotTable, rawDinucleotide: str):
        dinucleotide = dinucleotidesComplementaryMap.get(rawDinucleotide, rawDinucleotide)

        Omega = np.radians(rot_table.getTwist(dinucleotide))
        # Create rotation matrix of theta on Z axis
        matrices_Rz = \
            np.array([[np.cos(Omega/2), np.sin(Omega/2), 0, 0],
                        [-np.sin(Omega/2), np.cos(Omega/2), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        sigma = rot_table.getWedge(dinucleotide)
        delta = rot_table.getDirection(dinucleotide) * (1 if dinucleotide == rawDinucleotide else -1)
        alpha = np.radians(sigma)
        beta = np.radians(delta - 90)
        # Rotate of -beta on Z axis
        # Rotate of -alpha on X axis
        # Rotate of beta on Z axis
        matrices_Q = \
            np.array([[np.cos(-beta), np.sin(-beta), 0, 0],
                        [-np.sin(-beta), np.cos(-beta), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) \
            @ np.array([[1, 0, 0, 0],
                            [0, np.cos(-alpha), np.sin(-alpha), 0],
                            [0, -np.sin(-alpha), np.cos(-alpha), 0],
                            [0, 0, 0, 1]]) \
            @ np.array([[np.cos(beta), np.sin(beta), 0, 0],
                        [-np.sin(beta), np.cos(beta), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        
        return matrices_Rz, matrices_Q

    def draw(self):
        xyz = np.array(self.__Traj3D)
        print(xyz)
        x, y, z = xyz[:,0], xyz[:,1], xyz[:,2]
        self.ax.plot(x,y,z)
        plt.show()

    def save_fig(self, filename: str):
        self.fig.savefig(filename)

    def save_coords(self, filename: str):
        with open(filename, 'w') as f:
            for i in range(len(self.__Traj3D)):
                f.write(f"{self.__Traj3D[i][0]},{self.__Traj3D[i][1]},{self.__Traj3D[i][2]}\n")
            f.close()