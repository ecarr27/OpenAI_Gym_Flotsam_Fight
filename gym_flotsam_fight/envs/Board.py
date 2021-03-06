from Lifeboat import Lifeboat

class Board:

	lifeboatNumbers = [3, 4, 5, 6, 7, 8, 9, 10]

	def __init__(self, playerCount, lifeboats=lifeboatNumbers):
		if (lifeboats):
			self.lifeboats = []
			self.playerCount = playerCount
			self.validLifeboats = self.lifeboatNumbers
			self.usedLifeboats = []
			for number in lifeboats:
				self.lifeboats.append(Lifeboat(number))

	def lifeboats(self):
		return self.lifeboatNumbers

	def lifeboat(self, lifeboatNumber):
		return self.lifeboats[lifeboatNumber - 3]

	def canAddCardToLifeboat(self, card, lifeboatNumber):
		if (not lifeboatNumber in self.validLifeboats):
			return False
		elif (len(self.usedLifeboats) >= self.playerCount):
			if (lifeboatNumber in self.usedLifeboats):
				return self.lifeboat(lifeboatNumber).canAddCard(card)
			else:
				return False
		else:
			return self.lifeboat(lifeboatNumber).canAddCard(card)

	def getValidLifeboatsForCard(self, card):
		validLifeboatsForCard = []
		for lifeboatNumber in self.lifeboatNumbers:
			if(self.canAddCardToLifeboat(card, lifeboatNumber)):
				validLifeboatsForCard.append(lifeboatNumber)
		return validLifeboatsForCard

	def useALifeboat(self, lifeboatNumber):
		if (not lifeboatNumber in self.usedLifeboats):
			self.usedLifeboats.append(lifeboatNumber)

		if (len(self.usedLifeboats) >= self.playerCount):
			self.validLifeboats = self.usedLifeboats

	def addCardToLifeboat(self, card, lifeboatNumber):
		if (self.canAddCardToLifeboat(card, lifeboatNumber)):
			addedCard = self.lifeboat(lifeboatNumber).addCard(card)
			if (addedCard):
				self.useALifeboat(lifeboatNumber)
			return addedCard
		else:
			return False

	def getHighestNumbersAsString(self):
		values = ""
		for lifeboat in self.lifeboats:
			values = values + str(lifeboat.highestValue()).rjust(3)
		return values

	def state(self):
		return [lifeboat.highestValue() for lifeboat in self.lifeboats]

	def setBoard(self, cards):
		i = 0
		for card in cards:
			if (card):
				self.addCardToLifeboat(card, self.lifeboatNumbers[i])
			i = i + 1

	def __str__(self):
		boardString = ' '.join(str(i).rjust(2) for i in self.lifeboatNumbers)
		highestValues = self.getHighestNumbersAsString()
		return " " + boardString + "\n" + highestValues 
