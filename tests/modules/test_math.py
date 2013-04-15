import math

from ..base import BaseTopazTest


class TestMath(BaseTopazTest):
    def assert_float_equal(self, result, expected, eps=1e-15):
        assert abs(result - expected) < eps

    def test_domain_error(self, space):
        space.execute("Math::DomainError")

    def test_pi(self, space):
        w_res = space.execute("return Math::PI")
        assert space.float_w(w_res) == math.pi

    def test_e(self, space):
        w_res = space.execute("return Math::E")
        assert space.float_w(w_res) == math.e

    def test_acos(self, space):
        w_res = space.execute("return [Math.acos(0), Math.acos(1)]")
        assert self.unwrap(space, w_res) == [math.acos(0), 0]

    def test_acosh(self, space):
        w_res = space.execute("return [Math.acosh(1), Math.acosh(2)]")
        assert self.unwrap(space, w_res) == [0, math.acosh(2)]

        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "acosh"'):
            space.execute("Math.acosh(0)")

    def test_asin(self, space):
        w_res = space.execute("return [Math.asin(0), Math.asin(1)]")
        assert self.unwrap(space, w_res) == [0, math.asin(1)]

    def test_asinh(self, space):
        w_res = space.execute("return [Math.asinh(0), Math.asinh(1)]")
        assert self.unwrap(space, w_res) == [math.asinh(0), math.asinh(1)]

    def test_atan(self, space):
        w_res = space.execute("return [Math.atan(0), Math.atan(1)]")
        assert self.unwrap(space, w_res) == [0, math.atan(1)]

    def test_atan2(self, space):
        w_res = space.execute("return [Math.atan2(-0.0, -1.0), Math.atan2(-1, -1.0)]")
        assert self.unwrap(space, w_res) == [math.atan2(-0.0, -1.0), math.atan2(-1.0, -1)]

    def test_atanh(self, space):
        w_res = space.execute("return [Math.atanh(1), Math.atanh(-1), Math.atanh(0), Math.atanh(0.5)]")
        assert self.unwrap(space, w_res) == [float("inf"), float("-inf"), 0, math.atanh(0.5)]

        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "atanh"'):
            space.execute("Math.atanh(2)")

    def test_cbrt(self, space):
        w_res = space.execute("return [Math.cbrt(-8), Math.cbrt(-1), Math.cbrt(0)]")
        assert self.unwrap(space, w_res) == [-2.0, -1.0, 0]

        w_res = space.execute("return Math.cbrt(8)")
        self.assert_float_equal(space.float_w(w_res), 2.0)

        w_res = space.execute("return Math.cbrt(64)")
        self.assert_float_equal(space.float_w(w_res), 4.0)

    def test_cos(self, space):
        w_res = space.execute("return [Math.cos(0), Math.cos(1)]")
        assert self.unwrap(space, w_res) == [1, math.cos(1)]

    def test_cosh(self, space):
        w_res = space.execute("return [Math.cosh(0), Math.cosh(1), Math.cosh(123123)]")
        assert self.unwrap(space, w_res) == [1, math.cosh(1), float("inf")]

    def test_exp(self, space):
        w_res = space.execute("return [Math.exp(0.0), Math.exp(1)]")
        assert self.unwrap(space, w_res) == [1, math.exp(1)]

    def test_frexp(self, space):
        w_res = space.execute("return Math.frexp(1234)")
        assert self.unwrap(space, w_res) == [math.frexp(1234)[0], 11]

    def test_gamma(self, space):
        w_res = space.execute("return Math.gamma(5.0)")
        self.assert_float_equal(space.float_w(w_res), 24.0)

        w_res = space.execute("return Math.gamma(6.0)")
        self.assert_float_equal(space.float_w(w_res), 120.0)

        w_res = space.execute("return Math.gamma(0.5)")
        self.assert_float_equal(space.float_w(w_res), math.pi ** 0.5)

        w_res = space.execute("return Math.gamma(1000)")
        assert space.float_w(w_res) == float("inf")

        w_res = space.execute("return Math.gamma(0.0)")
        assert space.float_w(w_res) == float("inf")

        w_res = space.execute("return Math.gamma(-0.0)")
        assert space.float_w(w_res) == float("-inf")

        w_res = space.execute("return Math.gamma(Float::INFINITY)")
        assert space.float_w(w_res) == float("inf")

        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "gamma"'):
            space.execute("""Math.gamma(-1)""")
        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "gamma"'):
            space.execute("""Math.gamma(-Float::INFINITY)""")

        w_res = space.execute("return Math.gamma(Float::NAN)")
        assert math.isnan(space.float_w(w_res))

    def test_hypot(self, space):
        w_res = space.execute("return Math.hypot(3, 4)")
        assert self.unwrap(space, w_res) == 5

    def test_ldexp(self, space):
        w_res = space.execute("return Math.ldexp(Math.frexp(1234)[0], 11)")
        assert self.unwrap(space, w_res) == 1234

        w_expected = space.execute("Math.ldexp(1, 2)")
        expected = self.unwrap(space, w_expected)
        w_actual = space.execute("Math.ldexp(1, 2.3)")
        actual = self.unwrap(space, w_actual)
        assert expected == actual

    def test_log(self, space):
        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "log"'):
            space.execute("Math.log(-1)")

        w_res = space.execute("return Math.log(0)")
        assert space.float_w(w_res) == float("-inf")

        w_res = space.execute("return Math.log(4, 10)")
        self.assert_float_equal(space.float_w(w_res), math.log(4, 10))

        w_res = space.execute("return Math.log(28)")
        self.assert_float_equal(space.float_w(w_res), math.log(28))

        w_res = space.execute("return Math.log(3, 4)")
        self.assert_float_equal(space.float_w(w_res), math.log(3, 4))

    def test_log10(self, space):
        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "log10"'):
            space.execute("Math.log10(-1)")

        w_res = space.execute("return Math.log10(0)")
        assert space.float_w(w_res) == float("-inf")

        w_res = space.execute("return Math.log10(1)")
        assert space.float_w(w_res) == 0.0

        w_res = space.execute("return Math.log10(10)")
        assert space.float_w(w_res) == 1.0

    def test_log2(self, space):
        with self.raises(space, "Math::DomainError", 'Numerical argument is out of domain - "log2"'):
            space.execute("Math.log2(-1)")

        w_res = space.execute("return Math.log2(0)")
        assert space.float_w(w_res) == float("-inf")

        w_res = space.execute("return Math.log2(1)")
        assert space.float_w(w_res) == 0.0

        w_res = space.execute("return Math.log2(2)")
        assert space.float_w(w_res) == 1.0

        w_res = space.execute("return Math.log2(32768)")
        assert space.float_w(w_res) == 15.0

        w_res = space.execute("return Math.log2(65536)")
        assert space.float_w(w_res) == 16.0

    def test_sin(self, space):
        w_res = space.execute("return [Math.sin(0), Math.sin(1)]")
        assert self.unwrap(space, w_res) == [0, math.sin(1)]

    def test_sinh(self, space):
        w_res = space.execute("return [Math.sinh(0), Math.sinh(2), Math.sinh(1234)]")
        assert self.unwrap(space, w_res) == [0, math.sinh(2), float("inf")]

    def test_sqrt(self, space):
        w_res = space.execute("return [Math.sqrt(4), Math.sqrt(28)]")
        assert self.unwrap(space, w_res) == [2, math.sqrt(28)]

    def test_tan(self, space):
        w_res = space.execute("return Math.tan(Float::INFINITY)")
        assert math.isnan(space.float_w(w_res))

        w_res = space.execute("return [Math.tan(0), Math.tan(1)]")
        assert self.unwrap(space, w_res) == [0, math.tan(1)]

    def test_tanh(self, space):
        w_res = space.execute("return [Math.tanh(0), Math.tanh(1), Math.tanh(1234)]")
        assert self.unwrap(space, w_res) == [0, math.tanh(1), 1.0]

    def test_type_error(self, space):
        for funcname in ["acos", "acosh", "asin", "asinh", "atan",
                         "atanh", "cbrt", "cos", "cosh", "exp",
                         "frexp", "gamma", "log", "log10", "log2",
                         "sin", "sinh", "sqrt", "tan", "tanh"]:
            with self.raises(space, "TypeError",
                             "can't convert String into Float"):
                space.execute("Math.%s('some String')" % funcname)
            with self.raises(space, "TypeError",
                             "can't convert Symbol into Float"):
                space.execute("Math.%s(:some_Symbol)" % funcname)
        for funcname in ["ldexp", "hypot", "atan2"]:
            with self.raises(space, "TypeError",
                             "can't convert String into Float"):
                space.execute("Math.%s('some String', 1)" % funcname)
                space.execute("Math.%s(2.0, 'some String')" % funcname)
            with self.raises(space, "TypeError",
                             "can't convert Symbol into Float"):
                space.execute("Math.%s(:some_Symbol, 3)" % funcname)
                space.execute("Math.%s(4.0, :some_Symbol)" %funcname)

    def test_argument_error(self, space):
        for funcname in ["ldexp", "hypot", "atan2"]:
            with self.raises(space, "ArgumentError"):
                space.execute("Math.%s(:some_Symbol)" %funcname)
