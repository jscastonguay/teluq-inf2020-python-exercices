from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame import Color
import pygame
import random
import functools
from abc import ABC, abstractmethod

from piste import *


class Vehicule(ABC):
    """Classe abstraite définissant un véhicule sur la piste.
    """

    def __init__(
        self, vitesse: int, rect: Rect, voie: Voie) -> None:
        """Constructeur de Vehicule.

        Args:
            vitesse (int): La vitesse initiale du véhicule.
            
            rect (Rect): Un rectangle définissant les dimensions totales du
            véhicules. La position initiale en x est définie par rect mais la
            position initiale en y est définie par la voie.
            
            voie (Voie): La voie sur la piste sur laquelle le véhicule est
            localisée. La position initiale en y est définie par la voie.
        """
        self.vitesse: int = vitesse
        self.rect: Rect = rect
        self.voie: Voie = voie
        
        self.rect.centery = voie.rect.centery

        self.couleur_corp = self._get_courleur_aleatoire()
        self.couleur_habitacle = self._get_courleur_aleatoire()
        self.couleur_ailerons = self._get_courleur_aleatoire()

    def _get_courleur_aleatoire(self) -> Color:
        """Cette méthode retourne une couleur aléatoire dans une liste de
        couleur prédéfinie.

        Returns:
            Color: La couleur sélectionnée de façon aléatoire.
        """

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
            Color("magenta"),
        ]

        return random.choice(couleurs)

    def dessine(self, fenetre: Surface) -> None:
        """Cette méthode dessine le véhicule dans la fenêtre donnée.

        Args:
            fenetre (Surface): La fenêtre dans laquelle la voiture sera
            dessinée.
        """

        MARGE = 0.15
        LARGEUR_AILERONS = 0.1

        # Corp
        left = self.rect.left
        top = self.rect.top + self.rect.height * MARGE
        width = self.rect.width * (1 - 2 * MARGE)
        height = self.rect.height * (1 - 2 * MARGE)
        draw.rect(fenetre, self.couleur_corp, ((left, top), (width, height)))

        # Aileron avant
        left = self.rect.right - self.rect.width * LARGEUR_AILERONS
        top = self.rect.top
        width = self.rect.width * LARGEUR_AILERONS
        height = self.rect.height
        draw.rect(fenetre, self.couleur_ailerons, ((left, top), (width, height)))

        # Habitacle
        left = self.rect.left
        top = self.rect.top + self.rect.height * 2 * MARGE
        width = self.rect.width * (1 - 2 * MARGE)
        height = self.rect.height * (1 - 4 * MARGE)
        draw.rect(fenetre, self.couleur_habitacle, ((left, top), (width, height)))

        point1 = (left + width, top)
        point2 = (left + width, top + height)
        point3 = (self.rect.midright[0], self.rect.midright[1])
        pygame.draw.polygon(fenetre, self.couleur_habitacle, [point1, point2, point3])

        left = self.rect.left + self.rect.width * 0.2
        # top = même que précédent
        width = self.rect.width * 0.15
        # height = même que précédent
        draw.rect(fenetre, Color("black"), ((left, top), (width, height)))

        # Aileron arrière
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width * LARGEUR_AILERONS
        height = self.rect.height
        draw.rect(fenetre, self.couleur_ailerons, ((left, top), (width, height)))

        # Roues
        left = self.rect.left + self.rect.width * MARGE
        top = self.rect.top
        width = self.rect.width * MARGE
        height = self.rect.height * MARGE
        draw.rect(fenetre, Color("black"), ((left, top), (width, height)))

        left = left + 2 * self.rect.width * MARGE
        draw.rect(fenetre, Color("black"), ((left, top), (width, height)))

        top = top + self.rect.height * (1 - MARGE)
        draw.rect(fenetre, Color("black"), ((left, top), (width, height)))

        left = left - 2 * self.rect.width * MARGE
        draw.rect(fenetre, Color("black"), ((left, top), (width, height)))

    @abstractmethod
    def bouge(self, vitesse_joueur: int, voie: Voie = None):
        """Déplace le véhicule dans la voie donnée.
        
        Args:
            vitesse_joueur (int): La vitesse du véhicule du joueur.
            
            voie (Voie, optional): La voie dans laquelle le véhicule doit se
            trouver. Si la voie courante est différente, il y aura changement
            de voie. Défaut est None.
        """

    def est_chevauche(self, autre_vehicule: "Vehicule") -> bool:
        """Évalue s'il y a collision entre l'instance et un autre véhicule.

        Args:
            autre_vehicule (Vehicule): Autre véhicule.

        Returns:
            bool: True s'il y a ue collision.
        """
        chevauche: bool = False
        if autre_vehicule != self:
            chevauche = self.rect.colliderect(autre_vehicule)
        return chevauche

    def est_chevauche_liste(self, liste_vehicules: list["Vehicule"]) -> bool:
        """Évalue s'il y a collision entre l'instance et une liste d'autres
        véhicules.

        Args:
            liste_vehicules (list[Vehicule]): Liste de véhicule à évaluer.

        Returns:
            bool: True s'il y a une collision en l'instance et l'une des voitures.
        """
        try:
            return functools.reduce(
                lambda x, y: x or y,
                map(lambda x: self.est_chevauche(x), liste_vehicules),
            )
        except TypeError:
            return False


