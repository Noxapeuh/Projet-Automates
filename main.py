from lecture import lire_automate, afficher_automate, sauvegarder_automate
from manipulation import (est_deterministe, est_standard, est_complet,
                          standardiser, determiniser_et_completer, completer,
                          minimiser, reconnaitre_mot, complementaire)
import copy
import os


# fonction : afficher_menu_principal
# role : affiche le menu principal qui permet de choisir un automate ou de quitter le programme.
# parametres : aucun
def afficher_menu_principal():
    print("\n1. Choisir un automate")
    print("9. Quitter")


# fonction : afficher_menu_automate
# role : affiche le menu des operations disponibles pour l'automate charge.
#        indique l'etat actuel de l'automate (deterministe, standard, complet, minimise).
# parametres :
#   - numero_automate : numero de l'automate charge
#   - est_deterministe_flag : True si l'automate courant est deterministe
#   - est_standard_flag : True si l'automate courant est standard
#   - est_complet_flag : True si l'automate courant est complet
#   - est_minimise : True si l'automate courant a ete minimise
def afficher_menu_automate(numero_automate, est_deterministe_flag, est_standard_flag, est_complet_flag, est_minimise):
    print("\n" + "=" * 60)
    print(f"                     AUTOMATE N.{numero_automate}")
    print("=" * 60)

    # affichage etat actuel avec indicateurs
    print(f"  Deterministe : {'[OUI]' if est_deterministe_flag else '[NON]'}")
    print(f"  Standard     : {'[OUI]' if est_standard_flag else '[NON]'}")
    print(f"  Complet      : {'[OUI]' if est_complet_flag else '[NON]'}")
    print(f"  Minimise     : {'[OUI]' if est_minimise else '[NON]'}")

    print("-" * 60)
    print("  1. Afficher l'automate")
    print("  2. Standardiser")
    print("  3. Determiniser et completer")
    print("  4. Minimiser")
    print("  5. Reconnaitre un mot")
    print("  6. Automate complementaire")
    print("  7. Sauvegarder l'automate")
    print("  8. Choisir un autre automate")
    print("  9. Quitter")
    print("-" * 60)


