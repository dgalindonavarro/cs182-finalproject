class Team():
	def __init__(self, id, color):
		self.id = id
		self.snakes = []
		self.color = color

	def getScore(self):
		score = 0
		for snake in self.snakes:
			score += snake.length
		return score

	def updateSnake(self, snake_id, index):
		self.snakes[snake_id].updateSnake(index)


