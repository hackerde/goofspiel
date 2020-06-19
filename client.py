import socket

class Client:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "127.0.0.1"
		self.port = 7777
		self.addr = (self.server, self.port)
		self.id, self.num_clients = self.parse(self.connect())
		self.card = ""

	def parse(self,str):
		str = str.split(",")
		return int(str[0]), int(str[1])

	def getID(self):
		return int(self.id)

	def getPlayers(self):
		return int(self.num_clients)

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode("utf-8")
		except:
			pass

	def send(self, data=""):
		try:
			if data:
				self.client.send(str.encode(data))
			else:
				self.client.send(str.encode(self.card))
		except socket.error as e:
			print(e)

	def recv(self):
		try:
			return self.client.recv(2048).decode("utf-8")
		except socket.error as e:
			print(e)

