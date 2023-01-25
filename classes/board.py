# File containing a class to represent the board on which to place and fold the
# protein

import random
from classes.peptide import *


# Create square board as a grid. Board is initialized with a protein that needs
# to be placed (and folded) onto it. Board size is dependent on length of
# protein. 
# First protein is placed on initialization, in the middle of the board.
class Board:
    def __init__(self, protein):
        protein_length = len(protein.peptides)
        self.size = protein_length
        self.score = 0

        self.grid = [[0 for _ in range(protein_length * 2 + 1)]
                        for _ in range(protein_length * 2 + 1)]
        self.placed_peptides = []

        # Set first protein in the middle of the board (no parent -> None)
        board_middle = (protein_length, protein_length)
        self.put_peptide(board_middle, protein.peptides[0], None)
        self.last_set_coords = board_middle

        # Save proteins that still need to be placed.
        # All but the first one since it's always placed in the board middle
        self.protein = protein.peptides[1:]

        self.chain_coordinates = set()
        # self.score? voor opslaan van boards zodra er meerdere verschillende
        # worden gegenerate?


    # Get display bounds for printing the final folded protein
    # Actual grid is large, large enough to support a straight, non-folded
    # protein, but contains a lot of empty space that does not need to be
    # printed to get a clear visualization of the fold
    def get_display_bounds(self):
        coords_of_placed_peptides = [pep.loc for pep in self.placed_peptides]
        all_x_coords = [loc[0] for loc in coords_of_placed_peptides]
        all_y_coords = [loc[1] for loc in coords_of_placed_peptides]

        xrange = (min(all_x_coords) - 1, max(all_x_coords) + 1)
        yrange = (min(all_y_coords) - 1, max(all_y_coords) + 1)

        return xrange, yrange


    # Function to display the peptides and their bonds
    def display(self):
        xrange, yrange = self.get_display_bounds()

        for y in range(yrange[0], yrange[1] + 1):
            for x in range(xrange[0], xrange[1] + 1):
                # printing the peptides
                if self.grid[y][x] == 0:
                    print(".", end = "")
                else:
                    print(self.grid[y][x], end = "")
                # printing horizontal bonds
                if (
                    ((x, y), (x + 1, y)) in self.chain_coordinates or
                    ((x + 1, y), (x, y)) in self.chain_coordinates
                   ):
                    print(" — ", end = "")
                else:
                    print("   ", end = "")
            print()

            # printing the vertical bonds
            for x in range(xrange[0], xrange[1] + 1):
                if (
                    ((x, y), (x, y + 1)) in self.chain_coordinates or
                    ((x, y + 1), (x, y)) in self.chain_coordinates
                   ):
                    print("|   ", end = "")
                else:
                    print("    ", end = "")
            print()


    # Add peptide to the chain of peptides on grid
    # put as [y][x] due to indexing on grid
    def put_peptide(self, coords, type, parent):
        x, y = coords
        new_peptide = Peptide(type, (x, y), parent)
        self.grid[y][x] = new_peptide

        self.placed_peptides.append(new_peptide)

        if parent:
            parent.set_child(new_peptide)

        self.update_score(new_peptide)


    # Update the score of the board by checking if any bonds are made by
    # having added a new_peptide
    def update_score(self, new_peptide):
        type = self.placed_peptides[-1].type
        if type != "P":
            neighbours = self.get_non_chained_neighbours(new_peptide)

            if neighbours:
                for neighbor in neighbours:
                    neighbor_type = neighbor.type

                    if (type == "H" and neighbor_type == "H" or
                        type == "H" and neighbor_type == "C" or
                        type == "C" and neighbor_type == "H"):
                        self.score -= 1
                    elif type == "C" and neighbor_type == "C":
                        self.score -= 5


    # Add coordinate pairs which represent the chain-bonds between peptides to
    # the board. This is used for visualization of the chain.
    def add_connection(self, orig, dest):
        self.chain_coordinates.add((orig, dest))


    # Get non-occupied neighbouring (NWSE) tiles of board grid
    # Returns wind direction of empty tiles
    def get_possible_directions(self):
        neighbors = self.get_neighboring_spaces(self.last_set_coords)
        
        return [direction for direction in neighbors 
                if neighbors[direction] == 0]


    # Return contents of grid space at coords loc
    # Acces as (y, x) due to grid being an array of arrays (row index first)
    def get_grid_space(self, loc):
        x, y = loc
        return self.grid[y][x]


    # Return neighboring peptides of placed peptides that are not directly
    # chained to it.
    def get_non_chained_neighbours(self, peptide):
        x, y = peptide.loc
        neighbors = self.get_neighboring_spaces((x, y))
        # print(neighbors)

        return [neighbors[spot] for spot in neighbors
                if neighbors[spot] != 0 and
                   neighbors[spot] != peptide.parent and
                   neighbors[spot] != peptide.child]


    # Return contents of neighboring grid spaces of some space in grid
    def get_neighboring_spaces(self, peptide_loc):
        peptide_x, peptide_y = peptide_loc
        tiles = []

        # North, west, south, east
        for x_mod, y_mod in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            tiles.append(self.get_grid_space((peptide_x + x_mod, peptide_y + y_mod)))
        
        return {"N": tiles[0], "E": tiles[1], "S": tiles[2], "W": tiles[3]}

    

    # Calculate the score of a given board
    # For every neighbouring pair of H's (not counting those neighbouring in the
    # original chain) the score of the board decreases by 1
    # Function counts bonds twice (due to the second H of the bond being
    # checked when it is reached further in the chain) so the score is halved
    # before it is returned.
    ############################################################################
    # No longer needed since boards now keep track of their scores as peptides
    # are being placed on them.
    def calc_board_score(self):
        score = 0

        for peptide in self.placed_peptides:
            type = peptide.type
            if type == "H" or type == "C":
                neighbors = self.get_non_chained_neighbours(peptide)

                for neighbor in neighbors:
                    neighbor_type = neighbor.type

                    if (type == "H" and neighbor_type == "H" or
                        type == "H" and neighbor_type == "C" or
                        type == "C" and neighbor_type == "H"):
                        score -= 1
                    elif type == "C" and neighbor_type == "C":
                        score -= 5
                
        return int(score/2)

