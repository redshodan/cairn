"""templates.unix.restore.setup.CreateLVM Module"""



import commands


import cairn



def getClass():
	return CreateLVM()


class CreateLVM(object):

	def createPV(self, sysdef, pvElem):
		dev = pvElem.getText()
		cmd = "%s -u %s %s" % (sysdef.info.get("env/tools/pvcreate"),
							   pvElem.getAttr("uuid"), dev)
		(status, output) = commands.getstatusoutput(cmd)
		if (status != 0):
			raise cairn.Exception("Failed to create Physical Volume %d: %s" %
								  (dev, output))
		return


	def restoreVG(self, sysdef, vgElem):
		vgname = vgElem.getText()
		cmd = "%s %s" % (sysdef.info.get("env/tools/vgcfgrestore"), vgname)
		(status, output) = commands.getstatusoutput(cmd)
		if (status != 0):
			raise cairn.Exception("Failed to restore Volume Group %d: %s" %
								  (vgname, output))
		return


	def run(self, sysdef):
		cairn.log("Recreating Physical Volumes")
		for pv in sysdef.info.getElems("hardware/lvm-cfg/pvs/pv"):
			self.createPV(sysdef, sysdef, pv)
		cairn.log("Recreating Volume Groups")
		for vg in sysdef.info.getElems("hardware/lvm-cfg/vgs/vg"):
			self.restoreVG(sysdef, sysdef, vg)
		return True
