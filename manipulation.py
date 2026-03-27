import copy
from automate import Automate


# ============================================================================================
# Fonction : est_deterministe
# Role : Vérifie si l'automate est déterministe. Un automate est déterministe si et seulement
#        si : (1) il possède exactement un seul état initial, et (2) pour chaque état et
#        chaque symbole de l'alphabet, il y a AU PLUS une transition, et (3) il n'y a pas
#        d'epsilon-transitions.
#        Affiche les raisons si l'automate n'est pas déterministe.
# Parametres :
#   - automate : l'objet Automate à vérifier
# Retour : True si déterministe, False sinon
# ============================================================================================
def est_deterministe(automate):
    # On récupère l'alphabet si ce n'est pas déjà fait
    if not automate.alphabet:
        automate.get_alphabet()

    resultat = True  # Variable qui sera mise à False si on trouve une raison de non-déterminisme
    nombre_etats = len(automate.etats)

    # Condition 1 : vérifier qu'il y a exactement un seul état initial
    if len(automate.initial) != 1:
        print(f"  -> Non deterministe : il y a {len(automate.initial)} etats initiaux ({', '.join(automate.initial)}) au lieu de 1.")
        resultat = False

    # Condition 2 : vérifier qu'il n'y a pas plusieurs transitions pour le même symbole depuis un état
    # Boucle indice_depart : on regarde chaque état de départ
    for indice_depart in range(nombre_etats):
        for symbole in automate.alphabet:
            # On compte combien de transitions partent de l'état avec le symbole donné
            nombre_destinations = 0
            # Boucle indice_arrivee : on regarde chaque état d'arrivée possible
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[indice_depart][indice_arrivee]:
                    nombre_destinations += 1
            # S'il y a plus d'une destination pour un même symbole, ce n'est pas déterministe
            if nombre_destinations > 1:
                print(f"  -> Non deterministe : depuis l'etat {automate.etats[indice_depart]}, le symbole '{symbole}' mene a {nombre_destinations} etats.")
                resultat = False

        # Condition 3 : vérifier s'il y a des epsilon-transitions (rend l'automate non déterministe)
        for indice_arrivee in range(nombre_etats):
            if 'eps' in automate.transitions[indice_depart][indice_arrivee]:
                print(f"  -> Non deterministe : epsilon-transition de l'etat {automate.etats[indice_depart]} vers {automate.etats[indice_arrivee]}.")
                resultat = False

    return resultat


# ============================================================================================
# Fonction : est_standard
# Role : Vérifie si l'automate est standard. Un automate est standard si et seulement si :
#        (1) il possède un unique état initial, et (2) aucune transition ne mène vers cet
#        état initial (pas de flèche entrante sur l'état initial).
# Parametres :
#   - automate : l'objet Automate à vérifier
# Retour : True si standard, False sinon
# ============================================================================================
def est_standard(automate):
    # Condition 1 : un seul état initial
    if len(automate.initial) != 1:
        print(f"  -> Non standard : il y a {len(automate.initial)} etats initiaux au lieu de 1.")
        return False

    # indice_etat_initial : index de l'état initial dans la liste des états
    etat_initial = automate.initial[0]
    indice_etat_initial = automate.etats.index(etat_initial)
    nombre_etats = len(automate.etats)

    # Condition 2 : on vérifie qu'aucune transition ne pointe vers l'état initial
    # Boucle indice_depart : on parcourt chaque état de départ
    for indice_depart in range(nombre_etats):
        # transitions[indice_depart][indice_etat_initial] contient les symboles pour aller vers l'état initial
        if len(automate.transitions[indice_depart][indice_etat_initial]) > 0:
            print(f"  -> Non standard : il y a une transition de l'etat {automate.etats[indice_depart]} vers l'etat initial {etat_initial}.")
            return False

    return True


