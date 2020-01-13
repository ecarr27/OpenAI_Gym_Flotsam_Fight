from Hand import Hand
from Board import Board

class Player:

	PLAY = True
	PASS = "Pass"
	WON  = "WON"
	ACTION_PASS = [-1, -1]
	ACTION_FIRST_OPTION = [-2, -2]
	 

	def __init__(self, name, isAgent=False, alwaysPass=False):
		self.score = 0
		self.hand = Hand()
		self.isPass = False
		self.name = name
		self.isAgent = isAgent
		self.alwaysPass = alwaysPass

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
			return self.PASS
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
		if (len(validMoves) and not self.alwaysPass): #If player has valid moves, play one
			card, lifeboat = validMoves[0][0], validMoves[0][1][0]
			self.printCardToPlay(card, lifeboat, enabled)
			play = self.playCard(board, card, lifeboat)
			if (len(self.hand.cards) == 0):
				return self.WON
			if (play == True):
				play = self.PLAY
			return play
		else: #If no valid moves, pass							
			self.printPlayerPasses(enabled)
			self.passTurn()
			return self.PASS

	def play(self, board, action, enabled=True):
		if (not self.isAgent or action == self.ACTION_FIRST_OPTION):
			return self.autoPlay(board, enabled)
		elif (action == self.ACTION_PASS or self.isPass):
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
		