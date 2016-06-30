import sys

def doWork(max_len, text):
	while text.find('  ') != -1:
		text = text.replace('  ', ' ')
	text = text.strip()
	text += '\n'

	index = 0
	count_length = 0
	while index != len(text):
		if text[index] == '\n':
			count_length = 0
			index += 1
			continue
		else:
			count_length += 1

		if count_length > max_len:
			if text[index].isspace():
				text = text[:index] + '\n' + text[index + 1:]
			else:
				copy = index
				while index >=0 and not text[index].isspace():
					index -= 1
				if text[index] == '\n':
					index = copy
					while not text[index].isspace():
						index += 1
					if text[index] != '\n':
						text = text[:index] + '\n' + text[index + 1:]	
				else:
					if text[index] == ' ':
						text = text[:index] + '\n' + text[index + 1:]
					else:						
						index = copy
						while not text[index].isspace():
							index += 1
						text = text[:index] + '\n' + text[index + 1:]
			count_length = 0
		index += 1
	return text[:-1]
	

text = ""
max_len = int(input())
line = sys.stdin.readline()
while line:
	text = text + line
	line = sys.stdin.readline()

result = doWork(max_len, text)
print result