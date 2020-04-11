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


def fusion(vecteur1, vecteur2):
    """Fusionne deux vecteurs triés selon le 2ème élément de chaque
    sous-tableaux en un vecteur trié selon le 2ème élément des sous-tableaux"""
    i1, i2, n1, n2 = 0, 0, len(vecteur1), len(vecteur2)
    fus = [_ for _ in range(n1 + n2)]
    while i1 < n1 and i2 < n2:
        if vecteur1[i1][1] > vecteur2[i2][1]:
            fus[i1 + i2] = (vecteur1[i1])
            i1 += 1
        else:
            fus[i1 + i2] = (vecteur2[i2])
            i2 += 1
    if i1 == n1:
        fus[i1 + i2:] = (vecteur2[i2:])
    else:
        fus[i1 + i2:] = (vecteur1[i1:])
    return fus


def tri_fusion(vect_aires):
    """Réalise un tri fusion sur les aires de vect_aires"""
    if len(vect_aires) <= 1:
        return vect_aires
    else:
        vect_aires1 = [vect_aires[x] for x in range(len(vect_aires)//2)]
        vect_aires2 = [vect_aires[x] for x in range(len(vect_aires)//2,len(vect_aires))]
        return fusion(tri_fusion(vect_aires1), tri_fusion(vect_aires2))


def aire_polygones(polygones):
    """Calcul l'aire de chaque polygone du fichier et retourne un tableau
    contenant des tableaux contenant l'indice, l'aire du polygone et le
    polygone"""
    vect_aires = [[_, _, _] for _ in range(len(polygones))]
    for indice in range(len(polygones)):
        polygone = polygones[indice]
        vect_aires[indice] = ([indice, abs(polygone.area()), polygone])
    return vect_aires


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
# def inclusion_point2(polygone, point):
#     """Renvoie True si le point est inclu dans le polygone, False sinon"""
#     nb_pts = len(polygone.points)
#     abscisse_pts = [pts.coordinates[0] for pts in polygone.points]
#     if not (min(abscisse_pts) < point.coordinates[0] < max(abscisse_pts)):
#         return False
#
#     ordonnée_pts = [pts.coordinates[1] for pts in polygone.points]
#     if not (min(ordonnée_pts) < point.coordinates[1] < max(ordonnée_pts)):
#         return False
#
#     compteur = 0
#     for indice in range(-1, nb_pts - 1):
#         segment = [polygone.points[indice], polygone.points[indice + 1]]
#         if coupe_segment2(segment, point):
#             if point.coordinates[1] != segment[1].coordinates[1] and point.coordinates[1] != segment[0].coordinates[1]:
#                 compteur += 1
#             else:
#                 id_point_prec = indice - 1
#                 while (point.coordinates[1] == polygone.points[id_point_prec].coordinates[1]):
#                     id_point_prec -= 1
#                 if (polygone.points[id_point_prec].coordinates[1] < point.coordinates[1] < segment[1].coordinates[1]) or (polygone.points[id_point_prec].coordinates[1] > point.coordinates[1] > segment[1].coordinates[1]):
#                     compteur += 1
#     return compteur % 2 == 1


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



def trouve_inclusions4(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_aires, nb_poly = tri_fusion(aire_polygones(polygones)), len(polygones)
    vect_inclusions = [-1 for _ in range(nb_poly)]
    for i_polygon in range(1, nb_poly):
        num_polygon, _, polygon, = vect_aires[i_polygon]
        i_autre_polygon =  i_polygon - 1
        while i_autre_polygon >= 0:
            num_autre_polygon, _, autre_polygon = vect_aires[i_autre_polygon]
            if inclusion_point2(autre_polygon, polygon.points[0]):
                vect_inclusions[num_polygon] = num_autre_polygon
                break
            i_autre_polygon -= 1
    return vect_inclusions


# class Arbre:
#     def __init__(self):
#         self.racine = Noeud(-1, float("inf"), None)
#         self.feuilles = deque()
#
#     def insere_rec2(self, polygones, num_polygon, aire_poly, polygon, quadrants):
#         """Insere le ième polygon de polygones dans self"""
#         noeud_a_tester = self.feuilles.copy()
#         while noeud_a_tester:
#             node = noeud_a_tester.pop()
#             est_feuille = node in self.feuilles
#             if est_feuille:
#                 self.feuilles.pop()
#             num_autre_polygon = node.valeur
#             autre_polygon = polygones[num_autre_polygon]
#             if quadrants[num_polygon].intersect(quadrants[num_autre_polygon]):
#                 if node.aire > aire_poly:
#                     if inclusion_point2(autre_polygon, polygon.points[0]):
#                         new_noeud = Noeud(num_polygon, aire_poly, node)
#                         node.fils.append(new_noeud)
#                         self.feuilles.append(new_noeud)
#                         return
#             else:
#                 if est_feuille:
#                     self.feuilles.appendleft(node)
#                 if node.pere is not None and node.pere not in noeud_a_tester:
#                     noeud_a_tester.appendleft(node.pere)
#         new_noeud = Noeud(num_polygon, aire_poly, self.racine)
#         self.racine.fils.append(new_noeud)
#         self.feuilles.append(new_noeud)


# def trouve_inclusions7(polygones):
#     """
#     renvoie le vecteur des inclusions la ieme case contient l'indice du
#     polygone contenant le ieme polygone (-1 si aucun)
#     """
#     vect_aires = sorted(aire_polygones(polygones), key=lambda poly: poly[1], reverse=True)
#     quadrants = [polygon.bounding_quadrant() for polygon in polygones]
#     nb_poly = len(polygones)
#     arbre_inclu, vect_inclusions = Arbre(), [-1 for _ in range(nb_poly)]
#     for i_polygon in range(nb_poly):
#         num_polygon, aire_poly, polygon = vect_aires[i_polygon]
#         arbre_inclu.insere_rec2(polygones, num_polygon, aire_poly, polygon, quadrants)
#     complete_vect_inclu_rec(arbre_inclu.racine, vect_inclusions)
#     return vect_inclusions


# def transforme(poly):
#     """Change un tableau de couple en Polygon"""
#     n = len(poly)
#     liste_points = [Point([0, 0])] * n
#     for i_point in range(n):
#         liste_points[i_point] = Point(poly[i_point])
#     return Polygon(liste_points)


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
    polygones1 = read_instance("lourd.poly")
    inclusion1 = trouve_inclusions4(polygones1)
    print(inclusion1)
    # m = 0
    # for _ in range(10):
    #     m += chrono(trouve_inclusions4, polygones1)
    # print(m/10)
