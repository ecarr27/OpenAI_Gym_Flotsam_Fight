from Board import Board
class Hand:
	def __init__(self):
		self.cards = []

	def addCard(self, card):
		self.cards.append(card)

	def playCard(self, card, board, lifeboatNumber):
		if (not card in self.cards):
			return False
		
		return board.addCardToLifeboat(card, lifeboatNumber)

	def list(self):
		values = []
		for card in self.cards:
			values.append(str(card))
		return values

	def sort(self):
		self.cards.sort()
