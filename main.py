import id
import Queue
import threading
import UDPMessage
import timeToLive
import datagramSenderReceiver
import time

class Main:
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	multicastQueue = Queue.Queue(maxQueueLength) #queue that keeps messages from the multicast group
	sendQueue = Queue.Queue(maxQueueLength) #queue that keeps messages waiting to be sent out
	receiveQueue = Queue.Queue(maxQueueLength) #queue that keeps messages that we've recieved but haven't processed yet
	commandQueue = Queue.Queue(maxQueueLength) #queue that contains commands from the user
	alertQueue = Queue.Queue(maxQueueLength) #queue that contains messages that the user should see
	requestMap = {} #dictionary that contains all of the find and query requests that the user has made
	foundResources = {} #dictionary of resources that have been returned to us from a find request. An array with [description, lengthInBytes, MimeType]
	requestedResources = {} #dictionary of the resources that we have done a query request for and their bytearrays. An array with [description, lengthInBytes, MimeType, bytesReceived, lastPartRequested, lastTimeRequested]
	state = "not in" #current state of the threads
	peers = ["10.20.74.0"] #an array of the ip addresses of our current peers
	senderReceiver = datagramSenderReceiver.DatagramSenderReceiver(receiveQueue)
	resourcesMap = {} #our resources that we currently have

	def __init__(self, threadName = None, resourcesMap = None):
		self.running = True
		self.thread = threading.Thread(target = self.mainLoop, name = threadName)
		self.thread.start()
		if resourcesMap != None:
			Main.resourcesMap = resourcesMap
			
		if threadName == "monty":
			self.receiver = datagramSenderReceiver.DatagramSenderReceiver(Main.receiveQueue, listener=True)
		
	def mainLoop(self):
		ids = id.Id() #Create an id object
		while self.running:
			if Main.state == "join":
				if self.thread.name != "monty":
					while Main.state == "join":
						pass #trap the threads that aren't monty
				else:
					#TODO: send our IP# to joiner, clear out peers array, set peers array with response from joiner
					Main.changeState(self, "participate")
			elif Main.state == "joining":
				if self.thread.name != "monty":
					while Main.state == "joining":
						pass #trap the thread that aren't monty
				else:
					#TODO: listen for IP#s for x amount of time, assign people their new peers and send them, set peers
					Main.changeState(self, "participate")
			elif Main.state == "not in":
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				else:
					ids.idFactory()
			elif Main.state == "participate":
				if not Main.multicastQueue.empty():
					Main.changeState(self, "join")
				elif not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				elif not Main.sendQueue.empty():
					Main.handleSendQueue(self, Main.sendQueue.get())
				elif not Main.receiveQueue.empty():
					Main.handleReceiveQueue(self, Main.receiveQueue.get())
				else:
					requestedResource = Main.checkRequestedResources(self)
					if requestedResource.getAsHex() != id.Id(value=id.Id().zeroId).getAsHex():
						Main.requestPartNumber(self, partNumber=Main.requestedResources[requestedResource.getAsHex()][4], resourceId=requestedResource)
					else:
						ids.idFactory()
				
	def addToSendQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		global sendQueue
		Main.sendQueue.put(object)
		
	def addToRecieveQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		global receiveQueue
		Main.receiveQueue.put(object)
		
	def addToCommandQueue(self, object): #object is a command from the user with the command type as the 0th element and the parameter of the search as the 1st element
		global commandQueue
		Main.commandQueue.put(object)
		
	def addToAlertQueue(self, object): #object is a string intended for the user to see
		global commandQueue
		Main.alertQueue.put(object)
		
	def stopThread(self):
		self.running = False
		
	def stopListening(self):
		if self.thread.name == "monty":
			self.receiver.stopThread()
		
	def changeState(self, newState):
		Main.state = newState
		
	def checkRequestedResources(self): #check to see if we need to resend a query request for one of the resources we requested
		result = id.Id(value=id.Id().zeroId)
		for key in Main.requestedResources:
			requestedResource = Main.requestedResources[key]
			if requestedResource[5] + 10 < time.time():
				result = id.Id(value=key)
				break
		return result
		
	def handleCommandQueue(self, object): #object is a command from the user with the command type as the 0th element and the parameter of the search as the 1st element
		command = object[0]
		argument = object[1]
		if command == "query":
			id1 = id.Id()
			id2 = id.Id(value=argument)
			print Main.foundResources
			if id2.getAsHex() in Main.foundResources:
				foundResource = Main.foundResources[id2.getAsHex()]
				Main.requestMap[id1.getAsHex()] = ["query", id2.getAsHex()] #adds the value to the requestMap dictionary, making note of the fact that it was a send
				Main.requestedResources[id2.getAsHex()] = [foundResource[0], foundResource[1], foundResource[2], "", 1, time.time()]
				print "test"
				Main.requestPartNumber(self, partNumber=1, resourceId=id2, requestId=id1)
				print Main.requestedResources
			else:
				Main.addToAlertQueue(self, "Unknown resource: " + argument)
		elif command == "find":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, ttl=ttl, message=argument)
			Main.requestMap[id1.getAsHex()] = ["find", argument] #adds the value to the requestMap dictionary, making note of the fact that it was a find
			Main.addToSendQueue(self, [message.getDataGramPacket(), "127.0.0.1"]) #127.0.0.1 is used to show it came from the user

	def handleSendQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		for peer in Main.peers:
			#if peer != object[1]:
			Main.senderReceiver.send(peer, 12345, object[0])
	
	def handleReceiveQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		message = UDPMessage.UDPMessage(byteArray=object)
		if message.ttl.ttl > 0:
			message.ttl.dec()
			Main.addToSendQueue(self,[message.getDataGramPacket(), object[1]]) #no matter what we pass the message onto our peers
			if message.id2.getAsHex() in Main.requestMap: #check if the message is a response to one of our messages
				if Main.requestMap[message.id2.getAsHex()][0] == "query": #check if our message was a query
					Main.requestedResources[message.id1.getAsHex()][3] = Main.requestedResources[message.id1][3] + "" + message.message[20:len(message)]
					Main.requestedResources[message.id1.getAsHex()][4] = int(message.message[16:20])
					if len(message) < 456:
						Main.addToAlertQueue(self,"Resource #" + message.id1 + " has been received.")					
					else:
						requestPartNumber(self, id.Id(value=Main.requestedResources[message.id1][4]), message.id1)
				else: #otherwise it was a find
					if message.id2.getAsHex() not in Main.foundResources: #we don't need to put it in the foundResources dictionary if it's already there
						findMessageResponse = message.message[id.Id().idLengthInBytes:]
						delimiter = findMessageResponse[:1]
						responseArray = findMessageResponse.split(delimiter)
						Main.addToAlertQueue(self,"Found resource " + message.id2.getAsHex() + ". The description of the resource is " + responseArray[3] + " The length in bytes is " + responseArray[2] + ". The MimeType is " + responseArray[1] + ".")
						Main.foundResources[message.id2.getAsHex()] = [responseArray[3], responseArray[2], responseArray[1]]
			else: #the message was not related to us
				if message.id2.getAsHex() in Main.resourcesMap: #treat as a query
					partNumber = message.message[id.Id().idLengthInBytes:id.Id.idLengthInBytes + 4] #the part number of the requested resource
					requestedResource = Main.resourcesMap[message.id2.getAsHex()]
					resoucePartTtl = timeToLive.TimeToLive()
					if 456*(int(partNumber)) < int(requestedResource.getSizeInBytes()):
						resourcePart = id.Id().getAsBytes() + partNumber + requestedResource.fileBytes[456*(int(partNumber)-1):456*(int(partNumber))]
						resourcePartMessage = UDPMessage.UDPMessage(id1=message.id2, id2=message.id1, ttl=resourcePartTtl, message=resourcePart)
					else:
						resourcePart = id.Id().getAsBytes() + partNumber + requestedResource.fileBytes[456*(int(partNumber)-1):]
						resourcePartMessage = UDPMessage.UDPMessage(id1=message.id2, id2=message.id1, ttl=resourcePartTtl, message=resourcePart, lastPacket=True)
					Main.addToSendQueue(self,[resourcePartMessage.getDataGramPacket(), "127.0.0.1"])
				else: #treat as a find
					for key in Main.resourcesMap: #loop through all of our resources
						resource = Main.resourcesMap[key]
						if Main.removePadding(self,message.message) in resource.description: #check if we have a matching resource
							responseId1 = resource.id
							responseId2 = message.id1
							responseTtl = timeToLive.TimeToLive()
							responseMessage = id.Id().getAsString() + "|" + resource.mimeType + "|" + resource.getSizeInBytes() + "|" + resource.description
							responseDatagram = UDPMessage.UDPMessage(id1=responseId1, id2=responseId2, ttl=responseTtl, message=responseMessage);
							Main.addToSendQueue(self,[responseDatagram.getDataGramPacket(), "127.0.0.1"])

	def requestPartNumber(self, partNumber, resourceId, requestId=id.Id()):
		requestedResource = Main.requestedResources[resourceId.getAsHex()]
		resourcePartTtl = timeToLive.TimeToLive()
		resourcePart = id.Id().getAsString() +""+ str(partNumber)
		resourcePartMessage = UDPMessage.UDPMessage(requestId, resourceId, ttl=resourcePartTtl, message=resourcePart)
		requestedResource[5] = time.time()
		Main.addToSendQueue(self, [resourcePartMessage.getDataGramPacket(), "127.0.0.1"])
		
	def removePadding(self, message):
		return message.replace(message[-1:],"")		
		

		
		
		
	
