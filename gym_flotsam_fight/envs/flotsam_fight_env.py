import gym
from gym import error, spaces, utils
from gym.utils import seeding

from collections import deque
from itertools import cycle

from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

class FlotsamFightEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.number_of_players = 4
		self.number_of_cards_per_hand = 10
		self.players = [Player("Albus", True), Player("Bobby"), Player("Chloe"), Player("Debra")]
		self.agent = self.players[0]

		self.d = Deck()
		self.d.shuffle()

		self.b = Board(self.number_of_players)
		for i in range(self.number_of_cards_per_hand):
				for player in self.players:
					player.hand.addCard(self.d.deal())

		[player.hand.sort() for player in self.players]

		self.gameWinner = False
		self.roundNumber = 0
		self.lastPlayerToPlay = None
  
	def step(self, action):
		#The goal of this is to get 
		if (self.gameWinner):
			return False

		self.orderPlayers(self.players, self.agent) #Put Agent to play first

		for player in self.players:
			print(player)

			play = False
			if (player.isAgent):
				play = player.play(self.b, action)
			else:
				play = player.autoPlay(self.b)

			if (play == False):
				break
			elif (play == "Played"):
				self.lastPlayerToPlay = player
			elif (play == "Won"):
				self.lastPlayerToPlay = player
				self.gameWinner = player
				self.updateScores(self.players)
				self.printPlayerScores(self.players, True)
				break
			elif (play == "Passed" and self.countPassedPlayers(self.players) >= len(self.players) - 1): #Ending trick
				[self.deal2Cards(self.d, player, True) for player in self.players] #If a player is down to 1 card at the start of a trick, deal 2 more cards
				[player.newTrick() for player in self.players]
				players = self.orderPlayers(self.players, self.lastPlayerToPlay) #Player who played last goes first
				#Need to accommodate when the order changes and the agent isn't first
				self.b = Board(self.number_of_players) #Wipe the board and start a new trick
				break

		self.roundNumber = self.roundNumber+1	

		boardState = self.b.state()
		hand = self.agent.hand.cardValues()
		competitorCardCounts = self.competitorCardCounts(self.players)

		isWon = True if self.gameWinner else False

		agentMoves = self.agent.getValidMoves(self.b)
		competitorsHands = self.competitorsHands(self.players)

		return [[boardState, hand, competitorCardCounts], isWon, 0, [agentMoves, competitorsHands]]

	def reset(self):
		self.__init__()
  
	def render(self, mode='human', close=False):
		self.printBoard(self.b)
		[print(player.hand.cardValues()) for player in (player for player in self.players) if player.isAgent]
		self.printPlayerCardCounts(self.players) 
		print(self.agent.getValidMoves(self.b))

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
						play = player.autoPlay(b, self.loud)
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

	def correctPlayerIndex(self, players, index):
		if(index >= len(players)):
			return index-len(players)
		return index
	def test(self):
		"""
			Goals:
			Loop through list of players
			If there is an agent (that is not the first in the queue), have everyone play until it is at the front of the queue
			For example, you have these players [A, B, C*, D, E, F], where C is an agent.
			First play through:
				A plays, B plays. Loop stops and C is at the front of the list
			Second play through:
				C plays, D plays, E plays, F plays, A plays, B plays
			Third play through:
				C plays, D plays, E plays, F plays, A plays, B plays

			Now consider this example: [A, B, C*, D, E*, F]
			First pass:
				A plays, B plays. Loop stops and C is at the front of the list
			Second Pass:
				C plays, D plays, Loop stops and E is at the front of the list
			Third Pass:
				E plays, F plays, A plays, B plays, Loop stops and C is at the front of the list

			Now consider this example: [A, B, C*, D, E*, F], but F will get to play twice
				I don't think I'll consider this for now.
				Lets get the loop working then come back to this
		"""
		players = deque([Player('A'), Player('B'), Player('C', True), Player('D'), Player('E', True), Player('F')])

		print("Players: [A, B, C*, D, E*, F]   (* == Agent)")
		currentPlayer = None
		startPlayer = players[0]

		for i in range(5):
			print("starting loop")
			nextPlayer = None
			for player in players:
				nextPlayerIndex = self.correctPlayerIndex(players, players.index(player)+1)
				print(player)
				if (players[nextPlayerIndex].isAgent):
					break
			players.rotate(-1*nextPlayerIndex)

	def printNewTrick(self, loud=True):
		if (loud):
			print("\n_________________\n___ NEW TRICK ___\n_________________")

	def printRoundNumber(self, roundNumber, loud=True):
		if (loud):
			print("\n___ ROUND", roundNumber, "___")

	def printCurrentHands(self, players, loud=True):
		if (loud):
			print("Current Hands:")
			[print(player.hand.list()) for player in players]

	def printPassedPlayers(self, passedPlayers, loud=True):
		if (loud):
			print("Passed Players:",passedPlayers)

	def printRoundHeader(self, roundNumber, players, passedPlayers, loud=True):
		if (loud):
			self.printRoundNumber(roundNumber, loud)
			self.printCurrentHands(players, loud)
			self.printPassedPlayers(passedPlayers, loud)
			print("----------------\n")

	def printLastPlayerToPlay(self, lastPlayerToPlay, loud=True):
		if (loud):
			print("lastPlayerToPlay:", lastPlayerToPlay)

	def printGameWinner(self, gameWinner, roundNumber, loud=True):
		if (loud):
			print(gameWinner, "won in", roundNumber, "rounds!\n")

	def printGameHeader(self, gameNumber, players, loud=True):
		if (loud):
			print("\n____ GAME", gameNumber, "____")
			print("Scores:")
			self.printPlayerScores(players, loud)
			print("----------------")
			print("Shuffling and dealing cards\n")

	def printGameFooter(self, gameNumber, players, loud=True):
		if (loud):
			print("Ending Game",gameNumber)
			self.printPlayerScores(players, loud)
			print()

	def printGrandPrixFooter(self, players, loud=True):
		if (loud):
			sortedScores = self.sortScores(players)
			winningPlayer = list(sortedScores)[-1]
			print(winningPlayer, "won overall with", sortedScores[winningPlayer], "points!")

			self.printPlayerScores(players, loud)


	def printPlayerScores(self, players, loud=True):
		if (loud):
			sortedScores = self.sortScores(players)

			for player in reversed(list(sortedScores)):
				print(player, str(sortedScores[player]).rjust(2))

	def printBoard(self, board, loud=True):
		if (loud):
			print(board,"\n")

	def printPlayerCardCounts(self, players, loud=True):
		if (loud):
			[print(player, ":", len(player.hand.cards)) for player in players]

	def competitorCardCounts(self, players):
		cardCounts = []
		for player in players:
			if (not player.isAgent):
				cardCounts.append(len(player.hand.cards))
		return cardCounts

	def competitorsHands(self, players):
		hands = []
		for player in players:
			if (not player.isAgent):
				hands.append(player.hand.cardValues())
		return hands

	def sortScores(self, players):
		scores = {}
		for player in players:
			scores[player] = player.score

		return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

	def countPassedPlayers(self, players):
		passedPlayers = 0;
		for player in players:
			if (player.isPass):
				passedPlayers = passedPlayers + 1
		return passedPlayers

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