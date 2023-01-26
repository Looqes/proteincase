# fold BFS

from classes.board import *
import copy


def bfs(protein):
    start_board = Board(protein)

    final_states = bfs_states(start_board)

    return final_states[0]

    

# Function that creates all final folding states given a starting board with 
# a protein
def bfs_states(start_board):
    boards = [start_board]

    for peptide in start_board.protein:
        new_boards = []

        # Extend all boards in collection with each of their possible moves.
        # Attempt to place each peptide in each possible direction.
        for board in boards:
            directions = board.get_possible_directions()
            
            for dir in directions:
                new_board = copy.deepcopy(board)
                add_move(new_board, dir, peptide)

                new_boards.append(new_board)

        # Pruning, taking only most promising 100 boards
        boards = sort_boards(new_boards)[0:1000]
        # boards = sort_boards(new_boards)

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


def sort_boards(boards_list):
    return sorted(boards_list, key=lambda x: x.score)
