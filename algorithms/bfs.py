# fold BFS

from classes.board import *
import copy


def bfs(protein):
    start_board = Board(protein)

    final_states = bfs_states(start_board)

    return get_best_board(final_states)

    

# Function that creates all final folding states given a starting board with 
# a protein
def bfs_states(start_board):
    boards = [start_board]

    for peptide in start_board.protein:
        new_boards = []

        for board in boards:
        # Attempt to place each peptide in each possible direction
            directions = board.get_possible_directions()
            
            for dir in directions:
                new_board = copy.deepcopy(board)
                add_move(new_board, dir, peptide)

                new_boards.append(new_board)

        boards = new_boards

        # Pruning, taking only most promising 100 boards
        boards_with_scores = assign_board_scores(boards)
        sorted_boards = sort_boards(boards_with_scores)
        # Take only boards, leave scores
        boards = [pair[0] for pair in sorted_boards[0:100]]
    
    return boards



def add_move(board, direction, peptide):
    newx, newy = board.last_set_coords

    if direction == "N":
        newy -= 1
    elif direction == "E":
        newx += 1
    elif direction == "S":
        newy += 1
    elif direction == "W":
        newx -= 1

    board.put_peptide((newx, newy), peptide, board.placed_peptides[-1])
    board.add_connection(board.last_set_coords, (newx, newy))

    board.last_set_coords = (newx, newy)


def get_best_board(boards):
    boards_with_scores = assign_board_scores(boards)

    sorted_boards = sort_boards(boards_with_scores)

    return sorted_boards[0]

def assign_board_scores(boards_list):
    boards_with_scores = []

    for board in boards_list:
        score = board.calc_board_score_2()
        boards_with_scores.append((board, score))
    
    return boards_with_scores

def sort_boards(boards_scores_list):
    return sorted(boards_scores_list, key=lambda x: x[1])
