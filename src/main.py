from Card import Card
from Deck import Deck

print("Starting Card Test")

c = Card(84)
print(c.value)

d = Deck()
d.shuffle()
print(d.deal().value)
