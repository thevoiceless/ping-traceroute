Riley Moses
============
This is a repository for my Project 1 work in CSCI442 (Operating Systems) at Colorado School of Mines.

Files
----------
* `/src/ping.py`: A Python script that calls the ping command with a given hostname and TTL value  
* `/src/tracert.sh`: A Bash script that successively calls ping.py with a given hostname, increasing the TTL value each time  
* `/src/tracert-*.txt`: The output of running tracert.sh with 6 different hostnames, all but one of which is given in the filename. "tracert-longest.txt" is a file containing the longest route that I was able to find, which as of right now is to hash.phelix.lv

Behavior
----------
Both ping.py and tracert.sh are written to fail as fast as possible. Both will inform the user of incorrect arguments and/or usage, including any error messages from running the ping command. When running tracert.sh, it looks for ping.py in two locations: The directory in which tracert.sh is saved, and the directory from which it is being called. This wasn't a requirement for the project, just something I wanted to try. If a host does not respond 5 times in a row, tracert.sh will inform the user and then exit.

Other
----------
This project took approximately 5-6 hours, including testing and refinement. The basic requirements probably only took a couple of hours.