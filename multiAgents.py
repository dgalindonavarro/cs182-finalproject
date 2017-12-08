# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
# from game import Directions
import random, util, sys

# from game import Agent
from Snake import Snake

class Agent(Snake):

	# Pick the correct evaluation function
	def evaluationFunction(self, gameState, functionId):
		if functionId == 1:
			return self.evaluationFunction1(gameState)
		elif functionId == 2:
			return self.evaluationFunction2(gameState)
		elif functionId == 3:
			return self.evaluationFunction3(gameState)

	# Simple evaluation function (same as greedy)
	def evaluationFunction1(self, gameState):
		snake = gameState.teams[self.team_id].snakes[self.id]

		if not snake.isAlive():
			return -sys.maxint - 1
		else: 
			newPos = snake.head

			# Get current score
			score = gameState.teams[self.team_id].getScore()

			# Get positions of all food elements
			foodList = gameState.food

			# Initialize distance to closest food
			foodDistance = 0

			# Iterate over food list to find closest distance to food
			for index, food in enumerate(foodList):
				if index == 0:
					foodDistance = manhattanDistance(newPos, food)
				else:
					if manhattanDistance(newPos, food) < foodDistance:
						foodDistance = manhattanDistance(newPos, food)

			return (score * 100) - foodDistance

	# Second evaluation function that takes into account score differentials, total food distances
	# across teammates and opponents, number of snakes alive on each team
	def evaluationFunction2(self, gameState):

		score = 0
		totalFoodDistance = 0
		snakesAlive = 0
		teamSnakesAlive = 0

		# Iterate through teams to get differentials
		for team in gameState.teams:
			if team.id == self.team_id:
				score += team.getScore()
			else:
				score -= team.getScore()
			for snake in team.snakes:
				if snake.isAlive():
					foodDistance = 0
					for index, food in enumerate(gameState.food):
						foo = manhattanDistance(snake.head, food)
						if index == 0 or foo < foodDistance:
							foodDistance = foo

					if team.id == self.team_id:
						totalFoodDistance += foodDistance
						snakesAlive += 1
						teamSnakesAlive += 1
					else:
						totalFoodDistance -= foodDistance
						snakesAlive -= 1

		# If whole team is dead, return largest negative integer
		if teamSnakesAlive == 0:
			return -sys.maxint - 1
		
		return (score * 1000) - (totalFoodDistance * 10) + (snakesAlive * 5000)

	def evaluationFunction3(self, gameState):

		score = 0
		totalFoodDistance = 0
		snakesAlive = 0
		teamSnakesAlive = 0
		opponentsAlive = 0
		distanceToSelf = 0
		length = 0
		distanceToWall = 0

		# Iterate through teams to get differentials, get length and wall distance for correct self
		for team in gameState.teams:
			if team.id == self.team_id:
				score += team.getScore()
			else:
				score -= team.getScore()
			for snake in team.snakes:
				if snake.isAlive():
					foodDistance = 0
					for index, food in enumerate(gameState.food):
						foo = manhattanDistance(snake.head, food)
						if index == 0 or foo < foodDistance:
							foodDistance = foo

					if team.id == self.team_id:
						totalFoodDistance += foodDistance
						teamSnakesAlive += 1
						if snake.id == self.id:
							length = snake.length
							for cell in snake.position:
								distanceToSelf += manhattanDistance(snake.head, cell)
							(x, y) = snake.head
							distanceToWall = max([x-0,gameState.width-x-1,y-0,gameState.height-y-1])
					else:
						totalFoodDistance -= foodDistance
						opponentsAlive -=1

		# Encourage more active killing of opponents and surviving of teammates
		if opponentsAlive == 0 and teamSnakesAlive > 0:
			snakeAlive = 10
		elif opponentsAlive == 0 and score >= 0:
			snakesAlive = 10
		elif teamSnakesAlive == 0:
			return -sys.maxint - 1

		# Get average distance to own tail
		snakesAlive = teamSnakesAlive - opponentsAlive
		if length > 0:
			distanceToSelf = distanceToSelf * 1.0 / length
		else:
			distanceToSelf = 0

		return (score * 10000) - (totalFoodDistance * 100) + (snakesAlive * 50000) + (distanceToSelf * 50) + (distanceToWall * 50)

