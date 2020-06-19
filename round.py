class Round:

	def __init__(self, number, lastRound=None):
		self.number = number
		self.leaders = list()
		self.highest = 0
		if lastRound == None:
			self.cards = dict()
			self.points = 0
		else:
			self.cards = lastRound.cards
			self.points = lastRound.points

	def update(self, player, card):
		if player in self.cards:
			self.cards[player].append(card)
		else:
			self.cards[player] = list([card])
		self.points += card
		if self.leaders == []:
			self.leaders.append(player)
			self.highest = card
		else:
			if card == self.highest:
				self.leaders.append(player)
			elif card > self.highest:
				self.leaders = list()
				self.leaders.append(player)
				self.highest = card

	def status(self):
		print(self.cards)
		print("Total points:", self.points)