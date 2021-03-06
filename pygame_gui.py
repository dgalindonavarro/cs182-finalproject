import sys, pygame, util, random, argparse, cProfile, copy
from GameState import GameState
from Snake import Snake
from time import sleep

# misc. functions (not sure where these make most sense to eventually place)

# more miscellaneous functions to be put in the right place later
# these are to test snake collisions

# How to Call pygame_gui.py: (for now. this is a stupid way)
# >>> python pygame_gui.py [# of teams] [snakes per team] [game speed in seconds] [isUserControlled bool]... to be determined[]
#
# example: 2 teams, 2 snakes per team, user controls one snake
# >>> python pygame_gui.py 2 2 0.1 True
class Game():

    # Initialize the game screen
    def __init__(self, width, height, teams=2, snakes=1, speed=0.0, user=False, agent="A", functionId=1, no_graphics=False, csv=False, qLearning=False, episodes=100, pixel_size=10):

        # Store attributes from command line
        self.csv = csv == "True"
        self.qLearning = qLearning == "True"
        self.episodes = int(episodes)
        self.no_graphics = no_graphics == "True"
        self.agent = agent
        self.functionId = int(functionId)

        # Setup dimensions of game
        self.pixel_size = pixel_size
        self.width = width * self.pixel_size
        self.height = height * self.pixel_size

        # Hard coded color scheme for now (team1, team2, team3, USER)
        team_colors = [(0, 255, 0), (66,238,244), (189, 77, 219), (11, 102, 35)]

        # initialize Game State for first time
        self.state = GameState(int(teams), team_colors, width, height)
        self.game_over = False

        # create snakes and initialize them to be the right type of agent
        for team in xrange(int(teams)):
            for snake in xrange(int(snakes)):
                if snake == 0 and team == 0 and user == "True":
                    agent_type = "U"
                elif self.qLearning:
                    if snake == 0 and team == 0:
                        agent_type = "Q"
                    else:
                        # type of adversaries to train/employ Q learning against
                        agent_type = "R"
                # If not qlearning then team 0 snakes are of type agent from command line
                elif team == 0:
                    agent_type = agent
                # Team 1 snakes are reflex (greedy) agents
                else:
                    agent_type = "R"

                # Add snake to correct team with correct agent type
                self.state.addRandoSnake(width, height, 5, team, agent_type)

        # If no_graphics is false, initialize game screen
        if not self.no_graphics:
            pygame.init()

            # Load static images once
            self.loadImages()

            # Create the screen with black background
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.screen.fill((0, 0, 0))

            # Update screen
            pygame.display.flip()

        # Run Game
        self.run(float(speed))

    # Load images used in game play
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
                        head_color = (snake.color[0] / 2, snake.color[1] / 2, snake.color[2] / 2)
                        self.drawPixel(x, y, head_color) 
                        self.drawEyes(x, y, snake.direction)
                    else: 
                        self.drawPixel(x, y, snake.color)
                        if (x,y) in snake.eaten:
                            self.drawApple(x, y)

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
        self.game_over = True
        for team in self.state.teams:
            teamalive = False
            for snake in team.snakes:
                teamalive = snake.isAlive() or teamalive
            self.game_over = self.game_over and not teamalive

        return

    # return the a tuple of string, score, of the team with the highest score. If a tie, return tie.
    def getWinner(self):
        maxScore = 0
        otherScore = []
        winner = None

        for team in self.state.teams:
            score = team.getScore()
            otherScore.append(score)
            if score > maxScore:
                maxScore = score
                winner = str(team.id)
            elif score == maxScore:
                winner = "Tie"

        otherScore.remove(maxScore)

        # Write to correct csv file (THIS CODE IS FOR 2v2 DATA)
        if self.csv:
            fd = open('data/' + self.agent + '_Data_Eval' + str(self.functionId) + '.csv','a')
            newLine = "\n" + str(len(self.state.teams)) + "," + str(len(self.state.teams[0].snakes)) + "," + winner  + "," + str(maxScore) + "," + str(otherScore[0])
            fd.write(newLine)
            fd.close()

        return winner, maxScore        

    def run( self, speed ):
        """
        Main control loop for game play. 
        """

        if self.qLearning:
            # games including training phase and deployment phase
            games_run = 0

            # qsnek is an easy way to reference the special snake being trained snake 0 on team 0
            qSnek = self.state.teams[0].snakes[0]
            print 'Qsnek is beginning up to %d episodes of Training' % (qSnek.numTraining)

            # Run correct number of episodes
            while games_run < self.episodes:
                print "Game Number", games_run
                qSnek.startEpisode()

                # Run until game is over
                while not self.game_over:

                    if not self.no_graphics:
                        # gui saver
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                raise SystemExit

                        # Update the game screen
                        self.updateDisplay()

                    # Iterate through each snake and tell it to move
                    
                    actions = {}
                    for team in self.state.teams:
                        for snake in team.snakes:
                            # If the snake is a qlearning snake, deepcopy the state
                            if snake.isAlive() and team.id == 0 and snake.id == 0:
                                actions[(team.id, snake.id)] = snake.getAction(self.state.deepCopy(), self.functionId)
                            elif snake.isAlive():
                                actions[(team.id, snake.id)] = snake.getAction(self.state, self.functionId)
                    
                    for team in self.state.teams:
                        for snake in team.snakes:
                            if snake.isAlive():
                                snake.move(actions[(team.id, snake.id)])
                           

                    # Update the game state based on snake movements (check collisions)
                    self.state.update()
                    

                    # update Q values for snek
                    qSnek.observationFunction(self.state)
                    
                    # check if one team has been eliminated
                    self.gameOver()

                    # stop training if Q snake dies
                    if not qSnek.isAlive():
                       self.game_over = True  

                    # delay between timesteps
                    sleep(speed)

                qSnek.stopEpisode()
                winner = self.getWinner() 
                games_run += 1

                # RESET GAME STATE AS IT WAS INITIALLY, place the snakes on the board randomly to begin again
                self.state.resetSnakes(5, self.width, self.height)
                self.state.food = []
                self.game_over = False
                self.state.addRandoFood()

            print "printing q snake values"
            print qSnek.qValues
            return

        # Just run the game one time with non-q learning training and implementation
        else: 
            while not self.game_over:
                if not self.no_graphics:
                    # gui saver
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            raise SystemExit

                    # Update the game screen
                    self.updateDisplay()

                
                currentState = self.state.deepCopy()
                
                # Iterate through each snake and tell it to move
                for team in self.state.teams:
                    for snake in team.snakes:
                        if snake.isAlive():
                            snake.move(snake.getAction(currentState, self.functionId))

                # Update the game state based on snake movements (check collisions)
                self.state.update()
                # check if one team has been eliminated
                self.gameOver()

                # delay between timesteps
                sleep(speed)

            # Game is Over. Display game over graphic that makes the player sad
            print "Game Over! Sad!"
            print ""
            winner = self.getWinner()
            print("Winner: Team " + winner[0])
            print("Score: " + str(winner[1])) 
            return

# Game initializer and Argument Option Parser
game = Game(30, 30, *sys.argv[1:])
