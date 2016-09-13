#!/usr/bin/python

import sys

d = sys.argv[1]
f = open(d)
zeile = f.readlines()
anz = len(zeile)
Verb1 = False
neueVerb = False
dual = False
count = 0
result = ''
print 'Datei ist ' + d
for i in zeile:
	if i == 'Verbindungen 1\n':
		Verb1 = True
		continue
	if i[0:4] == 'Verb' and i != 'Verbindungen 1\n' and i != 'Verbindungen 2 dual\n':
		print result
		neueVerb = True
		Verb1 = False
		result = ''
		continue
	if i == 'Verbindungen 2 dual\n':
		print result
		dual = True
		neueVerb = True
		result = ''
		continue
	if Verb1:
		if i[0:10] == '[  3]  0.0':
			tmps = i.split()
			
			result = '0.' + tmps[4] + ', ,' + tmps[6]
			continue
		if 'packets sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'connections opened' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[3]
			continue
		if 'dupacks sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'rexmits sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'average RTT' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[2]
			continue

	if neueVerb:
		if i[0:10] == '[SUM]  0.0':
			tmps = i.split()
			
			if dual:
				count += 1
				if count == 1:
					result = ' ,' + tmps[5]
				if count == 2:
					result = result + ', ' + tmps[5]
					dual = False
				continue
			else:
				result = '0.' +  tmps[3] + ', ,' + tmps[5]
				continue
		if 'packets sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'connections opened' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[3]
			continue
		if 'dupacks sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'rexmits sent' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[0] + ', ' + tmps[3]
			continue
		if 'average RTT' in i:
			tmps = i.split()
			
			result = result + ', ' + tmps[2]
			continue
print result
result = ''
f.close()
 
