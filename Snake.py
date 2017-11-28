class Snake():
    def __init__(self, id, team_id):
        self.id
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