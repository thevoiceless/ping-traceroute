#!/usr/bin/python

import sys
import subprocess
import signal

# Register a signal handler to handle Control+C, exit with return code 3
def signal_handler(signal, frame):
    sys.exit(3)
signal.signal(signal.SIGINT, signal_handler)

# User must provide a hostname and TTL value, otherwise return code 1
def printCorrectUsage():
	print "Usage: ./ping.py <hostname> <TTL>"

# Get command-line arguments
numArgs = len(sys.argv)
argsList = sys.argv

# Check for correct usage

if numArgs != 3:
	printCorrectUsage()
	exit(1)

# Build the command to be executed
command = 'ping'
hostname = argsList[1]
ttyVal = argsList[2]
countArg = '-c1'
ttyArg = '-t' + ttyVal
pingCommand = ['ping', hostname, countArg, ttyArg]

# Ping and get result
p = subprocess.Popen(pingCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pingResult = p.communicate()
pingOutputText = pingResult[0].strip()
pingErrorText = pingResult[1]
pingReturnCode = p.returncode

# Check the result by searching for specific text in the output
# This is probably a terrible solution because it will break if the ping output varies at all
# Unfortunately, a return code of 1 could mean two things:
#     1. The host did not respond
#     2. The TTL was exceeded
# Key text for TTL exceeded
key_ttlExceededText = 'Time to live exceeded'
# Key text preceding the domain
# "From" is capitalized in the output when the packet expires, but lowercase otherwise
key_textBeforeDomain = 'rom '
# Key text following the domain
# Include the preceding whitespace
key_textAfterDomain = ' icmp_'

# Search for the keys
domainTextStartLoc = pingOutputText.find(key_textBeforeDomain) + len(key_textBeforeDomain)
domainTextEndLoc = pingOutputText.find(key_textAfterDomain)

# Ping return code is 0 if the destination is reached
if pingReturnCode == 0:
	# Subtract 1 from domainTextEndLoc to trim the ":" from the output
	print "Destination \"" + hostname + "\" reached: " + pingOutputText[domainTextStartLoc:domainTextEndLoc - 1]
	# Everything went according to plan, exit with return code 0
	exit(0)
# Ping return code is 1 if there was a problem reaching the given hostname
elif pingReturnCode == 1:
	print "Hop " + ttyVal + ":\t",
	# If the TTL was not exceeded, assume the domain is not responding and exit with return code 2
	if domainTextEndLoc == -1:
		print "Host not responding to ping"
		exit(2)
	# If the TTL was exceeded, print the last domain and exit with return code 1
	else:
		print pingOutputText[domainTextStartLoc:domainTextEndLoc]
		exit(1)
# Return code is 2 if there was a problem executing ping, print the error and correct usage
elif pingReturnCode == 2:
	print "Error:", pingErrorText
	printCorrectUsage()