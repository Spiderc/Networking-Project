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
	peers = [] #an array of the ip addresses of our current peers
	senderReceiver = datagramSenderReceiver.DatagramSenderReceiver(receiveQueue, multicastQueue)
	resourcesMap = {} #our resources that we currently have

	def __init__(self, threadName = None, resourcesMap = None):
		self.running = True
		self.thread = threading.Thread(target = self.mainLoop, name = threadName)
		self.thread.start()
		if resourcesMap != None:
			Main.resourcesMap = resourcesMap

	def mainLoop(self):
		ids = id.Id() #Create an id object
		while self.running:
			if Main.state == "join":
				if self.thread.name != "monty":
					while Main.state == "join":
						pass #trap the threads that aren't monty
				else:
					pass
					#TODO: send our IP# to joiner, clear out peers array, set peers array with response from joiner
					Main.state = "participate"
			if Main.state == "joining":
				if self.thread.name != "monty":
					while Main.state == "joining":
						pass #trap the thread that aren't monty
				else:
					pass
					#TODO: listen for IP#s for x amount of time, assign people their new peers and send them, set peers
					Main.state = "participate"
			if Main.state == "not in":
				if not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				else:
					ids.idFactory()
			elif Main.state == "participate":
				if not Main.multicastQueue.empty():
					Main.state = "join"
				elif not Main.commandQueue.empty():
					Main.handleCommandQueue(self, Main.commandQueue.get())
				elif not Main.sendQueue.empty():
					Main.handleSendQueue(self, Main.sendQueue.get())
				elif not Main.receiveQueue.empty():
					Main.handleReceiveQueue(self, Main.receiveQueue.get())
				else:
					requestedResource = checkRequestedResources(self)
					if requestedResource != id.Id().zeroId:
						requestPartNumber(self, requestedResources[requestedResource][4], requestedResource)
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
		
	def checkRequestedResources(self): #check to see if we need to resend a query request for one of the resources we requested
		result = id.Id().zeroId
		for key, requestedResouce in Main.requestedResources:
			if requestedResource[5] + 10 > time.time():
				result = key
				break
		return result
		
	def handleCommandQueue(self, object): #object is a command from the user with the command type as the 0th element and the parameter of the search as the 1st element
		command = object[0]
		argument = object[1]
		if command == "query":
			id1 = id.Id()
			id2 = id.Id(value=argument)
			if id2 in foundResources:
				foundResource = foundResources[id2]
				Main.requestMap[id1] = ["query", id2] #adds the value to the requestMap dictionary, making note of the fact that it was a send
				Main.requestedResources[id1] = [foundResource[0], foundResource[1], foundResource[2], , 0, time.time()]
				requestPartNumber(self, 0, id2, requestId=id1)
			else:
				addToAlertQueue(self, "Unknown resource: " + argument)
		elif command == "find":
			id1 = id.Id()
			id2 = id.Id()
			ttl = timeToLive.TimeToLive()
			message = UDPMessage.UDPMessage(id1=id1, id2=id2, timeToLive=ttl, message=argument)
			Main.requestMap[id1] = ["find", argument] #adds the value to the requestMap dictionary, making note of the fact that it was a find
			addToSendQueue(self, [message.getDataGramPacket(), "127.0.0.1"]) #127.0.0.1 is used to show it came from the user
			
	def handleSendQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		for peer in Main.peers:
			if peer != object[1]:
				Main.senderReceiver.sendToPeer(object[0], peer)
	
	def handleReceiveQueue(self, object): #object is an array with the datagramPacket as the 0th element and the IP address that we got it from orginally as the 1st element
		message = UDPMessage.UDPMessage(byteArray=object)
		if message.ttl > 0:
			message.ttl.dec()
			addToSendQueue(self,message.getDataGramPakcet(), object[1]) #no matter what we pass the message onto our peers
			if message.id2 in Main.requestMap: #check if the message is a response to one of our messages
				if Main.requestMap[message.id2][0] == "query": #check if our message was a query
					Main.requestedResources[message.id1][3] = Main.requestedResources[message.id1][3] + "" + message.message[20:len(message)]
					Main.requestedResources[message.id1][4] = message.message[16:20]			
					if len(message) < 456
						addToAlertQueue(self,"Resource #" + message.id1 + " has been received.")					
					else
						requestPartNumber(self, Main.requestedResources[message.id1][4], message.id1)
				else: #otherwise it was a find
					findMessageResponse = message.message[id.Id().idLengthInBytes:]
					delimiter = findMessageResponse[:1]
					responseArray = findMessageResponse.split(delimiter)
					addToAlertQueue(self,"Found resource #" + message.id2.getAsString() + ". The description of the resource is " + responseArray[5] + ". The length in bytes is " + responseArray[3] + ". The MimeType is " + responseArray[1] + "."
					Main.foundResources[message.id2] = [responseArray[5], responseArray[3], responseArray[1])
			else: #the message was not related to us
				if message.id2 in Main.resourcesMap: #treat as a query
					partNumber = message.message[id.Id().idLengthInBytes:id.Id.idLengthInBytes + 4] #the part number of the requested resource
					requestedResource = Main.resourcesMap[message.id2]
					resoucePartTtl = timeToLive.TimeToLive()
					resourcePart = id.Id() + partNumber + requestedResource.fileBytes[456*int(partNumber):456*(int(partNumber)+1)]
					resourcePartMessage = UDPMessage.UDPMessage(id1=message.id2, id2=message.id1, ttl=resourcePartTtl, message=resourcePart)
					addToSendQueue(self,[resourcePartMessage, "127.0.0.1"])
				else: #treat as a find
					for key, resource in Main.resourcesMap: #loop through all of our resources
						if message.message in resource.fileName or message.message in resource.description: #check if we have a matching resource
							responseId1 = id.Id()
							responseId2 = id.Id()
							responseTtl = timeToLive.TimeToLive()
							responseMessage = id.Id().getAsString() + "|" + resource.mimeType + "|" + len(resource.fileBytes) + "|" + resource.description
							responseDatagram = UDPMessage.UDPMessage(id1=responseId1, id2=responseId2, ttl=responseTtl, message=responseMessage);
							addToSendQueue(self,[responseDatagram, "127.0.0.1"])

	def  requestPartNumber(self, partNumber, resourceID, requestId=id.Id())
		requestedResource = Main.requestedResources[resourceID]
		resoucePartTtl = timeToLive.TimeToLive()
		resourcePart = id.Id() +""+ partNumber
		resourcePartMessage = UDPMessage.UDPMessage(requestId, resourceID, ttl=resourcePartTtl, message=resourcePart)
		requestedResource[5] = time.time()
		addToSendQueue(self, [resourcePartMessage, "127.0.0.1"])

		
		
		
	
