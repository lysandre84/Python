#!/usr/bin/env python3
"""
=====================================================================================================================================================

  /$$$$$$                                                   /$$                 /$$              
 /$$__  $$                                                 | $$                | $$              
| $$  \__/  /$$$$$$   /$$$$$$$ /$$$$$$$  /$$$$$$          /$$$$$$    /$$$$$$  /$$$$$$    /$$$$$$ 
| $$       |____  $$ /$$_____//$$_____/ /$$__  $$ /$$$$$$|_  $$_/   /$$__  $$|_  $$_/   /$$__  $$
| $$        /$$$$$$$|  $$$$$$|  $$$$$$ | $$$$$$$$|______/  | $$    | $$$$$$$$  | $$    | $$$$$$$$
| $$    $$ /$$__  $$ \____  $$\____  $$| $$_____/          | $$ /$$| $$_____/  | $$ /$$| $$_____/
|  $$$$$$/|  $$$$$$$ /$$$$$$$//$$$$$$$/|  $$$$$$$          |  $$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$
 \______/  \_______/|_______/|_______/  \_______/           \___/   \_______/   \___/   \_______/
                                                                                                 
                                                                                                                                                                                  
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : Interrupteur.py
 Auteur     : Lysius
 Date       : 01/07/2024
 Description: Ce script présente le puzzle des trois interrupteurs A, B, C
              et explique la méthode pour identifier celui qui allume
              une ampoule dans la pièce voisine, sachant que la porte
              ne peut être ouverte qu’une seule fois.

Processus :
 1) Allumer A et attendre quelques minutes.
 2) Éteindre A, allumer B.
 3) Laisser C éteint.
 4) Ouvrir la porte et inspecter l’ampoule :
    • Allumée    → interrupteur B.
    • Éteinte mais chaude → interrupteur A.
    • Éteinte et froide  → interrupteur C.
=====================================================================================================================================================
"""
import textwrap


def affiche_enonce() -> None:
    """Affiche l’énoncé du puzzle."""
    enonce = (
        "Trois interrupteurs (A, B, C) commandent une unique ampoule dans "
        "la pièce voisine. Vous ne pouvez ouvrir la porte qu’une seule "
        "fois. Comment identifier l’interrupteur correct ?"
    )
    print(textwrap.fill(enonce, 70))


def affiche_method() -> None:
    """Affiche la méthode pas-à-pas pour résoudre le puzzle."""
    method = (
        "1. Allumez l’interrupteur A et patientez quelques minutes (l’ampoule "
        "chauffe si c’est le bon).\n"
        "2. Éteignez A et allumez B.\n"
        "3. Laissez C éteint.\n"
        "4. Ouvrez la porte et examinez l’ampoule :\n"
        "   • Si elle est allumée, c’est B.\n"
        "   • Si elle est éteinte mais chaude, c’est A.\n"
        "   • Si elle est éteinte et froide, c’est C."
    )
    print(textwrap.fill(method, 70))


def main() -> None:
    """Point d’entrée du script."""
    affiche_enonce()
    input("\nAppuyez sur Entrée pour découvrir la méthode…\n")
    affiche_method()


if __name__ == "__main__":
    main()
