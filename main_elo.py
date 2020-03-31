#!/usr/bin/env python3


"""
Fichier principal pour la detection des inclusions.
Ce fichier est utilise pour les tests automatiques.
Attention donc lors des modifications.
"""


import sys
import time
import pdb
from random import randint
import matplotlib.pyplot as plt
# from tycat import read_instance
import numpy as np
from polygon import Polygon
from point import Point


def convert_polygones(nom_fichier):
    """
    Convertit le fichir en un vecteur de convert_polygones
    """

    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        nb_poly = int(lignes[-1].strip('\n').split()[0]) + 1
        vect_poly = [0 for _ in range(nb_poly)]

        ind_poly_prec = int(lignes[0][0])
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
                point_cour = [Point([float(infos_point[1]), float(infos_point[2])])]
                    # récup l'abs et l'ord du point
                ind_poly_prec = ind_poly

        vect_poly.append(Polygon(point_cour))

        return vect_poly  # ok


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
        vect_aires.append([indice_cour, abs(poly_cour.area())])

    return vect_aires  # ok


def fusion(vecteur1, vecteur2):
    """Fusionne deux vecteurs triés selon le 2ème élément de chaque
    sous-tableaux en un vecteur trié selon le 2ème élément des sous-tableaux"""
    i1, i2, n1, n2 = 0, 0, len(vecteur1), len(vecteur2)
    fus = []
    while i1 < n1 and i2 < n2:
        if vecteur1[i1][1] < vecteur2[i2][1]:
            fus.append(vecteur1[i1])
            i1 += 1
        else:
            fus.append(vecteur2[i2])
            i2 += 1
    if i1 == n1:
        fus.extend(vecteur2[i2:])
    else:
        fus.extend(vecteur1[i1:])
    return fus  # ok


def tri_fusion(vect_aires):
    """Réalise un tri fusion sur les aires de vect_aires"""
    if len(vect_aires) <= 1:
        return vect_aires
    else:
        vect_aires1 = [vect_aires[x] for x in range(len(vect_aires)//2)]
        vect_aires2 = [vect_aires[x] for x in range(len(vect_aires)//2,len(vect_aires))]
        return fusion(tri_fusion(vect_aires1), tri_fusion(vect_aires2))  # ok


# Complexité: O(1)
def isLeft2(segment, point):
    """Renvoie True si le point est à gauche du segment"""
    if segment[1].coordinates[0] - segment[0].coordinates[0] == 0:
        return point.coordinates[0] < segment[1].coordinates[0]
    coef_dir = (segment[1].coordinates[1] - segment[0].coordinates[1])/(segment[1].coordinates[0] - segment[0].coordinates[0])
    ord_origine = segment[0].coordinates[1] - coef_dir * segment[0].coordinates[0]
    return (point.coordinates[1] - ord_origine)/coef_dir > point.coordinates[0]


# Complexité: O(1)
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

    else:
        return isLeft2(segment, point)


# Complexité: O(nb_pts du polygone)
def inclusion_point2(polygone, point):
    """Renvoie True si le point est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone.points)
    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone.points[indice], polygone.points[indice + 1]]
        if coupe_segment2(segment, point):
            if point.coordinates[1] != segment[1].coordinates[1] and point.coordinates[1] != segment[0].coordinates[1]:
                compteur += 1
            elif (polygone.points[indice - 1].coordinates[1] < point.coordinates[1] < segment[1].coordinates[1]) or (polygone.points[indice - 1].coordinates[1] > point.coordinates[1] > segment[1].coordinates[1]):
                compteur += 1
    return compteur % 2 == 1


def indice_vect_aire(vect_aires_trie, indice_polygone):
    """Renvoie l'indice correspondant à la place du polygone dans le vecteur aires,
    sachant son indice_tri
    """
    for indice_cour in range(len(vect_aires_trie)):
        if vect_aires_trie[indice_cour][0] == indice_polygone:
            return indice_cour
        else:
            indice_cour += 1
    # on a des pb ici, car des fois indice_cour vaut None
    return -1


def trouve_inclusions4(vect_poly, indice_polygone, vect_aires, vect_inclusions):
    """
    Renvoie vect_inclusions tel que:
    on parcourt les éléments de vect_aires tels que leurs aires soient plus
    grandes que l'aire du polygone associé à indice_polygone
    si un point du polygone associé à indice_polygone est inclu dans un
    des polygones d'aires supérieures,
    alors on modifie vect_inclusions et on met l'indice de ce polygone d'aire
    supérieure en indice [indice_polygone][0]
    """
    point_poly = vect_poly[indice_polygone].points[0]  # un point de poly
    vect_aires_trie = tri_fusion(vect_aires)  # trie vect_aires
    indice_cour = indice_vect_aire(vect_aires_trie, indice_polygone) + 1

    if indice_cour >= len(vect_poly):
        vect_inclusions[indice_polygone] = -1
        return vect_inclusions

    while not inclusion_point2(vect_poly[vect_aires_trie[indice_cour][0]], point_poly):

        if indice_cour + 1 >= len(vect_poly):
            vect_inclusions[indice_polygone] = -1
            return vect_inclusions

        else:
            indice_cour += 1

    # si on sort du while, on a trouvé la premère inclusion
    vect_inclusions[indice_polygone] = vect_aires_trie[indice_cour][0]

    return vect_inclusions


# def chrono(func, polygones):
#     """Chronomètre le temps d'exécution de la fonction func"""
#     debut = time.time()
#     func(polygones)
#     fin = time.time()
#     return fin - debut


# def tracage_courbe():
#     """Trace  une courbe de performance en temps en fonction du nombre de
#     polygones utilisés."""
#     # plt.clr()
#     les_x = [100 * i for i in range(30)]
#     les_y_fct1 = [chrono(trouve_inclusions3, convert_polygones(nb_poly)) for nb_poly in les_x]
#     les_y_fct2 = [chrono(trouve_inclusions2, convert_polygones(nb_poly)) for nb_poly in les_x]
#     plt.plot(les_x, les_y_fct1, c = 'r' ,label = 'Fonction trouve_inclusions3')
#     plt.plot(les_x, les_y_fct2, c = 'g' , label = 'Fonction trouve_inclusions2')
#     plt.xlabel("Nombre de polygones")
#     plt.ylabel("Temps d'exécution de la fonction (s)")
#     plt.legend()
#     plt.title('Temps en fonction du nombre de polygones')
#     plt.savefig("Temps en fonction du nombre de polygones 2")


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    debut = time.time()
    vect_poly = convert_polygones("lourd.poly")
    longueur = len(vect_poly)
    vect_aires = aire_polygones(vect_poly)
    vect_inclusions = [-1 for _ in range(longueur)]  # -1 valeur par défaut
    for indice_polygone in range(longueur):
        vect_inclusions = trouve_inclusions4(vect_poly, indice_polygone, vect_aires, vect_inclusions)
    fin = time.time()
    print(fin - debut)


# def main():
#     """
#     charge chaque fichier .poly donne
#     trouve les inclusions
#     affiche l'arbre en format texte
#     """
#     for fichier in sys.argv[1:]:
#         polygones = read_instance(fichier)
#         inclusions = trouve_inclusions(polygones)
#         print(inclusions)


if __name__ == "__main__":
    main()
