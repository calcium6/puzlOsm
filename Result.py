class Result:
    def __init__(self, nodesExplored: int, depth, solution):
        self.nodesExplored = nodesExplored
        self.depth = depth
        self.solution = solution
    
    def print(self):
        print("Nodes Explored: ", self.nodesExplored)
        print(f'Solution Found at depth {self.depth}.')
        print('Steps: ')
        for step in self.solution:
            print(f'\t{step}')