class Joueur(Vehicule):
    """Classe définissant le véhicule du joueur.
    """

    def __init__(
        self, vitesse: int, rect: Rect, voie: Voie = None) -> None:
        super().__init__(vitesse, rect, voie)

    def bouge(self, vitesse_joueur: int, voie: Voie = None):
        """Déplace le véhicule dans la voie donnée.
        
        Le véhicule ne se déplace pas en x puisque tous les déplacements se
        font dans la perspective du joueur. Lors d'un changement de voie, le
        véhicule se déplace en y à la même vitesse qu'il devrait se déplacer
        en x.

        Args:
            vitesse_joueur (int): La vitesse du véhicule du joueur.
            
            voie (Voie, optional): La voie dans laquelle le véhicule doit se
            trouver. Si la voie courante est différente, il y aura changement
            de voie. Défaut à None.
        """
        vitesse_y: int = 0

        if voie:
            self.voie = voie
        if self.voie:
            vitesse_y = self.voie.rect.centery - self.rect.centery
            vitesse_y = min(vitesse_y, vitesse_joueur)
            vitesse_y = max(vitesse_y, -vitesse_joueur)

        self.rect = self.rect.move(0, vitesse_y)


class Competiteur(Vehicule):
    """Classe définissant un véhicule compétiteur.
    """

    def __init__(
        self, vitesse: int, rect: Rect, voie: Voie = None) -> None:
        super().__init__(vitesse, rect, voie)

    def bouge(self, vitesse_joueur: int, voie: Voie = None):
        """Déplace le véhicule dans la voie donnée.
        
        Le véhicule compétiteur se déplace en x selon la vitesse apparente
        entre sa vitesse et celle du véhicule du joueur.        
        
        Args:
            vitesse_joueur (int): La vitesse du véhicule du joueur.
            
            voie (Voie, optional): La voie dans laquelle le véhicule doit
            se trouver. N'a aucun effet. Défaut est None.
        """
        vitesse_x = self.vitesse - vitesse_joueur
        self.rect = self.rect.move(vitesse_x, 0)

    def ajuste_vitesse(self, autre_vehicule: "Vehicule"):
        """Ajuste la vitesse du véhicule en fonction d'un autre véhicule
        donnée.
        
        Si le véhicule donné se rapproche par l'avant dans une même voie et
        qu'il est à courte distance, la vitesse de l'instance de véhicule
        ralentit.

        Args:
            autre_vehicule (Vehicule): Autres véhicule.
        """
        if autre_vehicule != self:
            if autre_vehicule.voie == self.voie:
                if autre_vehicule.rect.left > self.rect.right:
                    if autre_vehicule.vitesse < self.vitesse:
                        if autre_vehicule.rect.left - self.rect.right < self.rect.width:
                            self.vitesse = self.vitesse - 1
