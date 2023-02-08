import numpy as np
from game_framework import helper_functions as hf


class Board:
    def __init__(self, n_slots=24, n_pieces=15, board_state=None):
        # board_state_size holds the size of the board state vector
        # need n_slots entries to encode number of white pieces on each slot
        # need n_slots entries to encode number of black pieces on each slot
        # need n_slots entries to encode whether white, black or none pieces are pinned.
        # 0 means no pinning. 1 means Player 0 is pinning. -1 means Player 1 is pinning.

        if board_state is None:
            board_state = []
        if not board_state:
            board_state = np.zeros((3, n_slots))
            board_state[0, 0] = n_pieces
            board_state[1, -1] = n_pieces
        else:
            board_state = np.array(board_state)

        self.n_slots = n_slots
        self.n_pieces = n_pieces
        self.board_state = board_state

    def is_player_pinned_at_location(self, slot_id, player_id):
        # This function returns true if player_id is pinned at location slot_id
        return self.board_state[2, slot_id] == 2 * player_id - 1

    def is_player_pinning_at_location(self, slot_id, player_id):
        # This function returns true if player_id is pinning at location slot_id
        return self.board_state[2, slot_id] == -2 * player_id + 1

    def move_piece_from_slot_to_slot(self, origin, destination, player_id):
        # This function changes the board state to capture a move for a player_id's piece from slot origin to slot
        # destination. The function returns true of the move was successfully performed, and false if the move is
        # illegal.
        # Note: This function does NOT check whether the origin/destination pair is consistent with the latest dice
        # roll!

        if self.n_slots > destination >= 0:  # if regular move
            # if player has a piece at the origin slot that is not pinned and the other player is not occupying the
            # destination slot
            if self.board_state[player_id, origin] > 0 \
                    and not self.is_player_pinned_at_location(origin, player_id) \
                    and not self.board_state[hf.get_other_player_id(player_id), destination] > 1 \
                    and not self.is_player_pinned_at_location(destination, player_id):

                # if player is pinning at the origin, mark origin as unpinned
                if self.is_player_pinning_at_location(origin, player_id) and self.board_state[player_id, origin] == 1:
                    self.board_state[2, origin] = 0

                # if player is pinning at the destination, mark destination as pinned
                if self.is_player_piece_vulnerable_at_slot(destination, hf.get_other_player_id(player_id)):
                    self.board_state[2, destination] = hf.mark_player_pinning(player_id)

                # move piece
                self.board_state[player_id, origin] -= 1
                self.board_state[player_id, destination] += 1

                return True
            else:
                return False

        elif destination == -1:  # if end-game move
            if player_id == 0 and self.is_white_endgame() and self.board_state[player_id, origin] > 0:

                # if player is pinning at the origin, mark origin as unpinned
                if self.is_player_pinning_at_location(origin, player_id) and self.board_state[player_id, origin] == 1:
                    self.board_state[2, origin] = 0

                self.board_state[0, origin] = self.board_state[0, origin] - 1
                return True
            elif player_id == 1 and self.is_black_endgame() and self.board_state[player_id, origin] > 0:

                # if player is pinning at the origin, mark origin as unpinned
                if self.is_player_pinning_at_location(origin, player_id) and self.board_state[player_id, origin] == 1:
                    self.board_state[2, origin] = 0

                self.board_state[1, origin] = self.board_state[1, origin] - 1
                return True
            else:
                return False
        else:
            return False

    def is_player_piece_vulnerable_at_slot(self, slot, player_id):
        # This function returns true if player_id has a vulnerable piece in slot
        if self.board_state[player_id, slot] == 1 and self.board_state[2, slot] == 0:
            return True
        else:
            return False

    def is_white_endgame(self):
        # This function returns true if player 1 (white) is in the endgame phase
        if np.all(self.board_state[0, 0:round(self.n_slots*0.75)] == 0) \
                and not np.any(self.board_state[2, :] == -1):
            return True
        else:
            return False

    def is_black_endgame(self):
        # This function returns true if player 2 (black) is in the endgame phase
        if np.all(self.board_state[1, round(self.n_slots*0.25):self.n_slots] == 0) \
                and not np.any(self.board_state[2, :] == 1):
            return True
        else:
            return False

    def is_game_over_player_1(self):
        # This function returns 1 or 2 if player 1 (white) won the game by 1 point or 2 points
        if np.all(self.board_state[0, :] == 0):
            if np.sum(self.board_state[1, :]) == self.n_pieces:
                return 2
            else:
                return 1
        return

    def is_game_over_player_2(self):
        # This function returns 1 or 2 if player 2 (black) won the game by 1 point or 2 points
        if np.all(self.board_state[1, :] == 0):
            if np.sum(self.board_state[0, :]) == self.n_pieces:
                return 2
            else:
                return 1
        return

    def __eq__(self, other_board):
        return np.array_equal(self.board_state, other_board.board_state)

    def __hash__(self):
        # needed to compare boards
        return hash(tuple(map(tuple, self.board_state)))
