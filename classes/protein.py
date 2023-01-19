# protein class


class Protein():
    def __init__(self, peptides):
        self.peptides = list(peptides)
    

def read_protein(filename):
    try:
        contents = open(filename).read()
    except FileNotFoundError:
        print("File \"" + filename + "\" does not exist")
        return 1

    return Protein(contents)
