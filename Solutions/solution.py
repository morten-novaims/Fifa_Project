class Solution:

    _id = 0

    def __init__(self, representation=None):
        self._solution_id = Solution._id
        Solution._id += 1
        self.representation = representation
        self.fitness = None
        self.value = None
        self.age = None
        self.overall = None
        self.potential = None
        self.valid = None



    def print(self):
        # A Print statement as a verbose should be coded here
        pass

