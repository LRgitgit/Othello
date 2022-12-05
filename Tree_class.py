from math import inf


class TreeNode:
    def __init__(self, legal_moves, white_pawns, black_pawns, pawns_to_flip, player, position, val_position,
                 alpha=-inf, beta=inf):
        self.legal_moves = legal_moves
        self.white_pawns = white_pawns
        self.black_pawns = black_pawns
        self.pawns_to_flip = pawns_to_flip
        self.player = player
        self.position = position
        self.val_position = val_position
        self.alpha = alpha
        self.beta = beta
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
