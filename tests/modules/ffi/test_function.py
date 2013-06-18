from tests.base import BaseTopazTest
from topaz.objects.classobject import W_ClassObject
from topaz.modules.ffi.function import W_FunctionObject
from rpython.rlib import clibffi

libm = clibffi.CDLL('libm.so')

class TestFunction(BaseTopazTest):

    def test_type_unwrap(self, space):
        w_type_object = space.execute("FFI::Type::VOID")
        w_type_symbol = space.execute(":void")
        w_some_int = space.execute("1")
        w_unknown_type = space.execute(":int42")
        assert (W_FunctionObject.type_unwrap(space, w_type_object)
                is w_type_object.ffi_type)
        assert (W_FunctionObject.type_unwrap(space, w_type_symbol)
                is w_type_object.ffi_type)
        with self.raises(space, "TypeError", "can't convert Fixnum into Type"):
            W_FunctionObject.type_unwrap(space, w_some_int)
        with self.raises(space, "TypeError", "can't convert Symbol into Type"):
            W_FunctionObject.type_unwrap(space, w_unknown_type)

    def test_initialize_typing(self, space):
        fname = "FFI::DynamicLibrary::Symbol.new(:fname)"
        w_function = space.execute("""
        FFI::Function.new(:void, [:int8, :int16], %s, {})
        """ % fname) #didn't crash
        w_function = space.execute("""
        FFI::Function.new(FFI::Type::VOID,
                          [FFI::Type::INT8, FFI::Type::INT16], %s, {})
        """ % fname) # didn't crash
        with self.raises(space, "TypeError", "can't convert Fixnum into Type"):
            space.execute("FFI::Function.new(1, [], %s, {})" % fname)
        with self.raises(space, "TypeError", "can't convert Fixnum into Type"):
            space.execute("FFI::Function.new(:void, [2], %s, {})" % fname)
        with self.raises(space, "TypeError", "can't convert Symbol into Type"):
            space.execute("FFI::Function.new(:null, [], %s, {})" % fname)
        with self.raises(space, "TypeError", "can't convert Symbol into Type"):
            space.execute("FFI::Function.new(:int32, [:array], %s, {})"
                          % fname)
        with self.raises(space, "TypeError",
                         "can't convert Fixnum into Symbol"):
            space.execute("FFI::Function.new(:void, [:uint8], 500, {})")

    def test_initialize_setvars(self, space):
        w_function = space.execute("""
        foo = FFI::DynamicLibrary::Symbol.new(:foo)
        FFI::Function.new(:int8, [:int16, :float64], foo, {})
        """)
        assert w_function.arg_types == [clibffi.ffi_type_sint16,
                                        clibffi.ffi_type_double]
        assert w_function.ret_type == clibffi.ffi_type_sint8
        assert w_function.name == 'foo'

    def test_attach(self, space):
        w_res = space.execute("""
        class LibraryMock
            def initialize
                local = FFI::DynamicLibrary::RTLD_LOCAL
                @ffi_libs = [FFI::DynamicLibrary.open('libm.so', local)]
            end
        end
        lib = LibraryMock.new
        pow = FFI::DynamicLibrary::Symbol.new(:pow)
        func = FFI::Function.new(:float64, [:float64, :float64], pow, {})
        func.attach(lib, 'power')
        arr1 = (0..5).each.map { |x| lib.power(x, 2) }
        """)
        for i, w_x in enumerate(w_res.listview(space)):
            assert self.unwrap(space, w_x) == i*i

# Just test whether both calculate the same results over 5 x 5 set
def results_equal(f1, f2):
    for i in range(5):
        for j in range(5):
            f1.push_arg(i)
            f1.push_arg(j)
            f2.push_arg(i)
            f2.push_arg(j)
            res1 = f1.call(clibffi.rffi.DOUBLE)
            res2 = f2.call(clibffi.rffi.DOUBLE)
            if res1 != res2:
                return False
    return True