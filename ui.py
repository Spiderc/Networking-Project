def error(command):
	print command + " is not a recongized command. Type help to see all reconized commands."

def exit(argument): #do we need to call leave from here?
	global looper
	global inCommunity
	if inCommunity:
		print "You are currently in the community, do you want to leave? (y/n)"
		input = raw_input(">")
		if input == "y":
			leave(argument)
			looper = False
		else:
			pass #do nothing because they decided not to leave
	else:
		looper = False

def find(argument):
	global inCommunity
	if inCommunity:
		print "Asking the peer community for resouces that have: " + argument + "."
		#put the request into the commandQueue
	else:
		print "You are not currently in the peer community so you can not find resources."		
		
def help(argument):
	print "The recognized commands are as follows:"
	print "exit		Exits the program"
	print "help		Displays this menu"
	print "join		Joins the peer community"
	print "leave		Leaves the peer community"
	print "query <String>	Queries the peer community for resources with the passed String"

def join(argument):
	global inCommunity
	if inCommunity:
		print "You are already in the peer community"
	else:
		print "Joining the peer community"
		#put the join stuff here
		inCommunity = True

def leave(argument):
	global inCommunity
	if inCommunity:
		print "Leaving the peer community"
		#put the leaving stuff here (probably just kill all threads and close ports)
		inCommunity = False
	else:
		print "You are not currently in the peer community"

def query(argument):
	global inCommunity
	if inCommunity:
		print "Querying the peer community for the resource: " + argument + "."
		#put the request into the commandQueue
	else:
		print "You are not currently in the peer community so you can not make queries."

print "Welcome to the FS implementation of the gossip protocol."
looper = True
inCommunity = False
map = {"exit": exit, "find": find, "help": help, "join": join, "leave": leave, "query": query}
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