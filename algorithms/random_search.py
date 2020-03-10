from algorithms.search_algorithm import SearchAlgorithm


class RandomSearch(SearchAlgorithm):
    def __init__(self, problem_instance, random_state):
        SearchAlgorithm.__init__(self, problem_instance)
        self._random_state = random_state


    def initialize(self):
        self.best_solution = self._generate_random_valid_solution()


    def search(self, n_iterations, report=False):
        i = self.best_solution
        for iteration in range(n_iterations):
            j = self._generate_random_valid_solution()
            i = self._get_best(i, j)

            if report and iteration%50 == 0:
                print(">>>> Current Best Solution RS: mean overall: %.2f   - total value: %.2f" % (i.fitness, i.value))
                print("_"*45)
#                self._verbose_reporter_inner(i, iteration)

        self.best_solution = i


    def _generate_random_solution(self):
        random_solution = self.problem_instance.generate_random_squad(self._random_state)
        self.problem_instance._evaluate(random_solution)
        return random_solution


    def _generate_random_valid_solution(self):
        solution = self._generate_random_solution()
        self.problem_instance._evaluate(solution)

        while not solution.valid:
            solution = self._generate_random_solution()
            self.problem_instance._evaluate(solution)

        return solution
