"""templates.unix.extract"""



from cairn import Options



def getSubModuleString(sysdef):
	str = "..archive.readmeta; "
	if Options.get("edit-meta"):
		return str + "meta.edit;"
	elif Options.get("replace-meta"):
		return str + "meta.Replace; ..archive.mergemeta;"
	elif Options.get("save-meta"):
		return str + "meta.Save;"
	elif Options.get("unshar"):
		return str + "meta.unshar;"
	else:
		# extract files
		return "..archive.read;"
