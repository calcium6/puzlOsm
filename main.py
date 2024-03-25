import time
from AStar import *
from Result import *
from Board import *

#goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
#start = [[0,1,3],[4,2,5],[7,8,6]]
#start = [[1,2,3],[8,4,6],[0,5,7]]
#start = [[8,6,7],[2,5,4],[3,0,1]]
#start = [[1,2,3,4],[5,6,0,8],[9,10,7,11],[13,14,15,12]]
#start = [[0,1,3],[4,2,5],[7,8,6]]
#start = [[1,3,5],[7,2,6],[8,0,4]]
start = [[1,3,5],[7,2,6],[8,0,4]]
board = Board(start)
goal = [[1,2,3],[4,5,6],[7,8,0]]
goalBoard = Board(goal)
star = AStar(board, goalBoard, True)

startTime = time.time()
result = star.run()
endTime = time.time()

print(f'Time taken: {(endTime-startTime) * 1000:.03f} ms\n')
result.print()
