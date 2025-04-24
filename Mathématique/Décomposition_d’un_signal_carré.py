#!/usr/bin/env python3
"""
=====================================================================================================================================================

 /$$      /$$             /$$     /$$                                 /$$     /$$                              
| $$$    /$$$            | $$    | $$                                | $$    |__/                              
| $$$$  /$$$$  /$$$$$$  /$$$$$$  | $$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$ 
| $$ $$/$$ $$ |____  $$|_  $$_/  | $$__  $$| $$_  $$_  $$ |____  $$|_  $$_/  | $$ /$$__  $$| $$  | $$ /$$__  $$
| $$  $$$| $$  /$$$$$$$  | $$    | $$  \ $$| $$ \ $$ \ $$  /$$$$$$$  | $$    | $$| $$  \ $$| $$  | $$| $$$$$$$$
| $$\  $ | $$ /$$__  $$  | $$ /$$| $$  | $$| $$ | $$ | $$ /$$__  $$  | $$ /$$| $$| $$  | $$| $$  | $$| $$_____/
| $$ \/  | $$|  $$$$$$$  |  $$$$/| $$  | $$| $$ | $$ | $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$$|  $$$$$$/|  $$$$$$$
|__/     |__/ \_______/   \___/  |__/  |__/|__/ |__/ |__/ \_______/   \___/  |__/ \____  $$ \______/  \_______/
                                                                                       | $$                    
                                                                                       | $$                    
                                                                                       |__/                    
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : Décomposition_d'un_signal_carré.py
 Auteur     : Lysius
 Date       : 01/12/2024
 Description: 
=====================================================================================================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

# Définition de la fonction 2π-périodique paire correspondante
# à un signal carré d'amplitude 1 centré sur 0
# f(t)=1 si t ∈ [0,π/2[ et f(t)=0 si t ∈ [π/2,π[
def f(t):
    # Calcul du modulo 2π avec symétrie paire
    x =  np.abs((t + np.pi) % (2*np.pi) - np.pi)

    return np.where(
        (x >= 0) &
        (x <= np.pi/2)
        , 1
        , 0
    )

# POINT D'ENTREE DU SCRIPT PYTHON
if __name__ == "__main__":

    # Etendue du tracé
    t = np.linspace(-2*np.pi, 2*np.pi, 2000)

    S_f = np.zeros_like(t)

    # Calcul des termes de la série de Fourier

    # . Rang désiré (rang >= 1)
    rang = 1

    # . Calcul des coefficents :
    #   * les 'bn' sont nuls car fonction paire

    # .. Calcul de 'a0'
    S_f = 1/2

    # .. Calcul de la somme 'a1', 'a3', 'a5', ...
    #    Forme non simplifiée :
    for n in range(1, rang+1) :
        an = (2/(n * np.pi)) * np.sin(n*np.pi/2)
        S_f +=  an * np.cos(n * t)

    # Construction des courbes
    fig, ax = plt.subplots(layout="constrained")

    # . Tracé du signal carré
    ax.plot(t, f(t), color="gray", linestyle="--")

    # . Tracé de la série de Fourier
    ax.plot(t, S_f, color="blue", linestyle="-")

    # . Titre de la figure
    fig.suptitle("Série de Fourier d'un signal carré")

    # . Légende de la figure
    plt.ylim(-0.5, 1.5) # On fixe les limites de l'axe des ordonnées pour permettre d'afficher la légende
    ax.legend(['$f(t)$ : signal carré', '$S_f\\;(t)$ : approximation par série de Fourier'], loc='lower right')

    # . Configuration de la grille de la courbe :
    #   * styles des grilles principales et secondaires
    ax.grid(which='major', color='#CCCCCC', linestyle='-')
    ax.grid(which='minor', color='#CCCCCC', linestyle='--')
    #   * une graduation horizontale principale toutes les 1 unités
    ax.xaxis.set_major_locator(tck.MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter(tck.FuncFormatter(
        lambda val,pos: '{:.0g}$\\pi$'.format(val/np.pi) if val !=0 else '0'
    ))
    #   * une graduation horizontale secondaire toutes les 0.2 unités
    ax.xaxis.set_minor_locator(tck.MultipleLocator(np.pi/2))
    #   * une graduation verticale principale toutes les 1 unités
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    #   * une graduation verticale secondaire toutes les 0.5 unités
    ax.yaxis.set_minor_locator(tck.MultipleLocator(0.5))

    # . Tracé des axes
    plt.axhline()
    plt.axvline()

    # . Affichage de la figure
    plt.show()