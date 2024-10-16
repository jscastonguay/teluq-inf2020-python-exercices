from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame import Color


MARGE = 50
LARGEUR_BORDURE = 5
NB_DE_VOIES = 3
DISTANCE_ENTRE_LIGNES = 100
LONGUEUR_LIGNES = 50

class Ligne:
    
    def __init__(self, pos_x: int, pos_y: int, longeur_ligne: int) -> None:
        
        # TODO enlever les 'self' si pas nécessaire
        self.longeur_ligne: int = longeur_ligne
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        
        self.point_gauche: list[int, int] = [pos_x, self.pos_y]
        self.point_droite: list[int, int] = [pos_x + self.longeur_ligne, self.pos_y]
        
    def dessine(self, fenetre: Surface):
        draw.line(fenetre, Color('white'), self.point_gauche, self.point_droite, LARGEUR_BORDURE)
        
    def bouge(self, vitesse: int) -> bool:
        '''Retourne true si la ligne doit être détruite.
        '''
        self.point_gauche[0] = self.point_gauche[0] - vitesse
        self.point_droite[0] = self.point_droite[0] - vitesse
        return self.point_gauche[0] < 0 and self.point_droite[0] < 0


class Voie:
    
    def __init__(self, dimension_piste: Rect, no: int, ligne_haut: bool = False, ligne_bas: bool = False) -> None:
        assert no >= 0 and no < NB_DE_VOIES
        
        self.lignes_haut: list[Ligne] = [] if ligne_haut else None
        self.lignes_bas: list[Ligne] = [] if ligne_bas else None
        hauteur: int = dimension_piste.height / 3
        self.rect: Rect = Rect((dimension_piste.topleft[0], dimension_piste.topleft[1] + no * hauteur), (dimension_piste.width, hauteur))
        self._construit_lignes()
        
        
    def _construit_lignes(self) -> None:
        # Créer des lignes jusqu'à ce qu'il a ait une à l'extérieur 
        # de la fenêtre.
        # Attention, la vitesse peut poser problème si elle est plus grande
        # que la longueur d'une ligne plus la distance entre les lignes.
        if self.lignes_haut != None:
            if len(self.lignes_haut) == 0:
                self.lignes_haut.append(Ligne(0, self.rect.top, LONGUEUR_LIGNES))
            while self.lignes_haut[-1].point_droite[0] <= self.rect.right:
                self.lignes_haut.append(Ligne(self.lignes_haut[-1].point_droite[0] + DISTANCE_ENTRE_LIGNES, self.rect.top, LONGUEUR_LIGNES))
                
        # TODO Utiliser des exceptions ici au lieu du test avec le 'if self.lignes_haut != None' ???
                
        if self.lignes_bas != None:
            if len(self.lignes_bas) == 0:
                self.lignes_bas.append(Ligne(0, self.rect.bottom, LONGUEUR_LIGNES))
            while self.lignes_bas[-1].point_droite[0] <= self.rect.right:
                self.lignes_bas.append(Ligne(self.lignes_bas[-1].point_droite[0] + DISTANCE_ENTRE_LIGNES, self.rect.bottom, LONGUEUR_LIGNES))
                
                    
    def _dessine_lignes(self, fenetre: Surface) -> None:
        if self.lignes_haut:
            for ligne in self.lignes_haut:
                ligne.dessine(fenetre)
        if self.lignes_bas:
            for ligne in self.lignes_bas:
                ligne.dessine(fenetre)
                
    def _bouge_lignes(self, vitesse):
        
        # TODO possibilité de programmation fonctionnelle avec filter
        # TODO possibilité d'utiliser des exceptions au lieu du 'if self.lignes_haut'
        
        if self.lignes_haut:
            for ligne in self.lignes_haut:
                a_enlever = ligne.bouge(vitesse)
                if a_enlever:
                    self.lignes_haut.remove(ligne)
        if self.lignes_bas:
            for ligne in self.lignes_bas:
                a_enlever = ligne.bouge(vitesse)
                if a_enlever:
                    self.lignes_bas.remove(ligne)
        
    def dessine(self, fenetre: Surface, vitesse: int) -> None:
        draw.rect(fenetre, Color('gray'), self.rect)
        self._bouge_lignes(vitesse)
        self._construit_lignes()
        self._dessine_lignes(fenetre)
        
        

class Piste:
    
    def __init__(self, largeur: int, hauteur: int) -> None:
        self.vitesse: int = 0
        self.rect: Rect = Rect((0, MARGE), (largeur,hauteur-2*MARGE))
        
        
        # TODO Possibilité de programmation fonctionnelle ???
        self.voies: list[Voie] = []
        for i in range(NB_DE_VOIES):
            self.voies.append(Voie(self.rect, i, ligne_haut = (i != 0)))
    
    def _dessine_bordure(self, fenetre: Surface) -> None:
        draw.line(fenetre, Color('white'), self.rect.topleft, self.rect.topright, LARGEUR_BORDURE)
        draw.line(fenetre, Color('white'), self.rect.bottomleft, self.rect.bottomright, LARGEUR_BORDURE)
        
    def get_nb_voies(self) -> int:
        return NB_DE_VOIES
    
    def get_voie(self, no_voie: int) -> Voie:
        index = max(no_voie, 0)
        index = min(index, NB_DE_VOIES - 1)
        return self.voies[index]
        
    def dessine(self, fenetre: Surface, vitesse: int) -> None:
        
        # Programmation fonctionnelle avec une lambda ???
        for i in range(NB_DE_VOIES):
            self.voies[i].dessine(fenetre, vitesse)
        
        self._dessine_bordure(fenetre)
