from Play_Othello import *


def eval_algo_MM_AB(IA_mode, nb_games=50):
    l_depth = [1, 2, 3, 4]
    l_score = []
    l_time = []
    for depth in l_depth:
        print('depth =', depth)
        start = time()
        score_IA = test_IA(IA_mode=IA_mode, depth=depth, GUI=False, nb_games=nb_games)
        exec_time = time() - start
        l_score.append(score_IA)
        l_time.append(exec_time / nb_games)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()
    ax1.bar(l_depth, l_score)
    ax1.set_xlabel('Profondeur')
    ax1.set_ylabel('Taux de victoires')

    ax2.bar(l_depth, l_time)
    ax2.set_xlabel('Profondeur')
    ax2.set_ylabel('Temps de calcul par partie')
    plt.show()


def eval_algo_MCTS(IA_mode, nb_games=50):
    # l_C = [0, 0.25, 0.5, 0.75]
    l_C = [1, 2, 3, 4]
    # l_C = [10, 20, 30, 40]
    # 3 listes de C pour faire des plots plus jolis
    l_nb_simul = [1, 3, 5, 10, 20, 30]
    # l_nb_simul = [1]
    l_score = []
    l_time = []
    for C in l_C:
        print('C =', C)
        l_score_C = []
        for mcts_simul in l_nb_simul:
            print('mcts_simul =', mcts_simul)
            start = time()
            score_IA = test_IA(IA_mode=IA_mode, depth=2, nb_games=nb_games, C=C, mcts_simul=mcts_simul, mcts_iter=10)
            exec_time = time() - start
            l_score_C.append(score_IA)
            if C == l_C[0]:
                # on ne calcule le temps qu'une seule fois car C n'influe pas sur le temps de calcul
                l_time.append(exec_time)
        l_score.append(l_score_C)

    print(l_score)
    n_row = 1
    n_col = len(l_score) + 1
    fig, axs = plt.subplots(n_row, n_col)
    st = fig.suptitle('Nombre de parties simulées par Rollout')

    for col in range(n_col - 1):
        axs[col].bar([k for k in range(len(l_nb_simul))], l_score[col])
        # axs[col].set_xlabel('Nombre de parties simulées par Rollout')
        axs[col].set_ylabel('Taux de victoires')
        axs[col].set_title('C =' + str(l_C[col]))
        axs[col].set_xticks([k for k in range(len(l_nb_simul))], [str(nb_simul) for nb_simul in l_nb_simul])
    axs[-1].bar([k for k in range(len(l_nb_simul))], l_time)
    # axs[-1].set_xlabel('Nombre de parties simulées par Rollout')
    axs[-1].set_ylabel('Temps de calcul par partie')
    axs[-1].set_xticks([k for k in range(len(l_nb_simul))], [str(nb_simul) for nb_simul in l_nb_simul])
    axs[-1].set_title('C =' + str(l_C[0]))

    fig.tight_layout()
    st.set_y(0.95)
    plt.show()

    # plt.bar([k for k in range(len(l_C))], l_score)
    # plt.xticks([k for k in range(len(l_C))], [str(C) for C in l_C])
    # plt.show()


if __name__ == '__main__':
    # IA_1 = 'alphabeta'
    # IA_2 = 'random'
    # IA_mode = (IA_1, IA_2)
    #
    # eval_algo_MM_AB(IA_mode, nb_games=50)
    # Pour évaluer MinMax ou AlphaBeta

    ###

    IA_1 = 'MCTS'
    IA_2 = 'random'
    IA_mode = (IA_1, IA_2)
    eval_algo_MCTS(IA_mode, nb_games=3)
    # Pour évaluer MCTS
