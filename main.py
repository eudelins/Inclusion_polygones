#!/usr/bin/env python3


"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""


import sys
# import matplotlib.pyplot as plt
from tycat import read_instance


def vecteur_polygone(nom_fichier):
    """Convertit le fichier en un vcteur de polygone"""
    with open(nom_fichier, 'r') as fichier:
        tab = fichier.readlines()
        nb_poly = int(tab[-1][0])
        vect_poly = [[] for _ in range(nb_poly + 1)]
        for ligne in tab:
            point = ligne.strip('\n').split()
            point = [int(point[0]), float(point[1]), float(point[2])]
            vect_poly[point[0]].append((point[1], point[2]))
        return vect_poly


def coupe_segment(segment, point):
    """Renvoie True si la demi-droite horizontal partant de point et allant
    vers la droite coupe le segment et False sinon"""
    if segment[0][1] > point[1] and segment[1][1] > point[1]:
        return False
    elif segment[0][1] < point[1] and segment[1][1] < point[1]:
        return False
    elif segment[0][1] == point[1] and segment[1][1] == point[1]:
        return False
    else:
        if segment[1][0] - segment[0][0] == 0:
            coef_dir = 0
        else:
            coef_dir = (segment[1][1] - segment[0][1])/(segment[1][0] - segment[0][0])
        ord_origine = segment[0][1] - coef_dir * segment[0][0]
        if coef_dir * point[0] + ord_origine >= point[1]:
            return True
        else:
            return False


def inclusion_point(polygone, point):
    """Renvoie True si le point est inclu dans le polygone, False sinon"""
    nb_pts = len(polygone)
    compteur = 0
    for indice in range(-1, nb_pts - 1):
        segment = [polygone[indice], polygone[indice + 1]]
        if coupe_segment(segment, point):
            compteur += 1
    if compteur % 2 == 1:
        return True
    return False


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
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
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    vect_inclu = [-1 for _ in range(len(polygones))]
    for index in range(len(polygones)):
        polygon = polygones[index]
        appartient_deja = False  # Indique si polygon appartient déjà à un polygone
        poly_appartient = -1  # Numéro du polygone dans lequel polygon est inclu
        for i_autre_polygon in range(len(polygones)):
            autre_polygon = polygones[i_autre_polygon]
            if i_autre_polygon != index:
                p_condition = inclusion_point(autre_polygon, polygon[0])
                d_condition = (appartient_deja and inclusion_point(polygones[poly_appartient], autre_polygon[0])) or not appartient_deja
                if p_condition and d_condition:
                    appartient_deja = True
                    poly_appartient = i_autre_polygon
        vect_inclu[index] = poly_appartient
    return vect_inclu


def tracage_courbe(fonction):
    """Trace  une courbe de performance en temps en fonction du nombre de
    polygones utilisés."""
    plt.clear()
    pass


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = vecteur_polygone(fichier)
        inclusions = trouve_inclusions2(polygones)
        print(inclusions)



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
