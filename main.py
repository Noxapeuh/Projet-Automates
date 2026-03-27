from lecture import lire_automate, afficher_automate, sauvegarder_automate
from manipulation import (est_deterministe, est_standard, est_complet,
                          standardiser, determiniser_et_completer, completer,
                          minimiser, reconnaitre_mot, complementaire)
import copy
import os


# ============================================================================================
# Fonction : afficher_menu_principal
# Role : Affiche le menu principal qui permet de choisir un automate ou de quitter le programme.
# Parametres : Aucun
# ============================================================================================
def afficher_menu_principal():
    print("\n" + "=" * 60)
    print("   PROJET AUTOMATES FINIS - EFREI P2 2025/2026")
    print("=" * 60)
    print("  1. Choisir un automate")
    print("  9. Quitter")
    print("-" * 60)


# ============================================================================================
# Fonction : afficher_menu_automate
# Role : Affiche le menu des opérations disponibles pour l'automate chargé.
#        Indique l'état actuel de l'automate (déterministe, standard, complet, minimisé).
# Parametres :
#   - numero_automate : numéro de l'automate chargé
#   - est_deterministe_flag : True si l'automate courant est déterministe
#   - est_standard_flag : True si l'automate courant est standard
#   - est_complet_flag : True si l'automate courant est complet
#   - est_minimise : True si l'automate courant a été minimisé
# ============================================================================================
def afficher_menu_automate(numero_automate, est_deterministe_flag, est_standard_flag, est_complet_flag, est_minimise):
    print("\n" + "=" * 60)
    print(f"   AUTOMATE N.{numero_automate}")
    print("=" * 60)

    # --- Affichage de l'état actuel de l'automate ---
    # On utilise des indicateurs pour montrer visuellement le statut
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


# ============================================================================================
# Fonction : verifier_proprietes
# Role : Vérifie les propriétés de l'automate (déterministe, standard, complet) SANS afficher
#        les messages détaillés. Utilisé pour mettre à jour les indicateurs du menu.
# Parametres :
#   - automate : l'objet Automate à vérifier
# Retour : tuple (verification_deterministe, verification_standard, verification_complet)
# ============================================================================================
def verifier_proprietes(automate):
    if not automate.alphabet:
        automate.get_alphabet()

    nombre_etats = len(automate.etats)

    # --- Vérification déterministe (silencieuse) ---
    verification_deterministe = True
    if len(automate.initial) != 1:
        verification_deterministe = False
    else:
        for indice_etat in range(nombre_etats):
            # On vérifie qu'il n'y a pas plusieurs transitions par symbole
            for symbole in automate.alphabet:
                nombre_destinations = 0
                for indice_arrivee in range(nombre_etats):
                    if symbole in automate.transitions[indice_etat][indice_arrivee]:
                        nombre_destinations += 1
                if nombre_destinations > 1:
                    verification_deterministe = False
                    break
            # On vérifie qu'il n'y a pas d'epsilon-transitions
            for indice_arrivee in range(nombre_etats):
                if 'eps' in automate.transitions[indice_etat][indice_arrivee]:
                    verification_deterministe = False
                    break
            if not verification_deterministe:
                break

    # --- Vérification standard (silencieuse) ---
    verification_standard = True
    if len(automate.initial) != 1:
        verification_standard = False
    else:
        indice_etat_initial = automate.etats.index(automate.initial[0])
        for indice_etat in range(nombre_etats):
            if len(automate.transitions[indice_etat][indice_etat_initial]) > 0:
                verification_standard = False
                break

    # --- Vérification complet (silencieuse, seulement si déterministe) ---
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