# fonction : verifier_proprietes
# role : verifie les proprietes de l'automate (deterministe, standard, complet) sans afficher
#        les messages detailles. utilise pour mettre a jour les indicateurs du menu.
# parametres :
#   - automate : l'objet Automate a verifier
# retour : tuple (verification_deterministe, verification_standard, verification_complet)
def verifier_proprietes(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # verif deterministe (silencieuse)
    verification_deterministe = True
    if len(automate.initial) != 1:
        verification_deterministe = False
    else:
        for indice_etat in range(nombre_etats):
            # check pas plusieurs transitions par symbole
            for symbole in automate.alphabet:
                nombre_destinations = 0
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        nombre_destinations += 1
                if nombre_destinations > 1:
                    verification_deterministe = False
                    break
            # check pas d'eps-transitions
            for indice_arrivee in range(nombre_etats):
                if 'eps' in automate.transitions[indice_etat][indice_arrivee]:
                    verification_deterministe = False
                    break
            if not verification_deterministe:
                break

    # verif standard (silencieuse)
    verification_standard = True
    if len(automate.initial) != 1:
        verification_standard = False
    else:
        indice_etat_initial = automate.etats.index(automate.initial[0])
        for indice_etat in range(nombre_etats):
            if len(automate.transitions[indice_etat][indice_etat_initial]) > 0:
                verification_standard = False
                break

    # verif complet (silencieuse, seulement si deterministe)
    verification_complet = False
    if verification_deterministe:
        verification_complet = True
        for indice_etat in range(nombre_etats):
            for symbole in automate.alphabet:
                transition_trouvee = False
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        transition_trouvee = True
                        break
                if not transition_trouvee:
                    verification_complet = False
                    break
            if not verification_complet:
                break

    return verification_deterministe, verification_standard, verification_complet


# fonction : main
# role : point d'entree du programme. implemente la boucle interactive avec un systeme de menus.
#        le menu principal permet de choisir un automate. le menu automate permet d'appliquer
#        les differentes operations et de sauvegarder le resultat.
# parametres : aucun
def main():
    # boucle principale, tourne jusqu'a quitter (option 9)
    while True:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip()

        if choix == '9':
            break
        elif choix == '1':
            # selection d'un automate
            numero_saisi = input("Numero de l'automate : ").strip()

            # verif que c'est un nombre
            if not numero_saisi.isdigit():
                print("Erreur : veuillez entrer un numero valide.")
                continue

            numero_automate = int(numero_saisi)
            nom_fichier = f"Automates_Test/{numero_automate:02d}.txt"

            # verif que le fichier existe
            if not os.path.exists(nom_fichier):
                print(f"Erreur : '{nom_fichier}' n'existe pas.")
                continue

            # chargement de l'automate depuis le fichier
            automate_original = lire_automate(nom_fichier)

            # automate_courant = celui sur lequel on travaille (peut etre transforme)
            automate_courant = copy.deepcopy(automate_original)

            # sera mis a true apres minimisation
            est_minimise = False

            # lancement menu automate
            quitter = menu_automate(numero_automate, automate_original, automate_courant, est_minimise)
            if quitter:
                break
        else:
            print("Choix invalide.")


# fonction : menu_automate
# role : gere le menu interactif pour un automate charge. permet d'appliquer les transformations
#        (standardiser, determiniser, minimiser), de tester des mots, de construire le
#        complementaire, et de sauvegarder le resultat.
# parametres :
#   - numero_automate : numero de l'automate (pour l'affichage et la sauvegarde)
#   - automate_original : l'automate tel qu'il a ete lu du fichier (jamais modifie)
#   - automate_courant : l'automate courant, potentiellement transforme
#   - est_minimise : True si l'automate a ete minimise
def menu_automate(numero_automate, automate_original, automate_courant, est_minimise):
    # boucle du menu automate
    while True:
        # recalcul des proprietes a chaque tour car l'automate peut changer
        verification_deterministe, verification_standard, verification_complet = verifier_proprietes(automate_courant)

        # affichage menu avec indicateurs a jour
        afficher_menu_automate(numero_automate, verification_deterministe, verification_standard, verification_complet, est_minimise)
        choix = input("Votre choix : ").strip()

        # option 1 : afficher l'automate
        if choix == '1':
            print(f"\nAlphabet : {automate_courant.alphabet}")
            print(f"Etats : {automate_courant.etats}")
            print(f"Etat(s) initial/initiaux : {automate_courant.initial}")
            print(f"Etat(s) final/finaux : {automate_courant.final}")

            # si correspondance (determ ou minim), on l'affiche
            if automate_courant.correspondance:
                print("\nCorrespondance des etats :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")

            print()
            # table de transitions formatee
            afficher_automate(automate_courant)

            # verifications detaillees
            print("Deterministe ?")
            resultat_deterministe = est_deterministe(automate_courant)
            print(f"  => {'OUI' if resultat_deterministe else 'NON'}")

            print("Standard ?")
            resultat_standard = est_standard(automate_courant)
            print(f"  => {'OUI' if resultat_standard else 'NON'}")

            if resultat_deterministe:
                print("Complet ?")
                resultat_complet = est_complet(automate_courant)
                print(f"  => {'OUI' if resultat_complet else 'NON'}")

        # option 2 : standardiser
        elif choix == '2':
            if verification_standard:
                print("\nL'automate est deja standard, pas besoin de le standardiser.")
            else:
                print("Standardisation...")
                # creation nouvel etat init sans transitions entrantes
                automate_courant = standardiser(automate_courant)
                est_minimise = False  # minimisation plus valide apres transfo
                afficher_automate(automate_courant)

        # option 3 : determiniser et completer
        elif choix == '3':
            if verification_deterministe and verification_complet:
                # on re-determinise pas un automate deja det (consigne)
                print("\nL'automate est deja deterministe et complet.")
            elif verification_deterministe and not verification_complet:
                print("\nL'automate est deterministe mais pas complet. Completion en cours...")
                # juste la completion car deja det
                automate_courant = completer(automate_courant)
                est_minimise = False
                print("Automate apres completion :")
                afficher_automate(automate_courant)
            else:
                print("\nDeterminisation et completion en cours...")
                # construction par sous-ensembles
                automate_courant = determiniser_et_completer(automate_courant)
                est_minimise = False
                print("\nAutomate deterministe complet (AFDC) :")
                print("Correspondance des etats :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")
                print()
                afficher_automate(automate_courant)

        # option 4 : minimiser
        elif choix == '4':
            if not verification_deterministe or not verification_complet:
                print("Il faut d'abord determiniser et completer (option 3).")
            elif est_minimise:
                print("\nL'automate est deja minimise.")
            else:
                print("Minimisation...")
                # algo de moore, affiche les partitions
                automate_courant = minimiser(automate_courant)
                est_minimise = True
                print("Correspondance :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")
                print()
                afficher_automate(automate_courant)

        # option 5 : reconnaissance de mot
        elif choix == '5':
            if not verification_deterministe or not verification_complet:
                print("Il faut d'abord determiniser et completer (option 3).")
            else:
                print(f"\nAlphabet de l'automate : {automate_courant.alphabet}")
                mot = input("Entrez le mot a tester (mot vide = epsilon) : ").strip()
                # test du mot sur l'automate
                if reconnaitre_mot(automate_courant, mot):
                    print(f"  => Le mot '{mot}' est RECONNU par l'automate.")
                else:
                    print(f"  => Le mot '{mot}' n'est PAS reconnu par l'automate.")

        # option 6 : automate complementaire
        elif choix == '6':
            if not verification_deterministe or not verification_complet:
                print("Il faut d'abord determiniser et completer (option 3).")
            else:
                print("Complementaire...")
                # inversion etats finaux/non-finaux
                automate_complementaire = complementaire(automate_courant)
                print(f"Etats finaux actuels : {automate_courant.final}")
                print(f"Nouveaux etats finaux (complementaire) : {automate_complementaire.final}\n")
                afficher_automate(automate_complementaire)

        # option 7 : sauvegarder
        elif choix == '7':
            # ecriture dans un fichier versionne
            chemin = sauvegarder_automate(automate_courant, numero_automate)
            print(f"\nAutomate sauvegarde dans : {chemin}")

        # option 8 : autre automate
        elif choix == '8':
            # retour au menu principal
            break

        # option 9 : quitter
        elif choix == '9':
            return True  # on signale au menu principal de quitter
        else:
            print("Choix invalide.")

    return False  # retour au menu principal sans quitter


# point d'entree, on appelle main() si le fichier est execute directement
if __name__ == '__main__':
    main()
