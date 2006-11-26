"""templates.unix.restore.setup.CreateLVM Module"""



import os
import commands


import cairn



def getClass():
	return CreateLVM()


class CreateLVM(object):

	def zeroPV(self, sysdef, pvElem):
		dev = pvElem.getText()
		try:
			pv = file(dev, "w")
			for i in range(0, 1024):
				pv.write("\000")
			pv.close()
		except Exception, err:
			raise cairn.Exception("Failed to zero Physical Volume %s" % dev, err)
		return


	def createPV(self, sysdef, pvElem, vgfiles):
		dev = pvElem.getText()
		vg = pvElem.getAttr("vg")
		cmd = "%s --restorefile %s -u %s %s" % \
			  (sysdef.info.get("env/tools/pvcreate"), vgfiles[vg],
			   pvElem.getAttr("uuid"), dev)
		(status, output) = commands.getstatusoutput(cmd)
		cairn.verbose(cmd)
		cairn.verbose(output)
		if (status != 0):
			raise cairn.Exception("Failed to create Physical Volume %s: %s" %
								  (dev, output))
		return


	def saveVGFiles(self, sysdef):
		cairn.verbose("Saving vgcfgrestore files")
		vgfiles = {}
		for vg in sysdef.readInfo.getElems("hardware/lvm-cfg/vg-backups/vg"):
			cfgfile = cairn.mktemp("cairn-vgcfg-")
			name = vg.getAttr("name")
			os.write(cfgfile[0], vg.getText())
			os.close(cfgfile[0])
			vgfiles[name] = cfgfile[1]
		return vgfiles


	def restoreVG(self, sysdef, vgElem, vgfiles):
		vgname = vgElem.getText()
		cmd = "%s -f %s %s" % (sysdef.info.get("env/tools/vgcfgrestore"),
							   vgfiles[vgname], vgname)
		(status, output) = commands.getstatusoutput(cmd)
		cairn.verbose(cmd)
		cairn.verbose(output)
		if (status != 0):
			raise cairn.Exception("Failed to restore Volume Group %d: %s" %
								  (vgname, output))
		return


	def activateVG(self, sysdef, vgElem):
		vgname = vgElem.getText()
		cmd = "%s -ay %s" % (sysdef.info.get("env/tools/vgchange"), vgname)
		(status, output) = commands.getstatusoutput(cmd)
		cairn.verbose(cmd)
		cairn.verbose(output)
		if (status != 0):
			raise cairn.Exception("Failed to activate Volume Group %d: %s" %
								  (vgname, output))
		return


	def run(self, sysdef):
		cairn.log("Recreating Physical Volumes:")
		vgfiles = self.saveVGFiles(sysdef)
		for pv in sysdef.readInfo.getElems("hardware/lvm-cfg/pvs/pv"):
			cairn.displayRaw("  %s" % pv.getText())
			self.zeroPV(sysdef, pv)
			self.createPV(sysdef, pv, vgfiles)
		cairn.displayNL()
		cairn.log("Recreating Volume Groups:")
		for vg in sysdef.readInfo.getElems("hardware/lvm-cfg/vgs/vg"):
			cairn.displayRaw("  %s" % vg.getText())
			self.restoreVG(sysdef, vg, vgfiles)
			self.activateVG(sysdef, vg)
		cairn.displayNL()
		return True
