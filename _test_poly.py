__author__ = 'yxy'

from polynomial import Poly


def main():
    p = Poly("-312*x^2 +13x^3")
    print("p =", p)
    print("p(10) =", p.application(10))
    print("2p =", p*2)
    print()

    q = Poly("9x^20 + 5 - 5x^3 + 1x")
    print("q =", q)
    print("-q =", -q)
    print("q coefficients:", q.power_series())
    print()

    r = Poly("7 - 3*x^5 + 10*x - 5")
    print("r =", r)
    print()

    s = Poly("1 - 1x + 1x^2 - 1x^3 + 1x^4")
    print("s =", s)
    print()

    s_ = Poly("1 - 1x + 1x^2 - 1x^3 + 1x^4 - 1x^5 + 1x^6 - 1x^7 + 1x^8 - 1x^9 + 1x^10")
    print("s_ =", s_)
    print()

    t = Poly([1, -2, 3, 4, -5, 6])
    print("t =", t)
    print()

    u = Poly.optimal_fit([1, 8, 27, 64])
    print("u =", u)
    print()

    print("p == q:", p == q)
    print("p + q =", p + q)
    print("p - q =", p - q)
    print("p * q =", p * q)
    print()

    target = Poly("1 - 1x + 1x^2 - 1x^3 + 1x^4 - 1x^5 + 1x^6 - 1x^7 + 1x^8 - 1x^9 + 1x^10")
    print(target)
    print(target.derivative())
    print()


if __name__ == '__main__':
    main()
