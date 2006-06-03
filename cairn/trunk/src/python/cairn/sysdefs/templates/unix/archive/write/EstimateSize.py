"""templates.unix.copy.write.EstimateSize Module"""



import os
import os.path
import stat


import cairn
from cairn import Options


TAR_BLKSIZE = 512



def getClass():
	return EstimateSize()



class EstimateSize(object):

	def collateExcludes(self, sysdef):
		excludeElems = sysdef.info.getElems("archive/excludes/exclude")
		if not excludeElems:
			return []
		all = []
		for excludeElem in excludeElems:
			exclude = excludeElem.getText()
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
			# Header block for current dir
			#cairn.debug("dir: %s, 512" % root)
			total = total + TAR_BLKSIZE
			for file in files:
				# Header block
				total = total + TAR_BLKSIZE
				fileName = os.path.join(root, file)
				#cairn.debug("file:  %s" % fileName)
				info = os.lstat(fileName)
				if stat.S_ISREG(info[stat.ST_MODE]) or \
					   stat.S_ISLNK(info[stat.ST_MODE]):
					#cairn.debug("       size=%d blocks=%d" %
					#			(info[stat.ST_SIZE],
					#			 (info[stat.ST_SIZE] / TAR_BLKSIZE)))
					# Whole number of blocks used
					total = total + (TAR_BLKSIZE *
									 (info[stat.ST_SIZE] / TAR_BLKSIZE))
					# Remainder (partial) block
					if (info[stat.ST_SIZE] % TAR_BLKSIZE) > 0:
						#cairn.debug("       +1 block")
						total = total + TAR_BLKSIZE
		return total


	def run(self, sysdef):
		excludes = self.collateExcludes(sysdef)
		cairn.log("Estimating archive size... ", False)
		totalSize = self.findTotalSize(sysdef, excludes)
		cairn.log("%.3fG" % (totalSize / 1073741824.0))
		sysdef.info.setChild("archive/estimated-size", "%ld" % (totalSize))
		return True
