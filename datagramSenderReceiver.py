import socket
import struct

class datagramSenderReceiver:
	datagramSocket = 12345
	multicastGroup = '140.209.121.187'

	def __init__(self, sendQueue, receiveQueue):
		self.sendQueue = sendQueue
		self.receiveQueue = receiveQueue
			
	def stop(self):
		#Stop Doing Everything!! ??Not sure if we need this
		pass
			
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
		#receiveQueue.put(sock.recv(10240)) #need to look at this, going to string?
		
		#buffer sizze of 10,240 for incoming data
		#while(true) #Determine length of the loop
		while x < 10000:
			print sock.recv(10240)
			x = x + 1
		
		
	  
	def send(self,datagramPacket):
					
		#Create a new socket (INET Sockets, Datagram Packets, UDP)			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		#Set socket options - TimeToLive??
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		#multicast send the datagramPacket
		     ###sock.sendto(datagramPacket, (datagramSenderReceiver.multicastGroup, datagramSenderReceiver.datagramSocket))
		
		#TEST CODE for sending HI
		sock.sendto("Hi", (datagramSenderReceiver.multicastGroup, datagramSenderReceiver.datagramSocket))
		
		
		
		
		