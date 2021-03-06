# qlearningAgents.py
# ------------------
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import random, util, sys
from util import manhattanDistance
from GameState import *
from Snake import Snake
from featureExtractors import *

import random,util,math,numpy

class QLearningAgent(Snake):
	"""
	  Q-Learning Agent

	  Functions you should fill in:
		- computeValueFromQValues
		- computeActionFromQValues
		- getQValue
		- getAction
		- update

	  Instance variables you have access to
		- self.epsilon (exploration prob)
		- self.alpha (learning rate)
		- self.discount (discount rate)

	  Functions you should use
		- self.getLegalActions(state)
		  which returns legal actions for a state
	"""
	def __init__(self, id, team_id, color, actionFn = None, numTraining=100, epsilon=0.5, alpha=0.3, gamma=0.9):
		# OUR OTHER SNAKE CLASS MEMBERS (same as other types of snakes)
		self.id = id
		self.position = []
		self.head = False
		self.length = 0
		self.direction = None
		self.team_id = team_id
		self.add_tail = False
		self.eaten = []
		self.color = color

		if actionFn == None:
			actionFn = self.getActions()

		self.actionFn = actionFn
		self.episodesSoFar = 0
		self.accumTrainRewards = 0.0
		self.accumTestRewards = 0.0
		self.numTraining = int(numTraining)
		self.epsilon = float(epsilon)
		self.alpha = float(alpha)
		self.discount = float(gamma)

		self.qValues = {}

	def getQValue(self, state, action):
		"""
		  Returns Q(state,action)
		  Should return 0.0 if we have never seen a state
		  or the Q node value otherwise
		"""
		"*** YOUR CODE HERE ***"
		if (state, action) not in self.qValues:
			return 0.
		return self.qValues[(state, action)]


	def computeValueFromQValues(self, state):
		"""
		  Returns max_action Q(state,action)
		  where the max is over legal actions.  Note that if
		  there are no legal actions, which is the case at the
		  terminal state, you should return a value of 0.0.
		"""
		"*** YOUR CODE HERE ***"
		actions = self.getActions()
		if actions:
			return max([self.getQValue(state, action) for action in actions])
		return 0.

	def computeActionFromQValues(self, state):
		"""
		  Compute the best action to take in a state.  Note that if there
		  are no legal actions, which is the case at the terminal state,
		  you should return None.
		"""
		"*** YOUR CODE HERE ***"
		actions = self.getActions()
		if actions:
			return actions[numpy.argmax([self.getQValue(state, action) for action in actions])]

		return None

	def getAction(self, state, functionId):
		"""
		  Compute the action to take in the current state.  With
		  probability self.epsilon, we should take a random action and
		  take the best policy action otherwise.  Note that if there are
		  no legal actions, which is the case at the terminal state, you
		  should choose None as the action.
		"""
		# Pick Action
		actions = self.getActions()
		action = None
		"*** YOUR CODE HERE ***"
		if actions:
			if random.random() < self.epsilon:
				action = random.choice(actions)
			else:
				action = self.computeActionFromQValues(state)

		self.lastState = state
		self.lastAction = action

		return action

	def update(self, state, action, nextState, reward):
		"""
		  The parent class calls this to observe a
		  state = action => nextState and reward transition.
		  You should do your Q-Value update here

		  NOTE: You should never call this function,
		  it will be called on your behalf
		"""
		"*** YOUR CODE HERE ***"
		self.qValues[(state, action)] = (((1. - self.alpha)
											* self.getQValue(state, action))
											+ (self.alpha
												* (reward
													+ (self.discount
														* (self.getValue(nextState))))))

	def getPolicy(self, state):
		return self.computeActionFromQValues(state)

	def getValue(self, state):
		return self.computeValueFromQValues(state)

	def observeTransition(self, state,action,nextState,deltaReward):
		# """
		# 	Called by environment to inform agent that a transition has
		# 	been observed. This will result in a call to self.update
		# 	on the same arguments

		# 	Note: Do *not* override or call this function
		# """
		self.episodeRewards += deltaReward
		self.update(state,action,nextState,deltaReward)

	def startEpisode(self):
		"""
		  Called by environment when new episode is starting
		"""
		self.lastState = None
		self.lastAction = None
		self.episodeRewards = 0.0

	def stopEpisode(self):
		"""
		Called by environment when episode is done
		"""
		if self.episodesSoFar < self.numTraining:
			self.accumTrainRewards += self.episodeRewards
		else:
			self.accumTestRewards += self.episodeRewards
			self.episodesSoFar += 1
			if self.episodesSoFar >= self.numTraining:
				# Take off the training wheels
				self.epsilon = 0.0 		# no exploration
				self.alpha = 0.0	   # no learning

	def isInTraining(self):
		return self.episodesSoFar < self.numTraining

	def isInTesting(self):
		return not self.isInTraining()

	def observationFunction(self, state):
		"""
			This is where we ended up after our last action.
			The simulation should somehow ensure this is called
		"""
		if not self.lastState is None:
			reward = self.evaluationFunction(state) - self.evaluationFunction(self.lastState)
			self.observeTransition(self.lastState, self.lastAction, state, reward)
		return state

	def evaluationFunction(self, state):
		snake = state.teams[self.team_id].snakes[self.id]

		if not snake.isAlive():
			return -sys.maxint - 1
		else: 
			newPos = snake.head

			# Get current score
			score = state.teams[self.team_id].getScore()

			# Get positions of all food elements
			foodList = state.food

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

	def registerInitialState(self, state):
		self.startEpisode()
		if self.episodesSoFar == 0:
			print 'Beginning %d episodes of Training' % (self.numTraining)


