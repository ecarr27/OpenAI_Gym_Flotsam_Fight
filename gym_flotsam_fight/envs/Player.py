from Hand import Hand
from Board import Board

class Player:

	PLAY = True
	PASS = "Pass"
	WON  = "WON"

	def __init__(self, name, isAgent=False):
		self.score = 0
		self.hand = Hand()
		self.isPass = False
		self.name = name
		self.isAgent = isAgent

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

	def autoPlay(self, board, enabled=True):
		validMoves = self.getValidMoves(board)
		self.printValidMoves(validMoves, enabled)
		if (len(validMoves)): #If player has valid moves, play one
			card, lifeboat = validMoves[0][0], validMoves[0][1][0]
			self.printCardToPlay(card, lifeboat, enabled)
			self.playCard(board, card, lifeboat)
			if (len(self.hand.cards) == 0):
				return self.WON
			return self.PLAY
		else: #If no valid moves, pass							
			self.printPlayerPasses(enabled)
			self.passTurn()
			return self.PASS

	def play(self, board, action, enabled=True):
		if (not self.isAgent or action == [-2, -2]):
			return self.autoPlay(board, enabled)
		elif (action == [-1, -1] or self.isPass):
			self.printPlayerPasses(enabled)
			self.passTurn()
			return self.PASS

		self.printCardToPlay(action[0], action[1], enabled)
		successfulPlay = self.playCard(board, action[0], action[1])
		if (not successfulPlay):
			return False
		elif (successfulPlay and len(self.hand.cards) == 0):
			returnValue = self.WON
		elif (successfulPlay):
			return successfulPlay
		else:
			print("Error in Player.Play()")
			return False

	def __str__(self):
		return self.name

	def printValidMoves(self, validMoves, enabled=True):
		if(enabled):
			print(self, ":", validMoves)

	def printCardToPlay(self, card, lifeboat, enabled=True):
		if(enabled):
			print("Playing", card, "in boat", lifeboat)

	def printPlayerPasses(self, enabled=True):
		if(enabled):
			print(self, "passes")
		