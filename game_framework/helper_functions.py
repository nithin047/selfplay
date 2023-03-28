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


def get_intermediate_afterstates(board, dice_value, player_id):
    # This function generates all possible partial afterstates, i.e., afterstates after playing a single die.
    afterstates_list = []

    # corresponding_moves_list contains a lost of source-destination pairs corresponding to the afterstate at the same
    # index
    corresponding_moves_list = []

    # loop over all slots on board
    for i in range(board.n_slots):

        # look at where the piece would land
        if player_id == 0:
            potential_next_slot = i + dice_value

            if board.is_white_endgame() and potential_next_slot >= board.n_slots:
                if (np.all(board.board_state[0, 18:i] == 0) and i >= 18) \
                        or i + dice_value == board.n_slots:
                    potential_next_slot = -1
                else:
                    continue

        # else if black's move
        else:
            potential_next_slot = i - dice_value

            if board.is_black_endgame() and potential_next_slot < 0:
                if (np.all(board.board_state[1, (i + 1):6] == 0) and i < 6) \
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
            corresponding_moves_list.append([i, potential_next_slot])

    return afterstates_list, corresponding_moves_list


# def get_action_space2(board, dice_values, player_id):
#     # This function returns the complete set of possible afterstates after moving pieces from both dice
#     board_copy = cp.deepcopy(board)
#
#     # record the remaining dice list
#     remaining_dice = []
#
#     # record the intermediate states list
#     intermediate_states = []
#
#     # afterstate source-destination pair list
#     afterstate_origin_destination_pair_list = []
#
#     # start with the case where both dice have different values
#     if dice_values[0] != dice_values[1]:
#         # Step 1a: determine slots that contain movable pieces of player_id for dice 0
#         action_space_list_dice_0, corresponding_moves_list_dice_0 = get_intermediate_afterstates(board, dice_values[0], player_id)
#
#         # Step 1b: determine slots that contain movable pieces of player_id for dice 1
#         action_space_list_dice_1, corresponding_moves_list_dice_1 = get_intermediate_afterstates(board, dice_values[1], player_id)
#
#         # Step 2a: determine slots that contain movable pieces of player_id for dice 1 after moving first piece using
#         # dice 0
#         action_space_list_dice_0_then_dice_1 = []
#         afterstate_origin_destination_pair_list_dice_0_then_dice_1 = []
#         is_dice_0_intermediate_state_eligible = np.zeros((len(action_space_list_dice_0), ))
#         for i in range(len(action_space_list_dice_0)):
#             additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(action_space_list_dice_0[i],
#                                                                           dice_values[1],
#                                                                           player_id)
#             action_space_list_dice_0_then_dice_1 += additional_afterstates
#
#             for j in range(len(corresponding_moves_list_additional_afterstates)):
#                 previous_state_destination_pair = [cp.deepcopy(corresponding_moves_list_dice_0)[i], corresponding_moves_list_additional_afterstates[j]]
#                 afterstate_origin_destination_pair_list_dice_0_then_dice_1 += [previous_state_destination_pair]
#
#             if additional_afterstates:
#                 is_dice_0_intermediate_state_eligible[i] = 1
#             else:
#                 is_dice_0_intermediate_state_eligible[i] = 0
#
#         # Step 2b: determine slots that contain movable pieces of player_id for dice 0 after moving first piece using
#         # dice 1
#         action_space_list_dice_1_then_dice_0 = []
#         afterstate_origin_destination_pair_list_dice_1_then_dice_0 = []
#         is_dice_1_intermediate_state_eligible = np.zeros((len(action_space_list_dice_1), ))
#         for i in range(len(action_space_list_dice_1)):
#             additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(action_space_list_dice_1[i],
#                                                                           dice_values[0],
#                                                                           player_id)
#             action_space_list_dice_1_then_dice_0 += additional_afterstates
#
#             for j in range(len(corresponding_moves_list_additional_afterstates)):
#                 previous_state_destination_pair = [cp.deepcopy(corresponding_moves_list_dice_1)[i], corresponding_moves_list_additional_afterstates[j]]
#                 afterstate_origin_destination_pair_list_dice_1_then_dice_0 += [previous_state_destination_pair]
#
#             if additional_afterstates:
#                 is_dice_1_intermediate_state_eligible[i] = 1
#             else:
#                 is_dice_1_intermediate_state_eligible[i] = 0
#
#         # Step 3: combine all potential afterstates in single structure
#         if not action_space_list_dice_0 and not action_space_list_dice_1:
#             combined_afterstates = []
#             afterstate_origin_destination_pair_list = []
#         elif not action_space_list_dice_0_then_dice_1 and not action_space_list_dice_1_then_dice_0:
#             if action_space_list_dice_0 and action_space_list_dice_1:
#                 # if we can only play one die, but not both, force to play the largest value
#                 if dice_values[0] > dice_values[1]:
#                     combined_afterstates = action_space_list_dice_0
#                     afterstate_origin_destination_pair_list = corresponding_moves_list_dice_0
#                 else:
#                     combined_afterstates = action_space_list_dice_1
#                     afterstate_origin_destination_pair_list = corresponding_moves_list_dice_1
#             else:
#                 combined_afterstates = action_space_list_dice_0 + action_space_list_dice_1
#                 afterstate_origin_destination_pair_list = corresponding_moves_list_dice_0 + corresponding_moves_list_dice_1
#         else:
#             combined_afterstates = action_space_list_dice_0_then_dice_1 + action_space_list_dice_1_then_dice_0
#             afterstate_origin_destination_pair_list = afterstate_origin_destination_pair_list_dice_0_then_dice_1 + afterstate_origin_destination_pair_list_dice_1_then_dice_0
#
#             # Step 4: save all intermediate states
#             filtered_action_space_list_dice_0 = [action_space_list_dice_0[i] for i in range(len(action_space_list_dice_0)) if is_dice_0_intermediate_state_eligible[i]]
#             filtered_action_space_list_dice_1 = [action_space_list_dice_1[i] for i in range(len(action_space_list_dice_1)) if is_dice_1_intermediate_state_eligible[i]]
#             intermediate_states = filtered_action_space_list_dice_0 + filtered_action_space_list_dice_1
#             for i in range(len(filtered_action_space_list_dice_0)):
#                 remaining_dice.append([dice_values[1]])
#             for i in range(len(filtered_action_space_list_dice_1)):
#                 remaining_dice.append([dice_values[0]])
#
#     # else, if the dice have the same value
#     else:
#         # Step 1: determine slots that contain movable pieces of player_id for first move
#         action_space_list_move_1, afterstate_origin_destination_pair_list_move_1 = get_intermediate_afterstates(board, dice_values[0], player_id)
#
#         # Step 2a: determine slots that contain movable pieces of player_id for second move
#         action_space_list_move_2 = []
#         afterstate_origin_destination_pair_list_move_2 = []
#         for i in range(len(action_space_list_move_1)):
#             additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(action_space_list_move_1[i],
#                                                                           dice_values[0],
#                                                                           player_id)
#             action_space_list_move_2 += additional_afterstates
#
#             for j in range(len(corresponding_moves_list_additional_afterstates)):
#                 previous_state_destination_pair = [cp.deepcopy(afterstate_origin_destination_pair_list_move_1)[i], corresponding_moves_list_additional_afterstates[j]]
#                 afterstate_origin_destination_pair_list_move_2 += [previous_state_destination_pair]
#
#         # Step 2b: determine slots that contain movable pieces of player_id for third move
#         action_space_list_move_3 = []
#         afterstate_origin_destination_pair_list_move_3 = []
#         for i in range(len(action_space_list_move_2)):
#             additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(action_space_list_move_2[i],
#                                                                           dice_values[0],
#                                                                           player_id)
#             action_space_list_move_3 += additional_afterstates
#
#             for j in range(len(corresponding_moves_list_additional_afterstates)):
#                 previous_state_destination_pair = cp.deepcopy(afterstate_origin_destination_pair_list_move_2)[i]
#                 previous_state_destination_pair.append(corresponding_moves_list_additional_afterstates[j])
#                 afterstate_origin_destination_pair_list_move_3 += [previous_state_destination_pair]
#
#         # Step 2c: determine slots that contain movable pieces of player_id for fourth move
#         action_space_list_move_4 = []
#         afterstate_origin_destination_pair_list_move_4 = []
#         for i in range(len(action_space_list_move_3)):
#             additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(action_space_list_move_3[i],
#                                                                           dice_values[0],
#                                                                           player_id)
#             action_space_list_move_4 += additional_afterstates
#
#             for j in range(len(corresponding_moves_list_additional_afterstates)):
#                 previous_state_destination_pair = cp.deepcopy(afterstate_origin_destination_pair_list_move_3)[i]
#                 previous_state_destination_pair.append(corresponding_moves_list_additional_afterstates[j])
#                 afterstate_origin_destination_pair_list_move_4 += [previous_state_destination_pair]
#
#         # Step 3: combine all potential afterstates in single structure
#         if not action_space_list_move_1:
#             combined_afterstates = []
#             afterstate_origin_destination_pair_list = []
#         elif not action_space_list_move_2:
#             combined_afterstates = action_space_list_move_1
#             afterstate_origin_destination_pair_list = afterstate_origin_destination_pair_list_move_1
#         elif not action_space_list_move_3:
#             combined_afterstates = action_space_list_move_2
#             afterstate_origin_destination_pair_list = afterstate_origin_destination_pair_list_move_2
#         elif not action_space_list_move_4:
#             combined_afterstates = action_space_list_move_3
#             afterstate_origin_destination_pair_list = afterstate_origin_destination_pair_list_move_3
#         else:
#             combined_afterstates = action_space_list_move_4
#             afterstate_origin_destination_pair_list = afterstate_origin_destination_pair_list_move_4
#
#         # Step 4: save all intermediate states
#         intermediate_states = action_space_list_move_1 + \
#                               action_space_list_move_2 + \
#                               action_space_list_move_3
#
#         for i in range(len(action_space_list_move_1)):
#             remaining_dice.append([dice_values[0], dice_values[0], dice_values[0]])
#         for i in range(len(action_space_list_move_2)):
#             remaining_dice.append([dice_values[0], dice_values[0]])
#         for i in range(len(action_space_list_move_3)):
#             remaining_dice.append([dice_values[0]])
#
#     # Step 5: remove repeated entries: convert to set then back to list. Uniqueness guaranteed from Board hash function
#     combined_afterstates_copy = cp.deepcopy(combined_afterstates)
#     combined_afterstates = list(set(combined_afterstates))
#     combined_afterstates_and_intermediate_states = combined_afterstates + intermediate_states + [board_copy]
#
#     afterstate_origin_destination_pair_list_simplified = [[]] * len(combined_afterstates)
#     for i in range(len(combined_afterstates)):
#         for j in range(len(combined_afterstates_copy)):
#             if combined_afterstates[i] == combined_afterstates_copy[j]:
#                 afterstate_origin_destination_pair_list_simplified[i] = afterstate_origin_destination_pair_list[j]
#                 break
#
#     remaining_dice_combined_afterstates = []
#     for i in range(len(combined_afterstates)):
#         remaining_dice_combined_afterstates.append([])
#
#     remaining_dice = remaining_dice_combined_afterstates + remaining_dice + [dice_values]
#
#     return combined_afterstates, \
#            afterstate_origin_destination_pair_list_simplified, \
#            combined_afterstates_and_intermediate_states, \
#            remaining_dice


