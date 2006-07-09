"""templates.unix.extract.archive.read.RunArchiver Module"""



import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.extract.archive.RunArchiver as tmpl



def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	# Disable progress display
	def processPercent(self, percent, buffSize):
		return


	def displayPercent(self, percent):
		return


	def finishDisplayPercent(self):
		return
