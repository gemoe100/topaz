from topaz.objects.objectobject import W_Object
from topaz.coerce import Coerce
from topaz.error import RubyError
from topaz.module import ClassDef
from rpython.rlib.rbigint import rbigint
from rpython.rtyper.lltypesystem import rffi

class W_BufferObject(W_Object):
    classdef = ClassDef('Buffer', W_Object.classdef)

    typesymbols = {'char': rffi.CHAR,
                   'uchar': rffi.CHAR,
                   'short': rffi.SHORT,
                   'ushort': rffi.SHORT,
                   'int': rffi.INT,
                   'uint': rffi.INT,
                   'long': rffi.LONG,
                   'ulong': rffi.ULONG,
                   'long_long': rffi.LONGLONG,
                   'ulong_long': rffi.ULONGLONG,
                   'float': rffi.FLOAT,
                   'double': rffi.DOUBLE}

    @classdef.setup_class
    def setup_class(cls, space, w_cls):
        pass
        # TODO: Try this, once method_alias works in topaz
        #w_cls.method_alias(space, space.newsymbol('alloc_inout'),
        #                          space.newsymbol('new'))
        # Repeat with all other aliases!

    @classdef.singleton_method('allocate')
    def singleton_method_allocate(self, space, args_w):
        return W_BufferObject(space)

    @classdef.method('initialize')
    def method_initialize(self, space, w_arg1, w_arg2=None):
        try:
            typesym = Coerce.str(space, w_arg1)
            length = Coerce.int(space, w_arg2)
            self.init_str_int(space, typesym, length)
        except RubyError:
            length = Coerce.int(space, w_arg1)
            self.init_int(space, length)

    def init_str_int(self, space, typesym, length):
        size = rffi.sizeof(self.typesymbols[typesym])
        self.buffer = (length * size) * ['\x00']

    def init_int(self, space, length):
        self.buffer = length * ['\x00']

    @classdef.method('total')
    def method_total(self, space):
        return space.newint(len(self.buffer))

    # TODO: Once method_alias works in topaz, try the code in setup_class
    #       instead of this.
    @classdef.singleton_method('new_in')
    @classdef.singleton_method('new_out')
    @classdef.singleton_method('new_inout')
    @classdef.singleton_method('alloc_in')
    @classdef.singleton_method('alloc_out')
    @classdef.singleton_method('alloc_inout')
    def singleton_method_alloc_inout(self, space, args_w):
        return self.method_new(space, args_w, None)

    @classdef.method('put_char', offset='int', val='int')
    @classdef.method('put_uchar', offset='int', val='int')
    def method_put_uchar(self, space, offset, val):
        self.buffer[offset] = chr(val)
        return self

    @classdef.method('get_char', offset='int')
    @classdef.method('get_uchar', offset='int')
    def method_get_uchar(self, space, offset):
        return space.newint(ord(self.buffer[offset]))

    @classdef.method('put_ushort', offset='int', val='int')
    def method_put_ushort(self, space, offset, val):
        byte0 = val / 256
        byte1 = val % 256
        self.buffer[offset+0] = chr(byte0)
        self.buffer[offset+1] = chr(byte1)
        return self

    @classdef.method('get_ushort', offset='int')
    def method_get_ushort(self, space, offset):
        byte0 = ord(self.buffer[offset])
        byte1 = ord(self.buffer[offset+1])
        return space.newint(  byte0 * 256**0
                            + byte1 * 256**1)

    @classdef.method('put_uint', offset='int', val='int')
    def method_put_uint(self, space, offset, val):
        byte = [val / 256**i % 256 for i in range(4)]
        for i in range(4):
            self.buffer[offset+i] = chr(byte[i])
        return self

    @classdef.method('get_uint', offset='int')
    def method_get_uint(self, space, offset):
        byte = [ord(x) for x in self.buffer[offset:offset+4]]
        return space.newint( sum([byte[i] * 256**i for i in range(4)]) )

    @classdef.method('put_ulong_long', offset='int', val='bigint')
    def method_put_ulong_long(self, space, offset, val):
        rbi_256 = rbigint.fromint(256)
        rbi_range8 = [rbigint.fromint(i) for i in range(8)]
        byte = [val.div(rbi_256.pow(rbi)).mod(rbi_256)
                for rbi in rbi_range8]
        for i in range(8):
            self.buffer[offset+i] = chr(byte[i].toint())
        return self

    @classdef.method('get_ulong_long', offset='int')
    def method_get_ulong_long(self, space, offset):
        byte = [ord(x) for x in self.buffer[offset:offset+8]]
        val = sum([byte[i] * 256**i for i in range(8)])
        return space.newbigint_fromrbigint(rbigint.fromlong(val))