import copy as cp
import random as rd


def roll_dice(n_dice_faces):
    # This function generates a random dice roll
    dice_0 = rd.randint(1, n_dice_faces)
    dice_1 = rd.randint(1, n_dice_faces)

    return [dice_0, dice_1]


def get_other_player_id(player_id):
    # This function returns other player's id
    return 1 - player_id


def mark_player_pinning(player_id):
    # This function returns the value to use in the 3rd row of the board_state to mark that the given player is pinning
    return -2 * player_id + 1


def get_possible_afterstates_single_dice(board, dice_value, player_id):
    # This function generates all possible partial afterstates, i.e., afterstates after playing a single dice.
    afterstates_list = []

    # loop over all slots on board
    for i in range(board.n_slots):

        # look at where the piece would land
        if player_id == 0:
            potential_next_slot = i + dice_value
        else:
            potential_next_slot = i - dice_value

        # copy board object
        potential_next_board_state = cp.deepcopy(board)

        # if slot contains at least one player_id's piece that is not pinned, and
        # if piece at location i is allowed to move by value of dice_value, i.e., does not exceed board and
        # does not land on location pinned by other player and does not land on other player's bridge
        # TODO: implement end-game case. May just call move_piece_from_slot_to_slot from Board.
        if potential_next_board_state.n_slots > potential_next_slot >= 0 \
                and board.board_state[player_id, i] > 0 \
                and not board.is_player_pinned_at_location(i, player_id) \
                and not potential_next_board_state.is_player_pinned_at_location(potential_next_slot, player_id) \
                and potential_next_board_state.board_state[get_other_player_id(player_id), potential_next_slot] <= 1:

            # if player is moving the last piece that was pinning, then mark unpinned
            if potential_next_board_state.board_state[player_id, i] == 1 \
                    and potential_next_board_state.is_player_pinning_at_location(i, player_id):
                potential_next_board_state.board_state[2, i] = 0

            # if player making a pinning move, then mark as pinned
            if potential_next_board_state.board_state[get_other_player_id(player_id), potential_next_slot] == 1 \
                    and potential_next_board_state.board_state[2, potential_next_slot] == 0:
                potential_next_board_state.board_state[2, potential_next_slot] = mark_player_pinning(player_id)

            # move piece
            potential_next_board_state.board_state[player_id, i] = \
                potential_next_board_state.board_state[player_id, i] - 1
            potential_next_board_state.board_state[player_id, potential_next_slot] = \
                potential_next_board_state.board_state[player_id, potential_next_slot] + 1

            # add afterstate to list
            afterstates_list.append(potential_next_board_state)

    return afterstates_list


def get_action_space(board, dice_values, player_id):
    # This function returns the complete set of possible afterstates after moving pieces from both dice
    # TODO: Test the function to verify that "forced moves" are working well. Particularly, if both dice can be played
    #  individually, but not together, the rules force to play the dice with the largest value (the player does not get
    #  the chance to choose which die to play).

    # start with the case where both dice have different values
    if dice_values[0] != dice_values[1]:
        # Step 1a: determine slots that contain movable pieces of player_id for dice 0
        action_space_list_dice_0 = get_possible_afterstates_single_dice(board, dice_values[0], player_id)

        # Step 1b: determine slots that contain movable pieces of player_id for dice 1
        action_space_list_dice_1 = get_possible_afterstates_single_dice(board, dice_values[1], player_id)

        # Step 2a: determine slots that contain movable pieces of player_id for dice 1 after moving first piece using
        # dice 0
        action_space_list_dice_0_then_dice_1 = []
        for i in range(len(action_space_list_dice_0)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_dice_0[i],
                                                                          dice_values[1],
                                                                          player_id)
            action_space_list_dice_0_then_dice_1 += additional_afterstates

        # Step 2b: determine slots that contain movable pieces of player_id for dice 0 after moving first piece using
        # dice 1
        action_space_list_dice_1_then_dice_0 = []
        for i in range(len(action_space_list_dice_1)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_dice_1[i],
                                                                          dice_values[0],
                                                                          player_id)
            action_space_list_dice_1_then_dice_0 += additional_afterstates

        # Step 3: combine all potential afterstates in single structure
        if not action_space_list_dice_0 and not action_space_list_dice_1:
            combined_afterstates = []
        elif not action_space_list_dice_0_then_dice_1 and not action_space_list_dice_1_then_dice_0:
            combined_afterstates = action_space_list_dice_0 + action_space_list_dice_1
        else:
            combined_afterstates = action_space_list_dice_0_then_dice_1 + action_space_list_dice_0_then_dice_1

    # else, if the dice have the same value
    else:
        # Step 1: determine slots that contain movable pieces of player_id for first move
        action_space_list_move_1 = get_possible_afterstates_single_dice(board, dice_values[0], player_id)

        # Step 2a: determine slots that contain movable pieces of player_id for second move
        action_space_list_move_2 = []
        for i in range(len(action_space_list_move_1)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_move_1[i],
                                                                          dice_values[0],
                                                                          player_id)
            action_space_list_move_2 += additional_afterstates

        # Step 2b: determine slots that contain movable pieces of player_id for third move
        action_space_list_move_3 = []
        for i in range(len(action_space_list_move_2)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_move_2[i],
                                                                          dice_values[0],
                                                                          player_id)
            action_space_list_move_3 += additional_afterstates

        # Step 2c: determine slots that contain movable pieces of player_id for third move
        action_space_list_move_4 = []
        for i in range(len(action_space_list_move_3)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_move_3[i],
                                                                          dice_values[0],
                                                                          player_id)
            action_space_list_move_4 += additional_afterstates

        # Step 3: combine all potential afterstates in single structure
        if not action_space_list_move_1:
            combined_afterstates = []
        elif not action_space_list_move_2:
            combined_afterstates = action_space_list_move_1
        elif not action_space_list_move_3:
            combined_afterstates = action_space_list_move_2
        elif not action_space_list_move_4:
            combined_afterstates = action_space_list_move_3
        else:
            combined_afterstates = action_space_list_move_4

    # Step 4: remove repeated entries: convert to set then back to list. Uniqueness guaranteed from Board hash function
    combined_afterstates = list(set(combined_afterstates))

    return combined_afterstates
