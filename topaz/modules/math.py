from __future__ import absolute_import

import math

from rpython.rlib import rfloat

from topaz.module import Module, ModuleDef, ClassDef
from topaz.objects.exceptionobject import W_StandardError, W_TypeError, \
                                          new_exception_allocate
from rpython.rlib.rfloat import NAN
from topaz.error import RubyError

def check_type_errors(*expected_types):
    def decorator(func):
        def cte_func(self, space, args_w):
            args = []
            for expected_type, w_arg in zip(expected_types, args_w):
                exp_type = getattr(space, expected_type) # not rpython
                if space.is_kind_of(w_arg, exp_type):
                    if expected_type == "w_integer":
                        args.append(space.int_w(w_arg))
                    else:
                        args.append(space.float_w(w_arg))
                else:
                    clsname = space.getclass(w_arg).name
                    errmsg = "can't convert %s into Float" % (clsname)
                    raise space.error(space.w_TypeError, errmsg)
            return func(self, space, *args)
        cte_func.func_name = func.func_name
        return cte_func
    return decorator

class Math(Module):
    moduledef = ModuleDef("Math", filepath=__file__)

    @moduledef.setup_module
    def setup_module(space, w_mod):
        space.set_const(w_mod, "PI", space.newfloat(math.pi))
        space.set_const(w_mod, "E", space.newfloat(math.e))
        space.set_const(w_mod, "DomainError", space.getclassfor(W_DomainError))

    @moduledef.setup_module
    def setup_module(space, w_mod):
        space.set_const(w_mod, "PI", space.newfloat(math.pi))
        space.set_const(w_mod, "E", space.newfloat(math.e))
        space.set_const(w_mod, "DomainError", space.getclassfor(W_DomainError))

    @moduledef.function("acos", value="float")
    @check_type_errors("w_numeric")
    def method_acos(self, space, value):
        return space.newfloat(math.acos(value))

    @moduledef.function("acosh", value="float")
    @check_type_errors("w_numeric")
    def method_acosh(self, space, value):
        try:
            res = math.acosh(value)
        except ValueError:
            raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "acosh"')
        return space.newfloat(res)

    @moduledef.function("asin", value="float")
    @check_type_errors("w_numeric")
    def method_asin(self, space, value):
        return space.newfloat(math.asin(value))

    @moduledef.function("asinh", value="float")
    @check_type_errors("w_numeric")
    def method_asinh(self, space, value):
        return space.newfloat(math.asinh(value))

    @moduledef.function("atan", value="float")
    @check_type_errors("w_numeric")
    def method_atan(self, space, value):
        return space.newfloat(math.atan(value))

    @moduledef.function("atan2", value1="float", value2="float")
    @check_type_errors("w_numeric", "w_numeric")
    def method_atan2(self, space, value1, value2):
        return space.newfloat(math.atan2(value1, value2))

    @moduledef.function("atanh", value="float")
    @check_type_errors("w_numeric")
    def method_atanh(self, space, value):
        try:
            res = math.atanh(value)
        except ValueError:
            if value == 1.0 or value == -1.0:
                # produce an infinity with the right sign
                res = rfloat.copysign(rfloat.INFINITY, value)
            else:
                raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "atanh"')
        return space.newfloat(res)

    @moduledef.function("cbrt", value="float")
    @check_type_errors("w_numeric")
    def method_cbrt(self, space, value):
        if value < 0:
            return space.newfloat(-math.pow(-value, 1.0 / 3.0))
        else:
            return space.newfloat(math.pow(value, 1.0 / 3.0))

    @moduledef.function("cos", value="float")
    @check_type_errors("w_numeric")
    def method_cos(self, space, value):
        return space.newfloat(math.cos(value))

    @moduledef.function("cosh", value="float")
    @check_type_errors("w_numeric")
    def method_cosh(self, space, value):
        try:
            res = math.cosh(value)
        except OverflowError:
            res = rfloat.copysign(rfloat.INFINITY, value)
        return space.newfloat(res)

    @moduledef.function("exp", value="float")
    @check_type_errors("w_numeric")
    def method_exp(self, space, value):
        return space.newfloat(math.exp(value))

    @moduledef.function("frexp", value="float")
    @check_type_errors("w_numeric")
    def method_frexp(self, space, value):
        mant, exp = math.frexp(value)
        w_mant = space.newfloat(mant)
        w_exp = space.newint(exp)
        return space.newarray([w_mant, w_exp])

    @moduledef.function("gamma", value="float")
    @check_type_errors("w_numeric")
    def method_gamma(self, space, value):
        try:
            res = rfloat.gamma(value)
        except ValueError:
            if value == 0.0:
                # produce an infinity with the right sign
                res = rfloat.copysign(rfloat.INFINITY, value)
            else:
                raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "gamma"')
        except OverflowError:
            res = rfloat.INFINITY
        return space.newfloat(res)

    @moduledef.function("hypot", value1="float", value2="float")
    @check_type_errors("w_numeric", "w_numeric")
    def method_hypot(self, space, value1, value2):
        return space.newfloat(math.hypot(value1, value2))

    @moduledef.function("ldexp", value1="float", value2="int")
    @check_type_errors("w_numeric", "w_integer")
    def method_ldexp(self, space, value1, value2):
        return space.newfloat(math.ldexp(value1, value2))

    @moduledef.function("log", value="float", base="float")
    @check_type_errors("w_numeric", "w_numeric")
    def method_log(self, space, value, base=math.e):
        try:
            res = 0.0
            if base == math.e:
                res = math.log(value)
            else:
                res = math.log(value) / math.log(base)
        except ValueError:
            if value == 0.0:
                res = float("-inf")
            else:
                raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "log"')

        return space.newfloat(res)

    @moduledef.function("log10", value="float")
    @check_type_errors("w_numeric")
    def method_log10(self, space, value):
        try:
            res = math.log10(value)
        except ValueError:
            if value == 0.0:
                res = float("-inf")
            else:
                raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "log10"')

        return space.newfloat(res)

    @moduledef.function("log2", value="float")
    @check_type_errors("w_numeric")
    def method_log2(self, space, value):
        try:
            res = math.log(value) / math.log(2)
        except ValueError:
            if value == 0.0:
                res = float("-inf")
            else:
                raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "log2"')

        return space.newfloat(res)

    @moduledef.function("sin", value="float")
    @check_type_errors("w_numeric")
    def method_sin(self, space, value):
        return space.newfloat(math.sin(value))

    @moduledef.function("sinh", value="float")
    @check_type_errors("w_numeric")
    def method_sinh(self, space, value):
        try:
            res = math.sinh(value)
        except OverflowError:
            res = rfloat.copysign(rfloat.INFINITY, value)
        return space.newfloat(res)

    @moduledef.function("sqrt", value="float")
    @check_type_errors("w_numeric")
    def method_sqrt(self, space, value):
        return space.newfloat(math.sqrt(value))

    @moduledef.function("tan", value="float")
    @check_type_errors("w_numeric")
    def method_tan(self, space, value):
        try:
            res = math.tan(value)
        except ValueError:
            res = NAN
        return space.newfloat(res)

    @moduledef.function("tanh", value="float")
    @check_type_errors("w_numeric")
    def method_tanh(self, space, value):
        return space.newfloat(math.tanh(value))


class W_DomainError(W_StandardError):
    classdef = ClassDef("Math::DomainError", W_StandardError.classdef, filepath=__file__)
    method_allocate = new_exception_allocate(classdef)
