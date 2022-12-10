from Othello_class import *
from time import time
import matplotlib.pyplot as plt


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


def load_position(position, player, depth):
    b_pawns, w_pawns = get_b_w(position)
    start_position = [b_pawns, w_pawns, player]
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


def test_IA(IA_mode, depth, GUI=False, nb_games=50, C=2, mcts_simul=100, mcts_iter=10):
    nb_win_white = 0
    nb_games = nb_games
    for k in range(nb_games):
        # print('game :', k+1)
        G = Game(nb_tiles=8,
                 GUI=GUI,
                 GUI_size=800,
                 exploration_depth=depth,
                 game_mode='IAvIA',
                 start_position='default',
                 IA_mode=IA_mode,
                 C=C,
                 mcts_simul=mcts_simul,
                 mcts_iter=mcts_iter)
        if G.GUI:
            G.init_GUI()
        G.init_game()
        G.start_playing()
        if G.root:
            G.root.mainloop()
        if G.winner == 'Blanc':
            nb_win_white += 1
    return nb_win_white / nb_games


if __name__ == '__main__':
    ''' play game PvP'''
    IA_1 = 'alphabeta'
    IA_2 = 'random'
    IA_mode = (IA_1, IA_2)
    G = Game(nb_tiles=8,
             GUI=True,
             GUI_size=800,
             exploration_depth=2,
             game_mode='PvP',
             start_position='default',
             IA_mode=IA_mode)
    G.init_GUI()
    G.init_game()
    G.start_playing()
    G.root.mainloop()
    print(G.winner)
    ''' play game PvP'''