import socket
import struct

class DatagramSenderReceiver:

	def __init__(self, receiveQueue, multicastQueue):
		self.receiveQueue = receiveQueue
		self.multicastQueue = multicastQueue
			
	def receive(self, ipAddress, datagramSocket):
		x = 0		
		#Create a new socket (INET Sockets, Datagram Packets, UDP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#Set socket options - Prevent TIME_WAIT state inorder to reuse the address
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Bind socket to IP and Port
		sock.bind((ipAddress, datagramSocket))
				
		#Put in incoming queue
		while x < 1000:
			DatagramSenderReceiver.receiveQueue.put(sock.recv(10240)) 
			##TEST CODE print sock.recv(10240)
			x = x - 1;
		
	def send(self, ipAddress, datagramSocket, datagramPacket):
		#Create a new socket (INET Sockets, Datagram Packets, UDP)			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		#Set socket options - TimeToLive?? - TEST TO MAKE SURE IT CAN BE REMOVED
		##sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		#multicast send the datagramPacket
		sock.sendto(datagramPacket, (ipAddress, datagramSocket))
		
		#TEST CODE for sending HI
		#####sock.sendto("Hi", (self.multicastGroup, self.datagramSocket))	