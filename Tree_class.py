from math import inf, sqrt, log

'''
Définition de la classe TreeNode pour générer des arbres utilisés dans les algorithmes de Othello_class.py
'''


class TreeNode:
    def __init__(self, legal_moves, white_pawns, black_pawns, pawns_to_flip, player, position, val_position,
                 alpha=-inf, beta=inf, nb_trial=0, mcts_score=0):
        self.legal_moves = legal_moves
        self.white_pawns = white_pawns
        self.black_pawns = black_pawns
        self.pawns_to_flip = pawns_to_flip
        self.player = player
        self.position = position
        self.val_position = val_position
        self.alpha = alpha
        self.beta = beta
        self.nb_trial = nb_trial
        self.mcts_score = mcts_score
        self.children_val = []
        self.children = []
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + '|__' if self.parent else ""

        # print(prefix + str(self.white_pawns) + str(self.black_pawns))
        print(prefix + str(self.val_position))
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def UCB1(self, C):
        if self.nb_trial == 0:  # on n'a jamais exploré ce noeud
            return inf
        else:
            return self.mcts_score/self.nb_trial + C * sqrt(log(self.parent.nb_trial)/self.nb_trial)

    def tree_traversal(self, C):
        max_ucb = -inf
        max_i = 0
        for i, tree_child in enumerate(self.children):
            ucb = tree_child.UCB1(C)
            if ucb > max_ucb:
                max_ucb = ucb
                max_i = i
        return self.children[max_i]
