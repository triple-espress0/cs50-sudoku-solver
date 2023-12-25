"""GUI sudoku solver of randomly generated board"""
from helpers import (
    find_empty_location,
    is_valid,
    generate_sudoku_list,
    )
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import DictProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from functools import partial
import time


class GridCell(MDLabel, EventDispatcher):
    pass


class BoardArea(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super(BoardArea, self).__init__(*args, **kwargs)

        self.label_indexes_dict = dict()
        self.label_indexes = DictProperty()
        self.sudoku_board = generate_sudoku_list()

        for i in range(9):
            for j in range(9):
                label = GridCell(id=f"cell{i}{j}", text="0")
                label.apply_class_lang_rules()
                self.add_widget(label)

        self.label_indexes_dict = self._populate_indexes_dict()
        self.label_indexes.set(self, self.label_indexes_dict)

    def _populate_indexes_dict(self):
        index = 80
        for i in range(9):
            for j in range(9):
                self.label_indexes_dict[(i, j)] = index
                index -= 1

        return self.label_indexes_dict

    def populate_board(self):
        '''Populates a sudoku board'''
        for i in range(9):
            for j in range(9):
                index = self.label_indexes_dict[(i, j)]
                if self.sudoku_board[i][j] == 0:
                    self.children[index].text = ""
                    self.children[index].apply_class_lang_rules()
                    continue

                self.children[index].text = str(self.sudoku_board[i][j])
                self.children[index].apply_class_lang_rules()
        return

    def generate_new_board(self):
        '''Generates new sudoku board and displays it on the GUI'''
        self.sudoku_board = generate_sudoku_list()

        for i in range(9):
            for j in range(9):
                index = self.label_indexes_dict[(i, j)]
                self.children[index].canvas.clear()
                if self.sudoku_board[i][j] == 0:
                    self.children[index].text = ""
                else:
                    self.children[index].text = str(self.sudoku_board[i][j])

                self.children[index].apply_class_lang_rules()
                self.apply_class_lang_rules()

        return

    def solve_board(self, sudoku_board):
        '''Solves a sudoku board using backtracking'''
        
        empty_row, empty_col = find_empty_location(sudoku_board)

        if empty_row is None:
            return True
        
        cell_index = self.label_indexes_dict[(empty_row, empty_col)]
        
        for num in range(1, 10):
            if is_valid(sudoku_board, empty_row, empty_col, num):
                sudoku_board[empty_row][empty_col] = num
                Clock.schedule_once(
                    partial(self.format_current_label, cell_index, num), -1
                )
                time.sleep(0.0005)

                if self.solve_board(sudoku_board):
                    return True

                sudoku_board[empty_row][empty_col] = 0

        return False


    def format_current_label(self, label_id, label_text, dt):
        '''Formats the currently evaluated sudoku cell'''
        self.children[label_id].text = str(label_text)
            

class SudokuGame(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SudokuGame, self).__init__(*args, **kwargs)
        game_widget = self.children[1]
        game_widget.populate_board()


class ButtonsArea(MDFloatLayout):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        game = SudokuGame()
        return game


if __name__ == "__main__":
    MainApp().run()
