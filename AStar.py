import copy
from queue import PriorityQueue
from Board import Board
from Result import Result

class AStar:
    def __init__(self, board: type[Board], goal: type[Board], priorityFunc: bool): #priorityFunc(True = Manhattan, False = Hamming)
        self.initialBoard = board
        self.goalBoard = goal
        self.boardSize = self.initialBoard.size
        self.priorityFunc = priorityFunc

    def priority(self, board: type[Board], depth: int) -> int:
        if self.priorityFunc:
            return depth + board.manhattan(self.goalBoard.tiles)
        return depth + board.hamming(self.goalBoard.tiles)
    
    def moveDirection(self, board: type[Board], movedTile: tuple[int]) -> str:
        emptyTile = board.getEmptySpace()
        rowDiff = movedTile[0] - emptyTile[0]
        if rowDiff == 1:
            return " down"
        if rowDiff == -1:
            return " up"
        colDiff = movedTile[1] - emptyTile[1]
        if colDiff == 1:
            return " right"
        if colDiff == -1:
            return " left"
    
    def boardMove(self, steps, board: type[Board], movedTile: tuple[int]) -> list[str]:
        newSteps = copy.deepcopy(steps)
        moveString = "Move " + str(board.tiles[movedTile[0]][movedTile[1]]) + self.moveDirection(board, movedTile)
        newSteps.append(moveString)
        return newSteps

    def run(self) -> type[Result]:
        visited = []
        nodesExplored = 1
        priorityQueue = PriorityQueue()
        priorityQueue.put((self.priority(self.initialBoard, 0), 0, self.initialBoard.tiles, []))

        while not priorityQueue.empty():
            _, depth, board, steps = priorityQueue.get() #board: type[Board]
            newBoard = Board(board, self.boardSize)

            if newBoard.isGoal(self.goalBoard.tiles):
                return Result(nodesExplored, depth, steps)
            
            prevEmpty = newBoard.getEmptySpace() #prevEmpty: tuple[int]
            visited.append(board)
            for n in newBoard.getNeighbors():
                if n not in visited:
                    nodesExplored += 1
                    nDepth = depth + 1
                    neighbor = Board(n, self.boardSize)
                    nStep = self.boardMove(steps, neighbor, prevEmpty)
                    priorityQueue.put((self.priority(neighbor, nDepth), nDepth, n, nStep))
        return None
