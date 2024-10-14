# -*- coding: utf-8 -*-
"""
TBD
"""

import pygame
from pygame import Color

from piste import Piste
from vehicules import *

def main():
    pygame.init()
    
    LARGEUR_FENETRE = 1200
    HAUTEUR_FENETRE = 800
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption('Grand prix formule 1 x 10^6')

    
    piste = Piste(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    horloge = pygame.time.Clock()
    
    vitesse: int = 0
    voie_joueur = 1
    
    
    # TODO récupérer la voie autrement que par l'Accès direct: piste.voies[voie_pilote]
    
    mon_vehicule = Vehicule(0, Rect((0, 0), (200, 100)), piste.voies[voie_joueur], vehicule_joueur=True)
    
    
    
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
            if event.key == pygame.K_UP:
                
                
                #TODO Doit gèrer l'Accès aux voies par la piste
                voie_joueur = max(voie_joueur - 1, 0)
                
            if event.key == pygame.K_DOWN:
                
                #TODO Doit gèrer le nombre max de voie différemment, idem pour l'Accès aux voies
                voie_joueur = min(voie_joueur + 1, 2)
        else:
        
            fenetre.fill(Color('black'))
            
            piste.dessine(fenetre, vitesse)
            mon_vehicule.bouge(vitesse, piste.voies[voie_joueur])
            mon_vehicule.dessine(fenetre)
            
            pygame.display.flip()
            horloge.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()