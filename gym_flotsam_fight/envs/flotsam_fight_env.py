import gym
from gym import error, spaces, utils
from gym.utils import seeding

from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

class FlotsamFightEnv(gym.Env):
	metadata = {'render.modes': ['human']}
	cardsPerHandByPlayerCount = {2:10, 3:10, 4:10, 5:10, 6:8}
	playerNames = ["Albus", "Beaux", "Coral", "Daria", "Edgar", "Fiona"]

	def __init__(self, numberOfPlayers=4, numberOfAgents=1):
		if (not numberOfPlayers in self.cardsPerHandByPlayerCount):
			print("Please use a number of players between 2-6 (inclusive)")
			return None

		self.numberOfPlayers = numberOfPlayers
		self.numberOfAgents = numberOfAgents

		self.numberOfCardsPerHand = self.cardsPerHandByPlayerCount[self.numberOfPlayers]
		self.players = self.pickPlayers(numberOfPlayers, numberOfAgents)
		# self.numberOfPlayers = 6
		# self.numberOfCardsPerHand = self.cardsPerHandByPlayerCount[self.numberOfPlayers]
		# self.players = [Player("Albus"), Player("Beaux"), Player("Cairo"), Player("Daria"), Player("Edgar"), Player("Fiona")]

		self.deck = Deck()
		self.deck.shuffle()

		self.board = Board(self.numberOfPlayers)

		for i in range(self.numberOfCardsPerHand):
			for player in self.players:
				player.hand.addCard(self.deck.deal())

		[player.hand.sort() for player in self.players]

		self.gameWinner = False
		self.roundNumber = 1
		self.i = 0
		self.roundLeader = self.players[self.i]
		self.passCount = 0
		self.lastAgentToStep = None
		self.lastAgentsPlay = None

		if (self.agents(self.players) and not self.players[0].isAgent): 	#Let all non-agent players play so the next time step() is called, an agent will be up
			self.step(loud)
	"""
		Cases: 
			Normal play: 
				Move to the next player in line
			False play: 
				Stay on current player
			Pass: 
				All but 1 pass: 
					If next person (who is also the last person to play) has more than 1 card left - move to the next player + new trick()
					If next person (who is also the last person to play) has exactly 1 card left - move to the next player 
				All players have passed:
					The last person must have 1 card left. Give them a chance to play it. Increment the index in case they don't win.
				Normal pass:
					Move to the next player in line		
			Someone Won: 
				Stop the loop

			After we decide who the next player is:
				If they are an agent: break
				If they aren't an agent: continue
	"""
	def step(self, action=None, loud=False):
		while (not self.gameWinner):
			if (self.i == self.getIndexOfPlayer(self.roundLeader)):
				self.render(loud)
			player = self.players[self.i]
			self.roundNumber = self.roundNumber + 1 if player == self.roundLeader else self.roundNumber

			play = player.play(self.board, action, loud)
			if (player.isAgent): 											#If player is agent, record the results of the play to calculate the reward later
				self.lastAgentToStep = player 
				self.lastAgentsPlay = play

			if (play == Player.PLAY): 										#If the play was valid and nothing special happens
				self.passCount = 0 
				self.incrementIndex()   									#Continue on to the next player
			elif (play == Player.INVALID): 									#If the action was invalid
				#self.i = self.i 											#Do nothing. Keep the index the same so the current player goes again
				break 
			elif (play == Player.PASS):
				self.passCount = self.passCount + 1
				if (self.passCount == (len(self.players)-1) and 			#If everyone but one player has passed
					len(self.players[self.nextIndex()].hand.cards) > 1):   	#And that person has more than 1 card in their hand
					self.newTrick(loud)									 	#Call a new trick
				elif (self.passCount == (len(self.players)-1) and 			#If everyone but one player has passed
					len(self.players[self.nextIndex()].hand.cards) == 1):  	#And that person has exactly 1 card in their hand
					self.incrementIndex() 								  	#Let them play
					self.printExtraPlayExplaination(self.players[self.i], loud)
				elif (self.passCount == (len(self.players))):
					self.printExtraPlayFailDisappointment(player, loud)
					self.newTrick(loud)
				else: 													  	#If not everyone has passed
					self.incrementIndex()									#Let the next player play
			elif (play == Player.WON):
				self.passCount = 0
				self.gameWon(player, loud)
				break

			if (self.players[self.i].isAgent):
				break

		return self.getStepReturns(self.lastAgentToStep, self.lastAgentsPlay)

	def reset(self, numberOfPlayers=None, numberOfAgents=None):
		numberOfPlayers = numberOfPlayers if numberOfPlayers != None else self.numberOfPlayers
		numberOfAgents = numberOfAgents if numberOfAgents != None else self.numberOfAgents

		self.__init__(numberOfPlayers, numberOfAgents)

		if (self.agents(self.players) and self.players[self.i].isAgent):
			return self.getInitReturns(self.players[self.i])
  
	def render(self, loud=False):
		self.printRoundHeader(self.roundNumber, self.players, self.i, self.passedPlayers(self.players), loud)
		if (self.gameWinner):
			self.printGameWinner(self.gameWinner, self.roundNumber, loud)
			self.printPlayerScores(self.players)
		else:
			self.printBoard(self.board, loud)
			[print(player, ":", player.getValidMoves(self.board)) for player in (player for player in self.players) if player.isAgent]
			pass

	def pickPlayers(self, numberOfPlayers, numberOfAgents):
		players = []
		for i in range(numberOfPlayers):
			isAgent = numberOfAgents > 0
			players.append(Player(self.playerNames[i], isAgent))
			numberOfAgents = numberOfAgents - 1
		return players


	def newTrick(self, loud):
		self.printNewTrick(loud)
		[self.deal2Cards(self.deck, player, loud) for player in self.players] 	#If a player is down to 1 card at the start of a trick, deal them 2 more cards
		[player.newTrick() for player in self.players]
		self.board = Board(self.numberOfPlayers) 								#Wipe the board and start a new trick

		self.incrementIndex()
		self.printRoundLeader(loud)

	def gameWon(self, player, loud):
		self.gameWinner = player
		self.updateScores(self.players)
		if (loud):
			print(); print(self.gameWinner, "won in", self.roundNumber-1,"rounds!!")
		self.printPlayerScores(self.players, loud)

	def getInitReturns(self, player):
		#Observations
		boardState = self.board.state()
		hand = player.hand.cardValues()
		competitorCardCounts = self.competitorCardCounts(self.players, player)

		#Reward
		reward = 0

		#isDone
		isWon = True if self.gameWinner else False

		#Additional Information 
		agentMoves = player.getValidMoves(self.board)
		competitorsHands = self.competitorsHands(self.players, player)

		return [[boardState, hand, competitorCardCounts, self.roundNumber], reward, isWon, [agentMoves, competitorsHands]]

	def getStepReturns(self, player, play, reward=0):
		if (self.gameWinner and not player):
			return self.getPlayerScores(self.players)
		elif (not self.gameWinner and not player):
			return False

		#Observations
		boardState = self.board.state()
		hand = player.hand.cardValues()
		competitorCardCounts = self.competitorCardCounts(self.players, player)

		#Reward
		reward = self.calculateReward(player, play)

		#isDone
		isWon = True if self.gameWinner else False

		#Additional Information 
		agentMoves = player.getValidMoves(self.board)
		competitorsHands = self.competitorsHands(self.players, player)

		return [[boardState, hand, competitorCardCounts, self.roundNumber], reward, isWon, [agentMoves, competitorsHands]]

	def calculateReward(self, player, play):
		if (play == Player.PLAY):
			return 0
		elif (play == Player.INVALID):
			return -1
		elif (play == Player.PASS):
			return -10
		elif (play == Player.WON):
			return 50
		else:
			print("Something when wrong with the rewards calculation. Play:", play)
			return 0

	def nextIndex(self, players=None, i=None):
		players = self.players if players == None else players
		i = self.i if i == None else i
		return (i+1) % len(players)

	def incrementIndex(self, players=None, i=None):
		players = self.players if players == None else players
		i = self.i if i == None else i
		self.i = self.nextIndex(players, i)
		return True			

	def getIndexOfPlayer(self, targetPlayer, players=None):
		players = self.players if players == None else players
		return players.index(targetPlayer)

	def correctPlayerIndex(self, players, index):
		return index % len(self.players)

	def test(self):
		print(self.board.validLifeboats)
		print(self.board.usedLifeboats)

	def printNewTrick(self, loud=True):
		if (loud):
			print("\n_________________\n___ NEW TRICK ___\n_________________")

	def printRoundNumber(self, roundNumber, loud=True):
		if (loud):
			print("\n___ ROUND", roundNumber, "___")

	def printCurrentHands(self, players, index, loud=True):
		if (loud):
			print("Current Hands:")

			for count in range(len(players)):
				player = players[index]
				print(player, "(", len(player.hand.cards), ")", ":", player.hand.list())
				index = self.nextIndex(players, index)

	def printPassedPlayers(self, passedPlayers, loud=True):
		if (loud):
			print("Passed Players:",passedPlayers)

	def printRoundHeader(self, roundNumber, players, index, passedPlayers, loud=True):
		if (loud):
			self.printRoundNumber(roundNumber, loud)
			self.printCurrentHands(players, index, loud)
			self.printPassedPlayers(passedPlayers, loud)
			print("----------------\n")

	def printRoundLeader(self, loud=True):
		if (self.roundLeader != self.players[self.i] and loud):
			self.roundLeader = self.players[self.i]
			print("New Trick - Round Leader:", self.roundLeader)
		elif (self.roundLeader != self.players[self.i] and not loud):
			self.roundLeader = self.players[self.i]
		elif (loud):
			print("New Trick -", self.roundLeader, "remains the Round Leader") #Round header will print automatically at the top of the step loop
		else:
			pass

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

	def getPlayerScores(self, players):
		sortedScores = self.sortScores(players)
		scores = {}
		for player in reversed(list(sortedScores)):
			scores[player.name] = sortedScores[player]
		return scores

	def printBoard(self, board, loud=True):
		if (loud):
			print(board,"\n")

	def printPlayerCardCounts(self, players, loud=True):
		if (loud):
			[print(player, ":", len(player.hand.cards)) for player in players]

	def printExtraPlayExplaination(self, player, loud=True):
		if (loud):
			print("Everyone has passed but",player, "has one more card left. They have a chance to close out!")

	def printExtraPlayFailDisappointment(self, player, loud=True):
		if (loud):
			print(player, "wasn't able to finish the job!")

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

	def passedPlayers(self, players=None):
		players = self.players if players == None else players
		return [player.name for player in (player for player in players) if player.isPass]

	def agents(self, players):
		return [player for player in (player for player in players) if player.isAgent]

	def countPassedPlayers(self, players=None):
		players = self.players if players == None else players
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
		if (len(list(sortedScores)) > 1):
			highestOfHighestCards.addScore(-1)