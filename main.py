import sys
# import random
from classes.protein import *
from classes.board import *
from algorithms.fold_random import *




# Reading input
if len(sys.argv) == 2:
    protein = read_protein("proteins/" + sys.argv[1])
    if protein == 1:
        exit(1)
else:
    print("Usage: fold.py [name of file containing protein]")
    exit(1)

print(protein.peptides)
print()


solved_board, score = random_folder(protein, 10000)


solved_board.display()
print(score)

