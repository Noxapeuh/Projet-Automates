# classe qui represente un automate
class Automate:
    # constructeur : on initialise tout a vide
    def __init__(self):
        self.etats = []          # liste des etats
        self.initial = []        # liste des etats initiaux
        self.final = []          # liste des etats finaux
        self.transitions = []    # matrice de transitions
        self.alphabet = []       # alphabet de l'automate
        self.correspondance = {} # correspondance des etats apres determinisation/minimisation

    # fonction qui calcule l'alphabet a partir des transitions
    def get_alphabet(self):
        alphabet = []
        nb_etats = len(self.etats)

        # on parcourt toute la matrice de transitions
        for i in range(nb_etats):
            for j in range(nb_etats):
                # pour chaque symbole dans la case [i][j]
                for symbole in self.transitions[i][j]:
                    # on n'ajoute pas epsilon et on evite les doublons
                    if symbole != 'eps' and symbole not in alphabet:
                        alphabet.append(symbole)

        # on trie l'alphabet
        alphabet.sort()
        self.alphabet = alphabet
        return self.alphabet
