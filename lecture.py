class Automate:
    def __init__(self):
        self.etats = []
        self.initial = []
        self.final = []
        self.transitions = []


    # Fonction : Affiche la table des transitions de l'automate
    def afficher_automate(self):
        print("Table des transitions :")
        print("\t" + self.etats.replace(", ", "\t"))
        print(5 * "\t-")
        for i in range(len(eval(self.etats))):
            print(f"{i}|", end="\t")
            for j in range(len(eval(self.etats))):
                print(self.transitions[i][j], end="\t")
            print()

# Fonction : Lis un des fichiers .txt et retourne un automate avec les informations correspondantes
def lire_automate(fichier):
    automate = Automate()
    with open(fichier, 'r') as f:
        automate.etats = f.readline().split(':')[-1].strip()
        automate.initial = f.readline().split(':')[-1].strip()
        automate.final = f.readline().split(':')[-1].strip()
        f.readline()
        NbEtats = len(eval(automate.etats))
        automate.transitions = [["" for i in range(NbEtats)] for j in range(NbEtats)]
        for x in f:
            ligne = x.strip()
            test = ligne.split(',')
            automate.transitions[eval(test[0])][eval(test[2])] = test[1]

    return automate

Automate = lire_automate('Automates_Test/02.txt')
Automate.afficher_automate()








