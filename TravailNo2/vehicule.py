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

    def bouge(self, vitesse_pilote: int, voie: Voie = None):
        
        vitesse_x: int = 0
        vitesse_y: int = 0
        
        if not self.vehicule_joueur:
            vitesse_x = self.vitesse - vitesse_pilote
        
        # Position y
        if voie:
            self.voie = voie
        if self.voie:
            vitesse_y: int = self.voie.rect.centery - self.rect.centery
            vitesse_y = min(vitesse_y, vitesse_pilote)
            vitesse_y = max(vitesse_y, -vitesse_pilote)

        self.rect = self.rect.move(vitesse_x, vitesse_y)
        
    # Noter dans le rapport la façon d'annoter une classe dans elle même.
    def ajuste_vitesse(self, autre_vehicule: 'Vehicule'):
        if autre_vehicule != self:
            if autre_vehicule.voie == self.voie:
                if autre_vehicule.rect.left > self.rect.right:
                    if autre_vehicule.vitesse < self.vitesse:
                        if autre_vehicule.rect.left - self.rect.right < self.rect.width:
                            self.vitesse = self.vitesse - 1

    def est_chevauche(self, autre_vehicule: 'Vehicule') -> bool:
        chevauche: bool = False
        if autre_vehicule != self:
            chevauche = self.rect.colliderect(autre_vehicule)
        return chevauche
    
    def est_chevauche_liste(self, liste_vehicules: list['Vehicule']) -> bool:
        chevauche: bool = False
        for vehicule in liste_vehicules:
            if self.est_chevauche(vehicule):
                chevauche = True
        return chevauche


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