import os
from automate import Automate


# ============================================================================================
# Fonction : lire_automate
# Role : Lit un fichier .txt contenant la description d'un automate et crée un objet Automate
#        correspondant. Le fichier doit suivre le format :
#          etats: 0, 1, 2
#          initial: 0
#          finaux: 1, 2
#          transitions:
#          0, a, 1
#        Gère les erreurs de formatage (virgule manquante, espaces en trop, etc.)
# Parametres :
#   - fichier : chemin du fichier .txt à lire (ex: 'Automates_Test/11.txt')
# Retour : Un objet Automate rempli avec les données du fichier
# ============================================================================================
def lire_automate(fichier):
    automate = Automate()

    with open(fichier, 'r') as f:
        # --- Lecture de la ligne des états ---
        # On split sur ':' pour séparer le label "etats" de la valeur, puis on split sur ','
        # pour obtenir la liste des états individuels. Le filtre 'if x.strip()' ignore les éléments vides.
        automate.etats = [x.strip() for x in f.readline().split(':')[-1].strip().split(',') if x.strip()]

        # --- Lecture de la ligne des états initiaux ---
        # Même logique : on extrait la partie après ':' et on sépare par ','
        automate.initial = [x.strip() for x in f.readline().split(':')[-1].strip().split(',') if x.strip()]

        # --- Lecture de la ligne des états finaux ---
        automate.final = [x.strip() for x in f.readline().split(':')[-1].strip().split(',') if x.strip()]

        # --- Lecture de la ligne "transitions:" (on la saute car c'est juste un label) ---
        f.readline()

        # --- Construction de la matrice de transitions ---
        # NbEtats : nombre total d'états de l'automate
        NbEtats = len(automate.etats)
        # transitions : matrice NxN initialisée avec des listes vides
        # transitions[i][j] contiendra les symboles permettant d'aller de l'état i à l'état j
        automate.transitions = [[[] for i in range(NbEtats)] for j in range(NbEtats)]

        # index_etats : dictionnaire {nom_état -> index} pour retrouver l'index d'un état par son nom
        # Nécessaire car les états peuvent être non-numériques (ex: 'P' pour l'état poubelle)
        index_etats = {nom: idx for idx, nom in enumerate(automate.etats)}

        # --- Lecture des transitions ligne par ligne ---
        # Chaque ligne est au format "état_départ, symbole, état_arrivée" (ex: "0, a, 1")
        # Certains fichiers ont des erreurs de format (ex: "7, eps 8" au lieu de "7, eps, 8")
        # Boucle : on lit chaque ligne restante du fichier
        for x in f:
            ligne = x.strip()
            # On ignore les lignes vides (fin de fichier ou lignes blanches)
            if not ligne:
                continue

            # On essaie d'abord le split par virgule (format normal)
            test = ligne.split(',')

            if len(test) == 3:
                # Format normal : "0, a, 1" -> ['0', ' a', ' 1']
                nom_depart = test[0].strip()
                symbole = test[1].strip()
                nom_arrivee = test[2].strip()
            elif len(test) == 2:
                # Format avec virgule manquante : "7, eps 8" -> ['7', ' eps 8']
                # On sépare la 2e partie par espaces pour récupérer le symbole et l'état d'arrivée
                parties = test[1].strip().split()
                if len(parties) == 2:
                    nom_depart = test[0].strip()
                    symbole = parties[0].strip()
                    nom_arrivee = parties[1].strip()
                else:
                    # Format complètement inconnu, on skip la ligne
                    print(f"  Attention : ligne ignoree (format invalide) : '{ligne}'")
                    continue
            else:
                # Si le split par virgule ne donne ni 2 ni 3 éléments, on essaie par espaces
                parties = ligne.split()
                if len(parties) == 3:
                    nom_depart = parties[0].strip()
                    symbole = parties[1].strip()
                    nom_arrivee = parties[2].strip()
                else:
                    print(f"  Attention : ligne ignoree (format invalide) : '{ligne}'")
                    continue

            # On utilise le dictionnaire index_etats pour retrouver les indices à partir des noms
            # Cela fonctionne pour les états numériques (ex: '0', '1') ET non-numériques (ex: 'P')
            if nom_depart in index_etats and nom_arrivee in index_etats:
                automate.transitions[index_etats[nom_depart]][index_etats[nom_arrivee]].append(symbole)
            else:
                print(f"  Attention : etat inconnu dans la transition : '{ligne}'")

    # On calcule l'alphabet à partir des transitions lues
    # Appel à get_alphabet() pour extraire automatiquement tous les symboles utilisés
    automate.get_alphabet()

    return automate


