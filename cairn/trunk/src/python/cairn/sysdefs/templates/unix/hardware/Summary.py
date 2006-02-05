"""templates.unix.hardware.Summary Module"""


from cairn import Options
from cairn import sysdefs



def getClass():
	return Summary()



class Summary(object):

	def run(self, sysdef):
		if Options.get("summary"):
			sysdef.printSummary()
			sysdefs.quit()
		return True
