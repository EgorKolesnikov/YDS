import sys

def compare(e1, e2):
	if e1[1] < e2[1] or (e1[1] == e2[1] and e1[0] > e2[0]):
		return 1
	return -1

def mapping(lines):
	result = {}
	for line in lines:
		line = line.rstrip('\n')
		for symbol in line:
			if symbol.isalpha():
				if symbol.lower() in result:
					result[symbol.lower()] += 1
				else:
					result[symbol.lower()] = 1
	items = result.items()
	result = sorted(items, cmp=compare)
	return result

lines = sys.stdin.readlines()
result = mapping(lines)
for el in result:
	print str(el[0]) + ": " + str(el[1])