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
    """Classe qui permet de dessiner et ensuite de bouger une ligne
    (ou segment) d'une line pointillée horizontale.
    """

    def __init__(self, pos_x: int, pos_y: int, longueur_ligne: int) -> None:
        """Constructeur d'une ligne horizontale.

        Args:
            pos_x (int): La position initiale en X de l'extrémité gauche.
            pos_y (int): La position initiale en y de l'extrémité gauche.
            longueur_ligne (int): La longueur de la ligne.
        """
        self.point_gauche: list[int, int] = [pos_x, pos_y]
        self.point_droite: list[int, int] = [pos_x + longueur_ligne, pos_y]

    def dessine(self, fenetre: Surface) -> None:
        """Dessine la ligne.

        Args:
            fenetre (Surface): La surface dans laquelle la ligne est dessinée.
        """
        try:
            draw.line(
                fenetre,
                Color("white"),
                self.point_gauche,
                self.point_droite,
                LARGEUR_BORDURE,
            )
        except TypeError as Err:
            print(
                f"Erreur durant le tracage d'une ligne dans la fonction {Ligne.dessine.__name__}: {Err}"
            )

    def bouge(self, vitesse: int) -> bool:
        """Bouge la ligne vers la gauche de façon horizontale.

        Args:
            vitesse (int): La vitesse à laquelle la ligne bouge.

        Returns:
            bool: True si la ligne est sortie de la surface de dessin.
        """
        self.point_gauche[0] = self.point_gauche[0] - vitesse
        self.point_droite[0] = self.point_droite[0] - vitesse
        return self.point_gauche[0] < 0 and self.point_droite[0] < 0


class LignePointillee:
    """Classe qui permet de dessiner et ensuite de bouger une ligne
    pointillée horizontalement."""

    def __init__(self, pos_x_limite: int = 0, pos_y: int = 0) -> None:
        """Constructeur de la ligne pointillée.

        Args:
            pos_x_limite (int, optional): La limite à droite de la ligne
            pointillée. Défaut à 0.
            pos_y (int, optional): La position de la ligne en y. Défaut à 0.
        """
        self.pos_x_limite = pos_x_limite
        self.pos_y: int = pos_y
        self.lignes: list[Ligne] = []
        self._construit()

    def _construit(self) -> None:
        """Construit la ligne pointillée.
        """
        if len(self.lignes) == 0:
            self.lignes.append(Ligne(0, self.pos_y, LONGUEUR_LIGNES))
        while self.lignes[-1].point_droite[0] <= self.pos_x_limite:
            self.lignes.append(
                Ligne(
                    self.lignes[-1].point_droite[0] + DISTANCE_ENTRE_LIGNES,
                    self.pos_y,
                    LONGUEUR_LIGNES,
                )
            )

    def dessine(self, fenetre: Surface) -> None:
        """Dessine la ligne pointillée.

        Args:
            fenetre (Surface): La surface dans laquelle la ligne est dessinée. 
        """
        self._construit()
        for ligne in self.lignes:
            ligne.dessine(fenetre)

    def bouge(self, vitesse):
        """Bouge la ligne pointillée vers la gauche de façon horizontale.

        Args:
            vitesse (_type_): La vitesse à laquelle la ligne bouge.
        """
        for ligne in self.lignes:
            a_enlever = ligne.bouge(vitesse)
            if a_enlever:
                self.lignes.remove(ligne)


class Voie:
    """Classe dessinant une voie ayant une de façon optionnelle une ligne
    pointillée sur le rebord du haut et/ou du bas.
    """

    def __init__(
        self,
        dimension_piste: Rect,
        no: int,
        lignes_haut: bool = False,
        lignes_bas: bool = False,
    ) -> None:
        """Constructeur de la voie.

        Args:
            dimension_piste (Rect): Dimension de la voie.
            no (int): Index de la voie, 
            lignes_haut (bool, optional): _description_. Defaults to False.
            lignes_bas (bool, optional): _description_. Defaults to False.
        """
        assert no >= 0 and no < NB_DE_VOIES

        hauteur: int = dimension_piste.height / NB_DE_VOIES

        self.rect: Rect = Rect(
            (dimension_piste.topleft[0], dimension_piste.topleft[1] + no * hauteur),
            (dimension_piste.width, hauteur),
        )
        self.lignes_pointillees: list[LignePointillee] = []
        if lignes_haut:
            self.lignes_pointillees.append(
                LignePointillee(self.rect.right, self.rect.top)
            )
        if lignes_bas:
            self.lignes_pointillees.append(
                LignePointillee(self.rect.right, self.rect.bottom)
            )

    def dessine(self, fenetre: Surface, vitesse: int) -> None:
        draw.rect(fenetre, Color("gray"), self.rect)
        for ligne in self.lignes_pointillees:
            ligne.bouge(vitesse)
            ligne.dessine(fenetre)


class Piste:

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.rect: Rect = Rect((0, MARGE), (largeur, hauteur - 2 * MARGE))
        self.voies: list[Voie] = []
        for i in range(NB_DE_VOIES):
            self.voies.append(Voie(self.rect, i, lignes_haut=(i != 0)))

    def _dessine_bordure(self, fenetre: Surface) -> None:
        try:
            draw.line(
                fenetre,
                Color("white"),
                self.rect.topleft,
                self.rect.topright,
                LARGEUR_BORDURE,
            )
            draw.line(
                fenetre,
                Color("white"),
                self.rect.bottomleft,
                self.rect.bottomright,
                LARGEUR_BORDURE,
            )
        except TypeError as Err:
            print(
                f"Erreur durant le tracage d'une ligne dans la fonction {Piste._dessine_bordure.__name__}: {Err}"
            )

    def get_nb_voies(self) -> int:
        return NB_DE_VOIES

    def get_voie(self, no_voie: int) -> Voie:
        index = max(no_voie, 0)
        index = min(index, NB_DE_VOIES - 1)
        return self.voies[index]

    def dessine(self, fenetre: Surface, vitesse: int) -> None:
        for i in range(NB_DE_VOIES):
            self.voies[i].dessine(fenetre, vitesse)
        self._dessine_bordure(fenetre)
