#imports
from Search_Space.search_space import Search_space
from Problems.first_squad import First_Squad
from algorithms.random_search import RandomSearch
from algorithms.hill_climbing import HillClimbing
from algorithms.genetic_algorithm import GeneticAlgorithm
from Visualisation.visualisation import show_squad
import numpy as np
import utils as utls


seed = np.random.randint(100)

# 0. Set up random state
random_state = utls.get_random_state(seed)

# 1. Set up Search Space & Problem Instance
search_space = Search_space()
problem_instance = First_Squad(search_space=search_space, budget=500, mean_age=25,
                               fitness_function="Overall_Sum_add_Potential")

# 2. Random Search
rs = RandomSearch(problem_instance, random_state)
rs.initialize()
rs.search(n_iterations=100, report=True)

# 3. Hill Climbing interpretation
hc = HillClimbing(problem_instance, random_state)
hc.initialize()
hc.search(n_iterations=200, report=True)

# 4. Genetic Algorithm Standard
ga = GeneticAlgorithm(problem_instance, random_state,
                      population_size=50,
                      selection_method="tournament",
                      crossover_method="one-point", crossover_rate=0.5,
                      mutation_method="position-flip", mutation_rate=0.5,
                      tournament_size=4)
ga.initialize()
ga.search(n_iterations=200, report=True)



print("_"*45)
print("Results of Random Search")
print("Cost of current Best Squad: %.2f Mil. Eur"% (rs.best_solution.value))
print("Mean Score of Current best Squad: %.1f" %(rs.best_solution.overall))
print("Average Age of Current best Squad: %.1f" %(rs.best_solution.age))
print("Average Potential of Current best Squad: %.1f" %(rs.best_solution.potential))
print()
show_squad(rs.best_solution.representation)


print("_" *45)
print("Results of Hill Climbing")
print("Cost of current Best Squad: %.2f Mil. Eur"% (hc.best_solution.value))
print("Mean Score of Current best Squad: %.1f" %(hc.best_solution.overall))
print("Average Age of Current best Squad: %.1f" %(hc.best_solution.age))
print("Average Potential of Current best Squad: %.1f" %(hc.best_solution.potential))
print()
show_squad(hc.best_solution.representation)


print("_" *45)
print("Results of Genetic Algorithm")
print("Cost of current Best Squad: %.2f Mil. Eur"% (ga.elite.value))
print("Mean Score of Current best Squad: %.1f" %(ga.elite.overall))
print("Average Age of Current best Squad: %.1f" %(ga.elite.age))
print("Average Potential of Current best Squad: %.1f" %(ga.elite.potential))
print()
show_squad(ga.elite.representation)



