import socket
import threading

class Server:
	def __init__(self, handlerClass, port=30100, address="127.0.0.1", maxConnections=20):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.maxConnections = maxConnections
		self.handlerClass = handlerClass
		self.maxData = 1024
		self.listning = False
		self.conections = []
		self.address = address
		self.port = port

	def getLocalIp(self):
		"""Получение локального IP адреса"""
		return socket.gethostbyname(socket.gethostname())

	def dataListner(self, conn):
		"""Базовый обработчик"""
		enable = True
		while enable:
			try:
				data = conn.recv(self.maxData)
				callback = self.handlerClass.request(data)
				conn.sendall(callback)
			except:
				enable = False

	def start(self):
		"""Начало работы сервера, прослушивание входящих соединений, команд"""
		self.socket.bind((self.address, self.port))
		self.listning = True
		self.socket.listen(self.maxConnections)

		while self.listning:
			conn, addr = self.socket.accept()

			connect = threading.Thread(target=self.dataListner, args=[conn])
			connect.start()
			self.conections.append(connect)

class handlerClass:
	def request(requestBytes):
		print(requestBytes)