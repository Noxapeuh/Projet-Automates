class Automate:
    def __init__(self):
        self.etats = []
        self.initial = []
        self.final = []
        self.transitions = []


    # Fonction : Affiche la table des transitions de l'automate
    def afficher_automate(self):
        print("Table des transitions :")
        print("\t" + str(self.etats))
        print(5 * "\t-")
        for i in range(len(self.etats)):
            print(f"{i}|", end="\t")
            for j in range(len(self.etats)):
                print(self.transitions[i][j], end="\t")
            print()