import id
import mimetypes

class Resource:
	
	def __init__(self, fileName, description):
		idObject = id.Id()
		self.id = idObject
		self.fileName = fileName
		self.description = description
		#file = open("resources/" + fileName)
		self.fileBytes = open(("resources/" + fileName),"rb").read()
		#file.close()
		self.mimeType = mimetypes.guess_type(fileName)[0]

	def getSizeInBytes(self):
		return str(len(self.fileBytes))
