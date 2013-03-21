Ping-Traceroute - Riley Moses
============

Files
----------
* `/src/ping.py`: A Python script that calls the ping command with a given hostname and TTL value  
* `/src/tracert.sh`: A Bash script that successively calls ping.py with a given hostname, increasing the TTL value each time

Behavior
----------
Both ping.py and tracert.sh are written to fail as fast as possible. Both will inform the user of incorrect arguments and/or usage, including any error messages from running the ping command. When running tracert.sh, it looks for ping.py in two locations: The directory in which tracert.sh is saved, and the directory from which it is being called. If a host does not respond 5 times in a row, tracert.sh will inform the user and then exit.