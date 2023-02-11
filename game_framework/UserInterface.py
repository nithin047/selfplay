import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from game_framework.GameManager import GameState
import logging
import copy as cp


def compute_position_grid_coordinates():
    horizontal_position_grid = np.zeros((7, 24))
    vertical_position_grid = np.zeros((7, 24))

    small_horizontal_delta = 34 / 612
    large_horizontal_delta = 54.5 / 612
    vertical_delta = 23 / 612

    horizontal_position_grid[0, 0] = 109 / 612
    vertical_position_grid[0, 0] = 455 / 612
    horizontal_position_grid[0, 23] = 109 / 612
    vertical_position_grid[0, 23] = 134 / 612

    for i in range(12):
        for j in range(7):
            if j > 0:
                horizontal_position_grid[j, i] = horizontal_position_grid[j - 1, i]
                vertical_position_grid[j, i] = vertical_position_grid[j - 1, i] - vertical_delta
        if not i == 5:
            horizontal_position_grid[0, i + 1] = horizontal_position_grid[0, i] + small_horizontal_delta
            vertical_position_grid[0, i + 1] = vertical_position_grid[0, i]
        else:
            horizontal_position_grid[0, i + 1] = horizontal_position_grid[0, i] + large_horizontal_delta
            vertical_position_grid[0, i + 1] = vertical_position_grid[0, i]

    for i in range(12):
        for j in range(7):
            if j > 0:
                horizontal_position_grid[j, 23 - i] = horizontal_position_grid[(j - 1), 23 - i]
                vertical_position_grid[j, 23 - i] = vertical_position_grid[(j - 1), 23 - i] + vertical_delta
        if not i == 11:
            if not i == 5:
                horizontal_position_grid[0, 23 - (i + 1)] = horizontal_position_grid[
                                                                0, 23 - i] + small_horizontal_delta
                vertical_position_grid[0, 23 - (i + 1)] = vertical_position_grid[0, 23 - i]
            else:
                horizontal_position_grid[0, 23 - (i + 1)] = horizontal_position_grid[
                                                                0, 23 - i] + large_horizontal_delta
                vertical_position_grid[0, 23 - (i + 1)] = vertical_position_grid[0, 23 - i]

    return horizontal_position_grid, vertical_position_grid


def compute_dice_button_coordinates():
    # 1st entry: entry left horizontal
    # 2nd entry: lower left vertical
    # 3rd entry: upper right horizontal
    # 4th entry: upper right vertical

    corner_coordinates = np.zeros((4, 1))
    corner_coordinates[0] = (250 / 612)
    corner_coordinates[1] = (30 / 612) + 0.1
    corner_coordinates[2] = (320 / 612) + 0.1
    corner_coordinates[3] = (30 / 612)

    return corner_coordinates


def compute_white_exit_arrow_button_coordinates():
    # 1st entry: entry left horizontal
    # 2nd entry: lower left vertical
    # 3rd entry: upper right horizontal
    # 4th entry: upper right vertical

    corner_coordinates = np.zeros((4, 1))
    corner_coordinates[0] = (10 / 612)
    corner_coordinates[1] = (183 / 612) + 0.1
    corner_coordinates[2] = (10 / 612) + 0.1
    corner_coordinates[3] = (183 / 612)

    return corner_coordinates


def compute_black_exit_arrow_button_coordinates():
    # 1st entry: entry left horizontal
    # 2nd entry: lower left vertical
    # 3rd entry: upper right horizontal
    # 4th entry: upper right vertical

    corner_coordinates = np.zeros((4, 1))
    corner_coordinates[0] = (10 / 612)
    corner_coordinates[1] = (368 / 612) + 0.1
    corner_coordinates[2] = (10 / 612) + 0.1
    corner_coordinates[3] = (368 / 612)

    return corner_coordinates


