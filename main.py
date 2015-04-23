import id
import Queue
import threading

class Main:
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	sendQueue = Queue.Queue(maxQueueLength)
	receiveQueue = Queue.Queue(maxQueueLength)
	commandQueue = Queue.Queue(maxQueueLength)

	def __init__(self):
		self.running = True
		thread = threading.Thread(target=self.mainLoop)
		thread.start()
	
	def getState(self):
		result = "participate"
		if False: #check the thing that i forgot the name for and if someone wants to join switch to join state
			result = "join"
		return result

	def mainLoop(self):
		#Create an id object
		ids = id.Id()
		while self.running:
			state = self.getState()
			if state == "join":
				pass
				#do join stuff here
			elif state == "participate":
				if not Main.commandQueue.empty():
					pass #handle the command
				elif not Main.sendQueue.empty():
					pass #handle the outgoing message
				elif not Main.receiveQueue.empty():
					pass #handle the incoming message
				else:
					ids.generateId()
				
	def addToSendQueue(self, object):
		global sendQueue
		Main.sendQueue.put(object)
		
	def addToRecieveQueue(self, object):
		global receiveQueue
		Main.receiveQueue.put(object)
		
	def addToCommandQueue(self, object):
		global commandQueue
		Main.commandQueue.put(object)
		
	def stopThread(self):
		self.running = False