import pygame, random

class Snake():
    def __init__(self, id, team_id, color):
        self.id = id
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None
        self.team = team_id
        self.new_tail = None
        self.color = color
        self.user = False

    # Add new coordinate as the new head of snake
    def push(self, new):
        self.position.insert(0, new)
        self.head = new
        
    # Pop the tail of the snake
    def pop(self):
        self.position.pop()

    # Get the neighboring coordinate of the snake's head based on direction
    def getNewHeadPos(self, direction):
        if direction == "north":
            pos = (self.head[0], self.head[1] - 1)
        elif direction == "east":
            pos = (self.head[0] + 1, self.head[1])
        elif direction =="south":
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
        actions = ["forward", "left", "right"]

        return actions

    # Return Action to take. If User controlled snake, look at current keypress.
    # If not, return a random action
    def getAction(self):
        if(self.user):
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

        # if snake is not a user snake, return a random action
        else:
            action = random.choice(self.getActions())

        return action

    # Move the snake based on its current direction and given action
    def move(self, action):

        # Pop off the last coordinate in the tail since we are moving
        ### Later we will have to check if we have eaten food ###
        self.pop()

        # Update snake's direction based on the action
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

    # Update the snake based on index to cut off
    def updateSnake(self, index):
        if index == -1:
            self.die()
        else:
            self.position = self.position[:index + 1]
            self.length = len(self.position)

    # Empty the snake's position and reset all values
    def die(self):
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None

    # Return whether or not the snake is alive
    def isAlive(self):
        return self.length != 0

    # adds to the tail of a snake when it passes over food
    def eat(self):
        tail = self.position[-1]
        new_tail = (0, 0)

        # corner case for only head existing, uses direction to get new tail location
        if self.length == 1:
            direction = self.direction
            if direction == "north":
                new_tail = (tail[0], tail[1] + 1)
            elif direction == "south":
                new_tail = (tail[0], tail[1] - 1)
            elif direction == "east":
                new_tail = (tail[0] - 1, tail[1])
            elif direction == "west":
                new_tail = (tail[0] + 1, tail[1])
        else:
            # Extend the vector from the tail to the second to last part of the snake, to the new tail
            second_toLastTail = self.position[-2]
            new_tail = (tail[0] - (second_toLastTail[0] - tail[0]), tail[1] - (second_toLastTail[1] - tail[1]))

        self.new_tail = new_tail

    def addTail(self):
        if self.new_tail != None:
            self.position.append(self.new_tail)
            self.length += 1
            self.new_tail = None
















