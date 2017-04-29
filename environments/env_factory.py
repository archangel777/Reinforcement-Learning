from environments.env_batidinha import Environment as EnvBatidinha
from environments.env_hanoi import Environment as EnvHanoi
from environments.env_2048 import Environment as Env2048
from environments.env_snake import Environment as EnvSnake

class EnvFactory:

	def env_batidinha():
		return EnvBatidinha

	def env_hanoi():
		return EnvHanoi

	def env_2048():
		return Env2048

	def env_snake():
		return EnvSnake