# ============================================================================================
# Fonction : est_complet
# Role : Vérifie si l'automate (déterministe) est complet. Un automate déterministe est
#        complet si pour chaque état et chaque symbole de l'alphabet, il existe exactement
#        une transition. Affiche les raisons si incomplet.
# Parametres :
#   - automate : l'objet Automate à vérifier
# Retour : True si complet, False sinon
# ============================================================================================
def est_complet(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)
    resultat = True  # Variable de résultat

    # Boucle indice_depart : on parcourt chaque état
    for indice_depart in range(nombre_etats):
        # Pour chaque symbole de l'alphabet, on vérifie qu'il existe au moins une transition
        for symbole in automate.alphabet:
            transition_trouvee = False  # Sera True si on trouve une transition pour ce symbole
            # Boucle indice_arrivee : on cherche si ce symbole apparaît dans une transition sortante
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[indice_depart][indice_arrivee]:
                    transition_trouvee = True
                    break  # Pas besoin de chercher plus loin, on a trouvé
            # Si aucune transition trouvée pour ce symbole depuis cet état
            if not transition_trouvee:
                print(f"  -> Non complet : pas de transition depuis l'etat {automate.etats[indice_depart]} avec le symbole '{symbole}'.")
                resultat = False

    return resultat


# ============================================================================================
# Fonction : standardiser
# Role : Crée un nouvel automate standard équivalent. On ajoute un nouvel état initial 'i'
#        qui reprend toutes les transitions sortantes des anciens états initiaux. L'ancien
#        état initial n'est plus initial. Si un ancien état initial était final, le nouvel
#        état 'i' est aussi final.
# Parametres :
#   - automate : l'objet Automate à standardiser
# Retour : Un nouvel objet Automate qui est la version standardisée
# ============================================================================================
def standardiser(automate):
    # On crée une copie profonde pour ne pas modifier l'original
    nouveau = copy.deepcopy(automate)

    nombre_etats_ancien = len(nouveau.etats)
    nouvel_etat = 'i'  # Nom du nouvel état initial

    # On ajoute le nouvel état au début de la liste des états
    nouveau.etats.insert(0, nouvel_etat)
    nombre_etats = len(nouveau.etats)

    # On reconstruit la matrice de transitions avec une ligne et une colonne en plus
    # nouvelle_matrice : matrice (nombre_etats x nombre_etats) initialisée avec des listes vides
    nouvelle_matrice = [[[] for _ in range(nombre_etats)] for _ in range(nombre_etats)]

    # On recopie l'ancienne matrice dans la nouvelle (décalée de 1 car on a inséré 'i' en position 0)
    # Boucle indice_ligne : parcourt les anciennes lignes
    # Boucle indice_colonne : parcourt les anciennes colonnes
    for indice_ligne in range(nombre_etats_ancien):
        for indice_colonne in range(nombre_etats_ancien):
            # indice_ligne+1 et indice_colonne+1 car le nouvel état 'i' occupe l'index 0
            nouvelle_matrice[indice_ligne + 1][indice_colonne + 1] = list(nouveau.transitions[indice_ligne][indice_colonne])

    # On copie toutes les transitions sortantes des anciens états initiaux vers le nouvel état 'i'
    # Cela permet au nouvel état initial de se comporter comme les anciens initiaux
    for ancien_initial in nouveau.initial:
        # indice_ancien_initial : index de l'ancien état initial dans la NOUVELLE liste d'états
        indice_ancien_initial = nouveau.etats.index(ancien_initial)
        # Boucle indice_destination : pour chaque destination possible depuis cet ancien état initial
        for indice_destination in range(nombre_etats):
            for symbole in nouvelle_matrice[indice_ancien_initial][indice_destination]:
                # On ajoute le symbole seulement s'il n'est pas déjà présent (éviter les doublons)
                if symbole not in nouvelle_matrice[0][indice_destination]:
                    nouvelle_matrice[0][indice_destination].append(symbole)

    nouveau.transitions = nouvelle_matrice

    # Si un des anciens états initiaux était final, le nouvel état doit aussi être final
    # Car l'automate original acceptait le mot vide
    nouvel_etat_est_final = False
    for ancien_initial in nouveau.initial:
        if ancien_initial in nouveau.final:
            nouvel_etat_est_final = True
            break

    if nouvel_etat_est_final:
        nouveau.final.append(nouvel_etat)

    # Le seul état initial est maintenant le nouvel état 'i'
    nouveau.initial = [nouvel_etat]

    # On recalcule l'alphabet car la structure a changé
    nouveau.get_alphabet()

    return nouveau


