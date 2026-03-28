import copy
from automate import Automate


# fonction : est_deterministe
# role : verifie si l'automate est deterministe. un automate est deterministe ssi :
#        (1) il possede exactement un seul etat initial, et (2) pour chaque etat et
#        chaque symbole de l'alphabet, il y a au plus une transition, et (3) il n'y a pas
#        d'epsilon-transitions.
#        affiche les raisons si l'automate n'est pas deterministe.
# parametres :
#   - automate : l'objet Automate a verifier
# retour : True si deterministe, False sinon
def est_deterministe(automate):
    # recup alphabet si pas deja fait
    if not automate.alphabet:
        automate.get_alphabet()

    resultat = True  # mis a false si on trouve un pb
    nombre_etats = len(automate.etats)

    # condition 1 : un seul etat initial
    if len(automate.initial) != 1:
        print(f"  -> Non deterministe : il y a {len(automate.initial)} etats initiaux ({', '.join(automate.initial)}) au lieu de 1.")
        resultat = False

    # condition 2 : pas plusieurs transitions pour le meme symbole depuis un etat
    for indice_depart in range(nombre_etats):
        for symbole in automate.alphabet:
            # on compte combien de transitions partent avec ce symbole
            nombre_destinations = 0
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[indice_depart][indice_arrivee]:
                    nombre_destinations += 1
            # plus d'une dest = pas deterministe
            if nombre_destinations > 1:
                print(f"  -> Non deterministe : depuis l'etat {automate.etats[indice_depart]}, le symbole '{symbole}' mene a {nombre_destinations} etats.")
                resultat = False

        # condition 3 : pas d'eps-transitions
        for indice_arrivee in range(nombre_etats):
            if 'eps' in automate.transitions[indice_depart][indice_arrivee]:
                print(f"  -> Non deterministe : epsilon-transition de l'etat {automate.etats[indice_depart]} vers {automate.etats[indice_arrivee]}.")
                resultat = False

    return resultat


# fonction : est_standard
# role : verifie si l'automate est standard. un automate est standard ssi :
#        (1) il possede un unique etat initial, et (2) aucune transition ne mene vers cet
#        etat initial (pas de fleche entrante sur l'etat initial).
# parametres :
#   - automate : l'objet Automate a verifier
# retour : True si standard, False sinon
def est_standard(automate):
    # un seul etat initial
    if len(automate.initial) != 1:
        print(f"  -> Non standard : il y a {len(automate.initial)} etats initiaux au lieu de 1.")
        return False

    # index de l'etat init
    etat_initial = automate.initial[0]
    indice_etat_initial = automate.etats.index(etat_initial)
    nombre_etats = len(automate.etats)

    # verif qu'aucune transition pointe vers l'etat init
    for indice_depart in range(nombre_etats):
        # si y'a des transitions vers l'etat init c'est pas standard
        if len(automate.transitions[indice_depart][indice_etat_initial]) > 0:
            print(f"  -> Non standard : il y a une transition de l'etat {automate.etats[indice_depart]} vers l'etat initial {etat_initial}.")
            return False

    return True


# fonction : est_complet
# role : verifie si l'automate (deterministe) est complet. un automate deterministe est
#        complet si pour chaque etat et chaque symbole de l'alphabet, il existe exactement
#        une transition. affiche les raisons si incomplet.
# parametres :
#   - automate : l'objet Automate a verifier
# retour : True si complet, False sinon
def est_complet(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)
    resultat = True  # var de resultat

    # pour chaque etat on verifie qu'il y a une transition par symbole
    for indice_depart in range(nombre_etats):
        for symbole in automate.alphabet:
            transition_trouvee = False  # true si on trouve une transition
            # on cherche si le symbole apparait dans une transition sortante
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[indice_depart][indice_arrivee]:
                    transition_trouvee = True
                    break  # pas besoin de chercher plus loin
            # si rien trouvé
            if not transition_trouvee:
                print(f"  -> Non complet : pas de transition depuis l'etat {automate.etats[indice_depart]} avec le symbole '{symbole}'.")
                resultat = False

    return resultat