# ============================================================================================
# Fonction : main
# Role : Point d'entrée du programme. Implémente la boucle interactive avec un système de menus.
#        Le menu principal permet de choisir un automate. Le menu automate permet d'appliquer
#        les différentes opérations et de sauvegarder le résultat.
# Parametres : Aucun
# ============================================================================================
def main():
    # --- Boucle principale du programme ---
    # La boucle tourne jusqu'à ce que l'utilisateur choisisse de quitter (option 9)
    while True:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip()

        if choix == '9':
            print("Au revoir !")
            break
        elif choix == '1':
            # --- Sélection d'un automate ---
            numero_saisi = input("Entrez le numero de l'automate : ").strip()

            # On vérifie que l'entrée est bien un nombre
            if not numero_saisi.isdigit():
                print("Erreur : veuillez entrer un numero valide.")
                continue

            numero_automate = int(numero_saisi)
            nom_fichier = f"Automates_Test/{numero_automate:02d}.txt"

            # On vérifie que le fichier existe avant de le lire
            if not os.path.exists(nom_fichier):
                print(f"Erreur : le fichier '{nom_fichier}' n'existe pas.")
                continue

            # Appel à lire_automate() pour charger l'automate depuis le fichier
            automate_original = lire_automate(nom_fichier)

            # automate_courant : l'automate sur lequel on travaille (peut être transformé)
            automate_courant = copy.deepcopy(automate_original)

            # est_minimise : sera mis à True après une minimisation explicite
            est_minimise = False

            # Appel au menu_automate() pour gérer les opérations sur cet automate
            quitter = menu_automate(numero_automate, automate_original, automate_courant, est_minimise)
            if quitter:
                print("Au revoir !")
                break
        else:
            print("Choix invalide.")


