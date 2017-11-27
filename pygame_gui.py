import sys, pygame, util, random
from time import sleep

# misc. functions (not sure where these make most sense to eventually place)

# Add a snake in a random place to begin which does not conflict with current environment objects, to the Game State.
# Returns a new Game State

def addRandoSnake(width, height, length, state, team = 1):
    new_state = state.deepCopy()
    snek = Snake()
    head = None

    # Get list of positions that are next to or on top of any other snakes as to avoid placing new head there
    taken_positions = []
    list_of_snakes = state.snakes + state.snakes2

    for snake in list_of_snakes:
        for cor in snake.position:
            taken_positions.append(cor)
            if cor:
                taken_positions.append( (cor[0]+1, cor[1]+1)  )
                taken_positions.append( (cor[0], cor[1]+1)  )
                taken_positions.append( (cor[0]-1, cor[1]+1)  )
                taken_positions.append( (cor[0]-1, cor[1])  )
                taken_positions.append( (cor[0]-1, cor[1]-1)  )
                taken_positions.append( (cor[0], cor[1]-1)  )
                taken_positions.append( (cor[0]+1, cor[1]-1)  )
                taken_positions.append( (cor[0]+1, cor[1])  )

    # Sample head until it is not in a taken position
    head = (int(random.uniform(length, width - length)) , int(random.uniform(length, height - length)))

    while(head in taken_positions):
        head = (int(random.uniform(length, width - length)) , int(random.uniform(length, height - length)))

    # Add head to snek
    snek.push(head)

    # Get a random direction for the snek to face
    facing = random.choice(getDirections())

    # Add rest of snek depending on direction it is facing
    cur = head
    if facing == "south":
        for i in range(length - 1):
            cur = (cur[0], cur[1]-1)
            snek.position.append(cur)
    if facing == "east":
        for i in range(length - 1):
            cur = (cur[0]-1, cur[1])
            snek.position.append(cur) 
    if facing == "north":
        for i in range(length - 1):
            cur = (cur[0], cur[1]+1)
            snek.position.append(cur)   
    if facing == "west":
        for i in range(length - 1):
            cur = (cur[0]+1, cur[1])
            snek.position.append(cur)

    # Update properties of snek
    snek.direction = facing
    snek.length = length

    # Append snek to correct team
    if(team == 2):
        new_state.snakes2.append(snek)
    else:
        new_state.snakes.append(snek)

    return new_state

def getDirections():
    directions = ["north", "east", "south", "west"]

    return directions

class Snake():
    def __init__(self):
        self.position = []
        self.head = None
        self.length = 0
        self.direction = None

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

    def getActions(self):
        actions = ["forward", "left", "right"]

        return actions

    def move(self, action):

        # Pop off the last coordinate in the tail since we are moving
        ### Later we will have to check if we have eaten food ###
        self.pop()

        # Update snake's direction based on the action
        directions = getDirections()
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


class GameState():
    def __init__( self, prevState = None ):

        #if prevState != None:
        #    # copy over everything from previous state
        #    pass 

        # Placeholders so we can test class
        self.snakes = []
        self.snakes2 = []
        self.food = [(5, 3), (49, 51), (53, 24)]

    # for duplicating the state (in case dicts become part of a State object)
    def deepCopy( self ):
        state = GameState( self )
        state.food = self.food
        state.snakes = self.snakes
        state.snakes2 = self.snakes2
        return state


class Game():

    # Initialize the game screen
    def __init__(self, width, height, pixel_size=10):
        pygame.init()

        # Setup dimensions of game
        self.pixel_size = pixel_size
        self.width = width * self.pixel_size
        self.height = height * self.pixel_size

        # initialize Game State for first time
        self.state = GameState()

        print "original state: "
        for snake in self.state.snakes:
            print snake.position
        for snake in self.state.snakes2:
            print snake.position

        # create some random snakes
        new_state = addRandoSnake(width, height, 10, self.state, 1)
        new_state = addRandoSnake(width, height, 5, new_state, 1)
        self.state = addRandoSnake(width, height, 8, new_state, 2)
        
        # Create the screen with black background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        # Update screen
        pygame.display.flip()

        # Run Game
        self.run()

    # Draw a specific "pixel" on the screen
    def drawPixel(self, xcor, ycor, color):
        self.screen.fill(color, (xcor * self.pixel_size, ycor * self.pixel_size, self.pixel_size, self.pixel_size))
        return

    def updateDisplay(self):
        state = self.state

        self.screen.fill((0, 0, 0))

        # Placeholder to iterate through snake coordinates and fill pixels with white
        print state.snakes[0].position
        for snake in state.snakes:
            for x, y in snake.position:
                if ((x,y) == snake.head):
                    self.drawPixel(x, y, (150, 150, 0))   
                else: 
                    self.drawPixel(x, y, (0, 255, 0))

        for snake in state.snakes2:
            for x, y in snake.position:
                if ((x,y) == snake.head):
                    self.drawPixel(x, y, (150, 60, 150))
                else:
                    self.drawPixel(x, y, (0, 60, 255))

        for x, y in state.food:
            self.drawPixel(x, y, (255, 0, 0))

        # Update screen
        pygame.display.flip()

    def run( self ):
        """
        Main control loop for game play. 
        (probably will be a while game.state = not_done loop or something)
        """
        for i in xrange(10):
            self.updateDisplay()
            sleep(1)
            for snake in self.state.snakes + self.state.snakes2:
                snake.move(random.choice(snake.getActions()))
        # Sleep for 5 seconds so we can see game screen
        sleep(1)

        return

game = Game(50, 50)

### CODE THAT CAME WITH PYGAME TUTORIAL FOR REFERENCE ###

# size = width, height = 800, 600
# speed = [10, 10]
# black = 0, 0, 0

# screen = pygame.display.set_mode(size)

# ball = pygame.image.load("static/ball.png")
# ballrect = ball.get_rect()

# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()

#     ballrect = ballrect.move(speed)
#     if ballrect.left < 0 or ballrect.right > width:
#         speed[0] = -speed[0]
#     if ballrect.top < 0 or ballrect.bottom > height:
#         speed[1] = -speed[1]

#     screen.fill(black)
#     screen.blit(ball, ballrect)
#     pygame.display.flip()