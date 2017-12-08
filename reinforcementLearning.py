# qlearningAgents.py
# ------------------
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


from GameState import *
from Snake import Snake
# from learningAgents import ReinforcementAgent
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
	def __init__(self, id, team_id, color, actionFn = None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
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

	def getAction(self, state):
		"""
		  Compute the action to take in the current state.  With
		  probability self.epsilon, we should take a random action and
		  take the best policy action otherwise.  Note that if there are
		  no legal actions, which is the case at the terminal state, you
		  should choose None as the action.

		  HINT: You might want to use util.flipCoin(prob)
		  HINT: To pick randomly from a list, use random.choice(list)
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

	# def getActions(self,state):
 #		"""
 #	  Get the actions available for a given
 #	  state. This is what you should use to
 #	  obtain legal actions for a state
 #	"""
 #	return self.actionFn(state)

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
	# """
	#   Called by environment when new episode is starting
	# """
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
			reward = state.teams[self.team_id].getScore() - self.lastState.teams[self.team_id].getScore()
			self.observeTransition(self.lastState, self.lastAction, state, reward)
		return state

	def registerInitialState(self, state):
		self.startEpisode()
		if self.episodesSoFar == 0:
			print 'Beginning %d episodes of Training' % (self.numTraining)

	# def final(self, state):
    #     """
    #       Called by Pacman game at the terminal state
    #     """
    #     deltaReward = state.teams[self.team_id].getScore() - self.lastState.teams[self.team_id].getScore()
    #     self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
    #     self.stopEpisode()

    #     # Make sure we have this var
    #     if not 'episodeStartTime' in self.__dict__:
    #         self.episodeStartTime = time.time()
    #     if not 'lastWindowAccumRewards' in self.__dict__:
    #         self.lastWindowAccumRewards = 0.0
    #     self.lastWindowAccumRewards += state.getScore()

    #     NUM_EPS_UPDATE = 100
    #     if self.episodesSoFar % NUM_EPS_UPDATE == 0:
    #         print 'Reinforcement Learning Status:'
    #         windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
    #         if self.episodesSoFar <= self.numTraining:
    #             trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
    #             print '\tCompleted %d out of %d training episodes' % (
    #                    self.episodesSoFar,self.numTraining)
    #             print '\tAverage Rewards over all training: %.2f' % (
    #                     trainAvg)
    #         else:
    #             testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
    #             print '\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining)
    #             print '\tAverage Rewards over testing: %.2f' % testAvg
    #         print '\tAverage Rewards for last %d episodes: %.2f'  % (
    #                 NUM_EPS_UPDATE,windowAvg)
    #         print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
    #         self.lastWindowAccumRewards = 0.0
    #         self.episodeStartTime = time.time()

    #     if self.episodesSoFar == self.numTraining:
    #         msg = 'Training Done (turning off epsilon and alpha)'
    #         print '%s\n%s' % (msg,'-' * len(msg))



# class PacmanQAgent(QLearningAgent):
# 	"Exactly the same as QLearningAgent, but with different default parameters"

# 	def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
# 		"""
# 		These default parameters can be changed from the pacman.py command line.
# 		For example, to change the exploration rate, try:
# 			python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

# 		alpha    - learning rate
# 		epsilon  - exploration rate
# 		gamma    - discount factor
# 		numTraining - number of training episodes, i.e. no learning after these many episodes
# 		"""
# 		args['epsilon'] = epsilon
# 		args['gamma'] = gamma
# 		args['alpha'] = alpha
# 		args['numTraining'] = numTraining
# 		self.index = 0  # This is always Pacman
# 		QLearningAgent.__init__(self, **args)

# 	def getAction(self, state):
# 		"""
# 		Simply calls the getAction method of QLearningAgent and then
# 		informs parent of action for Pacman.  Do not change or remove this
# 		method.
# 		"""
# 		action = QLearningAgent.getAction(self,state)
# 		self.doAction(state,action)
# 		return action


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
