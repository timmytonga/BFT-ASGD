import pickle
import socket

DEBUG = True
BACKLOG = 5
HEADERSIZE = 10


class Server:

	def __init__(self, port):
		"""
		Server object that can accept request at port=port
		Create a SOCK_STREAM socket and bind at localhost at port
		"""
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((socket.gethostname(), port))
		self.s.listen(BACKLOG)  # backlog = 5 by default
		self.clientsock = None
		self.clientaddress = None

	def recv(self):
		"""
		Blocking recv. Block to accept and receive.
		:return: msg to be pickled
		"""
		self.clientsock, self.clientaddress = self.s.accept()

		#if DEBUG:
			#print(f"Received message from {self.clientaddress}")

		full_msg = b''
		new_msg = True
		msglen = 0
		while True:  # receive full length
			msg = self.clientsock.recv(16)
			if new_msg:
				#print("new msg len:", msg[:HEADERSIZE])
				msglen += int(msg[:HEADERSIZE])
				new_msg = False
			full_msg += msg
			if len(full_msg) - HEADERSIZE == msglen:
				#print("full msg recvd")
				return pickle.loads(full_msg[HEADERSIZE:])

	def reply(self, msg, port):
		"""
		Reply to msg that we just received from
		:return: num_byte_sent
		"""
		
		loc = (self.clientaddress[0],port)
		# print(loc)
		return self.send(loc, msg)

	def get_socket(self):
		return self.s

	def send(self, location: (str, str), msgtosend):
		"""
		Send msg to location
		:param location: specify (address, port) to be sent to
		:param msgtosend: the msg will be pickled
		:return:
		"""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(location)
		msg = pickle.dumps(msgtosend)
		msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
		return s.send(msg)


class Client:

	def __init__(self):
		"""
		Client for communicating
		"""
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send(self, location: (str, str), msgtosend):
		"""
		Send msg to location
		:param location: specify (address, port) to be sent to
		:param msgtosend: the msg will be pickled
		:return:
		"""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(location)
		msg = pickle.dumps(msgtosend)
		msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
		return s.send(msg)
