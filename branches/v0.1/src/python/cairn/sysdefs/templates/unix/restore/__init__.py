"""templates.unix.restore"""



def getSubModuleString(sysdef):
	return "..archive.readmeta; resolve; setup; ..archive.read; adjust; bootloader; cleanup; DisplayDone;"
