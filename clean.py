import re
import sys
import unicodecsv as csv
regex = re.compile("(?P<location>.+)\s+\((?P<from>\w+)\W(?P<to>\w+)\)\W+(?P<state>[A-Z]{2})")
DIGITS = re.compile("[0-9]{4}")

writer = csv.DictWriter(sys.stdout, fieldnames=['name', 'county', 'state', 'from', 'to'])
writer.writeheader()

for line in sys.stdin.readlines():
	match = regex.search(line)
	if match:
		doc = match.groupdict()
		if not DIGITS.search(doc['to']):
			doc['to'] = ''
		parts = doc['location'].split(', ')
		if len(parts)>1:
			doc['county'] = parts[1]
		doc['name'] = parts[0]
		del doc['location']
		writer.writerow(doc)