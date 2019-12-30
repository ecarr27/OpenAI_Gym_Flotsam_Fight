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
players = [player for player in (Player() for i in range(number_of_players))]

print("Shuffling and dealing cards")
d.shuffle()
for i in range(number_of_cards_per_hand):
	for player in players:
		player.hand.addCard(d.deal())

print("Current Hands:")
for player in players:
	player.hand.sort()
	print(player.hand.list())

print("Player 0's Valid Moves:")
validMoves = players[0].getValidMoves(b)
print(validMoves)

print("Player 0 plays their first card:")
print(players[0].playCard(b, validMoves[0][0], validMoves[0][1][0]))
print(b)
# while(True):
# 	hasValidMove = True
# 	for player in players:
# 		validMoves = player.getValidMoves(b)
# 		player.
	

# 	break

print("Ending Game")