from pygame import Rect
from pygame import Surface

class Auto:
    def __init__(self, pos_initiale: tuple[float,float], grosseur_initiale: tuple[float,float]) -> None:
        r: Rect = Rect(pos_initiale, grosseur_initiale)
        pass
    
    def dessine(fenetre: Surface):
        