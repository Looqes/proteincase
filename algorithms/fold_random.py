import random
from classes.board import *


# Function that attempts a single random fold
def fold_random(protein):
    board = Board(protein)

    for peptide in board.protein:
        # If peptide placement results in a chain that folds itself into
        # a dead end, the fold is invalid
        if place_random(board, peptide) == 1:
            # print("dead end")
            return None
    
    return board


# Extend the peptide chain being placed on the board by making it select
# a possible direction to place the next peptide randomly
def place_random(board, peptide):
    x, y = board.last_set_coords
        
    possible_directions = board.get_possible_directions()
    if not possible_directions:
        return 1
    
    choice = random.choice(possible_directions)

    newx, newy = x, y

    if choice == "N":
        newy -= 1
    elif choice == "E":
        newx += 1
    elif choice == "S":
        newy += 1
    elif choice == "W":
        newx -= 1
    
    board.put_peptide((newx, newy), peptide, board.placed_peptides[-1])
    board.add_connection(board.last_set_coords, (newx, newy))

    board.last_set_coords = (newx, newy)


# Fold i number of times and return the best result
def random_folder(protein, iterations):
    best_score = 1
    best_board = None

    for i in range(iterations):
        result = fold_random(protein)
        
        if result:
            score = result.score
            if score < best_score:
                best_score = score
                best_board = result

    return best_board, best_board.score





