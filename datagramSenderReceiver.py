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
			
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('', datagramSocket))
		mreq = struct.pack("4sl", socket.inet_aton(multicastGroup), socket.INADDR_ANY)

		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		#Put in incomming queue
		#buffer sizze of 10,240 for incoming data
		receiveQueue.put(sock.recv(10240))
	  
	def send(self,datagramPacket):
		#send packet
				
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
			sock.sendto("robot", (multicastGroup, datagramSocket))
		
		
		
		
		