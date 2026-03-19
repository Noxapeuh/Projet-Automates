from automate import Automate

# Fonction : Lis un des fichiers .txt et retourne un automate avec les informations correspondantes
def lire_automate(fichier):
    automate = Automate()
    with open(fichier, 'r') as f:
        #Transforme la ligne des états en une liste du type ['0', '1', '2']
        temp = f.readline().split(':')[-1].strip()
        for i in range(0, len(temp), 3):
            automate.etats.append(temp[i])

        # Transforme la ligne des états initiaux en une liste du type ['0']
        temp = f.readline().split(':')[-1].strip()
        for i in range(0, len(temp), 3):
            automate.initial.append(temp[i])

        # Transforme la ligne des états en une liste du type ['0', '1', '2']
        temp = f.readline().split(':')[-1].strip()
        for i in range(0, len(temp), 3):
            automate.final.append(temp[i])


        f.readline()
        NbEtats = len(automate.etats)
        automate.transitions =  [[[] for i in range(NbEtats)] for j in range(NbEtats)]
        for x in f:
            ligne = x.strip()
            test = ligne.split(',')
            automate.transitions[eval(test[0])][eval(test[2])].append(test[1].strip())

    return automate

Automate = lire_automate('Automates_Test/11.txt')
Automate.afficher_automate()