from Hand import Hand
from Board import Board

class Player:

	def __init__(self, name):
		self.score = 0
		self.hand = Hand()
		self.isPass = False
		self.name = name

	def getValidMoves(self, board):
		moves = []
		for card in self.hand.cards:
			move = [card.value]
			validMoves = board.getValidLifeboatsForCard(card) 
			if (len(validMoves)):
				move.append(board.getValidLifeboatsForCard(card))
				moves.append(move)
		return moves

	def playCard(self, board, cardNumber, lifeboatNumber):
		if (self.isPass):
			return False
		card = self.hand.getCard(cardNumber)
		return self.hand.playCard(board, card, lifeboatNumber)

	def passTurn(self):
		if (not self.isPass):
			self.isPass = True
			return True
		return False

	def newTrick(self):
		self.isPass = False
		self.hand.sort()

	def addScore(self, score):
		self.score = self.score + score

	def highestCard(self):
		return self.hand.highestCard()

	def __str__(self):
		return self.name
		