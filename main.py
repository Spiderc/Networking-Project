import id as id

def getState():
	result = "participate"
	if False: #check the thing that i forgot the name for and if someone wants to join switch to join state
		result = "join"
	return result

def mainLoop():
	#Initialize sending & receiving queues
	maxQueueLength = 0 #0 means infinite queue size
	sendQueue = Queue.Queue(maxQueueLength)
	receiveQueue = Queue.Queue(maxQueueLength)
	commandQueue = Queue.Queue(maxQueueLength)
	
	#Create an id object
	ids = id.Id()
	
	while True:
		state = getState()
		if state == "join":
			pass
			#do join stuff here
		elif state == "participate":
			#check to see if there's any datagrams in the outgoing queue
			#else check to see if there's any datagrams in the incoming queue
			ids.generateId() #make this an else once the others parts are implemented
			
			#Check send queue
			#thread.datagramSenderReceiver.send(sendQueue.get(False))
			
			#Check for incomming datagramPackets
			#thread.datagramSenderReceiver.receive()
				
			