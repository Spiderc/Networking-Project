
class TimeToLive:
	sizeInBytes = 4;

	def __init__(self, timeToLive):
		self.ttl = timeToLive
		
		if timeToLive = -1:
			self.ttl = (random.getrandbits(4) + 10)
		
	def dec(self):
		self.ttl = self.ttl - 1;
