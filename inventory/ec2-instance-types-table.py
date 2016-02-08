#!/usr/bin/python

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# By Ilya Sher, Coding-Knight LTD.

# Quick hack to create CSV containing AWS EC2 instance types
# with their properties. This format is more convenient (at least for me)
# than the types page.

# 1. No warranties whatsoever!
# 2. Note that "micro" is "up to 2" EC2 Compute units, not "2"

# Prerequisites:
# * save http://aws.amazon.com/ec2/instance-types/
#   as 'Downloads/Amazon EC2 Instance Types.html'

import os, re

REGEXES = (
	'<p style="padding-left:2em;"><strong>(.*) Instance',
	'>(.*?) .iB.*memory',
	'(\d+) EC2 Compute Unit',
	'(.*) storage',
	'I/O Performance: (.*?)<',
	'EBS-Optimized Available: (.*?)<',
	'API name: (.*?)<',
)

REGEXES_N = len(REGEXES)

FNAME = os.path.join(
	os.getenv('HOME'),
	'Downloads/Amazon EC2 Instance Types.html'
)

regex_ptr = 0
print "Name , Memory , EC2 Compute units , Storage , I/O performance , EBS-Optimized Available , API name"
for line in open(FNAME):
	m = re.search(REGEXES[regex_ptr], line)
	if m:
		print m.group(1).replace(',', ''),
		regex_ptr = regex_ptr + 1
		if regex_ptr == REGEXES_N:
			regex_ptr = 0
			print
		else:
			print ",",
