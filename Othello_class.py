# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:02:16 2022

@author: prje
"""

import numpy as np
from tkinter import *
from tkinter import ttk
from math import floor

class Game():
    def __init__(self, gametype="H-H", nb_cases=8, GUI=True, GUI_size=800, exploration_depth=5):
        # Gametype = "H-H", "H-IA", "IA-IA"
        self.nb_cases = nb_cases
        self.GUI_size = GUI_size
        self.GUI = GUI

        self.joueur = False

        self.init_Board

        self.white_pawns = []
        self.black_pawns = []

        self.exploration_depth = exploration_depth

        self.is_over = False

        if self.GUI:
            self.init_GUI()

    def init_GUI(self):
        # Initialisation de la grille (manque les numero et lettre sur les côtés)
        root = Tk()
        self.grille = Canvas(root, width=self.GUI_size, height=self.GUI_size, background="green")
        self.grille.pack(side=LEFT)
        for i in range(self.nb_cases):
            self.grille.create_line((self.GUI_size / self.nb_cases) * (i + 1), 0,
                                    (self.GUI_size / self.nb_cases) * (i + 1), self.GUI_size, fill='white', width=2)
            self.grille.create_line(0, (self.GUI_size / self.nb_cases) * (i + 1), self.GUI_size,
                                    (self.GUI_size / self.nb_cases) * (i + 1), fill='white', width=2)

        # Haut gauche
        self.grille.create_oval(((self.nb_cases / 2) - 1) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                ((self.nb_cases / 2) - 1) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                outline='white', fill="white", width=2)
        self.white_pawns.append(((int((self.nb_cases / 2) - 1)), int((self.nb_cases / 2) - 1)))
        # Haut droit
        self.grille.create_oval((self.nb_cases / 2) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                ((self.nb_cases / 2) - 1) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                ((self.nb_cases / 2) + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                outline='black', fill="black", width=2)
        self.black_pawns.append((int((self.nb_cases / 2)), int((self.nb_cases / 2) - 1)))
        # Bas Gauche
        self.grille.create_oval(((self.nb_cases / 2) - 1) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                ((self.nb_cases / 2) + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                outline='black', fill="black", width=2)
        self.black_pawns.append(((int((self.nb_cases / 2) - 1)), int((self.nb_cases / 2))))
        # Bas droit
        self.grille.create_oval((self.nb_cases / 2) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                (self.nb_cases / 2) * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                ((self.nb_cases / 2) + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                ((self.nb_cases / 2) + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                outline='white', fill="white", width=2)
        self.white_pawns.append((int((self.nb_cases / 2)), int((self.nb_cases / 2))))

        self.compute_legal_moves()
        self.Compute_tree()

        # Gestion du click souris pour creer les pièces
        def gestion_clic(evt):

            x1 = floor((evt.x / (self.GUI_size / self.nb_cases))) * self.GUI_size / self.nb_cases  # floor == math.floor
            y1 = floor(evt.y / (self.GUI_size / self.nb_cases)) * self.GUI_size / self.nb_cases
            x2 = (floor(evt.x / (self.GUI_size / self.nb_cases)) + 1) * self.GUI_size / self.nb_cases
            y2 = (floor(evt.y / (self.GUI_size / self.nb_cases)) + 1) * self.GUI_size / self.nb_cases

            if self.joueur == 1:
                # /60 permet de réduire la taille des pions dans l'affichage, subjectif
                if (int(x1 / (self.GUI_size / self.nb_cases)),
                    int(y1 / (self.GUI_size / self.nb_cases))) in self.legal_moves:
                    self.grille.create_oval(x1 + self.GUI_size / 60, y1 + self.GUI_size / 60, x2 - self.GUI_size / 60,
                                            y2 - self.GUI_size / 60, outline='white', fill="white", width=2)
                    self.remove_legal_moves_GUI(int(x1 / (self.GUI_size / self.nb_cases)),
                                                int(y1 / (self.GUI_size / self.nb_cases)))
                    self.flip_pawns(int(x1 / (self.GUI_size / self.nb_cases)),
                                    int(y1 / (self.GUI_size / self.nb_cases)))

                    self.joueur = not (self.joueur)
                    self.compute_legal_moves()

                else:
                    print("Illegal Move")
            else:
                if (int(x1 / (self.GUI_size / self.nb_cases)),
                    int(y1 / (self.GUI_size / self.nb_cases))) in self.legal_moves:
                    self.grille.create_oval(x1 + self.GUI_size / 60, y1 + self.GUI_size / 60, x2 - self.GUI_size / 60,
                                            y2 - self.GUI_size / 60, outline='black', fill="black", width=2)
                    self.remove_legal_moves_GUI(int(x1 / (self.GUI_size / self.nb_cases)),
                                                int(y1 / (self.GUI_size / self.nb_cases)))
                    self.flip_pawns(int(x1 / (self.GUI_size / self.nb_cases)),
                                    int(y1 / (self.GUI_size / self.nb_cases)))

                    self.joueur = not (self.joueur)
                    self.compute_legal_moves()
                else:
                    print("Illegal Move")

            self.Compute_tree()

        self.grille.bind('<Button-1>', gestion_clic)

        root.mainloop()

    def init_Board(self):
        self.Board = Board(board_shape=self.nb_cases)

    def compute_legal_moves(self):
        # dictionnaire qui comprend les moves légaux et leurs conséquences
        self.legal_moves = []
        # Réinitialise le dictionnaire moves/conséquences
        self.pawns_to_flip = {}

        # print("Joueur : ", self.joueur)
        if self.joueur:  # Blanc
            # Check pour tous les pions noirs si une case adjacente permet une prise
            for pawn in self.black_pawns:
                # Dans les cases légales autour du pion noir considéré
                legal_neighbours = self.check_legal_neighbours(pawn)

                self.check_legal_move(pawn, legal_neighbours)

        else:  # Noir
            # Check pour tous les pions blancs si une case adjacente permet une prise
            for pawn in self.white_pawns:
                # Dans les cases libres autour du pion opposé considéré
                legal_neighbours = self.check_legal_neighbours(pawn)

                # On veut que check legal move nous dise : si je pose un pion noir sur un case libre, est-ce que ça fait une prise et si oui quelles conséquences ?
                self.check_legal_move(pawn, legal_neighbours)

        # Affichage en vert des legal_moves
        if self.GUI:
            for move in self.legal_moves:
                self.grille.create_oval(move[0] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                        move[1] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                        (move[0] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                        (move[1] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                        outline='yellow', fill="yellow", width=2)
                # if self.joueur : 
                #     self.grille.create_oval(move[0]*self.GUI_size/self.nb_cases + self.GUI_size/3, move[1]*self.GUI_size/self.nb_cases + self.GUI_size/3 , (move[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/3, (move[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/3, outline = 'white', fill = "white", width = 2)
                # else : 
                #     self.grille.create_oval(move[0]*self.GUI_size/self.nb_cases + self.GUI_size/3, move[1]*self.GUI_size/self.nb_cases + self.GUI_size/3 , (move[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/3, (move[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/3, outline = 'black', fill = "black", width = 2)

    def check_legal_neighbours(self, pawn):

        # Donne la liste des 8 cases autour du pion opposé considéré
        pawn_neighbours = self.compute_pawn_neighbours(pawn)

        legal_neighbours = []
        for neighbour_case in pawn_neighbours:
            # Condition pour ne checker que les cases libres autour du pion considéré
            if neighbour_case not in self.black_pawns and neighbour_case not in self.white_pawns:
                # On check pour les cases libres autour du pion opposé considéré si elles permettent la prise de ce pion
                legal_neighbours.append(neighbour_case)

        # print("pawn :" ,pawn ," neighbours_list : ", pawn_neighbours, "legal_neighbours : ", legal_neighbours)
        return legal_neighbours

    def compute_pawn_neighbours(self, pawn):
        neighbours_list = []

        for x in range(int(pawn[0]) - 1, int(pawn[0]) + 2):
            for y in range(int(pawn[1]) - 1, int(pawn[1]) + 2):
                neighbours_list.append((int(x), int(y)))

        neighbours_list.pop(neighbours_list.index(pawn))

        return neighbours_list

    def check_legal_move(self, pawn_to_check, legal_neighbours):
        # pawn_to_check = pion opposé considéré
        # legal_neighbours = Cases libres voisines du pion opposé

        # Si je met un pion noir sur une des cases libres, est-ce que ça prend au moins 1 pions blanc ?

        if self.joueur == 1:
            # Liste des pions noirs adjacents à la case à check
            pawns_to_check = [pawn for pawn in self.black_pawns if pawn in legal_neighbours]
        else:
            # print("Pions noirs : ", self.black_pawns, "case : ", case, "Voisins de case : ", case_neighbours)
            # Liste des pions blancs adjacents à la case à check
            pawns_to_check = [pawn for pawn in self.white_pawns if pawn in legal_neighbours]

        # print("legal_neighbours to check : ", legal_neighbours)
        # print("Pion : ", case, " pawns_to_check : ", pawns_to_check)
        for free_case in legal_neighbours:
            # déterminer le sens du vecteur entre la case à tester et le pion opposé considéré
            case_x = free_case[0]
            case_y = free_case[1]
            pawn_x = pawn_to_check[0]
            pawn_y = pawn_to_check[1]
            delta_x = pawn_x - case_x
            delta_y = pawn_y - case_y

            # print("Pawn to check : ", pawn_to_check, " Free case : ", free_case, "Delta : ", delta_x,",",delta_y)

            # Nombre de translations depuis la case, commence à 2 puisque 1 est le pions opposé considéré
            step = 2
            # Liste des coordonnées des pions à flip, on ajoute le premier qui n'est pas traité dans la boucle while suivante
            local_pawns_to_flip = [pawn_to_check]
            # A priori on suppose que legal == True, s'il ne l'est pas la valeur sera changée
            legal = True
            # Tant que la position à checker est dans le champs et que l'arrêt n'est pas déclenché
            while case_x + step * delta_x >= 0 and case_x + step * delta_x <= self.nb_cases - 1 and case_y + step * delta_y >= 0 and case_y + step * delta_y <= self.nb_cases - 1:
                coordinates_to_check = (case_x + step * delta_x, case_y + step * delta_y)
                # print("coord_to_check ", coordinates_to_check)
                if self.joueur:  # Joueur Blanc
                    if coordinates_to_check in self.white_pawns:
                        # Si le pion d'après est blanc : critère d'arret (ou break/continue) et ajout à pawn to flip du premier pion
                        x_pawn_to_add = coordinates_to_check[0] - delta_x
                        y_pawn_to_add = coordinates_to_check[1] - delta_y

                        # Si un seul pion entre deux blanc, evite d'ajouter le seul 2 fois
                        if (x_pawn_to_add, y_pawn_to_add) not in local_pawns_to_flip:
                            local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))

                        # On arrête la boucle while
                        break

                    if coordinates_to_check in self.black_pawns:
                        # Si le pion est noir : ajout à pawns_to_flip local et step += 1 et continue
                        x_pawn_to_add = coordinates_to_check[0]
                        y_pawn_to_add = coordinates_to_check[1]

                        # Ajoute le pions aux pions à retourner
                        local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))

                        # On va checker le pion suivant
                        step += 1
                        continue

                    # Si on arrive ici la case est focément vide
                    # print("Hors-cadre : ", coordinates_to_check)
                    legal = False
                    break

                else:  # Joueur Noir
                    if coordinates_to_check in self.black_pawns:
                        # Si le pion d'après est noir : critère d'arret (ou break/continue) et ajout à pawn to flip du premier pion
                        x_pawn_to_add = coordinates_to_check[0] - delta_x
                        y_pawn_to_add = coordinates_to_check[1] - delta_y

                        # Si un seul pion entre deux blanc, evite d'ajouter le seul 2 fois
                        if (x_pawn_to_add, y_pawn_to_add) not in local_pawns_to_flip:
                            local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))

                        # On arrête la boucle while
                        break

                    if coordinates_to_check in self.white_pawns:
                        # Si le pion est noir : ajout à pawns_to_flip local et step += 1 et continue
                        x_pawn_to_add = coordinates_to_check[0]
                        y_pawn_to_add = coordinates_to_check[1]

                        # Ajoute le pions aux pions à retourner
                        local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))

                        # On va checker le pion suivant
                        step += 1
                        continue

                    # Si on arrive ici la case est focément vide
                    # print("Hors-cadre : ", coordinates_to_check)
                    legal = False
                    break
            # Le cas d'une suite de pions d'une même couleur jusqu'à la sortie du cadre ne permet pas de passer legal à False puisqu'on sort du while sans être passé dessus
            # print("Pawn to check : ", pawn_to_check, " Free case : ", free_case, " local_pawns_to_flip", local_pawns_to_flip)
            # Cette condition permet de ne pas avoir à checker à la checker à chaque tour du while et determine si on est sorti parce que pion blanc ou parce que hors cadre
            # if  case_x + step*delta_x < 0 and case_x + step*delta_x > self.nb_cases - 1 and case_y + step*delta_y < 0 and case_y + step*delta_y > self.nb_cases -1 :
            if case_x + step * delta_x < 0 or case_x + step * delta_x > self.nb_cases - 1 or case_y + step * delta_y < 0 or case_y + step * delta_y > self.nb_cases - 1:
                legal = False
                # print("Legal = False  Free_Case : ", free_case)
            # Sorti du while avec legal toujours True <=> Pas de case vide rencontrées

            if legal:
                # print("Legal = True  Free_Case : ", free_case)
                # print("246")
                # On ne veut la position qu'une fois dans cette liste
                if free_case not in self.legal_moves:
                    self.legal_moves.append(free_case)
                # On ajoute au dictionnaire des consequences les pions à retourner si cette position est choisie
                if free_case in list(self.pawns_to_flip.keys()):
                    for local_pawn in local_pawns_to_flip:
                        self.pawns_to_flip[free_case].append(local_pawn)
                else:
                    self.pawns_to_flip.update({free_case: local_pawns_to_flip})
                # Suivre ce vecteur et l'allonger jusqu'à rencontrer une case blanche/noire/vide/hors cadre
                # print("self.pawns_to_flip", self.pawns_to_flip, "\n")

    def remove_legal_moves_GUI(self, x, y):
        # On enleve le move joué de la liste des coup jouables
        self.legal_moves.pop(self.legal_moves.index((x, y)))

        # On remet de la couleur du fond les coups jouables non joués
        for move in self.legal_moves:
            self.grille.create_oval(move[0] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                    move[1] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                    (move[0] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                    (move[1] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60, outline='green',
                                    fill="green", width=2)

    def flip_pawns(self, x, y):
        print("Joueur : ", self.joueur)
        print("Whites : ", self.white_pawns)
        print("Blacks : ", self.black_pawns)
        print("Coup joué : ", (x, y))
        print("Pions à retourner : ", self.pawns_to_flip[(x, y)])

        if self.joueur:
            # On ajoute le pion qui vient d'être placé
            self.white_pawns.append((x, y))
            for pawn in self.pawns_to_flip[(x, y)]:
                # On enlève de la liste des pions opposés chaque pion pris
                self.black_pawns.pop(self.black_pawns.index((pawn[0], pawn[1])))
                # On le rajoute dans la liste des pions similaires
                self.white_pawns.append((pawn[0], pawn[1]))
                # On remplace sa couleur sur la grille
                if self.GUI:  # La condition permet de ne pas créer d'erreur quand on appelle flip_pawns pour la construction de l'arbre
                    self.grille.create_oval(pawn[0] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                            pawn[1] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                            (pawn[0] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                            (pawn[1] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                            outline='white', fill="white", width=2)
        else:
            self.black_pawns.append((x, y))
            for pawn in self.pawns_to_flip[(x, y)]:
                self.white_pawns.pop(self.white_pawns.index((pawn[0], pawn[1])))
                self.black_pawns.append((pawn[0], pawn[1]))
                if self.GUI:  # La condition permet de ne pas créer d'erreur quand on appelle flip_pawns pour la construction de l'arbre
                    self.grille.create_oval(pawn[0] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                            pawn[1] * self.GUI_size / self.nb_cases + self.GUI_size / 60,
                                            (pawn[0] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                            (pawn[1] + 1) * self.GUI_size / self.nb_cases - self.GUI_size / 60,
                                            outline='black', fill="black", width=2)

        # print("(x,y) : ", x, ",", y)
        print("Whites : ", self.white_pawns)
        print("Blacks : ", self.black_pawns)
        print("\n")

    def Compute_tree(self):
        # En gros une suite de compute_legal_moves à partir d'une position initiale
        # On appelle la classe exploration qui va elle même s'appeler elle-même, normalement on retourne dans la classe game l'arbre finalement construit par la premiere classe exploration fille de game et parente de toutes les autres
        self.tree = {}
        self.x = Exploration(self.white_pawns, self.black_pawns, self.legal_moves, self.pawns_to_flip, self.nb_cases,
                             self.GUI_size, method="MinMax", initial_player=self.joueur,
                             exploration_depth=self.exploration_depth)
        self.tree.update({"legal_moves": self.x.tree,
                          "white_pawns": self.white_pawns,
                          # On veut les listes de noirs/blancs après que le coup a été joué
                          "black_pawns": self.black_pawns,
                          "player_turn": self.joueur})  # On définit le joueur pour un étage comme le joueur de qui ça va être le tour de jouer à partir de cette position

        print(self.tree)

        ####Il faudra supprimer tous les objets créés après avoir obtenu l'arbre, selon la profondeur ça pourra devenir conséquent en mémoire
        ####Il faudra architecturer pour qu'à chaque coup il ne recalcule que la profondeur d et pas tout l'arbre



# class Board() :
#     def __init__(self, board_shape = 8) : 
#         #Initialisation de la grille
#         self.board_shape = board_shape
#         self.grid = np.zeros((self.board_shape,self.board_shape), dtype = "str")

#         #Positionnement des premiers pions
#         mid_grid = int(self.board_shape/2) - 1
#         self.grid[mid_grid , mid_grid] = "0"
#         self.grid[mid_grid , mid_grid + 1] = "O"
#         self.grid[mid_grid + 1,mid_grid] = "O"
#         self.grid[mid_grid + 1,mid_grid + 1] = "0"

#         #Initialisation du dictionnaire d'historique --> Meilleur système de logging ? 
#         self.logs = {}


class Exploration(Game):
    def __init__(self, white_pawns, black_pawns, legal_moves, pawns_to_flip, nb_cases, GUI_size, exploration_depth,
                 method="", initial_player=0):
        self.init_pawns_to_flip = pawns_to_flip
        self.initial_white_pawns = white_pawns
        self.initial_black_pawns = black_pawns

        self.method = method  # method = MCTS, MinMax, AlphaBeta
        self.initial_joueur = initial_player

        self.init_legal_moves = legal_moves

        self.exploration_depth = exploration_depth
        self.nb_cases = nb_cases
        self.GUI_size = GUI_size
        self.GUI = False
        self.tree = {}
        self.method_IA = 'MinMax'  # 'MinMax', 'AlphaBeta' ou 'UCB1'
        # method_IA à passer dans Game puis comme argument dans compute_tree
        self.val_array = np.loadtxt('pos_value.txt', usecols=range(8))
        self.val_position = 0

        self.Compute_tree()

    def eval_position(self, position):
        # print("position : ", position)
        self.val_position = sum([self.val_array[pos] for pos in position])

    def Compute_tree(self):
        for move in self.init_legal_moves:  # Pour tous les coups possibles pour joueur à une profondeur donnée
            print("Profondeur : ", self.exploration_depth, " Move : ", move, "ID_classe : ", id(self))

            # On réinitialise les listes de pions qui vont être manipulées par self.flip_pawns à la position initiale pour tous les coups légaux
            self.white_pawns = list(
                self.initial_white_pawns)  # Comme la fonction flip_pawns manipule ces listes, à chaque coup joué pour une liste de coup les listes s'aggrégeraient
            self.black_pawns = list(
                self.initial_black_pawns)  # On en crée deux vide qu'on réinitialisera aux listes initiales à chaque passe de flip_pawns
            self.pawns_to_flip = self.init_pawns_to_flip
            self.legal_moves = list(self.init_legal_moves)
            self.joueur = self.initial_joueur
            print(id(self.pawns_to_flip), id(self.init_pawns_to_flip))

            x = move[0]
            y = move[1]
            self.flip_pawns(x, y)  # On joue un des coups possibles pour le joueur i
            self.joueur = not (self.initial_joueur)
            self.compute_legal_moves()  # On recalcule les coups légaux pour le joueur i+1 après qu'on ait joué le coup pour le joueur i

            if self.exploration_depth - 1 > 0:
                # On initialise la classe enfant avec les blancs/noirs après le coup du joueur i, avec les moves légaux et les conséquences rattachées pour le joueur i+1
                child_i = Exploration(self.white_pawns, self.black_pawns, self.legal_moves, self.pawns_to_flip,
                                      self.nb_cases, self.GUI_size, exploration_depth=self.exploration_depth - 1,
                                      method=self.method, initial_player=self.joueur)
                self.tree.update({str(move): {"legal_moves": child_i.tree,
                                              "white_pawns": self.white_pawns,
                                              # On veut les listes de noirs/blancs après que le coup ait été joué
                                              "black_pawns": self.black_pawns,
                                              "player_turn": self.joueur}})  # On définit le joueur pour un étage comme le joueur de qui ça va être le tour de jouer à partir de cette position

            else:
                # On est à la profondeur max et on ne veut pas recréer une classe Exploration
                # self.compute_legal_moves()
                # for move in self.legal_moves :
                # x = move[0]
                # y = move[1]

                # self.flip_pawns(x, y) #On joue un des coups possibles
                # self.joueur = not(self.initial_joueur)
                # self.compute_legal_moves() #On recalcule les coups légaux après qu'on ait joué le coup
                print("Fin d'arbre pour move : ", move, "\n")
                print("pions blancs : ", type(self.white_pawns))
                if self.joueur == False:  # joueur noir
                    self.eval_position(self.white_pawns)
                else:
                    self.eval_position(self.black_pawns)
                self.tree.update({str(move): {"legal_moves": self.legal_moves,
                                              "white_pawns": self.white_pawns,
                                              "black_pawns": self.black_pawns,
                                              "player_turn": not (
                                                  self.joueur),
                                              "val_position": self.val_position}})  # On définit une branche de l'arbre correspondant

G = Game(gametype="H-H",
         nb_cases=8,
         GUI=True,
         GUI_size=800,
         exploration_depth=2)
# A = Board()
