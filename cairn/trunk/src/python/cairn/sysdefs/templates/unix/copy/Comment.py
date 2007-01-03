"""templates.unix.copy.Comment"""


import re
import sys


import cairn
from cairn import Options



def getClass():
	return Comment()



class Comment(object):

	def askComment(self):
		cairn.displayRaw("Do you wish to place a comment in this image? [y/N]: ")
		line = sys.stdin.readline()
		cairn.displayNL()
		if re.match("[yY]", line):
			cairn.display("Enter comment text. To end enter a line with a '.' in it.")
			comment = []
			while True:
				line = sys.stdin.readline()
				line = line.strip()
				if line == ".":
					break
				else:
					comment.append(line)
			print "comment arr", comment
			return "\n".join(comment)
		else:
			return None


	def setComment(self, sysdef, comment):
		print "comment", comment
		sysdef.info.set("comment", comment)
		return


	def run(self, sysdef):
		if Options.get("comment"):
			self.setComment(sysdef, Options.get("comment"))
		else not Options.get("yes"):
			comment = self.askComment()
			if comment:
				self.setComment(sysdef, comment)
		return True
