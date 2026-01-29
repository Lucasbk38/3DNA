# ST2 (Théorie des Jeux) - EI Algorithmique Génétique

![CentraleSupelec Logo](./CentraleSupelec%20Quadri%20UPSaclay.jpg)


## Membres

- Lucas Bello-Kern
- Arthur Hakimi
- Florian Song
- Farès Gati

## Contexte
Toutes les cellules qui constituent la vie sur Terre comportent en elles une ou plusieurs molécules d'ADN qui sont le support de l'information génétique. Ces molécules, plus ou moins longues, sont composées d'une succession de nucléotides (ou bases : A, C, G et T) qui interagissent avec de nombreux éléments cellulaires et dont le positionnement dans l'espace joue un rôle important dans l'adaptation de la cellule à son environnement (chaleur, famine, stress...). Si les séquences d'ADN sont aujourd'hui très largement étudiées à travers leur séquence textuelle (succession de A, C, G et T), il est très instructif de les étudier à partir de leur trajectoire tri-dimensionnelle. En 1993, des biopysiciens ont établi un modèle de conformation 3D qui permet de transformer une suite de nucléotides (sous forme de lettres) en une trajectoire tri-dimensionnelle. Dès lors, il est possible de représenter toute séquence textuelle d'ADN en une trajectoire 3D.

<img src="documents/RotTable.png" alt="Rotation Table" width="45%"/><img src="documents/Traj3D.png" alt="3D Trajectory Building" width="55%"/>

