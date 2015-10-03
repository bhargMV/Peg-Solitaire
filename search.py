import pegSolitaireUtils
import config
import copy
import sys
import Queue as Q

#custom stack class to store trace
class Stack:

     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
     
     def print_stack(self):
        for e in reversed(self.items):
            print e
             
     def empty(self):
         while self.isEmpty() == False:
             self.pop()        
    

S = Stack() 	#Stores the current trace. If the goal state is reached, the stack contains the path from start to goal.
N = 0			#No. of nodes expanded

def string_game_state_list(gameState):
    """
    :param gameState:
    :return: The string representation of the game state
    All the items in the board are appended together to form a string.
    '-1' is not considered in the item list.
    """

    string_state = ''
    for innerList in gameState:
        for item in innerList:
            if str(item) != "-1":
                string_state += str(item)
    return string_state

def generate_trace(trace_dict, final_state_string):
    """
    :param trace_dict:  A dictionary which stores the game
    state (in string) and the moves to and from that state
    :param final_state_string: Final string state of the board
    :return: The final trace of the moves from start to goal state

    This function iteratively traverses through all the states
    and returns the set of moves to reach goal state.
    """
    check_key = final_state_string
    trace_list = []
    while True:
        if trace_dict.has_key(check_key):
            trace_list.append(trace_dict[check_key][1][1])
            trace_list.append(trace_dict[check_key][1][0])
            check_key = trace_dict[check_key][0]
        else:
            break
    return trace_list[::-1]

def isGoalState(gameState):
    """
    :param gameState: The state of the game
    :return: True / False based on whether the gameState is goal or not
    Checks if the entire board is empty except the centre. If yes return True, else False
    """
    if gameState[3][3] != 1:
        return False
    
    for i in range(0,7):
        for j in range(0,7):
            if (i != 3 or j != 3) and (gameState[i][j] == 1):
                return False
            
    return True

def ItrDeepSearch(pegSolitaireObject):
	global N
	#Run Iterative Deepening Search for all possible start positions of given game state.
        for i in range(0,7):
            for j in range(0,7):
                if pegSolitaireObject.gameState[i][j] == 1:
					#Vary the depths while calling depth limited search on chosen start position and game state
                    for d in range(1, 30):
                        tempGameObj = copy.deepcopy(pegSolitaireObject)
                        tempD = copy.deepcopy(d)

						# If depth limited search for particular depth returns true,
						# then update the trace and nodes expanded of the initial game object and return.
                        if depLimSearch((i,j), tempGameObj, tempD) == True:
                            # global N
                            pegSolitaireObject.nodesExpanded = N
                            pegSolitaireObject.trace = S.items
                            return
							
						#If depth limited search for particular depth returns False,
						# then re-initialize the nodes expanded to zero and empty the stack.
                        else:
                            # global N
                            N = 0
                        S.empty()

        return
    
