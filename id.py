import os
import Queue

class Id:
	idLengthInBytes = 16
	maxQueueLength = 10000
	idQueue = Queue.Queue(maxQueueLength)
	zeroID = "0" * idLengthInBytes

	def __init__(self):
		pass

	def generateId(self):
		Id.idQueue.put(os.urandom(Id.idLengthInBytes))

	def setIDLength(self,lengthInBytes):
		if lengthInBytes != Id.idLengthInBytes:
			Id.idLengthInBytes = lengthInBytes
			Id.zeroID = "0" * lengthInBytes
			#clear out the queue

	def setMaxQueueLength(self,length):
		Id.maxQueueLength = length
		while Id.idQueue.qsize() > length:
			Id.idQueue.get() #probably a better way of doing this