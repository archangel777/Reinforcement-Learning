import random

class Table:

	def __init__(self):
		self.reset()

	def top_card(self):
		if not self.cards:
			return None
		return self.cards[-1]

	def draw(self):
		return self.cards.pop()

	def play(self, card):
		self.cards.append(card)

	def reset(self):
		self.cards = []


class Deck:

	def __init__(self, table):
		self.table = table
		self.reset()

	def shuffle(self):
		random.shuffle(self.cards)

	def draw(self):
		if len(self.cards) <= 3:
			self.eat_table()
		return self.cards.pop()

	def eat_table(self):
		self.cards += self.table.cards[:-1]
		self.shuffle()
		self.table.cards = [self.table.cards[-1]]

	def reset(self):
		self.cards = [i for i in range(52)]
		self.shuffle()

class Environment:

	def __init__(self):
		self.table = Table()
		self.deck = Deck(self.table)

	def reset(self):
		self.table.reset()
		self.deck.reset()

	def get_individual_env(self):
		return IndividualEnv

class IndividualEnv:

	def __init__(self, environment):
		self.actions = [a for a in range(52*2)]
		self.deck = environment.deck
		self.table = environment.table
		self.state_index = {}
		self.hand = [self.deck.draw() for i in range(9)]		

	def step(self, action, subgoals=False):
		take_decision = int(action/52)
		drop_decision = int(action - take_decision*52)

		if drop_decision not in self.hand or (take_decision == 1 and not self.table.top_card()):
			return self.get_state(), -5, False

		if take_decision == 0:
			self.hand.append(self.deck.draw())
		else:
			self.hand.append(self.table.draw())

		if self.triple_number(self.hand) == 3:
			return self.get_state(), 1000, True

		self.hand.remove(drop_decision)
		self.table.play(drop_decision)

		if subgoals:
			if self.there_are_2_triples(self.hand):
				return self.get_state(), 10, False

			if self.there_is_a_triple(self.hand):
				return self.get_state(), 5, False

		return self.get_state(), 0, False

	def get_state(self):
		return tuple(sorted(self.hand) + [self.table.top_card()])

	def card(self, number):
		return number - 13 * int(number/13)

	def naipe(self, number):
		return int(number/13)


	def there_are_3_triples(self):
		l = sorted(self.hand, key=lambda x: self.card(x))
		eq_test = sorted(self.hand, key=lambda x: self.card(x))
		seq_test = sorted(self.hand)
		for i in [0,1]:
			if self.is_equal_triple(eq_test[i], eq_test[i+1], eq_test[i+2]) and self.there_are_2_triples(eq_test[i+3:]):
				return True
			if self.is_sequence(seq_test[i], seq_test[i+1], seq_test[i+2]) and self.there_are_2_triples(seq_test[i+3:]):
				return True
		return False

	def there_are_2_triples(self, l):
		eq_test = sorted(l, key=lambda x: self.card(x))
		seq_test = sorted(l)

		for i in range(len(l)%6 + 1):
			if self.is_equal_triple(eq_test[i], eq_test[i+1], eq_test[i+2]) and self.there_is_a_triple(eq_test[i+3:]):
				return True
			if self.is_sequence(seq_test[i], seq_test[i+1], seq_test[i+2]) and self.there_is_a_triple(seq_test[i+3:]):
				return True
		return False

	def there_is_a_triple(self, l):
		eq_test = sorted(l, key=lambda x: self.card(x))
		seq_test = sorted(l)

		for i in range(len(l)%3 + 1):
			if self.is_equal_triple(eq_test[i], eq_test[i+1], eq_test[i+2]):
				return True
			if self.is_sequence(seq_test[i], seq_test[i+1], seq_test[i+2]):
				return True
		return False

	def triple_number(self, l):
		eq_test = sorted(l, key=lambda x: self.card(x))
		seq_test = sorted(l)

		if len(l) < 3: return 0

		acc = 0

		for i in range(len(l)%3 + 1):
			if self.is_equal_triple(eq_test[i], eq_test[i+1], eq_test[i+2]):
				acc = max( acc, 1 + self.triple_number(eq_test[i + 3:]) )
			if self.is_sequence(seq_test[i], seq_test[i+1], seq_test[i+2]):
				acc = max( acc, 1 + self.triple_number(seq_test[i + 3:]) )
		return acc

	def is_sequence(self, c1, c2, c3):
		return (self.naipe(c1) == self.naipe(c2) == self.naipe(c3)) and (self.card(c1) == self.card(c2) - 1 == self.card(c3) - 2)

	def is_equal_triple(self, c1, c2, c3):
		return self.card(c1) == self.card(c2) == self.card(c3)

	def show(self):
		naipe = {0: 'paus', 1: 'espadas', 2: 'ouro', 3: 'copas'}
		h = [str(self.card(c)) + '-' + naipe[self.naipe(c)] for c in sorted(self.hand)]
		print(h)