def depLimSearch(start,pegSolitaireObject,d):
    
	#Push the start position to the stack
    S.push(start)
    
	#If depth = 1, stop exploring further nodes. If the current state is goal state, then return true else return false
    if d == 1:
        if isGoalState(pegSolitaireObject.gameState):
            S.pop()
            global N
            N = N + 1
            return True
        else:
            S.pop()
            return False
    
	#If there is a valid next possible move towards north from the current position, push this next position to the stack.
	#Update the game state, call depLimSearch for depth d-1 and for all possible start states in the updated game object.
	#If any of the depth limited search returns true(i.e there exists a goal state in the particular path) return true.
	#If there is no way to reach goal state pop the stack and try with different possible next position.
	
    if pegSolitaireObject.is_validMove(start, 'N') == True:
        tempObj = copy.deepcopy(pegSolitaireObject)
        S.push(tempObj.getNextPosition(start, 'N'))
        tempObj.gameState = tempObj.getNextState(start, 'N')
               
        for i in range(0,7):
            for j in range(0,7):
                if tempObj.gameState[i][j] == 1:
                    newObj = copy.deepcopy(tempObj)
                    # global N
                    N = N + 1
                    if depLimSearch((i, j), newObj, copy.deepcopy(d)-1) == True:
                        del newObj                        
                        return True
                    else:
                        del newObj 
        S.pop()

	#If there is a valid next possible move towards south from the current position, push this next position to the stack.
	#Update the game state, call depLimSearch for depth d-1 and for all possible start states in the updated game object.
	#If any of the depth limited search returns true(i.e there exists a goal state in the particular path) return true.
	#If there is no way to reach goal state pop the stack and try with different possible next position.
	
    if pegSolitaireObject.is_validMove(start, 'S') == True:
        tempObj = copy.deepcopy(pegSolitaireObject)
        S.push(tempObj.getNextPosition(start, 'S'))
        tempObj.gameState = tempObj.getNextState(start, 'S')
               
        for i in range(0,7):
            for j in range(0,7):
                if tempObj.gameState[i][j] == 1:
                    newObj = copy.deepcopy(tempObj)
                    # global N
                    N = N + 1
                    if depLimSearch((i, j), newObj, copy.deepcopy(d)-1) == True:
                        del newObj                        
                        return True
                    else:
                        del newObj
        S.pop()
                        
	#If there is a valid next possible move towards East from the current position, push this next position to the stack.
	#Update the game state,call depLimSearch for depth d-1 and for all possible start states in the updated game object.
	#If any of the depth limited search returns true(i.e there exists a goal state in the particular path) return true.
	#If there is no way to reach goal state pop the stack and try with different possible next position.
	
    if pegSolitaireObject.is_validMove(start, 'E') == True:
        tempObj = copy.deepcopy(pegSolitaireObject)
        S.push(tempObj.getNextPosition(start, 'E'))
        tempObj.gameState = tempObj.getNextState(start, 'E')
               
        for i in range(0,7):
            for j in range(0,7):
                if tempObj.gameState[i][j] == 1:
                    newObj = copy.deepcopy(tempObj)
                    # global N
                    N = N + 1
                    if depLimSearch((i, j), newObj, copy.deepcopy(d)-1) == True:
                        del newObj                        
                        return True
                    else:
                        del newObj
        S.pop()

	#If there is a valid next possible move towards West from the current position, push this next position to the stack.
	#Update the game state, call depLimSearch for depth d-1 and for all possible start states in the updated game object.
	#If any of the depth limited search returns true(i.e there exists a goal state in the particular path) return true.
	#If there is no way to reach goal state pop the stack.
	
    if pegSolitaireObject.is_validMove(start, 'W') == True:
        tempObj = copy.deepcopy(pegSolitaireObject)
        S.push(tempObj.getNextPosition(start, 'W'))
        tempObj.gameState = tempObj.getNextState(start, 'W')
                
        for i in range(0,7):
            for j in range(0,7):
                if tempObj.gameState[i][j] == 1:
                    newObj = copy.deepcopy(tempObj)
                    # global N
                    N = N + 1
                    if depLimSearch((i, j), newObj, copy.deepcopy(d)-1) == True:
                        del newObj                       
                        return True
                    else:
                        del newObj
        S.pop()
	
	#If there is no way to reach a goal state from the given start position and the game state,
	# then pop the start position from the stack.
	
    S.pop()
	
	#Return False if goal state cannot be reached.
    
    return False
    
    
	
	
