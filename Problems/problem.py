class Problem:
    def __init__(self, search_space, fitness_function, minimization):
        self.search_space = search_space
        self.fitness_function = fitness_function
        self.minimization = minimization