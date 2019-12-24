from Card import Card

class Deck:
	def __init__(self):
		self.cards = []
		numbers = [2, 3, 10, 11, 15]
		self.cards = [card for card in (Card(number) for number in numbers) if card.valid]

		# for i in range(2, 98):
		# 	self.deck.append(Card(i))

	def __str__(self):
		return self.deck[0]