def aStarTwo(pegSolitaireObject):
    """
    :param pegSolitaireObject:
    :return: None
    The function runs the A* search algorithm using a priority queue
    and saves the trace in pegSolitaireObject.
    Manhattan Heuristic is used
    """

    # Initialize a empty priority queue
    # It stores f_Value, game state string and the pegSolitaireObject

    priority_queue = Q.PriorityQueue()
    h_value = pegSolitaireObject.manhattan_distance_heuristic()
    game_state_string_g = string_game_state_list(pegSolitaireObject.gameState)
    closed = []
    visited = [game_state_string_g]
    g_val = dict()
    g_val[game_state_string_g] = 1
    f_value = h_value + g_val[game_state_string_g]
    priority_queue.put((f_value, game_state_string_g, pegSolitaireObject))
    trace_dict = {}

    while not priority_queue.empty():
        (f_val, game_state_string, game_state_obj) = priority_queue.get()
        if isGoalState(game_state_obj.gameState):
            pegSolitaireObject.nodesExpanded = len(closed)
            pegSolitaireObject.trace = \
                generate_trace(trace_dict, string_game_state_list(game_state_obj.gameState))
            return
        visited.remove(game_state_string) # Remove this node from visited list
        closed.append(game_state_string)  # Add it to the closed list

        neighbours = []

        for i in range(0, 7):
            for j in range(0, 7):
                pos = (i, j)
                game_state = game_state_obj.gameState

                # If towards south there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'S'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'S')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i+2, j))))

                # If towards north there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'N'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'N')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i-2, j))))

                # If towards east there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'E'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'E')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i, j+2))))

                # If towards west there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'W'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'W')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i, j-2))))


        for neighbour_tuple in neighbours:
            neighbour = neighbour_tuple[0]
            new_state_string = string_game_state_list(neighbour.gameState)
            # Check if this state is already in closed list
            if new_state_string in closed:
                continue

            prev_state_string = string_game_state_list(game_state_obj.gameState)
            new_g_score = g_val[prev_state_string] + 1
            # Check if new state is not visited or has a better g-score
            if (new_state_string not in visited) or (new_g_score < g_val[new_state_string]):
                g_val[new_state_string] = new_g_score
                # Calculate new f score using heuristic and g-value
                f_val_new = g_val[new_state_string] + neighbour.manhattan_distance_heuristic()
                visited.append(new_state_string)
                # Store the trace in dictionary
                trace_dict[new_state_string] = (prev_state_string, neighbour_tuple[1])
                priority_queue.put((f_val_new, new_state_string, neighbour))


def aStarOne(pegSolitaireObject):
    """
    :param pegSolitaireObject:
    :return: None
    The function runs the A* search algorithm using a priority queue
    and saves the trace in pegSolitaireObject.
    Possible Move Heuristic is used
    """

    # Initialize a empty priority queue
    # It stores f_Value, game state string and the pegSolitaireObject

    priority_queue = Q.PriorityQueue()
    h_value = pegSolitaireObject.possible_moves_heuristic()
    game_state_string_g = string_game_state_list(pegSolitaireObject.gameState)
    closed = []
    visited = [game_state_string_g]
    g_val = dict()
    g_val[game_state_string_g] = 1
    f_value = h_value + g_val[game_state_string_g]
    priority_queue.put((f_value, game_state_string_g, pegSolitaireObject))
    trace_dict = {}

    while not priority_queue.empty():
        (f_val, game_state_string, game_state_obj) = priority_queue.get()
        if isGoalState(game_state_obj.gameState):
            pegSolitaireObject.nodesExpanded = len(closed)
            pegSolitaireObject.trace = \
                generate_trace(trace_dict, string_game_state_list(game_state_obj.gameState))
            return
        visited.remove(game_state_string) # Remove from visited list
        closed.append(game_state_string) # mark this state / node as closed

        neighbours = []

        for i in range(0, 7):
            for j in range(0, 7):
                pos = (i, j)
                game_state = game_state_obj.gameState

                # If towards south there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'S'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'S')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i+2, j))))

                # If towards north there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'N'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'N')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i-2, j))))

                # If towards east there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'E'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'E')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i, j+2))))

                # If towards west there is a valid move, then push the new state in the possible neighbours list
                if game_state[i][j] == 1 and game_state_obj.is_validMove(pos, 'W'):
                    temp_state = copy.deepcopy(game_state_obj)
                    temp_game_state = temp_state.getNextState(pos, 'W')
                    temp_state.gameState = temp_game_state
                    neighbours.append((temp_state, (pos, (i, j-2))))


        for neighbour_tuple in neighbours:
            neighbour = neighbour_tuple[0]
            new_state_string = string_game_state_list(neighbour.gameState)
            if new_state_string in closed:
                continue

            prev_state_string = string_game_state_list(game_state_obj.gameState)
            new_g_score = g_val[prev_state_string] + 1
            # If the new state is not visited or has a better g score
            if (new_state_string not in visited) or (new_g_score < g_val[new_state_string]):
                g_val[new_state_string] = new_g_score
                # Calculate new f score using heuristic and g-value
                f_val_new = g_val[new_state_string] + neighbour.possible_moves_heuristic()
                visited.append(new_state_string)
                # Store the trace in dictionary
                trace_dict[new_state_string] = (prev_state_string, neighbour_tuple[1])
                priority_queue.put((f_val_new, new_state_string, neighbour))
