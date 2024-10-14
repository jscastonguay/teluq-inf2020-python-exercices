from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame import Color
import pygame
import random
from piste import *


class Vehicule:
    
    def __init__(self, vitesse: int, rect: Rect, voie: Voie = None, vehicule_joueur: bool = False) -> None:

        self.vitesse: int = vitesse
        self.rect: Rect = rect
        self.voie: Voie = voie
        self.vehicule_joueur: bool = vehicule_joueur
        
        if voie:
            self.rect.centerx = voie.rect.centerx
            self.rect.centery = voie.rect.centery
        
        self.couleur_corp = self._get_courleur_aleatoire()
        self.couleur_habitacle = self._get_courleur_aleatoire()
        self.couleur_ailerons = self._get_courleur_aleatoire()
        
    def _get_courleur_aleatoire(self):
        
        couleurs = [
            Color("red"),
            Color("green"),
            Color("blue"),
            Color("yellow"),
            Color("white"),
            Color("orange"),
            Color("purple"),
            Color("pink"),
            Color("brown"),
            Color("cyan"),
            Color("magenta")
        ]
        
        return random.choice(couleurs)
        
    def dessine(self, fenetre: Surface):
        
        #draw.rect(fenetre, Color('white'), ((0, 0),(self.rect.width,self.rect.height)))
        
        MARGE = 0.15
        LARGEUR_AILERONS = 0.1
        
        # Corp
        left = self.rect.left
        top = self.rect.top + self.rect.height * MARGE
        width = self.rect.width * (1 - 2 * MARGE)
        height = self.rect.height * (1 - 2 * MARGE)
        draw.rect(fenetre, self.couleur_corp, ((left, top),(width,height)))
        
        # Aileron avant
        left = self.rect.right - self.rect.width * LARGEUR_AILERONS
        top = self.rect.top
        width = self.rect.width * LARGEUR_AILERONS
        height = self.rect.height
        draw.rect(fenetre, self.couleur_ailerons, ((left, top),(width,height)))
        
        # Habitacle
        left = self.rect.left
        top = self.rect.top + self.rect.height * 2 *MARGE
        width = self.rect.width * (1 - 2 * MARGE)
        height = self.rect.height * (1 - 4 * MARGE)
        draw.rect(fenetre, self.couleur_habitacle, ((left, top),(width,height)))
                
        point1 = (left + width, top)
        point2 = (left + width, top + height)
        point3 = (self.rect.midright[0], self.rect.midright[1])
        pygame.draw.polygon(fenetre, self.couleur_habitacle, [point1, point2, point3])
        
        left = self.rect.left + self.rect.width * 0.2
        # top = même que précédent
        width = self.rect.width * 0.15
        # height = même que précédent
        draw.rect(fenetre, Color('black'), ((left, top),(width,height)))
        
        # Aileron arrière
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width * LARGEUR_AILERONS
        height = self.rect.height
        draw.rect(fenetre, self.couleur_ailerons, ((left, top),(width,height)))
        
        # Roues
        left = self.rect.left + self.rect.width * MARGE
        top = self.rect.top
        width = self.rect.width * MARGE
        height = self.rect.height * MARGE
        draw.rect(fenetre, Color('black'), ((left, top),(width,height)))
        
        left = left + 2 * self.rect.width * MARGE
        draw.rect(fenetre, Color('black'), ((left, top),(width,height)))
        
        top = top + self.rect.height * (1 - MARGE)
        draw.rect(fenetre, Color('black'), ((left, top),(width,height)))
        
        left = left - 2 * self.rect.width * MARGE
        draw.rect(fenetre, Color('black'), ((left, top),(width,height)))

    def bouge(self, vitesse: int, voie: Voie = None):
        
        vitesse_x: int = 0
        vitesse_y: int = 0
        
        if not self.vehicule_joueur:
            vitesse_x = vitesse
        
        self.voie = voie
        if self.voie:
            difference: int = self.voie.rect.centery - self.rect.centery
            difference = min(difference, vitesse)
            difference = max(difference, -vitesse)
            self.rect.centery = self.rect.centery + difference

        self.rect = self.rect.move(vitesse_x, vitesse_y)
    
    


# Test d'intégration
if __name__ == "__main__":
    pygame.init()
    LARGEUR_FENETRE = 1000
    HAUTEUR_FENETRE = 400
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption('Test de visualisation de la voiture')
    fin = False
    
    
    vehicule = Vehicule(0, Rect((0, 0), (200, 100)))
    
    horloge = pygame.time.Clock()
    
    while not fin:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            fin = True 
        else:
            fenetre.fill(Color('black'))        
            vehicule.dessine(fenetre)
            pygame.display.flip()
            
            vehicule.bouge(1)
            
            horloge.tick(60)
    
    pygame.quit()