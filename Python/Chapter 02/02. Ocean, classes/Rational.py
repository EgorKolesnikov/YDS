import sys


class Rational:

    #
    #   Constructors
    #

    def __init__(self, p=0, q=1):
        self.numerator = p
        self.denominator = q
        self.normilize()

    #
    #   Arithmetical operations
    #

    def __add__(self, other):
        result = Rational(
            self.numerator * other.denominator +
            other.numerator * self.denominator,
            self.denominator * other.denominator
        )
        result.normilize()
        return result

    def __sub__(self, other):
        result = Rational(
            self.numerator * other.denominator -
            other.numerator * self.denominator,
            self.denominator * other.denominator
        )
        result.normilize()
        return result

    def __mul__(self, other):
        result = Rational(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )
        result.normilize()
        return result

    def __div__(self, other):
        result = Rational(
            self.numerator * other.denominator,
            self.denominator * other.numerator
        )
        result.normilize()
        return result

    #
    #   == and != operators, converting to string, unary minus
    #

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __eq__(self, other):
        self.normilize()
        other.normilize()
        return (self.numerator == other.numerator and
                self.denominator == other.denominator)

    def __ne__(self, other):
        return not self == other

    #
    #   Subsidiary methods like compute gcd
    #   and normilize Rational number
    #

    def gcd(self):
        a = abs(self.numerator)
        b = abs(self.denominator)
        while (b):
            a %= b
            a, b = b, a
        return a

    def normilize(self):
        g = self.gcd()
        self.numerator /= g
        self.denominator /= g

        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = - self.denominator


exec(sys.stdin.read())
