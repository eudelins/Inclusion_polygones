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
from main import trouve_inclusions2, trouve_inclusions5, trouve_inclusions6
# from main import trouve_inclusions4


def chrono(func, polygones):
    """Chronomètre le temps d'exécution de la fonction func"""
    debut = time.time()
    func(polygones)
    fin = time.time()
    return fin - debut



def aire_polygones(polygones):
    """Calcul l'aire de chaque polygone du fichier et retourne un tableau
    contenant des tableaux contenant l'indice, l'aire du polygone et le
    polygone"""
    vect_aires = [[_, _, _] for _ in range(len(polygones))]
    for indice in range(len(polygones)):
        polygone = polygones[indice]
        vect_aires[indice] = ([indice, abs(polygone.area()), polygone])
    return vect_aires


def isLeft2(segment, point):
    """Renvoie True si le point est à gauche du segment"""
    if segment[1].coordinates[0] - segment[0].coordinates[0] == 0:
        return point.coordinates[0] < segment[1].coordinates[0]
    coef_dir = (segment[1].coordinates[1] - segment[0].coordinates[1])/(segment[1].coordinates[0] - segment[0].coordinates[0])
    ord_origine = segment[0].coordinates[1] - coef_dir * segment[0].coordinates[0]
    return (point.coordinates[1] - ord_origine)/coef_dir > point.coordinates[0]


def coupe_segment2(segment, point):
    """Renvoie True si la demi-droite horizontal partant de point et allant
    vers la droite coupe le segment et False sinon"""
    if segment[0].coordinates[1] > point.coordinates[1] and segment[1].coordinates[1] > point.coordinates[1]:
        return False
    elif segment[0].coordinates[1] < point.coordinates[1] and segment[1].coordinates[1] < point.coordinates[1]:
        return False
    elif segment[0].coordinates[1] == point.coordinates[1] and segment[1].coordinates[1] == point.coordinates[1]:
        return False

    # On a vérifié que l'ordonnée du point est entre celles des deux points du segments
    if segment[0].coordinates[0] < point.coordinates[0] and segment[1].coordinates[0] < point.coordinates[0]:
        return False
    elif segment[0].coordinates[0] > point.coordinates[0] and segment[1].coordinates[0] > point.coordinates[0]:
        return True
    else:
        return isLeft2(segment, point)


def inclusion_point2(polygone, point):
    """Renvoie True si autres est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone.points)
    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone.points[indice], polygone.points[indice + 1]]
        if coupe_segment2(segment, point):
            if point.coordinates[1] != segment[1].coordinates[1] and point.coordinates[1] != segment[0].coordinates[1]:
                compteur += 1
            else:
                id_point_prec = indice - 1
                while (point.coordinates[1] == polygone.points[id_point_prec].coordinates[1]):
                    id_point_prec -= 1
                if (polygone.points[id_point_prec].coordinates[1] < point.coordinates[1] < segment[1].coordinates[1]) or (polygone.points[id_point_prec].coordinates[1] > point.coordinates[1] > segment[1].coordinates[1]):
                    compteur += 1
    return compteur % 2 == 1


def trouve_inclusions4(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_aires = sorted(aire_polygones(polygones), key=lambda poly: poly[1], reverse=True)
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    nb_poly = len(polygones)
    vect_inclusions = [-1 for _ in range(nb_poly)]
    saut = 1

    debut = time.time()
    quadrillage = [[quadrants[vect_aires[0][0]], [vect_aires[0]]]]
    for i_polygon in range(1, nb_poly):
        num_polygon, aire_poly, polygon, = vect_aires[i_polygon]
        for case in quadrillage:
            if case[0].intersect(quadrants[i_polygon]):
                case[0].update(quadrants[i_polygon])
                case[1].append(vect_aires[i_polygon])
                break
        quadrillage.append([quadrants[i_polygon], [vect_aires[i_polygon]]])
    fin = time.time()
    print(fin - debut)

    for case in quadrillage:
        nb_poly_case = len(case[1])
        for i_polygon in range(1, nb_poly_case):
            num_polygon, aire_poly, polygon, = case[1][i_polygon]
            
            if aire_poly == case[1][i_polygon - 1][1]:
                saut += 1
                i_autre_polygon =  i_polygon - saut
            else:
                saut = 1
                i_autre_polygon =  i_polygon - saut
            
            while i_autre_polygon >= 0:
                num_autre_polygon, aire_autre_poly, autre_polygon = case[1][i_autre_polygon]
                if aire_poly < aire_autre_poly:
                    if quadrants[num_polygon].intersect(quadrants[num_autre_polygon]):
                        if inclusion_point2(autre_polygon, polygon.points[0]):
                            vect_inclusions[num_polygon] = num_autre_polygon
                            break
                i_autre_polygon -= 1
    return vect_inclusions



def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    polygones = read_instance(sys.argv[1])
    if sys.argv[2] == '4':
        print(chrono(trouve_inclusions4, polygones))
    elif sys.argv[2] == '5':
        print(chrono(trouve_inclusions5, polygones))
    else:
        print(chrono(trouve_inclusions6, polygones))



# if __name__ == "__main__":
main()
