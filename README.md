# Projet Automates finis - EFREI S4

Projet de maths/info sur les automates finis, réalisé en Python. Le programme permet de charger un automate depuis un fichier texte et d'appliquer dessus les opérations classiques vues en cours.

## Le groupe

- **Rayan BELHOUS**
- **Cyril ROUSSELLE**
- **Mathis GUICHERD CALLIN**
- **Aliyane BENCHEHIDA**

## Ce que fait le programme

On peut :

- Lire un automate depuis un fichier `.txt`
- Afficher sa table de transitions (avec marquage des états initiaux/finaux)
- Vérifier s'il est déterministe, standard, complet
- Le **standardiser** (ajout d'un nouvel état initial `i`)
- Le **déterminiser et compléter** (construction par sous-ensembles + état poubelle)
- Le **minimiser** (algorithme de Moore, partitionnement successif)
- Tester la **reconnaissance d'un mot**
- Construire l'**automate complémentaire** (inversion des états finaux)
- Sauvegarder le résultat dans un fichier

## Structure du projet

```
.
├── automate.py          # Classe Automate (structure de données)
├── lecture.py           # Lecture/écriture des fichiers .txt
├── manipulation.py      # Toutes les opérations sur les automates
├── main.py              # Menu interactif (point d'entrée)
└── Automates_Test/      # Les 44 automates de test + sauvegardes
    ├── 01.txt
    ├── 02.txt
    ├── ...
    └── 44.txt
```

## Format des fichiers automates

Les automates sont décrits dans des fichiers `.txt` avec ce format :

```
etats: 0, 1, 2
initial: 0
finaux: 1, 2
transitions:
0, a, 1
0, b, 2
1, a, 2
```

Chaque transition c'est `état_départ, symbole, état_arrivée`. On peut aussi mettre des epsilon-transitions avec `eps` comme symbole.

## Lancer le programme

```bash
python main.py
```

Ça ouvre un menu dans le terminal. On choisit un numéro d'automate (de 1 à 44), et ensuite on a accès à toutes les opérations.

Pour lancer les tests sur tous les automates d'un coup :

```bash
python test_all.py
```

## Comment ça marche (en gros)

Les automates sont stockés sous forme de **matrice de transitions** (liste de listes). Chaque case `transitions[i][j]` contient la liste des symboles qui permettent d'aller de l'état `i` à l'état `j`.

La déterminisation utilise la **construction par sous-ensembles** : chaque nouvel état correspond à un ensemble d'anciens états. Si l'automate a des epsilon-transitions, on calcule l'epsilon-fermeture avant.

La minimisation passe par l'**algorithme de Moore** : on part avec 2 groupes (finaux / non-finaux) et on raffine jusqu'à ce que la partition soit stable.

## Remarques

- Le programme gère les epsilon-transitions (symbole `eps` dans les fichiers)
- Les sauvegardes sont versionnées automatiquement (`F10Version1.txt`, `F10Version2.txt`, etc.)
- Il faut déterminiser et compléter avant de pouvoir minimiser ou tester un mot