class ReflexAgent(Snake):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState, functionId):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		actions = self.getActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in actions]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return actions[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState
		successorGameState = currentGameState.generateSuccessor(self.id, self.team_id, action)
		snake = successorGameState.teams[self.team_id].snakes[self.id]

		if not snake.isAlive():
			return -sys.maxint - 1

		else: 
			newPos = snake.head

			# Get current score
			score = successorGameState.teams[self.team_id].getScore()

			# Get positions of all food elements
			foodList = successorGameState.food

			# Initialize distance to closest food
			foodDistance = 0

			# Iterate over food list to find closest distance to food
			for index, food in enumerate(foodList):
				if index == 0:
					foodDistance = manhattanDistance(newPos, food)
				else:
					if manhattanDistance(newPos, food) < foodDistance:
						foodDistance = manhattanDistance(newPos, food)

			# Return evaluation function
			return (score * 100) - foodDistance

class MinimaxAgent(Agent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState, functionId):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.
		  Here are some method calls that might be useful when implementing minimax.
		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1
		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action
		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		self.functionId = functionId

		# Create list of all agents
		self.agent_list = [(self.id, self.team_id)]
		for team in gameState.teams:
			for snake in team.snakes:
				if not (snake.id == self.id and team.id == self.team_id):
					self.agent_list.append((snake.id, team.id))

		# Multiply depth by number of agents
		self.depth = 2 * len(self.agent_list)

		# Get an action from minimax tree
		action = self.value(gameState, 0, 0)
		return action

	def value(self, state, index, depth):
		if depth == self.depth or not state.teams[self.agent_list[index][1]].snakes[self.agent_list[index][0]].isAlive():
			return self.evaluationFunction(state, self.functionId)
		else:
			if self.agent_list[index][1] == self.team_id:
				return self.maxValue(state, index, depth)
			else:
				return self.minValue(state, index, depth)

	def maxValue(self, state, index, depth):
		v = -float("inf") - 1
		act = None
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, (index + 1) % len(self.agent_list), depth + 1)

			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)

			# If we've gotten back to the original function call, return an action instead of a value
			if depth == 0:
				if v < newVal:
					v = newVal
					act = action
			# Otherwise, we just need a value
			else:
				v = max(v, newVal)
		if depth == 0:
			return act
		return v

	def minValue(self, state, index, depth):
		v = float("inf")
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, (index + 1) % len(self.agent_list), depth + 1)
			
			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)

			v = min(v, newVal)
		return v

class AlphaBetaAgent(Agent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState, functionId):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		self.functionId = functionId

		# Create list of all agents
		self.agent_list = [(self.id, self.team_id)]
		for team in gameState.teams:
			for snake in team.snakes:
				if snake.isAlive():
					if not (snake.id == self.id and team.id == self.team_id):
						self.agent_list.append((snake.id, team.id))

		# Multiply depth by number of agents
		self.depth = 2 * len(self.agent_list)

		# Get an action from minimax tree
		action = self.value(gameState, -float("inf") - 1, float("inf"), 0, 0)
		return action

	def value(self, state, alpha, beta, index, depth):
		if depth == self.depth or not state.teams[self.agent_list[index][1]].snakes[self.agent_list[index][0]].isAlive():
			return self.evaluationFunction(state, self.functionId)
		else:
			if self.agent_list[index][1] == self.team_id:
				return self.maxValue(state, alpha, beta, index, depth)
			else:
				return self.minValue(state, alpha, beta, index, depth)

	def maxValue(self, state, alpha, beta, index, depth):
		v = -float("inf") - 1
		act = None
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, alpha, beta, (index + 1) % len(self.agent_list), depth + 1)
			
			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)

			# If we've gotten back to the original function call, return an action instead of a value
			if depth == 0:
				if v < newVal:
					v = newVal
					act = action
			else:
				v = max(v, newVal)

			# Pruning
			if v > beta:
			  return v
			alpha = max(alpha, v)
		if depth == 0:
			return act
		return v

	def minValue(self, state, alpha, beta, index, depth):
		v = float("inf")
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, alpha, beta, (index + 1) % len(self.agent_list), depth + 1)
			
			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)
			
			v = min(v, newVal)

			# Pruning
			if v < alpha:
			  return v
			beta = min(beta, v)
		return v
				  

class ExpectimaxAgent(Agent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState, functionId):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		self.functionId = functionId

		# Create list of all agents
		self.agent_list = [(self.id, self.team_id)]
		for team in gameState.teams:
			for snake in team.snakes:
				if not (snake.id == self.id and team.id == self.team_id):
					self.agent_list.append((snake.id, team.id))

		# Multiply depth by number of agents
		self.depth = 2 * len(self.agent_list)

		# Get an action from expectimax tree
		action = self.value(gameState, 0, 0)
		return action

	def value(self, state, index, depth):
		if depth == self.depth or not state.teams[self.agent_list[index][1]].snakes[self.agent_list[index][0]].isAlive():
			return self.evaluationFunction(state, self.functionId)
		else:
			if self.agent_list[index][1] == self.team_id:
				return self.maxValue(state, index, depth)
			else:
				return self.expValue(state, index, depth)

	def maxValue(self, state, index, depth):
		v = -float("inf") - 1
		act = None
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, (index + 1) % len(self.agent_list), depth + 1)
			
			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)

			# If we've gotten back to the original function call, return an action instead of a value
			if depth == 0:
				if v < newVal:
					v = newVal
					act = action
			else:
				v = max(v, newVal)
		if depth == 0:
			return act
		return v

	def expValue(self, state, index, depth):
		v = 0
		actions = self.getActions()
		for action in actions:
			# Execute move and store old attributes to undo
			direction, position, eaten, add_tail, food = state.executeMove(self.agent_list[index][0], self.agent_list[index][1], action)
			
			# Get value of next state
			newVal = self.value(state, (index + 1) % len(self.agent_list), depth + 1)
			
			# Undo the move after we have the value
			state.undoMove(self.agent_list[index][0], self.agent_list[index][1], direction, position, eaten, add_tail, food)
			
			# Calculate probability of action
			p = 1.0 / len(actions)

			# Added weighted value to total value
			v += newVal * p
		return v
