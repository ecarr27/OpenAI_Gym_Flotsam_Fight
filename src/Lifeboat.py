from Card import Card

class Lifeboat:
	def __init__(self, number):
		self.number = number
		self.cards = []

	def addCard(self, card):
		if ((self.number in card.factors) and (self.highestValue() < card.value)):
			self.cards.append(card)
			return True
		else:
			return False

	def clear(self):
		self.cards.clear()

	def list(self):
		values = []
		for card in self.cards:
			values.append(str(card))
		return values

	def highestValue(self):
		if (len(self.cards)):
			return self.cards[-1].value
		else:
			return 0