# ============================================================================================
# Fonction : menu_automate
# Role : Gère le menu interactif pour un automate chargé. Permet d'appliquer les transformations
#        (standardiser, déterminiser, minimiser), de tester des mots, de construire le
#        complémentaire, et de sauvegarder le résultat.
# Parametres :
#   - numero_automate : numéro de l'automate (pour l'affichage et la sauvegarde)
#   - automate_original : l'automate tel qu'il a été lu du fichier (jamais modifié)
#   - automate_courant : l'automate courant, potentiellement transformé
#   - est_minimise : True si l'automate a été minimisé
# ============================================================================================
def menu_automate(numero_automate, automate_original, automate_courant, est_minimise):
    # --- Boucle du menu automate ---
    while True:
        # On recalcule les propriétés à chaque tour car l'automate peut avoir changé
        # Appel à verifier_proprietes() pour obtenir les indicateurs sans messages verbeux
        verification_deterministe, verification_standard, verification_complet = verifier_proprietes(automate_courant)

        # Affichage du menu avec les indicateurs à jour
        afficher_menu_automate(numero_automate, verification_deterministe, verification_standard, verification_complet, est_minimise)
        choix = input("Votre choix : ").strip()

        # === Option 1 : Afficher l'automate ===
        if choix == '1':
            print(f"\nAlphabet : {automate_courant.alphabet}")
            print(f"Etats : {automate_courant.etats}")
            print(f"Etat(s) initial/initiaux : {automate_courant.initial}")
            print(f"Etat(s) final/finaux : {automate_courant.final}")

            # Si l'automate a une correspondance (il a été déterminisé ou minimisé),
            # on l'affiche pour que l'utilisateur comprenne la relation avec l'original
            if automate_courant.correspondance:
                print("\nCorrespondance des etats :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")

            print()
            # Appel à afficher_automate() pour montrer la table de transitions formatée
            afficher_automate(automate_courant)

            # On affiche aussi les vérifications détaillées
            print("--- Verifications detaillees ---")
            print("\n* Deterministe ?")
            # Appel à est_deterministe() pour afficher les raisons détaillées
            resultat_deterministe = est_deterministe(automate_courant)
            print(f"  => {'OUI' if resultat_deterministe else 'NON'}")

            print("\n* Standard ?")
            # Appel à est_standard() pour afficher les raisons détaillées
            resultat_standard = est_standard(automate_courant)
            print(f"  => {'OUI' if resultat_standard else 'NON'}")

            if resultat_deterministe:
                print("\n* Complet ?")
                # Appel à est_complet() pour afficher les raisons détaillées
                resultat_complet = est_complet(automate_courant)
                print(f"  => {'OUI' if resultat_complet else 'NON'}")

        # === Option 2 : Standardiser ===
        elif choix == '2':
            if verification_standard:
                print("\nL'automate est deja standard, pas besoin de le standardiser.")
            else:
                print("\nStandardisation en cours...")
                # Appel à standardiser() pour créer un nouvel état initial sans transitions entrantes
                automate_courant = standardiser(automate_courant)
                est_minimise = False  # La minimisation n'est plus valide après une transformation
                print("Automate standardise :")
                # Appel à afficher_automate() pour montrer le résultat
                afficher_automate(automate_courant)

        # === Option 3 : Déterminiser et compléter ===
        elif choix == '3':
            if verification_deterministe and verification_complet:
                # ATTENTION : on ne doit PAS re-déterminiser un automate déjà déterministe (consigne)
                print("\nL'automate est deja deterministe et complet.")
            elif verification_deterministe and not verification_complet:
                print("\nL'automate est deterministe mais pas complet. Completion en cours...")
                # Appel à completer() car seule la complétion est nécessaire
                automate_courant = completer(automate_courant)
                est_minimise = False
                print("Automate apres completion :")
                afficher_automate(automate_courant)
            else:
                print("\nDeterminisation et completion en cours...")
                # Appel à determiniser_et_completer() pour la construction par sous-ensembles
                automate_courant = determiniser_et_completer(automate_courant)
                est_minimise = False
                print("\nAutomate deterministe complet (AFDC) :")
                print("Correspondance des etats :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")
                print()
                afficher_automate(automate_courant)

        # === Option 4 : Minimiser ===
        elif choix == '4':
            if not verification_deterministe or not verification_complet:
                print("\nL'automate doit etre deterministe et complet avant la minimisation.")
                print("Veuillez d'abord choisir l'option 3 (Determiniser et completer).")
            elif est_minimise:
                print("\nL'automate est deja minimise.")
            else:
                print("\nMinimisation en cours...")
                print("Partitions successives :")
                # Appel à minimiser() pour l'algorithme de Moore (affiche les partitions)
                automate_courant = minimiser(automate_courant)
                est_minimise = True
                print("\nAutomate minimal (AFDCM) :")
                print("Correspondance des etats :")
                for etat, anciens in automate_courant.correspondance.items():
                    print(f"  {etat} <- {{{', '.join(anciens)}}}")
                print()
                afficher_automate(automate_courant)

        # === Option 5 : Reconnaissance de mot ===
        elif choix == '5':
            if not verification_deterministe or not verification_complet:
                print("\nL'automate doit etre deterministe et complet pour la reconnaissance de mots.")
                print("Veuillez d'abord choisir l'option 3 (Determiniser et completer).")
            else:
                print(f"\nAlphabet de l'automate : {automate_courant.alphabet}")
                mot = input("Entrez le mot a tester (mot vide = epsilon) : ").strip()
                # Appel à reconnaitre_mot() pour tester le mot sur l'automate
                if reconnaitre_mot(automate_courant, mot):
                    print(f"  => Le mot '{mot}' est RECONNU par l'automate.")
                else:
                    print(f"  => Le mot '{mot}' n'est PAS reconnu par l'automate.")

        # === Option 6 : Automate complémentaire ===
        elif choix == '6':
            if not verification_deterministe or not verification_complet:
                print("\nL'automate doit etre deterministe et complet pour calculer le complementaire.")
                print("Veuillez d'abord choisir l'option 3 (Determiniser et completer).")
            else:
                print("\nConstruction de l'automate complementaire...")
                # Appel à complementaire() pour inverser les états finaux et non-finaux
                automate_complementaire = complementaire(automate_courant)
                print(f"Etats finaux actuels : {automate_courant.final}")
                print(f"Nouveaux etats finaux (complementaire) : {automate_complementaire.final}\n")
                afficher_automate(automate_complementaire)

        # === Option 7 : Sauvegarder l'automate ===
        elif choix == '7':
            # Appel à sauvegarder_automate() pour écrire l'automate dans un fichier versionné
            chemin = sauvegarder_automate(automate_courant, numero_automate)
            print(f"\nAutomate sauvegarde dans : {chemin}")

        # === Option 8 : Choisir un autre automate ===
        elif choix == '8':
            # On sort du menu automate pour revenir au menu principal
            break

        # === Option 9 : Quitter ===
        elif choix == '9':
            return True  # On signale au menu principal qu'il faut quitter
        else:
            print("Choix invalide.")

    return False  # Retour au menu principal sans quitter


# Point d'entrée du programme
# On appelle main() uniquement si ce fichier est exécuté directement (pas importé)
if __name__ == '__main__':
    main()
