import random
import pygame
from time import sleep

from client import Client
from button import Button
from card import Card
from round import Round
from player import Player

pygame.init()
width = 1280
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Goofspiel")

playButton = Button((220,220,220), 600, 700, 80, 60, 'Play')

def redrawWindow(cards, table, win, turn=True):

	win.fill((255,255,255))
	for card in cards:
		card.draw(win)
	for i in range(len(table)):
		card = table[i]
		card.x = width//2-43
		card.y = height//2-30
			
		if i == 1:
			card.x -= 130
			card.y -= 100

		if i == 2:
			card.y -= 200

		if i == 3:
			card.x += 130
			card.y -= 100

		card.rect.topleft = (card.x, card.y)
		card.draw(win)
	playButton.draw(win, (0,0,0))
	pygame.display.update()

def play_game(Players, main_player):

	all_rounds = []
	for i in range(1, 14):
		table = []
		if all_rounds == []:
			current_round = Round(i)
		else:
			if len(all_rounds[-1].leaders) > 1:
				current_round = Round(i, all_rounds[-1])
			else:
				current_round = Round(i)
		moves = dict()
		for player in Players:
			if player.type == 0:
				print("Player %d" %player.id)
				print(player.getCards())
				played = -1

				while played == -1:
					for event in pygame.event.get():
						pos = pygame.mouse.get_pos()
						if event.type ==  pygame.QUIT:
							played = -2
							pygame.quit()
							exit()

						if event.type == pygame.MOUSEBUTTONDOWN:
							if playButton.isOver(pos):
								played = None
								for card in player.hand.values():
									if card.selected:
										played = card.value
										continue
								if played:
									table.append(player.hand[played])
								else:
									played = -1
									# del player.hand[played]
									
							for card in player.hand.values():
								if card.isOver(pos):
									card.selected = True
								else:
									card.selected = False
					# choice = (int)(input("Enter Move: "))
					# played = player.play(choice)

					redrawWindow(main_player.hand.values(), table, win)
				
				played = player.play(played)
				c.send("%d,%d" %(main_player.id, played.value))
				info = c.recv().split(",")
				for i in range(len(Players)-1):
					moves[int(info[2*i])] = int(info[2*i+1])

			else:
				played = player.play(moves[player.id])
				table.append(played)
				# print("Player %d played: %d" %(player.id, played))
			redrawWindow(main_player.hand.values(), table, win, False)
			current_round.update(player.id, played.value)
		all_rounds.append(current_round)
		current_round.status()
		if len(current_round.leaders) == 1:
			print("Round won by: Player %d" %current_round.leaders[0])
		for player in Players:
			player.update(current_round)
		sleep(2)

def print_result(Players):

	max_score = 0
	for player in Players:
		print("Player %d: %d" %(player.id, player.points))
		if player.points > max_score:
			max_score = player.points

	print("The winner(s) is(are): ", end="")
	for player in Players:
		if player.points == max_score:
			print("Player %d" %player.id, end=" ")
	print()

# main

c = Client()
main_player_id = c.getID()
num_players = c.getPlayers()
players = []

for i in range(num_players):
	if i == main_player_id:
		main_player = Player(i)
		players.insert(0,main_player)
	else:
		players.append(Player(i, 1))


c.send("%d: Created all players." %main_player_id)

#p2 = Player(2, 1)
# p3 = Player(3, 1)
# p4 = Player(4, 1)
# main_player = p1
# players = [main_player, p2, p3, p4]
play_game(players, main_player)
print_result(players)
pygame.quit()
exit()