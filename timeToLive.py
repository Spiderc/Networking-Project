import random
import struct

class TimeToLive:
	sizeInBytes = 4;

	def __init__(self, timeToLive=None):		
		if timeToLive == None:
			self.ttl = (random.getrandbits(4) + 10)
		else:
			self.ttl = struct.unpack(">I", timeToLive)[0]
		
	def dec(self):
		self.ttl = self.ttl - 1;
		
	def getAsBytes(self):
		return struct.pack(">I", self.ttl)
	
	def isIncorrectLength(self):
		return type(self.ttl) is not long
