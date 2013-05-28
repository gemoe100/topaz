from tests.base import BaseTopazTest
from topaz.modules.ffi.type import W_TypeObject
from topaz.objects.classobject import W_ClassObject
from topaz.objects.moduleobject import W_ModuleObject
from rpython.rlib import clibffi

class TestType(BaseTopazTest):

    primitive_types =  ['INT8', 'UINT8', 'INT16', 'UINT16',
                        'INT32', 'UINT32', 'INT64', 'UINT64',
                        'LONG', 'ULONG', 'FLOAT32', 'FLOAT64',
                        'VOID', 'LONGDOUBLE', 'POINTER', 'BOOL',
                        'VARARGS']
    alias_types = {'SCHAR': 'INT8',
                   'CHAR' : 'INT8',
                   'UCHAR' : 'UINT8',
                   'SHORT' : 'INT16',
                   'SSHORT' : 'INT16',
                   'USHORT' : 'UINT16',
                   'INT' : 'INT32',
                   'SINT' : 'INT32',
                   'UINT' : 'UINT32',
                   'LONG_LONG' : 'INT64',
                   'SLONG' : 'LONG',
                   'SLONG_LONG' : 'INT64',
                   'ULONG_LONG' : 'UINT64',
                   'FLOAT' : 'FLOAT32',
                   'DOUBLE' : 'FLOAT64',
                   'STRING' : 'POINTER',
                   'BUFFER_IN' : 'POINTER',
                   'BUFFER_OUT' : 'POINTER',
                   'BUFFER_INOUT' : 'POINTER'}

    def test_NativeType(self, space):
        w_native_type = space.execute('FFI::NativeType')
        assert isinstance(w_native_type, W_ModuleObject)
        for pt in TestType.primitive_types:
            space.execute('FFI::NativeType::%s' %pt)

    def test_Type_ll(self, space):
        w_type = W_TypeObject(space, 'TESTVOID', clibffi.ffi_type_void)
        assert w_type.native_type == 'TESTVOID'
        assert w_type.ffi_type is clibffi.ffi_type_void

    def test_Type(self, space):
        w_type = space.execute('FFI::Type')
        assert isinstance(w_type, W_ClassObject)

    def test_Builtin(self, space):
        w_builtin = space.execute('FFI::Type::Builtin')
        assert isinstance(w_builtin, W_ClassObject)
        w_type = space.execute('FFI::Type')
        assert w_builtin.superclass is w_type

    def test_Builtin_instances(self, space):
        for pt in TestType.primitive_types:
            w_ac = space.execute('FFI::Type::%s' %pt)
            w_ex = space.execute('FFI::NativeType::%s' % pt)
            assert self.unwrap(space, w_ac) == self.unwrap(space, w_ex)
        for at in TestType.alias_types:
            w_ac = space.execute('FFI::Type::%s' %at)
            w_ex = space.execute('FFI::Type::%s' %TestType.alias_types[at])
            assert self.unwrap(space, w_ac) == self.unwrap(space, w_ex)
        w_mapped = space.execute('FFI::Type::Mapped')
        assert isinstance(w_mapped, W_ClassObject)
        w_res = space.execute('FFI::Type::Mapped.respond_to? :method_missing')
        assert self.unwrap(space, w_res)
        w_res = space.execute('FFI::Type::Mapped.new(42)')