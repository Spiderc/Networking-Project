def getState():
	result = "participate"
	if False: #check the thing that i forgot the name for and if someone wants to join switch to join state
		result = "join"
	return result

while True:
	state = getState()
	if state == "join":
		print "joining"
		#do join stuff here
	elif state == "participate":
		print "participating"
		#check to see if there's any datagrams in the outgoing queue
		#else check to see if there's any datagrams in the incoming queue
		#else check to see if the id queue is not full
			#generate a new id to put into the id queue