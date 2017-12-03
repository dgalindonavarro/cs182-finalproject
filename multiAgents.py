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

class ReflexAgent(Snake):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        # legalMoves = gameState.getLegalActions()
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
        newPos = successorGameState.teams[self.team_id].snakes[self.id].head

        if newPos == None:
          return -sys.maxint - 1
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

        # Initialize distance to closest ghost
        # ghostDistance = 0

        # # Iterate over ghost list to find closest distance to ghost
        # for index, ghost in enumerate(newGhostStates):
        #   if index == 0:
        #     ghostDistance = manhattanDistance(newPos, ghost.getPosition())
        #   else:
        #     if manhattanDistance(newPost, ghost.getPosition()) < ghostDistance:
        #       ghostDistance = manhattanDistance(newPos, ghost.getPosition())

        # Return evaluation function
        return (score * 100) - foodDistance

# def scoreEvaluationFunction(currentGameState):
#     """
#       This default evaluation function just returns the score of the state.
#       The score is the same one displayed in the Pacman GUI.

#       This evaluation function is meant for use with adversarial search agents
#       (not reflex agents).
#     """
#     return currentGameState.getScore()

# class MultiAgentSearchAgent(Agent):
#     """
#       This class provides some common elements to all of your
#       multi-agent searchers.  Any methods defined here will be available
#       to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

#       You *do not* need to make any changes here, but you can if you want to
#       add functionality to all your adversarial search agents.  Please do not
#       remove anything, however.

#       Note: this is an abstract class: one that should not be instantiated.  It's
#       only partially specified, and designed to be extended.  Agent (game.py)
#       is another abstract class.
#     """

#     def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
#         self.index = 0 # Pacman is always agent index 0
#         self.evaluationFunction = util.lookup(evalFn, globals())
#         self.depth = int(depth)

class MinimaxAgent(Snake):
    """
      Your minimax agent (question 2)
    """

    def evaluationFunction(self, gameState):
        newPos = gameState.teams[self.team_id].snakes[self.id].head

        if newPos == None:
          return -sys.maxint - 1
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

    def getAction(self, gameState):
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
        self.agent_list = [(self.id, self.team_id)]
        for team in gameState.teams:
            for snake in team.snakes:
                if not (snake.id == self.id and team.id == self.team_id):
                    self.agent_list.append((snake.id, team.id))
        self.depth = 1 * len(self.agent_list)
        action = self.value(gameState, 0, 0)
        return action

    def value(self, state, index, depth):
        if depth == self.depth or not state.teams[self.agent_list[index][1]].snakes[self.agent_list[index][0]].isAlive():
            return self.evaluationFunction(state)
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
            successorState = state.generateSuccessor(self.agent_list[index][0], self.agent_list[index][1], action)
            newVal = self.value(successorState, (index + 1) % len(self.agent_list), depth + 1)

            if depth == 0:
                if v < newVal:
                    v = newVal
                    act = action
            else:
                v = max(v, newVal)
        if depth == 0:
            return act
        return v

    def minValue(self, state, index, depth):
        v = float("inf")
        actions = self.getActions()
        for action in actions:
            successorState = state.generateSuccessor(self.agent_list[index][0], self.agent_list[index][1], action)
            newVal = self.value(successorState, (index + 1) % len(self.agent_list), depth + 1)
            v = min(v, newVal)
        return v


        # def value(state, agent_id, team_id, depth):
        #   # print depth
        #   # print "Id", agent_id
        #   # print self.id
        #   # print "Team", team_id
        #   # print "My team is team", self.team_id
        #   # If at a terminal state or if max-depth has been reached, return
        #   # evaluation function
        #   # if state.isWin() or state.isLose() or (depth == 0 and agentIndex == 0):
        #   if (depth == 0 and agent_id == self.id and team_id == self.team_id):
        #     return self.evaluationFunction(state)

        #   # Otherwise, check whether next agent is min or max
        #   else:
        #     if team_id == self.team_id:
        #       v, action = maxValue(state, agent_id, team_id, depth)
        #       return v
        #     else:
        #       v, action = minValue(state, agent_id, team_id, depth)
        #       return v

        # def maxValue(state, agent_id, team_id, depth):
        #   # print "Depth Min:", depth
        #   v = -sys.maxint - 1

        #   agent = state.teams[team_id].snakes[agent_id]
        #   # Loop through all possible legal actions
        #   for index, action in enumerate(agent.getActions()):
        #     if state.teams[team_id].snakes[agent_id].isAlive():
        #         successorState = state.generateSuccessor(agent_id, team_id, action)
        #     else:
        #         successorState = state.deepCopy()

        #     if agent_id == self.id and len(state.teams[team_id].snakes) > 1:
        #         next_agent = (agent_id + 1) % len(state.teams[team_id].snakes)
        #         next_team = team_id
        #     else:
        #         next_agent = 0
        #         next_team = (team_id + 1) % len(state.teams)

        #     # Get value of successor state
        #     nextValue = value(successorState, next_agent, next_team, depth - 1)
        #     # If greater than v, assign to v
        #     if nextValue > v:
        #       v = nextValue
        #       bestAction = action
        #   # Return v and the associated action
        #   return v, bestAction

        # def minValue(state, agent_id, team_id, depth):
        #   # print "Depth Max:", depth
        #   v = sys.maxint

        #   agent = state.teams[team_id].snakes[agent_id]
        #   # Loop through all possible legal actions
        #   for index, action in enumerate(agent.getActions()):
        #     if state.teams[team_id].snakes[agent_id].isAlive():
        #         successorState = state.generateSuccessor(agent_id, team_id, action)
        #     else:
        #         successorState = state.deepCopy()

        #     if agent_id == len(state.teams[team_id].snakes) - 1:
        #         next_agent = self.id
        #         next_team = self.team_id
        #     else:
        #         next_agent = agent_id + 1
        #         next_team = team_id

        #     # Get value of successor state
        #     nextValue = value(successorState, next_agent, next_team, depth - 1)
        #     # If less than v, assign to v
        #     if nextValue < v:
        #       v = nextValue
        #       bestAction = action
        #   # Return v and the associated action
        #   return v, bestAction

        # print self.depth
        # Run algorithm starting with max agent