class UserInterface:

    def __init__(self, game_manager):

        self.game_manager = game_manager
        self.n_slots = game_manager.game_board.n_slots
        self.graphic_board_matrix = np.zeros((7, self.n_slots))

        self.dice_vals = cp.deepcopy(self.game_manager.current_dice)
        self.board_to_graphics()

        self.horizontal_position_grid, self.vertical_position_grid = compute_position_grid_coordinates()
        self.slot_button_rectangle_coordinates = self.compute_rectangle_button_coordinates()
        self.dice_button_rectangle_coordinates = compute_dice_button_coordinates()
        self.white_exit_arrow_rectangle_coordinates = compute_white_exit_arrow_button_coordinates()
        self.black_exit_arrow_rectangle_coordinates = compute_black_exit_arrow_button_coordinates()

        # setup GUI
        self.window = tk.Tk()
        self.window.title("Backgammon")
        self.window.geometry("612x612")
        self.original_image_dimensions = [612, 612]
        self.current_background_dimension = 612

        self.last_event_height = 612
        self.last_event_width = 612

        self.background_frame = Frame(self.window)
        self.background_frame.pack(fill=BOTH, expand=YES)
        self.background_frame.bind('<Configure>', self.resize_image)

        self.board_canvas = Canvas(self.background_frame)
        self.board_canvas.pack(fill=BOTH, expand=YES)

        # initialize class attributes
        self.backgammon_board_background_image = None
        self.img_copy_background = None
        self.board_image = None
        self.white_piece_image = []
        self.black_piece_image = []
        self.dice_image = []
        self.img_copy_white_piece = []
        self.img_copy_black_piece = []
        self.img_copy_dice = []
        self.white_piece_image_foreground = []
        self.black_piece_image_foreground = []
        self.white_exit_arrow_image = None
        self.img_copy_white_exit_arrow = None
        self.white_exit_arrow = None
        self.black_exit_arrow_image = None
        self.img_copy_black_exit_arrow = None
        self.black_exit_arrow = None
        self.white_piece_selected_image = None
        self.img_copy_white_piece_selected = None
        self.white_piece_selected = None
        self.black_piece_selected_image = None
        self.img_copy_black_piece_selected = None
        self.black_piece_selected = None

        self.dice_1_image = []
        self.dice_2_image = []
        self.dice_1_image_foreground = []
        self.dice_2_image_foreground = []

        self.load_media_files()

        self.normalized_piece_width = 0.033
        self.normalized_piece_height = 0.033
        self.normalized_dice_width = 0.1
        self.normalized_dice_height = 0.1
        self.normalized_arrow_width = 0.1
        self.normalized_arrow_height = 0.1

        self.board_canvas.create_image(0, 0, image=self.backgammon_board_background_image)

        self.slot_button_coordinates = self.get_slot_button_coordinates()
        self.dice_button_coordinates = self.get_dice_button_coordinates()
        self.white_exit_arrow_button_coordinates = self.get_white_exit_arrow_button_coordinates()
        self.black_exit_arrow_button_coordinates = self.get_black_exit_arrow_button_coordinates()

        self.board_canvas.bind("<Button-1>", self.on_button_click)

        self.window.mainloop()

    def load_media_files(self):
        # this function loads image files into the class attributes

        self.board_image = Image.open("Media Files/backgammon_board2.jpg")
        self.img_copy_background = self.board_image.copy()
        self.backgammon_board_background_image = ImageTk.PhotoImage(self.board_image)

        self.white_piece_image.append(Image.open("Media Files/white_piece.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_2.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_3.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_4.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_5.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_6.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_7.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_8.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_9.png"))
        self.white_piece_image.append(Image.open("Media Files/white_piece_10.png"))

        self.black_piece_image.append(Image.open("Media Files/black_piece.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_2.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_3.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_4.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_5.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_6.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_7.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_8.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_9.png"))
        self.black_piece_image.append(Image.open("Media Files/black_piece_10.png"))

        self.dice_image.append(Image.open("Media Files/dice_1.png"))
        self.dice_image.append(Image.open("Media Files/dice_2.png"))
        self.dice_image.append(Image.open("Media Files/dice_3.png"))
        self.dice_image.append(Image.open("Media Files/dice_4.png"))
        self.dice_image.append(Image.open("Media Files/dice_5.png"))
        self.dice_image.append(Image.open("Media Files/dice_6.png"))

        self.white_exit_arrow = Image.open("Media Files/white_exit_arrow.png")
        self.img_copy_white_exit_arrow = self.white_exit_arrow.copy()
        self.white_exit_arrow_image = ImageTk.PhotoImage(self.white_exit_arrow)

        self.black_exit_arrow = Image.open("Media Files/black_exit_arrow.png")
        self.img_copy_black_exit_arrow = self.black_exit_arrow.copy()
        self.black_exit_arrow_image = ImageTk.PhotoImage(self.black_exit_arrow)

        self.white_piece_selected = Image.open("Media Files/selected_white_piece.png")
        self.img_copy_white_piece_selected = self.white_piece_selected.copy()
        self.white_piece_selected_image = ImageTk.PhotoImage(self.white_piece_selected)

        self.black_piece_selected = Image.open("Media Files/selected_black_piece.png")
        self.img_copy_black_piece_selected = self.black_piece_selected.copy()
        self.black_piece_selected_image = ImageTk.PhotoImage(self.black_piece_selected)

        for i in range(10):
            self.img_copy_white_piece.append(self.white_piece_image[i].copy())
            self.img_copy_black_piece.append(self.black_piece_image[i].copy())
            self.white_piece_image_foreground.append(ImageTk.PhotoImage(self.white_piece_image[i]))
            self.black_piece_image_foreground.append(ImageTk.PhotoImage(self.black_piece_image[i]))

        for i in range(6):
            self.img_copy_dice.append(self.dice_image[i].copy())

        self.dice_1_image_foreground = ImageTk.PhotoImage(self.dice_image[self.dice_vals[0] - 1])
        self.dice_2_image_foreground = ImageTk.PhotoImage(self.dice_image[self.dice_vals[1] - 1])

    def on_refresh_gui_event(self):

        self.board_to_graphics()

        if self.last_event_height * self.original_image_dimensions[1] < \
                self.last_event_width * self.original_image_dimensions[0]:
            new_width_background = round(
                self.last_event_height * self.original_image_dimensions[1] / self.original_image_dimensions[0])
            new_height_background = self.last_event_height
        else:
            new_height_background = round(
                self.last_event_width * self.original_image_dimensions[0] / self.original_image_dimensions[1])
            new_width_background = self.last_event_width

        self.current_background_dimension = new_width_background

        new_width_piece = round(self.normalized_piece_width * new_width_background)
        new_height_piece = round(self.normalized_piece_height * new_height_background)

        self.board_image = self.img_copy_background.resize((new_width_background, new_height_background))
        self.backgammon_board_background_image = ImageTk.PhotoImage(self.board_image)
        self.board_canvas.create_image(0, 0, image=self.backgammon_board_background_image, anchor='nw')

        new_width_dice = round(self.normalized_dice_width * new_width_background)
        new_height_dice = round(self.normalized_dice_height * new_height_background)

        self.dice_1_image = self.img_copy_dice[self.dice_vals[0] - 1].resize((new_width_dice, new_height_dice))
        self.dice_1_image_foreground = ImageTk.PhotoImage(self.dice_1_image)
        self.board_canvas.create_image(round((250 / 612) * new_width_background),
                                       round((30 / 612) * new_height_background),
                                       image=self.dice_1_image_foreground, anchor='nw')

        self.dice_2_image = self.img_copy_dice[self.dice_vals[1] - 1].resize((new_width_dice, new_height_dice))
        self.dice_2_image_foreground = ImageTk.PhotoImage(self.dice_2_image)
        self.board_canvas.create_image(round((320 / 612) * new_width_background),
                                       round((30 / 612) * new_height_background),
                                       image=self.dice_2_image_foreground, anchor='nw')

        for i in range(10):
            self.white_piece_image[i] = self.img_copy_white_piece[i].resize((new_width_piece, new_height_piece))
            self.black_piece_image[i] = self.img_copy_black_piece[i].resize((new_width_piece, new_height_piece))
            self.white_piece_image_foreground[i] = ImageTk.PhotoImage(self.white_piece_image[i])
            self.black_piece_image_foreground[i] = ImageTk.PhotoImage(self.black_piece_image[i])

        self.white_piece_selected = self.img_copy_white_piece_selected.resize((new_width_piece, new_height_piece))
        self.black_piece_selected = self.img_copy_black_piece_selected.resize((new_width_piece, new_height_piece))
        self.white_piece_selected_image = ImageTk.PhotoImage(self.white_piece_selected)
        self.black_piece_selected_image = ImageTk.PhotoImage(self.black_piece_selected)

        for i in range(self.n_slots):
            for j in range(7):
                if self.graphic_board_matrix[j, i] > 0:
                    if self.game_manager.current_selected_slot == i \
                            and np.all(self.graphic_board_matrix[j + 1:7, i] == 0):
                        assert (self.graphic_board_matrix[j, i] == 1)
                        self.board_canvas.create_image(
                            round(self.horizontal_position_grid[j, i] * new_width_background),
                            round(self.vertical_position_grid[j, i] * new_height_background),
                            image=self.white_piece_selected_image, anchor='nw')
                    else:
                        self.board_canvas.create_image(
                            round(self.horizontal_position_grid[j, i] * new_width_background),
                            round(self.vertical_position_grid[j, i] * new_height_background),
                            image=self.white_piece_image_foreground[round(self.graphic_board_matrix[j, i] - 1)],
                            anchor='nw')
                elif self.graphic_board_matrix[j, i] < 0:
                    if self.game_manager.current_selected_slot == i \
                            and np.all(self.graphic_board_matrix[j + 1:7, i] == 0):
                        assert (self.graphic_board_matrix[j, i] == -1)
                        self.board_canvas.create_image(
                            round(self.horizontal_position_grid[j, i] * new_width_background),
                            round(self.vertical_position_grid[j, i] * new_height_background),
                            image=self.black_piece_selected_image,
                            anchor='nw')
                    else:
                        self.board_canvas.create_image(
                            round(self.horizontal_position_grid[j, i] * new_width_background),
                            round(self.vertical_position_grid[j, i] * new_height_background),
                            image=self.black_piece_image_foreground[
                                -1 * round(self.graphic_board_matrix[j, i]) - 1], anchor='nw')

        self.slot_button_coordinates = self.get_slot_button_coordinates()
        self.dice_button_coordinates = self.get_dice_button_coordinates()
        self.white_exit_arrow_button_coordinates = self.get_white_exit_arrow_button_coordinates()
        self.black_exit_arrow_button_coordinates = self.get_black_exit_arrow_button_coordinates()

        new_width_arrow = round(self.normalized_arrow_width * new_width_background)
        new_height_arrow = round(self.normalized_arrow_height * new_height_background)

        if self.game_manager.current_game_state == GameState.PLAYER_1_TURN \
                and self.game_manager.is_white_endgame():
            self.white_exit_arrow = self.img_copy_white_exit_arrow.resize((new_width_arrow, new_height_arrow))
            self.white_exit_arrow_image = ImageTk.PhotoImage(self.white_exit_arrow)
            self.board_canvas.create_image(round((10 / 612) * new_width_background),
                                           round((183 / 612) * new_width_background),
                                           image=self.white_exit_arrow_image,
                                           anchor='nw')
        elif self.game_manager.current_game_state == GameState.PLAYER_2_TURN \
                and self.game_manager.is_black_endgame():

            self.black_exit_arrow = self.img_copy_black_exit_arrow.resize((new_width_arrow, new_height_arrow))
            self.black_exit_arrow_image = ImageTk.PhotoImage(self.black_exit_arrow)
            self.board_canvas.create_image(round((10 / 612) * new_width_background),
                                           round((368 / 612) * new_width_background),
                                           image=self.black_exit_arrow_image,
                                           anchor='nw')

    def resize_image(self, event):
        self.last_event_height = event.height
        self.last_event_width = event.width
        self.on_refresh_gui_event()

    def board_to_graphics(self):
        # this function converts board object into a graphic_board_matrix so the UI knows where each piece needs to
        # be displayed

        self.graphic_board_matrix = np.zeros((7, self.n_slots))

        # loop over all slots
        for i in range(self.game_manager.game_board.n_slots):
            # if no piece is pinned
            if self.game_manager.game_board.board_state[2, i] == 0:
                # if there is at least one white piece in slot i
                if self.game_manager.game_board.board_state[0, i] > 0:
                    for j in range(1, 7):
                        if self.game_manager.game_board.board_state[0, i] > j:
                            self.graphic_board_matrix[j, i] = 1

                    if self.game_manager.game_board.board_state[0, i] > 7:
                        self.graphic_board_matrix[0, i] = self.game_manager.game_board.board_state[0, i] - 6
                    else:
                        self.graphic_board_matrix[0, i] = 1

                # if there is at least one black piece in slot i
                elif self.game_manager.game_board.board_state[1, i] > 0:
                    for j in range(1, 7):
                        if self.game_manager.game_board.board_state[1, i] > j:
                            self.graphic_board_matrix[j, i] = -1

                    if self.game_manager.game_board.board_state[1, i] > 7:
                        self.graphic_board_matrix[0, i] = -1 * (self.game_manager.game_board.board_state[1, i] - 6)
                    else:
                        self.graphic_board_matrix[0, i] = -1

                # if there are no pieces in slot i
                else:
                    continue

            # if white piece is pinning
            elif self.game_manager.game_board.board_state[2, i] == 1:
                assert (self.game_manager.game_board.board_state[1, i] == 1)
                assert (self.game_manager.game_board.board_state[0, i] > 0)

                self.graphic_board_matrix[0, i] = -1

                for j in range(1, 6):
                    if self.game_manager.game_board.board_state[0, i] > j:
                        self.graphic_board_matrix[j + 1, i] = 1

                if self.game_manager.game_board.board_state[0, i] > 6:
                    self.graphic_board_matrix[1, i] = self.game_manager.game_board.board_state[0, i] - 5
                else:
                    self.graphic_board_matrix[1, i] = 1

            # if black piece is pinning
            elif self.game_manager.game_board.board_state[2, i] == -1:
                assert (self.game_manager.game_board.board_state[0, i] == 1)
                assert (self.game_manager.game_board.board_state[1, i] > 0)

                self.graphic_board_matrix[0, i] = 1

                for j in range(1, 6):
                    if self.game_manager.game_board.board_state[1, i] > j:
                        self.graphic_board_matrix[j + 1, i] = -1

                if self.game_manager.game_board.board_state[1, i] > 6:
                    self.graphic_board_matrix[1, i] = -1 * (self.game_manager.game_board.board_state[1, i] - 5)
                else:
                    self.graphic_board_matrix[1, i] = -1

            else:
                assert False

    def compute_rectangle_button_coordinates(self):

        # 1st row: lower left horizontal
        # 2nd row: lower left vertical
        # 3rd row: upper right horizontal
        # 4th row: upper right vertical

        corner_coordinates = np.zeros((4, self.n_slots))

        for i in range(self.n_slots):
            if i < self.n_slots / 2:
                corner_coordinates[0, i] = self.horizontal_position_grid[0, i]
                corner_coordinates[1, i] = self.vertical_position_grid[0, i] + self.normalized_piece_height
                corner_coordinates[2, i] = self.horizontal_position_grid[6, i] + self.normalized_piece_width
                corner_coordinates[3, i] = self.vertical_position_grid[6, i]

            else:
                corner_coordinates[0, i] = self.horizontal_position_grid[6, i]
                corner_coordinates[1, i] = self.vertical_position_grid[6, i] + self.normalized_piece_height
                corner_coordinates[2, i] = self.horizontal_position_grid[0, i] + self.normalized_piece_width
                corner_coordinates[3, i] = self.vertical_position_grid[0, i]

        return corner_coordinates

    def get_slot_button_coordinates(self):
        return self.current_background_dimension * self.slot_button_rectangle_coordinates

    def get_dice_button_coordinates(self):
        return self.current_background_dimension * self.dice_button_rectangle_coordinates

    def get_white_exit_arrow_button_coordinates(self):
        return self.current_background_dimension * self.white_exit_arrow_rectangle_coordinates

    def get_black_exit_arrow_button_coordinates(self):
        return self.current_background_dimension * self.black_exit_arrow_rectangle_coordinates

    def on_button_click(self, event):
        x_click_coord = event.x
        y_click_coord = event.y

        if x_click_coord <= 30 and y_click_coord <= 30:
            debug = 1

        if self.dice_button_coordinates[0] <= x_click_coord <= self.dice_button_coordinates[2] and \
                self.dice_button_coordinates[3] <= y_click_coord <= self.dice_button_coordinates[1]:
            dice_click = 1
            if self.game_manager.current_game_state == GameState.PLAYER_1_DICE_ROLL or \
                    self.game_manager.current_game_state == GameState.PLAYER_2_DICE_ROLL:
                self.game_manager.dice_rolled()
                self.dice_vals = self.game_manager.current_dice
                self.on_refresh_gui_event()
        elif self.white_exit_arrow_button_coordinates[0] <= x_click_coord \
                <= self.white_exit_arrow_button_coordinates[2] and \
                self.white_exit_arrow_button_coordinates[3] <= y_click_coord \
                <= self.white_exit_arrow_button_coordinates[1]:
            white_arrow_click = 1
            if self.game_manager.current_game_state == GameState.PLAYER_1_TURN \
                    and self.game_manager.is_white_endgame() \
                    and self.game_manager.current_selected_slot > -1 \
                    and self.game_manager.is_valid_move(-1):
                is_piece_successfully_moved = \
                    self.game_manager.game_board \
                        .move_piece_from_slot_to_slot(self.game_manager.current_selected_slot, -1, 0)

                if is_piece_successfully_moved:
                    logging.info('White piece moved to home')
                    if np.any(np.array(self.game_manager.remaining_dice_moves)
                              == self.n_slots - self.game_manager.current_selected_slot):
                        self.game_manager.remove_value_from_remaining_dice_moves(
                            self.n_slots - self.game_manager.current_selected_slot)
                    else:
                        self.game_manager.remove_value_from_remaining_dice_moves(
                            max(self.game_manager.remaining_dice_moves))
                    self.game_manager.current_selected_slot = -1
                    self.on_refresh_gui_event()
                else:
                    logging.error("Illegal move caught")
                    assert False

        elif self.black_exit_arrow_button_coordinates[0] <= x_click_coord \
                <= self.black_exit_arrow_button_coordinates[2] \
                and self.black_exit_arrow_button_coordinates[3] <= y_click_coord \
                <= self.black_exit_arrow_button_coordinates[1]:
            black_arrow_click = 1
            if self.game_manager.current_game_state == GameState.PLAYER_2_TURN \
                    and self.game_manager.is_black_endgame() \
                    and self.game_manager.current_selected_slot > -1 \
                    and self.game_manager.is_valid_move(-1):

                is_piece_successfully_moved = \
                    self.game_manager.game_board \
                        .move_piece_from_slot_to_slot(self.game_manager.current_selected_slot, -1, 1)

                if is_piece_successfully_moved:
                    logging.info('Black piece moved to home')
                    if np.any(np.array(
                            self.game_manager.remaining_dice_moves) == 1 + self.game_manager.current_selected_slot):
                        self.game_manager.remove_value_from_remaining_dice_moves(
                            1 + self.game_manager.current_selected_slot)
                    else:
                        self.game_manager.remove_value_from_remaining_dice_moves(
                            max(self.game_manager.remaining_dice_moves))
                    self.game_manager.current_selected_slot = -1
                    self.on_refresh_gui_event()
                else:
                    logging.error("Illegal move caught")
                    assert False

        else:
            for i in range(self.n_slots):
                if self.slot_button_coordinates[0, i] <= x_click_coord <= self.slot_button_coordinates[2, i] \
                        and self.slot_button_coordinates[3, i] <= y_click_coord <= self.slot_button_coordinates[1, i]:
                    clicked_slot = i
                    if self.game_manager.current_game_state == GameState.PLAYER_1_TURN:
                        if self.game_manager.current_selected_slot == -1:
                            if self.game_manager.game_board.board_state[0, clicked_slot] > 0 \
                                    and self.game_manager.game_board.board_state[2, clicked_slot] != -1:
                                self.game_manager.current_selected_slot = clicked_slot
                                logging.info('White piece selected at slot: %s', str(clicked_slot + 1))
                                self.on_refresh_gui_event()
                        elif self.game_manager.is_valid_move(clicked_slot):

                            is_piece_successfully_moved = \
                                self.game_manager.game_board \
                                    .move_piece_from_slot_to_slot(self.game_manager.current_selected_slot,
                                                                  clicked_slot,
                                                                  0)

                            if is_piece_successfully_moved:
                                logging.info('White piece moved to slot: %s', str(clicked_slot + 1))
                                self.game_manager.remove_value_from_remaining_dice_moves(
                                    clicked_slot - self.game_manager.current_selected_slot)
                                self.game_manager.current_selected_slot = -1
                                self.on_refresh_gui_event()
                            else:
                                logging.error("Illegal move caught")
                                assert False
                            self.game_manager.current_selected_slot = -1
                        else:
                            logging.info('White piece unselected at slot: %s',
                                         str(self.game_manager.current_selected_slot + 1))
                            self.game_manager.current_selected_slot = -1
                            self.on_refresh_gui_event()

                    elif self.game_manager.current_game_state == GameState.PLAYER_2_TURN:
                        if self.game_manager.current_selected_slot == -1:
                            if self.game_manager.game_board.board_state[1, clicked_slot] > 0 \
                                    and self.game_manager.game_board.board_state[2, clicked_slot] != 1:
                                self.game_manager.current_selected_slot = clicked_slot
                                logging.info('Black piece selected at slot: %s', str(clicked_slot + 1))
                                self.on_refresh_gui_event()
                        elif self.game_manager.is_valid_move(clicked_slot):

                            is_piece_successfully_moved = \
                                self.game_manager.game_board \
                                    .move_piece_from_slot_to_slot(self.game_manager.current_selected_slot,
                                                                  clicked_slot,
                                                                  1)
                            if is_piece_successfully_moved:
                                logging.info('Black piece moved to slot: %s', str(clicked_slot + 1))
                                self.game_manager.remove_value_from_remaining_dice_moves(
                                    self.game_manager.current_selected_slot - clicked_slot)
                                self.game_manager.current_selected_slot = -1
                                self.on_refresh_gui_event()
                            else:
                                logging.error("Illegal move caught")
                                assert False

                            self.game_manager.current_selected_slot = -1
                        else:
                            logging.info('Black piece unselected at slot: %s',
                                         str(self.game_manager.current_selected_slot + 1))
                            self.game_manager.current_selected_slot = -1
                            self.on_refresh_gui_event()

                    break
