# -*- coding: utf-8 -*-
"""
TBD
"""

import pygame
from pygame import Color

from piste import Piste

def main():
    pygame.init()
    
    LARGEUR_FENETRE = 1200
    HAUTEUR_FENETRE = 800
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption('Grand prix formule 1 x 10^6')

    
    piste = Piste(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    horloge = pygame.time.Clock()
    
    vitesse: int = 0
    
    fin = False
    while not fin:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            fin = True 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vitesse = vitesse - 1
                vitesse = max(0, vitesse)
            if event.key == pygame.K_RIGHT:
                vitesse = vitesse + 1
                vitesse = min(vitesse, 20)
        else:
        
            fenetre.fill(Color('black'))
            piste.dessine(fenetre, vitesse)
            pygame.display.flip()
            horloge.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()