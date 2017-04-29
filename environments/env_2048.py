import random
import numpy as np

class Environment:

	def __init__(self):
		self.reset()
		
	def reset(self):
		self.matrix = np.zeros((4,4))
		self.zeros = [(i, j) for i in range(4) for j in range(4)]
		self.add_piece()
		self.add_piece()

	def add_piece(self):
		if not self.zeros: return False
		c = random.choice(self.zeros)
		if np.random.rand() < 0.1:	
			self.matrix[c] = 4
		else: 
			self.matrix[c] = 2
		self.zeros.remove(c)
		return True

	def max_piece(self):
		return np.amax(self.matrix)

	def can_move(self):
		can = False
		for i in range(4):
			for j in range(4):
				if i > 0 and (self.matrix[i-1, j] == 0 or self.matrix[i-1, j] == self.matrix[i, j]):
					can = True
				if j > 0 and (self.matrix[i, j-1] == 0 or self.matrix[i, j-1] == self.matrix[i, j]):
					can = True
				if i < 3 and (self.matrix[i+1, j] == 0 or self.matrix[i+1, j] == self.matrix[i, j]):
					can = True
				if j < 3 and (self.matrix[i, j+1] == 0 or self.matrix[i, j+1] == self.matrix[i, j]):
					can = True
		return can


	def move_piece(self, f, t):
		if t in self.zeros:
			self.zeros.remove(t)
		self.matrix[t] += self.matrix[f]
		self.zeros.append(f)
		self.matrix[f] = 0

	def up(self):
		points_to_add = 0
		moved = False
		for i in [1, 2, 3]:
			for j in range(4):
				if (i,j) in self.zeros:
					continue
				k = i
				while k > 0 and (k-1,j) in self.zeros:
					moved = True
					self.move_piece((k, j), (k-1, j))
					k -= 1
				if k > 0 and (self.matrix[k,j] == self.matrix[k-1,j]):
					moved = True
					self.move_piece((k, j), (k-1, j))
					points_to_add = self.matrix[k-1,j]
		if moved: self.add_piece()
		return points_to_add - 1

	def down(self):
		points_to_add = 0
		moved = False
		for i in [2, 1, 0]:
			for j in range(4):
				if (i,j) in self.zeros:
					continue
				k = i
				while k < 3 and (k+1,j) in self.zeros:
					moved = True
					self.move_piece((k, j), (k+1, j))
					k += 1
				if k < 3 and (self.matrix[k,j] == self.matrix[k+1,j]):
					moved = True
					self.move_piece((k, j), (k+1, j))
					points_to_add = self.matrix[k+1,j]
		if moved: self.add_piece()
		return points_to_add - 1

	def left(self):
		points_to_add = 0
		moved = False
		for j in [1, 2, 3]:
			for i in range(4):
				if (i,j) in self.zeros:
					continue
				k = j
				while k > 0 and (i,k-1) in self.zeros:
					moved = True
					self.move_piece((i, k), (i, k-1))
					k -= 1
				if k > 0 and (self.matrix[i,k] == self.matrix[i,k-1]):
					moved = True
					self.move_piece((i, k), (i, k-1))
					points_to_add = self.matrix[i,k-1]
		if moved: self.add_piece()
		return points_to_add - 10

	def right(self):
		points_to_add = 0
		moved = False
		for j in [2, 1, 0]:
			for i in range(4):
				if (i,j) in self.zeros:
					continue
				k = j
				while k < 3 and (i,k+1) in self.zeros:
					moved = True
					self.move_piece((i, k), (i, k+1))
					k += 1
				if k < 3 and (self.matrix[i,k] == self.matrix[i,k+1]):
					moved = True
					self.move_piece((i, k), (i, k+1))
					points_to_add = self.matrix[i,k+1]
		if moved: self.add_piece()
		return points_to_add - 1

	def get_individual_env(self):
		return IndividualEnv

class IndividualEnv:

	def __init__(self, environment):
		self.actions = [environment.up, environment.down, environment.left, environment.right]
		self.env = environment
		self.n_steps = 0

	def step(self, action):
		self.n_steps += 1

		if not self.env.can_move():
			return self.get_state(), -1, True

		reward = self.actions[action]()

		return self.get_state(), reward, False

	def get_state(self):
		return tuple(map(tuple, self.env.matrix))

	def show(self):
		print('=============================================')
		#print(self.env.matrix)
		print('Max value: ' + str(self.env.max_piece()))
