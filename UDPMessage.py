

class UDPMessage:
	
	def __init__(self, id1=None, id2=None, timeToLive=None, message=None, byteArray=None):
		
		if byteArray = None:
			self.id1 = id1
			self.id2 = id2
			self.ttl = timeToLive
			if message.length > 476:
				print "ERROR: Andrew sucks and your message is to long"
				pass
				#Send Error
			elif message.length < 476:
				while message.length < 476:
					#Pad Message
					message = message + "|"
					
			self.message = message
			
		else:
			self.byteArray = byteArray
		
	def getDataGramPacket(self):
	
		if self.id1 != None:
			dataGramPacket = self.id1 + self.id2 + self.ttl + self.message
			
		else:
			dataGramPacket = byteArray
	
		return dataGramPacket