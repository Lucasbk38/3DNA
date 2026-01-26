from individu import Individu
import random

class Selection():
    def select(self, individus: list[Individu], methode: str) -> list[Individu]:
        if methode == "elitism":
            return self.elitism(individus)
        elif methode == "roulette":
            return self.roulette(individus)
        elif methode == "tournament":
            return self.tournament(individus)
        elif methode == "rank":
            return self.rank(individus)
        else:
            raise ValueError(f"Méthode de sélection inconnue : {methode}")
        
    # Séléction par rang
    def rank(self, individus: list[Individu]) -> list[Individu]:
        
        selectionnes = []
        taille_selection = len(individus) // 2

        # Trier les individus par fitness croissante (le pire en premier)
        individus_tries = sorted(individus, key=lambda ind: ind.fitness)

        # Attribuer un rang à chaque individu (1 = pire, N = meilleur)
        N = len(individus_tries)
        rangs = list(range(1, N + 1))  # [1, 2, ..., N]

        # Somme des rangs
        somme_rangs = sum(rangs)

        for _ in range(taille_selection):
            r = random.uniform(0, somme_rangs)
            cumul = 0
            for ind, rang in zip(individus_tries, rangs):
                cumul += rang
                if cumul >= r:
                    selectionnes.append(ind)
                    break

        return selectionnes

    # Séléction par tournoi
    def tournament(self, individus: list[Individu]) -> list[Individu]:

        selectionnes = []
        taille_selection = len(individus) // 2

        for _ in range(taille_selection):
            # Choisir 2 individus au hasard
            concurrents = random.sample(individus, 2)
            # Prendre le meilleur du tournoi
            gagnant = max(concurrents, key=lambda ind: ind.fitness)
            selectionnes.append(gagnant)
        
        return selectionnes

    # Séléction par roulette
    def roulette(self, individus: list[Individu]) -> list[Individu]:

        selectionnes = []
        taille_selection = len(individus) // 2

        # Calculer la somme des fitness
        somme_fitness = sum(ind.fitness for ind in individus)

        for _ in range(taille_selection):
            # Choisir un individu au hasard
            roulette_choisi = random.uniform(0, somme_fitness)
            cumul_fitness = 0
            for ind in individus:
                cumul_fitness += ind.fitness
                if cumul_fitness >= roulette_choisi:
                    selectionnes.append(ind)
                    break
        return selectionnes



    # Séléction par elimination des plus faibles
    def elitism(self, individus: list[Individu]) -> list[Individu]:

        # Trier les individus par fitness décroissante
        individus_tries = sorted(individus, key=lambda ind: ind.fitness, reverse=True)
        
        # Garder la moitié des meilleurs
        moitié = len(individus_tries) // 2
        return individus_tries[:moitié]

