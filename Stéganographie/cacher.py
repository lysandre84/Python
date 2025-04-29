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
 Script     : cacher.py
 Auteur     : Lysius
 Date       : 29/04/2025
 Description: 
=====================================================================================================================================================
"""
from PIL import Image

png = Image.open("image.png")   # le nom du fichier de l'image
pixels = png.getdata()
larg, haut = png.size

texte = """




blablabla




"""


texte_bin = ""
for car in texte:
    texte_bin += str('{0:08b}'.format(ord(car)))
texte_bin += "111"  # pour etre sur que tut est bien chiffre

longueur = len(texte_bin)
index = 0
i = 0

# Dans le format png, un pixel peut Ãªtre composÃ© de 3 ou 4 valeurs.
nb_val = 3   # mettre eventuellement 4

for k in range(longueur//nb_val):
    if nb_val == 3:
        v=[pixels[k][0],pixels[k][1],pixels[k][2]]
    else:
        v=[pixels[k][0],pixels[k][1],pixels[k][2],pixels[k][3]]
    for j in range(nb_val):
        # Si la valeur du bit du texte ne correspond pas a la parite de l'image alors la modifer de 1
        if (v[j]%2==0 and int(texte_bin[i])==1) or (v[j]%2==1 and int(texte_bin[i])==0) :
            if v[j]>=255:
                v[j] -= 1
            else :
                v[j] += 1
        i += 1
    col = index % larg
    row = index // larg
    png.putpixel((col,row), tuple(v))
    index += 1

png.save('stegano.png')

print("Nouvelle image : stegano.png")