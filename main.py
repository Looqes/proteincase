import sys
# import random
from classes.protein import *
from classes.board import *
from algorithms.fold_random import *
from algorithms.bfs import *




# Reading input
if len(sys.argv) == 3:
    protein = read_protein("proteins/" + sys.argv[2])
    if protein == 1:
        exit(1)
else:
    print("Usage: fold.py [algorithm to use] [name of file containing protein]")
    print("Algorithms:")
    print("    - random")
    print("    - bfs")
    exit(1)

print(protein.peptides)
print()

if sys.argv[1] == "random":
    # solved_board, score = random_folder(protein, 10000)
    solved_board, score = random_folder(protein, 10000)

elif sys.argv[1] == "bfs":
    solved_board, score = bfs(protein)
else:
    print("unrecognized algorithm")

if solved_board:
    solved_board.display()
    print(score)
else:
    print("No solved board was made...")