# fonction : standardiser
# role : cree un nouvel automate standard equivalent. on ajoute un nouvel etat initial 'i'
#        qui reprend toutes les transitions sortantes des anciens etats initiaux. l'ancien
#        etat initial n'est plus initial. si un ancien etat initial etait final, le nouvel
#        etat 'i' est aussi final.
# parametres :
#   - automate : l'objet Automate a standardiser
# retour : un nouvel objet Automate qui est la version standardisee
def standardiser(automate):
    # copie profonde pour pas modifier l'original
    nouveau = copy.deepcopy(automate)

    nombre_etats_ancien = len(nouveau.etats)
    nouvel_etat = 'i'  # nom du nouvel etat init

    # ajout du nouvel etat au debut
    nouveau.etats.insert(0, nouvel_etat)
    nombre_etats = len(nouveau.etats)

    # reconstruction matrice transitions avec une ligne/colonne en plus
    nouvelle_matrice = [[[] for _ in range(nombre_etats)] for _ in range(nombre_etats)]

    # recopie ancienne matrice dans la nouvelle (decalee de 1 car 'i' en pos 0)
    for indice_ligne in range(nombre_etats_ancien):
        for indice_colonne in range(nombre_etats_ancien):
            # +1 car le nouvel etat 'i' occupe l'index 0
            nouvelle_matrice[indice_ligne + 1][indice_colonne + 1] = list(nouveau.transitions[indice_ligne][indice_colonne])

    # copie des transitions sortantes des anciens etats init vers 'i'
    # comme ca 'i' se comporte comme les anciens init
    for ancien_initial in nouveau.initial:
        # index de l'ancien etat init dans la nouvelle liste
        indice_ancien_initial = nouveau.etats.index(ancien_initial)
        # pour chaque dest possible depuis cet ancien init
        for indice_destination in range(nombre_etats):
            for symbole in nouvelle_matrice[indice_ancien_initial][indice_destination]:
                # ajout seulement si pas deja present (eviter doublons)
                if symbole not in nouvelle_matrice[0][indice_destination]:
                    nouvelle_matrice[0][indice_destination].append(symbole)

    nouveau.transitions = nouvelle_matrice

    # si un ancien init etait final, le nouvel etat doit etre final aussi
    # car l'automate original acceptait le mot vide
    nouvel_etat_est_final = False
    for ancien_initial in nouveau.initial:
        if ancien_initial in nouveau.final:
            nouvel_etat_est_final = True
            break

    if nouvel_etat_est_final:
        nouveau.final.append(nouvel_etat)

    # maintenant le seul etat init c'est 'i'
    nouveau.initial = [nouvel_etat]

    # recalcul alphabet
    nouveau.get_alphabet()

    return nouveau


# fonction : epsilon_fermeture
# role : calcule l'epsilon-fermeture d'un ensemble d'etats, cad tous les etats
#        atteignables depuis ces etats en ne suivant que des epsilon-transitions.
#        utilise un parcours en largeur (BFS) avec une pile.
# parametres :
#   - automate : l'objet Automate contenant les transitions
#   - ensemble_etats : liste d'indices d'etats dont on veut calculer l'eps-fermeture
# retour : ensemble (set) des indices d'etats dans l'epsilon-fermeture
def epsilon_fermeture(automate, ensemble_etats):
    # fermeture = ensemble des etats atteignables par eps
    fermeture = set(ensemble_etats)
    # pile pour le parcours
    pile = list(ensemble_etats)
    nombre_etats = len(automate.etats)

    # tant qu'il reste des etats a traiter
    while pile:
        # on retire un etat
        etat_en_cours = pile.pop()
        # on regarde toutes les transitions sortantes
        for indice_arrivee in range(nombre_etats):
            # eps-transition + pas encore visite
            if 'eps' in automate.transitions[etat_en_cours][indice_arrivee] and indice_arrivee not in fermeture:
                fermeture.add(indice_arrivee)
                pile.append(indice_arrivee)  # on ajoute pour explorer ses propres eps-transitions

    return fermeture


