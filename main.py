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
        vect_aires2 = [vect_aires[x] for x in range(len(vect_aires)//2, len(vect_aires))]
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


class Noeud:
    """
    Le but est de créer un arbre dont chaque noeud contient les indices des
    polygones et a pour fils les polygones inclus dedans
    """
    def __init__(self, valeur):
        self.valeur = valeur
        self.fils = []

    def insere(self, polygones, num_polygon):
        """Insere le ième polygon de polygones dans self"""
        polygon, est_inclu = polygones[num_polygon], False
        for node in self.fils:
            num_autre_polygon = node.valeur
            autre_polygon = polygones[num_autre_polygon]
            if inclusion_point2(autre_polygon, polygon.points[0]):
                est_inclu = True
                node.insere(polygones, num_polygon)
                break
        if not est_inclu:
            self.fils.append(Noeud(num_polygon))


def complete_vect_inclu(pere, node, vect_inclusions):
    """Complete le vecteur d'inclusions"""
    num_polygon = node.valeur
    vect_inclusions[num_polygon] = pere
    for fils in node.fils:
        complete_vect_inclu(num_polygon, fils, vect_inclusions)


def trouve_inclusions5(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_aires, nb_poly = tri_fusion(aire_polygones(polygones)), len(polygones)
    arbre_inclu, vect_inclusions = Noeud(-1), [-1 for _ in range(nb_poly)]
    for i_polygon in range(nb_poly):
        num_polygon, _, polygon = vect_aires[i_polygon]
        arbre_inclu.insere(polygones, num_polygon)
    for node in arbre_inclu.fils:
        complete_vect_inclu(-1, node, vect_inclusions)
    return vect_inclusions


def tracage_courbe():
    """Trace  une courbe de performance en temps en fonction du nombre de
    polygones utilisés."""
    # plt.clr()
    les_x = [100 * i for i in range(30)]
    les_y_fct1 = [chrono(trouve_inclusions3, generateur_polygones(nb_poly)) for nb_poly in les_x]
    les_y_fct2 = [chrono(trouve_inclusions2, generateur_polygones(nb_poly)) for nb_poly in les_x]
    plt.plot(les_x, les_y_fct1, c='r', label='Fonction trouve_inclusions3')
    plt.plot(les_x, les_y_fct2, c='g', label='Fonction trouve_inclusions2')
    plt.xlabel("Nombre de polygones")
    plt.ylabel("Temps d'exécution de la fonction (s)")
    plt.legend()
    plt.title('Temps en fonction du nombre de polygones')
    plt.savefig("Temps en fonction du nombre de polygones 2")


# def main():
#     """
#     charge chaque fichier .poly donne
#     trouve les inclusions
#     affiche l'arbre en format texte
#     """
    # tracage_courbe()
    # generateur_fichier("test.poly", 500)
    # polygones = vecteur_polygone(sys.argv[1])
    # print('La méthode 2 met ' + str(chrono(trouve_inclusions2, polygones)) + " a calculer le vecteur d'inclusions du fichier")
    # print('La méthode 3 met ' + str(chrono(trouve_inclusions3, polygones)) + " a calculer le vecteur d'inclusions du fichier")


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
    for fichier in sys.argv[1:]
        polygones = read_instance(fichier)
        inclusion = trouve_inclusions5(polygones)
        print(inclusion)


if __name__ == "__main__":
    main()