## Problématique
Ce modèle ayant été développé pour de courtes séquences d'ADN nu, il ne prend pas en compte toutes les caractéristiques d'une longue chaîne au sein de la cellule (surenroulements, nucléosomes, interactions longue distance...). Par exemple, si on observe un chromosome bactérien (longue séquence d'ADN constituant une bactérie) ou un plasmide (petite séquence présente au sein des bactéries), on s'aperçoit que ce chromosome ou ce plasmide est circulaire, i.e. les deux extrémités ont été "collées" l'une à l'autre. Le modèle pré-cité ne rend pas compte de ce phénomène lorsque l'on représente la trajectoire 3D d'un chromosome bactérien ou d'un plasmide.

## But et Objectif
L'objectif de ce projet est de modifier le modèle de conformation 3D donné afin de rendre un plasmide circulaire. Pour cela,  on a développé un algorithme génétique qui utilise la technique du recuit simulé pour affiner la recherche de modèle.

Ces algorithmes sont implementés en Python et structurés en classes (programmation orientée objet).


## Algorithme génétique

On utilise un algorithme génétique classique qui suit ces étapes:
- **Initialisation** : On part d'une génération 0 de N individus générés aléatoirement.  
- **Évaluation** : On évalue chaque individu avec la fonction d'évaluation que l'on cherche à minimiser ou maximiser.  
- **Sélection** : On sélectionne, en introduisant ou non de l'aléatoire, une partie de nos individus selon certaines règles qui dépendent de leur évaluation.  
- **Reproduction** : On choisit deux parents parmi les individus sélectionnés et on construit un enfant avec les règles de construction qu'on a définies.  
- **Mutation** : On tire au sort certains individus (parfois uniquement les enfants) que l'on modifie légèrement.


On réitère les étapes autant de fois que l'on veut de générations. Une classe est implémentée pour chaque étape.

## Modélisation du problème

- Un **individu** est une table de rotation.
- Une **mutation** est un changement de matrices de rotation dans la table de rotation représentant un individu.
- Un enfant (une table de rotation) est créé à partir des valeurs de ses parents (deux tables de rotation).
- Dans notre problème, on cherche à minimiser la distance entre le premier point de la trajectoire, qui est toujours $(0, 0, 0)$, et le dernier point. On utilise donc comme fonction d’évaluation la norme euclidienne du dernier point. Dans le code, on prend son opposé pour passer à un problème de maximisation.
- Un individu est sélectionné en fonction de son évaluation qui représente donc l'efficacité de la table de rotation à minimiser la distance entre le premier et le dernier nucléotide de la séquence.


## Présentation du Dossier

Le dossier 3DNA contient 3 dossiers:


- le dossier **dna** contient:
    - le fichier `Traj3D.py` implémentant le moteur de calcul d'une trajectoire 3D,
    - le fichier `Rot_Table.py` définissant la classe `RotTable`,
    - le fichier `table.json` contenant la table   de référence des matrice de rotations, avec les incertitudes sur chaque coefficient de ces matrices.
    - le fichier `main.py` permettant l'utilisation des fichiers ci-dessus. Pour ouvrir le menu d'aide tapez:
        > py -m dna -h


- le dossier **gen** contient:
    - le fichier `genetic.py` contient le corps de l'algorithme génétique dans la fonction `genetic_algorithm` et une fonction `benchmark` permettant de comparer les performances des différentes méthode de sélection, reproduction et mutation, de sauvegarder la table de matrices de rotation obtenue et d'obtenir une courbe traçant le logarithme de l'erreur de repliement du meilleur individu de la génération, l'écart type, la moyenne et la médiane des évaluations de notre génération.
    - le fichier `selection.py` définit les différentes méthodes de sélection à travers les classes (`ElitismSelection`, `TournamentSelection`, `RankSelection`, `TournamentWithHopeSelection` et `RouletteSelection`)
    - le fichier `mutation.py` définit les différents types de mutation à travers des classes (`GaussianAdditiveMutation`, `GaussianAdditiveDeltaMutation`, `GaussianMultiplicativeMutation`, `GaussianAdditiveDeltaLog10FitnessAnnealedMutation`). De plus, `SimulatedAnnealingMutation` applique la méthode de **recuit simulé** et `TresholdMutator` permet de définir la proportion de la population qui sera mutée d'une génération à l'autre. 
    - le fichier `crossover.py` définit les différents types de croisement à travers des classes (`MeanCrossover`, `FitnessWeightedMeanCrossover`, `ChooseBetweenParentsCrossover`)
    - le fichier `fitness.py` définit la manière d'évaluer un individu (l'opposé de la distance euclidenne entre le point départ et le point d'arrivée de la séquence d'ADN après avoir effectué les opérations de la table de rotation). On cherche à maximiser la fitness.
    - le fichier `result_on_plasmid.py` permet de tester une table de matrices de rotation sur une séquence de nucléotides données.

- le dossier **tests** contient tous les tests unitaires pour `mutation.py` (`test_mutation.py`), `selection.py` (`test_selection.py`), `RotTable.py` (`test_RotTable.py`) et `crossover.py` (`test_crossover.py`) afin de s'assurer un bon recouvrement du code (au delà de 80%)

## Exécution du code

Pour exécuter genetic.py ou main.py, il suffit de saisir 
> py -m gen 

dans le terminal (ou python3, ou python).

Les paramètres dans l'ordre sont le nombre de générations, la taille de la population, le pourcentage d'individus gardés, le taux de duplication, le taux de migration, le nom du fichier dans lequel est écrit le plasmide, le type de sélection, de mutation avec la probabilité de mutation et le facteur de diminution de l'écart-type, et le type de reproduction.
Vous pouvez vous amuser en changeant les arguments dans `main.py` 

Assurez-vous d'avoir installer les modules nécessaires dans `requirements.txt`
Le score du meilleur individu, la moyenne, la médiane et l'écart type seront donné pour chaque génération jusqu'à la dernière génération. Un graphique contenant les courbes s'affichera.



Pour exécuter tous les tests, il suffit de saisir `converage run -m pytest`
Pour voir le recouvrement d'un fichier, il suffit de saisir `python -m pytest tests/test_**nom_voulu**.py --cov=gen.**nom_voulu** --cov-report=term-missing`
Assurez-vous d'avoir installer le module `pytest` et `pytest-cov`






