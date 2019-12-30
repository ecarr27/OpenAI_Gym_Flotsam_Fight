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

# print("Current Hands:")
# for player in players:
# 	player.hand.sort()
# 	print(player.hand.list())
# 	print(player.getValidMoves(b))

print(b, "\n")
c = Card(3)
b.addCardToLifeboat(c, 3)
print(b, "\n")
c = Card(4)
b.addCardToLifeboat(c, 4)
print(b, "\n")
c = Card(5)
b.addCardToLifeboat(c, 5)
print(b, "\n")
c = Card(6)
b.addCardToLifeboat(c, 6)
print(b, "\n")
c = Card(7)
b.addCardToLifeboat(c, 7)
print(b, "\n")

print("Ending Game")