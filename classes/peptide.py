# Peptide class


class Peptide():
    # Class to represent a single peptide (sort of as a node) in a peptide chain
    # Peptides point to their parent (previous peptide in chain) and child
    # (next peptide).

    def __init__(self, type, loc, parent):
        self.type = type
        self.parent = parent
        self.loc = loc
        self.child = None
        
    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        self.child = child

    def __repr__(self) -> str:
        return str(self.type)