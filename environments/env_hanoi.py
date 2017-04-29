import random

class Environment:

	def __init__(self, n):
		self.n = n
		self.reset()
		
	def reset(self):
		self.start_stack = [self.n - i - 1 for i in range(self.n)]
		self.mid_stack = []
		self.goal = []

	def get_individual_env(self):
		return IndividualEnv

class IndividualEnv:

	def __init__(self, environment):
		self.actions = [a for a in range(9) if int(a/3) != int(a%3)]
		self.env = [environment.start_stack, environment.mid_stack, environment.goal]
		self.n_steps = 0

	def step(self, action):
		self.n_steps += 1
		#print(action)
		a = self.actions[action]
		take_decision = int(a/3)
		drop_decision = int(a%3)

		if not self.env[take_decision] or (self.env[drop_decision] and self.env[drop_decision][-1] < self.env[take_decision][-1]):
			return self.get_state(), -50, False

		#print(take_decision, drop_decision)

		self.env[drop_decision].append(self.env[take_decision].pop())

		if not self.env[0] and not self.env[1]:
			return self.get_state(), 50, True

		#print(self.get_state())

		return self.get_state(), -10, False

	def get_state(self):
		return tuple(map(tuple,self.env))

	def show(self):
		print('Won in ' + str(self.n_steps) + ' steps!')
