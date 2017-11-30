class Snake():
    def __init__(self, id, team_id):
        self.id = id
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None
        self.team = team_id

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

    def getDirections(self):
        directions = ["north", "east", "south", "west"]

        return directions

    def getActions(self):
        actions = ["forward", "left", "right"]

        return actions

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

    def updateSnake(self, index):
        if index == -1:
            self.die()
        else:
            self.position = self.position[:index + 1]
            self.length = len(self.position)

    def die(self):
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None

    def isAlive(self):
        return self.length != 0

    def eat(self):
        tail = self.position[-1]
        new_tail = (0, 0)
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
            second_toLastTail = self.position[-2]
            new_tail = (tail[0] - (second_toLastTail[0] - tail[0]), tail[1] - (second_toLastTail[1] - tail[1]))
        self.position.append(new_tail)
        self.length += 1
















