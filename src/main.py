from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board
from Player import Player

print("Starting Game")

d = Deck()
b = Board()

players = [player for player in (Player() for i in range(4))]
number_of_cards_per_hand = 10

print("Shuffling and dealing cards")
d.shuffle()
for i in range(number_of_cards_per_hand):
	for player in players:
		player.hand.addCard(d.deal())

print("Current Hands:")
for player in players:
	player.hand.sort()
	print(player.hand.list())

print(b)
print(players[0].getValidMoves(b))
print("Ending Game")