"""templates.unix.extract.meta.edit"""


from cairn import Options


def getSubModuleString(sysdef):
	return "PrepMetaForEdit; RunEditor; ReReadMeta; ..archive.mergemeta;"
