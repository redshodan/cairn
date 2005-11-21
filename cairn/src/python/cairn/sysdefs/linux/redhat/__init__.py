"""RedHat Linux system definitions"""



from cairn.sysdefs.linux.unknown import Unknown



def getClass():
	return RedHat()



class RedHat(Unknown):
	def __init__(self):
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def name(self):
		return "RedHat"
