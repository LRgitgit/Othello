# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:02:16 2022

@author: prje
"""

import numpy as np


class Game() : 
    def __init__(self, nb_human = 0, nb_computer = 0) : 
        pass
        

class Board() :
    def __init__(self) : 
        #Initialisation de la grille
        self.grid = np.zeros((8,8), dtype = "str")
        
        #Positionnement des premiers pions
        mid_grid = int(self.grid.shape[0]/2) - 1
        print(mid_grid)
        self.grid[mid_grid , mid_grid] = "0"
        self.grid[mid_grid , mid_grid + 1] = "O"
        self.grid[mid_grid + 1,mid_grid] = "O"
        self.grid[mid_grid + 1,mid_grid + 1] = "0"
        
    def compute_legal_moves() : 
        pass
        

class Move() :
    def __init__(self) : 
        pass
    

    
A= Board()
print(A.grid)
    
