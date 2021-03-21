import numpy as np
from random import randint, seed
import pickle
import pdb

ROUNDS = 1000
class Q1:
	def __init__(self, grid, t):
		self.grid = grid
		self.t = t
		self.width = len(grid)
		self.OMap = np.zeros(grid.shape)
		self.XMap = np.zeros(grid.shape)
		self.agentCount = 0
		self.forEachPerson(self.populateNeighbor)
		

	def populateNeighbor(self, row, col):
		def initMap(i,j):
			if i == row and j == col: return
			if self.grid[row][col] == 'O':
				self.OMap[i][j]+=1 
			elif self.grid[row][col] == 'X':
				self.XMap[i][j] +=1
		if self.grid[row][col] != '.': 
			self.agentCount += 1
		self.loopOverNeighbor(row, col, initMap)

	def forEachPerson(self, func):
		for row in range(self.width):
			for col in range(self.width):
				target = self.grid[row][col]
				if target != '.':
					func(row, col)

	def loopOverNeighbor(self, row, col, func):
		for i in range(max(0, row-1), min(self.width, row+2)):
			for j in range(max(0, col-1), min(self.width, col+2)):
				func(i, j)

	def moveNeighbor(self, target, oldr, oldc):
		m = self.OMap if target == 'O' else self.XMap
		
		def updateMap(i, j, tr, tc, v):
			if i!=tr or j != tc:
				m[i][j] = m[i][j] + v
		def isValidChoice(row, col):
			return (
				abs(row-oldr) >1 or abs(col-oldc) > 1 and \
				m[row][col] == self.t or m[row][col] > self.t
			) and self.grid[row][col] == '.'
		
		validChoices = [(row, col) for row in range(self.width) for col in range(self.width) if isValidChoice(row, col)]
		if len(validChoices) == 0: return False
		randChoice = randint(0, len(validChoices)-1)
		row, col = validChoices[randChoice]
		self.grid[row][col] = target
		self.grid[oldr][oldc] = '.'
		self.loopOverNeighbor(oldr, oldc, lambda i, j: updateMap(i, j, oldr, oldc, -1))
		self.loopOverNeighbor(row, col, lambda i, j: updateMap(i, j, row, col, 1))
		return True

	def getSimNeigherFraction(self, symbol):
		m = self.OMap if symbol == 'O' else self.XMap
		totalNeighbor = self.OMap + self.XMap
		zeros = totalNeighbor==0
		totalNeighbor[zeros] = 1
		m = m/totalNeighbor
		return sum(m[self.grid == symbol])

	def simulate(self):
		simularNeighbor = np.zeros(ROUNDS+1)
		hasMoved = 0
		# def handleNeighbor(time, row, col):
		# 	target = self.grid[row][col]
		# 	count, isValid = self.isValidNeighbors(target, row, col)
		# 	if not isValid:
		# 		hasMoved[0] += 1
		# 		self.moveNeighbor(target, row, col)

			# return sum([m[row][col]/(max(totalNeighbor[row][col], 1)) \
			# 	for row in range(self.width) for col in range(self.width) \
			# 	if self.grid[row][col] ==symbol
			# 	])
		while hasMoved < ROUNDS:
			status = False
			hasInvalid = False
			for row in range(self.width):
				if hasMoved >= ROUNDS: break
				simularNeighbor[hasMoved] += self.getSimNeigherFraction('O')
				simularNeighbor[hasMoved] += self.getSimNeigherFraction('X')
				hasMoved += 1
				for col in range(self.width):
					target = self.grid[row][col]
					if target != '.':
						isValid = self.isValidNeighbors(target, row, col)
						if not isValid:
							hasInvalid = True
							status1 = self.moveNeighbor(target, row, col)
							status = status1 or status

			if not status and hasInvalid:
				print("no more satisfy neighbor")
				break
		simularNeighbor[hasMoved] = self.getSimNeigherFraction('O') + self.getSimNeigherFraction('X')
		return simularNeighbor/self.agentCount

	def isValidNeighbors(self,target, row, col):
		if target == 'O':
			return self.OMap[row][col] >= self.t
		else:
			return self.XMap[row][col] >= self.t

def parseFile(path):
	grid = []
	with open(path, 'r') as f:
		line = f.readline()
		while (line):
			grid.append(line.strip().split('\t'))
			line = f.readline()
	return grid
if __name__ == "__main__":
	
	seed(2048)
	#grid = np.array([['X', '.', 'O'], ['.','.','.'],['O', 'X','.']])
	TIMES = 5
	LOW_T = 6
	HIGH_T = 6
	total_stats = []
	for threshold in range(LOW_T, HIGH_T+1):
		print("========="+str(threshold)+"==========")
		stats = np.zeros(ROUNDS+1)
		for i in range(TIMES):
			grid = np.array(parseFile('grid.txt'))
			q1 = Q1(grid, threshold)
			print(i)
			stats += q1.simulate()
		stats /= TIMES
		total_stats.append(stats)
		pickle.dump( total_stats, open( "q1_stats_new6.p", "wb" ) )
	# print(q1.grid)
	# print(q1.XMap)
	# print(q1.OMap)
	# print("-------------")
