class Automate:
    # ============================================================================================
    # Fonction : __init__
    # Role : Constructeur de la classe Automate. Initialise tous les attributs d'un automate vide.
    # Parametres : Aucun (self uniquement)
    # ============================================================================================
    def __init__(self):
        self.etats = []          # Liste des états de l'automate (ex: ['0', '1', '2'])
        self.initial = []        # Liste des états initiaux (ex: ['0'])
        self.final = []          # Liste des états finaux/terminaux (ex: ['1', '2'])
        self.transitions = []    # Matrice NxN : transitions[i][j] = liste des symboles pour aller de i à j
        self.alphabet = []       # Alphabet de l'automate (ex: ['a', 'b']), déduit des transitions
        self.correspondance = {} # Dictionnaire de correspondance des états (utilisé après déterminisation/minimisation)

    # ============================================================================================
    # Fonction : get_alphabet
    # Role : Parcourt toute la matrice de transitions pour en extraire l'alphabet (les symboles
    #        utilisés dans les transitions). Les epsilon-transitions ('eps') ne font PAS partie
    #        de l'alphabet. Le résultat est trié par ordre alphabétique.
    # Parametres : Aucun (self uniquement)
    # ============================================================================================
    def get_alphabet(self):
        alphabet = set()  # On utilise un set pour éviter les doublons automatiquement
        nb_etats = len(self.etats)

        # On parcourt chaque case de la matrice de transitions
        # Boucle i : parcourt les lignes (état de départ)
        # Boucle j : parcourt les colonnes (état d'arrivée)
        for i in range(nb_etats):
            for j in range(nb_etats):
                # Pour chaque symbole présent dans la case transitions[i][j]
                for symbole in self.transitions[i][j]:
                    # On n'ajoute pas epsilon à l'alphabet car ce n'est pas un vrai symbole
                    if symbole != 'eps':
                        alphabet.add(symbole)

        # On trie l'alphabet pour avoir un ordre cohérent (a, b, c, ...)
        self.alphabet = sorted(list(alphabet))
        return self.alphabet
