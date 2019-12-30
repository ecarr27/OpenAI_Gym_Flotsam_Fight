from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

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
while(not gameWinner):
	passedPlayers = 0
	while(passedPlayers < len(players)-1):
		roundNumber = roundNumber + 1	
		print("\n___ ROUND", roundNumber, "___\n")
		print("Current Hands:")
		for player in players:
			player.hand.sort()
			print(player, ":", player.hand.list())

		print("\n")

		passedPlayers = 0
		for player in players:
			validMoves = player.getValidMoves(b)
			print(player,":",validMoves)
			if (len(validMoves)):
				print("Playing this card:", validMoves[0][0], validMoves[0][1][0])
				print(player.playCard(b, validMoves[0][0], validMoves[0][1][0]))
				if (len(player.hand.cards) == 0):
					gameWinner = player
					passedPlayers = len(players)
			else:
				print(player, "passes")
				if (player.isPass):
					passedPlayers = passedPlayers + 1
					
			print(b)

	b = Board(number_of_players)
print(gameWinner, "won in", roundNumber, "rounds!")
print("Ending Game")