def get_action_space(board, dice_values, player_id):
    # This function returns the complete set of possible afterstates after moving pieces from both dice
    board_copy = cp.deepcopy(board)

    # record the remaining dice list
    remaining_dice = []

    # record the intermediate states list
    intermediate_states = []

    # start with the case where both dice have different values
    if dice_values[0] != dice_values[1]:
        # Step 1a: determine slots that contain movable pieces of player_id for dice 0
        action_space_list_dice_0, corresponding_moves_list_dice_0 = get_intermediate_afterstates(board, dice_values[0],
                                                                                                 player_id)

        # Step 1b: determine slots that contain movable pieces of player_id for dice 1
        action_space_list_dice_1, corresponding_moves_list_dice_1 = get_intermediate_afterstates(board, dice_values[1],
                                                                                                 player_id)

        # Step 2a: determine slots that contain movable pieces of player_id for dice 1 after moving first piece using
        # dice 0
        action_space_list_dice_0_then_dice_1 = []
        is_dice_0_intermediate_state_eligible = np.zeros((len(action_space_list_dice_0),))
        for i in range(len(action_space_list_dice_0)):
            additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(
                action_space_list_dice_0[i],
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
        is_dice_1_intermediate_state_eligible = np.zeros((len(action_space_list_dice_1),))
        for i in range(len(action_space_list_dice_1)):
            additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(
                action_space_list_dice_1[i],
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
                else:
                    combined_afterstates = action_space_list_dice_1
            else:
                combined_afterstates = action_space_list_dice_0 + action_space_list_dice_1
        else:
            combined_afterstates = action_space_list_dice_0_then_dice_1 + action_space_list_dice_1_then_dice_0

            # Step 4: save all intermediate states
            filtered_action_space_list_dice_0 = [action_space_list_dice_0[i] for i in
                                                 range(len(action_space_list_dice_0)) if
                                                 is_dice_0_intermediate_state_eligible[i]]
            filtered_action_space_list_dice_1 = [action_space_list_dice_1[i] for i in
                                                 range(len(action_space_list_dice_1)) if
                                                 is_dice_1_intermediate_state_eligible[i]]
            intermediate_states = filtered_action_space_list_dice_0 + filtered_action_space_list_dice_1
            for i in range(len(filtered_action_space_list_dice_0)):
                remaining_dice.append([dice_values[1]])
            for i in range(len(filtered_action_space_list_dice_1)):
                remaining_dice.append([dice_values[0]])

    # else, if the dice have the same value
    else:
        # Step 1: determine slots that contain movable pieces of player_id for first move
        action_space_list_move_1, \
          afterstate_origin_destination_pair_list_move_1 = get_intermediate_afterstates(board,
                                                                                        dice_values[0],
                                                                                        player_id)

        # Step 2a: determine slots that contain movable pieces of player_id for second move
        action_space_list_move_2 = []
        for i in range(len(action_space_list_move_1)):
            additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(
                action_space_list_move_1[i],
                dice_values[0],
                player_id)
            action_space_list_move_2 += additional_afterstates

        # Step 2b: determine slots that contain movable pieces of player_id for third move
        action_space_list_move_3 = []
        for i in range(len(action_space_list_move_2)):
            additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(
                action_space_list_move_2[i],
                dice_values[0],
                player_id)
            action_space_list_move_3 += additional_afterstates

        # Step 2c: determine slots that contain movable pieces of player_id for fourth move
        action_space_list_move_4 = []
        for i in range(len(action_space_list_move_3)):
            additional_afterstates, corresponding_moves_list_additional_afterstates = get_intermediate_afterstates(
                action_space_list_move_3[i],
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
           combined_afterstates_and_intermediate_states, \
           remaining_dice


def determine_moves_from_board_change(start_board, end_board, dice_roll, player_id, enable_check):
    position_diff = end_board.board_state[player_id, :] - start_board.board_state[player_id, :]

    initial_slot_id_list = []
    destination_slot_id_list = []

    for i in range(len(position_diff)):
        if position_diff[i] > 0:
            for j in range(position_diff[i]):
                destination_slot_id_list.append(i)
        elif position_diff[i] < 0:
            for j in range(-1 * position_diff[i]):
                initial_slot_id_list.append(i)

    initial_slot_id_list.sort()
    destination_slot_id_list.sort()

    if dice_roll[0] != dice_roll[1]:

        # if dice are different, then initial_slot_id_list can only have a length of 2, 1, or 0
        assert (len(initial_slot_id_list) <= 2)
        assert (len(destination_slot_id_list) <= len(initial_slot_id_list))

        if len(initial_slot_id_list) == 2:
            if len(destination_slot_id_list) == 2:

                if (abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[0]
                    and abs(initial_slot_id_list[1] - destination_slot_id_list[1]) == dice_roll[1]) \
                        or (abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[1]
                            and abs(initial_slot_id_list[1] - destination_slot_id_list[1]) == dice_roll[0]):

                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                               [initial_slot_id_list[1], destination_slot_id_list[1]]]

                elif (abs(initial_slot_id_list[0] - destination_slot_id_list[1]) == dice_roll[0]
                      and abs(initial_slot_id_list[1] - destination_slot_id_list[0]) == dice_roll[1]) \
                        or (abs(initial_slot_id_list[0] - destination_slot_id_list[1]) == dice_roll[1]
                            and abs(initial_slot_id_list[1] - destination_slot_id_list[0]) == dice_roll[0]):

                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[1]],
                                               [initial_slot_id_list[1], destination_slot_id_list[0]]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 1:
                if (abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[0]) \
                        or (abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[1]):

                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                               [initial_slot_id_list[1], -1]]

                elif (abs(initial_slot_id_list[1] - destination_slot_id_list[0]) == dice_roll[0]) \
                        or (abs(initial_slot_id_list[1] - destination_slot_id_list[0]) == dice_roll[1]):

                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], destination_slot_id_list[0]]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 0:
                source_destination_list = [[initial_slot_id_list[1], -1],
                                           [initial_slot_id_list[0], -1]]

            else:
                assert False

        elif len(initial_slot_id_list) == 1:
            if len(destination_slot_id_list) == 1:
                if abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[0] or \
                        abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == dice_roll[1] or \
                        abs(initial_slot_id_list[0] - destination_slot_id_list[0]) == (dice_roll[0] + dice_roll[1]):

                    source_destination_list = [initial_slot_id_list[0], destination_slot_id_list[0]]

                else:
                    assert False

            elif len(destination_slot_id_list) == 0:
                source_destination_list = [initial_slot_id_list[0], -1]

            else:
                assert False

        elif len(initial_slot_id_list) == 0:
            if len(destination_slot_id_list) == 0:
                source_destination_list = []
            else:
                assert False

        else:
            assert False

    else:
        dice_val = dice_roll[0]

        # if dice are the same, then initial_slot_id_list can only have a length of 4, 3, 2, 1, or 0
        assert (len(initial_slot_id_list) <= 4)
        assert (len(destination_slot_id_list) <= len(initial_slot_id_list))

        if len(initial_slot_id_list) == 4:
            if len(destination_slot_id_list) == 4:
                source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                           [initial_slot_id_list[1], destination_slot_id_list[1]],
                                           [initial_slot_id_list[2], destination_slot_id_list[2]],
                                           [initial_slot_id_list[3], destination_slot_id_list[3]]]

            elif len(destination_slot_id_list) == 3:

                if player_id == 0:
                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                               [initial_slot_id_list[1], destination_slot_id_list[1]],
                                               [initial_slot_id_list[2], destination_slot_id_list[2]],
                                               [initial_slot_id_list[3], -1]]
                elif player_id == 1:
                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], destination_slot_id_list[1]],
                                               [initial_slot_id_list[2], destination_slot_id_list[2]],
                                               [initial_slot_id_list[3], destination_slot_id_list[3]]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 2:
                if player_id == 0:
                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                               [initial_slot_id_list[1], destination_slot_id_list[1]],
                                               [initial_slot_id_list[2], -1],
                                               [initial_slot_id_list[3], -1]]
                elif player_id == 1:
                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], -1],
                                               [initial_slot_id_list[2], destination_slot_id_list[2]],
                                               [initial_slot_id_list[3], destination_slot_id_list[3]]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 1:
                if player_id == 0:
                    source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]],
                                               [initial_slot_id_list[1], -1],
                                               [initial_slot_id_list[2], -1],
                                               [initial_slot_id_list[3], -1]]
                elif player_id == 1:
                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], -1],
                                               [initial_slot_id_list[2], -1],
                                               [initial_slot_id_list[3], destination_slot_id_list[3]]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 0:
                if player_id == 0:
                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], -1],
                                               [initial_slot_id_list[2], -1],
                                               [initial_slot_id_list[3], -1]]
                elif player_id == 1:
                    source_destination_list = [[initial_slot_id_list[0], -1],
                                               [initial_slot_id_list[1], -1],
                                               [initial_slot_id_list[2], -1],
                                               [initial_slot_id_list[3], -1]]
                else:
                    assert False

            else:
                assert False

        elif len(initial_slot_id_list) == 3:

            potential_dest_list_1 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[2] + 2 * dice_val * mark_player_pinning(player_id)]

            potential_dest_list_2 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(player_id)]

            potential_dest_list_3 = [initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(player_id)]

            potential_dest_list_4 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(player_id)]

            potential_dest_list_1.sort()
            potential_dest_list_2.sort()
            potential_dest_list_3.sort()
            potential_dest_list_4.sort()

            if len(destination_slot_id_list) == 3:

                if destination_slot_id_list == potential_dest_list_1:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[2],
                                                initial_slot_id_list[2] + 2 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_2:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[2],
                                                initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_3:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[2],
                                                initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_4:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[2],
                                                initial_slot_id_list[2] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]

                else:
                    assert False

            elif len(destination_slot_id_list) == 2:

                if player_id == 0:

                    if destination_slot_id_list == potential_dest_list_1[0:1] and potential_dest_list_1[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] + 1 * dice_val],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_2[0:1] and potential_dest_list_2[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] + 2 * dice_val],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_3[0:1] and potential_dest_list_3[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 2 * dice_val],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] + 1 * dice_val],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_4[0:1] and potential_dest_list_4[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] + 1 * dice_val],
                                                   [initial_slot_id_list[2], -1]]

                    else:
                        assert False

                elif player_id == 1:
                    if destination_slot_id_list == potential_dest_list_1[1:2] and potential_dest_list_1[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 2 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_2[1:2] and potential_dest_list_2[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 2 * dice_val],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_3[1:2] and potential_dest_list_3[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_4[1:2] and potential_dest_list_3[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]
                    else:
                        assert False

                else:
                    assert False

            elif len(destination_slot_id_list) == 1:

                if player_id == 0:

                    if destination_slot_id_list == potential_dest_list_1[0] and potential_dest_list_1[1] >= len(position_diff) and potential_dest_list_1[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_2[0] and potential_dest_list_2[1] >= len(position_diff) and potential_dest_list_2[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_3[0] and potential_dest_list_3[1] >= len(position_diff) and potential_dest_list_3[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 2 * dice_val],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], -1]]

                    elif destination_slot_id_list == potential_dest_list_4[0] and potential_dest_list_4[1] >= len(position_diff) and potential_dest_list_4[2] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], -1]]
                    else:
                        assert False

                elif player_id == 1:
                    if destination_slot_id_list == potential_dest_list_1[2] and potential_dest_list_1[0] < 0 and potential_dest_list_1[1] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 2 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_2[2] and potential_dest_list_2[0] < 0 and potential_dest_list_2[1] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_3[2] and potential_dest_list_3[0] < 0 and potential_dest_list_3[1] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_4[2] and potential_dest_list_4[0] < 0 and potential_dest_list_4[1] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], -1],
                                                   [initial_slot_id_list[2], initial_slot_id_list[1] - 1 * dice_val]]
                    else:
                        assert False

                else:
                    assert False

            elif len(destination_slot_id_list) == 0:
                source_destination_list = [[initial_slot_id_list[0], -1],
                                           [initial_slot_id_list[1], -1],
                                           [initial_slot_id_list[2], -1]]

            else:
                assert False

        elif len(initial_slot_id_list) == 2:

            potential_dest_list_1 = [initial_slot_id_list[0] + 3 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id)].sort()

            potential_dest_list_2 = [initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(player_id)].sort()

            potential_dest_list_3 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 3 * dice_val * mark_player_pinning(player_id)].sort()

            potential_dest_list_4 = [initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id)].sort()

            potential_dest_list_5 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(player_id)].sort()

            potential_dest_list_6 = [initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(player_id),
                                     initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(player_id)].sort()

            if len(destination_slot_id_list) == 2:
                if destination_slot_id_list == potential_dest_list_1:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 3 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_2:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_3:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 3 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_4:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 2 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_5:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 2 * dice_val * mark_player_pinning(
                                                    player_id)]]

                elif destination_slot_id_list == potential_dest_list_6:
                    source_destination_list = [[initial_slot_id_list[0],
                                                initial_slot_id_list[0] + 1 * dice_val * mark_player_pinning(
                                                    player_id)],
                                               [initial_slot_id_list[1],
                                                initial_slot_id_list[1] + 1 * dice_val * mark_player_pinning(
                                                    player_id)]]
                else:
                    assert False

            elif len(destination_slot_id_list) == 1:

                if player_id == 0:

                    if destination_slot_id_list == potential_dest_list_1[0] \
                            and potential_dest_list_1[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 3 * dice_val],
                                                   [initial_slot_id_list[1], -1]]

                    elif destination_slot_id_list == potential_dest_list_2[0] \
                            and potential_dest_list_2[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 2 * dice_val],
                                                   [initial_slot_id_list[1], -1]]

                    elif destination_slot_id_list == potential_dest_list_3[0] \
                            and potential_dest_list_3[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1]]

                    elif destination_slot_id_list == potential_dest_list_4[0] \
                            and potential_dest_list_4[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 2 * dice_val],
                                                   [initial_slot_id_list[1], -1]]

                    elif destination_slot_id_list == potential_dest_list_5[0] \
                            and potential_dest_list_5[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1]]

                    elif destination_slot_id_list == potential_dest_list_6[0] \
                            and potential_dest_list_6[1] >= len(position_diff):
                        source_destination_list = [[initial_slot_id_list[0], initial_slot_id_list[0] + 1 * dice_val],
                                                   [initial_slot_id_list[1], -1]]
                    else:
                        assert False

                elif player_id == 1:
                    if destination_slot_id_list == potential_dest_list_1[1] and potential_dest_list_1[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 3 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_2[1] and potential_dest_list_2[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 2 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_3[1] and potential_dest_list_3[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_4[1] and potential_dest_list_4[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 2 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_5[1] and potential_dest_list_5[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val]]

                    elif destination_slot_id_list == potential_dest_list_6[1] and potential_dest_list_6[0] < 0:
                        source_destination_list = [[initial_slot_id_list[0], -1],
                                                   [initial_slot_id_list[1], initial_slot_id_list[1] - 1 * dice_val]]
                    else:
                        assert False

                else:
                    assert False

            elif len(destination_slot_id_list) == 0:
                source_destination_list = [[initial_slot_id_list[0], -1],
                                           [initial_slot_id_list[1], -1]]

            else:
                assert False

        elif len(initial_slot_id_list) == 1:

            if len(destination_slot_id_list) == 1:
                source_destination_list = [[initial_slot_id_list[0], destination_slot_id_list[0]]]

            elif len(destination_slot_id_list) == 0:
                source_destination_list = [[initial_slot_id_list[0], -1]]

            else:
                assert False

        elif len(initial_slot_id_list) == 0:
            source_destination_list = []

        else:
            assert False

    if enable_check:
        # Now make sure there was no mistake
        start_board_copy = cp.deepcopy(start_board)

        if player_id == 0:
            for i in range(len(source_destination_list)):
                is_success = start_board_copy.move_piece_from_slot_to_slot(source_destination_list[i][0],
                                                                           source_destination_list[i][1],
                                                                           player_id)
                assert is_success
        elif player_id == 1:
            for i in range(len(source_destination_list)-1, -1, -1):
                is_success = start_board_copy.move_piece_from_slot_to_slot(source_destination_list[i][0],
                                                                           source_destination_list[i][1],
                                                                           player_id)
                assert is_success
        else:
            assert False
        assert start_board_copy == end_board

    return source_destination_list
