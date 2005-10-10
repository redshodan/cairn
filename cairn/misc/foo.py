#!/usr/bin/env python

def handle(script, path, query, post_data, post_len):
    print "PYTHON: script=%s path=%s query=%s postData=%s postLen=%d\n" % (script, path, query, post_data, post_len)
    return "<html><body><p>python-fu!</body></html>"
