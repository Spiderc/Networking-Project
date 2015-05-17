import id
import mimetypes

class Resource:
	
	def __init__(self, fileName, description):
		idObject = id.Id()
		self.id = idObject
		self.fileName = fileName
		self.description = description
		file = open("resources/" + fileName)
		self.fileBytes = bytearray(file.read())
		file.close()
		self.mimeType = mimetypes.guess_type(fileName)[0]
