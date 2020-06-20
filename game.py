import random
import pygame
import sys
from time import sleep

from client import Client
from button import Button
from card import Card
from round import Round
from player import Player

def redrawWindow(cards, table, win):
	
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
	roundWinner.draw(win)
	for score in score_board.values():
		score.draw(win, (0,0,0))
	pygame.display.update()

def play_game(Players, main_player):

	all_rounds = []
	for i in range(1, 14):
		table = []
		if all_rounds == []:
			current_round = Round(i)
			if not computer:
				roundWinner.score = ""
		else:
			if len(all_rounds[-1].leaders) > 1:
				current_round = Round(i, all_rounds[-1])
			else:
				current_round = Round(i)
				if not computer:
					roundWinner.score = ""
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
				redrawWindow(main_player.hand.values(), table, win)
				c.send("%d,%d" %(main_player.id, played.value))
				info = c.recv().split(",")
				for i in range(len(Players)-1):
					moves[int(info[2*i])] = int(info[2*i+1])

			elif player.type == 2:
				played = player.play(random.choice(list(player.getCards())))
				# table.append(played)
				c.send("%d,%d" %(main_player.id, played))
				info = c.recv().split(",")
				for i in range(len(Players)-1):
					moves[int(info[2*i])] = int(info[2*i+1])
			else:
				played = player.play(moves[player.id])
				if not computer:
					table.append(played)
				# print("Player %d played: %d" %(player.id, played))
			if not computer:
				redrawWindow(main_player.hand.values(), table, win)
				current_round.update(player.id, played.value)
			else:
				current_round.update(player.id, played)
		all_rounds.append(current_round)
		current_round.status()
		if len(current_round.leaders) == 1:
			print("Round won by: Player %d" %current_round.leaders[0])
			if not computer:
				if current_round.leaders[0] == main_player_id:
					roundWinner.score = "You"
				else:
					roundWinner.score = "Player %d" %current_round.leaders[0]
		else:
			if not computer:
				roundWinner.score = "Tie"
		for player in Players:
			player.update(current_round)
			if not computer:
				score_board[player.id].score = str(player.points)
		if not computer:
			redrawWindow(main_player.hand.values(), table, win)
		sleep(2)

def print_result(Players):

	max_score = 0
	for player in Players:
		print("Player %d: %d" %(player.id, player.points))
		if player.points > max_score:
			max_score = player.points

	print("The winner is: ", end="")
	for player in Players:
		if player.points == max_score:
			print("Player %d" %player.id, end=" ")
	print()

# main

server = "127.0.0.1"
port = 7777
computer = False

if len(sys.argv) == 2:
	if sys.argv[1] == '-c' or sys.argv[1] == '--comp':
		computer = True
	elif sys.argv[1] == '-p' or sys.argv[1] == '--player':
		computer = False

if len(sys.argv) == 3:
	if sys.argv[1] == '-c' or sys.argv[1] == '--comp':
		computer = True
	elif sys.argv[1] == '-p' or sys.argv[1] == '--player':
		computer = False
	server = sys.argv[2]

if len(sys.argv) == 4:
	if sys.argv[1] == '-c' or sys.argv[1] == '--comp':
		computer = True
	elif sys.argv[1] == '-p' or sys.argv[1] == '--player':
		computer = False
	server = sys.argv[2]
	port = int(sys.argv[3])

if not computer:
	width = 1280
	height = 800
	pygame.init()
	win = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Goofspiel")	

	playButton = Button((220,220,220), 600, 700, 80, 60, 'Play')
	roundWinner = Button((255,255,255), width//2-75, 20, 150, 50, 'Winner:')

	score_board = dict()

c = Client(server, port)
main_player_id = c.getID()
num_players = c.getPlayers()
players = []

for i in range(num_players):
	if i == main_player_id:
		if computer:
			main_player = Player(i,2,comp=True)
		else:
			main_player = Player(i)
		players.insert(0,main_player)
	else:
		if computer:
			players.append(Player(i, 1, comp=True))
		else:
			players.append(Player(i, 1, comp=False))

if not computer:
	for i in range(len(players)):
		if players[i].id == main_player_id:
			score = Button((255,255,255), 20, 20+50*i, 150, 50, "Score:", "0")
		else:
			score = Button((255,255,255), 20, 20+50*i, 150, 50, "Player %d:" %players[i].id, "0")
		score_board[players[i].id] = score

c.send("%d: Ready to start." %main_player_id)

play_game(players, main_player)
print_result(players)

if not computer:
	pygame.quit()

exit()