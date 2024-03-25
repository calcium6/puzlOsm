import copy

class Board:
    def __init__(self, start: list[list[int]], size: int = None):
        self.tiles = start
        if size is None:
            self.size = self.getSize()
            if not self.isSolvable():
                raise Exception("This puzzle combination is not solvable")
        else:
            self.size = size

    def getSize(self) -> int:
        size = len(self.tiles)
        if size < 3:
            raise Exception("Board size is too small")
        for i in range(0, size):
            if size != len(self.tiles[i]):
                raise Exception("Board size invalid")
        return size

    def isGoal(self, goalBoard: list[list[int]]) -> bool:
        return self.tiles == goalBoard
    
    def hamming(self, goalBoard: list[list[int]]) -> int:
        hamming = 0
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.tiles[row][col] != goalBoard[row][col] and self.tiles[row][col] != 0:
                    hamming += 1
        return hamming

    def manhattan(self, startBoard: list[list[int]]) -> int:
        manhattan = 0
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.tiles[row][col] != startBoard[row][col] and self.tiles[row][col] != 0:
                    for startRow in startBoard:
                        if self.tiles[row][col] in startRow:
                            manhattan += abs(row - startBoard.index(startRow))
                            manhattan += abs(col - startRow.index(self.tiles[row][col]))
        return manhattan
    
    def getEmptySpace(self) -> tuple[int, int]:
        for row in self.tiles:
            if 0 in row:
                return (self.tiles.index(row), row.index(0))
            
    def getNeighborCoordinates(self, row: int, col: int) -> list[tuple[int]]:
        neighborCoords = []
        if row+1 < self.size:
            neighborCoords.append((row+1,col))
        if row-1 >= 0:
            neighborCoords.append((row-1,col))
        if col+1 < self.size:
            neighborCoords.append((row,col+1))
        if col-1 >= 0:
            neighborCoords.append((row,col-1))
        return neighborCoords
    
    def switchPositions(self, board: list[list[int]], pos1: tuple[int], pos2: tuple[int]) -> list[list[int]]:
        newBoard = copy.deepcopy(board)
        temp = newBoard[pos1[0]][pos1[1]]
        newBoard[pos1[0]][pos1[1]] = newBoard[pos2[0]][pos2[1]]
        newBoard[pos2[0]][pos2[1]] = temp
        return newBoard
    
    def getNeighbors(self) -> list[list[list[int]]]:
        neighbors = []
        pos = self.getEmptySpace()
        neighborCoords = self.getNeighborCoordinates(pos[0], pos[1])
        for n in neighborCoords:
            neighbors.append(self.switchPositions(self.tiles, pos, n))
        return neighbors
    
    def inversions(self) -> int:
        inv = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.tiles[i][j] != 0:
                    for k in range(i, self.size):
                        for l in range(0, self.size):
                            if not(i == k and l <= j):
                                if self.tiles[k][l] != 0:
                                    if self.tiles[i][j] > self.tiles[k][l]:
                                        inv += 1
        return inv
    
    def isSolvable(self) -> bool:
        if self.size % 2 == 1:
            if self.inversions() % 2 != 0:
                return False
            return True
        else:
            if (self.inversions() + self.getEmptySpace()[0]) % 2 != 1:
                return False
            return True
