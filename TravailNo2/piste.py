from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame import Color


MARGE = 50
LARGEUR_BORDURE = 5
NB_DE_VOIES = 3

class Ligne:
    
    def __init__(self, pos_y: int) -> None:
        self.LONGEUR_LIGNE: int = 50
        self.pos_y: int = pos_y
        self.point1: tuple[int, int] = (200, self.pos_y)
        self.point2: tuple[int, int] = (200 + self.LONGEUR_LIGNE, self.pos_y)
        
    def dessine(self, fenetre: Surface):
        draw.line(fenetre, Color('white'), self.point1, self.point2, LARGEUR_BORDURE)


class Voie:
    
    def __init__(self, dimension_piste: Rect, no: int, ligne_haut: bool = False, ligne_bas: bool = False) -> None:
        assert no >= 0 and no < NB_DE_VOIES
        
        self.ligne_haut: list[tuple[int ,int]] = [] if ligne_haut else None
        self.ligne_bas: list[tuple[int ,int]] = [] if ligne_bas else None
        hauteur: int = dimension_piste.height / 3
        self.rect: Rect = Rect((dimension_piste.topleft[0], dimension_piste.topleft[1] + no * hauteur), (dimension_piste.width, hauteur))
        
    def dessine(self, fenetre: Surface):
        draw.rect(fenetre, Color('gray'), self.rect)
        if self.ligne_haut != None:
            ligne = Ligne(self.rect.top)
            ligne.dessine(fenetre)
        if self.ligne_bas != None:
            ligne = Ligne(self.rect.bottom)
            ligne.dessine(fenetre)
        

class Piste:
    
    def __init__(self, largeur: int, hauteur: int) -> None:
        self.vitesse: int = 0
        self.rect: Rect = Rect((0, MARGE), (largeur,hauteur-2*MARGE))
    
    def _dessine_bordure(self, fenetre: Surface):
        draw.line(fenetre, Color('white'), self.rect.topleft, self.rect.topright, LARGEUR_BORDURE)
        draw.line(fenetre, Color('white'), self.rect.bottomleft, self.rect.bottomright, LARGEUR_BORDURE)
        
    def dessine(self, fenetre: Surface) -> None:
        self._dessine_bordure(fenetre)
        voie = Voie(self.rect, 1, ligne_haut=True)
        voie.dessine(fenetre)
