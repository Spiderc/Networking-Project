import main
import id

def createThread(argument):
	try:
		argument = int(argument)
		global threads
		if (argument + len(threads)) <= 50:
			for i in range(0, argument):
				thread = main.Main()
				threads.append(thread)
			print "Created " + str(argument) + " threads."
		else:
			print "You cannot have more than 50 threads. The current number of threads is " + str(len(threads)) + "."
	except ValueError:
		print "The createThread command only accepts integers as a parameter."

def countThreads(argument):
	global threads
	print "There are currently " + str(len(threads)) + " threads."

def error(command):
	print command + " is not a recongized command. Type help to see all reconized commands."

def exit(argument):
	global looper
	global inCommunity
	if inCommunity:
		print "You are currently in the community, do you want to leave? (y/n)"
		input = raw_input(">")
		if input == "y":
			leave(argument) #we're fine passing down the argument because it's not used for either
			looper = False
			killAllThreads()
		else:
			pass #do nothing because they decided not to leave
	else:
		looper = False
		killAllThreads()

def find(argument):
	global inCommunity
	if inCommunity:
		print "Asking the peer community for resouces that have: " + argument + "."
		global mainThread
		mainThread.addToCommandQueue(["find", argument])
	else:
		print "You are not currently in the peer community so you can not find resources."		
		
def help(argument):
	print "The recognized commands are as follows:"
	print "createThread <int>	Creates a number of threads equal to the passed integer"
	print "countThreads		Returns the number of currently active threads"
	print "exit			Exits the program"
	print "find <String>		Asks the peer community for resources that have the passed String"
	print "help			Displays this menu"
	print "join			Joins the peer community"
	print "leave			Leaves the peer community"
	print "query <String>		Queries the peer community for resources with the passed String"
	print "stopThread <int>		Stops a number of threads equal to the passed integer"

def join(argument):
	global inCommunity
	if inCommunity:
		print "You are already in the peer community"
	else:
		print "Joining the peer community"
		#put the join stuff here
		inCommunity = True

def killAllThreads():
	global threads
	size = len(threads)
	for i in range(0, size):
		threads.pop().stopThread()
		
def leave(argument):
	global inCommunity
	if inCommunity:
		print "Leaving the peer community"
		#close ports
		inCommunity = False
	else:
		print "You are not currently in the peer community."

def query(argument):
	global inCommunity
	if inCommunity:
		print "Querying the peer community for the resource: " + argument + "."
		global mainThread
		mainThread.addToCommandQueue(["query", argument])
	else:
		print "You are not currently in the peer community so you can not make queries."
		
def stopThread(argument):
	try:
		argument = int(argument)
		global threads
		if argument >= len(threads):
			print "You cannot have less than 1 thread. The current number of threads is " + str(len(threads)) + "."
		else:
			for i in range(0, argument):
				threads.pop().stopThread()
			print "Stopped " + str(argument) + " threads."
	except ValueError:
		print "The stopThread command only accepts integers as a parameter."

print "Welcome to the Spanish Inquisition's implementation of the gossip protocol."
looper = True
inCommunity = False
mainThread = main.Main()
map = {"createThread": createThread, "countThreads": countThreads, "exit": exit, "find": find, "help": help, "join": join, "leave": leave, "query": query, "stopThread": stopThread}
threads = [mainThread]
while looper:
	input = raw_input(">")
	command = input
	argument = ""
	if " " in input:
		input = input.partition(" ") #puts the input into an array with anything before the first space in [0], a space in [1], and the rest in [2]
		command = input[0]
		argument = input[2]
	if command in map:
		map[command](argument)
	else:
		error(command)