import main
import id
import Queue
import csv
import resource

def alerts(argument):
	global mainThread
	if mainThread.alertQueue.empty():
		print "There are currently no pending alerts."
	else:
		print mainThread.alertQueue.get()

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
	print command + " is not a recognized command. Type help to see all recognized commands."

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
	global mainThread
	if inCommunity:
		print "Asking the peer community for resources that have: " + argument + "."
		mainThread.addToCommandQueue(["find", argument])
	else:
		print "You are not currently in the peer community so you can not find resources."		
		
def help(argument):
	print "The recognized commands are as follows:"
	print "alerts		Prints out the next pending alert"
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
	global mainThread
	if inCommunity:
		print "You are already in the peer community"
	else:
		print "Joining the peer community"
		mainThread.changeState("join")
		#stop other threads? #TODO: fix this
		#TODO: start listening to multicast
		inCommunity = True

def killAllThreads():
	global threads
	threads[0].listenerThread.stopThread()
	size = len(threads)
	for i in range(0, size):
		threads.pop().stopThread()

def leave(argument):
	global inCommunity
	global mainThread
	if inCommunity:
		print "Leaving the peer community"
		#TODO: stop listening to multicast
		mainThread.changeState("not in")
		inCommunity = False
	else:
		print "You are not currently in the peer community."

def query(argument):
	global inCommunity
	global mainThread
	if inCommunity:
		print "Querying the peer community for the resource: " + argument + "."
		mainThread.addToCommandQueue(["query", argument])
	else:
		print "You are not currently in the peer community so you can not make queries."
		
def stopThread(argument):
	global threads
	try:
		argument = int(argument)
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
resourcesMap = {}
with open('resources/directory.txt', 'rb') as cvsfile:
	text = csv.reader(cvsfile, delimiter = '|')
	for row in text:
		res = resource.Resource(row[0], row[1])
		resourcesMap[res.id] = res
mainThread = main.Main(threadName = "monty", resourcesMap = resourcesMap)
map = {"alerts": alerts, "createThread": createThread, "countThreads": countThreads, "exit": exit, "find": find, "help": help, "join": join, "leave": leave, "query": query, "stopThread": stopThread}
threads = [mainThread]
while looper:
	if not mainThread.alertQueue.empty():
		print "You have " + str(mainThread.alertQueue.qsize()) + " alerts. Type alerts to see them." #TODO see if there's a better way to let the user know about new alerts
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
