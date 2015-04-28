

class UDPMessage:
	
	def __init__(self, id1, id2, timeToLive, message):
		self.id1 = id1
		self.id2 = id2
		self.ttl = timeToLive
		if message.length > 476:
			#WRITE ERROR MESSAGE
		elif message.length < 476:
			#PADD THE END OF THE MESSAGE TO 476
		self.message = message
		
	def getDataGramPacket(self):
	
		dataGramPacket = self.id1 + self.id2 + self.ttl + self.message
	
		return dataGramPacket