# fonction : determiniser_et_completer
# role : construit l'automate deterministe complet equivalent a l'automate courant en
#        utilisant la construction par sous-ensembles. gere les epsilon-transitions.
#        chaque etat du nouvel automate correspond a un ensemble d'etats de l'original.
#        la notation est "123" si tous les etats <= 9, "1.2.3" sinon.
# parametres :
#   - automate : l'objet Automate a determiniser
# retour : un nouvel objet Automate deterministe et complet
def determiniser_et_completer(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # check si y'a des eps-transitions
    possede_epsilon = False
    for indice_depart in range(nombre_etats):
        for indice_arrivee in range(nombre_etats):
            if 'eps' in automate.transitions[indice_depart][indice_arrivee]:
                possede_epsilon = True
                break
        if possede_epsilon:
            break

    # calcul etat init du nouvel automate
    indices_initiaux = [automate.etats.index(etat) for etat in automate.initial]

    # si eps-transitions, etat init = eps-fermeture des initiaux
    if possede_epsilon:
        etat_initial_determinise = frozenset(epsilon_fermeture(automate, indices_initiaux))
    else:
        etat_initial_determinise = frozenset(indices_initiaux)

    # construction par sous-ensembles
    # etats_determinises = {frozenset d'indices -> index dans le nouvel automate}
    etats_determinises = {etat_initial_determinise: 0}
    # file d'attente pour le parcours en largeur
    file_attente = [etat_initial_determinise]
    # transitions_determinisees = liste de dicos {symbole -> frozenset d'indices}
    transitions_determinisees = []
    # ordre_etats = liste ordonnee des frozensets
    ordre_etats = [etat_initial_determinise]

    # tant qu'il reste des etats a explorer
    while file_attente:
        # prochain ensemble d'etats a traiter
        ensemble_courant = file_attente.pop(0)
        transitions_etat = {}  # transitions pour cet etat

        # pour chaque symbole, on calcule les etats atteignables
        for symbole in automate.alphabet:
            # destinations depuis l'ensemble courant avec le symbole
            destinations = set()
            # pour chaque etat dans l'ensemble courant
            for indice_etat in ensemble_courant:
                # on regarde chaque etat d'arrivee possible
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        destinations.add(indice_arrivee)

            # si eps-transitions, on applique l'eps-fermeture
            if possede_epsilon and destinations:
                destinations = epsilon_fermeture(automate, list(destinations))

            destination_figee = frozenset(destinations)
            transitions_etat[symbole] = destination_figee

            # si cet ensemble est nouveau on l'ajoute
            if destination_figee not in etats_determinises:
                etats_determinises[destination_figee] = len(etats_determinises)
                file_attente.append(destination_figee)
                ordre_etats.append(destination_figee)

        transitions_determinisees.append(transitions_etat)

    # construction du nouvel automate
    nouveau = Automate()
    nombre_nouveaux_etats = len(ordre_etats)

    # plus grand num d'etat original, pour choisir la notation
    nombre_etat_max = max(int(etat) for etat in automate.etats if etat.isdigit()) if any(etat.isdigit() for etat in automate.etats) else 0
    # utiliser_points = true si etats >= 10 (notation "1.2.3")
    utiliser_points = nombre_etat_max >= 10

    # noms des nouveaux etats + dico de correspondance
    for indice, ensemble in enumerate(ordre_etats):
        if not ensemble:
            # ensemble vide = etat poubelle
            nom = 'P'
        else:
            # tri des indices pour nom coherent
            indices_tries = sorted(ensemble)
            noms_tries = [automate.etats[indice_etat] for indice_etat in indices_tries]
            if utiliser_points:
                # notation avec points si etats >= 10 (ex: "1.12.3")
                nom = '.'.join(noms_tries)
            else:
                # notation concatenee si etats <= 9 (ex: "123")
                nom = ''.join(noms_tries)
        nouveau.etats.append(nom)
        # stockage correspondance pour l'affichage
        nouveau.correspondance[nom] = [automate.etats[indice_etat] for indice_etat in sorted(ensemble)] if ensemble else ['P']

    # etat init = premier etat (index 0)
    nouveau.initial = [nouveau.etats[0]]

    # un etat est final si au moins un des etats originaux qu'il contient est final
    indices_finaux = {automate.etats.index(etat) for etat in automate.final}
    for indice, ensemble in enumerate(ordre_etats):
        # intersection entre l'ensemble courant et les indices finaux
        if ensemble & indices_finaux:
            nouveau.final.append(nouveau.etats[indice])

    # matrice de transitions du nouvel automate
    nouveau.transitions = [[[] for _ in range(nombre_nouveaux_etats)] for _ in range(nombre_nouveaux_etats)]
    for indice, ensemble in enumerate(ordre_etats):
        for symbole in automate.alphabet:
            destination_ensemble = transitions_determinisees[indice][symbole]
            indice_destination = etats_determinises[destination_ensemble]
            nouveau.transitions[indice][indice_destination].append(symbole)

    nouveau.alphabet = list(automate.alphabet)

    # completion : ajout etat poubelle si necessaire
    possede_poubelle = 'P' in nouveau.etats

    # si pas de poubelle, on check s'il en faut une
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
            # on appelle completer() pour ajouter la poubelle
            nouveau = completer(nouveau)

    return nouveau


# fonction : completer
# role : complete un automate deterministe en ajoutant un etat poubelle 'P' et en ajoutant
#        toutes les transitions manquantes vers cet etat poubelle. l'etat poubelle boucle
#        sur lui-meme pour tous les symboles.
# parametres :
#   - automate : l'objet Automate a completer
# retour : un nouvel objet Automate complet
def completer(automate):
    nouveau = copy.deepcopy(automate)
    if not nouveau.alphabet:
        nouveau.get_alphabet()

    nombre_etats = len(nouveau.etats)

    # on check si la completion est necessaire
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
        # deja complet, pas besoin de poubelle
        return nouveau

    # ajout etat poubelle 'P'
    nouveau.etats.append('P')
    nombre_etats_avec_poubelle = len(nouveau.etats)

    # agrandissement matrice pour inclure P
    nouvelle_matrice = [[[] for _ in range(nombre_etats_avec_poubelle)] for _ in range(nombre_etats_avec_poubelle)]
    # recopie ancienne matrice
    for indice_depart in range(nombre_etats):
        for indice_arrivee in range(nombre_etats):
            nouvelle_matrice[indice_depart][indice_arrivee] = list(nouveau.transitions[indice_depart][indice_arrivee])

    # pour chaque etat/symbole, si pas de transition on redirige vers P
    indice_poubelle = nombre_etats_avec_poubelle - 1
    for indice_depart in range(nombre_etats_avec_poubelle):
        for symbole in nouveau.alphabet:
            transition_existe = False
            for indice_arrivee in range(nombre_etats_avec_poubelle):
                if symbole in nouvelle_matrice[indice_depart][indice_arrivee]:
                    transition_existe = True
                    break
            # si aucune transition, on redirige vers poubelle
            if not transition_existe:
                nouvelle_matrice[indice_depart][indice_poubelle].append(symbole)

    nouveau.transitions = nouvelle_matrice
    return nouveau


# fonction : minimiser
# role : construit l'automate minimal equivalent en utilisant l'algorithme de moore
#        (partitionnement successif). affiche chaque etape de partitionnement.
#        l'automate doit etre deterministe et complet avant la minimisation.
# parametres :
#   - automate : l'objet Automate a minimiser
# retour : un nouvel objet Automate minimal
def minimiser(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # partition initiale (P0) : finaux (grp 1) et non-finaux (grp 0)
    partition = [0] * nombre_etats
    for indice_etat in range(nombre_etats):
        if automate.etats[indice_etat] in automate.final:
            partition[indice_etat] = 1

    numero_partition = 0  # compteur pour l'affichage
    print(f"  Partition {numero_partition} : {_afficher_partition(automate, partition)}")

    # raffinement successif jusqu'au point fixe
    while True:
        nouvelle_partition = [0] * nombre_etats
        # signatures = {signature -> num de nouveau groupe}
        signatures = {}
        prochain_groupe = 0  # compteur pour les nouveaux grp

        # pour chaque etat on calcule sa signature
        for indice_etat in range(nombre_etats):
            # signature = (grp actuel, grp des destinations par symbole)
            # meme signature = meme groupe
            signature = [partition[indice_etat]]
            for symbole in automate.alphabet:
                # destination de l'etat avec ce symbole
                groupe_destination = -1
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        groupe_destination = partition[indice_arrivee]
                        break
                signature.append(groupe_destination)

            signature_tuple = tuple(signature)  # tuple pour utiliser comme cle

            # si nouvelle signature, on lui donne un nouveau num de grp
            if signature_tuple not in signatures:
                signatures[signature_tuple] = prochain_groupe
                prochain_groupe += 1

            nouvelle_partition[indice_etat] = signatures[signature_tuple]

        numero_partition += 1
        print(f"  Partition {numero_partition} : {_afficher_partition(automate, nouvelle_partition)}")

        # si partition inchangee, point fixe atteint
        if nouvelle_partition == partition:
            print("  => Point fixe atteint, la partition est stable.")
            break

        partition = nouvelle_partition

    # construction automate minimal
    nouveau = Automate()
    nombre_groupes = max(partition) + 1

    # noms des nouveaux etats = num de groupe
    nouveau.etats = [str(groupe) for groupe in range(nombre_groupes)]

    # correspondance : quel grp = quels anciens etats
    for groupe in range(nombre_groupes):
        etats_du_groupe = [automate.etats[indice] for indice in range(nombre_etats) if partition[indice] == groupe]
        nouveau.correspondance[str(groupe)] = etats_du_groupe

    # etat init = grp contenant l'ancien etat init
    for etat_initial in automate.initial:
        indice_initial = automate.etats.index(etat_initial)
        groupe_initial = str(partition[indice_initial])
        if groupe_initial not in nouveau.initial:
            nouveau.initial.append(groupe_initial)

    # etats finaux = grp contenant au moins un ancien etat final
    for etat_final in automate.final:
        indice_final = automate.etats.index(etat_final)
        groupe_final = str(partition[indice_final])
        if groupe_final not in nouveau.final:
            nouveau.final.append(groupe_final)

    # matrice transitions du nouvel automate
    nouveau.transitions = [[[] for _ in range(nombre_groupes)] for _ in range(nombre_groupes)]
    # on prend un representant de chaque grp
    for groupe in range(nombre_groupes):
        # representant = premier etat du grp
        representant = -1
        for indice_etat in range(nombre_etats):
            if partition[indice_etat] == groupe:
                representant = indice_etat
                break
        # pour chaque symbole, on regarde ou va le representant
        for symbole in automate.alphabet:
            for indice_arrivee in range(nombre_etats):
                if symbole in automate.transitions[representant][indice_arrivee]:
                    groupe_destination = partition[indice_arrivee]
                    if symbole not in nouveau.transitions[groupe][groupe_destination]:
                        nouveau.transitions[groupe][groupe_destination].append(symbole)
                    break

    nouveau.alphabet = list(automate.alphabet)
    return nouveau


# fonction : _afficher_partition
# role : formate une partition pour l'affichage. regroupe les etats par numero de groupe.
#        fct utilitaire privee (prefixe _), utilisee uniquement par minimiser().
# parametres :
#   - automate : l'objet Automate dont on affiche la partition
#   - partition : liste d'entiers, partition[i] = numero de groupe de l'etat i
# retour : chaine formatee (ex: "{0, 2, 3} {1, 4}")
def _afficher_partition(automate, partition):
    # groupes = {num grp -> liste noms etats}
    groupes = {}
    for indice, numero_groupe in enumerate(partition):
        if numero_groupe not in groupes:
            groupes[numero_groupe] = []
        groupes[numero_groupe].append(automate.etats[indice])

    # formatage chaque grp entre accolades
    parties = []
    for numero_groupe in sorted(groupes.keys()):
        parties.append('{' + ', '.join(groupes[numero_groupe]) + '}')
    return ' '.join(parties)


# fonction : reconnaitre_mot
# role : teste si un mot est reconnu par l'automate deterministe complet. on part de l'etat
#        initial et on suit les transitions symbole par symbole. si on arrive sur un etat
#        final a la fin du mot, le mot est reconnu.
# parametres :
#   - automate : l'objet Automate deterministe complet
#   - mot : chaine de caracteres a tester (ex: "aab")
# retour : True si le mot est reconnu, False sinon
def reconnaitre_mot(automate, mot):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # etat courant, on part de l'etat init
    indice_etat_courant = automate.etats.index(automate.initial[0])

    # cas special : mot vide (epsilon)
    if mot == '' or mot == 'eps':
        return automate.etats[indice_etat_courant] in automate.final

    # parcours du mot symbole par symbole
    for symbole in mot:
        # verif que le symbole est dans l'alphabet
        if symbole not in automate.alphabet:
            print(f"  Le symbole '{symbole}' n'appartient pas a l'alphabet {automate.alphabet}.")
            return False

        # on cherche la transition depuis l'etat courant avec ce symbole
        transition_trouvee = False
        # on cherche l'etat d'arrivee
        for indice_arrivee in range(nombre_etats):
            if symbole in automate.transitions[indice_etat_courant][indice_arrivee]:
                indice_etat_courant = indice_arrivee  # on avance
                transition_trouvee = True
                break

        # si rien trouve (devrait pas arriver si automate complet)
        if not transition_trouvee:
            return False

    # apres lecture du mot, on check si l'etat courant est final
    return automate.etats[indice_etat_courant] in automate.final


# fonction : complementaire
# role : construit l'automate reconnaissant le langage complementaire. on inverse simplement
#        les etats finaux et non-finaux : les anciens finaux deviennent non-finaux et
#        vice-versa. l'automate doit etre deterministe et complet.
# parametres :
#   - automate : l'objet Automate deterministe complet
# retour : un nouvel objet Automate reconnaissant le langage complementaire
def complementaire(automate):
    # copie profonde pour pas toucher l'original
    nouveau = copy.deepcopy(automate)

    # nouveaux finaux = tous les etats qui etaient PAS finaux avant
    nouveaux_finaux = [etat for etat in nouveau.etats if etat not in nouveau.final]

    # on remplace
    nouveau.final = nouveaux_finaux

    return nouveau
