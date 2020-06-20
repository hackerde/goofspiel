from card import Card
from round import Round

class Player:

	def __init__(self, id, type=0, comp=False):
		self.id = id
		self.type = type
		self.allCards = list(range(1,14))
		self.hand = {}
		self.points = 0
		self.memory = dict()
		x = 30
		y = 550
		for i in range(1,14):
			if not comp:
				c = Card(x,y,i,"images/Heart_%d.png" %i)
				x += c.rect.width+1
				self.hand[i] = c
			else:
				self.hand[i] = i

	def play(self, card=0):
		if card in self.hand.keys():
			# del self.hand[card]
			return self.hand.pop(card)
		else:
			print("Cannot play %d. Card not in hand!" %card)
			return -1

	def getCards(self):
		return self.hand.keys()

	def update(self, round):
		if len(round.leaders) == 1:
			if round.leaders[0] == self.id:
				self.points += round.points
			for player in round.cards:
				if player not in self.memory:
					self.memory[player] = list([round.cards[player]])
				else:
					self.memory[player].append(round.cards[player])