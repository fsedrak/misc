#!/usr/bin/env python
import sys
import os
import re
import string

def main(filename, target_location):
	lines_per_file = 10000  # Lines on each small file
	lines = []  # Stores lines not yet written on a small file
	lines_counter = 0  # Same as len(lines)
	created_files = 0  # Counting how many small files have been created

	with open(filename) as big_file:
		path, filenamepart = os.path.split(filename)
		filepart, ext = filenamepart.split(".")
		for line in big_file:  # Go throught the whole big file
			line = filter(lambda x: x in string.printable, line)
			lines.append(line.replace("\r", "").replace("\n",""))
			lines_counter += 1
			if lines_counter == lines_per_file:
				idx = lines_per_file * (created_files + 1)
				with open('%s/%s_%s.%s' % (target_location, filepart, idx, ext), 'w') as small_file:
					# Write all lines on small file
					small_file.write(os.linesep.join(lines))
				lines = []  # Reset variables
				lines_counter = 0
				created_files += 1  # One more small file has been created
		# After for-loop has finished
		if lines_counter:  # There are still some lines not written on a file?
			idx = lines_per_file * (created_files + 1)
			with open('%s/%s_%s.%s' % (target_location, filepart, idx, ext), 'w') as small_file:
				# Write them on a last small file
				small_file.write('n'.join(lines))
			created_files += 1

	print '%s small files (with %s lines each) were created.' % (created_files,
                                                             lines_per_file)

if __name__ == "__main__":
    print "Splitting %s, target location %s" % (sys.argv[1], sys.argv[2])
    main(sys.argv[1], sys.argv[2])

