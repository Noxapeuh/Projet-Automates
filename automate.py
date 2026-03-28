# classe automate
class Automate:
    # constructeur, tout a vide
    def __init__(self):
        self.etats = []          # les etats
        self.initial = []        # etats initiaux
        self.final = []          # etats finaux
        self.transitions = []    # matrice transitions
        self.alphabet = []       # alphabet
        self.correspondance = {} # correspondance etats apres determ/minim

    # calcule l'alphabet depuis les transitions
    def get_alphabet(self):
        alphabet = []
        nb_etats = len(self.etats)

        # parcours matrice transitions
        for i in range(nb_etats):
            for j in range(nb_etats):
                # chaque symbole dans la case [i][j]
                for symbole in self.transitions[i][j]:
                    # on ajoute pas eps et pas de doublons
                    if symbole != 'eps' and symbole not in alphabet:
                        alphabet.append(symbole)

        # tri
        alphabet.sort()
        self.alphabet = alphabet
        return self.alphabet
