# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:02:16 2022

@author: prje
"""

import numpy as np
from tkinter import * 
from tkinter import ttk
from math import floor


class Game() : 
    def __init__(self, gametype = "H-H", nb_cases = 8, GUI = True, GUI_size = 800) : 
        #Gametype = "H-H", "H-IA", "IA-IA"
        self.nb_cases = nb_cases
        self.GUI_size= GUI_size
        
        self.joueur = False
        
        self.init_Board
        
        self.white_pawns = []
        self.black_pawns = []
        
        self.is_over = False
        
        if GUI : 
            self.init_GUI()
            
        
        
        
        
    
    def init_GUI(self) : 

        #Initialisation de la grille (manque les numero et lettre sur les côtés)
        root = Tk()
        self.grille = Canvas(root, width = self.GUI_size, height = self.GUI_size, background="green")
        self.grille.pack(side=LEFT)
        for i in range(self.nb_cases) :
            self.grille.create_line((self.GUI_size/self.nb_cases)*(i+1) , 0 , (self.GUI_size/self.nb_cases)*(i+1) , self.GUI_size , fill = 'white', width = 2)
            self.grille.create_line(0 , (self.GUI_size/self.nb_cases)*(i+1) , self.GUI_size , (self.GUI_size/self.nb_cases)*(i+1) , fill = 'white', width = 2)
            
        #Haut gauche 
        self.grille.create_oval(((self.nb_cases/2)-1)*self.GUI_size/self.nb_cases + self.GUI_size/60, ((self.nb_cases/2)-1)*self.GUI_size/self.nb_cases + self.GUI_size/60 , (self.nb_cases/2)*self.GUI_size/self.nb_cases - self.GUI_size/60, (self.nb_cases/2)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'white', fill = "white", width = 2)
        self.white_pawns.append(((int((self.nb_cases/2)-1)),int((self.nb_cases/2)-1)))
        #Haut droit
        self.grille.create_oval((self.nb_cases/2)*self.GUI_size/self.nb_cases + self.GUI_size/60, ((self.nb_cases/2)-1)*self.GUI_size/self.nb_cases + self.GUI_size/60 , ((self.nb_cases/2)+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, (self.nb_cases/2)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'black', fill = "black", width = 2)
        self.black_pawns.append((int((self.nb_cases/2)),int((self.nb_cases/2)-1)))
        #Bas Gauche
        self.grille.create_oval(((self.nb_cases/2)-1)*self.GUI_size/self.nb_cases + self.GUI_size/60, (self.nb_cases/2)*self.GUI_size/self.nb_cases + self.GUI_size/60 , (self.nb_cases/2)*self.GUI_size/self.nb_cases - self.GUI_size/60, ((self.nb_cases/2)+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'black', fill = "black", width = 2)
        self.black_pawns.append(((int((self.nb_cases/2)-1)),int((self.nb_cases/2))))
        #Bas droit
        self.grille.create_oval((self.nb_cases/2)*self.GUI_size/self.nb_cases + self.GUI_size/60, (self.nb_cases/2)*self.GUI_size/self.nb_cases + self.GUI_size/60 , ((self.nb_cases/2)+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, ((self.nb_cases/2)+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'white', fill = "white", width = 2)
        self.white_pawns.append((int((self.nb_cases/2)),int((self.nb_cases/2))))
        
        self.compute_legal_moves()
        
        #Gestion du click souris pour creer les pièces
        def gestion_clic(evt) :
            
            x1 = floor((evt.x/(self.GUI_size/self.nb_cases)))*self.GUI_size/self.nb_cases #floor == math.floor
            y1 = floor(evt.y/(self.GUI_size/self.nb_cases))*self.GUI_size/self.nb_cases
            x2 = (floor(evt.x/(self.GUI_size/self.nb_cases))+1)*self.GUI_size/self.nb_cases
            y2 = (floor(evt.y/(self.GUI_size/self.nb_cases))+1)*self.GUI_size/self.nb_cases
            
            if self.joueur == 1 : 
                #/60 permet de réduire la taille des pions dans l'affichage, subjectif
                if (int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases))) in self.legal_moves :
                    self.grille.create_oval(x1 + self.GUI_size/60, y1 + self.GUI_size/60 , x2 - self.GUI_size/60, y2 - self.GUI_size/60, outline = 'white', fill = "white", width = 2)
                    self.remove_legal_moves_GUI(int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases)))
                    self.flip_pawns(int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases)))
                    
                    self.joueur = not(self.joueur)
                    self.compute_legal_moves()
                    
                else : 
                    print("Illegal Move")
            else :
                if (int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases))) in self.legal_moves :
                    self.grille.create_oval(x1 + self.GUI_size/60, y1 + self.GUI_size/60 , x2 - self.GUI_size/60, y2 - self.GUI_size/60, outline = 'black', fill = "black", width = 2)
                    self.remove_legal_moves_GUI(int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases)))
                    self.flip_pawns(int(x1/(self.GUI_size/self.nb_cases)),int(y1/(self.GUI_size/self.nb_cases)))
                    
                    self.joueur = not(self.joueur)
                    self.compute_legal_moves()
                else : 
                    print("Illegal Move")
            
            
        
                
           

        self.grille.bind('<Button-1>' , gestion_clic)

        root.mainloop()
        
    def init_Board(self) : 
        self.Board = Board(board_shape=self.nb_cases)
    
    def compute_legal_moves(self) : 
        #dictionnaire qui comprend les moves légaux et leurs conséquences
        self.legal_moves = []
        #Réinitialise le dictionnaire moves/conséquences
        self.pawns_to_flip = {}
        
        print("Joueur : ", self.joueur)
        if self.joueur : #Blanc
            #Check pour tous les pions noirs si une case adjacente permet une prise
            for pawn in self.black_pawns : 
                #Dans les cases légales autour du pion noir considéré
                legal_neighbours = self.check_legal_neighbours(pawn)
                
                self.check_legal_move(pawn, legal_neighbours)
                    
        else : #Noir
            #Check pour tous les pions blancs si une case adjacente permet une prise
            for pawn in self.white_pawns : 
                #Dans les cases libres autour du pion opposé considéré
                legal_neighbours = self.check_legal_neighbours(pawn)
                
                #On veut que check legal move nous dise : si je pose un pion noir sur un case libre, est-ce que ça fait une prise et si oui quelles conséquences ?
                self.check_legal_move(pawn, legal_neighbours)

        #print("legal_moves : ", self.legal_moves)
        #print("pawns_to_flip : ", self.pawns_to_flip)
        #Affichage en vert des legal_moves
        for move in self.legal_moves :
            self.grille.create_oval(move[0]*self.GUI_size/self.nb_cases + self.GUI_size/60, move[1]*self.GUI_size/self.nb_cases + self.GUI_size/60 , (move[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, (move[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'yellow', fill = "yellow", width = 2)
            
    def check_legal_neighbours(self, pawn) : 
        
        #Donne la liste des 8 cases autour du pion opposé considéré
        pawn_neighbours = self.compute_pawn_neighbours(pawn)
        
        legal_neighbours = []
        for neighbour_case in pawn_neighbours : 
            #Condition pour ne checker que les cases libres autour du pion considéré
            if neighbour_case not in self.black_pawns and neighbour_case not in self.white_pawns :
                #On check pour les cases libres autour du pion opposé considéré si elles permettent la prise de ce pion
                legal_neighbours.append(neighbour_case)
        
        print("pawn :" ,pawn ," neighbours_list : ", pawn_neighbours, "legal_neighbours : ", legal_neighbours)
        return legal_neighbours
    
        # if not(len(self.legal_moves)) : 
        #     if self.joueur : 
        #         self.white_is_over = True
        #         self.joueur = not(self.joueur)
        #         self.compute_legal_moves()
        #     else : 
        #         self.black_is_over = True
        #         self.joueur = not(self.joueur)
        #         self.compute_legal_moves()
                    
    
    def compute_pawn_neighbours(self, pawn) :
        neighbours_list = []
        
        for x in range(int(pawn[0]) -1, int(pawn[0]) + 2) :
            for y in range(int(pawn[1]) -1, int(pawn[1]) + 2) :
                neighbours_list.append((int(x),int(y)))
        
        neighbours_list.pop(neighbours_list.index(pawn))
        
        return neighbours_list
    
    def check_legal_move(self, pawn_to_check, legal_neighbours) :
        #pawn_to_check = pion opposé considéré
        #legal_neighbours = Cases libres voisines du pion opposé 
        
        #Si je met un pion noir sur une des cases libres, est-ce que ça prend au moins 1 pions blanc ? 
        
        if self.joueur == 1 : 
            #Liste des pions noirs adjacents à la case à check
            pawns_to_check = [pawn for pawn in self.black_pawns if pawn in legal_neighbours]
        else : 
            #print("Pions noirs : ", self.black_pawns, "case : ", case, "Voisins de case : ", case_neighbours)
            #Liste des pions blancs adjacents à la case à check
            pawns_to_check = [pawn for pawn in self.white_pawns if pawn in legal_neighbours]
        
        print("legal_neighbours to check : ", legal_neighbours)
        #print("Pion : ", case, " pawns_to_check : ", pawns_to_check)
        for free_case in legal_neighbours : 
            #déterminer le sens du vecteur entre la case à tester et le pion opposé considéré
            case_x = free_case[0]
            case_y = free_case[1]
            pawn_x = pawn_to_check[0]
            pawn_y = pawn_to_check[1]
            delta_x = pawn_x - case_x 
            delta_y = pawn_y - case_y
            
            #print("Pawn to check : ", pawn_to_check, " Free case : ", free_case, "Delta : ", delta_x,",",delta_y)
            
            #Nombre de translations depuis la case, commence à 2 puisque 1 est le pions opposé considéré
            step = 2
            #Liste des coordonnées des pions à flip, on ajoute le premier qui n'est pas traité dans la boucle while suivante
            local_pawns_to_flip = [pawn_to_check]
            #A priori on suppose que legal == True, s'il ne l'est pas la valeur sera changée
            legal = True
            #Tant que la position à checker est dans le champs et que l'arrêt n'est pas déclenché
            while case_x + step*delta_x >= 0 and case_x + step*delta_x <= self.nb_cases -1 and case_y + step*delta_y >= 0 and case_y + step*delta_y <= self.nb_cases -1 :
                coordinates_to_check = (case_x + step*delta_x, case_y + step*delta_y)
                #print("coord_to_check ", coordinates_to_check)
                if self.joueur : #Joueur Blanc
                    if  coordinates_to_check in self.white_pawns :
                        #Si le pion d'après est blanc : critère d'arret (ou break/continue) et ajout à pawn to flip du premier pion
                        x_pawn_to_add = coordinates_to_check[0] - delta_x
                        y_pawn_to_add = coordinates_to_check[1] - delta_y
                        
                        #Si un seul pion entre deux blanc, evite d'ajouter le seul 2 fois
                        if (x_pawn_to_add,y_pawn_to_add) not in local_pawns_to_flip :
                            local_pawns_to_flip.append((x_pawn_to_add,y_pawn_to_add))
                        
                        #On arrête la boucle while
                        break
                    
                    if  coordinates_to_check in self.black_pawns :
                        #Si le pion est noir : ajout à pawns_to_flip local et step += 1 et continue
                        x_pawn_to_add = coordinates_to_check[0]
                        y_pawn_to_add = coordinates_to_check[1]
                        
                        #Ajoute le pions aux pions à retourner 
                        local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))
                        
                        #On va checker le pion suivant
                        step += 1
                        continue
                
                    #Si on arrive ici la case est focément vide 
                    print("Hors-cadre : ", coordinates_to_check)
                    legal = False
                    break
                    
                else : #Joueur Noir
                    if  coordinates_to_check in self.black_pawns :
                        #Si le pion d'après est noir : critère d'arret (ou break/continue) et ajout à pawn to flip du premier pion
                        x_pawn_to_add = coordinates_to_check[0] - delta_x
                        y_pawn_to_add = coordinates_to_check[1] - delta_y
                        
                        #Si un seul pion entre deux blanc, evite d'ajouter le seul 2 fois
                        if (x_pawn_to_add,y_pawn_to_add) not in local_pawns_to_flip :
                            local_pawns_to_flip.append((x_pawn_to_add,y_pawn_to_add))
                        
                        #On arrête la boucle while
                        break
                    
                    if  coordinates_to_check in self.white_pawns :
                        #Si le pion est noir : ajout à pawns_to_flip local et step += 1 et continue
                        x_pawn_to_add = coordinates_to_check[0]
                        y_pawn_to_add = coordinates_to_check[1]
                        
                        #Ajoute le pions aux pions à retourner 
                        local_pawns_to_flip.append((x_pawn_to_add, y_pawn_to_add))
                        
                        #On va checker le pion suivant
                        step += 1
                        continue
                
                    #Si on arrive ici la case est focément vide 
                    print("Hors-cadre : ", coordinates_to_check)
                    legal = False
                    break
            #Le cas d'une suite de pions d'une même couleur jusqu'à la sortie du cadre ne permet pas de passer legal à False puisqu'on sort du while sans être passé dessus
            #print("Pawn to check : ", pawn_to_check, " Free case : ", free_case, " local_pawns_to_flip", local_pawns_to_flip)
            #Cette condition permet de ne pas avoir à checker à la checker à chaque tour du while et determine si on est sorti parce que pion blanc ou parce que hors cadre
            #if  case_x + step*delta_x < 0 and case_x + step*delta_x > self.nb_cases - 1 and case_y + step*delta_y < 0 and case_y + step*delta_y > self.nb_cases -1 :
            if  case_x + step*delta_x  < 0 or case_x + step*delta_x > self.nb_cases - 1 or case_y + step*delta_y < 0 or case_y + step*delta_x > self.nb_cases -1 :
                legal = False
                print("Legal = False  Free_Case : ", free_case)
            #Sorti du while avec legal toujours True <=> Pas de case vide rencontrées 
            
            if legal :
                print("Legal = True  Free_Case : ", free_case)
                #print("246")
                #On ne veut la position qu'une fois dans cette liste
                if free_case not in self.legal_moves :
                    self.legal_moves.append(free_case)
                #On ajoute au dictionnaire des consequences les pions à retourner si cette position est choisie
                if free_case in list(self.pawns_to_flip.keys()) :
                    for local_pawn in local_pawns_to_flip :
                        self.pawns_to_flip[free_case].append(local_pawn)
                else : 
                    self.pawns_to_flip.update({free_case : local_pawns_to_flip})
                #Suivre ce vecteur et l'allonger jusqu'à rencontrer une case blanche/noire/vide/hors cadre
                print("self.pawns_to_flip", self.pawns_to_flip, "\n")
            
    def remove_legal_moves_GUI(self, x, y) :
        #On enleve le move joué de la liste des coup jouables
        self.legal_moves.pop(self.legal_moves.index((x,y)))
        
        #On remet de la couleur du fond les coups jouables non joués
        for move in self.legal_moves : 
            self.grille.create_oval(move[0]*self.GUI_size/self.nb_cases + self.GUI_size/60, move[1]*self.GUI_size/self.nb_cases + self.GUI_size/60 , (move[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, (move[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'green', fill = "green", width = 2)

    def flip_pawns(self, x, y) :

        if self.joueur : 
            #On ajoute le pion qui vient d'être placé
            self.white_pawns.append((x,y))
            for pawn in self.pawns_to_flip[(x,y)] :
                print("Pawn : ", pawn)
                print("self.black_pawns : ", self.black_pawns)
                print("self.white_pawns : ", self.white_pawns)
                #On enlève de la liste des pions opposés chaque pion pris
                self.black_pawns.pop(self.black_pawns.index((pawn[0],pawn[1])))
                #On le rajoute dans la liste des pions similaires
                self.white_pawns.append((pawn[0],pawn[1]))
                #On remplace sa couleur sur la grille
                self.grille.create_oval(pawn[0]*self.GUI_size/self.nb_cases + self.GUI_size/60, pawn[1]*self.GUI_size/self.nb_cases + self.GUI_size/60 , (pawn[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, (pawn[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'white', fill = "white", width = 2)
        else : 
            self.black_pawns.append((x,y))
            for pawn in self.pawns_to_flip[(x,y)] :
                print("Pawn : ", pawn)
                print("self.black_pawns : ", self.black_pawns)
                print("self.white_pawns : ", self.white_pawns)
                self.white_pawns.pop(self.white_pawns.index((pawn[0],pawn[1])))
                self.black_pawns.append((pawn[0],pawn[1]))
                self.grille.create_oval(pawn[0]*self.GUI_size/self.nb_cases + self.GUI_size/60, pawn[1]*self.GUI_size/self.nb_cases + self.GUI_size/60 , (pawn[0]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, (pawn[1]+1)*self.GUI_size/self.nb_cases - self.GUI_size/60, outline = 'black', fill = "black", width = 2)
        
        # print("(x,y) : ", x, ",", y)
        # print("self.black_pawns : ", self.black_pawns)
        # print("self.white_pawns : ", self.white_pawns)
        # print("\n")
                
                
class Board() :
    def __init__(self, board_shape = 8) : 
        #Initialisation de la grille
        self.board_shape = board_shape
        self.grid = np.zeros((self.board_shape,self.board_shape), dtype = "str")
        
        #Positionnement des premiers pions
        mid_grid = int(self.board_shape/2) - 1
        self.grid[mid_grid , mid_grid] = "0"
        self.grid[mid_grid , mid_grid + 1] = "O"
        self.grid[mid_grid + 1,mid_grid] = "O"
        self.grid[mid_grid + 1,mid_grid + 1] = "0"
        
        #Initialisation du dictionnaire d'historique --> Meilleur système de logging ? 
        self.logs = {}
        
        

    
    def compute_score_moves(moves) :
        pass
        
    def flip_tiles(move) : 
        pass
    
    

class Move() :
    def __init__(self) : 
        pass
    
G = Game(gametype="H-H", 
         nb_cases=8, 
         GUI=True, 
         GUI_size=800)
A = Board()

    
