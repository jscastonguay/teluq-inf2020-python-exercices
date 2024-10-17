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
    
    
class LignePointillee:
    
    def __init__(self, pos_x_limite: int = 0, pos_y: int = 0) -> None:
        self.pos_x_limite = pos_x_limite
        self.pos_y: int = pos_y
        self.lignes: list[Ligne] = []
        self.construit()
        
    def construit(self) -> None:
        # Créer des lignes de la position 0 jusqu'à ce qu'il a ait une à l'extérieur 
        # du rectangle.
        # Attention, la vitesse peut poser problème si elle est plus grande
        # que la longueur d'une ligne plus la distance entre les lignes.
        if len(self.lignes) == 0:
            self.lignes.append(Ligne(0, self.pos_y, LONGUEUR_LIGNES))
        while self.lignes[-1].point_droite[0] <= self.pos_x_limite:
            self.lignes.append(Ligne(self.lignes[-1].point_droite[0] + DISTANCE_ENTRE_LIGNES, self.pos_y, LONGUEUR_LIGNES))
                
    def dessine(self, fenetre: Surface) -> None:
        for ligne in self.lignes:
            ligne.dessine(fenetre)
                
    
    def bouge(self, vitesse):
        
        # TODO possibilité de programmation fonctionnelle avec filter
        # TODO possibilité d'utiliser des exceptions au lieu du 'if self.lignes_haut'
        for ligne in self.lignes:
            a_enlever = ligne.bouge(vitesse)
            if a_enlever:
                self.lignes.remove(ligne)

class Voie:
    
    def __init__(self, dimension_piste: Rect, no: int, lignes_haut: bool = False, lignes_bas: bool = False) -> None:
        assert no >= 0 and no < NB_DE_VOIES
        
        hauteur: int = dimension_piste.height / NB_DE_VOIES
        
        self.rect: Rect = Rect((dimension_piste.topleft[0], dimension_piste.topleft[1] + no * hauteur), (dimension_piste.width, hauteur))
        self.ligne_pointillee: list[LignePointillee] = []
        if lignes_haut:
            self.ligne_pointillee.append(LignePointillee(self.rect.right, self.rect.top))
        if lignes_bas:
            self.ligne_pointillee.append(LignePointillee(self.rect.right, self.rect.top))
                
    def dessine(self, fenetre: Surface, vitesse: int) -> None:
        draw.rect(fenetre, Color('gray'), self.rect)        
        for ligne in self.ligne_pointillee:
            ligne.bouge(vitesse)
            ligne.construit()
            ligne.dessine(fenetre)


class Piste:
    
    def __init__(self, largeur: int, hauteur: int) -> None:
        self.vitesse: int = 0
        self.rect: Rect = Rect((0, MARGE), (largeur,hauteur-2*MARGE))
        
        
        # TODO Possibilité de programmation fonctionnelle ???
        self.voies: list[Voie] = []
        for i in range(NB_DE_VOIES):
            self.voies.append(Voie(self.rect, i, lignes_haut = (i != 0)))
    
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
