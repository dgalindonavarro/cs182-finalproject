class Team():
	def __init__(self, id, color):
		self.id = id
		self.snakes = []
		self.color = color

	# Return current score of team, which is equal to the sum of snake lengths
	def getScore(self):
		score = 0
		for snake in self.snakes:
			score += snake.length
		return score

	# Update a member of the team
	def updateSnake(self, snake_id, index):
		self.snakes[snake_id].updateSnake(index)


