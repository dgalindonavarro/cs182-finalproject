import sys, pygame, util, random
from GameState import GameState
from Snake import Snake
from time import sleep

# misc. functions (not sure where these make most sense to eventually place)

# more miscellaneous functions to be put in the right place later
# these are to test snake collisions


class Game():

    # Initialize the game screen
    def __init__(self, width, height, pixel_size=10):
        pygame.init()

        # Setup dimensions of game
        self.pixel_size = pixel_size
        self.width = width * self.pixel_size
        self.height = height * self.pixel_size

        team_colors = [(0, 255, 0), (66,238,244)]

        # initialize Game State for first time
        self.state = GameState(2, team_colors)

        # print "original state: "
        # for snake in self.state.snakes:
        #     print snake.position
        # for snake in self.state.snakes2:
        #     print snake.position

        # create some random snakes
        self.state.addRandoSnake(width, height, 10, 0)
        self.state.addRandoSnake(width, height, 5, 0)
        self.state.addRandoSnake(width, height, 8, 1)
        
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
        # print state.snakes[0].position

        for team in state.teams:
            for snake in team.snakes:
                for x, y in snake.position:
                    if ((x,y) == snake.head):
                        tail_color = (team.color[0] / 2, team.color[1] / 2, team.color[2] / 2)
                        self.drawPixel(x, y, tail_color)   
                    else: 
                        self.drawPixel(x, y, team.color)

        for x, y in state.food:
            self.drawPixel(x, y, (255, 0, 0))

        # Update screen
        pygame.display.flip()

    def run( self ):
        """
        Main control loop for game play. 
        (probably will be a while game.state = not_done loop or something)
        """

        # number of timesteps to take
        for i in xrange(3000):
            #frances' gui saver
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            self.updateDisplay()
            for team in self.state.teams:
                for snake in team.snakes:
                    snake.move(random.choice(snake.getActions()))

            self.state.update()
            
            # uncomment for collisions per timestep:

            # delay between timesteps
            sleep(0.1)

        # Sleep for 5 seconds so we can see game screen
        #sleep(100.0/100.0)

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