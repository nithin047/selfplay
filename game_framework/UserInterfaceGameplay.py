from game_framework.UserInterface import UserInterface
from game_framework.GameManager import GameState


class UserInterfaceGameplay(UserInterface):
    def __init__(self, game_manager):
        UserInterface.__init__(self, game_manager)
        self.board_canvas.bind("<Button-1>", self.on_button_click)
        self.window.mainloop()

    def on_button_click(self, event):
        x_click_coord = event.x
        y_click_coord = event.y
        self.on_click_coordinates(x_click_coord, y_click_coord)

    def on_click_coordinates(self, x_click_coord, y_click_coord):

        # just here for live debugging
        if x_click_coord <= 30 and y_click_coord <= 30:
            debug = 1

        if self.dice_button_coordinates[0] <= x_click_coord <= self.dice_button_coordinates[2] and \
                self.dice_button_coordinates[3] <= y_click_coord <= self.dice_button_coordinates[1]:
            self.on_dice_click()

        elif self.white_exit_arrow_button_coordinates[0] <= x_click_coord \
                <= self.white_exit_arrow_button_coordinates[2] and \
                self.white_exit_arrow_button_coordinates[3] <= y_click_coord \
                <= self.white_exit_arrow_button_coordinates[1]:
            self.on_white_arrow_click()

        elif self.black_exit_arrow_button_coordinates[0] <= x_click_coord \
                <= self.black_exit_arrow_button_coordinates[2] \
                and self.black_exit_arrow_button_coordinates[3] <= y_click_coord \
                <= self.black_exit_arrow_button_coordinates[1]:
            self.on_black_arrow_click()

        else:
            for i in range(self.n_slots):
                if self.slot_button_coordinates[0, i] <= x_click_coord <= self.slot_button_coordinates[2, i] \
                        and self.slot_button_coordinates[3, i] <= y_click_coord <= self.slot_button_coordinates[1, i]:
                    clicked_slot = i
                    self.on_slot_click(clicked_slot)
                    break

    def on_dice_click(self):
        if self.game_manager.current_game_state == GameState.PLAYER_1_DICE_ROLL or \
                self.game_manager.current_game_state == GameState.PLAYER_2_DICE_ROLL:
            self.game_manager.dice_rolled()
            self.dice_vals = self.game_manager.current_dice
            self.on_refresh_gui_event()
