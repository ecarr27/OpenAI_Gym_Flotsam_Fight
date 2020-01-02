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

		# players = [player for player in (Player() for i in range(number_of_players))]
		players = [Player("Albus"), Player("Bobby"), Player("Chloe"), Player("Debra")]

		#Grand Prix Loop
		for gameNumber in range(1,4):
			self.printGameHeader(gameNumber, players)
			
			d = Deck()
			d.shuffle()

			b = Board(number_of_players)
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
				players = self.orderPlayers(players, lastPlayerToPlay) #Player who played last goes first

				#Trick Loop
				while(passedPlayers < len(players)-1): #If at least two players haven't passed, keep playing 
					roundNumber = roundNumber + 1
					self.printRoundHeader(roundNumber, players, passedPlayers)	

					for player in players:
						play = player.play(b)
						if (play == "Played"):
							lastPlayerToPlay = player
						elif (play == "Won"):
							lastPlayerToPlay = player
							passedPlayers = len(players)
							gameWinner = player
						elif (play == "Passed" and player.passTurn()):
							passedPlayers = passedPlayers + 1

						print(b,"\n")

				if(not gameWinner):						
					self.printLastPlayerToPlay(lastPlayerToPlay)
				b = Board(number_of_players) #Wipe the board and start a new trick

			self.printGameWinner(gameWinner, roundNumber)
			self.updateScores(players)
			self.printGameFooter(gameNumber, players)

		self.printGrandPrixFooter(players)

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

	def printLastPlayerToPlay(self, lastPlayerToPlay):
		print("lastPlayerToPlay:", lastPlayerToPlay)

	def printGameWinner(self, gameWinner, roundNumber):
		print(gameWinner, "won in", roundNumber, "rounds!\n")

	def printGameHeader(self, gameNumber, players):
		print("\n____ GAME", gameNumber, "____")
		print("Scores:")
		self.printPlayerScores(players)
		print("----------------")
		print("Shuffling and dealing cards\n")

	def printGameFooter(self, gameNumber, players):
		print("Ending Game",gameNumber)
		self.printPlayerScores(players)
		print()

	def printGrandPrixFooter(self, players):
		sortedScores = self.sortScores(players)
		winningPlayer = list(sortedScores)[-1]
		print(winningPlayer, "won overall with", sortedScores[winningPlayer], "points!")

	def printPlayerScores(self, players):
		sortedScores = self.sortScores(players)

		for player in reversed(list(sortedScores)):
			print(player, str(sortedScores[player]).rjust(2))

	def sortScores(self, players):
		scores = {}
		for player in players:
			scores[player] = player.score

		return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

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
		scores = {}
		for player in players:
			if (len(player.hand.cards) == 0):
				player.addScore(2)
			else: 
				scores[player] = player.highestCard().value

		sortedScores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
		lowestOfHighestCards = list(sortedScores)[0]
		highestOfHighestCards = list(sortedScores)[-1]

		lowestOfHighestCards.addScore(1)
		highestOfHighestCards.addScore(-1)