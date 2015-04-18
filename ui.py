def error(command):
	print command + " is not a recongized command. Type help to see all reconized commands."

def exit(argument):
	global looper
	looper = False
	
def help(argument):
	print "The recognized commands are as follows:"
	print "exit		Exits the program"
	print "help		Displays this menu"
	print "query <String>	Queries the peer community for resources with the passed String"

def query(argument):
	print "Querying the peer community for the resource: " + argument + "."

print "Welcome to the FS implementation of the gossip protocol."
looper = True
map = {"exit": exit, "help": help, "query": query}
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