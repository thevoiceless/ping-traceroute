#!/bin/bash

# Check for correct usage
if [[ $# -ne 1 ]]
then
	echo "Usage: ./tracert.sh <hostname>"
	exit 1
fi

# Host name is the first (and only) argument
hostname=$1
# Name of the ping script to use
pingScriptName="ping.py"
# Directory that this script is called from
calledFromDir=`pwd`
# Directory that this script is saved in
scriptDir=`readlink -f \`dirname $0\``

# Check that the ping script exists in either
#     1. The directory that this script is called from, or
#     2. The directory that this script is saved in
# Just a bit of needless flexibility
if [[ -f ${calledFromDir}/${pingScriptName} ]]
then
	pingScript=${calledFromDir}/${pingScriptName}
elif [[ -f ${scriptDir}/${pingScriptName} ]]
then
	pingScript=${scriptDir}/${pingScriptName}
else
	echo "$pingScriptName not found"
	exit 1
fi

# Initial TTY
(( ttyCounter = 1 ))
# A bogus initial return code
(( returnCode = 1337 ))
# The number of times the hostname has not responded to ping
(( notRespondingCount = 0 ))

# Loop until the destination is reached (return code of 0)
until [[ $returnCode -eq 0 ]]
do
	# Run the ping script
	$pingScript $hostname $ttyCounter
	# Store the return code
	returnCode=$?
	# Return code of 3 means the user pressed Control+C, exit
	if [[ $returnCode -eq 3 ]]
	then
		exit 3
	# Return code of 2 means that the hostname did not respond, increment notRespondingCount
	elif [[ $returnCode -eq 2 ]]
	then
		(( notRespondingCount++ ))
		# Exit after 5 counts of the host not responding
		if [[ notRespondingCount -ge 5 ]]
		then
			echo "Host did not respond the last 5 tries, giving up"
			exit 2
		fi
	# Reset notRespondingCount if needed
	elif [[ $returnCode -eq 1 ]]
	then
		(( notRespondingCount = 0 ))
	fi
	# Increment the TTY counter
	(( ttyCounter++ ))
done