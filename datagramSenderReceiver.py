import socket
import struct

class datagramSenderReceiver:
	datagramSocket = 12345
	multicastGroup = '224.1.1.1'

	def __init__(self, sendQueue, receiveQueue):
		self.sendQueue = sendQueue
		self.receiveQueue = receiveQueue
			
	def stop(self):
		#Stop Doing Everything!! ??Not sure if we need this
		pass
			
	def receive(self):
		#look for incoming traffic, put in queue
		
		#Create a new socket (INET Sockets, Datagram Packets, UDP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#Set socket options - Prevent TIME_WAIT state inorder to reuse the address
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Bind socket to IP and Port
		sock.bind((multicastGroup, datagramSocket))
		
		#??MemberShip request packet
		mreq = struct.pack("4sl", socket.inet_aton(multicastGroup), socket.INADDR_ANY)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		#Put in incomming queue
		#buffer sizze of 10,240 for incoming data
		while(true) #Determine length of the loop
			receiveQueue.put(sock.recv(10240)) #need to look at this, going to string?
	  
	def send(self,datagramPacket):
					
		#Create a new socket (INET Sockets, Datagram Packets, UDP)			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		#Set socket options - TimeToLive??
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		#multicast send the datagramPacket
		sock.sendto(datagramPacket, (multicastGroup, datagramSocket))
		
		
		
		
		