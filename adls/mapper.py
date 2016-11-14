#!/usr/bin/env python
"""This is a python mapper that generate files and folder structures based on the provided input.
	The expected input is a csv of filepath,size_in_bytes
"""

import sys
import os
import subprocess
import uuid
import re

def read_input(file):
	for line in file:
		# split the line into filepath and size
		yield line.split(",")

def main():
	# input comes from STDIN (standard input)
	data = read_input(sys.stdin)
	for (filepath, size) in data:
	path, filename = os.path.split(filepath)
	print filename
	print path
	print size
	size = re.sub("[^0-9]", "", size)
	random_temp_name = str(uuid.uuid4()).replace("-","") + ".tmp"
	# generate file
	process = subprocess.Popen(['/bin/dd', 'if=/dev/urandom', 'of='+random_temp_name, ('bs=%s' % size), 'count=1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	process.wait()
	
	process = subprocess.Popen(['/usr/bin/hdfs', 'dfs', '-mkdir', '-p','adl://<adls account>.azuredatalakestore.net/'+path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	process.wait()

	process = subprocess.Popen(['/usr/bin/hdfs', 'dfs', '-copyFromLocal', random_temp_name, 'adl://<adls account>.azuredatalakestore.net/'+filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	process.wait()
	
	process = subprocess.Popen(['/bin/rm', random_temp_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	process.wait()

if __name__ == "__main__":
    main()
