import os
import Queue

class Id:
	idLengthInBytes = 16
	maxQueueLength = 10000
	idQueue = Queue.Queue(maxQueueLength)
	zeroId = bytearray(idLengthInBytes)

	def __init__(self):
		self.id = bytearray(os.urandom(Id.idLengthInBytes))

	def idFactory(self):
		if Id.idQueue.qsize() < Id.maxQueueLength:
			Id.idQueue.put(os.urandom(Id.idLengthInBytes))
		
	def generateId(self):
		if Id.idQueue.empty():
			self.id = os.urandom(Id.idLengthInBytes)
		else:
			self.id = Id.idQueue.get();

	def setIdLength(self,lengthInBytes):
		if lengthInBytes != Id.idLengthInBytes:
			Id.idLengthInBytes = lengthInBytes
			Id.zeroId = "0" * lengthInBytes
			while Id.idQueue.qsize() > 0:
				Id.idQueue.get() #probably a better way of doing this
			self.generateId()

	def setMaxQueueLength(self,length):
		Id.maxQueueLength = length
		while Id.idQueue.qsize() > length:
			Id.idQueue.get() #probably a better way of doing this
	
	def getAsHex(self):
		return self.getAsString().encode("hex")
		
	def getAsString(self):
		return str(self.id)