class ApproximateQAgent(QLearningAgent):
 	"""
 	   ApproximateQLearningAgent

 	   You should only have to overwrite getQValue
 	   and update.  All other QLearningAgent functions
 	   should work as is.
 	"""
 	def __init__(self, id, team_id, color, extractor='IdentityExtractor', **args):

		self.qValues = {}

 		#self.featExtractor = util.lookup(extractor, globals())()
 		QLearningAgent.__init__(self, id, team_id, color, **args)
 		self.weights = util.Counter()

 	def getWeights(self):
 		return self.weights

 	def getQValue(self, state, action):
 		"""
 		  Should return Q(state,action) = w * featureVector
 		  where * is the dotProduct operator
 		"""
 		"*** YOUR CODE HERE ***"
 		features = self.getFeatures(state, action)
 		q = 0.
 		for feature in features:
 			if feature in self.getWeights():
 				q += self.weights[feature] * features[feature]
 		return q

 	def update(self, state, action, nextState, reward):
 		"""
 		   Should update your weights based on transition
 		"""
 		"*** YOUR CODE HERE ***"
		
 		features = self.getFeatures(state, action)
 		weights = self.weights.copy()
 		for feature in features:
 			weight = 0
 			if feature in self.weights:
 				weight = self.weights[feature]
 			difference = (reward + (self.discount * self.getValue(nextState))
 								- self.getQValue(state, action))
 			weights[feature] = weight + (self.alpha * difference * features[feature])
 		self.weights = weights

 	def final(self, state):
 		"Called at the end of each game."
 		# call the super-class final method
 		PacmanQAgent.final(self, state)

 		# did we finish training?
 		if self.episodesSoFar == self.numTraining:
 			# you might want to print your weights here for debugging
 			"*** YOUR CODE HERE ***"
 			pass

	def getFeatures(self, state, action):
		# extract the grid of food and wall locations and get the ghost locations
		food = state.food
		legalPositions = state.legalPositions
		qSnake = state.teams[0].snakes[0]

		enemysnakes = []
		# assuming only ever Team 1, Snake 1 is learning
		for team in state.teams[1:]:
			for snake in team.snakes:
				enemysnakes = enemysnakes + snake.position

		friendlies = []
		for snake in state.teams[0].snakes[1:]:
			friendlies = friendlies + snake.position

		features = util.Counter()

		features["bias"] = 1.0

		# compute the location of snake after he takes the action
		oldhead = qSnake.head
		olddirection, oldposition, oldeaten, oldadd_tail, oldfood = state.executeMove(0, 0, action)
		
		newdirection = qSnake.direction
		neweaten = qSnake.eaten
		newhead = qSnake.head
		newposition = qSnake.position
		neweaten = qSnake.eaten
		
		if qSnake.isAlive():
			features["isLiving"] = 1.0
			features["score"] = state.teams[0].getScore()*100.0

			state.undoMove(0, 0, olddirection, oldposition, oldeaten, oldadd_tail, oldfood)
			
			#radius of compactness
			r = int(qSnake.length/5) 

			# measure the compactness of the snake
			# surrounding blocks
			radius = []
			for i in range(-r, r+1):
				for j in range(-r, r+1):
					point = (newhead[0] + r, newhead[1] + r)
					if point in legalPositions:
						radius.append(point)

			tailsclose = 0
			for tail in newposition: 
				if tail in radius: 
					tailsclose += 1
			if len(radius) != 0:
				compact = float(tailsclose)/float(len(radius))
			else:
				compact = 0

			features["Snake Compactness"] = compact*10

			# if snake is not too compact then add distance to food
			if compact < 0.5:
				# Initialize distance to closest food
				foodDistance = 0

				# Iterate over food list to find closest distance to food
				for index, f in enumerate(food):
					if index == 0:
						foodDistance = util.manhattanDistance(newhead, f)
					else:
						if util.manhattanDistance(newPos, f) < foodDistance:
							foodDistance = util.manhattanDistance(newhead, f)

				features["Dist to Food"] = foodDistance
		else:
			features["isLiving"] = 0

		features.divideAll(10.0)
		return features
