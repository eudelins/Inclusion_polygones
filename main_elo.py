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
# from tycat import read_instance
import numpy as np
from polygon import Polygon


def convert_polygones(nom_fichier):
    """Convertit le fichier en un vecteur de polygones"""
    with open(nom_fichier, 'r') as fichier:
        ligne = fichier.readlines()
        nb_poly = int(ligne[-1].strip('\n').split()[0])
        vect_poly = [[] for _ in range(nb_poly + 1)]
        for ligne in ligne:
            point = ligne.strip('\n').split()
            ind_poly = int(point[0])
            abs = float(point[1])
            ord = float(point[2])
            vect_poly[ind_poly].append([abs, ord])
        return vect_poly


def aire_polygones(vect_poly):
    """ calcul l'aire de chaque polygone du fichier
    retourne un tableau contenant des tableaux de dimension 2
    pour lesquels la case d'indice 0 est l'indice du polygone
    et la case d'indice 1 est l'aire en valeur absolue du polygone correspondant
    """
    vect_aires = []
    for indice in range(len(vect_poly)):
        polygones = Polygon(vect_poly[indice])
        vect_aires.append([indice, abs(polygones.area())])
    return vect_aires


def fusion(vecteur1, vecteur2):
    if vecteur1 == []:
        return vecteur2
    if vecteur2 == []:
        return vecteur1
    if vecteur1[0][1] < vecteur2[0][1] :
        return [vecteur1[0]] + fusion(vecteur1[1 :],vecteur2)
    else :
        return [vecteur2[0]] + fusion(vecteur1,vecteur2[1 :])


def tri_fusion(vect_aires):
    if len(vect_aires) <= 1:
        return vect_aires
    else:
        vect_aires1 = [vect_aires[x] for x in range(len(vect_aires)//2)]
        vect_aires2 = [vect_aires[x] for x in range(len(vect_aires)//2,len(vect_aires))]
        return fusion(trifusion(vect_aires1),trifusion(vect_aires2))


def indice_tri(vect_aires, indice_polygone):
    indice_cour = 0
    while indice_polygone != vect_aires[indice_cour][0]:
        indice_cour += 1
    return indice_cour


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


def inclusion_point(polygone, point):
    """Renvoie True si le point est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone)
    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone[indice], polygone[indice + 1]]
        if coupe_segment(segment, point):
            if point[1] != segment[1][1]:
                compteur += 1
    return compteur % 2 == 1


def trouve_inclusions4(vect_poly, indice_polygone, vect_aires, vect_inclusions):
    point_poly = vect_poly[indice_polygone][0]
    indice_cour = indice_tri(vect_aires, indice_polygone)
    while not inclusion_point(vect_poly[indice_cour], point_poly):
        if indice_cour == len(vect_aires) - 1:
            vect_inclusions[indice_polygone] = -1
            return vect_inclusions
        else:
            indice_cour += 1
    # si on sort du while, on a trouvé la premère inclusion
    vect_inclusions[indice_polygone] = vect_aires[indice_cour][0]
    return vect_inclusions


# def chrono(func, polygones):
    """Chronomètre le temps d'exécution de la fonction func"""
    debut = time.time()
    func(polygones)
    fin = time.time()
    return fin - debut


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
    vect_poly = convert_polygones("10x10.poly")
    longueur = len(vect_poly)
    vect_aires = aire_polygones(vect_poly)
    vect_inclusions = [-1 for _ in range(longueur)]  # -1 valeur par défaut
    tri_fusion(vect_aires)
    for indice_polygone in range(longueur):
        trouve_inclusions4(vect_poly, indice_polygone, vect_aires, vect_inclusions)
    print(vect_inclusions)


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
