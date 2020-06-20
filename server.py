import socket
from _thread import *
import sys
from time import sleep

server = "127.0.0.1"
port = 7777
max_clients = 4
num_clients = 0

if len(sys.argv) == 2:
	max_clients = int(sys.argv[1])

if len(sys.argv) == 3:
	max_clients = int(sys.argv[1])
	server = sys.argv[2]

if len(sys.argv) == 4:
	max_clients = int(sys.argv[1])
	server = sys.argv[2]
	port = int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

s.listen(2)
print("Waiting...")

card_array = dict()
num_ready = 0

def threaded_client(conn, id):
	global num_clients
	global card_array
	global num_ready
	conn.send(str.encode("%d,%d" %(id, num_clients)))
	print("Received:", conn.recv(2048).decode("utf-8"))
	num_ready += 1
	reply = ""
	while num_ready != num_clients:
		continue
	conn.send(str.encode("ACK"))
	while True:
		try:
			data = conn.recv(2048).decode("utf-8")
			data = data.split(",")
			card_array[data[0]] = data[1]

			while not all(card_array.values()):
				continue

			status = ""
			for player in card_array:
				if int(player) != id:
					status += player+","+card_array[player]+","
			conn.send(str.encode(status))
			sleep(1)
			for i in range(num_clients):
				card_array[str(i)] = ""
		except:
			break

	print("Lost connection.")
	conn.close()
	num_clients -= 1

connections = []
while num_clients < max_clients:
	conn, addr = s.accept()
	print("Connected:", addr)
	num_clients += 1
	connections.append(conn)

for i in range(num_clients):
	card_array[str(i)] = ""
	start_new_thread(threaded_client, (connections[i], i))

input()