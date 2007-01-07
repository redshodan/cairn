"""cairn.ExceptionReporter"""



import cairn
from cairn import Options
from cairn import Logging


# This is ultra super secret! Its so important that I almost closed sourced
# cairn because of this. This will make it **IMPOSSIBLE** for spammers to
# spam the CGI script that will be waiting for these reports. Totally
# absolutely impossible.... ok ok ok .. enough of that. So yeah, just a very
# stupidly basic effort to cut off the lazy spammers.
__ultraSuperSecretKey = "thEgREeAtaNdaLmIgHtycaIrNseCrEtkEyZ0r"

__reportServer = "cairn-project.org"
__reportPath = "/autoExReport"



def report(msg):
	global __reportServer, __reportPath, __ultraSuperSecretKey
	# Try to prevent early exceptions from totally breaking everything
	# because the base framework is not all setup yet.
	try:
		import httplib
		try:
			conn = httplib.HTTPSConnection(__reportServer)
		except:
			conn = httplib.HTTPConnection(__reportServer)
		Logging.shutdown()
		content = ""
		if Logging.getAllLogFile():
			logfile = file(Logging.getAllLogFile(), "r")
			content = logfile.read()
			logfile.close()
		content = "%s\n%s" % (content, msg)
		#conn.set_debuglevel(10)
		conn.request("POST", __reportPath, content,
					 {"CAIRN-Key" :__ultraSuperSecretKey})
		resp = conn.getresponse()
		code = resp.status
		reason = resp.reason
		conn.close()
		return (code, reason)
	except Exception, err:
		return str(err)
	return None
