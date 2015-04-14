import os
import Queue

class Id:
	idLengthInBytes = 16
	maxQueueLength = 10000
	idQueue = Queue.Queue(maxQueueLength)
	zeroId = "0" * idLengthInBytes

	def __init__(self):
		pass

	def generateId(self):
		if Id.idQueue.qsize() < Id.maxQueueLength:
			Id.idQueue.put(os.urandom(Id.idLengthInBytes))
		
	def getId(self):
		if Id.idQueue.empty():
			return os.urandom(Id.idLengthInBytes)
		else:
			return Id.idQueue.get();

	def setIdLength(self,lengthInBytes):
		if lengthInBytes != Id.idLengthInBytes:
			Id.idLengthInBytes = lengthInBytes
			Id.zeroId = "0" * lengthInBytes
			#clear out the queue

	def setMaxQueueLength(self,length):
		Id.maxQueueLength = length
		while Id.idQueue.qsize() > length:
			Id.idQueue.get() #probably a better way of doing this
	
	def getIdString(self):
		return self.getId().encode("hex")
