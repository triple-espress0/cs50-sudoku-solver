"""CLI sudoku solver of randomly generated board"""
import copy
from helpers import (
    find_empty_cell,
    get_candidates,
    generate_sudoku_list,
    populate_candidate_values,
)


input_board = generate_sudoku_list()


def solve_board(board):
    """Main sudoku solver function that keeps track of all possible solutions"""
    solutions = []
    board_copy = copy.deepcopy(board)

    def recurse(current_board):
        """Recursive function that solves a given board"""
        solution = copy.deepcopy(current_board)
        candidates_values = populate_candidate_values(solution)
        if find_empty_cell(candidates_values) == (-1, -1):
            solutions.append(solution)
            return solutions
        empty_row, empty_col = find_empty_cell(candidates_values)
        index = get_candidates(empty_row, empty_col, candidates_values)
        if get_candidates(empty_row, empty_col, candidates_values) == -1:
            solution[empty_row][empty_col] = 0
            return
        for item in list(candidates_values[index].values())[0]:
            solution[empty_row][empty_col] = item
            recurse(solution)

    recurse(board_copy)

    if len(solutions) == 0:
        return "unsolvable"

    if len(solutions) > 1:
        print(solutions)
        return "not unique"

    return solutions


print(solve_board(input_board))
