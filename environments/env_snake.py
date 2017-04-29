import random
import numpy as np

class Environment:

	def __init__(self, n=20, vision_radius = 2):
		self.n = n
		self.vision_radius = vision_radius
		self.reset()
		
	def reset(self):
		self.points = 0
		self.matrix = np.zeros((self.n, self.n))
		self.empty = [(i, j) for i in range(self.n) for j in range(self.n)]
		self.obstacles =[(0, i) for i in range(self.n)] + \
						[(self.n-1, i) for i in range(self.n)] + \
						[(i, 0) for i in range(1, self.n-1)] + \
						[(i, self.n-1) for i in range(1, self.n-1)]
		for obs in self.obstacles:
			self.empty.remove(obs)
			self.matrix[obs] = 3
		first_pos = random.choice(self.empty)
		self.matrix[first_pos] = 1
		self.snake = [first_pos]
		self.empty.remove(first_pos)
		self.direction = self.right
		self.new_food()

	def get_individual_env(self):
		return IndividualEnv

	def new_food(self):
		self.food = random.choice(self.empty)
		self.matrix[self.food] = 2
		self.empty.remove(self.food)

	def do_nothing(self):
		return self.direction()

	def up(self):
		if self.direction == self.down:
			return self.down()
		self.direction = self.up
		head = self.snake[0]
		new_head = (head[0]-1, head[1])
		return self.update(new_head)

	def down(self):
		if self.direction == self.up:
			return self.up()
		self.direction = self.down
		head = self.snake[0]
		new_head = (head[0]+1, head[1])
		return self.update(new_head)

	def left(self):
		if self.direction == self.right:
			return self.right()
		self.direction = self.left
		head = self.snake[0]
		new_head = (head[0], head[1]-1)
		return self.update(new_head)

	def right(self):
		if self.direction == self.left:
			return self.left()
		self.direction = self.right
		head = self.snake[0]
		new_head = (head[0], head[1]+1)
		return self.update(new_head)
		
	def update(self, new_head):
		if new_head in self.obstacles or new_head in self.snake:
			return True
		self.snake = [new_head] + self.snake
		self.matrix[new_head] = 1
		if new_head in self.empty:
			self.empty.remove(new_head)
			tail = self.snake.pop()
			self.empty.append(tail)
			self.matrix[tail] = 0
			return False
		self.points += 10
		self.new_food()
		return False			

class IndividualEnv:

	def __init__(self, environment):
		self.actions = [environment.up, environment.down, environment.left, environment.right, environment.do_nothing]
		self.env = environment
		self.n_steps = 0

	def step(self, action):
		self.n_steps += 1
		#print(action)
		a = self.actions[action]

		done = a()

		if done:
			return self.get_state(), self.env.points, True

		return self.get_state(), -1, False

	def get_state(self):
		snake_head = self.env.snake[0]
		size = 2*self.env.vision_radius + 1
		x = np.zeros((size, size))
		for i in range(-int(size/2), int(size/2)+1):
			for j in range(-int(size/2), int(size/2)+1):
				if snake_head[0] + i >= 0 and snake_head[1] + j >= 0 and snake_head[0] + i < self.env.matrix.shape[0] and snake_head[1] + j < self.env.matrix.shape[1]:
					x[i+int(size/2), j+int(size/2)] = self.env.matrix[snake_head[0] + i, snake_head[1] + j]
		return tuple(map(tuple, x))

	def show(self):
		print('Won with ' + str(self.env.points) + ' points!')
