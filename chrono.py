#!/usr/bin/env python3


"""
Fichier pour chronométrer
"""


import sys
import time
from random import randint
import matplotlib.pyplot as plt
from tycat import read_instance
from geo.polygon import Polygon
from geo.point import Point
import numpy as np
from main import trouve_inclusions2, trouve_inclusions4, trouve_inclusions5




def chrono(func, polygones):
    """Chronomètre le temps d'exécution de la fonction func"""
    debut = time.time()
    func(polygones)
    fin = time.time()
    return fin - debut


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        print(chrono(trouve_inclusions5, polygones))


if __name__ == "__main__":
    main()
