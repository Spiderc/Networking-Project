import id
import Queue
import threading
import UDPMessage
import timeToLive

class Main:
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	sendQueue = Queue.Queue(maxQueueLength)
	receiveQueue = Queue.Queue(maxQueueLength)
	commandQueue = Queue.Queue(maxQueueLength)
	alertQueue = Queue.Queue(maxQueueLength)
	requestMap = {}
	state = "not in" #current state of the threads

	def __init__(self):
		self.running = True
		thread = threading.Thread(target=self.mainLoop)
		thread.start()

	def mainLoop(self):
		#Create an id object
		ids = id.Id()
		while self.running:
			if Main.state == "join":
				pass #TODO: fix this
			if Main.state == "joining":
				pass #TODO: fix this
			if Main.state == "not in":
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				else:
					ids.idFactory()
			elif Main.state == "participate":
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				elif not Main.sendQueue.empty():
					pass #handle the outgoing message
				elif not Main.receiveQueue.empty():
					pass #handle the incoming message
				else:
					ids.idFactory()
				
	def addToSendQueue(self, object):
		global sendQueue
		Main.sendQueue.put(object)
		
	def addToRecieveQueue(self, object):
		global receiveQueue
		Main.receiveQueue.put(object)
		
	def addToCommandQueue(self, object):
		global commandQueue
		Main.commandQueue.put(object)
		
	def addToAlertQueue(self, object):
		global commandQueue
		Main.alertQueue.put(object)
		
	def stopThread(self):
		self.running = False
		
	def handleCommandQueue(self, object):
		command = object[0]
		argument = object[1]
		if command == "query":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, timeToLive=ttl, message=argument) #TODO: fix this
			Main.requestMap[id1] = ["query", argument] #adds the value to the requestMap dictionary
			addToSendQueue(self, message) #TODO: fix this
		elif command == "find":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, timeToLive=ttl, message=argument) #TODO: fix this
			Main.requestMap[id1] = ["find", argument] #adds the value to the requestMap dictionary
			addToSendQueue(self, message) #TODO: fix this
