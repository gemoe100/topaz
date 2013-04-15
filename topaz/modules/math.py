from __future__ import absolute_import

import math

from rpython.rlib import rfloat

from topaz.module import Module, ModuleDef, ClassDef
from topaz.objects.exceptionobject import W_StandardError, \
                                          new_exception_allocate
from topaz.coerce import Coerce
from rpython.rlib.rfloat import NAN

def check_type_errors(*exp_ruby_types):
    exp_wrapper_types = ['w_' + i.lower() for i in exp_ruby_types]
    def decorator(func):
        def cte_func(self, space, args_w):
            args = []
            for exp_wrapper_type, w_arg in zip(exp_wrapper_types, args_w):
                exp_type = getattr(space, exp_wrapper_type)
                if space.is_kind_of(w_arg, exp_type):
                    if exp_type is space.w_integer:
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

def converter(func):
    def wrapper(self, space, args_w):
        f_args = []
        for w_arg in args_w:
            if space.is_kind_of(w_arg, space.w_numeric):
                f_arg = Coerce.float(space, w_arg)
                f_args.append(f_arg)
            else:
                raise_type_error(space, w_arg)
        return func(self, space, *f_args)
    wrapper.func_name = func.func_name
    return wrapper

def ldexp_converter(func):
    def wrapper(self, space, args_w):
        if len(args_w) == 2:
            w_value1, w_value2 = args_w
        else:
            # delegate and hope that the gateway will raise an
            # ArgumentError
            args = [Coerce.float(space, w_arg) for w_arg in args_w]
            return func(self, space, args)
        if space.is_kind_of(w_value1, space.w_numeric):
            if space.is_kind_of(w_value2, space.w_numeric):
                value1 = Coerce.float(space, w_value1)
                value2 = Coerce.int(space, w_value2)
                return func(self, space, value1, value2)
            else:
                raise_type_error(space, w_value2)
        else:
            raise_type_error(space, w_value1)
    wrapper.func_name = func.func_name
    return wrapper

def raise_type_error(space, w_variable):
    clsname = space.getclass(w_variable).name
    errmsg = "can't convert %s into Float" % clsname
    raise space.error(space.w_TypeError, errmsg)

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
    @converter
    def method_acos(self, space, value):
        return space.newfloat(math.acos(value))

    @moduledef.function("acosh", value="float")
    @converter
    def method_acosh(self, space, value):
        try:
            res = math.acosh(value)
        except ValueError:
            raise space.error(space.getclassfor(W_DomainError), 'Numerical argument is out of domain - "acosh"')
        return space.newfloat(res)

    @moduledef.function("asin", value="float")
    @converter
    def method_asin(self, space, value):
        return space.newfloat(math.asin(value))

    @moduledef.function("asinh", value="float")
    @converter
    def method_asinh(self, space, value):
        return space.newfloat(math.asinh(value))

    @moduledef.function("atan", value="float")
    @converter
    def method_atan(self, space, value):
        return space.newfloat(math.atan(value))

    @moduledef.function("atan2", value1="float", value2="float")
    @converter
    def method_atan2(self, space, value1, value2):
        return space.newfloat(math.atan2(value1, value2))

    @moduledef.function("atanh", value="float")
    @converter
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
    @converter
    def method_cbrt(self, space, value):
        if value < 0:
            return space.newfloat(-math.pow(-value, 1.0 / 3.0))
        else:
            return space.newfloat(math.pow(value, 1.0 / 3.0))

    @moduledef.function("cos", value="float")
    @converter
    def method_cos(self, space, value):
        return space.newfloat(math.cos(value))

    @moduledef.function("cosh", value="float")
    @converter
    def method_cosh(self, space, value):
        try:
            res = math.cosh(value)
        except OverflowError:
            res = rfloat.copysign(rfloat.INFINITY, value)
        return space.newfloat(res)

    @moduledef.function("exp", value="float")
    @converter
    def method_exp(self, space, value):
        return space.newfloat(math.exp(value))

    @moduledef.function("frexp", value="float")
    @converter
    def method_frexp(self, space, value):
        mant, exp = math.frexp(value)
        w_mant = space.newfloat(mant)
        w_exp = space.newint(exp)
        return space.newarray([w_mant, w_exp])

    @moduledef.function("gamma", value="float")
    @converter
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
    @converter
    def method_hypot(self, space, value1, value2):
        return space.newfloat(math.hypot(value1, value2))

    @moduledef.function("ldexp", value1="float", value2="int")
    @ldexp_converter
    def method_ldexp(self, space, value1, value2):
        return space.newfloat(math.ldexp(value1, value2))

    @moduledef.function("log", value="float", base="float")
    @converter
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
    @converter
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
    @converter
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
    @converter
    def method_sin(self, space, value):
        return space.newfloat(math.sin(value))

    @moduledef.function("sinh", value="float")
    @converter
    def method_sinh(self, space, value):
        try:
            res = math.sinh(value)
        except OverflowError:
            res = rfloat.copysign(rfloat.INFINITY, value)
        return space.newfloat(res)

    @moduledef.function("sqrt", value="float")
    @converter
    def method_sqrt(self, space, value):
        return space.newfloat(math.sqrt(value))

    @moduledef.function("tan", value="float")
    @converter
    def method_tan(self, space, value):
        try:
            res = math.tan(value)
        except ValueError:
            res = NAN
        return space.newfloat(res)

    @moduledef.function("tanh", value="float")
    @converter
    def method_tanh(self, space, value):
        return space.newfloat(math.tanh(value))


class W_DomainError(W_StandardError):
    classdef = ClassDef("Math::DomainError", W_StandardError.classdef, filepath=__file__)
    method_allocate = new_exception_allocate(classdef)
