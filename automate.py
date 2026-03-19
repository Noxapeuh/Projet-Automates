class Automate:
    def __init__(self):
        self.etats = []
        self.initial = []
        self.final = []
        self.transitions = []
        self.est_deterministe = None
        self.est_minimaliste = None


    # Fonction : Affiche la table des transitions de l'automate
    def afficher_automate(self):
        print("Tous les états de l'automate :")
        for i in self.etats:
            print(i, end=", ")
        print()

        print("Table des transitions :")
        print("\t" + str(self.etats))
        print(5 * "\t-")
        for i in range(len(self.etats)):
            print(f"{i}|", end="\t")
            for j in range(len(self.etats)):
                print(self.transitions[i][j], end="\t")
            print()

        
    def est_deterministe(self):
        if len(self.initial) != 1:
            return False

        for i in range(len(self.etats)):
            for j in range(len(self.etats)):
                if len(self.transitions[i][j]) != 1:
                    return False

        return True
