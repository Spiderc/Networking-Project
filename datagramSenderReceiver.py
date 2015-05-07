import socket
import struct

class DatagramSenderReceiver:
	datagramSocket = 12345
	multicastGroup = '140.209.121.187'

	def __init__(self, receiveQueue):
		self.receiveQueue = receiveQueue
			
	def receive(self):
		x = 0
		#look for incoming traffic, put in queue
		
		#Create a new socket (INET Sockets, Datagram Packets, UDP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#Set socket options - Prevent TIME_WAIT state inorder to reuse the address
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Bind socket to IP and Port
		sock.bind((datagramSenderReceiver.multicastGroup, datagramSenderReceiver.datagramSocket))
		
		#Put in incomming queue
		#Determine Loop Size
		while x < 1000:
			receiveQueue.put(sock.recv(10240)) #need to look at this, going to string?
			##TEST CODE print sock.recv(10240)
		
	def send(self,datagramPacket):
		#Create a new socket (INET Sockets, Datagram Packets, UDP)			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		#Set socket options - TimeToLive??
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		#multicast send the datagramPacket
		sock.sendto(datagramPacket, (datagramSenderReceiver.multicastGroup, datagramSenderReceiver.datagramSocket))
		
		#TEST CODE for sending HI
		#####sock.sendto("Hi", (datagramSenderReceiver.multicastGroup, datagramSenderReceiver.datagramSocket))
		
	def sendToPeer(self, datagramPacket, peerIP):
		pass #TODO: fix this
	
		