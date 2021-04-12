# Tic-Tac-Toe (Monte Carlo)
# Author - Noel Pereira
# Submission - http://www.codeskulptor.org/#user47_xW3N3MWlRgXKSjN.py

####################################################################

"""
    Monte Carlo Tic-Tac-Toe Player
    """

# general import
import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
        This function takes a current board and the next player to move.
        starting with the given player by making random moves, alternating between players.
        """
    while not board.check_win():
        row, col = random.choice(board.get_empty_squares())
        board.move(row, col, player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
        This function takes a grid of scores (a list of lists) with the same dimensions
        as the Tic-Tac-Toe board, a board from a completed game, and which player the machine player is.
        This function scores the completed board and updates the scores grid.
        """
    status = board.check_win()
    alter_player = provided.switch_player(player)
    dim = board.get_dim()
    if status == player:
        score_current_temp = SCORE_CURRENT
        score_other_temp = SCORE_OTHER
    elif status == alter_player:
        score_current_temp = -SCORE_CURRENT
        score_other_temp = -SCORE_OTHER
    else:
        return
    for dummy_row in range(dim):
        for dummy_col in range(dim):
            square = board.square(dummy_row,dummy_col)
            if square == player:
                scores[dummy_row][dummy_col] += score_current_temp
            elif square == alter_player:
                scores[dummy_row][dummy_col] -= score_other_temp

def get_best_move(board, scores):
    """
        This function takes a current board and a grid of scores.
        The function should find all of the empty squares with the maximum score
        and randomly return one of them as a (row, column) tuple.
        """
    empty = board.get_empty_squares()
    score_max = float('-inf')
    score_max_pos = []
    for square in empty:
        row, col = square
        if scores[row][col] > score_max:
            score_max_pos = [(row,col)]
            score_max = scores[row][col]
        elif scores[row][col] == score_max:
            score_max_pos.append((row,col))
    return random.choice(score_max_pos)

def mc_move(board, player, trials):
    """
        This function takes a current board, which player the machine player is,
        and the number of trials to run.
        return a move for the machine player in the form of a (row, column) tuple.
        """
    scores = [[0 for dummy_x in range(board.get_dim())] for dummy_x in range(board.get_dim())]
    for dummy_trial in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)