#!/usr/bin/env python3
"""
=====================================================================================================================================================

             /$$                                                                                              /$$       /$$          
            | $$                                                                                             | $$      |__/          
  /$$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$ | $$$$$$$  /$$  /$$$$$$ 
 /$$_____/|_  $$_/   /$$__  $$ /$$__  $$ |____  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$|____  $$ /$$__  $$| $$__  $$| $$ /$$__  $$
|  $$$$$$   | $$    | $$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \__/ /$$$$$$$| $$  \ $$| $$  \ $$| $$| $$$$$$$$
 \____  $$  | $$ /$$| $$_____/| $$  | $$ /$$__  $$| $$  | $$| $$  | $$| $$  | $$| $$      /$$__  $$| $$  | $$| $$  | $$| $$| $$_____/
 /$$$$$$$/  |  $$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/| $$  | $$| $$|  $$$$$$$
|_______/    \___/   \_______/ \____  $$ \_______/|__/  |__/ \______/  \____  $$|__/      \_______/| $$____/ |__/  |__/|__/ \_______/
                               /$$  \ $$                               /$$  \ $$                   | $$                              
                              |  $$$$$$/                              |  $$$$$$/                   | $$                              
                               \______/                                \______/                    |__/                              
           
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : montrer.py
 Auteur     : Lysius
 Date       : 29/04/2025
 Description: 
=====================================================================================================================================================
"""
from PIL import Image

# fonction qui convertit un entier binaire en decimal
def bin2dec(binaire) :
    longueur=len(binaire)
    res=0
    for i in range(longueur):
       res += int(binaire[i])*2**(longueur-i-1)
    return res

# ouvrir l'image et recuperer les pixels
png = Image.open("photo_2024-04-08_23-15-59.jpg")
pixels = png.getdata()

# Dans le format png, un pixel peut Ãªtre composÃ© de 3 ou 4 valeurs.
nb_val = 3   # mettre eventuellement 4

liste_bits = [0]*(len(pixels)*nb_val)
i = 0  #compteur du nombre de bits

# Pour tous les pixels reconstruire la chaine de bits en fonction de la parite des valeurs des pixels
for rgb in pixels :
    liste_bits[i]=rgb[0]%2
    i += 1
    liste_bits[i]=rgb[1]%2
    i += 1
    liste_bits[i]=rgb[2]%2
    i += 1
    if nb_val == 4:
        liste_bits[i]=rgb[3]%2
        i += 1

# Calcul du nombre de caracteres sur 8 bits
nb_car = len(liste_bits)//8

# texte devoile
for i in range(nb_car-1) :
    # Ecriture du texte caractere par caractere par plages de 8 bits
    print(chr(bin2dec(liste_bits[8*i:8*(i+1)])), end="")