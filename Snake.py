import pygame, random

class Snake():

    def __init__(self, id, team_id, color):
        self.id = id
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None
        self.team_id = team_id
        self.add_tail = False
        self.eaten = []
        self.color = color

    def __eq__( self, other ):
        if other == None:
            return False
        if not self.id == other.id: return False
        if not self.team_id == other.team_id: return False
        if not self.direction == other.direction: return False
        if not self.add_tail == other.add_tail: return False
        if not len(self.position) == len(other.position): return False
        for cell in xrange(len(self.position)):
            if not self.position[cell] == other.position[cell]: return False
        if not len(self.eaten) == len(other.eaten): return False
        for food in xrange(len(self.eaten)):
            if not self.eaten[food] == other.eaten[food]: return False
        return True

    def __hash__(self):
        return int((hash(tuple(self.position)) + 13*hash(self.id) + 113* hash(tuple(self.eaten)) + 7 * hash(self.direction)) % 1048575 )

    def deepCopy(self):
        snake = Snake(self.id, self.team_id, self.color)
        snake.position = self.position[:]
        snake.head = self.head
        snake.length = self.length
        snake.direction = self.direction
        snake.add_tail = self.add_tail
        snake.eaten = self.eaten[:]
        return snake

    # Add new coordinate as the new head of snake
    def push(self, new):
        self.position.insert(0, new)
        self.head = new
        
    # Pop the tail of the snake
    def pop(self):
        self.position.pop()

    # Get the neighboring coordinate of the snake's head based on direction
    def getNewHeadPos(self, direction):
        if not self.isAlive(): return "dead"

        if direction == "north":
            pos = (self.head[0], self.head[1] - 1)
        elif direction == "east":
            pos = (self.head[0] + 1, self.head[1])
        elif direction == "south":
            pos = (self.head[0], self.head[1] + 1)
        else:
            pos = (self.head[0] - 1, self.head[1])

        return pos

    # Return list of directions
    def getDirections(self):
        directions = ["north", "east", "south", "west"]
        return directions

    # Return list of actions
    def getActions(self):
        if self.isAlive():
            actions = ["forward", "left", "right"]
            return actions
        else:
            return []

    # return a random action
    def getAction(self, state):

        action = random.choice(self.getActions())

        return action

    # Move the snake based on its current direction and given action
    def move(self, action):
        # Update snake's direction based on the action
        if not self.isAlive(): return "dead"

        directions = self.getDirections()
        if action == "left" and self.direction != "north":
            self.direction = directions[directions.index(self.direction) - 1]
        elif action == "left":
            self.direction = "west"
        elif action == "right" and self.direction != "west":
            self.direction = directions[directions.index(self.direction) + 1]
        elif action == "right":
            self.direction = "north"

        # Push new head onto snake in the correct direction
        self.push(self.getNewHeadPos(self.direction))

        # If it's not time to add to tail, pop tail
        if not self.add_tail:
            self.pop()
        # Otherwise, add the correct eaten apple to tail and update "eaten" list
        else:
            self.eaten.pop(0)
            self.length += 1
            self.add_tail = False

        # If tail is on an eaten apple, add to tail next timestep
        if len(self.eaten) > 0 and self.position[-1] == self.eaten[0]:
            self.add_tail = True

    def undoMove(self, direction, position, eaten, add_tail):
        self.direction = direction
        self.position = position
        self.head = self.position[0]
        self.length = len(self.position)
        self.add_tail = add_tail
        self.eaten = eaten

    # Update the snake based on index to cut off
    def updateSnake(self, index):
        if index == -1:
            self.die()
        else:
            self.position = self.position[:index]
            self.length = len(self.position)
            while len(self.eaten) > 0:
                if self.eaten[0] not in self.position:
                    self.eaten.pop(0)
                    self.add_tail = False
                else:
                    break
            if len(self.eaten) > 0 and self.position[-1] == self.eaten[0]:
                self.add_tail = True

    # Empty the snake's position and reset all values
    def die(self):
        # self.final_score = len(self.position) + len(self.eaten)
        self.position = []
        self.head = None
        self.direction = None

    # Return whether or not the snake is alive
    def isAlive(self):
        return self.head != None

    # Add apple to "eaten" list
    def eat(self, food):
        self.eaten.append(food)
        if len(self.position) == 1:
            self.add_tail = True

class UserAgent(Snake):

    def getAction(self, gameState):
        actions = self.getActions()
        pressed = pygame.key.get_pressed()
        direction = self.direction

        if pressed[pygame.K_UP] and direction != "south":
            if direction == "north":
                action = actions[0]
            elif direction == "west":
                action = actions[2]
            elif direction == "east":
                action = actions[1]
        elif pressed[pygame.K_DOWN] and direction != "north":
            if direction == "south":
                action = actions[0]
            elif direction == "east":
                action = actions[2]
            elif direction == "west":
                action = actions[1]
        elif pressed[pygame.K_LEFT] and direction != "east":
            if direction == "west":
                action = actions[0]
            elif direction == "south":
                action = actions[2]
            elif direction == "north":
                action = actions[1]
        elif pressed[pygame.K_RIGHT] and direction != "west":
            if direction == "east":
                action = actions[0]
            elif direction == "north":
                action = actions[2]
            elif direction == "south":
                action = actions[1]

        # if no arrow keystroke detected
        else:
            action = actions[0]
        return action
    