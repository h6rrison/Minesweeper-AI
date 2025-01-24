# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and ay3 additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================


from AI import AI
from Action import Action

class MyAI(AI):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rows = rowDimension
        self.cols = colDimension
        self.startX = startX
        self.startY = startY
        self.mines = totalMines
        self.grid = [[-1 for x in range(rowDimension)] for y in range(colDimension)]
        self.grid[startX][startY] = 0
        self.lastPosition = (startX, startY)
        self.flags = 0
        self.allMinesFlagged = False

    def getAction(self, number: int) -> "Action Object":
        if number != -1:
            self.grid[self.lastPosition[0]][self.lastPosition[1]] = number
        if self.allMinesFlagged:
            return self.uncoverAll()
        zeroMove = self.uncoverAroundZeros()
        if zeroMove:
            return zeroMove
        neighbourCheck = self.analyzeNeighbours()
        if neighbourCheck:
            return neighbourCheck
        return self.findBestGuess()

    def analyzeNeighbours(self):
        for cellNum in range(1, 9):
            for x in range(self.cols):
                for y in range(self.rows):
                    if self.grid[x][y] == cellNum:
                        coveredNeighbours = []
                        flaggedCellNum = 0
                        for x2 in [-1, 0, 1]:
                            for y2 in [-1, 0, 1]:
                                x3, y3 = x + x2, y + y2
                                if 0 <= x3 < self.cols and 0 <= y3 < self.rows:
                                    if self.grid[x3][y3] == -1:
                                        coveredNeighbours.append((x3, y3))
                                    elif self.grid[x3][y3] == 'flagged':
                                        flaggedCellNum += 1
                        if len(coveredNeighbours) + flaggedCellNum == cellNum:
                            for coveredX, coveredY in coveredNeighbours:
                                self.flags += 1
                                if self.flags == self.mines:
                                    self.allMinesFlagged = True
                                self.grid[coveredX][coveredY] = 'flagged'
                                return Action(AI.Action.FLAG, coveredX, coveredY)
                        if flaggedCellNum == cellNum and coveredNeighbours:
                            self.lastPosition = coveredNeighbours[0]
                            return Action(AI.Action.UNCOVER, coveredNeighbours[0][0], coveredNeighbours[0][1])

    def uncoverAll(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.grid[x][y] == -1:
                    self.lastPosition = (x, y)
                    return Action(AI.Action.UNCOVER, x, y)
        return Action(AI.Action.LEAVE)

    def uncoverAroundZeros(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.grid[x][y] == 0:
                    for x2 in [-1, 0, 1]:
                        for y2 in [-1, 0, 1]:
                            x3, y3 = x + x2, y + y2
                            if 0 <= x3 < self.cols and 0 <= y3 < self.rows:
                                if self.grid[x3][y3] == -1:
                                    self.lastPosition = (x3, y3)
                                    return Action(AI.Action.UNCOVER, x3, y3)
                                
    def findBestGuess(self):
        minPercentage = 2.0
        bestGuess = None
        for x in range(self.cols):
            for y in range(self.rows):
                if self.grid[x][y] == -1:
                    percentage = self.calculatePercentage(x,y)
                    if percentage < minPercentage:
                        minPercentage = percentage
                        bestGuess = (x, y)
        if bestGuess:
            self.lastPosition = bestGuess
            return Action(AI.Action.UNCOVER, bestGuess[0], bestGuess[1])
        return Action(AI.Action.LEAVE)

    def calculatePercentage(self, x, y):
        totalpercentage = 0
        relevantLabels = 0
        for x2 in [-1, 0, 1]:
            for y2 in [-1, 0, 1]:
                x3, y3 = x + x2, y + y2
                if 0 <= x3 < self.cols and 0 <= y3 < self.rows:
                    neighbourLabel = self.grid[x3][y3]
                    if isinstance(neighbourLabel, int) and 1 <= neighbourLabel <= 8:
                        coveredNeighbours = self.coveredNeighbours(x3, y3)
                        flaggedNeighbours = self.flaggedNeighbours(x3, y3)
                        remainingMines = neighbourLabel - flaggedNeighbours
                        if remainingMines > 0 and coveredNeighbours > 0:
                            currentPercentage = remainingMines / coveredNeighbours
                            totalpercentage += currentPercentage
                            relevantLabels += 1
        if relevantLabels > 0:
            return totalpercentage / relevantLabels
        return 1.0
    
    def coveredNeighbours(self, x, y):
        coveredNeighboursCount = 0
        for x2 in [-1, 0, 1]:
            for y2 in [-1, 0, 1]:
                x3, y3 = x + x2, y + y2
                if 0 <= x3 < self.cols and 0 <= y3 < self.rows and self.grid[x3][y3] == -1:
                    coveredNeighboursCount += 1
        return coveredNeighboursCount

    def flaggedNeighbours(self, x, y):
        flaggedNeighboursCount = 0
        for x2 in [-1, 0, 1]:
            for y2 in [-1, 0, 1]:
                x3, y3 = x + x2, y + y2
                if 0 <= x3 < self.cols and 0 <= y3 < self.rows and self.grid[x3][y3] == 'flagged':
                    flaggedNeighboursCount += 1
        return flaggedNeighboursCount