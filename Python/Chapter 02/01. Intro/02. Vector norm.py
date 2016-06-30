def Norm(p, vector):
	result = 0
	for i in xrange(len(vector)):
		result += pow(abs(vector[i]), p)
	return pow(result, (1.0 / p))

p = int(input())
vector = raw_input().split()
for i in xrange(len(vector)):
	vector[i] = float(vector[i])
print Norm(p, vector)