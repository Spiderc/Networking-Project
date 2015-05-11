import id
import timeToLive

class UDPMessage:
	
	def __init__(self, id1=None, id2=None, ttl=None, message=None, byteArray=None, lastPacket = False):
		idObject = id.Id()
		ttlObject = timeToLive.TimeToLive()
		
		if byteArray == None:
			if len(id1) != idObject.idLengthInBytes:
				print "ERROR: Id1 is the wrong length"
			else:
				self.id1 = id.Id(value = id1)
				
			if len(id2) != idObject.idLengthInBytes:
				print "ERROR: Id2 is the wrong length"
			else:
				self.id2 = id.Id(value = id2)

			if len(ttl) != ttlObject.sizeInBytes:
				print "ERROR: TTL is the wrong length"
			else:
				self.ttl = timeToLive.TimeToLive(timeToLive = ttl)			
			
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
			self.id1 = byteArray[0,idObject.idLengthInBytes]
			self.id2 = byteArray[idObject.idLengthInBytes, (idObject.idLengthInBytes + idObject.idLengthInBytes)]
			self.timeToLive = byteArray[(idObject.idLengthInBytes + idObject.idLengthInBytes),((idObject.idLengthInBytes + idObject.idLengthInBytes) + ttlObject.sizeInBytes)]
			self.message = byteArray[((idObject.idLengthInBytes + idObject.idLengthInBytes) + ttlObject.sizeInBytes), len(byteArray)]
		
	def getDataGramPacket(self):
		if self.id1 != None:
			self.dataGramPacket = self.id1 + self.id2 + self.ttl + self.message
		else:
			self.dataGramPacket = byteArray
		return dataGramPacket