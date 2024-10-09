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
    
    fin = False
    while not fin:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            fin = True 
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        
        piste.dessine(fenetre)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()