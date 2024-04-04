class Result:
    def __init__(self, nodesExplored: int, depth: int, solution: list[str], boards: list[list[list[int]]]):
        self.nodesExplored = nodesExplored
        self.depth = depth
        self.solution = solution
        self.boards = boards
    
    def toString(self) -> str:
        string = "Nodes explored: " + str(self.nodesExplored) + "\n"
        string += "Solution found at depth " + str(self.depth) + "\n"
        string += "Steps:\n"
        for step in self.solution:
            string += "\t" + step + "\n"
        return string
