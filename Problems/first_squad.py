from Problems.problem import Problem
from Solutions.solution import Solution
import numpy as np

class First_Squad(Problem):
    def __init__(self, search_space, fitness_function="Overall_Sum", system="4-4-2", budget=None, minimization=False,
                 mean_age=25):
        Problem.__init__(self, search_space, fitness_function, minimization)
        self.system = self._translate_system(system)
        self.budget = budget
        self.mean_age = mean_age
        self.threshold = 0.1


    def _evaluate(self, solution):

        solution.overall = self.search_space.data.loc[
            self.search_space.data["ID"].isin(solution.representation), "Overall"].mean()

        solution.value = self.search_space.data.loc[
            self.search_space.data["ID"].isin(solution.representation), "Value"].sum()

        solution.age = self.search_space.data.loc[
            self.search_space.data["ID"].isin(solution.representation), "Age"].mean()

        solution.potential = self.search_space.data.loc[
            self.search_space.data["ID"].isin(solution.representation), "Potential_Gain"].mean()


            # fitness functions
        if self.fitness_function == "Overall_Sum":
            solution.fitness = solution.overall

        elif self.fitness_function == "Overall_Sum_min_Age":
            solution.fitness = solution.overall - (abs(self.mean_age - solution.age)/2)

        elif self.fitness_function == "Overall_Sum_add_Potential":
            solution.fitness = solution.overall + solution.potential/3



        self._validate(solution)
        return solution


    def _validate(self, solution):
        if (solution.representation.shape[0] == 11) and\
                (len(solution.representation) == len(np.unique(solution.representation))):
           if self.budget == None:
                    solution.valid = True
           elif solution.value <= self.budget:
                    solution.valid = True
           return solution
        else:
            return False

    def generate_random_squad(self, random_state):
        data = self.search_space.data

        # partition the data into areas
        # GK tolist() statement to init a new list
        data_gk = data.loc[data["Normalized_Position"] == "GK", "ID"].tolist()
        squad = random_state.choice(data_gk, size=1, replace=False)

        # all positions but GK
        for position in self.system[1:]:
            data["diff"] = (data["Overall"] - data[position]) /data["Overall"]
            data_part = data.loc[data["diff"] < self.threshold, "ID"]
            squad = np.append(squad, random_state.choice(data_part, size=1, replace=False))

        return Solution(squad)

    def _position_flip(self, squad, position, random_state):
        data = self.search_space.data

        if self.system[position] == "GK":
            data = data.loc[data["Normalized_Position"] == "GK", "ID"]

        else:
            data["diff"] = (data["Overall"] - data[self.system[position]]) / data["Overall"]
            data = data.loc[data["diff"] < self.threshold, "ID"]

        squad[position] = data.sample(n=1, replace=False, random_state=random_state)

        return squad

    def _translate_system(self, system):
        if system == "4-4-2":
            position_list = [           "GK",
                              "RB", "RCB", "LCB", "LB",
                              "RM", "RCM", "LCM", "LM",
                                     "LS", "RS"]

        return position_list