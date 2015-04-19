__author__ = 'yxy'

import re
from functools import reduce
from operator import mul

_POLYNOMIAL_FORMAT = re.compile(r"""
    \s*
    (?P<sign>[-+]?)
    \s?
    (?P<coefficient>[0-9]+)
    (?P<x>\*?x(?:\^(?P<exponent>[0-9]+))?)?
""", re.VERBOSE)


class Poly(object):

    def __init__(self, form=None):
        self.poly = {}
        if form is not None:
            if isinstance(form, str):
                for match in re.finditer(_POLYNOMIAL_FORMAT, form):
                    if match.group("x") is None:
                        if match.group("sign") != '-':
                            self.poly[0] = self.poly.get(0, 0) + int(match.group("coefficient"))
                        else:
                            self.poly[0] = self.poly.get(0, 0) - int(match.group("coefficient"))
                    else:
                        try:
                            exp = int(match.group("exponent"))
                        except TypeError:
                            exp = 1
                        if match.group("sign") != '-':
                            self.poly[exp] = self.poly.get(exp, 0) + int(match.group("coefficient"))
                        else:
                            self.poly[exp] = self.poly.get(exp, 0) - int(match.group("coefficient"))
            elif isinstance(form, list):
                for index, coeff in enumerate(form):  # interpreted as a series starting from exponent 0
                    if coeff != 0:
                        self.poly[index] = coeff
            else:
                raise TypeError("argument must either be a string or a list")

    def add_single_component(self, exponent, coefficient):
        self.poly[exponent] = self.poly.get(exponent, 0) + coefficient
        if self.poly[exponent] == 0:
            del self.poly[exponent]

    def __add__(self, other):
        if isinstance(other, (int, float)):
            result = self.copy()
            result.add_single_component(0, other)
            return result
        elif isinstance(other, Poly):
            result = self.copy()
            for exp, coeff in other.poly.items():
                result.add_single_component(exp, coeff)
            return result
        else:
            raise TypeError("unsupported type for +")

    __radd__ = __add__

    def __neg__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + (-other)

    def _scalar_mul(self, a):
        for exp in self.poly:
            self.poly[exp] *= a

    @staticmethod
    def _single_component_mul(exp_a, coeff_a, exp_b, coeff_b):
        result = Poly()
        result.add_single_component(exp_a + exp_b, coeff_a * coeff_b)
        return result

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = self.copy()
            result._scalar_mul(other)
            return result
        elif isinstance(other, Poly):
            result = 0
            for exp_a, coeff_a in self.poly.items():
                for exp_b, coeff_b in other.poly.items():
                    result += Poly._single_component_mul(exp_a, coeff_a, exp_b, coeff_b)
            return result
        else:
            raise TypeError("unsupported type for *")

    __rmul__ = __mul__

    def __eq__(self, other):
        for exp in (set(self.poly.keys()) | set(other.poly.keys())):
            if self.poly.get(exp, 0) != other.poly.get(exp, 0):
                return False
        return True

    def degree(self):
        return max(self.poly.keys())

    def application(self, x):
        result = 0
        for exp, coeff in self.poly.items():
            result += coeff * x ** exp
        return result

    def power_series(self):
        coefficients = []
        for exp in range(max(self.poly.keys()) + 1):
            coefficients.append(self.poly.get(exp, 0))
        return coefficients

    @classmethod
    def optimal_fit(cls, fit):
        result = cls()
        for index, i in enumerate(fit):
            increment = reduce(mul, [cls([-j, 1]) for j in range(1, index+1)], Poly([1]))
            times = (i - result.application(index+1)) / increment.application(index+1)
            result += increment * times
        return result

    def derivative(self):
        result = Poly()
        for exp, coeff in self.poly.items():
            result.add_single_component(exp-1, coeff*exp)
        return result

    def copy(self):
        poly_copy = Poly()
        poly_copy.poly = self.poly.copy()
        return poly_copy

    def __str__(self):
        poly_str = ""
        for exp in sorted(self.poly.keys(), reverse=True):
            if self.poly[exp] > 0:
                if exp == 1:
                    component = "+ " + str(self.poly[exp]) + "x "
                elif exp == 0:
                    component = "+ " + str(self.poly[exp])
                else:
                    component = "+ " + str(self.poly[exp]) + "x^" + str(exp) + " "
                poly_str += component
            elif self.poly[exp] < 0:
                if exp == 1:
                    component = "- " + str(-self.poly[exp]) + "x "
                elif exp == 0:
                    component = "- " + str(-self.poly[exp])
                else:
                    component = "- " + str(-self.poly[exp]) + "x^" + str(exp) + " "
                poly_str += component
        poly_str = poly_str.rstrip(" ").lstrip("+ ")
        return poly_str
