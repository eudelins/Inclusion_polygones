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


# Complexité: O(1)
def isLeft(segment, point):
    """Renvoie True si le point est à gauche du segment"""
    if segment[1][0] - segment[0][0] == 0:
        return point[0] < segment[1][0]
    coef_dir = (segment[1][1] - segment[0][1])/(segment[1][0] - segment[0][0])
    ord_origine = segment[0][1] - coef_dir * segment[0][0]
    return (point[1] - ord_origine)/coef_dir > point[0]


# Complexité: O(1)
def coupe_segment(segment, point):
    """Renvoie True si la demi-droite horizontal partant de point et allant
    vers la droite coupe le segment et False sinon"""
    if segment[0][1] > point[1] and segment[1][1] > point[1]:
        return False
    elif segment[0][1] < point[1] and segment[1][1] < point[1]:
        return False
    elif segment[0][1] == point[1] and segment[1][1] == point[1]:
        return False

    # On a vérifié que l'ordonnée du point est entre celles des deux points du segments

    else:
        return isLeft(segment, point)


# Complexité: O(nb_pts du polygone)
def inclusion_point(polygone, point):
    """Renvoie True si le point est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone)
    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone[indice], polygone[indice + 1]]
        if coupe_segment(segment, point):
            if point[1] != segment[0][1] and point[1] != segment[1][1]:
                compteur += 1
            elif (polygone[indice - 1][1] < point[1] < segment[1][1]) or (polygone[indice - 1][1] > point[1] > segment[1][1]):
                compteur += 1
    return compteur % 2 == 1


# Complexité: O(n³ * nb_pts_poly) avec n le nb de polygone
def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_inclu = [[] for _ in range(len(polygones))]
    for index_poly in range(len(polygones)):
        polygone = polygones[index_poly]
        for indice in range(len(polygones)):
            autre_polygone = polygones[indice]
            if indice != index_poly and inclusion_point(autre_polygone, polygone[0]):
                vect_inclu[index_poly].append(indice)
    for index_poly in range(len(polygones)):
        if len(vect_inclu[index_poly]) == 0:
            vect_inclu[index_poly] = -1
        else:
            for indice in vect_inclu[index_poly]:
                b = True
                for j in vect_inclu[index_poly]:
                    if indice != j and not inclusion_point(polygones[j], polygones[indice][0]):
                        b = False
                        break
                if b:
                    vect_inclu[index_poly] = indice
                    break
    return vect_inclu


# Complexité: O(n² * nb_pts_poly) avec n le nb de polygone
def trouve_inclusions2(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_inclu = [-1 for _ in range(len(polygones))]
    for index in range(len(polygones)):
        polygon = polygones[index]
        appartient_deja = False  # Indique si polygon appartient déjà à un polygone
        poly_appartient = -1  # Numéro du polygone dans lequel polygon est inclu
        for i_autre_polygon in range(len(polygones)):
            if i_autre_polygon != index:
                autre_polygon = polygones[i_autre_polygon]
                if inclusion_point(autre_polygon, polygon[0]):
                    if not appartient_deja or inclusion_point(polygones[poly_appartient], autre_polygon[0]):
                        appartient_deja = True
                        poly_appartient = i_autre_polygon
        vect_inclu[index] = poly_appartient
    return vect_inclu


# Complexité: O(n² * nb_pts_poly) avec n le nb de polygone
def trouve_inclusions3(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_inclu = [-1 for _ in range(len(polygones))]
    for index in range(len(polygones)):
        polygon = polygones[index]
        poly_appartient = vect_inclu[index]  # Numéro du polygone dans lequel polygon est inclu
        appartient_deja = (poly_appartient != -1)  # Indique si polygon appartient déjà à un polygone
        for i_autre_polygon in range(index + 1, len(polygones)):
            autre_polygon = polygones[i_autre_polygon]
            if i_autre_polygon != poly_appartient:
                if inclusion_point(autre_polygon, polygon[0]):
                    if not appartient_deja or inclusion_point(polygones[poly_appartient], autre_polygon[0]):
                        appartient_deja = True
                        poly_appartient = i_autre_polygon
                if inclusion_point(polygon, autre_polygon[0]):
                    if vect_inclu[i_autre_polygon] == -1 or inclusion_point(polygones[vect_inclu[i_autre_polygon]], polygon[0]):
                        vect_inclu[i_autre_polygon] = index
        vect_inclu[index] = poly_appartient
    return vect_inclu


def tracage_courbe():
    """Trace  une courbe de performance en temps en fonction du nombre de
    polygones utilisés."""
    # plt.clr()
    les_x = [100 * i for i in range(30)]
    les_y_fct1 = [chrono(trouve_inclusions3, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct2 = [chrono(trouve_inclusions2, generateur_polygones(nb_poly)) for nb_poly in les_x]
    plt.plot(les_x, les_y_fct1, c = 'r' ,label = 'Fonction trouve_inclusions3')
    plt.plot(les_x, les_y_fct2, c = 'g' , label = 'Fonction trouve_inclusions2')
    plt.xlabel("Nombre de polygones")
    plt.ylabel("Temps d'exécution de la fonction (s)")
    plt.legend()
    plt.title('Temps en fonction du nombre de polygones')
    plt.savefig("Temps en fonction du nombre de polygones 2")


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    tracage_courbe()
    generateur_fichier("test.poly", 500)
    polygones = vecteur_polygone(sys.argv[1])
    print('La méthode 2 met ' + str(chrono(trouve_inclusions2, polygones)) + " a calculer le vecteur d'inclusions du fichier")
    print('La méthode 3 met ' + str(chrono(trouve_inclusions3, polygones)) + " a calculer le vecteur d'inclusions du fichier")


main()