# ============================================================================================
# Fonction : epsilon_fermeture
# Role : Calcule l'epsilon-fermeture d'un ensemble d'états, c'est-à-dire tous les états
#        atteignables depuis ces états en ne suivant QUE des epsilon-transitions.
#        Utilise un parcours en largeur (BFS) avec une pile.
# Parametres :
#   - automate : l'objet Automate contenant les transitions
#   - ensemble_etats : liste d'indices d'états dont on veut calculer l'epsilon-fermeture
# Retour : ensemble (set) des indices d'états dans l'epsilon-fermeture
# ============================================================================================
def epsilon_fermeture(automate, ensemble_etats):
    # fermeture : ensemble qui contiendra tous les états atteignables par epsilon
    fermeture = set(ensemble_etats)
    # pile : file de traitement pour le parcours en largeur
    pile = list(ensemble_etats)
    nombre_etats = len(automate.etats)

    # Tant qu'il reste des états à traiter dans la pile
    while pile:
        # On retire un état de la pile pour le traiter
        etat_en_cours = pile.pop()
        # Boucle indice_arrivee : on regarde toutes les transitions sortantes de cet état
        for indice_arrivee in range(nombre_etats):
            # Si il y a une epsilon-transition et qu'on n'a pas encore visité cet état
            if 'eps' in automate.transitions[etat_en_cours][indice_arrivee] and indice_arrivee not in fermeture:
                fermeture.add(indice_arrivee)
                pile.append(indice_arrivee)  # On ajoute pour explorer ses propres epsilon-transitions

    return fermeture


