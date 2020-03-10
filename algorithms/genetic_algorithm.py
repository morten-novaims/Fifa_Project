from algorithms.search_algorithm import SearchAlgorithm
from Solutions.solution import Solution
import numpy as np


class GeneticAlgorithm(SearchAlgorithm):
    def __init__(self, problem_instance, random_state,
                 population_size, selection_method,
                 crossover_method, crossover_rate,
                 mutation_method, mutation_rate,
                 tournament_size=None):
        SearchAlgorithm.__init__(self, problem_instance)
        self._random_state = random_state
        self._population_size = population_size
        self._selection_method = selection_method
        self._crossover_method = crossover_method
        self.crossover_rate = crossover_rate
        self._mutation_method = mutation_method
        self.mutation_rate = mutation_rate
        self._tournament_size = tournament_size
        self.population = None
        self.elite = None


    def initialize(self):
        self.population = self._initialize_population()
        self.elite  = self._get_elite()

    def search(self, n_iterations, elitism=False, report=False):

        for iteration in range(n_iterations):
            new_population = []

            if elitism:
                new_population.append(self.elite)

            while len(new_population) < self._population_size:

                # selection
                parent_1 = offspring_1 = self._selection()
                offspring_2 = None

                # crossover
                if self._random_state.uniform(0,1) < self.crossover_rate:
                    parent_2 = self._selection()
                    offspring_1, offspring_2 = self._crossover(parent_1, parent_2)

                # mutation
                if self._random_state.uniform(0,1) < self.mutation_rate:
                    offspring_1 = self._mutation(offspring_1)

                if (offspring_2 is not None) and (self._random_state.uniform(0,1) < self.mutation_rate):
                    offspring_2 = self._mutation(offspring_2)

                #checking for validity and appending to new population
                if offspring_1.valid:
                    new_population.append(offspring_1)

                if offspring_2 is not None:
                    if offspring_2.valid:
                        new_population.append(offspring_2)

            self.population = new_population[:self._population_size-1]   # safety net
            self.elite = self._get_elite()

            if report and iteration%50 == 0:
                print(">>>> Current Best Solution GA: mean overall: %.2f   - total value: %.2f" % (self.elite.fitness,
                                                                                                   self.elite.value))
                print("_"*45)

        return self.elite


    def _initialize_population(self):
        population = [self._generate_random_solution()]

        while len(population) < self._population_size:
            population.append(self._generate_random_solution())

        return population


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


    def _get_elite(self):
        fitness_values = [solution.fitness for solution in self.population]
        elite_idx = np.argmax(fitness_values)
        elite = self.population[elite_idx]
        return elite


    def _selection(self):
        if self._selection_method == "tournament":
            parent = self.tournament()
        return parent


    def tournament(self):
        tournament_pool = self._random_state.choice(self.population, size=self._tournament_size, replace=True)
        tournament_fitness = [tournament_pool[idx].fitness for idx in range(self._tournament_size)]
        parent_idx = np.argmax(tournament_fitness)
        return tournament_pool[parent_idx]


    def _crossover(self, parent_1, parent_2):
        if self._crossover_method == "one-point":
            offspring_1, offspring_2 = self.one_point_crossover(parent_1, parent_2)

        offspring_1 = self.problem_instance._evaluate(Solution(offspring_1))
        offspring_2 = self.problem_instance._evaluate(Solution(offspring_2))

        return offspring_1, offspring_2

    def one_point_crossover(self, parent_1, parent_2):
        crossover_point = self._random_state.randint(len(parent_1.representation))

        offspring_1 = np.append(parent_1.representation[:crossover_point],
                                     parent_2.representation[crossover_point:])
        offspring_2 = np.append(parent_2.representation[:crossover_point],
                                     parent_1.representation[crossover_point:])

        return offspring_1, offspring_2

    def _mutation(self, offspring):
        if self._mutation_method == "position-flip":
            offspring = self.position_flip(offspring)

        offspring = self.problem_instance._evaluate(Solution(offspring))
        return offspring

    def position_flip(self, offspring):
        position = self._random_state.randint(len(offspring.representation))
        offspring = self.problem_instance._position_flip(offspring.representation, position, self._random_state)
        return offspring
