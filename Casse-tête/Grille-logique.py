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
 Script     : Grille-logique.py
 Auteur     : Lysius
 Date       : 29/06/2024
 Description: Script de démonstration pour résoudre une grille logique :
              Chaque personne (Emma, Léo, Noé, Yara) est associée à une ville
              (Athènes, Berlin, Lima, Oslo) et à un souvenir
              (Aimant, Écharpe, Livre, Mug) à partir d’indices logiques.

            Le script affiche l’énoncé, attend une touche, puis présente
            la solution formatée dans la console.
=====================================================================================================================================================
"""
import textwrap
from itertools import permutations
from typing import List, Tuple, Dict

# --- Données du problème ---
PERSONNES: List[str] = ["Emma", "Léo", "Noé", "Yara"]
VILLES:    List[str] = ["Athènes", "Berlin", "Lima", "Oslo"]
SOUVENIRS: List[str] = ["Aimant", "Écharpe", "Livre", "Mug"]


def affiche_enonce() -> None:
    """Affiche l'énoncé dans la console."""
    enonce = (
        "Personnes : Emma, Léo, Noé, Yara\n"
        "Villes    : Athènes, Berlin, Lima, Oslo\n"
        "Souvenirs : Aimant, Écharpe, Livre, Mug\n\n"
        "Indices :\n"
        "1. Athènes n’a pas donné un mug.\n"
        "2. Yara a rapporté un aimant.\n"
        "3. Noé n’est pas allé en Europe (Athènes, Berlin, Oslo).\n"
        "4. Le livre provient de Berlin.\n"
        "5. L’écharpe ne vient pas d’Oslo."
    )
    print(textwrap.fill(enonce, 70))


def trouve_solution() -> List[List[Tuple[str, str, str]]]:
    """
    Recherche par brute force de la solution.
    Retourne une liste de solutions (personne, ville, souvenir).
    """
    solutions: List[List[Tuple[str, str, str]]] = []
    for villes_perm in permutations(VILLES):
        for souvenirs_perm in permutations(SOUVENIRS):
            perso_to_ville: Dict[str, str] = dict(zip(PERSONNES, villes_perm))
            ville_to_souvenir: Dict[str, str] = dict(zip(villes_perm, souvenirs_perm))

            # Vérification des indices
            cond1 = ville_to_souvenir.get("Athènes") != "Mug"
            cond2 = ville_to_souvenir.get(perso_to_ville["Yara"]) == "Aimant"
            cond3 = perso_to_ville["Noé"] not in ["Athènes", "Berlin", "Oslo"]
            cond4 = ville_to_souvenir.get("Berlin") == "Livre"
            cond5 = ville_to_souvenir.get("Oslo") != "Écharpe"

            if all([cond1, cond2, cond3, cond4, cond5]):
                solution = [
                    (p, perso_to_ville[p], ville_to_souvenir[perso_to_ville[p]])
                    for p in PERSONNES
                ]
                solutions.append(solution)
    return solutions


def affiche_solution(sol: List[Tuple[str, str, str]]) -> None:
    """Affiche une solution formatée."""
    print("\nSolution :")
    for personne, ville, souvenir in sol:
        print(f"{personne:<5} — {ville:<8} — {souvenir}")


def main() -> None:
    affiche_enonce()
    input("\nAppuyez sur Entrée pour afficher la solution…\n")
    solutions = trouve_solution()
    if solutions:
        affiche_solution(solutions[0])
    else:
        print("Aucune solution trouvée.")


if __name__ == "__main__":
    main()
