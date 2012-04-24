#!/usr/local/bin/python2.2
def daemonize():
	""" Become a daemon"""
	import os,sys
	if os.fork(): os._exit(0)
	os.setsid()
	sys.stdin  = sys.__stdin__  = open('/dev/null','r')
	sys.stdout = sys.__stdout__ = open('/dev/null','w')
	sys.stdout = sys.__stderr__ = os.dup(sys.stdout.fileno())

def daemonize_log_watcher():
	import time, os, re, smtplib

	""" Configs.  Should  probably move these to a config file?  or take args? """
	log_filename = 	'/var/log/php_errors.log'
	search_keywords = ['PHP Parse error', 'PHP Fatal error']
	mailserver = 'localhost'
	From = 'py_log_watch@example.com'
	To = 'email@example.com'
	Subj = 'Log Watcher Alert'
	
	""" Open File, get last mod time """
	file = open(log_filename, 'r')
	watcher = os.stat(log_filename)
	this_modified = last_modified = watcher.st_mtime
	
	""" Go to the end of the file """
	file.seek(0,2)	
	
	""" Main Loop """
	while 1:
		if this_modified > last_modified:
			last_modified = this_modified
			""" File was modified, so read new lines, look for error keywords """
			while 1:
				line = file.readline()
				if not line: break	
				for keyword in search_keywords:
					if re.search(keyword, line):
						text = ('From: %s\nTo: %s\nSubject: %s\n' % (From, To, Subj)) + line
						server = smtplib.SMTP(mailserver)
						failed = server.sendmail(From, To, text)
						server.quit()
							
		
		watcher = os.stat(log_filename)
		this_modified = watcher.st_mtime
		time.sleep(1)

if __name__=='__main__':
	daemonize()
	daemonize_log_watcher()
