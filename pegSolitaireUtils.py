import readGame

class game:
	def __init__(self, filePath):
		self.gameState = readGame.readGameState(filePath)
		self.nodesExpanded = 0
		self.trace = []
                
	def get_gameState(self):
                return self.gameState

	def manhattan_distance_heuristic(self):
		"""This heuristic calculates the sum of manhattan distances
		of all the pegs from the centre peg (3,3)
		"""
		value = 0
		for i in range(0,7):
			for j in range(0,7):
				if self.gameState[i][j] == 1:
					value += abs(i - 3) + abs(j - 3)
		return value

	def possible_moves_heuristic(self):
		"""This heuristic increments the cost by 1 for every move which
		is possible from that given state.
		"""
		value = 0
		for i in range(0,7):
			for j in range(0,7):
				if self.gameState[i][j] == 1:
					if self.is_validMove((i,j),'S'):
						value = value + 1
					if self.is_validMove((i,j),'N'):
						value = value + 1
					if self.is_validMove((i,j),'E'):
						value = value + 1
					if self.is_validMove((i,j),'W'):
						value = value + 1
		return value
	
	def is_corner(self, pos):
                
                if pos[0] < 0 or pos[0] > 6 or pos[1] < 0 or pos[1] > 6: 	# Checking if the given position is out of the board.
                    return True
                
                for i in range(0,2):						# Checking if the given position is in top left 2 x 2 square.
                    for j in range(0,2):
                        if pos == (i,j):
                            return True
                        
                for i in range(5,7):						# Checking if the given position is in bottom left 2 x 2 square.
                    for j in range(0,2):
                        if pos == (i,j):
                            return True
						
                for i in range(0,2):						# Checking if the given position is in top right 2 x 2 square.
                    for j in range(5,7):
                        if pos == (i,j):
                            return True
                        
                for i in range(5,7):						# Checking if the given position is in bottom right 2 x 2 square.
                    for j in range(5,7):
                        if pos == (i,j):
                            return True
                
		return False	
	
	
	def getNextPosition(self, oldPos, direction):
				
				#This function just returns the next position from the current position in the given direction.
				#It does not check the validity of the position.
				
                newPos = list(oldPos)
                if(direction == 'N'):
                    newPos[0] = oldPos[0] - 2
                    newPos[1] = oldPos[1]
                    
                if(direction == 'S'):
                    newPos[0] = oldPos[0] + 2
                    newPos[1] = oldPos[1] 
                
                if(direction == 'E'):
                    newPos[0] = oldPos[0] 
                    newPos[1] = oldPos[1] + 2
                
                if(direction == 'W'):
                    newPos[0] = oldPos[0] 
                    newPos[1] = oldPos[1] - 2
                                    
		return tuple(newPos) 
	
	
	def is_validMove(self, oldPos, direction):
		#########################################
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		newPos = self.getNextPosition(oldPos, direction)
		if self.is_corner(newPos):
			return False	
		#########################################
		
		
				#If the new position is out of the board return False
                
                if newPos[0] < 0 or newPos[0] > 6 or newPos[1] < 0 or newPos[1] > 6:
                    return False
                
                #If there is already a marble in new position or the old position does not have a marble, return false            
                if self.gameState[newPos[0]][newPos[1]] == 1 or self.gameState[oldPos[0]][oldPos[1]] == 0:
                    return False
                
                midPos = list(oldPos)
                
				#If there is no marble in the intermediate position while
				# reaching new position from old position, return False
				
                if(direction == 'N'):
                    midPos[0] = midPos[0] - 1
                    if self.gameState[midPos[0]][midPos[1]] == 0:
                        return False

                elif(direction == 'S'):
                    midPos[0] = midPos[0] + 1
                    if self.gameState[midPos[0]][midPos[1]] == 0:
                        return False
                
                elif(direction == 'E'):
                    midPos[1] = midPos[1] + 1
                    if self.gameState[midPos[0]][midPos[1]] == 0:
                        return False
                
                elif(direction == 'W'):
                    midPos[1] = midPos[1] - 1
                    if self.gameState[midPos[0]][midPos[1]] == 0:
                        return False
        
		#If all checks are passed, then it is a valid move
		return True

	def getNextState(self, oldPos, direction):
		
		#This function actually modifies the game state given the current position and the direction to move.
		#This function cross verifies if it is valid to move in the direction mention.
		
		###############################################
		self.nodesExpanded += 1
		if not self.is_validMove(oldPos, direction):
			print "Error, You are not checking for valid move"
			exit(0)
		###############################################
		
				#If it is valid to move from current position in the given direction,
				# update the game state by actually moving the marbles.
                
                newPos = self.getNextPosition(oldPos, direction)
                
                self.gameState[oldPos[0]][oldPos[1]] = 0 	#Remove marble from current position
                self.gameState[newPos[0]][newPos[1]] = 1	#Put the removed marble to the position
				
				#Also remove the marble which is in between current position and new position. 
                
                midPos = list(oldPos) 						
                
                if(direction == 'N'):
                    midPos[0] = midPos[0] - 1
                    self.gameState[midPos[0]][midPos[1]] = 0
                
                elif(direction == 'S'):
                    midPos[0] = midPos[0] + 1
                    self.gameState[midPos[0]][midPos[1]] = 0
                    
                elif(direction == 'E'):
                    midPos[1] = midPos[1] + 1
                    self.gameState[midPos[0]][midPos[1]] = 0
                
                elif(direction == 'W'):
                    midPos[1] = midPos[1] - 1
                    self.gameState[midPos[0]][midPos[1]] = 0
                
                
		return self.gameState
