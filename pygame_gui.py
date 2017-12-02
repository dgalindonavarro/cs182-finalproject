import sys, pygame, util, random, argparse
from GameState import GameState
from Snake import Snake
from time import sleep

# misc. functions (not sure where these make most sense to eventually place)

# more miscellaneous functions to be put in the right place later
# these are to test snake collisions

# How to Call pygame_gui.py: (for now. this is a stupid way)
# >>> python pygame_gui.py [# of teams] [snakes per team] [game speed in seconds] ... to be determined[]

class Game():

    # Initialize the game screen
    def __init__(self, width, height, teams=2, snakes=1, speed=0.5, pixel_size=10):
        pygame.init()

        # Setup dimensions of game
        self.pixel_size = pixel_size
        self.width = width * self.pixel_size
        self.height = height * self.pixel_size

        # Hard coded color scheme for now
        team_colors = [(0, 255, 0), (66,238,244), (189, 77, 219)]

        # initialize Game State for first time
        self.state = GameState(int(teams), team_colors, width, height)
        self.game_over = False

        self.loadImages()

        # create some random snakes
        for team in xrange(int(teams)):
            for snake in xrange(int(snakes)):
                self.state.addRandoSnake(width, height, 5, team)
            
        # Create the screen with black background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        # Update screen
        pygame.display.flip()

        # Run Game
        self.run(float(speed))

    def loadImages(self):
        self.apple = pygame.image.load("images/apple.png")
        self.apple = pygame.transform.scale(self.apple, (self.pixel_size, self.pixel_size))
        self.eyes = pygame.image.load("images/eyes2.png")
        self.eyes = pygame.transform.scale(self.eyes, (self.pixel_size, self.pixel_size))

    # Draw a specific "pixel" on the screen
    def drawPixel(self, xcor, ycor, color):
        self.screen.fill(color, (xcor * self.pixel_size, ycor * self.pixel_size, self.pixel_size, self.pixel_size))
        return

    # Draw an apple on the screen
    def drawApple(self, xcor, ycor):
        self.screen.blit(self.apple, (xcor * self.pixel_size, ycor * self.pixel_size, self.pixel_size, self.pixel_size))

    # Draw eyes on snake at correct pixel with correct orientation
    def drawEyes(self, x, y, direction):
        eyes = pygame.transform.rotate(self.eyes, self.directionToAngle(direction))
        self.screen.blit(eyes, (x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))

    # Return the angle that the eyes need to be rotated by based on direction
    def directionToAngle(self, direction):
        if direction == "north":
            return 180
        elif direction == "east":
            return 90
        elif direction == "west":
            return 270
        else:
            return 0

    # Update score
    def updateScore(self):
        for i in xrange(len(self.state.teams)):
            white = (255, 255, 255)
            message = "Team " + str(i + 1) + ": " + str(self.state.teams[i].getScore())
            font = pygame.font.Font(None, 20)
            text = font.render(message, 1, white)
            self.screen.blit(text, ((i * 80) + 10,0))

    # Update the game screen based on the current game state
    def updateDisplay(self):
        state = self.state

        # Redraw the black background
        self.screen.fill((0, 0, 0))

        # Iterate through every snake and draw all pixels and eyes
        for team in state.teams:
            for snake in team.snakes:
                for x, y in snake.position:
                    if ((x,y) == snake.head):
                        head_color = (team.color[0] / 2, team.color[1] / 2, team.color[2] / 2)
                        self.drawPixel(x, y, head_color) 
                        self.drawEyes(x, y, snake.direction)
                    else: 
                        self.drawPixel(x, y, team.color)

        # Iterate through food and draw all apples
        for x, y in state.food:
            self.drawApple(x, y)

        # Update score
        self.updateScore()
        
        # Update screen
        pygame.display.flip()

    def gameOver(self):
        # check if one team has no snakes
        # if one has no snakes, update game over parameter of Game
        for team in self.state.teams:
            teamalive = False
            for snake in team.snakes:
                teamalive = snake.isAlive() or teamalive
            if not teamalive:
                self.game_over = True

        return

    # return the a tuple of string, score, of the team with the highest score. If a tie, return tie.
    def getWinner(self):
        maxScore = 0
        winner = None

        for team in self.state.teams:
            score = team.getScore()
            if score > maxScore:
                maxScore = score
                winner = str(team.id)
            elif score == maxScore:
                winner = "Tie"

        return winner, maxScore        

    def run( self, speed ):
        """
        Main control loop for game play. 
        (probably will be a while game.state = not_done loop or something)
        """

        # number of timesteps to take
        
        while not self.game_over:
            #frances' gui saver
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            # Update the game screen
            self.updateDisplay()

            # Iterate through each snake and tell it to move
            for team in self.state.teams:
                for snake in team.snakes:
                    if snake.isAlive():
                        snake.addTail()
                        snake.move(random.choice(snake.getActions()))
                        # snake.move("forward")

            # Update the game state based on snake movements (check collisions)
            self.state.update()
            # check if one team has been eliminated
            self.gameOver()

            # Update each teams' score
            for team in self.state.teams:
                #print team.getScore()
                pass
            # delay between timesteps
            sleep(speed)

        # Game is Over. Display game over graphic that makes the player sad

        print "Game Over! Sad!"
        print ""
        winner = self.getWinner()
        print("Winner: Team " + winner[0])
        print("Score: " + str(winner[1])) 
        return

if len(sys.argv) == 1:
    game = Game(30, 30)
elif len(sys.argv) == 2:
    print sys.argv[1]
    game = Game(30, 30, sys.argv[1])
elif len(sys.argv) == 3:
    game = Game(30, 30, sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    game = Game(30, 30, sys.argv[1], sys.argv[2], sys.argv[3])


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