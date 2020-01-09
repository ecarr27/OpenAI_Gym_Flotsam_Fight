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

	def __init__(self, loud=False):
		self.players = deque([Player("Albus", False, True), Player("Bobby",True), Player("Chloe", False, False), Player("Debra", False, True)])
		self.number_of_players = len(self.players)

		self.number_of_cards_per_hand = 10

		self.d = Deck()
		self.d.shuffle()

		self.b = Board(self.number_of_players)
		for i in range(self.number_of_cards_per_hand):
				for player in self.players:
					player.hand.addCard(self.d.deal())

		[player.hand.sort() for player in self.players]

		self.gameWinner = False
		self.roundNumber = 0
		self.firstPlayer = self.players[0]
		self.lastPlayerToPlay = None
		self.nextPlayerIndex = 0

		if (self.agents(self.players) and not self.players[0].isAgent): #Let all non-agent players play so the next time step() is called, an agent will be up
			self.step(loud)
	"""
		Cases: 
			Normal play: move to the next player in line
			False play: Stay on current player
			Someone Won: Stop the loop
				gameWon()
				select the winner
				Update scores
				print scores
			Normal pass: move to the next player in line
			All but 1 pass: 
				If next person (who is also the last person to play) has exactly 1 card left - move to the next player 
				If next person (who is also the last person to play) has more than 1 card left - move to the next player + new trick()
				newTrick()
					round increments
					player that starts trick is now the firstPlayer (used for round counting)
					those with 1 card, get two more
					new board

			After we decide who the next player is:
				If they are an agent: break
				If they aren't an agent: autoPlay

			
	"""
	def step(self, action=None, loud=True):
		if (self.gameWinner):
			return False
		print("Hit firstPlayer: ",self.firstPlayer, "nextPlayerIndex:", self.nextPlayerIndex)
		player = None
		for i in range(len(self.players)):
			player = self.players[i]
			print("Hit2",player)
			if (player == self.firstPlayer):
				self.roundNumber = self.roundNumber + 1

			play = player.play(self.b, action, loud)
			print("Hit3",play)
			if (play == False):
				print("Hit4")
				self.nextPlayerIndex = i
				break
			elif (play == Player.PLAY):
				print("Hit5")
				self.nextPlayerIndex = (i+1) % len(self.players)
				self.lastPlayerToPlay = player
			elif (play == Player.WON):
				print("Hit6")
				self.gameWinner = self.lastPlayerToPlay = player
				self.updateScores(self.players)
				self.printPlayerScores(self.players, loud)
				break
																						#Ending the trick if
			elif (play == Player.PASS and 												#This player passes
					self.countPassedPlayers(self.players) >= len(self.players)-1 and 	#And all but one player has passed
					len(self.players[(i+1)%len(self.players)].hand.cards) > 1):		 	#And the next player has more than 1 card left
				print("Hit7")
				[self.deal2Cards(self.d, player, loud) for player in self.players] 		#If a player is down to 1 card at the start of a trick, deal them 2 more cards
				[player.newTrick() for player in self.players]
				self.players = self.orderPlayers(self.players, self.lastPlayerToPlay) 	#Player who played last goes first next round
				self.firstPlayer = self.players[0]
				self.nextPlayerIndex = 0
				self.b = Board(self.number_of_players) 									#Wipe the board and start a new trick
				self.printNewTrick(loud)
				if (not self.firstPlayer.isAgent):										#Need to fast forward to the next agent
					print("Hit10")
					self.step(action, loud) 
				break
			elif(play == Player.PASS):
				print("Hit8")
				self.nextPlayerIndex = (i+1) % len(self.players)

			if (self.players[self.nextPlayerIndex].isAgent):
				break	

		self.players.rotate(-1*self.nextPlayerIndex)
		print("Hit9")
		#Observations
		boardState = self.b.state()
		hand = player.hand.cardValues()
		competitorCardCounts = self.competitorCardCounts(self.players, player)

		#Reward
		reward = 0

		#isDone
		isWon = True if self.gameWinner else False

		#Additional Information 
		agentMoves = player.getValidMoves(self.b)
		competitorsHands = self.competitorsHands(self.players, player)

		return [[boardState, hand, competitorCardCounts, self.roundNumber], reward, isWon, [agentMoves, competitorsHands]]

	def reset(self):
		self.__init__()
  
	def render(self, mode='human', close=False):
		self.printRoundHeader(self.roundNumber, self.players, self.passedPlayers(self.players), True)
		if (self.gameWinner):
			self.printGameWinner(self.gameWinner, self.roundNumber, True)
			self.printPlayerScores(self.players)
		else:
			self.printBoard(self.b)
			[print(player, ":", player.getValidMoves(self.b)) for player in (player for player in self.players) if player.isAgent]

	def correctPlayerIndex(self, players, index):
		return index % len(self.players)

	def test(self):
		"""
		This doesn't work.
		A, B*, C, D

		A Pass, B* Pass, C Plays, D Pass
		What should happen:
			A Pass, pause on B

		What actually happens:
			C Plays, D Pass, A Pass, pause on A

		Need a way to just play the non agents

		I'm going to switch to a while loop. 
		Instead of iterating through the players, I'm always going to move the list and pick the first player
		This way, even if the loop breaks (which is expected often) the right player will be first next
		"""
		players = deque([Player('A'), Player('B'), Player('C', True), Player('D'), Player('E', True), Player('F')])

		print("Players: [A, B, C*, D, E*, F]   (* == Agent)")

		for i in range(3):
			print("starting loop")
			while (True):
				player = players[0]
				print(player, "plays")
				players.rotate(-1)		
				print("Next player:", players[0])
				if (players[0].isAgent):
					break







		# currentPlayer = None
		# startPlayer = players[0]

		# for i in range(5):
		# 	print("starting loop")
		# 	nextPlayer = None
		# 	for player in players:
		# 		nextPlayerIndex = self.correctPlayerIndex(players, players.index(player)+1)
		# 		print(player)
		# 		if (players[nextPlayerIndex].isAgent):
		# 			break
		# 	players.rotate(-1*nextPlayerIndex)
		# return self.agents(self.players)

	def printNewTrick(self, loud=True):
		if (loud):
			print("\n_________________\n___ NEW TRICK ___\n_________________")

	def printRoundNumber(self, roundNumber, loud=True):
		if (loud):
			print("\n___ ROUND", roundNumber, "___")

	def printCurrentHands(self, players, loud=True):
		if (loud):
			print("Current Hands:")
			[print(player, "(", len(player.hand.cards), ")", ":", player.hand.list()) for player in players]

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

	def competitorCardCounts(self, players, targetPlayer):
		cardCounts = []
		for player in players:
			if (player != targetPlayer):
				cardCounts.append(len(player.hand.cards))
		return cardCounts

	def competitorsHands(self, players, targetPlayer):
		hands = []
		for player in players:
			if (player != targetPlayer):
				hands.append(player.hand.cardValues())
		return hands

	def sortScores(self, players):
		scores = {}
		for player in players:
			scores[player] = player.score

		return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

	def passedPlayers(self, players):
		return [player.name for player in (player for player in players) if player.isPass]

	def agents(self, players):
		return [player for player in (player for player in players) if player.isAgent]

	def countPassedPlayers(self, players):
		return len(self.passedPlayers(players))

	def deal2Cards(self, d, player, loud):
		if(len(player.hand.cards) == 1 and len(d.cards)>= 2):
			if (loud):
				print("Giving 2 extra cards to", player)
			player.hand.addCard(d.deal())
			player.hand.addCard(d.deal())

	def orderPlayers(self, players, lastPlayerToPlay): #Makes the last player to play to be the first player 
		if(not lastPlayerToPlay):
			return players 

		indexOfLastPlayerToPlay = players.index(lastPlayerToPlay);
		players.rotate(indexOfLastPlayerToPlay*-1)
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