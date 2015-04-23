

class UDPMessage:
	
	def __init__(self, id1, id2, timeToLive, message):
		self.id1 = id1
		self.id2 = id2
		self.ttl = timeToLive
		self.message = message
		
	def getDataGramPacket():
	
		dataGramPacket = self.id1 + "," + self.id2 + "," + self.ttl + "," + self.message
	
		return dataGramPacket