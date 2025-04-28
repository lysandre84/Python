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
 Script     : Fractal_Régression_FFT_Dérivé_Intégrale.py
 Auteur     : Lysius
 Date       : 28/11/2024
 Description: Mélange deux volets très différents : un exemple de régression logistique en machine learning et la définition d’une fonction de calcul de la fractale de Mandelbrot.
=====================================================================================================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy import signal
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Machine Learning Mathématique : Régression Logistique
X, y = make_classification(n_samples=200, n_features=2, n_redundant=0, n_clusters_per_class=1, random_state=0)
model = LogisticRegression()
model.fit(X, y)
y_pred = model.predict(X)
print("Précision du modèle :", classification_report(y, y_pred))

# 2. Maths appliquées et visuelles : Fractale de Mandelbrot
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return np.array([[mandelbrot(complex(r, i), max_iter) for r in r1] for i in r2])

mandelbrot_img = mandelbrot_set(-2.0, 1.0, -1.5, 1.5, 300, 300, 50)
plt.figure(figsize=(6, 6))
plt.imshow(mandelbrot_img, extent=(-2, 1, -1.5, 1.5), cmap='inferno')
plt.title("Fractale de Mandelbrot")
plt.xlabel("Re")
plt.ylabel("Im")
plt.colorbar(label="Itérations avant divergence")
plt.show()

# 3. Transformées et Signaux : FFT
t = np.linspace(0, 1, 500, endpoint=False)
signal_data = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*20*t)
fft_data = np.fft.fft(signal_data)
freqs = np.fft.fftfreq(len(t), d=t[1] - t[0])
plt.figure(figsize=(10, 4))
plt.plot(freqs[:250], np.abs(fft_data)[:250])
plt.title("Transformée de Fourier d’un signal composé")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# 4. Analyse Mathématique : Dérivée et Intégrale
x = sp.symbols('x')
f = sp.sin(x) * sp.exp(-x)
f_prime = sp.diff(f, x)
f_integral = sp.integrate(f, x)

f_lambd = sp.lambdify(x, f, modules=["numpy"])
f_prime_lambd = sp.lambdify(x, f_prime, modules=["numpy"])
f_integral_lambd = sp.lambdify(x, f_integral, modules=["numpy"])

x_vals = np.linspace(0, 10, 500)
plt.figure(figsize=(12, 6))
plt.plot(x_vals, f_lambd(x_vals), label='f(x)', linewidth=2)
plt.plot(x_vals, f_prime_lambd(x_vals), label="f'(x)", linestyle='--')
plt.plot(x_vals, f_integral_lambd(x_vals), label="∫f(x)dx", linestyle=':')
plt.title("f(x), sa dérivée et son intégrale")
plt.legend()
plt.grid(True)
plt.show()
