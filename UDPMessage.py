import id
import timeToLive

class UDPMessage:
	
	def __init__(self, id1=None, id2=None, ttl=None, message=None, byteArray=None, lastPacket = False):
		idObject = id.Id()
		ttlObject = timeToLive.TimeToLive()
		
		if byteArray == None:
			if id1.isIncorrectLength():
				print "ERROR: Id1 is the wrong length"
			else:
				self.id1 = id1
				
			if id2.isIncorrectLength():
				print "ERROR: Id2 is the wrong length"
			else:
				self.id2 = id2

			if ttl.isIncorrectLength():
				print "ERROR: TTL is the wrong length"
			else:
				self.ttl = ttl
			
			if len(message) > 476:
				print "ERROR: Message is to long"
				#Send Error
			elif len(message) < 476 and lastPacket == False:
				while len(message) < 476:
					#Pad Message
					message = message + "|"
					
			self.message = message
			
		else:
			self.byteArray = byteArray
			self.id1 = id.Id(value = bytearray(byteArray[:idObject.idLengthInBytes]))
			self.id2 = id.Id(value = bytearray(byteArray[idObject.idLengthInBytes: idObject.idLengthInBytes*2]))
			self.ttl = timeToLive.TimeToLive(timeToLive = bytearray(byteArray[idObject.idLengthInBytes*2:(idObject.idLengthInBytes*2 + ttlObject.sizeInBytes)]))
			self.message = byteArray[(idObject.idLengthInBytes*2 + ttlObject.sizeInBytes):]
		
	def getDataGramPacket(self):
		if self.id1 != None:
			print self.id1.getAsHex()
			self.dataGramPacket = self.id1.getAsBytes() + self.id2.getAsBytes() + self.ttl.getAsBytes() + bytearray(self.message)
		else:
			self.dataGramPacket = self.byteArray
		return self.dataGramPacket
