"""Helper functions for the CLI sudoku solver"""
from dokusan import generators


def find_empty_cell(candidates_values_list):
    """Helper function that returns an empty cell with the smallest amount of possible values"""
    if len(candidates_values_list) == 0:
        return (-1, -1)
    candidates_values_list_sorted = sorted(
        candidates_values_list, key=lambda x: sum(len(v) for v in x.values())
    )

    return list(candidates_values_list_sorted[0].keys())[0]


def generate_sudoku_list():
    """Generates random sudoku puzzle and transforms it into list of lists representing
    each row of the sudoku puzzle"""
    sudoku = str(generators.random_sudoku(avg_rank=150))
    return [[int(i) for i in list(sudoku[j : j + 9])] for j in range(0, 81, 9)]


def get_box_candidates(board, row, column):
    """Helper function that returns list of unassigned values in a given 3x3 box of the board"""
    row_bound = row // 3
    column_bound = column // 3
    box_items = [
        board[i][j]
        for i in range(row_bound * 3, (row_bound * 3) + 3)
        for j in range(column_bound * 3, (column_bound * 3) + 3)
    ]
    result = [i for i in range(1, 10) if i not in box_items]
    return result


def get_column_candidates(board, column):
    """Helper function that returns list of unassigned values in a given column of the board"""
    column_items = [board[i][column] for i in range(9)]
    result = [i for i in range(1, 10) if i not in column_items]
    return result


def get_row_candidates(board, row):
    """Helper function that returns list of unassigned values in a given row of the board"""
    result = [i for i in range(1, 10) if i not in board[row]]
    return result


def get_candidates(row, column, candidates_values):
    """Helper function that returns the index of the {x, y}: [] dictionary item from the list
    of all candidate values"""
    try:
        index = [
            key
            for (key, value) in enumerate(candidates_values)
            if value.get((row, column))
        ][0]
    except IndexError:
        index = -1

    return index


def populate_candidate_values(board):
    """Helper function that generates a list of dictionaries for all possible candidate values
    of all unassigned sudoku elements"""
    candidates_values = [{(i, j): [0]} for i in range(9) for j in range(9)]
    for i in range(9):
        for j in range(9):
            index = [
                key
                for (key, value) in enumerate(candidates_values)
                if value.get((i, j))
            ][0]
            if board[i][j] != 0:
                candidates_values.pop(index)
                continue
            row_candidates = get_row_candidates(board, i)
            column_candidates = get_column_candidates(board, j)
            box_candidates = get_box_candidates(board, i, j)
            cell_candidates = list(
                set(row_candidates) & set(column_candidates) & set(box_candidates)
            )
            candidates_values[index][(i, j)] = cell_candidates
    return candidates_values
