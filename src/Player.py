from Hand import Hand
from Board import Board

class Player:

	def __init__(self):
		self.score = 0
		self.hand = Hand()
		self.validMoves = []

	def getValidMoves(self, board):
		moves = []
		for card in self.hand.cards:
			move = [card.value]
			move.append(board.getValidLifeboatsForCard(card))
			moves.append(move)
		return moves

	def playCard(self, board, cardNumber, lifeboatNumber):
		card = self.hand.getCard(cardNumber)
		print(card, lifeboatNumber)
		return self.hand.playCard(board, card, lifeboatNumber)

		