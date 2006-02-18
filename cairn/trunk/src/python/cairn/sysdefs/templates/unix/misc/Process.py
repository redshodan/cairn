"""cairn.sysdefs.templates.unix.misc.Process"""


import os

import cairn



class ProcessInfo(object):
	def __init__(self):
		self.name = None
		self.pid = None
		self.stdin = None
		self.stdout = None
		self.stderr = None
		self.err = ""
		self.exitCode = 0
		return


	def wait(self):
		cairn.verbose("Waiting on: %s" % (self.name))
		self.close()
		try:
			self.exitCode = os.waitpid(self.pid, 0)[1]
		except Exception, err:
			raise cairn.Exception("Failed to wait for process %s: %s" % \
								  (self.name, err))
		return


	def close(self):
		try:
			os.close(self.stdin)
		except:
			pass
		try:
			os.close(self.stdout)
		except:
			pass
		try:
			os.close(self.stderr)
		except:
			pass


	def exit(self):
		return os.WEXITSTATUS(self.exitCode)



def startCmd(name, cmd, stdin, stdout, stderr):
	cairn.verbose("Running: %s" % (cmd))
	if not stdin:
		pstdin = os.pipe()
	if not stdout:
		pstdout = os.pipe()
	if not stderr:
		pstderr = os.pipe()
	pid = os.fork()
	if pid == 0:
		if stdin:
			os.dup2(stdin, 0)
		else:
			os.dup2(pstdin[0], 0)
			os.close(pstdin[0])
			os.close(pstdin[1])
		if stdout:
			os.dup2(stdout, 1)
		else:
			os.dup2(pstdout[1], 1)
			os.close(pstdout[0])
			os.close(pstdout[1])
		if stderr:
			os.dup2(stderr, 2)
		else:
			os.dup2(pstderr[1], 2)
			os.close(pstderr[0])
			os.close(pstderr[1])
		arr = cmd.split()
		os.execv(arr[0], arr)
		raise cairn.Exception("Failed to exec command: %s" % (cmd))
	else:
		ret = ProcessInfo()
		ret.name = name
		ret.pid = pid
		if stdin:
			ret.stdin = stdin
		else:
			ret.stdin = pstdin[1]
			os.close(pstdin[0])
		if stdout:
			ret.stdout = stdout
		else:
			ret.stdout = pstdout[0]
			os.close(pstdout[1])
		if stderr:
			ret.stderr = stderr
		else:
			ret.stderr = pstderr[0]
			os.close(pstderr[1])
		return ret
	return
