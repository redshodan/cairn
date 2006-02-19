"""templates.unix.copy.EstimateSize Module"""



import os
import os.path
import stat


import cairn
from cairn import Options



def getClass():
	return EstimateSize()



class EstimateSize(object):

	def collateExcludes(self, sysdef):
		excludeElems = sysdef.info.getElems("archive/excludes/exclude")
		if not excludeElems:
			return []
		all = []
		for excludeElem in excludeElems:
			exclude = sysdef.info.getText(excludeElem)
			exclude = exclude.strip().rstrip("*").rstrip("/")
			allRemoves = []
			if len(all):
				excludePath = exclude + "/"
				add = True
				for iter in all:
					if iter.startswith(excludePath):
						allRemoves.append(iter)
						break
					elif exclude.startswith(iter):
						add = False
						break
				if add:
					all.append(exclude)
				for r in allRemoves:
					all.remove(r)
			elif not exclude in all:
				all.append(exclude)
		return all


	# This is a measure of the space usage of tar (also star) file format
	def findTotalSize(self, sysdef, excludes):
		total = 0L
		removes = []
		for root, dirs, files in os.walk("/"):
			for dir in dirs:
				full = os.path.join(root, dir)
				if full in excludes:
					excludes.remove(full)
					removes.append(dir)
			if len(removes):
				for iter in removes:
					dirs.remove(iter)
				removes = []
			total = total + 512
			for file in files:
				fileName = os.path.join(root, file)
				info = os.lstat(fileName)
				if stat.S_ISREG(info[stat.ST_MODE]) or \
					   stat.S_ISLNK(info[stat.ST_MODE]):
					remain = info[stat.ST_SIZE] % 512
					if remain > 0:
						total = total + (512 + info[stat.ST_SIZE] +
										 512 - remain)
					else:
						total = total + (512 + info[stat.ST_SIZE])
				else:
					total = total + 512
		return total


	def run(self, sysdef):
		excludes = self.collateExcludes(sysdef)
		cairn.log("Estimating archive size... ", False)
		totalSize = self.findTotalSize(sysdef, excludes)
		cairn.log("%.3fG" % (totalSize / 1073741824.0))
		sysdef.info.set("archive/estimated-size", "%ld" % (totalSize))
		return True