# ============================================================================================
# Fonction : afficher_automate
# Role : Affiche la table de transitions de l'automate de manière formatée, avec des colonnes
#        alignées. Chaque état est marqué 'E' s'il est initial et 'S' s'il est final.
#        Format demandé dans l'énoncé du projet.
# Parametres :
#   - automate : l'objet Automate à afficher
# ============================================================================================
def afficher_automate(automate):
    # On récupère l'alphabet pour savoir quelles colonnes afficher
    # Appel à get_alphabet() car on a besoin de connaître les symboles pour les colonnes
    if not automate.alphabet:
        automate.get_alphabet()

    nb_etats = len(automate.etats)
    alphabet = automate.alphabet

    # --- Construction du contenu de chaque cellule ---
    # tableau_contenu[i][symbole] = chaîne représentant les destinations depuis l'état i avec le symbole
    tableau_contenu = []
    for i in range(nb_etats):
        ligne = {}
        for symbole in alphabet:
            # On collecte tous les états d'arrivée pour le couple (état i, symbole)
            destinations = []
            # Boucle j : on regarde chaque état d'arrivée possible
            for j in range(nb_etats):
                if symbole in automate.transitions[i][j]:
                    destinations.append(automate.etats[j])
            # Si aucune destination, on met '--' pour indiquer l'absence de transition
            if not destinations:
                ligne[symbole] = '--'
            else:
                # On joint les destinations avec des virgules (ex: "0,1")
                ligne[symbole] = ','.join(destinations)
        tableau_contenu.append(ligne)

    # --- Calcul des largeurs de colonnes pour un affichage aligné ---
    # largeur_etat : largeur de la colonne des états (inclut les marqueurs E/S)
    largeur_etat = 4  # Minimum pour "E/S "
    for i in range(nb_etats):
        # On calcule la largeur nécessaire pour chaque état avec ses marqueurs
        marqueur = ''
        if automate.etats[i] in automate.initial:
            marqueur += 'E'
        if automate.etats[i] in automate.final:
            marqueur += 'S'
        label = marqueur + ' ' + str(automate.etats[i]) if marqueur else '  ' + str(automate.etats[i])
        if len(label) + 1 > largeur_etat:
            largeur_etat = len(label) + 1

    # largeur_col : dictionnaire contenant la largeur de chaque colonne de symbole
    largeur_col = {}
    for symbole in alphabet:
        # La largeur minimale est celle du nom du symbole lui-même
        largeur_col[symbole] = len(symbole)
        for i in range(nb_etats):
            # On prend la largeur maximale entre le symbole et le contenu de la cellule
            if len(tableau_contenu[i][symbole]) > largeur_col[symbole]:
                largeur_col[symbole] = len(tableau_contenu[i][symbole])

    # --- Affichage de l'en-tête ---
    # On affiche d'abord une ligne avec les noms des symboles de l'alphabet
    entete = ' ' * largeur_etat + '|'
    for symbole in alphabet:
        entete += ' ' + symbole.center(largeur_col[symbole]) + ' |'
    print(entete)

    # Ligne de séparation (tirets)
    separateur = '-' * largeur_etat + '+'
    for symbole in alphabet:
        separateur += '-' * (largeur_col[symbole] + 2) + '+'
    print(separateur)

    # --- Affichage de chaque ligne (un état par ligne) ---
    # Boucle i : on parcourt chaque état pour afficher sa ligne
    for i in range(nb_etats):
        # Construction du marqueur E (entrée/initial) et S (sortie/final)
        marqueur = ''
        if automate.etats[i] in automate.initial:
            marqueur += 'E'
        if automate.etats[i] in automate.final:
            marqueur += 'S'

        # Formatage de la cellule d'état avec le marqueur
        if marqueur:
            label = marqueur + ' ' + str(automate.etats[i])
        else:
            label = '  ' + str(automate.etats[i])

        ligne = label.ljust(largeur_etat) + '|'
        # On ajoute le contenu pour chaque symbole de l'alphabet
        for symbole in alphabet:
            ligne += ' ' + tableau_contenu[i][symbole].center(largeur_col[symbole]) + ' |'
        print(ligne)

    print()  # Ligne vide pour la lisibilité


# ============================================================================================
# Fonction : sauvegarder_automate
# Role : Sauvegarde un automate dans un fichier .txt au même format que les fichiers d'entrée.
#        Le nom du fichier suit le format "F(num_automate)(VersionX).txt".
#        Si une version existe déjà, on incrémente le numéro de version.
# Parametres :
#   - automate : l'objet Automate à sauvegarder
#   - num_automate : le numéro de l'automate original (ex: 11)
#   - dossier : le dossier où sauvegarder (par défaut 'Automates_Test')
# Retour : Le chemin du fichier créé
# ============================================================================================
def sauvegarder_automate(automate, num_automate, dossier='Automates_Test'):
    # --- Calcul du numéro de version ---
    # On cherche les fichiers existants pour déterminer le prochain numéro de version
    # Ex: si F11Version1.txt existe, on crée F11Version2.txt
    version = 1
    while True:
        nom_fichier = f"F{num_automate}Version{version}.txt"
        chemin = os.path.join(dossier, nom_fichier)
        # Si le fichier n'existe pas encore, on utilise ce nom
        if not os.path.exists(chemin):
            break
        version += 1  # Sinon on incrémente et on réessaie

    # --- Écriture du fichier ---
    with open(chemin, 'w') as f:
        # Ligne 1 : les états séparés par des virgules
        f.write(f"etats: {', '.join(automate.etats)}\n")
        # Ligne 2 : les états initiaux
        f.write(f"initial: {', '.join(automate.initial)}\n")
        # Ligne 3 : les états finaux
        f.write(f"finaux: {', '.join(automate.final)}\n")
        # Ligne 4 : le label "transitions:"
        f.write("transitions:\n")

        # --- Écriture des transitions ---
        # On parcourt la matrice pour écrire chaque transition non-vide
        nb_etats = len(automate.etats)
        # Boucle i : état de départ
        for i in range(nb_etats):
            # Boucle j : état d'arrivée
            for j in range(nb_etats):
                # Pour chaque symbole dans la case transitions[i][j]
                for symbole in automate.transitions[i][j]:
                    # On écrit au format "état_départ, symbole, état_arrivée"
                    f.write(f"{i}, {symbole}, {j}\n")

    return chemin