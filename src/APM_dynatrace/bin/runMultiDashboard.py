import os
import datetime
import sys
import subprocess
from xml.etree import ElementTree
import requests

from xml.dom import minidom

import lxml.etree as ET
from urllib2 import URLError, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, install_opener, build_opener


DTSERVER="192.168.1.69:8020"
#DASHBOARD="Database%20Dashboard"
DASHBOARD_LIST="filename"
TIMEFRAME="Last5Min"
USERNAME="admin"
PASSWORD="admin"

with open('DASHBOARD_LIST', 'r') as f:
	for line in f:
		run_dashboard(line)

def run_dashboard(dashboard_name):
	xsl_filename = dashboard_name + "_report.xsl"
	feed_url = "http://"+ DTSERVER + "/rest/management/reports/create/"+ dashboard_name + "?type=XML&format=XML+Export&filter=tf:" + TIMEFRAME

	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

	# Set up a HTTPS request with username/password authentication
	try:
	  file = requests.get(feed_url, auth=(USERNAME, PASSWORD))
	  file.raise_for_status()

	except Exception as e:
		if(file.status_code==404):
			print('%s: Page could not be found.' % e.reason)
		if(file.status_code>=500):
			print ('%s: Server error [%s]' % (e.reason, manifest_response.status_code))
		print 'URLError: "%s"' % e

	appdir = os.path.dirname(os.path.dirname(__file__))
	xsl_file = os.path.join(appdir, "bin", xsl_filename)
	out_dir = os.path.join(appdir,"log")

	#print >> sys.stderr, "The XSL File", xsl_file

	dom = ET.parse(file)
	#print >> sys.stderr, "The Feed file" , ET.tostring(dom, pretty_print=True)

	xslt = ET.parse(xsl_file)

	#print >> sys.stderr, "The XSLT file" , ET.tostring(xslt, pretty_print=True)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)

	print str(newdom)


	#print >> sys.stderr, "The New file" , str(newdom)