# ============================================================================================
# Fonction : determiniser_et_completer
# Role : Construit l'automate déterministe complet équivalent à l'automate courant en
#        utilisant la construction par sous-ensembles. Gère les epsilon-transitions.
#        Chaque état du nouvel automate correspond à un ensemble d'états de l'original.
#        La notation est "123" si tous les états <= 9, "1.2.3" sinon.
# Parametres :
#   - automate : l'objet Automate à déterminiser
# Retour : Un nouvel objet Automate déterministe et complet
# ============================================================================================
def determiniser_et_completer(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # possede_epsilon : indique si l'automate a des epsilon-transitions
    possede_epsilon = False
    for indice_depart in range(nombre_etats):
        for indice_arrivee in range(nombre_etats):
            if 'eps' in automate.transitions[indice_depart][indice_arrivee]:
                possede_epsilon = True
                break
        if possede_epsilon:
            break

    # --- Calcul de l'état initial du nouvel automate ---
    indices_initiaux = [automate.etats.index(etat) for etat in automate.initial]

    # Si l'automate a des epsilon-transitions, l'état initial est l'epsilon-fermeture des initiaux
    if possede_epsilon:
        etat_initial_determinise = frozenset(epsilon_fermeture(automate, indices_initiaux))
    else:
        etat_initial_determinise = frozenset(indices_initiaux)

    # --- Construction par sous-ensembles ---
    # etats_determinises : dictionnaire {frozenset d'indices -> index dans le nouvel automate}
    etats_determinises = {etat_initial_determinise: 0}
    # file_attente : file d'attente des états à traiter (parcours en largeur)
    file_attente = [etat_initial_determinise]
    # transitions_determinisees : liste de dictionnaires {symbole -> frozenset d'indices}
    transitions_determinisees = []
    # ordre_etats : liste ordonnée des frozensets pour garder l'ordre de découverte
    ordre_etats = [etat_initial_determinise]

    # Tant qu'il reste des états à explorer
    while file_attente:
        # On récupère le prochain ensemble d'états à traiter
        ensemble_courant = file_attente.pop(0)
        transitions_etat = {}  # Dictionnaire des transitions pour cet état

        # Pour chaque symbole de l'alphabet, on calcule l'ensemble des états atteignables
        for symbole in automate.alphabet:
            # destinations : ensemble des états atteignables depuis l'ensemble courant avec le symbole
            destinations = set()
            # Boucle : pour chaque état individuel dans l'ensemble courant
            for indice_etat in ensemble_courant:
                # Boucle indice_arrivee : on regarde chaque état d'arrivée possible
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        destinations.add(indice_arrivee)

            # Si l'automate a des epsilon-transitions, on applique l'epsilon-fermeture
            if possede_epsilon and destinations:
                destinations = epsilon_fermeture(automate, list(destinations))

            destination_figee = frozenset(destinations)
            transitions_etat[symbole] = destination_figee

            # Si cet ensemble d'états est nouveau, on l'ajoute à la liste
            if destination_figee not in etats_determinises:
                etats_determinises[destination_figee] = len(etats_determinises)
                file_attente.append(destination_figee)
                ordre_etats.append(destination_figee)

        transitions_determinisees.append(transitions_etat)

    # --- Construction du nouvel automate ---
    nouveau = Automate()
    nombre_nouveaux_etats = len(ordre_etats)

    # nombre_etat_max : le plus grand numéro d'état original, pour décider de la notation
    nombre_etat_max = max(int(etat) for etat in automate.etats if etat.isdigit()) if any(etat.isdigit() for etat in automate.etats) else 0
    # utiliser_points : True si les états originaux ont des numéros >= 10 (notation "1.2.3")
    utiliser_points = nombre_etat_max >= 10

    # On construit les noms des nouveaux états et le dictionnaire de correspondance
    for indice, ensemble in enumerate(ordre_etats):
        if not ensemble:
            # Ensemble vide = état poubelle
            nom = 'P'
        else:
            # On trie les indices pour avoir un nom cohérent
            indices_tries = sorted(ensemble)
            noms_tries = [automate.etats[indice_etat] for indice_etat in indices_tries]
            if utiliser_points:
                # Notation avec points si des états ont des numéros >= 10 (ex: "1.12.3")
                nom = '.'.join(noms_tries)
            else:
                # Notation concaténée si tous les états <= 9 (ex: "123")
                nom = ''.join(noms_tries)
        nouveau.etats.append(nom)
        # On stocke la correspondance pour l'affichage
        nouveau.correspondance[nom] = [automate.etats[indice_etat] for indice_etat in sorted(ensemble)] if ensemble else ['P']

    # L'état initial du nouvel automate est le premier état (index 0)
    nouveau.initial = [nouveau.etats[0]]

    # Un état du nouvel automate est final si AU MOINS UN des états originaux qu'il contient est final
    indices_finaux = {automate.etats.index(etat) for etat in automate.final}
    for indice, ensemble in enumerate(ordre_etats):
        # On vérifie l'intersection entre l'ensemble courant et les indices finaux
        if ensemble & indices_finaux:
            nouveau.final.append(nouveau.etats[indice])

    # Construction de la matrice de transitions du nouvel automate
    nouveau.transitions = [[[] for _ in range(nombre_nouveaux_etats)] for _ in range(nombre_nouveaux_etats)]
    for indice, ensemble in enumerate(ordre_etats):
        for symbole in automate.alphabet:
            destination_ensemble = transitions_determinisees[indice][symbole]
            indice_destination = etats_determinises[destination_ensemble]
            nouveau.transitions[indice][indice_destination].append(symbole)

    nouveau.alphabet = list(automate.alphabet)

    # --- Complétion : ajouter l'état poubelle si nécessaire ---
    possede_poubelle = 'P' in nouveau.etats

    # Si l'état poubelle n'existe pas, on vérifie s'il faut en ajouter un
    if not possede_poubelle:
        transition_manquante = False
        for indice_depart in range(nombre_nouveaux_etats):
            for symbole in nouveau.alphabet:
                transition_trouvee = False
                for indice_arrivee in range(nombre_nouveaux_etats):
                    if symbole in nouveau.transitions[indice_depart][indice_arrivee]:
                        transition_trouvee = True
                        break
                if not transition_trouvee:
                    transition_manquante = True
                    break
            if transition_manquante:
                break

        if transition_manquante:
            # On appelle completer() pour ajouter l'état poubelle et les transitions manquantes
            nouveau = completer(nouveau)

    return nouveau


# ============================================================================================
# Fonction : completer
# Role : Complète un automate déterministe en ajoutant un état poubelle 'P' et en ajoutant
#        toutes les transitions manquantes vers cet état poubelle. L'état poubelle boucle
#        sur lui-même pour tous les symboles.
# Parametres :
#   - automate : l'objet Automate à compléter
# Retour : Un nouvel objet Automate complet
# ============================================================================================
def completer(automate):
    nouveau = copy.deepcopy(automate)
    if not nouveau.alphabet:
        nouveau.get_alphabet()

    nombre_etats = len(nouveau.etats)

    # On vérifie d'abord si la complétion est nécessaire
    besoin_poubelle = False
    for indice_depart in range(nombre_etats):
        for symbole in nouveau.alphabet:
            transition_trouvee = False
            for indice_arrivee in range(nombre_etats):
                if symbole in nouveau.transitions[indice_depart][indice_arrivee]:
                    transition_trouvee = True
                    break
            if not transition_trouvee:
                besoin_poubelle = True
                break
        if besoin_poubelle:
            break

    if not besoin_poubelle:
        # L'automate est déjà complet, pas besoin d'ajouter un état poubelle
        return nouveau

    # On ajoute l'état poubelle 'P' à la liste des états
    nouveau.etats.append('P')
    nombre_etats_avec_poubelle = len(nouveau.etats)

    # On agrandit la matrice de transitions pour inclure la nouvelle colonne et ligne de 'P'
    nouvelle_matrice = [[[] for _ in range(nombre_etats_avec_poubelle)] for _ in range(nombre_etats_avec_poubelle)]
    # On recopie l'ancienne matrice dans la nouvelle
    for indice_depart in range(nombre_etats):
        for indice_arrivee in range(nombre_etats):
            nouvelle_matrice[indice_depart][indice_arrivee] = list(nouveau.transitions[indice_depart][indice_arrivee])

    # Pour chaque état et chaque symbole, s'il n'y a pas de transition, on redirige vers P
    # indice_poubelle : index de l'état poubelle dans la liste des états
    indice_poubelle = nombre_etats_avec_poubelle - 1
    for indice_depart in range(nombre_etats_avec_poubelle):
        for symbole in nouveau.alphabet:
            transition_existe = False
            for indice_arrivee in range(nombre_etats_avec_poubelle):
                if symbole in nouvelle_matrice[indice_depart][indice_arrivee]:
                    transition_existe = True
                    break
            # Si aucune transition n'existe, on redirige vers l'état poubelle
            if not transition_existe:
                nouvelle_matrice[indice_depart][indice_poubelle].append(symbole)

    nouveau.transitions = nouvelle_matrice
    return nouveau


# ============================================================================================
# Fonction : minimiser
# Role : Construit l'automate minimal équivalent en utilisant l'algorithme de Moore
#        (partitionnement successif). Affiche chaque étape de partitionnement.
#        L'automate doit être déterministe et complet avant la minimisation.
# Parametres :
#   - automate : l'objet Automate à minimiser
# Retour : Un nouvel objet Automate minimal
# ============================================================================================
def minimiser(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # --- Partition initiale (Partition 0) ---
    # On sépare les états en deux groupes : finaux (groupe 1) et non-finaux (groupe 0)
    partition = [0] * nombre_etats
    for indice_etat in range(nombre_etats):
        if automate.etats[indice_etat] in automate.final:
            partition[indice_etat] = 1

    numero_partition = 0  # Compteur de partitions pour l'affichage
    print(f"  Partition {numero_partition} : {_afficher_partition(automate, partition)}")

    # --- Raffinement successif ---
    # On raffine la partition jusqu'à ce qu'elle ne change plus (point fixe)
    while True:
        nouvelle_partition = [0] * nombre_etats
        # signatures : dictionnaire {signature -> numéro de nouveau groupe}
        signatures = {}
        prochain_groupe = 0  # Compteur pour nommer les nouveaux groupes

        # Boucle indice_etat : pour chaque état, on calcule sa "signature"
        for indice_etat in range(nombre_etats):
            # La signature d'un état = (son groupe actuel, les groupes de ses destinations par symbole)
            # Deux états avec la même signature restent dans le même groupe
            signature = [partition[indice_etat]]
            for symbole in automate.alphabet:
                # On cherche la destination de l'état avec le symbole
                groupe_destination = -1
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        groupe_destination = partition[indice_arrivee]
                        break
                signature.append(groupe_destination)

            signature_tuple = tuple(signature)  # On convertit en tuple pour l'utiliser comme clé

            # Si cette signature est nouvelle, on lui attribue un nouveau numéro de groupe
            if signature_tuple not in signatures:
                signatures[signature_tuple] = prochain_groupe
                prochain_groupe += 1

            nouvelle_partition[indice_etat] = signatures[signature_tuple]

        numero_partition += 1
        print(f"  Partition {numero_partition} : {_afficher_partition(automate, nouvelle_partition)}")

        # Si la partition n'a pas changé, on a atteint le point fixe
        if nouvelle_partition == partition:
            print("  => Point fixe atteint, la partition est stable.")
            break

        partition = nouvelle_partition

    # --- Construction de l'automate minimal ---
    nouveau = Automate()
    nombre_groupes = max(partition) + 1

    # On nomme les nouveaux états par leur numéro de groupe
    nouveau.etats = [str(groupe) for groupe in range(nombre_groupes)]

    # Correspondance : quel groupe correspond à quels anciens états
    for groupe in range(nombre_groupes):
        etats_du_groupe = [automate.etats[indice] for indice in range(nombre_etats) if partition[indice] == groupe]
        nouveau.correspondance[str(groupe)] = etats_du_groupe

    # L'état initial est le groupe contenant l'ancien état initial
    for etat_initial in automate.initial:
        indice_initial = automate.etats.index(etat_initial)
        groupe_initial = str(partition[indice_initial])
        if groupe_initial not in nouveau.initial:
            nouveau.initial.append(groupe_initial)

    # Les états finaux sont les groupes contenant au moins un ancien état final
    for etat_final in automate.final:
        indice_final = automate.etats.index(etat_final)
        groupe_final = str(partition[indice_final])
        if groupe_final not in nouveau.final:
            nouveau.final.append(groupe_final)

    # Construction de la matrice de transitions du nouvel automate
    nouveau.transitions = [[[] for _ in range(nombre_groupes)] for _ in range(nombre_groupes)]
    # On prend un représentant de chaque groupe pour définir les transitions
    for groupe in range(nombre_groupes):
        # representant : le premier état trouvé dans ce groupe
        representant = -1
        for indice_etat in range(nombre_etats):
            if partition[indice_etat] == groupe:
                representant = indice_etat
                break
        # Pour chaque symbole, on regarde où va le représentant
        for symbole in automate.alphabet:
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[representant][indice_arrivee]:
                    groupe_destination = partition[indice_arrivee]
                    if symbole not in nouveau.transitions[groupe][groupe_destination]:
                        nouveau.transitions[groupe][groupe_destination].append(symbole)
                    break

    nouveau.alphabet = list(automate.alphabet)
    return nouveau


# ============================================================================================
# Fonction : _afficher_partition
# Role : Formate une partition pour l'affichage. Regroupe les états par numéro de groupe.
#        Fonction utilitaire privée (préfixe _), utilisée uniquement par minimiser().
# Parametres :
#   - automate : l'objet Automate dont on affiche la partition
#   - partition : liste d'entiers, partition[i] = numéro de groupe de l'état i
# Retour : chaîne formatée (ex: "{0, 2, 3} {1, 4}")
# ============================================================================================
def _afficher_partition(automate, partition):
    # groupes : dictionnaire {numéro de groupe -> liste des noms d'états}
    groupes = {}
    for indice, numero_groupe in enumerate(partition):
        if numero_groupe not in groupes:
            groupes[numero_groupe] = []
        groupes[numero_groupe].append(automate.etats[indice])

    # On formate chaque groupe entre accolades
    parties = []
    for numero_groupe in sorted(groupes.keys()):
        parties.append('{' + ', '.join(groupes[numero_groupe]) + '}')
    return ' '.join(parties)


# ============================================================================================
# Fonction : reconnaitre_mot
# Role : Teste si un mot est reconnu par l'automate déterministe complet. On part de l'état
#        initial et on suit les transitions symbole par symbole. Si on arrive sur un état
#        final à la fin du mot, le mot est reconnu.
# Parametres :
#   - automate : l'objet Automate déterministe complet
#   - mot : chaîne de caractères à tester (ex: "aab")
# Retour : True si le mot est reconnu, False sinon
# ============================================================================================
def reconnaitre_mot(automate, mot):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # indice_etat_courant : index de l'état courant, on part de l'état initial
    indice_etat_courant = automate.etats.index(automate.initial[0])

    # Cas spécial : le mot vide (epsilon)
    if mot == '' or mot == 'eps':
        return automate.etats[indice_etat_courant] in automate.final

    # On parcourt le mot symbole par symbole
    for symbole in mot:
        # On vérifie que le symbole fait partie de l'alphabet
        if symbole not in automate.alphabet:
            print(f"  Le symbole '{symbole}' n'appartient pas a l'alphabet {automate.alphabet}.")
            return False

        # On cherche la transition depuis l'état courant avec ce symbole
        transition_trouvee = False
        # Boucle indice_arrivee : on cherche l'état d'arrivée
        for indice_arrivee in range(nombre_etats):
            if symbole in automate.transitions[indice_etat_courant][indice_arrivee]:
                indice_etat_courant = indice_arrivee  # On avance vers l'état d'arrivée
                transition_trouvee = True
                break

        # Si aucune transition trouvée (ne devrait pas arriver si l'automate est complet)
        if not transition_trouvee:
            return False

    # Après avoir lu tout le mot, on vérifie si l'état courant est un état final
    return automate.etats[indice_etat_courant] in automate.final


# ============================================================================================
# Fonction : complementaire
# Role : Construit l'automate reconnaissant le langage complémentaire. On inverse simplement
#        les états finaux et non-finaux : les anciens finaux deviennent non-finaux et
#        vice-versa. L'automate doit être déterministe et complet.
# Parametres :
#   - automate : l'objet Automate déterministe complet
# Retour : Un nouvel objet Automate reconnaissant le langage complémentaire
# ============================================================================================
def complementaire(automate):
    # On crée une copie profonde pour ne pas modifier l'original
    nouveau = copy.deepcopy(automate)

    # nouveaux_finaux : tous les états qui N'ETAIENT PAS finaux dans l'automate original
    nouveaux_finaux = [etat for etat in nouveau.etats if etat not in nouveau.final]

    # On remplace les anciens états finaux par les nouveaux
    nouveau.final = nouveaux_finaux

    return nouveau
