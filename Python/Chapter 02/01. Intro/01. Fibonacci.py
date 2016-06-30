def Fibonacci(n):
	f_2 = 0
	f_1 = 1
	f_n = 1

	if n == 0 : return f_2
	if n == 1 : return f_1

	for i in xrange(2, n + 1):
		f_n = f_2 + f_1
		f_2, f_1 = f_1, f_n

	return f_n

print Fibonacci(int(input()))