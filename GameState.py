import random
from Snake import Snake
from Team import Team

class GameState():
    def __init__( self, num_teams, team_colors, width, height, obstacles=[]):

        #if prevState != None:
        #    # copy over everything from previous state
        #    pass 

        # Placeholders so we can test class
        # self.snakes = []
        # self.snakes2 = []
        self.teams = []
        for i in xrange(num_teams):
            self.teams.append(Team(i, team_colors[i]))
        self.food = []

        self.legalPositions = []
        for i in xrange(width):
            for j in xrange(height):
                if (i, j) not in obstacles:
                    self.legalPositions.append((i, j))

    # for duplicating the state (in case dicts become part of a State object)
    def deepCopy( self ):
        state = GameState( self )
        state.food = self.food
        # state.snakes = self.snakes
        # state.snakes2 = self.snakes2
        state.teams = self.teams
        return state

    # Set snake position list to empty
    def updateSnake(self, team_id, snake_id, index):
        ### Maybe add an is Dead check to other functions later? ###
        self.teams[team_id].updateSnake(snake_id, index)

    # Update and check collisions
    def update(self):
        collisions = self.collisionsOnBoard()
        for collision in collisions:
            self.updateSnake(*collision)
        self.snakesEating()
        self.addRandoFood()

    def addRandoFood(self):
        possible = [x for x in self.legalPositions if x not in self.food]
        for team in self.teams:
            for snake in team.snakes:
                possible = [x for x in possible if x not in snake.position]            
        food = random.choice(possible)
        self.food.append(food)
                

    # Add a snake in a random place to begin which does not conflict with current environment objects, to the Game State.
    # Returns a new Game State

    def addRandoSnake(self, width, height, length, team_id):
        # Get index of snake
        snek_id = len(self.teams[team_id].snakes)
        snek = Snake(snek_id, team_id)
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

    # returns a list of snakes to remove, and from what position to delete it, or None if no collision
    # we should have snake IDs
    # the second item in the tuple is from what index to delete the snake, -1 means the whole thing
    def snakeCollision(self, snake1_id, team1_id, snake2_id, team2_id):

        ### ADD COLLISION CHECKING WITH SELF ###

        snake1 = self.teams[team1_id].snakes[snake1_id]
        snake2 = self.teams[team2_id].snakes[snake2_id]        

        if team1_id == team2_id:
            if snake1_id == snake2_id:
                if snake1.head in snake1.position[1:]:
                    return [(team1_id, snake1_id, -1)]
                else:
                    return []
            else:
                if snake1.head == snake2.head:
                    return [(team1_id, snake1_id, 0), (team2_id, snake2_id, 0)]
                elif snake1.head in snake2.position:
                    return [(team2_id, snake2_id, snake2.position.index(snake1.head))]
                elif snake2.head in snake1.position:
                    return [(team1_id, snake1_id, snake1.position.index(snake2.head))]
                else:
                    return []
        else:
            if snake1.head == snake2.head:
                return [(team1_id, snake1_id, -1), (team2_id, snake2_id, -1)]
            elif snake1.head in snake2.position:
                return [(team1_id, snake1_id, -1)]
            elif snake2.head in snake1.position:
                return [(team2_id, snake2_id, -1)]
            else:
                return []

    def boardCollision(self, snake_id, team_id):
        snake = self.teams[team_id].snakes[snake_id]
        if snake.head not in self.legalPositions:
            return [(team_id, snake_id, -1)]
        else:
            return []

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

    def snakesEating(self):
        for i in xrange(len(self.teams)):
            for j in xrange(len(self.teams[i].snakes)):
                if self.teams[i].snakes[j].isAlive():
                    tail = self.teams[i].snakes[j].position[-1]
                    if tail in self.food:
                        self.teams[i].snakes[j].eat()
                        self.food.remove(tail)
