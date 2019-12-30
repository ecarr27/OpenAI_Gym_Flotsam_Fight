from Hand import Hand
from Board import Board

class Player:

	def __init__(self):
		self.score = 0
		self.hand = Hand()

	def getValidMoves(self, board):
		return board