import id
import Queue
import threading
import UDPMessage
import timeToLive
import datagramSenderReceiver
import time
import struct
import mimetypes

class Main:
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	multicastQueue = Queue.Queue(maxQueueLength) #queue that keeps messages from the multicast group
	sendQueue = Queue.Queue(maxQueueLength) #queue that keeps messages waiting to be sent out
	receiveQueue = Queue.Queue(maxQueueLength) #queue that keeps messages that we've recieved but haven't processed yet
	commandQueue = Queue.Queue(maxQueueLength) #queue that contains commands from the user
	alertQueue = Queue.Queue(maxQueueLength) #queue that contains messages that the user should see
	requestMap = {} #dictionary that contains all of the find and query requests that the user has made
	foundResources = {} #dictionary of resources that have been returned to us from a find request. An array with [description, lengthInBytes, MimeType, localId]
	requestedResources = {} #dictionary of the resources that we have done a query request for and their bytearrays. An array with [description, lengthInBytes, MimeType, bytesReceived, lastPartRequested, lastTimeRequested, localId, requestId]
	state = "not in" #current state of the threads
	peers = ["140.209.121.104"] #an array of the ip addresses of our current peers
	senderReceiver = datagramSenderReceiver.DatagramSenderReceiver(receiveQueue)
	resourcesMap = {} #our resources that we currently have
	localIdCounter = 1 #counter to keep track of our local ids for resources
	completedResources = {} #the resources that we have finished downloading. An array with [description, fileBytes, MimeType, localId]

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
						Main.requestPartNumber(self, partNumber=Main.requestedResources[requestedResource.getAsHex()][4], resourceId=requestedResource, requestId=Main.requestedResources[requestedResource.getAsHex()][7])
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
			if requestedResource[3] < requestedResource[1] and requestedResource[5] + 10 < time.time():
				result = id.Id(value=key)
				break
		return result
		
	def printFoundResources(self):
		for key in Main.foundResources:
			foundResource = Main.foundResources[key]
			print "Resource description is '" + foundResource[0] + "', length in bytes is '" + foundResource[1] + "', MimeType is '" + foundResource[2] + ". It has a global id of " + key + " and a local id of " + str(foundResource[3]) + "."
			
	def printCompletedResources(self):
		for key in Main.completedResources:
			completedResource = Main.completedResources[key]
			print "Resource description is '" + completedResource[0] + "', MimeType is '" + completedResource[2] + "'. It has a global id of " + key + " and a local id of " + str(completedResource[3]) + "."
			
	def download(self, resource):
		if resource in Main.completedResources: #check if they're using the global id
			with open(str(resource) + mimetypes.guess_extension(Main.completedResources[resource][2]), "wb") as output:
				output.write(Main.completedResources[resource][1])
		else:
			for key in Main.completedResources: #loop throught to check if they're using the local id
				completedResource = Main.completedResources[key]
				if completedResource[3] == resource:
					with open(str(resource) + mimetypes.guess_extension(completedResource[2]), "wb") as output:
						output.write(completedResource[1])
		
	def handleCommandQueue(self, object): #object is a command from the user with the command type as the 0th element and the parameter of the search as the 1st element
		command = object[0]
		argument = object[1]
		if command == "query":
			id1 = id.Id()
			if len(argument) != (id.Id().idLengthInBytes*2):
				for key in Main.foundResources:
					foundResource = Main.foundResources[key]
					if argument == foundResource[3]:
						id2 = id.Id(value=key)
						Main.requestMap[id1.getAsHex()] = ["query", key] #adds the value to the requestMap dictionary, making note of the fact that it was a send
						Main.requestedResources[key] = [foundResource[0], foundResource[1], foundResource[2], "", 1, time.time(), foundResource[3], id1]
						Main.requestPartNumber(self, partNumber=1, resourceId=id2, requestId=id1)
			else:
				id2 = id.Id(value=argument)
				if id2.getAsHex() in Main.foundResources:
					foundResource = Main.foundResources[id2.getAsHex()]
					Main.requestMap[id1.getAsHex()] = ["query", id2.getAsHex()] #adds the value to the requestMap dictionary, making note of the fact that it was a send
					Main.requestedResources[id2.getAsHex()] = [foundResource[0], foundResource[1], foundResource[2], "", 1, time.time(), foundResource[3], id1]
					Main.requestPartNumber(self, partNumber=1, resourceId=id2, requestId=id1)
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
					messagePartNumber = struct.unpack(">I",message.message[message.id1.idLengthInBytes:message.id1.idLengthInBytes+4])[0] #4 is the size of the partNumber
					if messagePartNumber == Main.requestedResources[message.id1.getAsHex()][4]: #check to see if the message has the part number that matches that last one that we requested
						Main.requestedResources[message.id1.getAsHex()][3] = Main.requestedResources[message.id1.getAsHex()][3] + "" + message.message[message.id1.idLengthInBytes+4:] #4 is the size of the partNumber
						Main.requestedResources[message.id1.getAsHex()][4] = Main.requestedResources[message.id1.getAsHex()][4] + 1
						if len(message.message) < 456: #check to see if this was the last part
							Main.addToAlertQueue(self,"Resource " + message.id1.getAsHex() + " has been received.")
							Main.completedResources[message.id1.getAsHex()] = [Main.requestedResources[message.id1.getAsHex()][0], Main.requestedResources[message.id1.getAsHex()][3], Main.requestedResources[message.id1.getAsHex()][2], Main.requestedResources[message.id1.getAsHex()][6]]
						else:
							Main.requestPartNumber(self, partNumber=Main.requestedResources[message.id1.getAsHex()][4], resourceId=message.id1, requestId=Main.requestedResources[message.id1.getAsHex()][7])
				else: #otherwise it was a find
					if message.id1.getAsHex() not in Main.foundResources: #we don't need to put it in the foundResources dictionary if it's already there
						findMessageResponse = message.message[id.Id().idLengthInBytes:]
						delimiter = findMessageResponse[:1]
						responseArray = findMessageResponse.split(delimiter)
						Main.addToAlertQueue(self,"Found resource " + message.id1.getAsHex() + ". The description of the resource is '" + responseArray[3] + "' The length in bytes is " + responseArray[2] + ". The MimeType is " + responseArray[1] + ". Its local id is: " + str(Main.localIdCounter))
						Main.foundResources[message.id1.getAsHex()] = [responseArray[3], responseArray[2], responseArray[1], str(Main.localIdCounter)]
						Main.localIdCounter = Main.localIdCounter + 1
			else: #the message was not related to us
				if message.id2.getAsHex() in Main.resourcesMap: #treat as a query
					partNumberBytes = message.message[id.Id().idLengthInBytes:id.Id().idLengthInBytes + 4] #the part number of the requested resource
					partNumber = struct.unpack(">I",partNumberBytes)[0]
					requestedResource = Main.resourcesMap[message.id2.getAsHex()]
					resourcePartTtl = timeToLive.TimeToLive()
					if 456*(int(partNumber)) < int(requestedResource.getSizeInBytes()):
						resourcePart = id.Id().getAsBytes() + partNumberBytes + requestedResource.fileBytes[456*(int(partNumber)-1):456*(int(partNumber))]
						resourcePartMessage = UDPMessage.UDPMessage(id1=requestedResource.id, id2=message.id1, ttl=resourcePartTtl, message=resourcePart)
					else:
						resourcePart = id.Id().getAsBytes() + partNumberBytes + requestedResource.fileBytes[456*(int(partNumber)-1):]
						resourcePartMessage = UDPMessage.UDPMessage(id1=requestedResource.id, id2=message.id1, ttl=resourcePartTtl, message=resourcePart, lastPacket=True)
					Main.addToSendQueue(self,[resourcePartMessage.getDataGramPacket(), "127.0.0.1"])
				else: #treat as a find
					for key in Main.resourcesMap: #loop through all of our resources
						resource = Main.resourcesMap[key]
						if Main.removePadding(self,message.message) in resource.description: #check if we have a matching resource
							responseId1 = resource.id
							responseId2 = message.id1
							responseTtl = timeToLive.TimeToLive()
							responseMessage = id.Id().getAsBytes() + "|" + resource.mimeType + "|" + resource.getSizeInBytes() + "|" + resource.description
							responseDatagram = UDPMessage.UDPMessage(id1=responseId1, id2=responseId2, ttl=responseTtl, message=responseMessage);
							Main.addToSendQueue(self,[responseDatagram.getDataGramPacket(), "127.0.0.1"])

	def requestPartNumber(self, partNumber, resourceId, requestId):
		requestedResource = Main.requestedResources[resourceId.getAsHex()]
		resourcePartTtl = timeToLive.TimeToLive()
		resourcePart = id.Id().getAsBytes() + bytearray(struct.pack(">I", partNumber))
		resourcePartMessage = UDPMessage.UDPMessage(requestId, resourceId, ttl=resourcePartTtl, message=resourcePart)
		requestedResource[5] = time.time()
		Main.addToSendQueue(self, [resourcePartMessage.getDataGramPacket(), "127.0.0.1"])
		
	def removePadding(self, message):
		return message.replace(message[-1:],"")		

