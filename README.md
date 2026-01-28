# ST2 (Théorie des Jeux) - EI Algorithmique Génétique

![CentraleSupelec Logo](https://www.centralesupelec.fr/sites/all/themes/cs_theme/medias/common/images/intro/logo_nouveau.jpg)


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
L'objectif de ce projet est de modifier le modèle de conformation 3D donné afin de rendre un plasmide circulaire. Pour cela, deux algorithmes seront développés :
- un recuit simulé, et
- un algorithme génétique

Ces algorithmes seront implantés en Python et structuré en classes (programmation orientée objet).

## Modélisation du problème

- Un individu sera une table de rotation
- Une mutation sera un changement de l'angle de rotation d'une séquence de 2 nucléotides dans la table de rotation
- Un enfant (une table de rotation) sera crée à partir des valeurs de ses parents (deux tables de rotations)
- Dans notre problème, on cherche à minimiser la distance entre le premier point de la trajectoire, qui est toujours (0, 0, 0), et le dernier point. On utilise donc comme fonction d’évaluation la norme euclidienne du dernier point. Dans le code, **on prend son opposé pour transformer le problème en maximisation**.
- Un individu sera sélectionné en fonction de son score, ie l'efficacité de la table de rotation à minimiser la distance entre le premier et le dernier nucléotide de la séquence.

## Algorithme génétique

On utilise un algorithme génétique classique qui suit ces étapes:
- **Initialisation** : On part d'une génération 0 de N individus générés aléatoirement.  
- **Évaluation** : On évalue chaque individu avec la fonction d'évaluation que l'on cherche à minimiser.  
- **Sélection** : On sélectionne, en introduisant ou non de l'aléatoire, une partie de nos individus selon certaines règles qui dépendent de leur évaluation.  
- **Reproduction** : On choisit deux parents parmi les individus sélectionnés et on construit un enfant avec les règles de construction qu'on a définies.  
- **Mutation** : On tire au sort certains individus (parfois uniquement les enfants) que l'on modifie légèrement.


On réitère les étapes autant de fois que l'on veut de générations. Une classe est implémentée pour chaque étape.


## Présentation du Dossier

Le dossier 3DNA contient 3 dossier:


- le dossier **dna** contient:
    - le fichier `Traj3D.py` implémentant le moteur de calcul d'une trajectoire 3D,
    - le fichier `Rot_Table.py` contenant la table de rotations (avec les écart-types) nécessaires au calcul d'une trajectoire 3D,
    - le fichier `main.py` illustrant un exemple d'utilisation de la classe Traj3D.

- le dossier **gen** contient:
    - le fichier `genetic.py` et `main.py` permettent de renvoyer le score du meilleur individu de la dernière génération. De plus, on obtient les courbes de la moyenne, la médiane, l'écart-type et le score du meilleur individu en fonction de la n-ème génération (échelle log).
    - le fichier `selection.py` définit les différentes méthodes de sélections à travers des classes (**Élitisme**, **Roulette**, **Rang**, **Tournoi** et **Tournoi avec espoir**)
    - le fichier `mutation.py` définit les différents types de mutations à travers des classes (**GaussianAdditiveMutation**, **GaussianAdditiveDeltaMutation**, **GaussianMultiplicativeMutation**, **GaussianAdditiveDeltaLog10FitnessAnnealedMutation**). De plus, **SimulatedAnnealingMutation** dans mutation.py retranscrit l'idée de **recuit simulé**
    - le fichier `crossover.py` définit les différents types de croisement à travers des classes (**MeanCrossover**, **FitnessWeightedMeanCrossover**, **ChooseBetweenParentsCrossover**)
    - le fichier `fitness.py` définit la manière d'évaluer un individu (l'opposé de la distance euclidenne entre le point départ et le point d'arrivée de la séquence d'ADN après avoir effectué les opérations de la table de rotation). On cherche à maximiser la fitness.
    - le fichier `result_on_plasmid.py` garde la meilleure table de rototation trouvée pour un plasmide de taille 8k et 180k

- le dossier **tests** contient tous les tests unitaires pour `mutation.py` (`test_mutation.py`), `selection.py` (`test_selection.py`), `RotTable.py` (`test_RotTable.py` (celui de l'énoncé)) et `crossover.py` (`test_crossover.py`) afin de s'assurer un bon recouvrement du code (au delà de 80%)

## Exécution du code

Pour exécuter genetic.py ou main.py, il suffit de saisir `python -m gen` dans le terminal.
Vous pouvez vous amuser en changeant le type de mutation, de sélection et de croisement.

Assurez-vous d'avoir installer les modules nécessaires dans `requirements.txt`
Le score du meilleur individu, la moyenne, la médiane et l'écart type seront donné pour chaque génération jusqu'à la dernière génération. Un graphique contenant les courbes s'affichera.



Pour exécuter tous les tests, il suffit de saisir `converage run -m pytest`
Pour voir le recouvrement d'un fichier, il suffit de saisir `python -m pytest tests/test_**nom_voulu**.py --cov=gen.**nom_voulu** --cov-report=term-missing`
Assurez-vous d'avoir installer le module `pytest` et `pytest-cov`






