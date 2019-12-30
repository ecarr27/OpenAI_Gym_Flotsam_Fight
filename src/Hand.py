from Board import Board
class Hand:
	def __init__(self):
		self.cards = []

	def addCard(self, card):
		self.cards.append(card)

	def getCard(self, number):
		for card in self.cards:
			if (card.value == number):
				return card
		return False

	def playCard(self, board, card, lifeboatNumber):
		if (not card in self.cards):
			return False
		didPlayCard = board.addCardToLifeboat(card, lifeboatNumber)
		if (didPlayCard):
			self.cards.remove(card)
		return didPlayCard

	def list(self):
		values = []
		for card in self.cards:
			values.append(str(card))
		return values

	def sort(self):
		self.cards.sort()
