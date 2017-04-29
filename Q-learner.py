import numpy as np
import random
import os.path
import pickle
from ast import literal_eval
from environments.env_factory import EnvFactory

class Agent:

	def __init__(self):
		self.alpha = 0.5
		self.epsilon = 0.1
		self.discount = 0.9
		self.started_Q = False


	def start_game(self, environment):
		self.env = environment.get_individual_env()(environment)
		self.currentState = self.env.get_state()
		#self.Q = {self.currentState : np.random.randn(len(self.env.actions))}
		if not self.started_Q:
			self.Q = {}
			self.started_Q = True
		if self.currentState not in self.Q:
			self.Q[self.currentState] = np.random.randn(len(self.env.actions))

		self.currentAction = self.get_action(self.currentState)

	def play(self, serious=False):
		
		made_a_move = False
		done = False

		while not made_a_move and not done:

			self.currentState = self.env.get_state()
			if self.currentState not in self.Q:
				self.Q[self.currentState] = np.random.randn(len(self.env.actions))

			if serious: self.currentAction = self.get_action_greedy(self.currentState)
			else: 		self.currentAction = self.get_action(self.currentState)

			nextState, reward, done = self.env.step(self.currentAction)
			made_a_move = nextState != self.currentState
			
			if nextState not in self.Q:
				self.Q[nextState] = np.random.randn(len(self.env.actions))

			nextAction = self.get_action_greedy(nextState)

			self.Q[self.currentState][self.currentAction] += self.alpha * (reward + self.discount * self.Q[nextState][nextAction] - self.Q[self.currentState][self.currentAction])

		return done

	def get_action(self, state):
		if np.random.rand() <= self.epsilon:
			return random.randint(0, len(self.env.actions)-1)
		return self.get_action_greedy(state)

	def get_action_greedy(self, state):
		return np.argmax(self.Q[state][:])

	def update_Q_values(self, newQ):
		if not self.started_Q:
			self.Q = {}
			self.started_Q = True
		self.Q.update(newQ)

	def show(self):
		self.env.show()

def load_Q(agent_list, game_name):
	print('loading...')
	if os.path.isfile('Q-values-' + game_name + '.txt'):
		with open('Q-values-' + game_name + '.txt', 'rb') as f:
			Q = pickle.load(f)
			for agent in agent_list:
				agent.update_Q_values(Q)
	print('done!')

def save_Q(agent, game_name):
	print('saving...')
	with open('Q-values-' + game_name + '.txt', 'wb') as f:
		pickle.dump(agent.Q, f, pickle.HIGHEST_PROTOCOL)
	print('done!')

def run_episode(agents, environment, serious=False):
	environment.reset()
	for agent in agents:
		agent.start_game(environment)
		agent.epsilon *= 0.999
	while True:
		results = [agent.play(serious=serious) for agent in agents]
		if True in results:
			winner = agents[results.index(True)]
			winner.show()
			for agent in agents:
				agent.update_Q_values(winner.Q)
			break;

class Game:

	def __init__(self, n_episodes, batch_size, n_players):
		self.agents = None
		self.n_episodes = n_episodes
		self.batch_size = batch_size
		self.n_players = n_players

	def set_env(self, env):
		self.environment = env

	def train(self):
		self.agents = [Agent() for i in range(self.n_players)]
		load_Q(self.agents, self.game_name())

		for i in range(self.n_episodes):
			run_episode(self.agents, self.environment)
			if (i != 0 and i%self.batch_size == 0) or i == self.n_episodes - 1:
				save_Q(self.agents[0], self.game_name())

		print('There are ' + str(len(self.agents[0].Q)) + ' states')

	def play_seriously(self):
		if not self.agents:
			self.agents = [Agent() for i in range(self.n_players)]
			load_Q(self.agents, self.game_name())
		print('Playing seriously')
		run_episode(self.agents, self.environment, serious=True)


class GameBatidinha(Game):

	def __init__(self, n_episodes, batch_size, n_players=4):
		super(GameBatidinha, self).__init__(n_episodes, batch_size, n_players)
		self.set_env(EnvFactory.env_batidinha()())

	def game_name(self):
		return 'batidinha'

class GameHanoi(Game):

	def __init__(self, n_episodes, batch_size, n_pieces=7):
		super(GameHanoi, self).__init__(n_episodes, batch_size, 1)
		self.set_env(EnvFactory.env_hanoi()(n_pieces))

	def game_name(self):
		return 'hanoi'

class Game2048(Game):

	def __init__(self, n_episodes, batch_size):
		super(Game2048, self).__init__(n_episodes, batch_size, 1)
		self.set_env(EnvFactory.env_2048()())

	def game_name(self):
		return '2048'

class GameSnake(Game):

	def __init__(self, n_episodes, batch_size, board_size=10, vision_radius = 2):
		super(GameSnake, self).__init__(n_episodes, batch_size, 1)
		self.set_env(EnvFactory.env_snake()(board_size, vision_radius))

	def game_name(self):
		return 'snake'


'''
	Main code

'''

n_episodes = 100000
batch_size = 1000

batidinha = GameBatidinha(n_episodes, batch_size)
hanoi = GameHanoi(n_episodes, batch_size, 8)
game2048 = Game2048(n_episodes, batch_size)
snake = GameSnake(n_episodes, batch_size, vision_radius=3)

snake.train()

snake.play_seriously()
		

