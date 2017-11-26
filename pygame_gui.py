import sys, pygame
from time import sleep

# Placeholders so we can test class
snakes = [
    [(1, 1), (1, 2), (1, 3), (1, 4), (1,5)],
    [(10, 40), (11, 40), (12, 40), (13, 40), (14,40)],
]
food = [(5, 3), (49, 51), (53, 24)]

class Game():

    # Initialize the game screen
    def __init__(self, width, height, pixel_size=10):
        pygame.init()

        # Setup dimensions of game
        self.pixel_size = pixel_size
        self.width = width * self.pixel_size
        self.height = height * self.pixel_size

        # Create the screen with black background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        # Placeholder to iterate through snake coordinates and fill pixels with white
        for snake in snakes:
            for x, y in snake:
                self.drawPixel(x, y, (0, 255, 0))

        for x, y in food:
            self.drawPixel(x, y, (255, 0, 0))

        # Update screen
        pygame.display.flip()

        # Sleep for 5 seconds so we can see game screen
        sleep(5)

        return

    # Draw a specific "pixel" on the screen
    def drawPixel(self, xcor, ycor, color):
        self.screen.fill(color, (xcor * self.pixel_size, ycor * self.pixel_size, self.pixel_size, self.pixel_size))
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