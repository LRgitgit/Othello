from Othello_class import *


# G = Game(nb_tiles=8,
#          GUI=True,
#          GUI_size=800,
#          exploration_depth=2,
#          game_mode='IAvIA',
#          start_position='default')
#
# G.start_game()


# print(G.position.transpose())
# print(G.black_pawns)

# position = np.array([
#     [1., -1.,  1.,  1.,  1.,  1.,  1.,  1.],
#     [1., -1., -1.,  1., -1., -1.,  1.,  1.],
#     [1., -1.,  1.,  1.,  1., -1.,  1.,  1.],
#     [1., -1., -1., -1.,  1.,  1., -1.,  1.],
#     [1.,  1., -1., -1., -1., -1., -1., -1.],
#     [1., -1.,  1., -1., -1.,  1.,  1.,  1.],
#     [1., -1.,  1.,  1., -1.,  1.,  1.,  1.],
#     [1.,  1.,  1.,  1.,  1., -1., -1., -1.]
# ])


def get_b_w(position):
    # prendre G.position.transpose()
    white, black = [], []
    n_r, n_c = position.shape
    for i in range(n_r):
        for j in range(n_c):
            if position[i, j] == 1:
                white.append((j, i))
            elif position[i, j] == -1:
                black.append((j, i))
    return black, white


def recursion_MinMax(tree, joueur):
    # print(type(tree), tree)
    # print(type(tree['legal_moves']), tree['legal_moves'])
    # print(type(tree['legal_moves']['(1, 1)']), tree['legal_moves']['(1, 1)'])
    # print(type(tree['legal_moves']['(1, 1)']['legal_moves']), tree['legal_moves']['(1, 1)']['legal_moves'])
    # print(type(tree['legal_moves']['(1, 1)']['legal_moves']['(1, 3)']), tree['legal_moves']['(1, 1)']['legal_moves']['(1, 3)'])
    '''
    <class 'dict'> {'legal_moves': {'(1, 1)': {'legal_moves': [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (1, 1), (2, 2), (3, 3)], 'black_pawns': [(4, 3), (5, 3)], 'human_turn': True, 'val_position': -56.0}, '(2, 1)': {'legal_moves': [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (1, 1)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (2, 1), (2, 2)], 'black_pawns': [(3, 3), (4, 3), (5, 3)], 'human_turn': True, 'val_position': -7.0}, '(3, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (4, 2)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (3, 2), (3, 3), (4, 3)], 'black_pawns': [(2, 2), (5, 3)], 'human_turn': True, 'val_position': -7.0}, '(4, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (3, 1), (5, 1)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (4, 2), (4, 3)], 'black_pawns': [(2, 2), (3, 3), (5, 3)], 'human_turn': True, 'val_position': -6.0}, '(5, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (6, 3)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (5, 2), (4, 3), (5, 3)], 'black_pawns': [(2, 2), (3, 3)], 'human_turn': True, 'val_position': -7.0}, '(6, 2)': {'legal_moves': [(1, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (6, 3)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (6, 2), (5, 3)], 'black_pawns': [(2, 2), (3, 3), (4, 3)], 'human_turn': True, 'val_position': -7.0}, '(6, 3)': {'legal_moves': [(2, 4), (5, 5)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (6, 3), (5, 3), (4, 3), (3, 3)], 'black_pawns': [(2, 2)], 'human_turn': True, 'val_position': -9.0}}, 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4)], 'black_pawns': [(2, 2), (3, 3), (4, 3), (5, 3)], 'human_turn': True}
    <class 'dict'> {'(1, 1)': {'legal_moves': [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (1, 1), (2, 2), (3, 3)], 'black_pawns': [(4, 3), (5, 3)], 'human_turn': True, 'val_position': -56.0}, '(2, 1)': {'legal_moves': [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (1, 1)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (2, 1), (2, 2)], 'black_pawns': [(3, 3), (4, 3), (5, 3)], 'human_turn': True, 'val_position': -7.0}, '(3, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (4, 2)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (3, 2), (3, 3), (4, 3)], 'black_pawns': [(2, 2), (5, 3)], 'human_turn': True, 'val_position': -7.0}, '(4, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (3, 1), (5, 1)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (4, 2), (4, 3)], 'black_pawns': [(2, 2), (3, 3), (5, 3)], 'human_turn': True, 'val_position': -6.0}, '(5, 2)': {'legal_moves': [(1, 3), (2, 4), (3, 5), (5, 5), (6, 3)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (5, 2), (4, 3), (5, 3)], 'black_pawns': [(2, 2), (3, 3)], 'human_turn': True, 'val_position': -7.0}, '(6, 2)': {'legal_moves': [(1, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (6, 3)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (6, 2), (5, 3)], 'black_pawns': [(2, 2), (3, 3), (4, 3)], 'human_turn': True, 'val_position': -7.0}, '(6, 3)': {'legal_moves': [(2, 4), (5, 5)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (6, 3), (5, 3), (4, 3), (3, 3)], 'black_pawns': [(2, 2)], 'human_turn': True, 'val_position': -9.0}}
    <class 'dict'> {'legal_moves': [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)], 'white_pawns': [(2, 3), (3, 4), (4, 4), (5, 4), (1, 1), (2, 2), (3, 3)], 'black_pawns': [(4, 3), (5, 3)], 'human_turn': True, 'val_position': -56.0}
    <class 'list'> [(1, 3), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)]
    '''
    # if not tree['white_pawns']:  # les blancs ont perdu
    #     # print(tree['move'])
    #     if joueur:
    #         val = -inf
    #     else:
    #         val = inf
    #     return tree['move'], val
    # elif not tree['black_pawns']:  # les noirs ont perdu
    #     if joueur:
    #         val = inf
    #     else:
    #         val = -inf
    #     return tree['move'], val
    #
    # if type(tree['legal_moves']) == list:  # on est sur une feuille
    #     print(tree['move'])
    #     return tree['move'], tree['val_position']  # on remonte le coup et sa valeur estimée

    l_coups = []
    for move in tree['legal_moves']:
        if type(tree['legal_moves']) == list:  # on est sur une feuille
            print(tree['legal_moves'])
            print(tree['move'])
            return tree['move'], tree['val_position']  # on remonte le coup et sa valeur estimée
        if not tree['legal_moves'][move]['white_pawns']:  # les blancs ont perdu
            # print(tree['move'])
            if joueur:
                val = -inf
            else:
                val = inf
            return tree['move'], val
        elif not tree['legal_moves'][move]['black_pawns']:  # les noirs ont perdu
            if joueur:
                val = inf
            else:
                val = -inf
            return tree['move'], val


        # on n'est pas sur un noeud feuille donc on parcourt tous les coups possibles pour ce noeud
        l_coups.append(recursion_MinMax(tree['legal_moves'][move], not joueur))
    max_val, min_val = -inf, inf
    if joueur:  # joueur blanc => on remonte le max
        max_i = 0
        for i, coup in enumerate(l_coups):
            if coup[1] >= max_val:  # si la position remontée est plus élevée que le max
                max_val = coup[1]
                max_i = i
        return l_coups[max_i]
    else:
        min_i = 0
        for i, coup in enumerate(l_coups):
            if coup[1] <= min_val:  # si la position remontée est plus basse que le min
                min_val = coup[1]
                min_i = i
        return l_coups[min_i]


