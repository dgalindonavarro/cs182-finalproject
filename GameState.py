import random
from Snake import Snake
from Team import Team

class GameState():
    def __init__( self, num_teams, team_colors):

        #if prevState != None:
        #    # copy over everything from previous state
        #    pass 

        # Placeholders so we can test class
        # self.snakes = []
        # self.snakes2 = []
        self.teams = []
        for i in xrange(num_teams):
            self.teams.append(Team(i, team_colors[i]))
        self.food = [(5, 3), (49, 51), (53, 24)]

    # for duplicating the state (in case dicts become part of a State object)
    def deepCopy( self ):
        state = GameState( self )
        state.food = self.food
        # state.snakes = self.snakes
        # state.snakes2 = self.snakes2
        state.teams = self.teams
        return state

    # Update and check collisions
    def update(self):


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
    def collision(snake1_id, team1_id, snake2_id, team2_id):

        ### ADD COLLISION CHECKING WITH SELF ###

        snake1 = self.teams[team1_id].snakes[snake1_id]
        snake2 = self.teams[team2_id].snakes[snake2_id]        

        if team1_id == team2_id:
            if snake1.head == snake2.head:
                return [(team1_id, snake1_id, 0), (team2_id, snake2_id, 0)]
            elif snake1.head in snake2.position:
                return [(team2_id, snake2_id, snake2.position.index(snake1.head))]
            elif snake2.head in snake1.position:
                return [(team1_id, snake1_id, snake1.position.index(snake2.head))]
            else:
                return None
        else:
            if snake1.head == snake2.head:
                return [(team1_id, snake1_id, -1), (team2_id, snake2_id, -1)]
            elif snake1.head in snake2.position:
                return [(team1_id, snake1_id, -1)]
            elif snake2.head in snake1.position:
                return [(team2_id, snake2_id, -1)]
            else:
                return None

    def collisionsOnBoard(state):
        collisions = []

        for i in xrange(len(state.teams)):
            for j in xrange(len(state.teams[i].snakes)):
                for k in xrange(i, len(state.teams)):
                    start_index = 0
                    if i == k:
                        start_index = j
                    for l in xrange(start_index, len(state.teams[k].snakes)):
                        foo = collision(j, i, l, k)
                        if foo != None:
                            collisions.append(foo)



        # for i in range(len(state.snakes)):
        #     for j in range(len(state.snakes)):
        #         if i != j:
        #             foo = collision(state.snakes[i], state.snakes[j], True, state)
        #             if foo != None:
        #                 collisions.append(foo)
        #     for j in range(len(state.snakes2)):
        #         foo = collision(state.snakes[i], state.snakes2[j], False, state)
        #         if foo != None:
        #             collisions.append(foo)

        # for i in range(len(state.snakes2)):
        #     for j in range(len(state.snakes2)):
        #         if i != j:
        #             foo = collision(state.snakes2[i], state.snakes2[j], True, state)
        #             if foo != None:
        #                 collisions.append(foo)
        return collisions