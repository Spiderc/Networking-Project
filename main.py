import id
import Queue
import threading
import UDPMessage
import timeToLive
import datagramSenderReceiver

class Main:
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	sendQueue = Queue.Queue(maxQueueLength)
	receiveQueue = Queue.Queue(maxQueueLength)
	commandQueue = Queue.Queue(maxQueueLength)
	alertQueue = Queue.Queue(maxQueueLength)
	requestMap = {}
	#TODO: create a new dictionary that contains all of the resources we've found out about
	requestedResources = {}
	state = "not in" #current state of the threads
	peers = []
	senderReceiver = datagramSenderReceiver.DatagramSenderReceiver(receiveQueue, multicastQueue)

	def __init__(self):
		self.running = True
		thread = threading.Thread(target=self.mainLoop)
		thread.start()

	def mainLoop(self):
		#Create an id object
		ids = id.Id()
		while self.running:
			if Main.state == "join":
				pass #TODO: send our IP# to joiner, clear out peers array, set peers array with responce from joiner, set state back to participate
			if Main.state == "joining":
				pass #TODO: listen for IP#s for x amount of time, assign people their new peers and send them, set peers, set state to participate
			if Main.state == "not in":
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				else:
					ids.idFactory()
			elif Main.state == "participate":
				#TODO: first check to see if there's a message from the multicast group. if so, stop threads and change state to join
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				elif not Main.sendQueue.empty():
					Main.handleSendQueue(self, Main.sendQueue.get())
				elif not Main.receiveQueue.empty():
					Main.handleReceiveQueue(self, Main.receiveQueue.get())
				#elif #TODO: check to see if we have any resources that we queried for that aren't complete
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
		
	def handleCommandQueue(self, object): #object is a command from the user with the command type as the 0th element and the parameter of the search as the 1st element
		command = object[0]
		argument = object[1]
		if command == "query":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, timeToLive=ttl, message=argument)
			Main.requestMap[id1] = ["query", argument] #adds the value to the requestMap dictionary, making note of the fact that it was a send
			Main.requestedResources[id1] = []
			addToSendQueue(self, [message.getDataGramPacket(), "127.0.0.1"]) #127.0.0.1 is used to show it came from the user
		elif command == "find":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, timeToLive=ttl, message=argument)
			Main.requestMap[id1] = ["find", argument] #adds the value to the requestMap dictionary, making note of the fact that it was a find
			addToSendQueue(self, [message.getDataGramPacket(), "127.0.0.1"]) #127.0.0.1 is used to show it came from the user
			
	def handleSendQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		for peer in Main.peers:
			if peer != "127.0.0.1" and peer != object[1]:
				Main.senderReceiver.sendToPeer(object[0], peer)
	
	def handleReceiveQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		message = UDPMessage.UDPMessage(byteArray=object)
		if message.ttl > 0:
			message.ttl.dec()
			addToSendQueue(message.getDataGramPakcet(), object[1])
			if message.id2 in Main.requestMap: #check if the message is a responce to one of our messages
				if Main.requestMap[message.id2][0] == "query": #check if our message was a query
					pass #TODO: add to the resource map the new parts we got. if we have all the parts, let the user know, otherwise ask for more
				else: #otherwise it was a find
					pass #TODO: let the user know about what we found
			else: #the message was not related to us
				pass #TODO: check if the id2 matches the id of any of our resources, if so: treat as a query, otherwise: treat as a find
