import utils as utls

class Search_space:
    def __init__(self, position="simple"):
        self.position = position
        self.data = utls.data_import(normalized_positions=True)
