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
 Script     : Séries_Fourier.py
 Auteur     : Lysius
 Date       : 09/08/2024
 Description: illustre l’approximation d’une fonction créneau périodique (période 2𝜋) par sa série de Fourier, et compare la forme idéale au développement tronqué avec différents nombres de termes impairs.
=====================================================================================================================================================
"""
import numpy as np
import matplotlib.pyplot as plt

# Définir la fonction créneau (période 2π)
def square_wave(x):
    return np.where(np.sin(x) >= 0, 1, -1)

# Série de Fourier approximative
def fourier_series(x, n_terms):
    result = np.zeros_like(x)
    for n in range(1, n_terms + 1, 2):  # seulement les termes impairs
        result += (4 / (np.pi * n)) * np.sin(n * x)
    return result

# Domaine x
x = np.linspace(-np.pi, np.pi, 1000)

# Fonction originale
original = square_wave(x)

# Approximation avec différents nombres de termes
approximations = {
    1: fourier_series(x, 1),
    3: fourier_series(x, 3),
    5: fourier_series(x, 5),
    15: fourier_series(x, 15)
}

# Tracer les courbes
plt.figure(figsize=(12, 8))
plt.plot(x, original, label='Fonction créneau', linewidth=2, color='black')

for n, y in approximations.items():
    plt.plot(x, y, label=f'Série de Fourier (n={n})')

plt.title("Série de Fourier pour une fonction créneau")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.show()
