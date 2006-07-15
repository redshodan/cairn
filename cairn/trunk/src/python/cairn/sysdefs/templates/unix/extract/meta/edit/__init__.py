"""templates.unix.extract.meta.edit"""


from cairn import Options


def getSubModuleString(sysdef):
	if Options.get("edit-meta"):
		return "PrepMetaForEdit; RunEditor; ReReadMeta; ..archive.mergemeta;"
	else:
		return None
