
class timeToLive:

	def __init__(self, timeToLive):
		self.ttl = timeToLive
		
		if timeToLive = -1:
			self.ttl = (os.urandom(1) + 10)
		
	def dec(self):
		self.ttl = self.ttl - 1;
