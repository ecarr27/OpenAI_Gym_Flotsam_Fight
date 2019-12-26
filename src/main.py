from Card import Card
from Deck import Deck
from Hand import Hand
from Board import Board

print("Starting Test")

d = Deck()
b = Board()
h = Hand()

c3 = Card(3)
c15 = Card(15)
c72 = Card(72)

h.addCard(c3)
h.addCard(c15)
h.addCard(c72)

print(h.playCard(c3, b, 3))
print(h.playCard(c72, b, 3))
print(h.playCard(c15, b, 3))
# d.shuffle()
# print(d.deal().value)

# hands = [Hand(), Hand(), Hand(), Hand()]

# cards_per_hand = 10
# k = 0
# for i in range(cards_per_hand):
# 	for j in range(len(hands)):
# 		hands[j].addCard(d.deal())

# for hand in hands:
# 	print(hand.list())

# print(d.list())
print("Ending Test")