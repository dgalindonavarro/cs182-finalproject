import random, copy
from multiAgents import ReflexAgent
from Snake import Snake
from Team import Team

class GameState():
    def __init__( self, num_teams, team_colors, width, height, obstacles=[]):

        # Create specified number of teams and assign colors
        self.teams = []
        for i in xrange(num_teams):
            self.teams.append(Team(i, team_colors[i]))

        # Create list of food positions
        self.food = []

        # Add all positions on the board that are not part of obstacles to the
        # legal positions for snakes
        self.legalPositions = []
        for i in xrange(width):
            for j in xrange(height):
                if (i, j) not in obstacles:
                    self.legalPositions.append((i, j))

        self.addRandoFood()

        self.remove_food = None

    # for duplicating the state (in case dicts become part of a State object)
    def deepCopy( self ):
        state = copy.deepcopy(self)
        return state

    # Update snake position list based on index
    def updateSnake(self, team_id, snake_id, index):
        ### Maybe add an is Dead check to other functions later? ###
        self.teams[team_id].updateSnake(snake_id, index)

    # Update and check collisions
    def update(self):
        if self.remove_food != None:
            self.removeFood(self.remove_food)

        collisions = self.collisionsOnBoard()

        # Iterate through snakes with collisions and update each one
        for collision in collisions:
            self.updateSnake(*collision)

        # Check if snakes are eating food in this timestep
        self.snakesEating()

    # Add a food item anywhere on the board that isn't going to be taken
    def addRandoFood(self):
        possible = [x for x in self.legalPositions if x not in self.food]
        for team in self.teams:
            for snake in team.snakes:
                possible = [x for x in possible if x not in snake.position]            
        food = random.choice(possible)
        self.food.append(food)
                

    # Add a snake in a random place to begin which does not conflict with current environment objects, to the Game State.

    def addRandoSnake(self, width, height, length, team_id):
        # Get index of snake
        snek_id = len(self.teams[team_id].snakes)
        snek = ReflexAgent(snek_id, team_id)
        head = None

        # Get list of positions that are next to or on top of any other snakes as to avoid placing new head there
        taken_positions = []
        list_of_snakes = []
        for team in self.teams:
            list_of_snakes += team.snakes

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
        facing = random.choice(snek.getDirections())

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
        self.teams[team_id].snakes.append(snek)

    # returns a list of snakes to remove, and from what position to delete it
    # the third item in the tuple is from what index to delete the snake, -1 means the whole thing
    def snakeCollision(self, snake1_id, team1_id, snake2_id, team2_id):

        snake1 = self.teams[team1_id].snakes[snake1_id]
        snake2 = self.teams[team2_id].snakes[snake2_id]        

        # If on the same team
        if team1_id == team2_id:
            # If the same snake
            if snake1_id == snake2_id:
                # If snake has crashed into itself, snake should die
                if snake1.head in snake1.position[1:]:
                    return [(team1_id, snake1_id, -1)]
                # Otherwise, no collision
                else:
                    return []
            # If different snake on the same team
            else:
                # If head to head collision, both snakes retain only their heads
                if snake1.head == snake2.head:
                    return [(team1_id, snake1_id, 0), (team2_id, snake2_id, 0)]
                # If one snake has crashed into the other's tail, cut off tail
                elif snake1.head in snake2.position:
                    return [(team2_id, snake2_id, snake2.position.index(snake1.head))]
                elif snake2.head in snake1.position:
                    return [(team1_id, snake1_id, snake1.position.index(snake2.head))]
                # No collision
                else:
                    return []
        # If different teams
        else:
            # If head to head collision, both snakes die
            if snake1.head == snake2.head:
                return [(team1_id, snake1_id, -1), (team2_id, snake2_id, -1)]
            # Otherwise, snake that crashed into the other's tail will die
            elif snake1.head in snake2.position:
                return [(team1_id, snake1_id, -1)]
            elif snake2.head in snake1.position:
                return [(team2_id, snake2_id, -1)]
            # No collision
            else:
                return []

    # Check if snake has crashed into any walls or obstacles
    def boardCollision(self, snake_id, team_id):
        snake = self.teams[team_id].snakes[snake_id]

        # If snake has crashed into a wall, snake dies
        if snake.head not in self.legalPositions:
            return [(team_id, snake_id, -1)]
        else:
            return []

    # Iterate through all pairs of snakes to check if there were any collisions
    # Return list of snakes with collisions
    def collisionsOnBoard(self):
        collisions = []

        for i in xrange(len(self.teams)):
            for j in xrange(len(self.teams[i].snakes)):
                collisions += self.boardCollision(j, i)
                for k in xrange(i, len(self.teams)):
                    start_index = 0
                    if i == k:
                        start_index = j
                    for l in xrange(start_index, len(self.teams[k].snakes)):
                        collisions += self.snakeCollision(j, i, l, k)

        return collisions

    # Checks if snake tails are over food, has snakes eat the food and removes the food from the board
    def snakesEating(self):
        for i in xrange(len(self.teams)):
            for j in xrange(len(self.teams[i].snakes)):
                if self.teams[i].snakes[j].isAlive():
                    snake = self.teams[i].snakes[j]
                    if snake.head in self.food:
                        self.foodEaten(snake.head)
                        snake.eat(snake.head)

    # Adds a new food object and removes eaten food from board
    def foodEaten(self, food):
        self.addRandoFood()
        self.food.remove(food)

    # Returns a successor based on a single snake's action
    def generateSuccessor(self, snake_id, team_id, action):
        successor = self.deepCopy()
        successor.teams[team_id].snakes[snake_id].move(action)
        successor.update()
        return successor
