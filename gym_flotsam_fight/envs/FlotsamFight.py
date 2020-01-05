from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

class FlotsamFight:

	def seed(self, seed=None):
		# self.np_random, seed = seeding.np_random(seed)
  #       return [seed]
		return False

	def step(self, action):
		return False

	def reset(self):
		return False

	def render(self):
		return False

	def close(self):
		return False

	def test(self):
		d = Deck()
		maxCard, maxFactors = None, None
		maxFactorLen = 0
		for card in d.cards:
			print(card, card.factors)
			if (len(card.factors) > maxFactorLen):
				maxCard, maxFactors = card, card.factors
				maxFactorLen = len(card.factors)
		print(card, card.factors)

	def play(self, gameCount = 3, loud=True):
		# print("Starting Game")
		self.loud = loud
		number_of_players = 4
		number_of_cards_per_hand = 10

		# players = [player for player in (Player() for i in range(number_of_players))]
		players = [Player("Albus"), Player("Bobby"), Player("Chloe"), Player("Debra")]

		#Grand Prix Loop
		for gameNumber in range(1, gameCount):
			self.printGameHeader(gameNumber, players, self.loud)
			
			d = Deck()
			d.shuffle()

			b = Board(number_of_players)
			for i in range(number_of_cards_per_hand):
				for player in players:
					player.hand.addCard(d.deal())

			gameWinner = False
			roundNumber = 0
			lastPlayerToPlay = None
			#Game Loop
			while(not gameWinner):
				self.printNewTrick(self.loud)
				passedPlayers = 0
				[self.deal2Cards(d, player, loud) for player in players] #If a player is down to 1 card at the start of a trick, deal 2 more cards
				[player.newTrick() for player in players]
				players = self.orderPlayers(players, lastPlayerToPlay) #Player who played last goes first

				#Trick Loop
				while(passedPlayers < len(players)-1): #If at least two players haven't passed, keep playing 
					roundNumber = roundNumber + 1
					self.printRoundHeader(roundNumber, players, passedPlayers, self.loud)	

					for player in players:
						play = player.play(b, self.loud)
						if (play == "Played"):
							lastPlayerToPlay = player
						elif (play == "Won"):
							lastPlayerToPlay = player
							passedPlayers = len(players)
							gameWinner = player
							break
						elif (play == "Passed" and player.passTurn()):
							passedPlayers = passedPlayers + 1

						self.printBoard(b, self.loud)

				if(not gameWinner):						
					self.printLastPlayerToPlay(lastPlayerToPlay, self.loud)

				b = Board(number_of_players) #Wipe the board and start a new trick

			self.printGameWinner(gameWinner, roundNumber, self.loud)
			self.updateScores(players)
			self.printGameFooter(gameNumber, players, self.loud)

		self.printGrandPrixFooter(players, True)

	def printNewTrick(self, loud):
		if (loud):
			print("\n_________________\n___ NEW TRICK ___\n_________________")

	def printRoundNumber(self, roundNumber, loud):
		if (loud):
			print("\n___ ROUND", roundNumber, "___")

	def printCurrentHands(self, players, loud):
		if (loud):
			print("Current Hands:")
			[print(player.hand.list()) for player in players]

	def printPassedPlayers(self, passedPlayers, loud):
		if (loud):
			print("Passed Players:",passedPlayers)

	def printRoundHeader(self, roundNumber, players, passedPlayers, loud):
		if (loud):
			self.printRoundNumber(roundNumber, loud)
			self.printCurrentHands(players, loud)
			self.printPassedPlayers(passedPlayers, loud)
			print("----------------\n")

	def printLastPlayerToPlay(self, lastPlayerToPlay, loud):
		if (loud):
			print("lastPlayerToPlay:", lastPlayerToPlay)

	def printGameWinner(self, gameWinner, roundNumber, loud):
		if (loud):
			print(gameWinner, "won in", roundNumber, "rounds!\n")

	def printGameHeader(self, gameNumber, players, loud):
		if (loud):
			print("\n____ GAME", gameNumber, "____")
			print("Scores:")
			self.printPlayerScores(players, loud)
			print("----------------")
			print("Shuffling and dealing cards\n")

	def printGameFooter(self, gameNumber, players, loud):
		if (loud):
			print("Ending Game",gameNumber)
			self.printPlayerScores(players, loud)
			print()

	def printGrandPrixFooter(self, players, loud):
		if (loud):
			sortedScores = self.sortScores(players)
			winningPlayer = list(sortedScores)[-1]
			print(winningPlayer, "won overall with", sortedScores[winningPlayer], "points!")

			self.printPlayerScores(players, loud)


	def printPlayerScores(self, players, loud):
		if (loud):
			sortedScores = self.sortScores(players)

			for player in reversed(list(sortedScores)):
				print(player, str(sortedScores[player]).rjust(2))

	def printBoard(self, board, loud):
		if (loud):
			print(board,"\n")

	def sortScores(self, players):
		scores = {}
		for player in players:
			scores[player] = player.score

		return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

	def deal2Cards(self, d, player, loud):
		if(len(player.hand.cards) == 1 and len(d.cards)>= 2):
			if (loud):
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