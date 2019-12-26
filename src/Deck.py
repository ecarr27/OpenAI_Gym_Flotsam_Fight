import random

from Card import Card

class Deck:
	def __init__(self):
		self.cards = []
		self.cards = [card for card in (Card(number) for number in range(2, 98)) if card.valid]

	def __str__(self):
		return self.deck[0]

	def shuffle(self):
		random.shuffle(self.cards, random.random)

	def deal(self):
		return self.cards.pop(0)

