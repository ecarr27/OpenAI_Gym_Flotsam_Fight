from Lifeboat import Lifeboat

class Board:

	lifeboatNumbers = [3, 4, 5, 6, 7, 8, 9, 10]

	def __init__(self, lifeboats=lifeboatNumbers):
		if (lifeboats):
			self.lifeboats = []
			for number in lifeboats:
				self.lifeboats.append(Lifeboat(number))

	def lifeboats(self):
		return self.lifeboatNumbers


	def lifeboat(self, lifeboatNumber):
		return self.lifeboats[lifeboatNumber - 3]

	def canAddCardToLifeboat(self, card, lifeboatNumber):
		if (not lifeboatNumber in self.lifeboatNumbers):
			return False
		return self.lifeboat(lifeboatNumber).canAddCard(card)

	def addCardToLifeboat(self, card, lifeboatNumber):
		if (self.canAddCardToLifeboat(card, lifeboatNumber)):
			return self.lifeboat(lifeboatNumber).addCard(card)
		else:
			return False
