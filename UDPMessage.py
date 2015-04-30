import id
import timeToLive

class UDPMessage:
	
	def __init__(self, id1=None, id2=None, timeToLive=None, message=None, byteArray=None):
		idObject = id.Id()
		ttlObject = timeToLive.TimeToLive()
		print idObject.idLengthInBytes
		
		if byteArray == None:
			if len(id1.id) != idObject.idLengthInBytes:
				print "ERROR: Id1 is the wrong length"
				pass
			else:
				self.id1 = id1
				
			if len(id2.id) != idObject.idLengthInBytes:
				print "ERROR: Id2 is the wrong length"
				pass
			else:
				self.id2 = id2

			if len(timeToLive.ttl) != ttlObject.sizeInBytes:
				print "ERROR: TTL is the wrong length"
				pass
			else:
				self.ttl = timeToLive			
			
			if message.length > 476:
				print "ERROR: Message is to long"
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