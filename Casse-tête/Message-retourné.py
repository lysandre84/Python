#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
 Script     : Message-retourné.py
 Auteur     : Lysius
 Date       : 12/08/2024
 Description: Écrivez la phrase « LES MATHS SONT FUN » puis faites pivoter
              chaque caractère de 180°.
              Quel mot français positif apparaît ?

Processus :
 1) Afficher l’énoncé.
 2) Attendre une touche.
 3) Afficher la réponse.
=====================================================================================================================================================
"""
import textwrap


def affiche_enonce() -> None:
    """Affiche l’énoncé du puzzle dans la console."""
    enonce = (
        "Écrivez la phrase « LES MATHS SONT FUN » puis faites pivoter "
        "chaque caractère de 180°. Quel mot français positif apparaît ?"
    )
    print(textwrap.fill(enonce, 70))


def affiche_reponse() -> None:
    """Affiche la solution à l’issue de l’appui sur une touche."""
    reponse = "Réponse : FUN"
    print(reponse)


def main() -> None:
    """Point d’entrée du script."""
    affiche_enonce()
    input("\nAppuyez sur Entrée pour la réponse…\n")
    affiche_reponse()


if __name__ == "__main__":
    main()