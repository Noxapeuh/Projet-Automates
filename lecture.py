import os
from automate import Automate


# fonction qui lit un automate depuis un fichier texte
def lire_automate(fichier):
    automate = Automate()

    f = open(fichier, 'r')

    # lecture de la ligne des etats
    ligne_etats = f.readline()
    partie_etats = ligne_etats.split(':')
    liste_etats = partie_etats[-1].strip().split(',')
    automate.etats = []
    for e in liste_etats:
        e = e.strip()
        if e != '':
            automate.etats.append(e)

    # lecture de la ligne des etats initiaux
    ligne_initiaux = f.readline()
    partie_initiaux = ligne_initiaux.split(':')
    liste_initiaux = partie_initiaux[-1].strip().split(',')
    automate.initial = []
    for e in liste_initiaux:
        e = e.strip()
        if e != '':
            automate.initial.append(e)

    # lecture de la ligne des etats finaux
    ligne_finaux = f.readline()
    partie_finaux = ligne_finaux.split(':')
    liste_finaux = partie_finaux[-1].strip().split(',')
    automate.final = []
    for e in liste_finaux:
        e = e.strip()
        if e != '':
            automate.final.append(e)

    # on saute la ligne "transitions:"
    f.readline()

    # construction de la matrice de transitions (NxN de listes vides)
    nb_etats = len(automate.etats)
    automate.transitions = []
    for i in range(nb_etats):
        ligne = []
        for j in range(nb_etats):
            ligne.append([])
        automate.transitions.append(ligne)

    # dictionnaire pour retrouver l'index d'un etat par son nom
    index_etats = {}
    for idx in range(len(automate.etats)):
        index_etats[automate.etats[idx]] = idx

    # lecture des transitions ligne par ligne
    for x in f:
        ligne = x.strip()
        if ligne == '':
            continue

        # on essaie de couper par virgule
        test = ligne.split(',')

        if len(test) == 3:
            # format normal : "0, a, 1"
            nom_depart = test[0].strip()
            symbole = test[1].strip()
            nom_arrivee = test[2].strip()
        elif len(test) == 2:
            # format avec virgule manquante : "7, eps 8"
            parties = test[1].strip().split()
            if len(parties) == 2:
                nom_depart = test[0].strip()
                symbole = parties[0].strip()
                nom_arrivee = parties[1].strip()
            else:
                print("  Attention : ligne ignoree (format invalide) : '" + ligne + "'")
                continue
        else:
            # on essaie de couper par espaces
            parties = ligne.split()
            if len(parties) == 3:
                nom_depart = parties[0].strip()
                symbole = parties[1].strip()
                nom_arrivee = parties[2].strip()
            else:
                print("  Attention : ligne ignoree (format invalide) : '" + ligne + "'")
                continue

        # on ajoute la transition dans la matrice
        if nom_depart in index_etats and nom_arrivee in index_etats:
            i = index_etats[nom_depart]
            j = index_etats[nom_arrivee]
            automate.transitions[i][j].append(symbole)
        else:
            print("  Attention : etat inconnu dans la transition : '" + ligne + "'")

    f.close()

    # on calcule l'alphabet
    automate.get_alphabet()

    return automate


# fonction qui affiche la table de transitions de l'automate
def afficher_automate(automate):
    # on recupere l'alphabet
    if len(automate.alphabet) == 0:
        automate.get_alphabet()

    nb_etats = len(automate.etats)
    alphabet = automate.alphabet

    # on construit le contenu de chaque cellule
    tableau_contenu = []
    for i in range(nb_etats):
        ligne = {}
        for symbole in alphabet:
            # on cherche toutes les destinations depuis l'etat i avec ce symbole
            destinations = []
            for j in range(nb_etats):
                if symbole in automate.transitions[i][j]:
                    destinations.append(automate.etats[j])
            # si pas de destination, on met '--'
            if len(destinations) == 0:
                ligne[symbole] = '--'
            else:
                ligne[symbole] = ','.join(destinations)
        tableau_contenu.append(ligne)

    # calcul des largeurs de colonnes
    largeur_etat = 4
    for i in range(nb_etats):
        marqueur = ''
        if automate.etats[i] in automate.initial:
            marqueur = marqueur + 'E'
        if automate.etats[i] in automate.final:
            marqueur = marqueur + 'S'
        if marqueur != '':
            label = marqueur + ' ' + str(automate.etats[i])
        else:
            label = '  ' + str(automate.etats[i])
        if len(label) + 1 > largeur_etat:
            largeur_etat = len(label) + 1

    largeur_col = {}
    for symbole in alphabet:
        largeur_col[symbole] = len(symbole)
        for i in range(nb_etats):
            if len(tableau_contenu[i][symbole]) > largeur_col[symbole]:
                largeur_col[symbole] = len(tableau_contenu[i][symbole])

    # affichage de l'en-tete
    entete = ' ' * largeur_etat + '|'
    for symbole in alphabet:
        entete = entete + ' ' + symbole.center(largeur_col[symbole]) + ' |'
    print(entete)

    # ligne de separation
    separateur = '-' * largeur_etat + '+'
    for symbole in alphabet:
        separateur = separateur + '-' * (largeur_col[symbole] + 2) + '+'
    print(separateur)

    # affichage de chaque ligne
    for i in range(nb_etats):
        marqueur = ''
        if automate.etats[i] in automate.initial:
            marqueur = marqueur + 'E'
        if automate.etats[i] in automate.final:
            marqueur = marqueur + 'S'

        if marqueur != '':
            label = marqueur + ' ' + str(automate.etats[i])
        else:
            label = '  ' + str(automate.etats[i])

        ligne = label.ljust(largeur_etat) + '|'
        for symbole in alphabet:
            ligne = ligne + ' ' + tableau_contenu[i][symbole].center(largeur_col[symbole]) + ' |'
        print(ligne)

    print()


# fonction qui sauvegarde un automate dans un fichier texte
def sauvegarder_automate(automate, num_automate, dossier='Automates_Test'):
    # on cherche le prochain numero de version disponible
    version = 1
    while True:
        nom_fichier = "F" + str(num_automate) + "Version" + str(version) + ".txt"
        chemin = os.path.join(dossier, nom_fichier)
        if not os.path.exists(chemin):
            break
        version = version + 1

    # ecriture du fichier
    f = open(chemin, 'w')
    f.write("etats: " + ', '.join(automate.etats) + "\n")
    f.write("initial: " + ', '.join(automate.initial) + "\n")
    f.write("finaux: " + ', '.join(automate.final) + "\n")
    f.write("transitions:\n")

    nb_etats = len(automate.etats)
    for i in range(nb_etats):
        for j in range(nb_etats):
            for symbole in automate.transitions[i][j]:
                f.write(str(i) + ", " + symbole + ", " + str(j) + "\n")

    f.close()

    return chemin