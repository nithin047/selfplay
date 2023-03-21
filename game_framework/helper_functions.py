import copy as cp
import random as rd
import numpy as np


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

            if board.is_white_endgame() and potential_next_slot >= board.n_slots:
                if np.all(board.board_state[0, round(board.n_slots*0.75):i] == 0) \
                        or i + dice_value == board.n_slots:
                    potential_next_slot = -1
                else:
                    continue

        # else if black's move
        else:
            potential_next_slot = i - dice_value

            if board.is_black_endgame() and potential_next_slot < 0:
                if np.all(board.board_state[1, (i+1):round(board.n_slots*0.25)] == 0) \
                        or i - dice_value == -1:
                    potential_next_slot = -1
                else:
                    continue

        # copy board object
        potential_next_board_state = cp.deepcopy(board)

        is_move_success = potential_next_board_state.move_piece_from_slot_to_slot(i, potential_next_slot, player_id)
        if is_move_success:
            # add afterstate to list
            afterstates_list.append(potential_next_board_state)

    return afterstates_list


def get_action_space(board, dice_values, player_id):
    # This function returns the complete set of possible afterstates after moving pieces from both dice
    board_copy = cp.deepcopy(board)

    # forced_dice takes a non-zero value whenever player is forced to play only one of the two dice, and needs to
    # play the largest of the two dice values. forced_dice takes the value of the largest of the two values.
    forced_dice = 0

    # record the remaining dice list
    remaining_dice = []

    intermediate_states = []

    # start with the case where both dice have different values
    if dice_values[0] != dice_values[1]:
        # Step 1a: determine slots that contain movable pieces of player_id for dice 0
        action_space_list_dice_0 = get_possible_afterstates_single_dice(board, dice_values[0], player_id)

        # Step 1b: determine slots that contain movable pieces of player_id for dice 1
        action_space_list_dice_1 = get_possible_afterstates_single_dice(board, dice_values[1], player_id)

        # Step 2a: determine slots that contain movable pieces of player_id for dice 1 after moving first piece using
        # dice 0
        action_space_list_dice_0_then_dice_1 = []
        is_dice_0_intermediate_state_eligible = np.zeros((len(action_space_list_dice_0), ))
        for i in range(len(action_space_list_dice_0)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_dice_0[i],
                                                                          dice_values[1],
                                                                          player_id)
            action_space_list_dice_0_then_dice_1 += additional_afterstates
            if additional_afterstates:
                is_dice_0_intermediate_state_eligible[i] = 1
            else:
                is_dice_0_intermediate_state_eligible[i] = 0

        # Step 2b: determine slots that contain movable pieces of player_id for dice 0 after moving first piece using
        # dice 1
        action_space_list_dice_1_then_dice_0 = []
        is_dice_1_intermediate_state_eligible = np.zeros((len(action_space_list_dice_1), ))
        for i in range(len(action_space_list_dice_1)):
            additional_afterstates = get_possible_afterstates_single_dice(action_space_list_dice_1[i],
                                                                          dice_values[0],
                                                                          player_id)
            action_space_list_dice_1_then_dice_0 += additional_afterstates
            if additional_afterstates:
                is_dice_1_intermediate_state_eligible[i] = 1
            else:
                is_dice_1_intermediate_state_eligible[i] = 0

        # Step 3: combine all potential afterstates in single structure
        if not action_space_list_dice_0 and not action_space_list_dice_1:
            combined_afterstates = []
        elif not action_space_list_dice_0_then_dice_1 and not action_space_list_dice_1_then_dice_0:
            if action_space_list_dice_0 and action_space_list_dice_1:
                # if we can only play one die, but not both, force to play the largest value
                if dice_values[0] > dice_values[1]:
                    combined_afterstates = action_space_list_dice_0
                    forced_dice = dice_values[0]
                else:
                    combined_afterstates = action_space_list_dice_1
                    forced_dice = dice_values[1]
            else:
                combined_afterstates = action_space_list_dice_0 + action_space_list_dice_1
        else:
            combined_afterstates = action_space_list_dice_0_then_dice_1 + action_space_list_dice_1_then_dice_0

            # Step 4: save all intermediate states
            filtered_action_space_list_dice_0 = [action_space_list_dice_0[i] for i in range(len(action_space_list_dice_0)) if is_dice_0_intermediate_state_eligible[i]]
            filtered_action_space_list_dice_1 = [action_space_list_dice_1[i] for i in range(len(action_space_list_dice_1)) if is_dice_1_intermediate_state_eligible[i]]
            intermediate_states = filtered_action_space_list_dice_0 + filtered_action_space_list_dice_1
            for i in range(len(filtered_action_space_list_dice_0)):
                remaining_dice.append([dice_values[1]])
            for i in range(len(filtered_action_space_list_dice_1)):
                remaining_dice.append([dice_values[0]])

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

        # Step 4: save all intermediate states
        intermediate_states = action_space_list_move_1 + \
                              action_space_list_move_2 + \
                              action_space_list_move_3

        for i in range(len(action_space_list_move_1)):
            remaining_dice.append([dice_values[0], dice_values[0], dice_values[0]])
        for i in range(len(action_space_list_move_2)):
            remaining_dice.append([dice_values[0], dice_values[0]])
        for i in range(len(action_space_list_move_3)):
            remaining_dice.append([dice_values[0]])

    # Step 5: remove repeated entries: convert to set then back to list. Uniqueness guaranteed from Board hash function
    combined_afterstates = list(set(combined_afterstates))
    combined_afterstates_and_intermediate_states = combined_afterstates + intermediate_states + [board_copy]

    remaining_dice_combined_afterstates = []
    for i in range(len(combined_afterstates)):
        remaining_dice_combined_afterstates.append([])

    remaining_dice = remaining_dice_combined_afterstates + remaining_dice + [dice_values]

    return combined_afterstates, \
           forced_dice, \
           combined_afterstates_and_intermediate_states, \
           remaining_dice


def would_move_get_player_stuck(board, origin, destination, player_id, remaining_dice_move):
    # copy board
    potential_next_board = cp.deepcopy(board)

    # move piece
    is_success = potential_next_board.move_piece_from_slot_to_slot(origin, destination, player_id)

    # check that the move was successful
    assert is_success

    if player_id == 0 and potential_next_board.is_white_endgame():
        return False
    elif player_id == 1 and potential_next_board.is_black_endgame():
        return False

    action_space = get_possible_afterstates_single_dice(potential_next_board, remaining_dice_move, player_id)

    # if action_space is not empty, player is not stuck
    if action_space:
        return False
    else:
        return True