# class AlphaBetaAgent(MultiAgentSearchAgent):
#     """
#       Your minimax agent with alpha-beta pruning (question 3)
#     """

#     def getAction(self, gameState):
#         """
#           Returns the minimax action using self.depth and self.evaluationFunction
#         """
#         "*** YOUR CODE HERE ***"
#         def maxValue(state, depth, a, b, agentIndex):
#           v = -sys.maxint - 1
#           # Loop through all possible legal actions
#           for index, action in enumerate(state.getLegalActions(agentIndex)):
#             successorState = state.generateSuccessor(agentIndex, action)
#             # Get value of successor state
#             newValue = alphabeta(successorState, depth - 1, a, b, 1)
#             # If greater than v, assign to v
#             if newValue > v:
#               v = newValue
#               bestAction = action
#             a = max(a, v)
#             # If alpha greater than beta, break out of loop
#             if b < a:
#               break
#           # Return v and the associated action
#           return v, bestAction

#         def minValue(state, depth, a, b, agentIndex):
#           # Check if next agent is max or min
#           nextAgent = agentIndex + 1
#           if nextAgent == state.getNumAgents():
#             nextAgent = 0
#           v = sys.maxint
#           # Loop through all possible legal actions
#           for index, action in enumerate(state.getLegalActions(agentIndex)):
#             successorState = state.generateSuccessor(agentIndex, action)
#             # Get value of successor state
#             newValue = alphabeta(successorState, depth, a, b, nextAgent)
#             # If less than v, assign to v
#             if newValue < v:
#               v = newValue
#               bestAction = action
#             b = min(b, v)
#             # If alpha greater than beta, break out of loop
#             if b < a:
#               break
#           # Return v and the associated action
#           return v, bestAction

#         def alphabeta(state, depth, a, b, agentIndex):
#           # If at a terminal state or if max-depth has been reached, return
#           # evaluation function
#           if state.isWin() or state.isLose() or (depth == 0 and agentIndex == 0):
#             return self.evaluationFunction(state)

#           # Otherwise, check whether next agent is min or max
#           else:
#             if agentIndex == 0:
#               v, action = maxValue(state, depth, a, b, agentIndex)
#               return v
#             else:
#               v, action = minValue(state, depth, a, b, agentIndex)
#               return v

#         # Run algorithm starting with max agent
#         value, action = maxValue(gameState, self.depth, -sys.maxint - 1, sys.maxint, 0)
#         return action
                  

# class ExpectimaxAgent(MultiAgentSearchAgent):
#     """
#       Your expectimax agent (question 4)
#     """

#     def getAction(self, gameState):
#         """
#           Returns the expectimax action using self.depth and self.evaluationFunction

#           All ghosts should be modeled as choosing uniformly at random from their
#           legal moves.
#         """
#         "*** YOUR CODE HERE ***"
#         def expectimax(state, depth, agentIndex):
#           if state.isWin() or state.isLose() or (agentIndex == 0 and depth == 0):
#             return self.evaluationFunction(state)
#           else:
#             if agentIndex == 0:
#               v, action = maxValue(state, depth, agentIndex)
#               return v
#             else:
#               v = expValue(state, depth, agentIndex)
#               return v

#         def maxValue(state, depth, agentIndex):
#           v = -sys.maxint - 1
#           # Loop through all possible legal actions
#           for index, action in enumerate(state.getLegalActions(agentIndex)):
#             successorState = state.generateSuccessor(agentIndex, action)
#             # Get value of successor state
#             newValue = expectimax(successorState, depth - 1, agentIndex + 1)
#             # If greater than v, assign to v
#             if newValue > v:
#               v = newValue
#               bestAction = action
#           # Return v and the associated action
#           return v, bestAction

#         def expValue(state, depth, agentIndex):
#           # Check if next agent is max or min
#           nextAgent = agentIndex + 1
#           if nextAgent == state.getNumAgents():
#             nextAgent = 0
#           v = 0
#           actions = state.getLegalActions(agentIndex)
#           # Probability is uniform across all actions
#           p = 1.0 / len(actions)
#           # Loop through all possible legal actions
#           for index, action in enumerate(actions):
#             successorState = state.generateSuccessor(agentIndex, action)
#             v += p * expectimax(successorState, depth, nextAgent)
#           return v

#         # Run algorithm starting with max agent
#         value, action = maxValue(gameState, self.depth, 0)
#         return action

# def betterEvaluationFunction(currentGameState):
#     """
#       Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
#       evaluation function (question 5).

#       DESCRIPTION: <write something here so we know what you did>
#     """
#     "*** YOUR CODE HERE ***"
#     util.raiseNotDefined()

# # Abbreviation
# better = betterEvaluationFunction

