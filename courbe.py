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
from main import trouve_inclusions4, trouve_inclusions5
from methode1 import trouve_inclusions, trouve_inclusions2, trouve_inclusions3


def generateur_fichier(nom_fichier, nb_poly):
    """Génère nb_poly carrés les uns dans les autres dans nom_fichier"""
    with open(nom_fichier, 'w') as fichier:
        for indice in range(nb_poly):
            point1 = str(indice) + " " + str(0 + indice) + " " + str(0 + indice) + "\n"
            point2 = str(indice) + " " + str(2 * nb_poly + 100 - indice) + " " + str(0 + indice) + "\n"
            point3 = str(indice) + " " + str(2 * nb_poly + 100 - indice) + " " + str(2 * nb_poly + 100 - indice) + "\n"
            point4 = str(indice) + " " + str(0 + indice) + " " + str(2 * nb_poly + 100 - indice) + "\n"
            fichier.writelines(point1 + point2 + point3 + point4)


def generateur_polygones(nb_poly):
    """Génère nb_poly carrés les uns dans les autres stockés dans un tableau"""
    tab = []
    for indice in range(nb_poly):
        point1 = (0 + indice, 0 + indice)
        point2 = (2 * nb_poly + 100 - indice, 0 + indice)
        point3 = (2 * nb_poly + 100 - indice, 2 * nb_poly + 100 - indice)
        point4 = (0 + indice, 2 * nb_poly + 100 - indice)
        tab.append([point1, point2, point3, point4])
    return tab


def generateur_polygones2(nb_poly):
    """Génère nb_poly carrés les uns dans les autres stockés dans un tableau"""
    tab = []
    for indice in range(nb_poly):
        point1 = Point([0 + indice, 0 + indice])
        point2 = Point([2 * nb_poly + 100 - indice, 0 + indice])
        point3 = Point([2 * nb_poly + 100 - indice, 2 * nb_poly + 100 - indice])
        point4 = Point([0 + indice, 2 * nb_poly + 100 - indice])
        tab.append(Polygon([point1, point2, point3, point4]))
    return tab


def vecteur_polygone(nom_fichier):
    """Convertit le fichier en un vcteur de polygone"""
    with open(nom_fichier, 'r') as fichier:
        tab = fichier.readlines()
        nb_poly = int(tab[-1].strip('\n').split()[0])
        vect_poly = [[] for _ in range(nb_poly + 1)]
        for ligne in tab:
            point = ligne.strip('\n').split()
            point = [int(point[0]), float(point[1]), float(point[2])]
            vect_poly[point[0]].append([point[1], point[2]])
        return vect_poly


def chrono(func, polygones):
    """Chronomètre le temps d'exécution de la fonction func"""
    debut = time.time()
    func(polygones)
    fin = time.time()
    return fin - debut


def tracage_courbe1():
    """Trace  une courbe de performance en temps en fonction du nombre de
    polygones utilisés."""
    les_x = [100 * i for i in range(5)]
    les_y_fct1 = [chrono(trouve_inclusions, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct2 = [chrono(trouve_inclusions2, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct3 = [chrono(trouve_inclusions3, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct4 = [chrono(trouve_inclusions4, generateur_polygones2(nb_poly)) for nb_poly in les_x]
    les_y_fct5 = [chrono(trouve_inclusions5, generateur_polygones2(nb_poly)) for nb_poly in les_x]
    plt.plot(les_x, les_y_fct1, c='r', label='Fonction trouve_inclusions')
    plt.plot(les_x, les_y_fct2, c='g', label='Fonction trouve_inclusions2')
    plt.plot(les_x, les_y_fct3, c='b', label='Fonction trouve_inclusions3')
    plt.plot(les_x, les_y_fct4, c='k', label='Fonction trouve_inclusions4')
    plt.plot(les_x, les_y_fct5, c='m', label='Fonction trouve_inclusions5')
    plt.xlabel("Nombre de polygones")
    plt.ylabel("Temps d'exécution de la fonction (s)")
    plt.legend()
    plt.title('Temps en fonction du nombre de polygones')
    plt.savefig("Performance1.png")


def tracage_courbe2():
    """Trace  une courbe de performance en temps en fonction du nombre de
    polygones utilisés."""
    les_x = [100 * i for i in range(20)]
    les_y_fct2 = [chrono(trouve_inclusions2, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct3 = [chrono(trouve_inclusions3, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct4 = [chrono(trouve_inclusions4, generateur_polygones2(nb_poly)) for nb_poly in les_x]
    les_y_fct5 = [chrono(trouve_inclusions5, generateur_polygones2(nb_poly)) for nb_poly in les_x]
    plt.plot(les_x, les_y_fct2, c='g', label='Fonction trouve_inclusions2')
    plt.plot(les_x, les_y_fct3, c='b', label='Fonction trouve_inclusions3')
    plt.plot(les_x, les_y_fct4, c='k', label='Fonction trouve_inclusions4')
    plt.plot(les_x, les_y_fct5, c='m', label='Fonction trouve_inclusions5')
    plt.xlabel("Nombre de polygones")
    plt.ylabel("Temps d'exécution de la fonction (s)")
    plt.legend()
    plt.title('Temps en fonction du nombre de polygones')
    plt.savefig("Performance2.png")


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    tracage_courbe2()


if __name__ == "__main__":
    main()
