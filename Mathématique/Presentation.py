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
 Script     : presentation.py
 Auteur     : Lysius
 Date       : 11/02/2024
 Description: 
=====================================================================================================================================================
"""
import pygame
import sys

# Couleurs
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Texte des slides
slides = [
    "Bienvenue au BTS CIEL (Cloud, Infrastructures, Ecosystèmes Numériques)\n"
    "au Lycée Alphonse Benoît.\n\n"
    "Formation :\n- 2 ans pour devenir expert en IT\n- Équipe pédagogique expérimentée\n- Laboratoires modernes\n",

    "Options proposées :\n\n"
    "1. Option IR (Infrastructures et Réseaux)\n"
    "- Gestion des réseaux\n- Cybersécurité\n- Maintenance informatique\n\n"
    "2. Option ER (Écosystèmes Numériques)\n"
    "- Développement d'applications\n- Gestion de projets numériques",

    "Débouchés professionnels :\n\n"
    "- Administrateur réseaux\n"
    "- Consultant IT\n"
    "- Développeur cloud\n"
    "- Responsable cybersécurité\n\n"
    "Poursuite d'études :\nLicence pro, école d'ingénieurs...",

    "Pourquoi le BTS CIEL au Lycée Alphonse Benoît ?\n\n"
    "- Environnement propice à l'innovation\n"
    "- Suivi personnalisé\n"
    "- Stages en entreprise pour une expérience concrète\n",

    "Le secteur IT :\n\n"
    "- Croissance continue\n"
    "- Demande forte pour des experts IT\n"
    "- Opportunités en France et à l'international\n",

    "Merci pour votre attention !\n\n"
    "Pour plus d'informations :\n"
    "Lycée Alphonse Benoît\n"
    "Contact : [À compléter]"
]

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Terminal - Présentation BTS CIEL")

# Police
font = pygame.font.Font(pygame.font.match_font("consolas"), 24)  # Style console

# Gestion du découpage des lignes
def wrap_text_with_prompt(prompt, text, font, max_width, prompt_width):
    """Découpe le texte pour qu'il respecte la largeur de la fenêtre tout en incluant le prompt."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        line_text = f"{prompt} {' '.join(current_line)}"
        if font.size(line_text)[0] > max_width:
            current_line.pop()
            lines.append(f"{prompt} {' '.join(current_line)}")
            current_line = [word]
    lines.append(f"{prompt} {' '.join(current_line)}")
    return lines

def render_slide(prompt, text):
    """Affiche le contenu d'un slide avec un prompt."""
    screen.fill(BLACK)
    max_width = width - 50  # Espace pour le texte
    prompt_width = font.size(prompt)[0]
    x, y = 50, 50
    lines = wrap_text_with_prompt(prompt, text, font, max_width, prompt_width)
    for line in lines:
        text_surface = font.render(line, True, GREEN)
        screen.blit(text_surface, (x, y))
        y += font.size(line)[1]
    button_rect = draw_button()
    pygame.display.flip()
    return button_rect

def draw_button():
    """Dessine un bouton en bas à droite."""
    button_text = "$"
    button_surface = font.render(button_text, True, BLACK, GREEN)
    button_rect = button_surface.get_rect(center=(width - 50, height - 50))
    screen.blit(button_surface, button_rect)
    return button_rect

def presentation():
    """Permet de naviguer entre les slides."""
    current_slide = 0
    prompt = "Maprésentation@AlphonseBenoit#"
    while current_slide < len(slides):
        button_rect = render_slide(prompt, slides[current_slide])
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        current_slide += 1
                        waiting = False

# Boucle principale
def main():
    try:
        presentation()
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
