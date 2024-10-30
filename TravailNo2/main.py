# -*- coding: utf-8 -*-
"""Ce programme implémente un jeu de course de voiture très simple afin de
s'exercer à la programmation python.
"""

import pygame
from pygame import Color
import random
import time
import itertools

from piste import Piste
from vehicule import *

LARGEUR_FENETRE = 1600
HAUTEUR_FENETRE = 800
VITESSE_MAX = 20
LONGUEUR_VEHICULE = 200
LARGEUR_VEHICULE = 100
PERIODE_CREATION_COMPETITEURS = 2


class NoValueReturned(Exception):
    """Exception utilisée lorsqu'une fonction n'est pas en mesure de retourner
    une valeur attendue.
    """

    pass


def creer_competiteur(piste: Piste, vitesse: int) -> Competiteur:
    """Cette fonction crée et retourne un compétiteur dans une voie choisie au
       hasard sur la piste donnée.

    Args:
        piste (Piste): La piste sur laquelle le compétiteur sera créer.
        vitesse (int): La vitesse initiale du véhicule créé.

    Raise:
        NoValueReturned: Lorsqu'aucun compétiteur n'a pu être créé (exemple,
        indisponibilité de la voie où devait être créée le compétiteur).

    Returns:
        Vehicule: Le compétiteur créé.
    """
    no_voie = random.randrange(0, piste.get_nb_voies())
    vitesse_competiteur: int = random.randrange(7, VITESSE_MAX)
    vitesse_apparante: int = vitesse_competiteur - vitesse
    try:
        if vitesse_apparante > 0:
            return Competiteur(
                vitesse_competiteur,
                Rect((-LONGUEUR_VEHICULE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)),
                piste.get_voie(no_voie),
            )
        elif vitesse_apparante < 0:
            return Competiteur(
                vitesse_competiteur,
                Rect((LARGEUR_FENETRE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)),
                piste.get_voie(no_voie),
            )
        else:
            raise NoValueReturned
    except ValueError:
        raise NoValueReturned


def main():
    """Fonction principale du programme."""

    random.seed()
    pygame.init()
    pygame.font.init()

    fenetre: Surface = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption("Grand prix FORMULE 1 x 10^6")

    competiteurs: list[Competiteur] = []
    piste = Piste(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    horloge = pygame.time.Clock()
    vitesse: int = 0
    voie_joueur = 1
    try:
        joueur = Joueur(
            0,
            Rect((0.2 * LARGEUR_FENETRE, 0), (LONGUEUR_VEHICULE, LARGEUR_VEHICULE)),
            piste.get_voie(voie_joueur),
        )
    except NoValueReturned as Err:
        print(
            f"Erreur lors de la création du véhicule du joueur dans la fonction {main.__name__}: {Err}"
        )
    compteur: int = (
        int(time.perf_counter())
        + 5  # Donne 5 secondes de délai avant l'arrivé des premiers compétiteurs
    )
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
                voie_joueur = max(voie_joueur - 1, 0)

            if event.key == pygame.K_DOWN:
                voie_joueur = min(voie_joueur + 1, piste.get_nb_voies() - 1)
        else:

            if not game_over:

                fenetre.fill(Color("black"))
                piste.dessine(fenetre, vitesse)
                try:
                    joueur.bouge(vitesse, piste.get_voie(voie_joueur))
                except NoValueReturned:
                    print(
                        f"Erreur lors du déplacement du véhicule du joueur dans la fonction {main.__name__}: {Err}"
                    )
                joueur.dessine(fenetre)

                # Nettoie les compétiteurs en ne gardant que ceux qui sont visibles.
                competiteurs = list(
                    filter(
                        lambda v: fenetre.get_rect().colliderect(v.rect), competiteurs
                    )
                )

                # Ajuste la vitesse lorsqu'une collision est possible entre compétiteurs.
                for c1, c2 in itertools.combinations(competiteurs, 2):
                    c1.ajuste_vitesse(c2)
                    c2.ajuste_vitesse(c1)

                if time.perf_counter() > compteur:
                    compteur = time.perf_counter() + PERIODE_CREATION_COMPETITEURS
                    try:
                        competiteur = creer_competiteur(piste, vitesse)
                        if not competiteur.est_chevauche_liste(competiteurs):
                            competiteurs.append(competiteur)
                    except NoValueReturned:
                        pass

                for competiteur in competiteurs:
                    competiteur.bouge(vitesse)
                    competiteur.dessine(fenetre)

                if joueur.est_chevauche_liste(competiteurs):
                    game_over = True

            else:

                # Game over
                my_font = pygame.font.SysFont("Comic Sans MS", 200)
                text_surface = my_font.render("Game over", False, Color("red"))
                textRect = text_surface.get_rect()
                textRect.center = (LARGEUR_FENETRE / 2, HAUTEUR_FENETRE / 2)
                fenetre.blit(text_surface, textRect)

            pygame.display.flip()
            horloge.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
