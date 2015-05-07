import id
import timeToLive

class UDPMessage:
	
	def __init__(self, id1=None, id2=None, timeToLive=None, message=None, byteArray=None):
		idObject = id.Id()
		ttlObject = timeToLive.TimeToLive()
		
		if byteArray == None:
			if len(id1.id) != idObject.idLengthInBytes:
				print "ERROR: Id1 is the wrong length"
			else:
				self.id1 = id1
				
			if len(id2.id) != idObject.idLengthInBytes:
				print "ERROR: Id2 is the wrong length"
			else:
				self.id2 = id2

			if len(timeToLive.ttl) != ttlObject.sizeInBytes:
				print "ERROR: TTL is the wrong length"
			else:
				self.ttl = timeToLive			
			
			if message.length > 476:
				print "ERROR: Message is to long"
				#Send Error
			elif message.length < 476:
				while message.length < 476:
					#Pad Message
					message = message + "|"
					
			self.message = message
			
		else:
			self.byteArray = byteArray #TODO: split the bytearray into the different parts of the message
		
	def getDataGramPacket(self):
		if self.id1 != None:
			self.dataGramPacket = self.id1 + self.id2 + self.ttl + self.message
		else:
			self.dataGramPacket = byteArray
		return dataGramPacket