def eval_MinMax(G):
    G.compute_tree()
    tree = G.tree
    joueur = G.joueur
    best_move = recursion_MinMax(tree, joueur)
    return best_move


def load_position(position, joueur, depth):
    b_pawns, w_pawns = get_b_w(position)
    start_position = [b_pawns, w_pawns, joueur]
    G = Game(nb_tiles=8,
             GUI=True,
             GUI_size=800,
             exploration_depth=depth,
             game_mode='IAvIA',
             start_position=start_position)
    if G.GUI:
        G.init_GUI()
    G.init_game()
    # print(G.position.transpose())
    G.compute_legal_moves()

    # eval_MinMax(G)
    # G.compute_tree()
    return G


if __name__ == '__main__':
    # b_pawns = [(2, 2), (3, 3), (5, 3), (4, 3)]
    # w_pawns = [(3, 4), (2, 3), (5, 4), (4, 4)]
    b_pawns = [(4, 3), (1, 3), (2, 3), (3, 3)]
    w_pawns = [(3, 4), (4, 4), (5, 4), (1, 1), (2, 2), (6, 2), (5, 3)]
    # b_pawns = [(4, 2), (4, 3), (6, 4), (5, 3), (4, 6), (5, 5), (4, 5)]
    # w_pawns = [(3, 3), (3, 5), (3, 4), (5, 4), (4, 4)]

    position = np.zeros((8, 8))
    for elem in w_pawns:
        position[elem] = 1
    for elem in b_pawns:
        position[elem] = -1
    position = position.transpose()
    # print(position)
    # print(position)
    joueur = False

    G = load_position(position, joueur, 1)
    # G.start_playing()
    G.eval_position()
    # initialisation de l'arbre des coups
    # print(G.position.transpose())
    tree_root = TreeNode(G.legal_moves.copy(), G.white_pawns.copy(), G.black_pawns.copy(), G.pawns_to_flip.copy(),
                         G.joueur, G.position, G.val_position)
    # print(tree_root.val_position)
    # print(G.position.transpose())
    id_best_move = G.compute_tree(depth=2, tree_parent=tree_root)
    # G.black_pawns, G.white_pawns = tree_root.black_pawns, tree_root.white_pawns

    # print(tree_root.black_pawns, tree_root.white_pawns)
    print(id_best_move)
    tree_root.print_tree()
    # print(eval_MinMax(G))
    if G.root:
        G.root.mainloop()

