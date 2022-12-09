# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:02:16 2022

@author: prje
"""

import numpy as np
from tkinter import *
from tkinter import ttk
from math import floor, inf
from random import choice
from Tree_class import *


class Game:
    def __init__(self, nb_tiles=8, GUI=True, GUI_size=800, exploration_depth=5, game_mode='PvP',
                 start_position='default', IA_mode=('random', 'random'), C=2, mcts_simul=100, mcts_iter=10):
        self.root = None
        self.nb_tiles = nb_tiles
        self.GUI_size = GUI_size
        self.tile_size = int(self.GUI_size / self.nb_tiles)
        self.offset = 0.1
        self.GUI = GUI

        self.player = False

        self.white_pawns = []
        self.black_pawns = []
        self.position = np.zeros((8, 8))
        self.winner = None
        self.start_position = start_position
        self.exploration_depth = exploration_depth
        self.C = C
        self.mcts_simul = mcts_simul
        self.mcts_iter = mcts_iter
        self.val_array = np.loadtxt('pos_value.txt', usecols=range(8))
        self.while_eval = False
        self.turn_pass = 0
        self.is_over = False
        self.human_turn = True
        self.game_mode = game_mode  # 'PvP' // 'PvIA' // 'IAvIA'
        self.IA_mode = IA_mode
        if game_mode in ('PvP', 'PvIA'):
            self.GUI = True

    def start_game(self):
        if self.GUI:
            self.init_GUI()
        self.init_game()
        self.start_playing()
        if self.root:
            self.root.mainloop()

    def init_GUI(self):
        # Initialisation de la grille (manque les numero et lettre sur les côtés)
        self.root = Tk()
        self.grille = Canvas(self.root, width=self.GUI_size, height=self.GUI_size, background="green")
        self.grille.pack(side=LEFT)
        for i in range(self.nb_tiles):
            self.grille.create_line(self.tile_size * (i + 1), 0,
                                    self.tile_size * (i + 1), self.GUI_size, fill='white', width=2)
            self.grille.create_line(0, self.tile_size * (i + 1), self.GUI_size,
                                    self.tile_size * (i + 1), fill='white', width=2)

        # Gestion du click souris pour creer les pièces
        self.grille.bind('<Button-1>', self.gestion_clic)

    def init_game(self):
        if self.start_position == 'default':
            for row in [int((self.nb_tiles / 2) - 1), int((self.nb_tiles / 2))]:
                for col in [int((self.nb_tiles / 2) - 1), int((self.nb_tiles / 2))]:
                    if row == col:
                        color = 'white'
                        self.white_pawns.append((row, col))
                        self.position[(row, col)] = 1
                    else:
                        color = 'black'
                        self.black_pawns.append((row, col))
                        self.position[(row, col)] = -1
                    if self.GUI:
                        self.update_board((row, col), color)
        else:
            # self.position = self.position.transpose()
            for w_pawn in self.start_position[1]:  # Pions noirs à placer au départ
                self.white_pawns.append(w_pawn)
                self.position[w_pawn] = 1
                if self.GUI:
                    self.update_board(w_pawn, 'white')
            for b_pawn in self.start_position[0]:  # Pions noirs à placer au départ
                self.black_pawns.append(b_pawn)
                self.position[b_pawn] = -1
                if self.GUI:
                    self.update_board(b_pawn, 'black')
            self.player = self.start_position[2]
            # self.position = self.position.transpose()

    def start_playing(self):
        self.compute_legal_moves()

        if self.check_pass():  # Pas de coup jouable donc on passe le tour
            # check_pass rechange de joueur et recalcule les coups légaux
            # si après le coup de l'IA il n'y a pas de coups légaux, l'IA rejoue forcément
            if self.check_end():  # Le joueur peut rejouer donc la partie ne s'arrête pas
                self.compute_winner()  # self.player = not self.player
                # self.compute_legal_moves()
            else:
                self.IA_play()
                ##print(self.position.transpose())
        else:  # si on ne passe pas le tour
            if self.game_mode == 'IAvIA':
                self.human_turn = False
                self.IA_play()
        # if self.game_mode == 'IAvIA':
        #
        #     self.human_turn = False
        #     self.IA_play()

    def gestion_clic(self, evt):
        if not self.is_over:
            # print(self.player)
            if self.human_turn:
                x = floor(evt.x / self.tile_size)  # * self.tile_size  # floor == math.floor
                y = floor(evt.y / self.tile_size)  # * self.tile_size

                if (x, y) in self.legal_moves:
                    if self.player:  # Au tour des blancs
                        color = 'white'
                        self.position[(x, y)] = 1
                    else:
                        color = 'black'
                        self.position[(x, y)] = -1
                    self.update_board((x, y), color)
                    self.remove_legal_moves_GUI(x, y)
                    self.flip_pawns(x, y)
                    self.player = not self.player
                    self.compute_legal_moves()
                    if not self.check_pass():  # Le joueur suivant ne passe pas
                        if self.game_mode == 'PvIA':  # En PvIA, c'est donc au tour de l'IA
                            self.human_turn = False
                            self.IA_play()
                        elif self.game_mode == 'PvP':  # En PvP c'est au tour de l'humain (mais le joueur suivant)
                            self.human_turn = True
                    else:  # Pas de coup jouable donc on passe le tour
                        # check_pass rechange de joueur et recalcule les coups légaux
                        # ici, c'est encore au tour du joueur humain
                        self.human_turn = True
                        if self.check_end():
                            self.compute_winner()
                            # print(self.position.transpose())
                else:
                    print("Illegal Move")
            else:
                print("Not Player's turn")
        else:
            print('GAME OVER')

    def update_board(self, move, color):
        if not self.while_eval:
            x, y = move
            self.grille.create_oval(self.tile_size * (x + self.offset),
                                    self.tile_size * (y + self.offset),
                                    self.tile_size * ((x + 1) - self.offset),
                                    self.tile_size * ((y + 1) - self.offset),
                                    outline=color, fill=color, width=2)

    def check_pass(self):
        if not self.legal_moves:  # le joueur passe si aucun n'est jouable
            ##print('turn_pass')
            self.player = not self.player  # on change de joueur = on revient au joueur qui vient de jouer
            self.compute_legal_moves()
            return True
        return False

    def check_end(self):  # n'est appelé que si check_pass est vrai
        # si les 2 joueurs passent leur tour, la partie est finie
        if not self.legal_moves:  # le joueur passe si aucun n'est jouable
            self.is_over = True
            ##print('is_over: ', self.is_over)
            return True
        return False

    def compute_legal_moves(self):
        # dictionnaire qui comprend les moves légaux et leurs conséquences
        self.legal_moves = []
        # Réinitialise le dictionnaire moves/conséquences
        self.pawns_to_flip = {}

        if self.player:  # Blanc
            # Check pour tous les pions noirs si une case adjacente permet une prise
            for pawn in self.black_pawns:
                # Dans les tiles légales autour du pion noir considéré
                legal_neighbours = self.check_legal_neighbours(pawn)

                self.check_legal_move(pawn, legal_neighbours)

        else:  # Noir
            # Check pour tous les pions blancs si une case adjacente permet une prise
            for pawn in self.white_pawns:
                # Dans les tiles libres autour du pion opposé considéré
                legal_neighbours = self.check_legal_neighbours(pawn)

                # On veut que check legal move nous dise : si je pose un pion noir sur un case libre, est-ce que ça fait une prise et si oui quelles conséquences ?
                self.check_legal_move(pawn, legal_neighbours)

        # Affichage en vert des legal_moves
        if self.GUI:
            for move in self.legal_moves:
                self.update_board(move, 'yellow')
                # if self.player : 
                #     self.grille.create_oval(move[0]*self.GUI_size/self.nb_tiles + self.GUI_size/3, move[1]*self.GUI_size/self.nb_tiles + self.GUI_size/3 , (move[0]+1)*self.GUI_size/self.nb_tiles - self.GUI_size/3, (move[1]+1)*self.GUI_size/self.nb_tiles - self.GUI_size/3, outline = 'white', fill = "white", width = 2)
                # else : 
                #     self.grille.create_oval(move[0]*self.GUI_size/self.nb_tiles + self.GUI_size/3, move[1]*self.GUI_size/self.nb_tiles + self.GUI_size/3 , (move[0]+1)*self.GUI_size/self.nb_tiles - self.GUI_size/3, (move[1]+1)*self.GUI_size/self.nb_tiles - self.GUI_size/3, outline = 'black', fill = "black", width = 2)

    def check_legal_neighbours(self, pawn):

        # Donne la liste des 8 tiles autour du pion opposé considéré
        pawn_neighbours = self.compute_pawn_neighbours(pawn)

        legal_neighbours = []
        for neighbour_case in pawn_neighbours:
            # Condition pour ne checker que les tiles libres autour du pion considéré
            if neighbour_case not in self.black_pawns and neighbour_case not in self.white_pawns:
                # On check pour les tiles libres autour du pion opposé considéré si elles permettent la prise de ce pion
                legal_neighbours.append(neighbour_case)

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
        # legal_neighbours = tiles libres voisines du pion opposé

        # Si je met un pion noir sur une des tiles libres, est-ce que ça prend au moins 1 pions blanc ?

        if self.player == 1:
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
            while case_x + step * delta_x >= 0 and case_x + step * delta_x <= self.nb_tiles - 1 and case_y + step * delta_y >= 0 and case_y + step * delta_y <= self.nb_tiles - 1:
                coordinates_to_check = (case_x + step * delta_x, case_y + step * delta_y)
                # print("coord_to_check ", coordinates_to_check)
                if self.player:  # Joueur Blanc
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
            # if  case_x + step*delta_x < 0 and case_x + step*delta_x > self.nb_tiles - 1 and case_y + step*delta_y < 0 and case_y + step*delta_y > self.nb_tiles -1 :
            if case_x + step * delta_x < 0 or case_x + step * delta_x > self.nb_tiles - 1 or case_y + step * delta_y < 0 or case_y + step * delta_y > self.nb_tiles - 1:
                legal = False
                # print("Legal = False  Free_Case : ", free_case)
            # Sorti du while avec legal toujours True <=> Pas de case vide rencontrées

            if legal:
                # print("Legal = True  Free_Case : ", free_case)
                # print("246")
                # On ne veut la position qu'une fois dans cette liste
                if free_case not in self.legal_moves and self.nb_tiles not in free_case and free_case[0] >= 0 and \
                        free_case[1] >= 0:
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
        # On enlève le move joué de la liste des coups jouables
        self.legal_moves.pop(self.legal_moves.index((x, y)))
        # On remet de la couleur du fond les coups jouables non joués
        if self.GUI:
            for move in self.legal_moves:
                self.update_board(move, 'green')

    def flip_pawns(self, x, y):
        # print("Joueur : ", ['Noir', 'Blanc'][self.player])  # Affiche Noir si joueur est False (cad ==0) et Blanc sinon
        # print("Whites : ", self.white_pawns)
        # print("Blacks : ", self.black_pawns)
        # print("Coup joué : ", (x, y))
        # print("Pions à retourner : ", self.pawns_to_flip[(x, y)])

        if self.player:
            # On ajoute le pion qui vient d'être placé
            self.white_pawns.append((x, y))
            self.position[(x, y)] = 1
            for pawn in self.pawns_to_flip[(x, y)]:
                # On enlève de la liste des pions opposés chaque pion pris
                self.black_pawns.pop(self.black_pawns.index((pawn[0], pawn[1])))
                # On le rajoute dans la liste des pions similaires
                self.white_pawns.append((pawn[0], pawn[1]))
                self.position[(pawn)] = 1
                # On remplace sa couleur sur la grille
                if self.GUI:  # La condition permet de ne pas créer d'erreur quand on appelle flip_pawns pour la construction de l'arbre
                    self.update_board(pawn, 'white')

        else:
            self.black_pawns.append((x, y))
            self.position[(x, y)] = -1
            for pawn in self.pawns_to_flip[(x, y)]:
                self.white_pawns.pop(self.white_pawns.index((pawn[0], pawn[1])))
                self.black_pawns.append((pawn[0], pawn[1]))
                self.position[pawn] = -1
                if self.GUI:  # La condition permet de ne pas créer d'erreur quand on appelle flip_pawns pour la construction de l'arbre
                    self.update_board(pawn, 'black')

    def IA_play(self):
        # print('IA_play :', self.legal_moves)
        if not self.is_over:
            # print(self.player)
            move = self.IA_chose_move()  # par défaut l'IA choisit le 1er coup
            if not self.player:  # au tour des noirs
                color = 'black'
                self.position[move] = -1
            else:
                color = 'white'
                self.position[move] = 1
            if self.GUI:
                self.update_board(move, color)
            self.remove_legal_moves_GUI(move[0], move[1])
            self.flip_pawns(move[0], move[1])

            self.player = not self.player  # on change de joueur
            self.compute_legal_moves()
            if self.check_pass():  # Pas de coup jouable donc on passe le tour
                # check_pass rechange de joueur et recalcule les coups légaux
                # si après le coup de l'IA il n'y a pas de coups légaux, l'IA rejoue forcément
                if self.check_end():  # Le joueur peut rejouer donc la partie ne s'arrête pas
                    self.compute_winner()  # self.player = not self.player
                    # self.compute_legal_moves()
                else:
                    self.IA_play()
                    ##print(self.position.transpose())
            else:  # si on ne passe pas le tour
                if self.game_mode == 'IAvIA':
                    self.IA_play()
                else:  # ceci n'est appelé que si 'PvIA' ou 'IAvIA' donc ce cas est 'PvIA'
                    self.human_turn = True
            # print(self.position.transpose())
            # print(self.tree)

    def IA_chose_move(self):
        # init_player = self.player
        # init_legal_moves = self.legal_moves.copy()
        self.eval_position()
        # if self.player != init_player:
        #     self.player = init_player
        #     self.legal_moves = init_legal_moves
        tree_root = TreeNode(self.legal_moves.copy(), self.white_pawns.copy(), self.black_pawns.copy(),
                             self.pawns_to_flip.copy(), self.player, np.array(self.position), self.val_position)

        if self.player:  # le joueur blanc choisit son coup
            if self.IA_mode[0] == 'minmax':  # les blancs jouent en minmax
                id_best_move = self.MinMax(depth=self.exploration_depth, tree_parent=tree_root)
                move = self.legal_moves[id_best_move]
            elif self.IA_mode[0] == 'alphabeta':
                id_best_move = self.AlphaBeta(depth=self.exploration_depth, tree_parent=tree_root)
                # print(id_best_move)
                move = self.legal_moves[id_best_move]
                # print(self.player, move)
            elif self.IA_mode[0] == 'MCTS':
                id_best_move = self.MCTS(tree_root, C=self.C, n_simul=self.mcts_simul, n_iter=self.mcts_iter)
                move = self.legal_moves[id_best_move]
            elif self.IA_mode[0] == 'random':
                move = choice(self.legal_moves)

        else:  # le joueur noir choisit un coup
            if self.IA_mode[1] == 'minmax':  # les blancs jouent en minmax
                id_best_move = self.MinMax(depth=self.exploration_depth, tree_parent=tree_root)
                move = self.legal_moves[id_best_move]
            elif self.IA_mode[1] == 'alphabeta':
                id_best_move = self.AlphaBeta(depth=self.exploration_depth, tree_parent=tree_root)
                # print(id_best_move)
                move = self.legal_moves[id_best_move]
                # print(self.player, move)
            elif self.IA_mode[1] == 'MCTS':
                id_best_move = self.MCTS(tree_root, C=self.C, n_simul=self.mcts_simul, n_iter=self.mcts_iter)
                move = self.legal_moves[id_best_move]
            elif self.IA_mode[1] == 'random':
                move = choice(self.legal_moves)
        # print(self.player, move)
        # print(self.player, move)
        return move

    def compute_winner(self):
        if self.position.sum() > 0:  # Plus de pions blancs que noirs donc les blancs gagnent
            self.winner = 'Blanc'
            ##print('Les blancs gagnent')
        elif self.position.sum() < 0:
            self.winner = 'Noir'
            ##print('Les noirs gagnent')
        else:
            # print('Draw')
            pass

    def init_param(self, tree):
        self.white_pawns = tree.white_pawns.copy()
        self.black_pawns = tree.black_pawns.copy()
        self.pawns_to_flip = tree.pawns_to_flip.copy()
        self.legal_moves = tree.legal_moves.copy()
        self.player = tree.player
        self.position = np.array(tree.position)

    def MinMax(self, depth, tree_parent):
        self.while_eval = True

        if depth == 0:  # on est sur un noeud feuille
            self.eval_position()
            return self.val_position

        if self.check_pass():  # check_pass rechange le joueur et relance compute_legal_moves
            if self.check_end():  # la partie est finie
                self.compute_winner()
                self.is_over = False  # Pour ne pas arrêter la partie
                if self.winner == 'Blanc':
                    return 2000
                elif self.winner == 'Noir':
                    return -2000
                else:
                    return 0  # Egalité : on évalue la position à 0

        if depth > 0:
            for move in tree_parent.legal_moves.copy():
                self.init_param(tree_parent)
                if not self.check_pass():
                    x, y = move
                    self.flip_pawns(x, y)
                    self.player = not tree_parent.player
                    self.compute_legal_moves()
                self.eval_position()
                tree_child = TreeNode(self.legal_moves.copy(), self.white_pawns.copy(), self.black_pawns.copy(),
                                      self.pawns_to_flip.copy(), self.player, np.array(self.position),
                                      self.val_position)
                tree_child.add_parent(tree_parent)
                tree_parent.children_val.append(self.MinMax(depth=depth - 1, tree_parent=tree_child))

            if tree_parent.parent is None:
                self.while_eval = False
                self.init_param(tree_parent)
                if tree_parent.player:  # les blancs commencent
                    return np.argmax(tree_parent.children_val)
                else:
                    return np.argmin(tree_parent.children_val)

            if tree_parent.player:  # les blancs jouent
                return max(tree_parent.children_val)
            else:
                return min(tree_parent.children_val)

    def AlphaBeta(self, depth, tree_parent):
        self.while_eval = True

        if depth == 0:  # on est sur un noeud feuille
            self.eval_position()
            return self.val_position

        if self.check_pass():  # check_pass rechange le joueur et relance compute_legal_moves
            if self.check_end():  # la partie est finie
                self.compute_winner()
                self.is_over = False  # Pour ne pas arrêter la partie
                if self.winner == 'Blanc':
                    return 2000
                elif self.winner == 'Noir':
                    return -2000
                else:
                    return 0  # Egalité : on évalue la position à 0

        if depth > 0:
            for move in tree_parent.legal_moves.copy():
                self.init_param(tree_parent)
                # print(self.player)
                if not self.check_pass():
                    x, y = move
                    self.flip_pawns(x, y)
                    # print(tree_root.player)
                    # print(self.player)
                    self.player = not tree_parent.player
                    self.compute_legal_moves()
                self.eval_position()
                tree_child = TreeNode(self.legal_moves.copy(), self.white_pawns.copy(), self.black_pawns.copy(),
                                      self.pawns_to_flip.copy(), self.player, np.array(self.position),
                                      self.val_position, tree_parent.alpha, tree_parent.beta)
                tree_child.add_parent(tree_parent)
                children_val = self.AlphaBeta(depth=depth - 1, tree_parent=tree_child)
                tree_parent.children_val.append(children_val)
                if tree_parent.player:  # parent joue blanc donc remonte le max des alpha
                    tree_parent.alpha = max(tree_parent.alpha, children_val)
                    if tree_parent.alpha >= tree_parent.beta and tree_parent.parent is not None:
                        return tree_parent.alpha
                else:
                    tree_parent.beta = min(tree_parent.beta, children_val)
                    if tree_parent.alpha >= tree_parent.beta and tree_parent.parent is not None:
                        return tree_parent.beta

            if tree_parent.parent is None:
                self.while_eval = False
                self.init_param(tree_parent)
                # print('is over:', self.is_over)
                if tree_parent.player:  # les blancs commencent
                    # print(np.argmax(tree_parent.children_val))
                    return np.argmax(tree_parent.children_val)
                else:
                    # print(np.argmin(tree_parent.children_val))
                    return np.argmin(tree_parent.children_val)
            elif tree_parent.player:
                return tree_parent.alpha
            else:
                return tree_parent.beta

    def MCTS(self, tree_root, C=2, n_simul=100, n_iter=10):
        """
        :type tree_parent: TreeNode
        """
        self.while_eval = True
        cpt = 0
        for _ in range(n_iter):
            # print('iteration :', cpt)
            current_node = tree_root
        # 1 : Tree traversal
            while current_node.children or current_node == tree_root:
                # is current not a leaf node
                # or the start node
                if current_node == tree_root and not current_node.children:
                    # on est sur le noeud racine mais on n'a pas encore développé les noeuds fils
                    break
                current_node = current_node.tree_traversal(C)
        # 2 : Node Expansion
            if current_node.nb_trial != 0:
                if current_node.legal_moves:  # Il y a des coups jouables à partir de la position
                    for move in current_node.legal_moves:
                        self.init_param(current_node)
                        x, y = move
                        self.flip_pawns(x, y)
                        self.player = not current_node.player
                        self.compute_legal_moves()
                        # self.eval_position()
                        tree_child = TreeNode(self.legal_moves.copy(), self.white_pawns.copy(), self.black_pawns.copy(),
                                              self.pawns_to_flip.copy(), self.player, np.array(self.position),
                                              self.val_position)
                        current_node.add_child(tree_child)
                    current_node = current_node.children[0]
                else:  # Il n'y a pas de coup jouable à partir de la position
                    if self.check_pass():
                        if self.check_end():  # Si la partie est finie on ne fait rien
                            self.is_over = False
                        else:  # Si la partie n'est pas finie, le noeud suivant est la même position pour l'adversaire
                            tree_child = TreeNode(self.legal_moves.copy(), self.white_pawns.copy(),
                                                  self.black_pawns.copy(),
                                                  self.pawns_to_flip.copy(), self.player, np.array(self.position),
                                                  self.val_position)
                            current_node.add_child(tree_child)
                            current_node = tree_child
        # 3 : Rollout
            l_score = [0, 0]
            self.init_param(current_node)
            for k in range(n_iter):  # on va simuler n_iter parties et compter le nombre de victoires
                start_position = [self.black_pawns.copy(), self.white_pawns.copy(), self.player]
                # noinspection PyTypeChecker
                G = Game(nb_tiles=self.nb_tiles, GUI=False, GUI_size=self.GUI_size,
                         exploration_depth=self.exploration_depth, game_mode=self.game_mode,
                         start_position=start_position)
                G.init_game()
                G.start_playing()
                if G.winner == 'Blanc':
                    l_score[1] += 1
                elif G.winner == 'Noir':
                    l_score[0] += 1
                self.init_param(current_node)
            score = l_score[self.player]  # 1er élément si joueur noir a commencé, 2ème sinon
            current_node.mcts_score += score/n_iter
            current_node.nb_trial += 1
        # 4 : Backpropagation
            while current_node.parent is not None:
                current_node = current_node.parent
                current_node.mcts_score += score
                current_node.nb_trial += 1
            cpt += 1
        l_val = [tree_child.mcts_score for tree_child in tree_root.children]
        self.while_eval = False
        self.init_param(tree_root)
        return l_val.index(min(l_val))


    def eval_position(self):
        # print("position : ", position)
        # print(self.val_array)
        # print(self.position.transpose())
        # print(self.val_array*self.position.transpose())
        if not self.white_pawns:  # il n'y a plus de pions blancs
            self.val_position = -2000  # valeur arbitraire très grande en valeur absolue pour victoire ou défaite
            # si val_position = inf cela cause des problèmes avec le inf du alpha beta à l'initialisation
        elif not self.black_pawns:
            self.val_position = 2000
        elif self.check_pass():
            if self.check_end():
                self.compute_winner()
                self.is_over = False
                if self.winner == 'Blanc':
                    self.val_position = 2000
                elif self.winner == 'Noir':
                    self.val_position = -2000
                else:
                    self.val_position = 0
            else:
                # self.player = not self.player  # on retourne au joueur d'avant
                self.val_position = (self.val_array * self.position).sum()
            # self.player = not self.player
            # self.compute_legal_moves()
        else:
            self.val_position = (self.val_array * self.position).sum()


def play_game(nb_tiles=8, GUI=True, GUI_size=800, exploration_depth=2, game_mode='IAvIA'):
    G = Game(nb_tiles=nb_tiles, GUI=GUI, GUI_size=GUI_size, exploration_depth=exploration_depth, game_mode=game_mode)
    return G.winner == 'Blanc'


if __name__ == '__main__':
    print(play_game())
