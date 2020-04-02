#!/usr/bin/env python3

"""
Fichier principal pour la detection des inclusions.
Ce fichier est utilise pour les tests automatiques.
Attention donc lors des modifications.
"""

import sys
import time
from random import randint
import matplotlib.pyplot as plt
from tycat import read_instance
from geo.polygon import Polygon
from geo.point import Point
import numpy as np


def convert_polygones(nom_fichier):
    """
    Convertit le fichir en un vecteur de convert_polygones
    """

    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        nb_poly = int(lignes[-1].strip('\n').split()[0]) + 1
        vect_poly = [0 for _ in range(nb_poly)]

        ind_poly_prec = lignes[0][0]
        point_cour = []
        vect_poly = []

        for ligne in lignes:
            infos_point = ligne.strip('\n').split()
                # récup chaîne de caractR sans les espaces ni les sauts de ligne
            ind_poly = int(infos_point[0])
                # récup l'indice du point

            if ind_poly == ind_poly_prec:
                point_cour.append(Point([float(infos_point[1]), float(infos_point[2])]))
                    # récup l'abs et l'ord du point
            else:
                vect_poly.append(Polygon(point_cour))
                point_cour = [Point([infos_point[1], infos_point[2]])]
                    # récup l'abs et l'ord du point
                ind_poly_prec = ind_poly


        return vect_poly


def aire_polygones(vect_poly):
    """
    Calcul l'aire de chaque polygone du fichier
    retourne un tableau contenant des tableaux de dimension 2
    pour lesquels la case d'indice 0 est l'indice du polygone
    et la case d'indice 1 est l'aire en valeur absolue du polygone correspondant
    """

    vect_aires = []

    for indice_cour in range(len(vect_poly)):
        poly_cour = vect_poly[indice_cour]
        vect_aires.append(abs(poly_cour.area()))

    return vect_aires


def main():
    """
    Charge un fichier .poly et renvoie le vecteur d'inclusions
    """

    vect_poly = convert_polygones("10x10.poly")
    longueur = len(vect_poly)
    vect_aires = aire_polygones(vect_poly)


if __name__ == "__main__":
    main()
