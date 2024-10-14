# -*- coding: utf-8 -*-
"""
TBD
"""

import pygame
from pygame import Color
import random
import time

from piste import Piste
from vehicule import *

LARGEUR_FENETRE = 1600
HAUTEUR_FENETRE = 800
VITESSE_MAX = 20
LONGUEUR_VEHICULE = 200
LARGEUR_VEHICULE = 100


competiteurs: list[Vehicule] = []


def creer_competiteur(piste: Piste, vitesse_courante: int) -> Vehicule:
    no_voie = random.randrange(0, piste.get_nb_voies())
    vitesse_vehicule: int = random.randrange(7, VITESSE_MAX)
    vitesse_apparante: int = vitesse_vehicule - vitesse_courante
    nouveau: Vehicule = None
    if vitesse_apparante > 0:
        nouveau = Vehicule(vitesse_vehicule, Rect((-LONGUEUR_VEHICULE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)), piste.get_voie(no_voie))
    elif vitesse_apparante < 0:
        nouveau = Vehicule(vitesse_vehicule, Rect((LARGEUR_FENETRE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)), piste.get_voie(no_voie))
    return nouveau


def nettoie_competiteurs(competiteurs: list[Vehicule]):
    for competiteur in competiteurs:
        if competiteur.rect.left < 0 and competiteur.rect.right < 0:
            competiteurs.remove(competiteur)
        if competiteur.rect.left > LARGEUR_FENETRE and competiteur.rect.right > LARGEUR_FENETRE:
            competiteurs.remove(competiteur)
            

def main():
    
    random.seed()
    
    pygame.init()
    pygame.font.init()
    
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption('Grand prix formule 1 x 10^6')

    
    piste = Piste(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    horloge = pygame.time.Clock()
    
    vitesse: int = 0
    voie_joueur = 1
    
    
    # TODO récupérer la voie autrement que par l'Accès direct: piste.voies[voie_pilote]
    
    mon_vehicule = Vehicule(0, Rect((0.2 * LARGEUR_FENETRE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)), piste.get_voie(voie_joueur), vehicule_joueur=True)
    
    
    compteur: int = int(time.perf_counter()) + 5
    game_over: bool = False
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
                vitesse = min(vitesse, VITESSE_MAX)
            if event.key == pygame.K_UP:
                
                
                #TODO Doit gèrer l'Accès aux voies par la piste
                voie_joueur = max(voie_joueur - 1, 0)
                
            if event.key == pygame.K_DOWN:
                
                #TODO Doit gèrer le nombre max de voie différemment, idem pour l'Accès aux voies
                voie_joueur = min(voie_joueur + 1, piste.get_nb_voies() - 1)
        else:
            
            if not game_over:
        
                fenetre.fill(Color('black'))
                
                piste.dessine(fenetre, vitesse)
                
                mon_vehicule.bouge(vitesse, piste.get_voie(voie_joueur))
                mon_vehicule.dessine(fenetre)
                
                nettoie_competiteurs(competiteurs)
                for competiteur1 in competiteurs:
                    for competiteur2 in competiteurs:
                        competiteur1.ajuste_vitesse(competiteur2)
                
                if time.perf_counter() > compteur:
                    compteur = time.perf_counter() + 2
                    vehicule = creer_competiteur(piste, vitesse)
                    if vehicule:
                        if not vehicule.est_chevauche_liste(competiteurs):
                            competiteurs.append(vehicule)
                    
                for competiteur in competiteurs:
                    competiteur.bouge(vitesse)
                    competiteur.dessine(fenetre)
                    
                if mon_vehicule.est_chevauche_liste(competiteurs):
                    game_over = True
                    
            else:
                
                # Game over
                my_font = pygame.font.SysFont('Comic Sans MS', 200)
                text_surface = my_font.render('Game over', False, Color('red'))
                textRect = text_surface.get_rect()
                textRect.center = (LARGEUR_FENETRE / 2, HAUTEUR_FENETRE / 2)
                fenetre.blit(text_surface, textRect)
            
            pygame.display.flip()
            horloge.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()