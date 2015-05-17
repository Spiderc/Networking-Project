import socket
import struct

class DatagramSenderReceiver:

	def __init__(self, receiveQueue):
		self.receiveQueue = receiveQueue
		self.running = True
			
	def receive(self):
		sockName = 0		
		#Create a new socket (INET Sockets, Datagram Packets, UDP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#Set socket options - Prevent TIME_WAIT state inorder to reuse the address
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Bind socket to IP and Port
		sock.bind(("10.20.74.0", 12345))
		#Put in incoming queue
<<<<<<< HEAD
		while True:
			self.receiveQueue.put(sock.recv(10240))
=======
		while self.running:
			self.receiveQueue.put(sock.recv(10240))
			
	def stopThread(self):
		self.running = False
>>>>>>> origin/master
		
	def send(self, ipAddress, datagramSocket, datagramPacket):
		#Create a new socket (INET Sockets, Datagram Packets, UDP)			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		#Set socket options - TimeToLive?? - TEST TO MAKE SURE IT CAN BE REMOVED
		##sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		#multicast send the datagramPacket
		sock.sendto(datagramPacket, (ipAddress, datagramSocket))
