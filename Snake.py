class Snake():
    # def __init__(self, id, team_id):
    #     self.id = id
    #     self.position = []
    #     self.head = None
    #     self.length = 0
    #     self.direction = None
    #     self.team_id = team_id
    #     self.add_tail = False
    #     self.eaten = []

    def __init__(self, id, team_id, state):
        self.state = state
        self.id = id
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None
        self.team_id = team_id
        self.add_tail = False
        self.eaten = []

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
        if self.isAlive():
            actions = ["forward", "left", "right"]
            return actions
        else:
            return []

    # Move the snake based on its current direction and given action
    def move(self, action):
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

        # If it's not time to add to tail, pop tail
        if not self.add_tail:
            self.pop()
        # Otherwise, add the correct eaten apple to tail and update "eaten" list
        else:
            self.eaten.pop(0)
            self.length += 1
            self.add_tail = False

        # If tail is on an eaten apple, add to tail next timestep
        # print "List:", self.position
        # print self.position[-1]
        if len(self.eaten) > 0 and self.position[-1] == self.eaten[0]:
            self.add_tail = True

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
        self.direction = None

    # Return whether or not the snake is alive
    def isAlive(self):
        return self.head != None

    # Add apple to "eaten" list
    def eat(self, food):
        self.eaten.append(food)
        # print len(self.position)
        if len(self.position) == 1:
            self.add_tail = True

    