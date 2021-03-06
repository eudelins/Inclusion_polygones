#!/usr/bin/env python3


"""
Fichier principal pour la detection des inclusions.
Ce fichier est utilise pour les tests automatiques.
Attention donc lors des modifications.
"""


import sys
import time
from tycat import read_instance
from geo.polygon import Polygon
from geo.point import Point
from geo.quadrant import Quadrant
from collections import deque


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


def isLeft(segment, point):
    """Renvoie True si le point est à gauche du segment"""
    if segment[1][0] - segment[0][0] == 0:
        return point[0] < segment[1][0]
    coef_dir = (segment[1][1] - segment[0][1])/(segment[1][0] - segment[0][0])
    ord_origine = segment[0][1] - coef_dir * segment[0][0]
    return (point[1] - ord_origine)/coef_dir > point[0]


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
    if segment[0][0] < point[0] and segment[1][0] < point[0]:
        return False
    elif segment[0][0] > point[0] and segment[1][0] > point[0]:
        return True
    else:
        return isLeft(segment, point)


def inclusion_point(polygone, point):
    """Renvoie True si le point est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone)
    abscisse_pts = [pts[0] for pts in polygone]
    if not (min(abscisse_pts) < point[0] < max(abscisse_pts)):
        return False

    ordonnée_pts = [pts[1] for pts in polygone]
    if not (min(ordonnée_pts) < point[1] < max(ordonnée_pts)):
        return False

    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone[indice], polygone[indice + 1]]
        if coupe_segment(segment, point):
            if point[1] != segment[0][1] and point[1] != segment[1][1]:
                compteur += 1
            else:
                id_point_prec = indice - 1
                while (point[1] == polygone[id_point_prec][1]):
                    id_point_prec -= 1
                if (polygone[id_point_prec][1] < point[1] < segment[1][1]) or (polygone[id_point_prec][1] > point[1] > segment[1][1]):
                    compteur += 1
    return compteur % 2 == 1


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


    # quadrillage = [[quadrants[vect_aires[0][0]], [vect_aires[0]]]]
    # for i_polygon in range(1, nb_poly):
    #     num_polygon, aire_poly, polygon, = vect_aires[i_polygon]
    #     for case in quadrillage:
    #         if case[0].intersect(quadrants[i_polygon]):
    #             case[0].update(quadrants[i_polygon])
    #             case[1].append(vect_aires[i_polygon])
    #             break
    #     quadrillage.append([quadrants[i_polygon], [vect_aires[i_polygon]]])


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

    for i_polygon in range(1, nb_poly):
        num_polygon, aire_poly, polygon, = vect_aires[i_polygon]
        
        if aire_poly == vect_aires[i_polygon - 1][1]:
            saut += 1
            i_autre_polygon =  i_polygon - saut
        else:
            saut = 1
            i_autre_polygon =  i_polygon - saut
        
        while i_autre_polygon >= 0:
            num_autre_polygon, _, autre_polygon = vect_aires[i_autre_polygon]
            if quadrants[num_polygon].intersect(quadrants[num_autre_polygon]):
                if inclusion_point2(autre_polygon, polygon.points[0]):
                    vect_inclusions[num_polygon] = num_autre_polygon
                    break
            i_autre_polygon -= 1
    return vect_inclusions


class Noeud:
    """
    Le but est de créer un arbre dont chaque noeud contient les indices des
    polygones et a pour fils les polygones inclus dedans
    """
    def __init__(self, valeur, aire):
        self.valeur = valeur
        self.aire = aire
        # self.pere = pere
        self.fils = deque()

    def insere(self, polygones, num_polygon, aire_poly, polygon, quadrants):
        """Insere le ième polygon de polygones dans self"""
        noeud_a_tester, est_inclu = self.fils.copy(), False
        while noeud_a_tester:
            node = noeud_a_tester.popleft()
            num_autre_polygon = node.valeur
            autre_polygon = polygones[num_autre_polygon]
            if node.aire > aire_poly:
                if quadrants[num_polygon].intersect(quadrants[num_autre_polygon]):
                    if inclusion_point2(autre_polygon, polygon.points[0]):
                        est_inclu, noeud_inclu = True, node
                        noeud_a_tester = node.fils.copy()
        if not est_inclu:
            self.fils.append(Noeud(num_polygon, aire_poly))
        else:
            noeud_inclu.fils.append(Noeud(num_polygon, aire_poly))

    def insere_rec(self, polygones, num_polygon, aire_poly, polygon, quadrants):
        """Insere le ième polygon de polygones dans self"""
        est_inclu = False
        for node in self.fils:
            num_autre_polygon = node.valeur
            autre_polygon = polygones[num_autre_polygon]
            if quadrants[num_polygon].intersect(quadrants[num_autre_polygon]):
                if node.aire > aire_poly:
                    if inclusion_point2(autre_polygon, polygon.points[0]):
                        est_inclu = True
                        node.insere(polygones, num_polygon, aire_poly, polygon, quadrants)
                        break
        if not est_inclu:
            self.fils.append(Noeud(num_polygon, aire_poly))


def complete_vect_inclu(pere, vect_inclusions):
    """Complete le vecteur d'inclusions"""
    noeuds_a_completer = [[pere.valeur, pere.fils.copy()]]
    while noeuds_a_completer:
        noeuds_fils = noeuds_a_completer.pop()
        while noeuds_fils[1]:
            noeud = noeuds_fils[1].pop()
            num_polygon = noeud.valeur
            vect_inclusions[num_polygon] = noeuds_fils[0]
            noeuds_a_completer.append([num_polygon, noeud.fils.copy()])


def complete_vect_inclu_rec(pere, vect_inclusions):
    """Complete le vecteur d'inclusions"""
    for fils in pere.fils:
        num_polygon = fils.valeur
        vect_inclusions[num_polygon] = pere.valeur
        complete_vect_inclu(fils, vect_inclusions)


def trouve_inclusions5(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_aires = sorted(aire_polygones(polygones), key=lambda poly: poly[1], reverse=True)
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    nb_poly = len(polygones)
    arbre_inclu, vect_inclusions = Noeud(-1, float("inf")), [-1 for _ in range(nb_poly)]
    for i_polygon in range(nb_poly):
        num_polygon, aire_poly, polygon = vect_aires[i_polygon]
        arbre_inclu.insere_rec(polygones, num_polygon, aire_poly, polygon, quadrants)
    complete_vect_inclu_rec(arbre_inclu, vect_inclusions)
    return vect_inclusions


def trouve_inclusions6(polygones):
    """
    renvoie le vecteur des inclusions la ieme case contient l'indice du
    polygone contenant le ieme polygone (-1 si aucun)
    """
    vect_aires = sorted(aire_polygones(polygones), key=lambda poly: poly[1], reverse=True)
    quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    nb_poly = len(polygones)
    arbre_inclu, vect_inclusions = Noeud(-1, float("inf")), [-1 for _ in range(nb_poly)]
    for i_polygon in range(nb_poly):
        num_polygon, aire_poly, polygon = vect_aires[i_polygon]
        arbre_inclu.insere(polygones, num_polygon, aire_poly, polygon, quadrants)
    complete_vect_inclu(arbre_inclu, vect_inclusions)
    return vect_inclusions


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        # polygones = read_instance(fichier)
        polygones = read_instance(fichier)
        inclusion = trouve_inclusions4(polygones)
        print(inclusion)


if __name__ == "__main__":
    main()
