from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

class FlotsamFight:

	def play(self):
		print("Starting Game")

		number_of_players = 4
		number_of_cards_per_hand = 10

		d = Deck()
		b = Board(number_of_players)
		# players = [player for player in (Player() for i in range(number_of_players))]
		players = [Player("Albus"), Player("Bobby"), Player("Chloe"), Player("Debra")]

		print("Shuffling and dealing cards")
		d.shuffle()
		for i in range(number_of_cards_per_hand):
			for player in players:
				player.hand.addCard(d.deal())

		gameWinner = False
		roundNumber = 0

		#Game Loop
		while(not gameWinner):
			self.printNewTrick()
			lastPlayerToPlay = None
			passedPlayers = 0
			[self.deal2Cards(d, player) for player in players] #If a player is down to 1 card at the start of a trick, deal 2 more cards
			[player.newTrick() for player in players]

			#Trick Loop
			while(passedPlayers < len(players)-1): #If at least two players haven't passed, keep playing 
				roundNumber = roundNumber + 1
				self.printRoundHeader(roundNumber, players, passedPlayers)	
				players = self.orderPlayers(players, lastPlayerToPlay) #Player who played last goes first

				for player in players:
					validMoves = player.getValidMoves(b)
					self.printValidMoves(player, validMoves)
					if (len(validMoves)): #If player has valid moves, play one
						card, lifeboat = validMoves[0][0], validMoves[0][1][0]
						self.printCardToPlay(card, lifeboat)
						player.playCard(b, card, lifeboat)
						lastPlayerToPlay = player
						if (len(player.hand.cards) == 0):
							passedPlayers = len(players)
							gameWinner = player
					else: #If no valid moves, pass							
						self.printPlayerPasses(player)
						if (player.passTurn()):
							passedPlayers = passedPlayers + 1
					print(b,"\n")

			self.printLastPlayerToPlay(lastPlayerToPlay)
			b = Board(number_of_players) #Wipe the board and start a new trick

		self.printGameWinner(gameWinner, roundNumber)
		self.updateScores(players)
		print("Ending Game")


	def printNewTrick(self):
		print("\n_________________\n___ NEW TRICK ___\n_________________")

	def printRoundNumber(self, roundNumber):
		print("\n___ ROUND", roundNumber, "___")

	def printCurrentHands(self, players):
		print("Current Hands:")
		[print(player.hand.list()) for player in players]

	def printPassedPlayers(self, passedPlayers):
		print("Passed Players:",passedPlayers)

	def printRoundHeader(self, roundNumber, players, passedPlayers):
		self.printRoundNumber(roundNumber)
		self.printCurrentHands(players)
		self.printPassedPlayers(passedPlayers)
		print("----------------\n")

	def printValidMoves(self, player, validMoves):
		print(player, ":", validMoves)

	def printCardToPlay(self, card, lifeboat):
		print("Playing", card, "in boat", lifeboat)

	def printPlayerPasses(self, player):
		print(player, "passes")

	def printLastPlayerToPlay(self, lastPlayerToPlay):
		print("lastPlayerToPlay:", lastPlayerToPlay)

	def printGameWinner(self, gameWinner, roundNumber):
		print(gameWinner, "won in", roundNumber, "rounds!")

	def deal2Cards(self, d, player):
		if(len(player.hand.cards) == 1):
			print("Giving 2 extra cards to", player)
			player.hand.addCard(d.deal())
			player.hand.addCard(d.deal())

	def orderPlayers(self, players, lastPlayerToPlay): #Makes the last player to play to be the first player 
		while(lastPlayerToPlay and players[0].name != lastPlayerToPlay.name):
			player = players.pop(0)
			players.append(player)

		return players 

	def updateScores(self, players):
		for player in players:
			if (len(player.hand.cards) == 0):
				player.addScore(2)
			else: 
				print(player, player.highestCard())
