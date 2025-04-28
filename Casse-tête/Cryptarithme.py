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
 Script     : Cryptarithme.py
 Auteur     : Lysius
 Date       : 19/06/2024
 Description: Script de démonstration du cryptarithme :
             (S U M) × S = S Q U A R E
             Chaque lettre représente un chiffre distinct, S ≠ 0.
             Ce script vérifie par force brute qu'aucune affectation ne satisfait l'équation,
             confirmant ainsi l'impossibilité du cryptarithme.
=====================================================================================================================================================
"""
import itertools
import textwrap

def solve_cryptarithm() -> bool:
    """
    Parcourt toutes les permutations de chiffres pour les lettres S, U, M, Q, A, R, E.
    Retourne True si une solution est trouvée, False sinon.
    """
    lettres = 'SUMQARE'
    for perm in itertools.permutations('0123456789', len(lettres)):
        mapping = dict(zip(lettres, perm))
        # S ne peut pas être 0
        if mapping['S'] == '0':
            continue
        # Construction des nombres SUM et SQUARE
        sum_val = int(''.join(mapping[c] for c in 'SUM'))
        square_val = int(''.join(mapping[c] for c in 'SQUARE'))
        # Vérification de l'égalité
        if sum_val * int(mapping['S']) == square_val:
            print(f"Solution trouvée : SUM = {sum_val}, S = {mapping['S']} => SQUARE = {square_val}")
            return True
    return False


def main():
    # Affichage de l'énoncé
    enonce = (
        "Chaque lettre représente un chiffre distinct (S ≠ 0).\n"
        "Peut-on avoir (S U M) × S = S Q U A R E ?"
    )
    print(textwrap.fill(enonce, 70))
    input("\nAppuyez sur Entrée pour lancer la recherche…\n")

    # Recherche de la solution
    if not solve_cryptarithm():
        demo = (
            "Aucune solution n'a été trouvée parmi les 10P7 = 6048000 affectations possibles. "
            "Le cryptarithme est donc impossible."
        )
        print(textwrap.fill(demo, 70))

if __name__ == '__main__':
    main()
