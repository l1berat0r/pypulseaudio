# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-I/usr/lib/gcc/x86_64-linux-gnu/9/include/', '-I', '/usr/include/glib-2.0/', '-I', '/usr/lib/x86_64-linux-gnu/glib-2.0/include', '-I/usr/include/pulse']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes


_libraries = {}
_libraries['libpulse.so.0'] = ctypes.CDLL('libpulse.so.0')
def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))



class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass



class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16

_libraries['libpulse-mainloop-glib.so'] = ctypes.CDLL('libpulse-mainloop-glib.so')
_libraries['libpulse-simple.so.0'] = ctypes.CDLL('libpulse-simple.so.0')


pa_get_library_version = _libraries['libpulse.so.0'].pa_get_library_version
pa_get_library_version.restype = ctypes.POINTER(ctypes.c_char)
pa_get_library_version.argtypes = []

# values for enumeration 'pa_sample_format'
pa_sample_format__enumvalues = {
    0: 'PA_SAMPLE_U8',
    1: 'PA_SAMPLE_ALAW',
    2: 'PA_SAMPLE_ULAW',
    3: 'PA_SAMPLE_S16LE',
    4: 'PA_SAMPLE_S16BE',
    5: 'PA_SAMPLE_FLOAT32LE',
    6: 'PA_SAMPLE_FLOAT32BE',
    7: 'PA_SAMPLE_S32LE',
    8: 'PA_SAMPLE_S32BE',
    9: 'PA_SAMPLE_S24LE',
    10: 'PA_SAMPLE_S24BE',
    11: 'PA_SAMPLE_S24_32LE',
    12: 'PA_SAMPLE_S24_32BE',
    13: 'PA_SAMPLE_MAX',
    -1: 'PA_SAMPLE_INVALID',
}
PA_SAMPLE_U8 = 0
PA_SAMPLE_ALAW = 1
PA_SAMPLE_ULAW = 2
PA_SAMPLE_S16LE = 3
PA_SAMPLE_S16BE = 4
PA_SAMPLE_FLOAT32LE = 5
PA_SAMPLE_FLOAT32BE = 6
PA_SAMPLE_S32LE = 7
PA_SAMPLE_S32BE = 8
PA_SAMPLE_S24LE = 9
PA_SAMPLE_S24BE = 10
PA_SAMPLE_S24_32LE = 11
PA_SAMPLE_S24_32BE = 12
PA_SAMPLE_MAX = 13
PA_SAMPLE_INVALID = -1
pa_sample_format = ctypes.c_int32 # enum
pa_sample_format_t = pa_sample_format
pa_sample_format_t__enumvalues = pa_sample_format__enumvalues
class struct_pa_sample_spec(Structure):
    pass

struct_pa_sample_spec._pack_ = 1 # source:False
struct_pa_sample_spec._fields_ = [
    ('format', pa_sample_format_t),
    ('rate', ctypes.c_uint32),
    ('channels', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

pa_sample_spec = struct_pa_sample_spec
pa_usec_t = ctypes.c_uint64
size_t = ctypes.c_uint64
pa_bytes_per_second = _libraries['libpulse.so.0'].pa_bytes_per_second
pa_bytes_per_second.restype = size_t
pa_bytes_per_second.argtypes = [ctypes.POINTER(struct_pa_sample_spec)]
pa_frame_size = _libraries['libpulse.so.0'].pa_frame_size
pa_frame_size.restype = size_t
pa_frame_size.argtypes = [ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_size = _libraries['libpulse.so.0'].pa_sample_size
pa_sample_size.restype = size_t
pa_sample_size.argtypes = [ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_size_of_format = _libraries['libpulse.so.0'].pa_sample_size_of_format
pa_sample_size_of_format.restype = size_t
pa_sample_size_of_format.argtypes = [pa_sample_format_t]
uint64_t = ctypes.c_uint64
pa_bytes_to_usec = _libraries['libpulse.so.0'].pa_bytes_to_usec
pa_bytes_to_usec.restype = pa_usec_t
pa_bytes_to_usec.argtypes = [uint64_t, ctypes.POINTER(struct_pa_sample_spec)]
pa_usec_to_bytes = _libraries['libpulse.so.0'].pa_usec_to_bytes
pa_usec_to_bytes.restype = size_t
pa_usec_to_bytes.argtypes = [pa_usec_t, ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_spec_init = _libraries['libpulse.so.0'].pa_sample_spec_init
pa_sample_spec_init.restype = ctypes.POINTER(struct_pa_sample_spec)
pa_sample_spec_init.argtypes = [ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_format_valid = _libraries['libpulse.so.0'].pa_sample_format_valid
pa_sample_format_valid.restype = ctypes.c_int32
pa_sample_format_valid.argtypes = [ctypes.c_uint32]
uint32_t = ctypes.c_uint32
pa_sample_rate_valid = _libraries['libpulse.so.0'].pa_sample_rate_valid
pa_sample_rate_valid.restype = ctypes.c_int32
pa_sample_rate_valid.argtypes = [uint32_t]
uint8_t = ctypes.c_uint8
pa_channels_valid = _libraries['libpulse.so.0'].pa_channels_valid
pa_channels_valid.restype = ctypes.c_int32
pa_channels_valid.argtypes = [uint8_t]
pa_sample_spec_valid = _libraries['libpulse.so.0'].pa_sample_spec_valid
pa_sample_spec_valid.restype = ctypes.c_int32
pa_sample_spec_valid.argtypes = [ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_spec_equal = _libraries['libpulse.so.0'].pa_sample_spec_equal
pa_sample_spec_equal.restype = ctypes.c_int32
pa_sample_spec_equal.argtypes = [ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_sample_spec)]
pa_sample_format_to_string = _libraries['libpulse.so.0'].pa_sample_format_to_string
pa_sample_format_to_string.restype = ctypes.POINTER(ctypes.c_char)
pa_sample_format_to_string.argtypes = [pa_sample_format_t]
pa_parse_sample_format = _libraries['libpulse.so.0'].pa_parse_sample_format
pa_parse_sample_format.restype = pa_sample_format_t
pa_parse_sample_format.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_sample_spec_snprint = _libraries['libpulse.so.0'].pa_sample_spec_snprint
pa_sample_spec_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_sample_spec_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_sample_spec)]
pa_bytes_snprint = _libraries['libpulse.so.0'].pa_bytes_snprint
pa_bytes_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_bytes_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.c_uint32]
pa_sample_format_is_le = _libraries['libpulse.so.0'].pa_sample_format_is_le
pa_sample_format_is_le.restype = ctypes.c_int32
pa_sample_format_is_le.argtypes = [pa_sample_format_t]
pa_sample_format_is_be = _libraries['libpulse.so.0'].pa_sample_format_is_be
pa_sample_format_is_be.restype = ctypes.c_int32
pa_sample_format_is_be.argtypes = [pa_sample_format_t]

# values for enumeration 'pa_channel_position'
pa_channel_position__enumvalues = {
    -1: 'PA_CHANNEL_POSITION_INVALID',
    0: 'PA_CHANNEL_POSITION_MONO',
    1: 'PA_CHANNEL_POSITION_FRONT_LEFT',
    2: 'PA_CHANNEL_POSITION_FRONT_RIGHT',
    3: 'PA_CHANNEL_POSITION_FRONT_CENTER',
    1: 'PA_CHANNEL_POSITION_LEFT',
    2: 'PA_CHANNEL_POSITION_RIGHT',
    3: 'PA_CHANNEL_POSITION_CENTER',
    4: 'PA_CHANNEL_POSITION_REAR_CENTER',
    5: 'PA_CHANNEL_POSITION_REAR_LEFT',
    6: 'PA_CHANNEL_POSITION_REAR_RIGHT',
    7: 'PA_CHANNEL_POSITION_LFE',
    7: 'PA_CHANNEL_POSITION_SUBWOOFER',
    8: 'PA_CHANNEL_POSITION_FRONT_LEFT_OF_CENTER',
    9: 'PA_CHANNEL_POSITION_FRONT_RIGHT_OF_CENTER',
    10: 'PA_CHANNEL_POSITION_SIDE_LEFT',
    11: 'PA_CHANNEL_POSITION_SIDE_RIGHT',
    12: 'PA_CHANNEL_POSITION_AUX0',
    13: 'PA_CHANNEL_POSITION_AUX1',
    14: 'PA_CHANNEL_POSITION_AUX2',
    15: 'PA_CHANNEL_POSITION_AUX3',
    16: 'PA_CHANNEL_POSITION_AUX4',
    17: 'PA_CHANNEL_POSITION_AUX5',
    18: 'PA_CHANNEL_POSITION_AUX6',
    19: 'PA_CHANNEL_POSITION_AUX7',
    20: 'PA_CHANNEL_POSITION_AUX8',
    21: 'PA_CHANNEL_POSITION_AUX9',
    22: 'PA_CHANNEL_POSITION_AUX10',
    23: 'PA_CHANNEL_POSITION_AUX11',
    24: 'PA_CHANNEL_POSITION_AUX12',
    25: 'PA_CHANNEL_POSITION_AUX13',
    26: 'PA_CHANNEL_POSITION_AUX14',
    27: 'PA_CHANNEL_POSITION_AUX15',
    28: 'PA_CHANNEL_POSITION_AUX16',
    29: 'PA_CHANNEL_POSITION_AUX17',
    30: 'PA_CHANNEL_POSITION_AUX18',
    31: 'PA_CHANNEL_POSITION_AUX19',
    32: 'PA_CHANNEL_POSITION_AUX20',
    33: 'PA_CHANNEL_POSITION_AUX21',
    34: 'PA_CHANNEL_POSITION_AUX22',
    35: 'PA_CHANNEL_POSITION_AUX23',
    36: 'PA_CHANNEL_POSITION_AUX24',
    37: 'PA_CHANNEL_POSITION_AUX25',
    38: 'PA_CHANNEL_POSITION_AUX26',
    39: 'PA_CHANNEL_POSITION_AUX27',
    40: 'PA_CHANNEL_POSITION_AUX28',
    41: 'PA_CHANNEL_POSITION_AUX29',
    42: 'PA_CHANNEL_POSITION_AUX30',
    43: 'PA_CHANNEL_POSITION_AUX31',
    44: 'PA_CHANNEL_POSITION_TOP_CENTER',
    45: 'PA_CHANNEL_POSITION_TOP_FRONT_LEFT',
    46: 'PA_CHANNEL_POSITION_TOP_FRONT_RIGHT',
    47: 'PA_CHANNEL_POSITION_TOP_FRONT_CENTER',
    48: 'PA_CHANNEL_POSITION_TOP_REAR_LEFT',
    49: 'PA_CHANNEL_POSITION_TOP_REAR_RIGHT',
    50: 'PA_CHANNEL_POSITION_TOP_REAR_CENTER',
    51: 'PA_CHANNEL_POSITION_MAX',
}
PA_CHANNEL_POSITION_INVALID = -1
PA_CHANNEL_POSITION_MONO = 0
PA_CHANNEL_POSITION_FRONT_LEFT = 1
PA_CHANNEL_POSITION_FRONT_RIGHT = 2
PA_CHANNEL_POSITION_FRONT_CENTER = 3
PA_CHANNEL_POSITION_LEFT = 1
PA_CHANNEL_POSITION_RIGHT = 2
PA_CHANNEL_POSITION_CENTER = 3
PA_CHANNEL_POSITION_REAR_CENTER = 4
PA_CHANNEL_POSITION_REAR_LEFT = 5
PA_CHANNEL_POSITION_REAR_RIGHT = 6
PA_CHANNEL_POSITION_LFE = 7
PA_CHANNEL_POSITION_SUBWOOFER = 7
PA_CHANNEL_POSITION_FRONT_LEFT_OF_CENTER = 8
PA_CHANNEL_POSITION_FRONT_RIGHT_OF_CENTER = 9
PA_CHANNEL_POSITION_SIDE_LEFT = 10
PA_CHANNEL_POSITION_SIDE_RIGHT = 11
PA_CHANNEL_POSITION_AUX0 = 12
PA_CHANNEL_POSITION_AUX1 = 13
PA_CHANNEL_POSITION_AUX2 = 14
PA_CHANNEL_POSITION_AUX3 = 15
PA_CHANNEL_POSITION_AUX4 = 16
PA_CHANNEL_POSITION_AUX5 = 17
PA_CHANNEL_POSITION_AUX6 = 18
PA_CHANNEL_POSITION_AUX7 = 19
PA_CHANNEL_POSITION_AUX8 = 20
PA_CHANNEL_POSITION_AUX9 = 21
PA_CHANNEL_POSITION_AUX10 = 22
PA_CHANNEL_POSITION_AUX11 = 23
PA_CHANNEL_POSITION_AUX12 = 24
PA_CHANNEL_POSITION_AUX13 = 25
PA_CHANNEL_POSITION_AUX14 = 26
PA_CHANNEL_POSITION_AUX15 = 27
PA_CHANNEL_POSITION_AUX16 = 28
PA_CHANNEL_POSITION_AUX17 = 29
PA_CHANNEL_POSITION_AUX18 = 30
PA_CHANNEL_POSITION_AUX19 = 31
PA_CHANNEL_POSITION_AUX20 = 32
PA_CHANNEL_POSITION_AUX21 = 33
PA_CHANNEL_POSITION_AUX22 = 34
PA_CHANNEL_POSITION_AUX23 = 35
PA_CHANNEL_POSITION_AUX24 = 36
PA_CHANNEL_POSITION_AUX25 = 37
PA_CHANNEL_POSITION_AUX26 = 38
PA_CHANNEL_POSITION_AUX27 = 39
PA_CHANNEL_POSITION_AUX28 = 40
PA_CHANNEL_POSITION_AUX29 = 41
PA_CHANNEL_POSITION_AUX30 = 42
PA_CHANNEL_POSITION_AUX31 = 43
PA_CHANNEL_POSITION_TOP_CENTER = 44
PA_CHANNEL_POSITION_TOP_FRONT_LEFT = 45
PA_CHANNEL_POSITION_TOP_FRONT_RIGHT = 46
PA_CHANNEL_POSITION_TOP_FRONT_CENTER = 47
PA_CHANNEL_POSITION_TOP_REAR_LEFT = 48
PA_CHANNEL_POSITION_TOP_REAR_RIGHT = 49
PA_CHANNEL_POSITION_TOP_REAR_CENTER = 50
PA_CHANNEL_POSITION_MAX = 51
pa_channel_position = ctypes.c_int32 # enum
pa_channel_position_t = pa_channel_position
pa_channel_position_t__enumvalues = pa_channel_position__enumvalues
pa_channel_position_mask_t = ctypes.c_uint64

# values for enumeration 'pa_channel_map_def'
pa_channel_map_def__enumvalues = {
    0: 'PA_CHANNEL_MAP_AIFF',
    1: 'PA_CHANNEL_MAP_ALSA',
    2: 'PA_CHANNEL_MAP_AUX',
    3: 'PA_CHANNEL_MAP_WAVEEX',
    4: 'PA_CHANNEL_MAP_OSS',
    5: 'PA_CHANNEL_MAP_DEF_MAX',
    0: 'PA_CHANNEL_MAP_DEFAULT',
}
PA_CHANNEL_MAP_AIFF = 0
PA_CHANNEL_MAP_ALSA = 1
PA_CHANNEL_MAP_AUX = 2
PA_CHANNEL_MAP_WAVEEX = 3
PA_CHANNEL_MAP_OSS = 4
PA_CHANNEL_MAP_DEF_MAX = 5
PA_CHANNEL_MAP_DEFAULT = 0
pa_channel_map_def = ctypes.c_uint32 # enum
pa_channel_map_def_t = pa_channel_map_def
pa_channel_map_def_t__enumvalues = pa_channel_map_def__enumvalues
class struct_pa_channel_map(Structure):
    pass

struct_pa_channel_map._pack_ = 1 # source:False
struct_pa_channel_map._fields_ = [
    ('channels', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('map', pa_channel_position * 32),
]

pa_channel_map = struct_pa_channel_map
pa_channel_map_init = _libraries['libpulse.so.0'].pa_channel_map_init
pa_channel_map_init.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_init.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_init_mono = _libraries['libpulse.so.0'].pa_channel_map_init_mono
pa_channel_map_init_mono.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_init_mono.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_init_stereo = _libraries['libpulse.so.0'].pa_channel_map_init_stereo
pa_channel_map_init_stereo.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_init_stereo.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_init_auto = _libraries['libpulse.so.0'].pa_channel_map_init_auto
pa_channel_map_init_auto.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_init_auto.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.c_uint32, pa_channel_map_def_t]
pa_channel_map_init_extend = _libraries['libpulse.so.0'].pa_channel_map_init_extend
pa_channel_map_init_extend.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_init_extend.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.c_uint32, pa_channel_map_def_t]
pa_channel_position_to_string = _libraries['libpulse.so.0'].pa_channel_position_to_string
pa_channel_position_to_string.restype = ctypes.POINTER(ctypes.c_char)
pa_channel_position_to_string.argtypes = [pa_channel_position_t]
pa_channel_position_from_string = _libraries['libpulse.so.0'].pa_channel_position_from_string
pa_channel_position_from_string.restype = pa_channel_position_t
pa_channel_position_from_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_channel_position_to_pretty_string = _libraries['libpulse.so.0'].pa_channel_position_to_pretty_string
pa_channel_position_to_pretty_string.restype = ctypes.POINTER(ctypes.c_char)
pa_channel_position_to_pretty_string.argtypes = [pa_channel_position_t]
pa_channel_map_snprint = _libraries['libpulse.so.0'].pa_channel_map_snprint
pa_channel_map_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_channel_map_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_parse = _libraries['libpulse.so.0'].pa_channel_map_parse
pa_channel_map_parse.restype = ctypes.POINTER(struct_pa_channel_map)
pa_channel_map_parse.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(ctypes.c_char)]
pa_channel_map_equal = _libraries['libpulse.so.0'].pa_channel_map_equal
pa_channel_map_equal.restype = ctypes.c_int32
pa_channel_map_equal.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_valid = _libraries['libpulse.so.0'].pa_channel_map_valid
pa_channel_map_valid.restype = ctypes.c_int32
pa_channel_map_valid.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_compatible = _libraries['libpulse.so.0'].pa_channel_map_compatible
pa_channel_map_compatible.restype = ctypes.c_int32
pa_channel_map_compatible.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_sample_spec)]
pa_channel_map_superset = _libraries['libpulse.so.0'].pa_channel_map_superset
pa_channel_map_superset.restype = ctypes.c_int32
pa_channel_map_superset.argtypes = [ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_can_balance = _libraries['libpulse.so.0'].pa_channel_map_can_balance
pa_channel_map_can_balance.restype = ctypes.c_int32
pa_channel_map_can_balance.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_can_fade = _libraries['libpulse.so.0'].pa_channel_map_can_fade
pa_channel_map_can_fade.restype = ctypes.c_int32
pa_channel_map_can_fade.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_can_lfe_balance = _libraries['libpulse.so.0'].pa_channel_map_can_lfe_balance
pa_channel_map_can_lfe_balance.restype = ctypes.c_int32
pa_channel_map_can_lfe_balance.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_to_name = _libraries['libpulse.so.0'].pa_channel_map_to_name
pa_channel_map_to_name.restype = ctypes.POINTER(ctypes.c_char)
pa_channel_map_to_name.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_to_pretty_name = _libraries['libpulse.so.0'].pa_channel_map_to_pretty_name
pa_channel_map_to_pretty_name.restype = ctypes.POINTER(ctypes.c_char)
pa_channel_map_to_pretty_name.argtypes = [ctypes.POINTER(struct_pa_channel_map)]
pa_channel_map_has_position = _libraries['libpulse.so.0'].pa_channel_map_has_position
pa_channel_map_has_position.restype = ctypes.c_int32
pa_channel_map_has_position.argtypes = [ctypes.POINTER(struct_pa_channel_map), pa_channel_position_t]
pa_channel_map_mask = _libraries['libpulse.so.0'].pa_channel_map_mask
pa_channel_map_mask.restype = pa_channel_position_mask_t
pa_channel_map_mask.argtypes = [ctypes.POINTER(struct_pa_channel_map)]

# values for enumeration 'pa_context_state'
pa_context_state__enumvalues = {
    0: 'PA_CONTEXT_UNCONNECTED',
    1: 'PA_CONTEXT_CONNECTING',
    2: 'PA_CONTEXT_AUTHORIZING',
    3: 'PA_CONTEXT_SETTING_NAME',
    4: 'PA_CONTEXT_READY',
    5: 'PA_CONTEXT_FAILED',
    6: 'PA_CONTEXT_TERMINATED',
}
PA_CONTEXT_UNCONNECTED = 0
PA_CONTEXT_CONNECTING = 1
PA_CONTEXT_AUTHORIZING = 2
PA_CONTEXT_SETTING_NAME = 3
PA_CONTEXT_READY = 4
PA_CONTEXT_FAILED = 5
PA_CONTEXT_TERMINATED = 6
pa_context_state = ctypes.c_uint32 # enum
pa_context_state_t = pa_context_state
pa_context_state_t__enumvalues = pa_context_state__enumvalues

# values for enumeration 'pa_stream_state'
pa_stream_state__enumvalues = {
    0: 'PA_STREAM_UNCONNECTED',
    1: 'PA_STREAM_CREATING',
    2: 'PA_STREAM_READY',
    3: 'PA_STREAM_FAILED',
    4: 'PA_STREAM_TERMINATED',
}
PA_STREAM_UNCONNECTED = 0
PA_STREAM_CREATING = 1
PA_STREAM_READY = 2
PA_STREAM_FAILED = 3
PA_STREAM_TERMINATED = 4
pa_stream_state = ctypes.c_uint32 # enum
pa_stream_state_t = pa_stream_state
pa_stream_state_t__enumvalues = pa_stream_state__enumvalues

# values for enumeration 'pa_operation_state'
pa_operation_state__enumvalues = {
    0: 'PA_OPERATION_RUNNING',
    1: 'PA_OPERATION_DONE',
    2: 'PA_OPERATION_CANCELLED',
}
PA_OPERATION_RUNNING = 0
PA_OPERATION_DONE = 1
PA_OPERATION_CANCELLED = 2
pa_operation_state = ctypes.c_uint32 # enum
pa_operation_state_t = pa_operation_state
pa_operation_state_t__enumvalues = pa_operation_state__enumvalues

# values for enumeration 'pa_context_flags'
pa_context_flags__enumvalues = {
    0: 'PA_CONTEXT_NOFLAGS',
    1: 'PA_CONTEXT_NOAUTOSPAWN',
    2: 'PA_CONTEXT_NOFAIL',
}
PA_CONTEXT_NOFLAGS = 0
PA_CONTEXT_NOAUTOSPAWN = 1
PA_CONTEXT_NOFAIL = 2
pa_context_flags = ctypes.c_uint32 # enum
pa_context_flags_t = pa_context_flags
pa_context_flags_t__enumvalues = pa_context_flags__enumvalues

# values for enumeration 'pa_direction'
pa_direction__enumvalues = {
    1: 'PA_DIRECTION_OUTPUT',
    2: 'PA_DIRECTION_INPUT',
}
PA_DIRECTION_OUTPUT = 1
PA_DIRECTION_INPUT = 2
pa_direction = ctypes.c_uint32 # enum
pa_direction_t = pa_direction
pa_direction_t__enumvalues = pa_direction__enumvalues

# values for enumeration 'pa_device_type'
pa_device_type__enumvalues = {
    0: 'PA_DEVICE_TYPE_SINK',
    1: 'PA_DEVICE_TYPE_SOURCE',
}
PA_DEVICE_TYPE_SINK = 0
PA_DEVICE_TYPE_SOURCE = 1
pa_device_type = ctypes.c_uint32 # enum
pa_device_type_t = pa_device_type
pa_device_type_t__enumvalues = pa_device_type__enumvalues

# values for enumeration 'pa_stream_direction'
pa_stream_direction__enumvalues = {
    0: 'PA_STREAM_NODIRECTION',
    1: 'PA_STREAM_PLAYBACK',
    2: 'PA_STREAM_RECORD',
    3: 'PA_STREAM_UPLOAD',
}
PA_STREAM_NODIRECTION = 0
PA_STREAM_PLAYBACK = 1
PA_STREAM_RECORD = 2
PA_STREAM_UPLOAD = 3
pa_stream_direction = ctypes.c_uint32 # enum
pa_stream_direction_t = pa_stream_direction
pa_stream_direction_t__enumvalues = pa_stream_direction__enumvalues

# values for enumeration 'pa_stream_flags'
pa_stream_flags__enumvalues = {
    0: 'PA_STREAM_NOFLAGS',
    1: 'PA_STREAM_START_CORKED',
    2: 'PA_STREAM_INTERPOLATE_TIMING',
    4: 'PA_STREAM_NOT_MONOTONIC',
    8: 'PA_STREAM_AUTO_TIMING_UPDATE',
    16: 'PA_STREAM_NO_REMAP_CHANNELS',
    32: 'PA_STREAM_NO_REMIX_CHANNELS',
    64: 'PA_STREAM_FIX_FORMAT',
    128: 'PA_STREAM_FIX_RATE',
    256: 'PA_STREAM_FIX_CHANNELS',
    512: 'PA_STREAM_DONT_MOVE',
    1024: 'PA_STREAM_VARIABLE_RATE',
    2048: 'PA_STREAM_PEAK_DETECT',
    4096: 'PA_STREAM_START_MUTED',
    8192: 'PA_STREAM_ADJUST_LATENCY',
    16384: 'PA_STREAM_EARLY_REQUESTS',
    32768: 'PA_STREAM_DONT_INHIBIT_AUTO_SUSPEND',
    65536: 'PA_STREAM_START_UNMUTED',
    131072: 'PA_STREAM_FAIL_ON_SUSPEND',
    262144: 'PA_STREAM_RELATIVE_VOLUME',
    524288: 'PA_STREAM_PASSTHROUGH',
}
PA_STREAM_NOFLAGS = 0
PA_STREAM_START_CORKED = 1
PA_STREAM_INTERPOLATE_TIMING = 2
PA_STREAM_NOT_MONOTONIC = 4
PA_STREAM_AUTO_TIMING_UPDATE = 8
PA_STREAM_NO_REMAP_CHANNELS = 16
PA_STREAM_NO_REMIX_CHANNELS = 32
PA_STREAM_FIX_FORMAT = 64
PA_STREAM_FIX_RATE = 128
PA_STREAM_FIX_CHANNELS = 256
PA_STREAM_DONT_MOVE = 512
PA_STREAM_VARIABLE_RATE = 1024
PA_STREAM_PEAK_DETECT = 2048
PA_STREAM_START_MUTED = 4096
PA_STREAM_ADJUST_LATENCY = 8192
PA_STREAM_EARLY_REQUESTS = 16384
PA_STREAM_DONT_INHIBIT_AUTO_SUSPEND = 32768
PA_STREAM_START_UNMUTED = 65536
PA_STREAM_FAIL_ON_SUSPEND = 131072
PA_STREAM_RELATIVE_VOLUME = 262144
PA_STREAM_PASSTHROUGH = 524288
pa_stream_flags = ctypes.c_uint32 # enum
pa_stream_flags_t = pa_stream_flags
pa_stream_flags_t__enumvalues = pa_stream_flags__enumvalues
class struct_pa_buffer_attr(Structure):
    pass

struct_pa_buffer_attr._pack_ = 1 # source:False
struct_pa_buffer_attr._fields_ = [
    ('maxlength', ctypes.c_uint32),
    ('tlength', ctypes.c_uint32),
    ('prebuf', ctypes.c_uint32),
    ('minreq', ctypes.c_uint32),
    ('fragsize', ctypes.c_uint32),
]

pa_buffer_attr = struct_pa_buffer_attr

# values for enumeration 'pa_error_code'
pa_error_code__enumvalues = {
    0: 'PA_OK',
    1: 'PA_ERR_ACCESS',
    2: 'PA_ERR_COMMAND',
    3: 'PA_ERR_INVALID',
    4: 'PA_ERR_EXIST',
    5: 'PA_ERR_NOENTITY',
    6: 'PA_ERR_CONNECTIONREFUSED',
    7: 'PA_ERR_PROTOCOL',
    8: 'PA_ERR_TIMEOUT',
    9: 'PA_ERR_AUTHKEY',
    10: 'PA_ERR_INTERNAL',
    11: 'PA_ERR_CONNECTIONTERMINATED',
    12: 'PA_ERR_KILLED',
    13: 'PA_ERR_INVALIDSERVER',
    14: 'PA_ERR_MODINITFAILED',
    15: 'PA_ERR_BADSTATE',
    16: 'PA_ERR_NODATA',
    17: 'PA_ERR_VERSION',
    18: 'PA_ERR_TOOLARGE',
    19: 'PA_ERR_NOTSUPPORTED',
    20: 'PA_ERR_UNKNOWN',
    21: 'PA_ERR_NOEXTENSION',
    22: 'PA_ERR_OBSOLETE',
    23: 'PA_ERR_NOTIMPLEMENTED',
    24: 'PA_ERR_FORKED',
    25: 'PA_ERR_IO',
    26: 'PA_ERR_BUSY',
    27: 'PA_ERR_MAX',
}
PA_OK = 0
PA_ERR_ACCESS = 1
PA_ERR_COMMAND = 2
PA_ERR_INVALID = 3
PA_ERR_EXIST = 4
PA_ERR_NOENTITY = 5
PA_ERR_CONNECTIONREFUSED = 6
PA_ERR_PROTOCOL = 7
PA_ERR_TIMEOUT = 8
PA_ERR_AUTHKEY = 9
PA_ERR_INTERNAL = 10
PA_ERR_CONNECTIONTERMINATED = 11
PA_ERR_KILLED = 12
PA_ERR_INVALIDSERVER = 13
PA_ERR_MODINITFAILED = 14
PA_ERR_BADSTATE = 15
PA_ERR_NODATA = 16
PA_ERR_VERSION = 17
PA_ERR_TOOLARGE = 18
PA_ERR_NOTSUPPORTED = 19
PA_ERR_UNKNOWN = 20
PA_ERR_NOEXTENSION = 21
PA_ERR_OBSOLETE = 22
PA_ERR_NOTIMPLEMENTED = 23
PA_ERR_FORKED = 24
PA_ERR_IO = 25
PA_ERR_BUSY = 26
PA_ERR_MAX = 27
pa_error_code = ctypes.c_uint32 # enum
pa_error_code_t = pa_error_code
pa_error_code_t__enumvalues = pa_error_code__enumvalues

# values for enumeration 'pa_subscription_mask'
pa_subscription_mask__enumvalues = {
    0: 'PA_SUBSCRIPTION_MASK_NULL',
    1: 'PA_SUBSCRIPTION_MASK_SINK',
    2: 'PA_SUBSCRIPTION_MASK_SOURCE',
    4: 'PA_SUBSCRIPTION_MASK_SINK_INPUT',
    8: 'PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT',
    16: 'PA_SUBSCRIPTION_MASK_MODULE',
    32: 'PA_SUBSCRIPTION_MASK_CLIENT',
    64: 'PA_SUBSCRIPTION_MASK_SAMPLE_CACHE',
    128: 'PA_SUBSCRIPTION_MASK_SERVER',
    256: 'PA_SUBSCRIPTION_MASK_AUTOLOAD',
    512: 'PA_SUBSCRIPTION_MASK_CARD',
    767: 'PA_SUBSCRIPTION_MASK_ALL',
}
PA_SUBSCRIPTION_MASK_NULL = 0
PA_SUBSCRIPTION_MASK_SINK = 1
PA_SUBSCRIPTION_MASK_SOURCE = 2
PA_SUBSCRIPTION_MASK_SINK_INPUT = 4
PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT = 8
PA_SUBSCRIPTION_MASK_MODULE = 16
PA_SUBSCRIPTION_MASK_CLIENT = 32
PA_SUBSCRIPTION_MASK_SAMPLE_CACHE = 64
PA_SUBSCRIPTION_MASK_SERVER = 128
PA_SUBSCRIPTION_MASK_AUTOLOAD = 256
PA_SUBSCRIPTION_MASK_CARD = 512
PA_SUBSCRIPTION_MASK_ALL = 767
pa_subscription_mask = ctypes.c_uint32 # enum
pa_subscription_mask_t = pa_subscription_mask
pa_subscription_mask_t__enumvalues = pa_subscription_mask__enumvalues

# values for enumeration 'pa_subscription_event_type'
pa_subscription_event_type__enumvalues = {
    0: 'PA_SUBSCRIPTION_EVENT_SINK',
    1: 'PA_SUBSCRIPTION_EVENT_SOURCE',
    2: 'PA_SUBSCRIPTION_EVENT_SINK_INPUT',
    3: 'PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT',
    4: 'PA_SUBSCRIPTION_EVENT_MODULE',
    5: 'PA_SUBSCRIPTION_EVENT_CLIENT',
    6: 'PA_SUBSCRIPTION_EVENT_SAMPLE_CACHE',
    7: 'PA_SUBSCRIPTION_EVENT_SERVER',
    8: 'PA_SUBSCRIPTION_EVENT_AUTOLOAD',
    9: 'PA_SUBSCRIPTION_EVENT_CARD',
    15: 'PA_SUBSCRIPTION_EVENT_FACILITY_MASK',
    0: 'PA_SUBSCRIPTION_EVENT_NEW',
    16: 'PA_SUBSCRIPTION_EVENT_CHANGE',
    32: 'PA_SUBSCRIPTION_EVENT_REMOVE',
    48: 'PA_SUBSCRIPTION_EVENT_TYPE_MASK',
}
PA_SUBSCRIPTION_EVENT_SINK = 0
PA_SUBSCRIPTION_EVENT_SOURCE = 1
PA_SUBSCRIPTION_EVENT_SINK_INPUT = 2
PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT = 3
PA_SUBSCRIPTION_EVENT_MODULE = 4
PA_SUBSCRIPTION_EVENT_CLIENT = 5
PA_SUBSCRIPTION_EVENT_SAMPLE_CACHE = 6
PA_SUBSCRIPTION_EVENT_SERVER = 7
PA_SUBSCRIPTION_EVENT_AUTOLOAD = 8
PA_SUBSCRIPTION_EVENT_CARD = 9
PA_SUBSCRIPTION_EVENT_FACILITY_MASK = 15
PA_SUBSCRIPTION_EVENT_NEW = 0
PA_SUBSCRIPTION_EVENT_CHANGE = 16
PA_SUBSCRIPTION_EVENT_REMOVE = 32
PA_SUBSCRIPTION_EVENT_TYPE_MASK = 48
pa_subscription_event_type = ctypes.c_uint32 # enum
pa_subscription_event_type_t = pa_subscription_event_type
pa_subscription_event_type_t__enumvalues = pa_subscription_event_type__enumvalues
class struct_pa_timing_info(Structure):
    pass

class struct_timeval(Structure):
    pass

struct_timeval._pack_ = 1 # source:False
struct_timeval._fields_ = [
    ('tv_sec', ctypes.c_int64),
    ('tv_usec', ctypes.c_int64),
]

struct_pa_timing_info._pack_ = 1 # source:False
struct_pa_timing_info._fields_ = [
    ('timestamp', struct_timeval),
    ('synchronized_clocks', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('sink_usec', ctypes.c_uint64),
    ('source_usec', ctypes.c_uint64),
    ('transport_usec', ctypes.c_uint64),
    ('playing', ctypes.c_int32),
    ('write_index_corrupt', ctypes.c_int32),
    ('write_index', ctypes.c_int64),
    ('read_index_corrupt', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('read_index', ctypes.c_int64),
    ('configured_sink_usec', ctypes.c_uint64),
    ('configured_source_usec', ctypes.c_uint64),
    ('since_underrun', ctypes.c_int64),
]

pa_timing_info = struct_pa_timing_info
class struct_pa_spawn_api(Structure):
    pass

struct_pa_spawn_api._pack_ = 1 # source:False
struct_pa_spawn_api._fields_ = [
    ('prefork', ctypes.CFUNCTYPE(None)),
    ('postfork', ctypes.CFUNCTYPE(None)),
    ('atfork', ctypes.CFUNCTYPE(None)),
]

pa_spawn_api = struct_pa_spawn_api

# values for enumeration 'pa_seek_mode'
pa_seek_mode__enumvalues = {
    0: 'PA_SEEK_RELATIVE',
    1: 'PA_SEEK_ABSOLUTE',
    2: 'PA_SEEK_RELATIVE_ON_READ',
    3: 'PA_SEEK_RELATIVE_END',
}
PA_SEEK_RELATIVE = 0
PA_SEEK_ABSOLUTE = 1
PA_SEEK_RELATIVE_ON_READ = 2
PA_SEEK_RELATIVE_END = 3
pa_seek_mode = ctypes.c_uint32 # enum
pa_seek_mode_t = pa_seek_mode
pa_seek_mode_t__enumvalues = pa_seek_mode__enumvalues

# values for enumeration 'pa_sink_flags'
pa_sink_flags__enumvalues = {
    0: 'PA_SINK_NOFLAGS',
    1: 'PA_SINK_HW_VOLUME_CTRL',
    2: 'PA_SINK_LATENCY',
    4: 'PA_SINK_HARDWARE',
    8: 'PA_SINK_NETWORK',
    16: 'PA_SINK_HW_MUTE_CTRL',
    32: 'PA_SINK_DECIBEL_VOLUME',
    64: 'PA_SINK_FLAT_VOLUME',
    128: 'PA_SINK_DYNAMIC_LATENCY',
    256: 'PA_SINK_SET_FORMATS',
}
PA_SINK_NOFLAGS = 0
PA_SINK_HW_VOLUME_CTRL = 1
PA_SINK_LATENCY = 2
PA_SINK_HARDWARE = 4
PA_SINK_NETWORK = 8
PA_SINK_HW_MUTE_CTRL = 16
PA_SINK_DECIBEL_VOLUME = 32
PA_SINK_FLAT_VOLUME = 64
PA_SINK_DYNAMIC_LATENCY = 128
PA_SINK_SET_FORMATS = 256
pa_sink_flags = ctypes.c_uint32 # enum
pa_sink_flags_t = pa_sink_flags
pa_sink_flags_t__enumvalues = pa_sink_flags__enumvalues

# values for enumeration 'pa_sink_state'
pa_sink_state__enumvalues = {
    -1: 'PA_SINK_INVALID_STATE',
    0: 'PA_SINK_RUNNING',
    1: 'PA_SINK_IDLE',
    2: 'PA_SINK_SUSPENDED',
    -2: 'PA_SINK_INIT',
    -3: 'PA_SINK_UNLINKED',
}
PA_SINK_INVALID_STATE = -1
PA_SINK_RUNNING = 0
PA_SINK_IDLE = 1
PA_SINK_SUSPENDED = 2
PA_SINK_INIT = -2
PA_SINK_UNLINKED = -3
pa_sink_state = ctypes.c_int32 # enum
pa_sink_state_t = pa_sink_state
pa_sink_state_t__enumvalues = pa_sink_state__enumvalues


# values for enumeration 'pa_source_flags'
pa_source_flags__enumvalues = {
    0: 'PA_SOURCE_NOFLAGS',
    1: 'PA_SOURCE_HW_VOLUME_CTRL',
    2: 'PA_SOURCE_LATENCY',
    4: 'PA_SOURCE_HARDWARE',
    8: 'PA_SOURCE_NETWORK',
    16: 'PA_SOURCE_HW_MUTE_CTRL',
    32: 'PA_SOURCE_DECIBEL_VOLUME',
    64: 'PA_SOURCE_DYNAMIC_LATENCY',
    128: 'PA_SOURCE_FLAT_VOLUME',
}
PA_SOURCE_NOFLAGS = 0
PA_SOURCE_HW_VOLUME_CTRL = 1
PA_SOURCE_LATENCY = 2
PA_SOURCE_HARDWARE = 4
PA_SOURCE_NETWORK = 8
PA_SOURCE_HW_MUTE_CTRL = 16
PA_SOURCE_DECIBEL_VOLUME = 32
PA_SOURCE_DYNAMIC_LATENCY = 64
PA_SOURCE_FLAT_VOLUME = 128
pa_source_flags = ctypes.c_uint32 # enum
pa_source_flags_t = pa_source_flags
pa_source_flags_t__enumvalues = pa_source_flags__enumvalues

# values for enumeration 'pa_source_state'
pa_source_state__enumvalues = {
    -1: 'PA_SOURCE_INVALID_STATE',
    0: 'PA_SOURCE_RUNNING',
    1: 'PA_SOURCE_IDLE',
    2: 'PA_SOURCE_SUSPENDED',
    -2: 'PA_SOURCE_INIT',
    -3: 'PA_SOURCE_UNLINKED',
}
PA_SOURCE_INVALID_STATE = -1
PA_SOURCE_RUNNING = 0
PA_SOURCE_IDLE = 1
PA_SOURCE_SUSPENDED = 2
PA_SOURCE_INIT = -2
PA_SOURCE_UNLINKED = -3
pa_source_state = ctypes.c_int32 # enum
pa_source_state_t = pa_source_state
pa_source_state_t__enumvalues = pa_source_state__enumvalues

pa_free_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(None))

# values for enumeration 'pa_port_available'
pa_port_available__enumvalues = {
    0: 'PA_PORT_AVAILABLE_UNKNOWN',
    1: 'PA_PORT_AVAILABLE_NO',
    2: 'PA_PORT_AVAILABLE_YES',
}
PA_PORT_AVAILABLE_UNKNOWN = 0
PA_PORT_AVAILABLE_NO = 1
PA_PORT_AVAILABLE_YES = 2
pa_port_available = ctypes.c_uint32 # enum
pa_port_available_t = pa_port_available
pa_port_available_t__enumvalues = pa_port_available__enumvalues
class struct_pa_mainloop_api(Structure):
    pass

class struct_pa_io_event(Structure):
    pass


# values for enumeration 'pa_io_event_flags'
pa_io_event_flags__enumvalues = {
    0: 'PA_IO_EVENT_NULL',
    1: 'PA_IO_EVENT_INPUT',
    2: 'PA_IO_EVENT_OUTPUT',
    4: 'PA_IO_EVENT_HANGUP',
    8: 'PA_IO_EVENT_ERROR',
}
PA_IO_EVENT_NULL = 0
PA_IO_EVENT_INPUT = 1
PA_IO_EVENT_OUTPUT = 2
PA_IO_EVENT_HANGUP = 4
PA_IO_EVENT_ERROR = 8
pa_io_event_flags = ctypes.c_uint32 # enum
class struct_pa_time_event(Structure):
    pass

class struct_pa_defer_event(Structure):
    pass

struct_pa_mainloop_api._pack_ = 1 # source:False
struct_pa_mainloop_api._fields_ = [
    ('userdata', ctypes.POINTER(None)),
    ('io_new', ctypes.CFUNCTYPE(ctypes.POINTER(struct_pa_io_event), ctypes.POINTER(struct_pa_mainloop_api), ctypes.c_int32, pa_io_event_flags, ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_io_event), ctypes.c_int32, pa_io_event_flags, ctypes.POINTER(None)), ctypes.POINTER(None))),
    ('io_enable', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_io_event), pa_io_event_flags)),
    ('io_free', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_io_event))),
    ('io_set_destroy', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_io_event), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_io_event), ctypes.POINTER(None)))),
    ('time_new', ctypes.CFUNCTYPE(ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_timeval), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(struct_timeval), ctypes.POINTER(None)), ctypes.POINTER(None))),
    ('time_restart', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(struct_timeval))),
    ('time_free', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_time_event))),
    ('time_set_destroy', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_time_event), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(None)))),
    ('defer_new', ctypes.CFUNCTYPE(ctypes.POINTER(struct_pa_defer_event), ctypes.POINTER(struct_pa_mainloop_api), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_defer_event), ctypes.POINTER(None)), ctypes.POINTER(None))),
    ('defer_enable', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_defer_event), ctypes.c_int32)),
    ('defer_free', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_defer_event))),
    ('defer_set_destroy', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_defer_event), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_defer_event), ctypes.POINTER(None)))),
    ('quit', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.c_int32)),
]

pa_mainloop_api = struct_pa_mainloop_api
pa_io_event_flags_t = pa_io_event_flags
pa_io_event_flags_t__enumvalues = pa_io_event_flags__enumvalues
pa_io_event = struct_pa_io_event
pa_io_event_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_io_event), ctypes.c_int32, pa_io_event_flags, ctypes.POINTER(None))
pa_io_event_destroy_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_io_event), ctypes.POINTER(None))
pa_time_event = struct_pa_time_event
pa_time_event_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(struct_timeval), ctypes.POINTER(None))
pa_time_event_destroy_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_time_event), ctypes.POINTER(None))
pa_defer_event = struct_pa_defer_event
pa_defer_event_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_defer_event), ctypes.POINTER(None))
pa_defer_event_destroy_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_defer_event), ctypes.POINTER(None))
pa_mainloop_api_once = _libraries['libpulse.so.0'].pa_mainloop_api_once
pa_mainloop_api_once.restype = None
pa_mainloop_api_once.argtypes = [ctypes.POINTER(struct_pa_mainloop_api), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(None)), ctypes.POINTER(None)]
class struct_pa_operation(Structure):
    pass

pa_operation = struct_pa_operation
pa_operation_notify_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_operation), ctypes.POINTER(None))
pa_operation_ref = _libraries['libpulse.so.0'].pa_operation_ref
pa_operation_ref.restype = ctypes.POINTER(struct_pa_operation)
pa_operation_ref.argtypes = [ctypes.POINTER(struct_pa_operation)]
pa_operation_unref = _libraries['libpulse.so.0'].pa_operation_unref
pa_operation_unref.restype = None
pa_operation_unref.argtypes = [ctypes.POINTER(struct_pa_operation)]
pa_operation_cancel = _libraries['libpulse.so.0'].pa_operation_cancel
pa_operation_cancel.restype = None
pa_operation_cancel.argtypes = [ctypes.POINTER(struct_pa_operation)]
pa_operation_get_state = _libraries['libpulse.so.0'].pa_operation_get_state
pa_operation_get_state.restype = pa_operation_state_t
pa_operation_get_state.argtypes = [ctypes.POINTER(struct_pa_operation)]
pa_operation_set_state_callback = _libraries['libpulse.so.0'].pa_operation_set_state_callback
pa_operation_set_state_callback.restype = None
pa_operation_set_state_callback.argtypes = [ctypes.POINTER(struct_pa_operation), pa_operation_notify_cb_t, ctypes.POINTER(None)]
class struct_pa_proplist(Structure):
    pass

pa_proplist = struct_pa_proplist
pa_proplist_new = _libraries['libpulse.so.0'].pa_proplist_new
pa_proplist_new.restype = ctypes.POINTER(struct_pa_proplist)
pa_proplist_new.argtypes = []
pa_proplist_free = _libraries['libpulse.so.0'].pa_proplist_free
pa_proplist_free.restype = None
pa_proplist_free.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_key_valid = _libraries['libpulse.so.0'].pa_proplist_key_valid
pa_proplist_key_valid.restype = ctypes.c_int32
pa_proplist_key_valid.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_proplist_sets = _libraries['libpulse.so.0'].pa_proplist_sets
pa_proplist_sets.restype = ctypes.c_int32
pa_proplist_sets.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
pa_proplist_setp = _libraries['libpulse.so.0'].pa_proplist_setp
pa_proplist_setp.restype = ctypes.c_int32
pa_proplist_setp.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char)]
pa_proplist_setf = _libraries['libpulse.so.0'].pa_proplist_setf
pa_proplist_setf.restype = ctypes.c_int32
pa_proplist_setf.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
pa_proplist_set = _libraries['libpulse.so.0'].pa_proplist_set
pa_proplist_set.restype = ctypes.c_int32
pa_proplist_set.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), size_t]
pa_proplist_gets = _libraries['libpulse.so.0'].pa_proplist_gets
pa_proplist_gets.restype = ctypes.POINTER(ctypes.c_char)
pa_proplist_gets.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char)]
pa_proplist_get = _libraries['libpulse.so.0'].pa_proplist_get
pa_proplist_get.restype = ctypes.c_int32
pa_proplist_get.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_uint64)]

# values for enumeration 'pa_update_mode'
pa_update_mode__enumvalues = {
    0: 'PA_UPDATE_SET',
    1: 'PA_UPDATE_MERGE',
    2: 'PA_UPDATE_REPLACE',
}
PA_UPDATE_SET = 0
PA_UPDATE_MERGE = 1
PA_UPDATE_REPLACE = 2
pa_update_mode = ctypes.c_uint32 # enum
pa_update_mode_t = pa_update_mode
pa_update_mode_t__enumvalues = pa_update_mode__enumvalues
pa_proplist_update = _libraries['libpulse.so.0'].pa_proplist_update
pa_proplist_update.restype = None
pa_proplist_update.argtypes = [ctypes.POINTER(struct_pa_proplist), pa_update_mode_t, ctypes.POINTER(struct_pa_proplist)]
pa_proplist_unset = _libraries['libpulse.so.0'].pa_proplist_unset
pa_proplist_unset.restype = ctypes.c_int32
pa_proplist_unset.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char)]
pa_proplist_unset_many = _libraries['libpulse.so.0'].pa_proplist_unset_many
pa_proplist_unset_many.restype = ctypes.c_int32
pa_proplist_unset_many.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char) * 0]
pa_proplist_iterate = _libraries['libpulse.so.0'].pa_proplist_iterate
pa_proplist_iterate.restype = ctypes.POINTER(ctypes.c_char)
pa_proplist_iterate.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.POINTER(None))]
pa_proplist_to_string = _libraries['libpulse.so.0'].pa_proplist_to_string
pa_proplist_to_string.restype = ctypes.POINTER(ctypes.c_char)
pa_proplist_to_string.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_to_string_sep = _libraries['libpulse.so.0'].pa_proplist_to_string_sep
pa_proplist_to_string_sep.restype = ctypes.POINTER(ctypes.c_char)
pa_proplist_to_string_sep.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char)]
pa_proplist_from_string = _libraries['libpulse.so.0'].pa_proplist_from_string
pa_proplist_from_string.restype = ctypes.POINTER(struct_pa_proplist)
pa_proplist_from_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_proplist_contains = _libraries['libpulse.so.0'].pa_proplist_contains
pa_proplist_contains.restype = ctypes.c_int32
pa_proplist_contains.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(ctypes.c_char)]
pa_proplist_clear = _libraries['libpulse.so.0'].pa_proplist_clear
pa_proplist_clear.restype = None
pa_proplist_clear.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_copy = _libraries['libpulse.so.0'].pa_proplist_copy
pa_proplist_copy.restype = ctypes.POINTER(struct_pa_proplist)
pa_proplist_copy.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_size = _libraries['libpulse.so.0'].pa_proplist_size
pa_proplist_size.restype = ctypes.c_uint32
pa_proplist_size.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_isempty = _libraries['libpulse.so.0'].pa_proplist_isempty
pa_proplist_isempty.restype = ctypes.c_int32
pa_proplist_isempty.argtypes = [ctypes.POINTER(struct_pa_proplist)]
pa_proplist_equal = _libraries['libpulse.so.0'].pa_proplist_equal
pa_proplist_equal.restype = ctypes.c_int32
pa_proplist_equal.argtypes = [ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(struct_pa_proplist)]
class struct_pa_context(Structure):
    pass

pa_context = struct_pa_context
pa_context_notify_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(None))
pa_context_success_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_int32, ctypes.POINTER(None))
pa_context_event_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(None))
pa_context_new = _libraries['libpulse.so.0'].pa_context_new
pa_context_new.restype = ctypes.POINTER(struct_pa_context)
pa_context_new.argtypes = [ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(ctypes.c_char)]
pa_context_new_with_proplist = _libraries['libpulse.so.0'].pa_context_new_with_proplist
pa_context_new_with_proplist.restype = ctypes.POINTER(struct_pa_context)
pa_context_new_with_proplist.argtypes = [ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_proplist)]
pa_context_unref = _libraries['libpulse.so.0'].pa_context_unref
pa_context_unref.restype = None
pa_context_unref.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_ref = _libraries['libpulse.so.0'].pa_context_ref
pa_context_ref.restype = ctypes.POINTER(struct_pa_context)
pa_context_ref.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_set_state_callback = _libraries['libpulse.so.0'].pa_context_set_state_callback
pa_context_set_state_callback.restype = None
pa_context_set_state_callback.argtypes = [ctypes.POINTER(struct_pa_context), pa_context_notify_cb_t, ctypes.POINTER(None)]
pa_context_set_event_callback = _libraries['libpulse.so.0'].pa_context_set_event_callback
pa_context_set_event_callback.restype = None
pa_context_set_event_callback.argtypes = [ctypes.POINTER(struct_pa_context), pa_context_event_cb_t, ctypes.POINTER(None)]
pa_context_errno = _libraries['libpulse.so.0'].pa_context_errno
pa_context_errno.restype = ctypes.c_int32
pa_context_errno.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_is_pending = _libraries['libpulse.so.0'].pa_context_is_pending
pa_context_is_pending.restype = ctypes.c_int32
pa_context_is_pending.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_get_state = _libraries['libpulse.so.0'].pa_context_get_state
pa_context_get_state.restype = pa_context_state_t
pa_context_get_state.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_connect = _libraries['libpulse.so.0'].pa_context_connect
pa_context_connect.restype = ctypes.c_int32
pa_context_connect.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_context_flags_t, ctypes.POINTER(struct_pa_spawn_api)]
pa_context_disconnect = _libraries['libpulse.so.0'].pa_context_disconnect
pa_context_disconnect.restype = None
pa_context_disconnect.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_drain = _libraries['libpulse.so.0'].pa_context_drain
pa_context_drain.restype = ctypes.POINTER(struct_pa_operation)
pa_context_drain.argtypes = [ctypes.POINTER(struct_pa_context), pa_context_notify_cb_t, ctypes.POINTER(None)]
pa_context_exit_daemon = _libraries['libpulse.so.0'].pa_context_exit_daemon
pa_context_exit_daemon.restype = ctypes.POINTER(struct_pa_operation)
pa_context_exit_daemon.argtypes = [ctypes.POINTER(struct_pa_context), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_default_sink = _libraries['libpulse.so.0'].pa_context_set_default_sink
pa_context_set_default_sink.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_default_sink.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_default_source = _libraries['libpulse.so.0'].pa_context_set_default_source
pa_context_set_default_source.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_default_source.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_is_local = _libraries['libpulse.so.0'].pa_context_is_local
pa_context_is_local.restype = ctypes.c_int32
pa_context_is_local.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_set_name = _libraries['libpulse.so.0'].pa_context_set_name
pa_context_set_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_get_server = _libraries['libpulse.so.0'].pa_context_get_server
pa_context_get_server.restype = ctypes.POINTER(ctypes.c_char)
pa_context_get_server.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_get_protocol_version = _libraries['libpulse.so.0'].pa_context_get_protocol_version
pa_context_get_protocol_version.restype = uint32_t
pa_context_get_protocol_version.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_get_server_protocol_version = _libraries['libpulse.so.0'].pa_context_get_server_protocol_version
pa_context_get_server_protocol_version.restype = uint32_t
pa_context_get_server_protocol_version.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_proplist_update = _libraries['libpulse.so.0'].pa_context_proplist_update
pa_context_proplist_update.restype = ctypes.POINTER(struct_pa_operation)
pa_context_proplist_update.argtypes = [ctypes.POINTER(struct_pa_context), pa_update_mode_t, ctypes.POINTER(struct_pa_proplist), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_proplist_remove = _libraries['libpulse.so.0'].pa_context_proplist_remove
pa_context_proplist_remove.restype = ctypes.POINTER(struct_pa_operation)
pa_context_proplist_remove.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char) * 0, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_get_index = _libraries['libpulse.so.0'].pa_context_get_index
pa_context_get_index.restype = uint32_t
pa_context_get_index.argtypes = [ctypes.POINTER(struct_pa_context)]
pa_context_rttime_new = _libraries['libpulse.so.0'].pa_context_rttime_new
pa_context_rttime_new.restype = ctypes.POINTER(struct_pa_time_event)
pa_context_rttime_new.argtypes = [ctypes.POINTER(struct_pa_context), pa_usec_t, pa_time_event_cb_t, ctypes.POINTER(None)]
pa_context_rttime_restart = _libraries['libpulse.so.0'].pa_context_rttime_restart
pa_context_rttime_restart.restype = None
pa_context_rttime_restart.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_time_event), pa_usec_t]
pa_context_get_tile_size = _libraries['libpulse.so.0'].pa_context_get_tile_size
pa_context_get_tile_size.restype = size_t
pa_context_get_tile_size.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_sample_spec)]
pa_context_load_cookie_from_file = _libraries['libpulse.so.0'].pa_context_load_cookie_from_file
pa_context_load_cookie_from_file.restype = ctypes.c_int32
pa_context_load_cookie_from_file.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char)]
pa_direction_valid = _libraries['libpulse.so.0'].pa_direction_valid
pa_direction_valid.restype = ctypes.c_int32
pa_direction_valid.argtypes = [pa_direction_t]
pa_direction_to_string = _libraries['libpulse.so.0'].pa_direction_to_string
pa_direction_to_string.restype = ctypes.POINTER(ctypes.c_char)
pa_direction_to_string.argtypes = [pa_direction_t]
pa_strerror = _libraries['libpulse.so.0'].pa_strerror
pa_strerror.restype = ctypes.POINTER(ctypes.c_char)
pa_strerror.argtypes = [ctypes.c_int32]
class struct_pa_ext_device_manager_role_priority_info(Structure):
    pass

struct_pa_ext_device_manager_role_priority_info._pack_ = 1 # source:False
struct_pa_ext_device_manager_role_priority_info._fields_ = [
    ('role', ctypes.POINTER(ctypes.c_char)),
    ('priority', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

pa_ext_device_manager_role_priority_info = struct_pa_ext_device_manager_role_priority_info
class struct_pa_ext_device_manager_info(Structure):
    pass

struct_pa_ext_device_manager_info._pack_ = 1 # source:False
struct_pa_ext_device_manager_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('icon', ctypes.POINTER(ctypes.c_char)),
    ('index', ctypes.c_uint32),
    ('n_role_priorities', ctypes.c_uint32),
    ('role_priorities', ctypes.POINTER(struct_pa_ext_device_manager_role_priority_info)),
]

pa_ext_device_manager_info = struct_pa_ext_device_manager_info
pa_ext_device_manager_test_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_uint32, ctypes.POINTER(None))
pa_ext_device_manager_test = _libraries['libpulse.so.0'].pa_ext_device_manager_test
pa_ext_device_manager_test.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_test.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_manager_test_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_read_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_ext_device_manager_info), ctypes.c_int32, ctypes.POINTER(None))
pa_ext_device_manager_read = _libraries['libpulse.so.0'].pa_ext_device_manager_read
pa_ext_device_manager_read.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_read.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_manager_read_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_set_device_description = _libraries['libpulse.so.0'].pa_ext_device_manager_set_device_description
pa_ext_device_manager_set_device_description.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_set_device_description.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_delete = _libraries['libpulse.so.0'].pa_ext_device_manager_delete
pa_ext_device_manager_delete.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_delete.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char) * 0, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_enable_role_device_priority_routing = _libraries['libpulse.so.0'].pa_ext_device_manager_enable_role_device_priority_routing
pa_ext_device_manager_enable_role_device_priority_routing.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_enable_role_device_priority_routing.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_reorder_devices_for_role = _libraries['libpulse.so.0'].pa_ext_device_manager_reorder_devices_for_role
pa_ext_device_manager_reorder_devices_for_role.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_reorder_devices_for_role.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_subscribe = _libraries['libpulse.so.0'].pa_ext_device_manager_subscribe
pa_ext_device_manager_subscribe.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_manager_subscribe.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_manager_subscribe_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(None))
pa_ext_device_manager_set_subscribe_cb = _libraries['libpulse.so.0'].pa_ext_device_manager_set_subscribe_cb
pa_ext_device_manager_set_subscribe_cb.restype = None
pa_ext_device_manager_set_subscribe_cb.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_manager_subscribe_cb_t, ctypes.POINTER(None)]

# values for enumeration 'pa_encoding'
pa_encoding__enumvalues = {
    0: 'PA_ENCODING_ANY',
    1: 'PA_ENCODING_PCM',
    2: 'PA_ENCODING_AC3_IEC61937',
    3: 'PA_ENCODING_EAC3_IEC61937',
    4: 'PA_ENCODING_MPEG_IEC61937',
    5: 'PA_ENCODING_DTS_IEC61937',
    6: 'PA_ENCODING_MPEG2_AAC_IEC61937',
    7: 'PA_ENCODING_TRUEHD_IEC61937',
    8: 'PA_ENCODING_DTSHD_IEC61937',
    9: 'PA_ENCODING_MAX',
    -1: 'PA_ENCODING_INVALID',
}
PA_ENCODING_ANY = 0
PA_ENCODING_PCM = 1
PA_ENCODING_AC3_IEC61937 = 2
PA_ENCODING_EAC3_IEC61937 = 3
PA_ENCODING_MPEG_IEC61937 = 4
PA_ENCODING_DTS_IEC61937 = 5
PA_ENCODING_MPEG2_AAC_IEC61937 = 6
PA_ENCODING_TRUEHD_IEC61937 = 7
PA_ENCODING_DTSHD_IEC61937 = 8
PA_ENCODING_MAX = 9
PA_ENCODING_INVALID = -1
pa_encoding = ctypes.c_int32 # enum
pa_encoding_t = pa_encoding
pa_encoding_t__enumvalues = pa_encoding__enumvalues
pa_encoding_to_string = _libraries['libpulse.so.0'].pa_encoding_to_string
pa_encoding_to_string.restype = ctypes.POINTER(ctypes.c_char)
pa_encoding_to_string.argtypes = [pa_encoding_t]
pa_encoding_from_string = _libraries['libpulse.so.0'].pa_encoding_from_string
pa_encoding_from_string.restype = pa_encoding_t
pa_encoding_from_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
class struct_pa_format_info(Structure):
    pass

struct_pa_format_info._pack_ = 1 # source:False
struct_pa_format_info._fields_ = [
    ('encoding', pa_encoding_t),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('plist', ctypes.POINTER(struct_pa_proplist)),
]

pa_format_info = struct_pa_format_info
pa_format_info_new = _libraries['libpulse.so.0'].pa_format_info_new
pa_format_info_new.restype = ctypes.POINTER(struct_pa_format_info)
pa_format_info_new.argtypes = []
pa_format_info_copy = _libraries['libpulse.so.0'].pa_format_info_copy
pa_format_info_copy.restype = ctypes.POINTER(struct_pa_format_info)
pa_format_info_copy.argtypes = [ctypes.POINTER(struct_pa_format_info)]
pa_format_info_free = _libraries['libpulse.so.0'].pa_format_info_free
pa_format_info_free.restype = None
pa_format_info_free.argtypes = [ctypes.POINTER(struct_pa_format_info)]
pa_format_info_valid = _libraries['libpulse.so.0'].pa_format_info_valid
pa_format_info_valid.restype = ctypes.c_int32
pa_format_info_valid.argtypes = [ctypes.POINTER(struct_pa_format_info)]
pa_format_info_is_pcm = _libraries['libpulse.so.0'].pa_format_info_is_pcm
pa_format_info_is_pcm.restype = ctypes.c_int32
pa_format_info_is_pcm.argtypes = [ctypes.POINTER(struct_pa_format_info)]
pa_format_info_is_compatible = _libraries['libpulse.so.0'].pa_format_info_is_compatible
pa_format_info_is_compatible.restype = ctypes.c_int32
pa_format_info_is_compatible.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(struct_pa_format_info)]
pa_format_info_snprint = _libraries['libpulse.so.0'].pa_format_info_snprint
pa_format_info_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_format_info_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_format_info)]
pa_format_info_from_string = _libraries['libpulse.so.0'].pa_format_info_from_string
pa_format_info_from_string.restype = ctypes.POINTER(struct_pa_format_info)
pa_format_info_from_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_format_info_from_sample_spec = _libraries['libpulse.so.0'].pa_format_info_from_sample_spec
pa_format_info_from_sample_spec.restype = ctypes.POINTER(struct_pa_format_info)
pa_format_info_from_sample_spec.argtypes = [ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_channel_map)]
pa_format_info_to_sample_spec = _libraries['libpulse.so.0'].pa_format_info_to_sample_spec
pa_format_info_to_sample_spec.restype = ctypes.c_int32
pa_format_info_to_sample_spec.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_channel_map)]

# values for enumeration 'pa_prop_type_t'
pa_prop_type_t__enumvalues = {
    0: 'PA_PROP_TYPE_INT',
    1: 'PA_PROP_TYPE_INT_RANGE',
    2: 'PA_PROP_TYPE_INT_ARRAY',
    3: 'PA_PROP_TYPE_STRING',
    4: 'PA_PROP_TYPE_STRING_ARRAY',
    -1: 'PA_PROP_TYPE_INVALID',
}
PA_PROP_TYPE_INT = 0
PA_PROP_TYPE_INT_RANGE = 1
PA_PROP_TYPE_INT_ARRAY = 2
PA_PROP_TYPE_STRING = 3
PA_PROP_TYPE_STRING_ARRAY = 4
PA_PROP_TYPE_INVALID = -1
pa_prop_type_t = ctypes.c_int32 # enum
pa_format_info_get_prop_type = _libraries['libpulse.so.0'].pa_format_info_get_prop_type
pa_format_info_get_prop_type.restype = pa_prop_type_t
pa_format_info_get_prop_type.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char)]
pa_format_info_get_prop_int = _libraries['libpulse.so.0'].pa_format_info_get_prop_int
pa_format_info_get_prop_int.restype = ctypes.c_int32
pa_format_info_get_prop_int.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int32)]
pa_format_info_get_prop_int_range = _libraries['libpulse.so.0'].pa_format_info_get_prop_int_range
pa_format_info_get_prop_int_range.restype = ctypes.c_int32
pa_format_info_get_prop_int_range.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
pa_format_info_get_prop_int_array = _libraries['libpulse.so.0'].pa_format_info_get_prop_int_array
pa_format_info_get_prop_int_array.restype = ctypes.c_int32
pa_format_info_get_prop_int_array.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)), ctypes.POINTER(ctypes.c_int32)]
pa_format_info_get_prop_string = _libraries['libpulse.so.0'].pa_format_info_get_prop_string
pa_format_info_get_prop_string.restype = ctypes.c_int32
pa_format_info_get_prop_string.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
pa_format_info_get_prop_string_array = _libraries['libpulse.so.0'].pa_format_info_get_prop_string_array
pa_format_info_get_prop_string_array.restype = ctypes.c_int32
pa_format_info_get_prop_string_array.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_char))), ctypes.POINTER(ctypes.c_int32)]
pa_format_info_free_string_array = _libraries['libpulse.so.0'].pa_format_info_free_string_array
pa_format_info_free_string_array.restype = None
pa_format_info_free_string_array.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int32]
pa_format_info_get_sample_format = _libraries['libpulse.so.0'].pa_format_info_get_sample_format
pa_format_info_get_sample_format.restype = ctypes.c_int32
pa_format_info_get_sample_format.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(pa_sample_format)]
pa_format_info_get_rate = _libraries['libpulse.so.0'].pa_format_info_get_rate
pa_format_info_get_rate.restype = ctypes.c_int32
pa_format_info_get_rate.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_uint32)]
pa_format_info_get_channels = _libraries['libpulse.so.0'].pa_format_info_get_channels
pa_format_info_get_channels.restype = ctypes.c_int32
pa_format_info_get_channels.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_ubyte)]
pa_format_info_get_channel_map = _libraries['libpulse.so.0'].pa_format_info_get_channel_map
pa_format_info_get_channel_map.restype = ctypes.c_int32
pa_format_info_get_channel_map.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(struct_pa_channel_map)]
pa_format_info_set_prop_int = _libraries['libpulse.so.0'].pa_format_info_set_prop_int
pa_format_info_set_prop_int.restype = None
pa_format_info_set_prop_int.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.c_int32]
pa_format_info_set_prop_int_array = _libraries['libpulse.so.0'].pa_format_info_set_prop_int_array
pa_format_info_set_prop_int_array.restype = None
pa_format_info_set_prop_int_array.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
pa_format_info_set_prop_int_range = _libraries['libpulse.so.0'].pa_format_info_set_prop_int_range
pa_format_info_set_prop_int_range.restype = None
pa_format_info_set_prop_int_range.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
pa_format_info_set_prop_string = _libraries['libpulse.so.0'].pa_format_info_set_prop_string
pa_format_info_set_prop_string.restype = None
pa_format_info_set_prop_string.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
pa_format_info_set_prop_string_array = _libraries['libpulse.so.0'].pa_format_info_set_prop_string_array
pa_format_info_set_prop_string_array.restype = None
pa_format_info_set_prop_string_array.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int32]
pa_format_info_set_sample_format = _libraries['libpulse.so.0'].pa_format_info_set_sample_format
pa_format_info_set_sample_format.restype = None
pa_format_info_set_sample_format.argtypes = [ctypes.POINTER(struct_pa_format_info), pa_sample_format_t]
pa_format_info_set_rate = _libraries['libpulse.so.0'].pa_format_info_set_rate
pa_format_info_set_rate.restype = None
pa_format_info_set_rate.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.c_int32]
pa_format_info_set_channels = _libraries['libpulse.so.0'].pa_format_info_set_channels
pa_format_info_set_channels.restype = None
pa_format_info_set_channels.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.c_int32]
pa_format_info_set_channel_map = _libraries['libpulse.so.0'].pa_format_info_set_channel_map
pa_format_info_set_channel_map.restype = None
pa_format_info_set_channel_map.argtypes = [ctypes.POINTER(struct_pa_format_info), ctypes.POINTER(struct_pa_channel_map)]
class struct_pa_ext_device_restore_info(Structure):
    pass

struct_pa_ext_device_restore_info._pack_ = 1 # source:False
struct_pa_ext_device_restore_info._fields_ = [
    ('type', pa_device_type_t),
    ('index', ctypes.c_uint32),
    ('n_formats', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('formats', ctypes.POINTER(ctypes.POINTER(struct_pa_format_info))),
]

pa_ext_device_restore_info = struct_pa_ext_device_restore_info
pa_ext_device_restore_test_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_uint32, ctypes.POINTER(None))
pa_ext_device_restore_test = _libraries['libpulse.so.0'].pa_ext_device_restore_test
pa_ext_device_restore_test.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_restore_test.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_restore_test_cb_t, ctypes.POINTER(None)]
pa_ext_device_restore_subscribe = _libraries['libpulse.so.0'].pa_ext_device_restore_subscribe
pa_ext_device_restore_subscribe.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_restore_subscribe.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_device_restore_subscribe_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), pa_device_type, ctypes.c_uint32, ctypes.POINTER(None))
pa_ext_device_restore_set_subscribe_cb = _libraries['libpulse.so.0'].pa_ext_device_restore_set_subscribe_cb
pa_ext_device_restore_set_subscribe_cb.restype = None
pa_ext_device_restore_set_subscribe_cb.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_restore_subscribe_cb_t, ctypes.POINTER(None)]
pa_ext_device_restore_read_device_formats_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_ext_device_restore_info), ctypes.c_int32, ctypes.POINTER(None))
pa_ext_device_restore_read_formats_all = _libraries['libpulse.so.0'].pa_ext_device_restore_read_formats_all
pa_ext_device_restore_read_formats_all.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_restore_read_formats_all.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_device_restore_read_device_formats_cb_t, ctypes.POINTER(None)]
pa_ext_device_restore_read_formats = _libraries['libpulse.so.0'].pa_ext_device_restore_read_formats
pa_ext_device_restore_read_formats.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_restore_read_formats.argtypes = [ctypes.POINTER(struct_pa_context), pa_device_type_t, uint32_t, pa_ext_device_restore_read_device_formats_cb_t, ctypes.POINTER(None)]
pa_ext_device_restore_save_formats = _libraries['libpulse.so.0'].pa_ext_device_restore_save_formats
pa_ext_device_restore_save_formats.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_device_restore_save_formats.argtypes = [ctypes.POINTER(struct_pa_context), pa_device_type_t, uint32_t, uint8_t, ctypes.POINTER(ctypes.POINTER(struct_pa_format_info)), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_volume_t = ctypes.c_uint32
class struct_pa_cvolume(Structure):
    pass

struct_pa_cvolume._pack_ = 1 # source:False
struct_pa_cvolume._fields_ = [
    ('channels', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('values', ctypes.c_uint32 * 32),
]

pa_cvolume = struct_pa_cvolume
pa_cvolume_equal = _libraries['libpulse.so.0'].pa_cvolume_equal
pa_cvolume_equal.restype = ctypes.c_int32
pa_cvolume_equal.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_init = _libraries['libpulse.so.0'].pa_cvolume_init
pa_cvolume_init.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_init.argtypes = [ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_set = _libraries['libpulse.so.0'].pa_cvolume_set
pa_cvolume_set.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_set.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.c_uint32, pa_volume_t]
pa_cvolume_snprint = _libraries['libpulse.so.0'].pa_cvolume_snprint
pa_cvolume_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_cvolume_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_cvolume)]
pa_sw_cvolume_snprint_dB = _libraries['libpulse.so.0'].pa_sw_cvolume_snprint_dB
pa_sw_cvolume_snprint_dB.restype = ctypes.POINTER(ctypes.c_char)
pa_sw_cvolume_snprint_dB.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_snprint_verbose = _libraries['libpulse.so.0'].pa_cvolume_snprint_verbose
pa_cvolume_snprint_verbose.restype = ctypes.POINTER(ctypes.c_char)
pa_cvolume_snprint_verbose.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), ctypes.c_int32]
pa_volume_snprint = _libraries['libpulse.so.0'].pa_volume_snprint
pa_volume_snprint.restype = ctypes.POINTER(ctypes.c_char)
pa_volume_snprint.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, pa_volume_t]
pa_sw_volume_snprint_dB = _libraries['libpulse.so.0'].pa_sw_volume_snprint_dB
pa_sw_volume_snprint_dB.restype = ctypes.POINTER(ctypes.c_char)
pa_sw_volume_snprint_dB.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, pa_volume_t]
pa_volume_snprint_verbose = _libraries['libpulse.so.0'].pa_volume_snprint_verbose
pa_volume_snprint_verbose.restype = ctypes.POINTER(ctypes.c_char)
pa_volume_snprint_verbose.argtypes = [ctypes.POINTER(ctypes.c_char), size_t, pa_volume_t, ctypes.c_int32]
pa_cvolume_avg = _libraries['libpulse.so.0'].pa_cvolume_avg
pa_cvolume_avg.restype = pa_volume_t
pa_cvolume_avg.argtypes = [ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_avg_mask = _libraries['libpulse.so.0'].pa_cvolume_avg_mask
pa_cvolume_avg_mask.restype = pa_volume_t
pa_cvolume_avg_mask.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), pa_channel_position_mask_t]
pa_cvolume_max = _libraries['libpulse.so.0'].pa_cvolume_max
pa_cvolume_max.restype = pa_volume_t
pa_cvolume_max.argtypes = [ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_max_mask = _libraries['libpulse.so.0'].pa_cvolume_max_mask
pa_cvolume_max_mask.restype = pa_volume_t
pa_cvolume_max_mask.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), pa_channel_position_mask_t]
pa_cvolume_min = _libraries['libpulse.so.0'].pa_cvolume_min
pa_cvolume_min.restype = pa_volume_t
pa_cvolume_min.argtypes = [ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_min_mask = _libraries['libpulse.so.0'].pa_cvolume_min_mask
pa_cvolume_min_mask.restype = pa_volume_t
pa_cvolume_min_mask.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), pa_channel_position_mask_t]
pa_cvolume_valid = _libraries['libpulse.so.0'].pa_cvolume_valid
pa_cvolume_valid.restype = ctypes.c_int32
pa_cvolume_valid.argtypes = [ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_channels_equal_to = _libraries['libpulse.so.0'].pa_cvolume_channels_equal_to
pa_cvolume_channels_equal_to.restype = ctypes.c_int32
pa_cvolume_channels_equal_to.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
pa_sw_volume_multiply = _libraries['libpulse.so.0'].pa_sw_volume_multiply
pa_sw_volume_multiply.restype = pa_volume_t
pa_sw_volume_multiply.argtypes = [pa_volume_t, pa_volume_t]
pa_sw_cvolume_multiply = _libraries['libpulse.so.0'].pa_sw_cvolume_multiply
pa_sw_cvolume_multiply.restype = ctypes.POINTER(struct_pa_cvolume)
pa_sw_cvolume_multiply.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume)]
pa_sw_cvolume_multiply_scalar = _libraries['libpulse.so.0'].pa_sw_cvolume_multiply_scalar
pa_sw_cvolume_multiply_scalar.restype = ctypes.POINTER(struct_pa_cvolume)
pa_sw_cvolume_multiply_scalar.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
pa_sw_volume_divide = _libraries['libpulse.so.0'].pa_sw_volume_divide
pa_sw_volume_divide.restype = pa_volume_t
pa_sw_volume_divide.argtypes = [pa_volume_t, pa_volume_t]
pa_sw_cvolume_divide = _libraries['libpulse.so.0'].pa_sw_cvolume_divide
pa_sw_cvolume_divide.restype = ctypes.POINTER(struct_pa_cvolume)
pa_sw_cvolume_divide.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume)]
pa_sw_cvolume_divide_scalar = _libraries['libpulse.so.0'].pa_sw_cvolume_divide_scalar
pa_sw_cvolume_divide_scalar.restype = ctypes.POINTER(struct_pa_cvolume)
pa_sw_cvolume_divide_scalar.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
pa_sw_volume_from_dB = _libraries['libpulse.so.0'].pa_sw_volume_from_dB
pa_sw_volume_from_dB.restype = pa_volume_t
pa_sw_volume_from_dB.argtypes = [ctypes.c_double]
pa_sw_volume_to_dB = _libraries['libpulse.so.0'].pa_sw_volume_to_dB
pa_sw_volume_to_dB.restype = ctypes.c_double
pa_sw_volume_to_dB.argtypes = [pa_volume_t]
pa_sw_volume_from_linear = _libraries['libpulse.so.0'].pa_sw_volume_from_linear
pa_sw_volume_from_linear.restype = pa_volume_t
pa_sw_volume_from_linear.argtypes = [ctypes.c_double]
pa_sw_volume_to_linear = _libraries['libpulse.so.0'].pa_sw_volume_to_linear
pa_sw_volume_to_linear.restype = ctypes.c_double
pa_sw_volume_to_linear.argtypes = [pa_volume_t]
pa_cvolume_remap = _libraries['libpulse.so.0'].pa_cvolume_remap
pa_cvolume_remap.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_remap.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_channel_map)]
pa_cvolume_compatible = _libraries['libpulse.so.0'].pa_cvolume_compatible
pa_cvolume_compatible.restype = ctypes.c_int32
pa_cvolume_compatible.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_sample_spec)]
pa_cvolume_compatible_with_channel_map = _libraries['libpulse.so.0'].pa_cvolume_compatible_with_channel_map
pa_cvolume_compatible_with_channel_map.restype = ctypes.c_int32
pa_cvolume_compatible_with_channel_map.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map)]
pa_cvolume_get_balance = _libraries['libpulse.so.0'].pa_cvolume_get_balance
pa_cvolume_get_balance.restype = ctypes.c_float
pa_cvolume_get_balance.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map)]
pa_cvolume_set_balance = _libraries['libpulse.so.0'].pa_cvolume_set_balance
pa_cvolume_set_balance.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_set_balance.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), ctypes.c_float]
pa_cvolume_get_fade = _libraries['libpulse.so.0'].pa_cvolume_get_fade
pa_cvolume_get_fade.restype = ctypes.c_float
pa_cvolume_get_fade.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map)]
pa_cvolume_set_fade = _libraries['libpulse.so.0'].pa_cvolume_set_fade
pa_cvolume_set_fade.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_set_fade.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), ctypes.c_float]
pa_cvolume_get_lfe_balance = _libraries['libpulse.so.0'].pa_cvolume_get_lfe_balance
pa_cvolume_get_lfe_balance.restype = ctypes.c_float
pa_cvolume_get_lfe_balance.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map)]
pa_cvolume_set_lfe_balance = _libraries['libpulse.so.0'].pa_cvolume_set_lfe_balance
pa_cvolume_set_lfe_balance.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_set_lfe_balance.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), ctypes.c_float]
pa_cvolume_scale = _libraries['libpulse.so.0'].pa_cvolume_scale
pa_cvolume_scale.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_scale.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
pa_cvolume_scale_mask = _libraries['libpulse.so.0'].pa_cvolume_scale_mask
pa_cvolume_scale_mask.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_scale_mask.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t, ctypes.POINTER(struct_pa_channel_map), pa_channel_position_mask_t]
pa_cvolume_set_position = _libraries['libpulse.so.0'].pa_cvolume_set_position
pa_cvolume_set_position.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_set_position.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), pa_channel_position_t, pa_volume_t]
pa_cvolume_get_position = _libraries['libpulse.so.0'].pa_cvolume_get_position
pa_cvolume_get_position.restype = pa_volume_t
pa_cvolume_get_position.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_channel_map), pa_channel_position_t]
pa_cvolume_merge = _libraries['libpulse.so.0'].pa_cvolume_merge
pa_cvolume_merge.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_merge.argtypes = [ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_cvolume)]
pa_cvolume_inc_clamp = _libraries['libpulse.so.0'].pa_cvolume_inc_clamp
pa_cvolume_inc_clamp.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_inc_clamp.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t, pa_volume_t]
pa_cvolume_inc = _libraries['libpulse.so.0'].pa_cvolume_inc
pa_cvolume_inc.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_inc.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
pa_cvolume_dec = _libraries['libpulse.so.0'].pa_cvolume_dec
pa_cvolume_dec.restype = ctypes.POINTER(struct_pa_cvolume)
pa_cvolume_dec.argtypes = [ctypes.POINTER(struct_pa_cvolume), pa_volume_t]
class struct_pa_ext_stream_restore_info(Structure):
    pass

struct_pa_ext_stream_restore_info._pack_ = 1 # source:False
struct_pa_ext_stream_restore_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('channel_map', pa_channel_map),
    ('volume', pa_cvolume),
    ('device', ctypes.POINTER(ctypes.c_char)),
    ('mute', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

pa_ext_stream_restore_info = struct_pa_ext_stream_restore_info
pa_ext_stream_restore_test_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_uint32, ctypes.POINTER(None))
pa_ext_stream_restore_test = _libraries['libpulse.so.0'].pa_ext_stream_restore_test
pa_ext_stream_restore_test.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_stream_restore_test.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_stream_restore_test_cb_t, ctypes.POINTER(None)]
pa_ext_stream_restore_read_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_ext_stream_restore_info), ctypes.c_int32, ctypes.POINTER(None))
pa_ext_stream_restore_read = _libraries['libpulse.so.0'].pa_ext_stream_restore_read
pa_ext_stream_restore_read.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_stream_restore_read.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_stream_restore_read_cb_t, ctypes.POINTER(None)]
pa_ext_stream_restore_write = _libraries['libpulse.so.0'].pa_ext_stream_restore_write
pa_ext_stream_restore_write.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_stream_restore_write.argtypes = [ctypes.POINTER(struct_pa_context), pa_update_mode_t, struct_pa_ext_stream_restore_info * 0, ctypes.c_uint32, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_stream_restore_delete = _libraries['libpulse.so.0'].pa_ext_stream_restore_delete
pa_ext_stream_restore_delete.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_stream_restore_delete.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char) * 0, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_stream_restore_subscribe = _libraries['libpulse.so.0'].pa_ext_stream_restore_subscribe
pa_ext_stream_restore_subscribe.restype = ctypes.POINTER(struct_pa_operation)
pa_ext_stream_restore_subscribe.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_ext_stream_restore_subscribe_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(None))
pa_ext_stream_restore_set_subscribe_cb = _libraries['libpulse.so.0'].pa_ext_stream_restore_set_subscribe_cb
pa_ext_stream_restore_set_subscribe_cb.restype = None
pa_ext_stream_restore_set_subscribe_cb.argtypes = [ctypes.POINTER(struct_pa_context), pa_ext_stream_restore_subscribe_cb_t, ctypes.POINTER(None)]
class struct_pa_glib_mainloop(Structure):
    pass

pa_glib_mainloop = struct_pa_glib_mainloop
class struct__GMainContext(Structure):
    pass

pa_glib_mainloop_new = _libraries['libpulse-mainloop-glib.so'].pa_glib_mainloop_new
pa_glib_mainloop_new.restype = ctypes.POINTER(struct_pa_glib_mainloop)
pa_glib_mainloop_new.argtypes = [ctypes.POINTER(struct__GMainContext)]
pa_glib_mainloop_free = _libraries['libpulse-mainloop-glib.so'].pa_glib_mainloop_free
pa_glib_mainloop_free.restype = None
pa_glib_mainloop_free.argtypes = [ctypes.POINTER(struct_pa_glib_mainloop)]
pa_glib_mainloop_get_api = _libraries['libpulse-mainloop-glib.so'].pa_glib_mainloop_get_api
pa_glib_mainloop_get_api.restype = ctypes.POINTER(struct_pa_mainloop_api)
pa_glib_mainloop_get_api.argtypes = [ctypes.POINTER(struct_pa_glib_mainloop)]
class struct_pa_sink_port_info(Structure):
    pass

struct_pa_sink_port_info._pack_ = 1 # source:False
struct_pa_sink_port_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('priority', ctypes.c_uint32),
    ('available', ctypes.c_int32),
]

pa_sink_port_info = struct_pa_sink_port_info
class struct_pa_sink_info(Structure):
    pass

struct_pa_sink_info._pack_ = 1 # source:False
struct_pa_sink_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('sample_spec', pa_sample_spec),
    ('channel_map', pa_channel_map),
    ('owner_module', ctypes.c_uint32),
    ('volume', pa_cvolume),
    ('mute', ctypes.c_int32),
    ('monitor_source', ctypes.c_uint32),
    ('monitor_source_name', ctypes.POINTER(ctypes.c_char)),
    ('latency', ctypes.c_uint64),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('flags', pa_sink_flags_t),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('configured_latency', ctypes.c_uint64),
    ('base_volume', ctypes.c_uint32),
    ('state', pa_sink_state_t),
    ('n_volume_steps', ctypes.c_uint32),
    ('card', ctypes.c_uint32),
    ('n_ports', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('ports', ctypes.POINTER(ctypes.POINTER(struct_pa_sink_port_info))),
    ('active_port', ctypes.POINTER(struct_pa_sink_port_info)),
    ('n_formats', ctypes.c_ubyte),
    ('PADDING_3', ctypes.c_ubyte * 7),
    ('formats', ctypes.POINTER(ctypes.POINTER(struct_pa_format_info))),
]

pa_sink_info = struct_pa_sink_info
pa_sink_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_sink_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_sink_info_by_name = _libraries['libpulse.so.0'].pa_context_get_sink_info_by_name
pa_context_get_sink_info_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sink_info_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_sink_info_cb_t, ctypes.POINTER(None)]
pa_context_get_sink_info_by_index = _libraries['libpulse.so.0'].pa_context_get_sink_info_by_index
pa_context_get_sink_info_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sink_info_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_sink_info_cb_t, ctypes.POINTER(None)]
pa_context_get_sink_info_list = _libraries['libpulse.so.0'].pa_context_get_sink_info_list
pa_context_get_sink_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sink_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_sink_info_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_volume_by_index = _libraries['libpulse.so.0'].pa_context_set_sink_volume_by_index
pa_context_set_sink_volume_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_volume_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_volume_by_name = _libraries['libpulse.so.0'].pa_context_set_sink_volume_by_name
pa_context_set_sink_volume_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_volume_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_mute_by_index = _libraries['libpulse.so.0'].pa_context_set_sink_mute_by_index
pa_context_set_sink_mute_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_mute_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_mute_by_name = _libraries['libpulse.so.0'].pa_context_set_sink_mute_by_name
pa_context_set_sink_mute_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_mute_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_suspend_sink_by_name = _libraries['libpulse.so.0'].pa_context_suspend_sink_by_name
pa_context_suspend_sink_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_suspend_sink_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_suspend_sink_by_index = _libraries['libpulse.so.0'].pa_context_suspend_sink_by_index
pa_context_suspend_sink_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_suspend_sink_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_port_by_index = _libraries['libpulse.so.0'].pa_context_set_sink_port_by_index
pa_context_set_sink_port_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_port_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_port_by_name = _libraries['libpulse.so.0'].pa_context_set_sink_port_by_name
pa_context_set_sink_port_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_port_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_source_port_info(Structure):
    pass

struct_pa_source_port_info._pack_ = 1 # source:False
struct_pa_source_port_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('priority', ctypes.c_uint32),
    ('available', ctypes.c_int32),
]

pa_source_port_info = struct_pa_source_port_info
class struct_pa_source_info(Structure):
    pass

struct_pa_source_info._pack_ = 1 # source:False
struct_pa_source_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('sample_spec', pa_sample_spec),
    ('channel_map', pa_channel_map),
    ('owner_module', ctypes.c_uint32),
    ('volume', pa_cvolume),
    ('mute', ctypes.c_int32),
    ('monitor_of_sink', ctypes.c_uint32),
    ('monitor_of_sink_name', ctypes.POINTER(ctypes.c_char)),
    ('latency', ctypes.c_uint64),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('flags', pa_source_flags_t),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('configured_latency', ctypes.c_uint64),
    ('base_volume', ctypes.c_uint32),
    ('state', pa_source_state_t),
    ('n_volume_steps', ctypes.c_uint32),
    ('card', ctypes.c_uint32),
    ('n_ports', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('ports', ctypes.POINTER(ctypes.POINTER(struct_pa_source_port_info))),
    ('active_port', ctypes.POINTER(struct_pa_source_port_info)),
    ('n_formats', ctypes.c_ubyte),
    ('PADDING_3', ctypes.c_ubyte * 7),
    ('formats', ctypes.POINTER(ctypes.POINTER(struct_pa_format_info))),
]

pa_source_info = struct_pa_source_info
pa_source_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_source_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_source_info_by_name = _libraries['libpulse.so.0'].pa_context_get_source_info_by_name
pa_context_get_source_info_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_source_info_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_source_info_cb_t, ctypes.POINTER(None)]
pa_context_get_source_info_by_index = _libraries['libpulse.so.0'].pa_context_get_source_info_by_index
pa_context_get_source_info_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_source_info_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_source_info_cb_t, ctypes.POINTER(None)]
pa_context_get_source_info_list = _libraries['libpulse.so.0'].pa_context_get_source_info_list
pa_context_get_source_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_source_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_source_info_cb_t, ctypes.POINTER(None)]
pa_context_set_source_volume_by_index = _libraries['libpulse.so.0'].pa_context_set_source_volume_by_index
pa_context_set_source_volume_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_volume_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_volume_by_name = _libraries['libpulse.so.0'].pa_context_set_source_volume_by_name
pa_context_set_source_volume_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_volume_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_mute_by_index = _libraries['libpulse.so.0'].pa_context_set_source_mute_by_index
pa_context_set_source_mute_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_mute_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_mute_by_name = _libraries['libpulse.so.0'].pa_context_set_source_mute_by_name
pa_context_set_source_mute_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_mute_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_suspend_source_by_name = _libraries['libpulse.so.0'].pa_context_suspend_source_by_name
pa_context_suspend_source_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_suspend_source_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_suspend_source_by_index = _libraries['libpulse.so.0'].pa_context_suspend_source_by_index
pa_context_suspend_source_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_suspend_source_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_port_by_index = _libraries['libpulse.so.0'].pa_context_set_source_port_by_index
pa_context_set_source_port_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_port_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_port_by_name = _libraries['libpulse.so.0'].pa_context_set_source_port_by_name
pa_context_set_source_port_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_port_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_server_info(Structure):
    pass

struct_pa_server_info._pack_ = 1 # source:False
struct_pa_server_info._fields_ = [
    ('user_name', ctypes.POINTER(ctypes.c_char)),
    ('host_name', ctypes.POINTER(ctypes.c_char)),
    ('server_version', ctypes.POINTER(ctypes.c_char)),
    ('server_name', ctypes.POINTER(ctypes.c_char)),
    ('sample_spec', pa_sample_spec),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('default_sink_name', ctypes.POINTER(ctypes.c_char)),
    ('default_source_name', ctypes.POINTER(ctypes.c_char)),
    ('cookie', ctypes.c_uint32),
    ('channel_map', pa_channel_map),
]

pa_server_info = struct_pa_server_info
pa_server_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_server_info), ctypes.POINTER(None))
pa_context_get_server_info = _libraries['libpulse.so.0'].pa_context_get_server_info
pa_context_get_server_info.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_server_info.argtypes = [ctypes.POINTER(struct_pa_context), pa_server_info_cb_t, ctypes.POINTER(None)]
class struct_pa_module_info(Structure):
    pass

struct_pa_module_info._pack_ = 1 # source:False
struct_pa_module_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('argument', ctypes.POINTER(ctypes.c_char)),
    ('n_used', ctypes.c_uint32),
    ('auto_unload', ctypes.c_int32),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
]

pa_module_info = struct_pa_module_info
pa_module_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_module_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_module_info = _libraries['libpulse.so.0'].pa_context_get_module_info
pa_context_get_module_info.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_module_info.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_module_info_cb_t, ctypes.POINTER(None)]
pa_context_get_module_info_list = _libraries['libpulse.so.0'].pa_context_get_module_info_list
pa_context_get_module_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_module_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_module_info_cb_t, ctypes.POINTER(None)]
pa_context_index_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_uint32, ctypes.POINTER(None))
pa_context_load_module = _libraries['libpulse.so.0'].pa_context_load_module
pa_context_load_module.restype = ctypes.POINTER(struct_pa_operation)
pa_context_load_module.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_index_cb_t, ctypes.POINTER(None)]
pa_context_unload_module = _libraries['libpulse.so.0'].pa_context_unload_module
pa_context_unload_module.restype = ctypes.POINTER(struct_pa_operation)
pa_context_unload_module.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_client_info(Structure):
    pass

struct_pa_client_info._pack_ = 1 # source:False
struct_pa_client_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('owner_module', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
]

pa_client_info = struct_pa_client_info
pa_client_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_client_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_client_info = _libraries['libpulse.so.0'].pa_context_get_client_info
pa_context_get_client_info.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_client_info.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_client_info_cb_t, ctypes.POINTER(None)]
pa_context_get_client_info_list = _libraries['libpulse.so.0'].pa_context_get_client_info_list
pa_context_get_client_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_client_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_client_info_cb_t, ctypes.POINTER(None)]
pa_context_kill_client = _libraries['libpulse.so.0'].pa_context_kill_client
pa_context_kill_client.restype = ctypes.POINTER(struct_pa_operation)
pa_context_kill_client.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_card_profile_info(Structure):
    pass

struct_pa_card_profile_info._pack_ = 1 # source:False
struct_pa_card_profile_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('n_sinks', ctypes.c_uint32),
    ('n_sources', ctypes.c_uint32),
    ('priority', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

pa_card_profile_info = struct_pa_card_profile_info
class struct_pa_card_profile_info2(Structure):
    pass

struct_pa_card_profile_info2._pack_ = 1 # source:False
struct_pa_card_profile_info2._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('n_sinks', ctypes.c_uint32),
    ('n_sources', ctypes.c_uint32),
    ('priority', ctypes.c_uint32),
    ('available', ctypes.c_int32),
]

pa_card_profile_info2 = struct_pa_card_profile_info2
class struct_pa_card_port_info(Structure):
    pass

struct_pa_card_port_info._pack_ = 1 # source:False
struct_pa_card_port_info._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('priority', ctypes.c_uint32),
    ('available', ctypes.c_int32),
    ('direction', ctypes.c_int32),
    ('n_profiles', ctypes.c_uint32),
    ('profiles', ctypes.POINTER(ctypes.POINTER(struct_pa_card_profile_info))),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('latency_offset', ctypes.c_int64),
    ('profiles2', ctypes.POINTER(ctypes.POINTER(struct_pa_card_profile_info2))),
]

pa_card_port_info = struct_pa_card_port_info
class struct_pa_card_info(Structure):
    pass

struct_pa_card_info._pack_ = 1 # source:False
struct_pa_card_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('owner_module', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('n_profiles', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('profiles', ctypes.POINTER(struct_pa_card_profile_info)),
    ('active_profile', ctypes.POINTER(struct_pa_card_profile_info)),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('n_ports', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('ports', ctypes.POINTER(ctypes.POINTER(struct_pa_card_port_info))),
    ('profiles2', ctypes.POINTER(ctypes.POINTER(struct_pa_card_profile_info2))),
    ('active_profile2', ctypes.POINTER(struct_pa_card_profile_info2)),
]

pa_card_info = struct_pa_card_info
pa_card_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_card_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_card_info_by_index = _libraries['libpulse.so.0'].pa_context_get_card_info_by_index
pa_context_get_card_info_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_card_info_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_card_info_cb_t, ctypes.POINTER(None)]
pa_context_get_card_info_by_name = _libraries['libpulse.so.0'].pa_context_get_card_info_by_name
pa_context_get_card_info_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_card_info_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_card_info_cb_t, ctypes.POINTER(None)]
pa_context_get_card_info_list = _libraries['libpulse.so.0'].pa_context_get_card_info_list
pa_context_get_card_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_card_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_card_info_cb_t, ctypes.POINTER(None)]
pa_context_set_card_profile_by_index = _libraries['libpulse.so.0'].pa_context_set_card_profile_by_index
pa_context_set_card_profile_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_card_profile_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_card_profile_by_name = _libraries['libpulse.so.0'].pa_context_set_card_profile_by_name
pa_context_set_card_profile_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_card_profile_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
int64_t = ctypes.c_int64
pa_context_set_port_latency_offset = _libraries['libpulse.so.0'].pa_context_set_port_latency_offset
pa_context_set_port_latency_offset.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_port_latency_offset.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_sink_input_info(Structure):
    pass

struct_pa_sink_input_info._pack_ = 1 # source:False
struct_pa_sink_input_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('owner_module', ctypes.c_uint32),
    ('client', ctypes.c_uint32),
    ('sink', ctypes.c_uint32),
    ('sample_spec', pa_sample_spec),
    ('channel_map', pa_channel_map),
    ('volume', pa_cvolume),
    ('buffer_usec', ctypes.c_uint64),
    ('sink_usec', ctypes.c_uint64),
    ('resample_method', ctypes.POINTER(ctypes.c_char)),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('mute', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('corked', ctypes.c_int32),
    ('has_volume', ctypes.c_int32),
    ('volume_writable', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('format', ctypes.POINTER(struct_pa_format_info)),
]

pa_sink_input_info = struct_pa_sink_input_info
pa_sink_input_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_sink_input_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_sink_input_info = _libraries['libpulse.so.0'].pa_context_get_sink_input_info
pa_context_get_sink_input_info.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sink_input_info.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_sink_input_info_cb_t, ctypes.POINTER(None)]
pa_context_get_sink_input_info_list = _libraries['libpulse.so.0'].pa_context_get_sink_input_info_list
pa_context_get_sink_input_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sink_input_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_sink_input_info_cb_t, ctypes.POINTER(None)]
pa_context_move_sink_input_by_name = _libraries['libpulse.so.0'].pa_context_move_sink_input_by_name
pa_context_move_sink_input_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_move_sink_input_by_name.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_move_sink_input_by_index = _libraries['libpulse.so.0'].pa_context_move_sink_input_by_index
pa_context_move_sink_input_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_move_sink_input_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_input_volume = _libraries['libpulse.so.0'].pa_context_set_sink_input_volume
pa_context_set_sink_input_volume.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_input_volume.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_sink_input_mute = _libraries['libpulse.so.0'].pa_context_set_sink_input_mute
pa_context_set_sink_input_mute.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_sink_input_mute.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_kill_sink_input = _libraries['libpulse.so.0'].pa_context_kill_sink_input
pa_context_kill_sink_input.restype = ctypes.POINTER(struct_pa_operation)
pa_context_kill_sink_input.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_source_output_info(Structure):
    pass

struct_pa_source_output_info._pack_ = 1 # source:False
struct_pa_source_output_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('owner_module', ctypes.c_uint32),
    ('client', ctypes.c_uint32),
    ('source', ctypes.c_uint32),
    ('sample_spec', pa_sample_spec),
    ('channel_map', pa_channel_map),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('buffer_usec', ctypes.c_uint64),
    ('source_usec', ctypes.c_uint64),
    ('resample_method', ctypes.POINTER(ctypes.c_char)),
    ('driver', ctypes.POINTER(ctypes.c_char)),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
    ('corked', ctypes.c_int32),
    ('volume', pa_cvolume),
    ('mute', ctypes.c_int32),
    ('has_volume', ctypes.c_int32),
    ('volume_writable', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('format', ctypes.POINTER(struct_pa_format_info)),
]

pa_source_output_info = struct_pa_source_output_info
pa_source_output_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_source_output_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_source_output_info = _libraries['libpulse.so.0'].pa_context_get_source_output_info
pa_context_get_source_output_info.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_source_output_info.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_source_output_info_cb_t, ctypes.POINTER(None)]
pa_context_get_source_output_info_list = _libraries['libpulse.so.0'].pa_context_get_source_output_info_list
pa_context_get_source_output_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_source_output_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_source_output_info_cb_t, ctypes.POINTER(None)]
pa_context_move_source_output_by_name = _libraries['libpulse.so.0'].pa_context_move_source_output_by_name
pa_context_move_source_output_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_move_source_output_by_name.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_move_source_output_by_index = _libraries['libpulse.so.0'].pa_context_move_source_output_by_index
pa_context_move_source_output_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_move_source_output_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_output_volume = _libraries['libpulse.so.0'].pa_context_set_source_output_volume
pa_context_set_source_output_volume.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_output_volume.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.POINTER(struct_pa_cvolume), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_source_output_mute = _libraries['libpulse.so.0'].pa_context_set_source_output_mute
pa_context_set_source_output_mute.restype = ctypes.POINTER(struct_pa_operation)
pa_context_set_source_output_mute.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, ctypes.c_int32, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_kill_source_output = _libraries['libpulse.so.0'].pa_context_kill_source_output
pa_context_kill_source_output.restype = ctypes.POINTER(struct_pa_operation)
pa_context_kill_source_output.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pa_stat_info(Structure):
    pass

struct_pa_stat_info._pack_ = 1 # source:False
struct_pa_stat_info._fields_ = [
    ('memblock_total', ctypes.c_uint32),
    ('memblock_total_size', ctypes.c_uint32),
    ('memblock_allocated', ctypes.c_uint32),
    ('memblock_allocated_size', ctypes.c_uint32),
    ('scache_size', ctypes.c_uint32),
]

pa_stat_info = struct_pa_stat_info
pa_stat_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_stat_info), ctypes.POINTER(None))
pa_context_stat = _libraries['libpulse.so.0'].pa_context_stat
pa_context_stat.restype = ctypes.POINTER(struct_pa_operation)
pa_context_stat.argtypes = [ctypes.POINTER(struct_pa_context), pa_stat_info_cb_t, ctypes.POINTER(None)]
class struct_pa_sample_info(Structure):
    pass

struct_pa_sample_info._pack_ = 1 # source:False
struct_pa_sample_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('volume', pa_cvolume),
    ('sample_spec', pa_sample_spec),
    ('channel_map', pa_channel_map),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('duration', ctypes.c_uint64),
    ('bytes', ctypes.c_uint32),
    ('lazy', ctypes.c_int32),
    ('filename', ctypes.POINTER(ctypes.c_char)),
    ('proplist', ctypes.POINTER(struct_pa_proplist)),
]

pa_sample_info = struct_pa_sample_info
pa_sample_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_sample_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_sample_info_by_name = _libraries['libpulse.so.0'].pa_context_get_sample_info_by_name
pa_context_get_sample_info_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sample_info_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_sample_info_cb_t, ctypes.POINTER(None)]
pa_context_get_sample_info_by_index = _libraries['libpulse.so.0'].pa_context_get_sample_info_by_index
pa_context_get_sample_info_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sample_info_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_sample_info_cb_t, ctypes.POINTER(None)]
pa_context_get_sample_info_list = _libraries['libpulse.so.0'].pa_context_get_sample_info_list
pa_context_get_sample_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_sample_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_sample_info_cb_t, ctypes.POINTER(None)]

# values for enumeration 'pa_autoload_type'
pa_autoload_type__enumvalues = {
    0: 'PA_AUTOLOAD_SINK',
    1: 'PA_AUTOLOAD_SOURCE',
}
PA_AUTOLOAD_SINK = 0
PA_AUTOLOAD_SOURCE = 1
pa_autoload_type = ctypes.c_uint32 # enum
pa_autoload_type_t = pa_autoload_type
pa_autoload_type_t__enumvalues = pa_autoload_type__enumvalues
class struct_pa_autoload_info(Structure):
    pass

struct_pa_autoload_info._pack_ = 1 # source:False
struct_pa_autoload_info._fields_ = [
    ('index', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('type', pa_autoload_type_t),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('module', ctypes.POINTER(ctypes.c_char)),
    ('argument', ctypes.POINTER(ctypes.c_char)),
]

pa_autoload_info = struct_pa_autoload_info
pa_autoload_info_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.POINTER(struct_pa_autoload_info), ctypes.c_int32, ctypes.POINTER(None))
pa_context_get_autoload_info_by_name = _libraries['libpulse.so.0'].pa_context_get_autoload_info_by_name
pa_context_get_autoload_info_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_autoload_info_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_autoload_type_t, pa_autoload_info_cb_t, ctypes.POINTER(None)]
pa_context_get_autoload_info_by_index = _libraries['libpulse.so.0'].pa_context_get_autoload_info_by_index
pa_context_get_autoload_info_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_autoload_info_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_autoload_info_cb_t, ctypes.POINTER(None)]
pa_context_get_autoload_info_list = _libraries['libpulse.so.0'].pa_context_get_autoload_info_list
pa_context_get_autoload_info_list.restype = ctypes.POINTER(struct_pa_operation)
pa_context_get_autoload_info_list.argtypes = [ctypes.POINTER(struct_pa_context), pa_autoload_info_cb_t, ctypes.POINTER(None)]
pa_context_add_autoload = _libraries['libpulse.so.0'].pa_context_add_autoload
pa_context_add_autoload.restype = ctypes.POINTER(struct_pa_operation)
pa_context_add_autoload.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_autoload_type_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_context_index_cb_t, ctypes.POINTER(None)]
pa_context_remove_autoload_by_name = _libraries['libpulse.so.0'].pa_context_remove_autoload_by_name
pa_context_remove_autoload_by_name.restype = ctypes.POINTER(struct_pa_operation)
pa_context_remove_autoload_by_name.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_autoload_type_t, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_remove_autoload_by_index = _libraries['libpulse.so.0'].pa_context_remove_autoload_by_index
pa_context_remove_autoload_by_index.restype = ctypes.POINTER(struct_pa_operation)
pa_context_remove_autoload_by_index.argtypes = [ctypes.POINTER(struct_pa_context), uint32_t, pa_context_success_cb_t, ctypes.POINTER(None)]
class struct_pollfd(Structure):
    pass

class struct_pa_mainloop(Structure):
    pass

pa_mainloop = struct_pa_mainloop
pa_mainloop_new = _libraries['libpulse.so.0'].pa_mainloop_new
pa_mainloop_new.restype = ctypes.POINTER(struct_pa_mainloop)
pa_mainloop_new.argtypes = []
pa_mainloop_free = _libraries['libpulse.so.0'].pa_mainloop_free
pa_mainloop_free.restype = None
pa_mainloop_free.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_mainloop_prepare = _libraries['libpulse.so.0'].pa_mainloop_prepare
pa_mainloop_prepare.restype = ctypes.c_int32
pa_mainloop_prepare.argtypes = [ctypes.POINTER(struct_pa_mainloop), ctypes.c_int32]
pa_mainloop_poll = _libraries['libpulse.so.0'].pa_mainloop_poll
pa_mainloop_poll.restype = ctypes.c_int32
pa_mainloop_poll.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_mainloop_dispatch = _libraries['libpulse.so.0'].pa_mainloop_dispatch
pa_mainloop_dispatch.restype = ctypes.c_int32
pa_mainloop_dispatch.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_mainloop_get_retval = _libraries['libpulse.so.0'].pa_mainloop_get_retval
pa_mainloop_get_retval.restype = ctypes.c_int32
pa_mainloop_get_retval.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_mainloop_iterate = _libraries['libpulse.so.0'].pa_mainloop_iterate
pa_mainloop_iterate.restype = ctypes.c_int32
pa_mainloop_iterate.argtypes = [ctypes.POINTER(struct_pa_mainloop), ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
pa_mainloop_run = _libraries['libpulse.so.0'].pa_mainloop_run
pa_mainloop_run.restype = ctypes.c_int32
pa_mainloop_run.argtypes = [ctypes.POINTER(struct_pa_mainloop), ctypes.POINTER(ctypes.c_int32)]
pa_mainloop_get_api = _libraries['libpulse.so.0'].pa_mainloop_get_api
pa_mainloop_get_api.restype = ctypes.POINTER(struct_pa_mainloop_api)
pa_mainloop_get_api.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_mainloop_quit = _libraries['libpulse.so.0'].pa_mainloop_quit
pa_mainloop_quit.restype = None
pa_mainloop_quit.argtypes = [ctypes.POINTER(struct_pa_mainloop), ctypes.c_int32]
pa_mainloop_wakeup = _libraries['libpulse.so.0'].pa_mainloop_wakeup
pa_mainloop_wakeup.restype = None
pa_mainloop_wakeup.argtypes = [ctypes.POINTER(struct_pa_mainloop)]
pa_poll_func = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_pollfd), ctypes.c_uint64, ctypes.c_int32, ctypes.POINTER(None))
pa_mainloop_set_poll_func = _libraries['libpulse.so.0'].pa_mainloop_set_poll_func
pa_mainloop_set_poll_func.restype = None
pa_mainloop_set_poll_func.argtypes = [ctypes.POINTER(struct_pa_mainloop), pa_poll_func, ctypes.POINTER(None)]
class struct_pa_signal_event(Structure):
    pass

pa_signal_event = struct_pa_signal_event
pa_signal_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_signal_event), ctypes.c_int32, ctypes.POINTER(None))
pa_signal_destroy_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_mainloop_api), ctypes.POINTER(struct_pa_signal_event), ctypes.POINTER(None))
pa_signal_init = _libraries['libpulse.so.0'].pa_signal_init
pa_signal_init.restype = ctypes.c_int32
pa_signal_init.argtypes = [ctypes.POINTER(struct_pa_mainloop_api)]
pa_signal_done = _libraries['libpulse.so.0'].pa_signal_done
pa_signal_done.restype = None
pa_signal_done.argtypes = []
pa_signal_new = _libraries['libpulse.so.0'].pa_signal_new
pa_signal_new.restype = ctypes.POINTER(struct_pa_signal_event)
pa_signal_new.argtypes = [ctypes.c_int32, pa_signal_cb_t, ctypes.POINTER(None)]
pa_signal_free = _libraries['libpulse.so.0'].pa_signal_free
pa_signal_free.restype = None
pa_signal_free.argtypes = [ctypes.POINTER(struct_pa_signal_event)]
pa_signal_set_destroy = _libraries['libpulse.so.0'].pa_signal_set_destroy
pa_signal_set_destroy.restype = None
pa_signal_set_destroy.argtypes = [ctypes.POINTER(struct_pa_signal_event), pa_signal_destroy_cb_t]
class struct_pa_stream(Structure):
    pass

pa_stream = struct_pa_stream
pa_stream_success_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_stream), ctypes.c_int32, ctypes.POINTER(None))
pa_stream_request_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_stream), ctypes.c_uint64, ctypes.POINTER(None))
pa_stream_notify_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_stream), ctypes.POINTER(None))
pa_stream_event_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_proplist), ctypes.POINTER(None))
pa_stream_new = _libraries['libpulse.so.0'].pa_stream_new
pa_stream_new.restype = ctypes.POINTER(struct_pa_stream)
pa_stream_new.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_channel_map)]
pa_stream_new_with_proplist = _libraries['libpulse.so.0'].pa_stream_new_with_proplist
pa_stream_new_with_proplist.restype = ctypes.POINTER(struct_pa_stream)
pa_stream_new_with_proplist.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_proplist)]
pa_stream_new_extended = _libraries['libpulse.so.0'].pa_stream_new_extended
pa_stream_new_extended.restype = ctypes.POINTER(struct_pa_stream)
pa_stream_new_extended.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(struct_pa_format_info)), ctypes.c_uint32, ctypes.POINTER(struct_pa_proplist)]
pa_stream_unref = _libraries['libpulse.so.0'].pa_stream_unref
pa_stream_unref.restype = None
pa_stream_unref.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_ref = _libraries['libpulse.so.0'].pa_stream_ref
pa_stream_ref.restype = ctypes.POINTER(struct_pa_stream)
pa_stream_ref.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_state = _libraries['libpulse.so.0'].pa_stream_get_state
pa_stream_get_state.restype = pa_stream_state_t
pa_stream_get_state.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_context = _libraries['libpulse.so.0'].pa_stream_get_context
pa_stream_get_context.restype = ctypes.POINTER(struct_pa_context)
pa_stream_get_context.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_index = _libraries['libpulse.so.0'].pa_stream_get_index
pa_stream_get_index.restype = uint32_t
pa_stream_get_index.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_device_index = _libraries['libpulse.so.0'].pa_stream_get_device_index
pa_stream_get_device_index.restype = uint32_t
pa_stream_get_device_index.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_device_name = _libraries['libpulse.so.0'].pa_stream_get_device_name
pa_stream_get_device_name.restype = ctypes.POINTER(ctypes.c_char)
pa_stream_get_device_name.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_is_suspended = _libraries['libpulse.so.0'].pa_stream_is_suspended
pa_stream_is_suspended.restype = ctypes.c_int32
pa_stream_is_suspended.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_is_corked = _libraries['libpulse.so.0'].pa_stream_is_corked
pa_stream_is_corked.restype = ctypes.c_int32
pa_stream_is_corked.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_connect_playback = _libraries['libpulse.so.0'].pa_stream_connect_playback
pa_stream_connect_playback.restype = ctypes.c_int32
pa_stream_connect_playback.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_buffer_attr), pa_stream_flags_t, ctypes.POINTER(struct_pa_cvolume), ctypes.POINTER(struct_pa_stream)]
pa_stream_connect_record = _libraries['libpulse.so.0'].pa_stream_connect_record
pa_stream_connect_record.restype = ctypes.c_int32
pa_stream_connect_record.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_buffer_attr), pa_stream_flags_t]
pa_stream_disconnect = _libraries['libpulse.so.0'].pa_stream_disconnect
pa_stream_disconnect.restype = ctypes.c_int32
pa_stream_disconnect.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_begin_write = _libraries['libpulse.so.0'].pa_stream_begin_write
pa_stream_begin_write.restype = ctypes.c_int32
pa_stream_begin_write.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_uint64)]
pa_stream_cancel_write = _libraries['libpulse.so.0'].pa_stream_cancel_write
pa_stream_cancel_write.restype = ctypes.c_int32
pa_stream_cancel_write.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_write = _libraries['libpulse.so.0'].pa_stream_write
pa_stream_write.restype = ctypes.c_int32
pa_stream_write.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(None), size_t, pa_free_cb_t, int64_t, pa_seek_mode_t]
pa_stream_write_ext_free = _libraries['libpulse.so.0'].pa_stream_write_ext_free
pa_stream_write_ext_free.restype = ctypes.c_int32
pa_stream_write_ext_free.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(None), size_t, pa_free_cb_t, ctypes.POINTER(None), int64_t, pa_seek_mode_t]
pa_stream_peek = _libraries['libpulse.so.0'].pa_stream_peek
pa_stream_peek.restype = ctypes.c_int32
pa_stream_peek.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_uint64)]
pa_stream_drop = _libraries['libpulse.so.0'].pa_stream_drop
pa_stream_drop.restype = ctypes.c_int32
pa_stream_drop.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_writable_size = _libraries['libpulse.so.0'].pa_stream_writable_size
pa_stream_writable_size.restype = size_t
pa_stream_writable_size.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_readable_size = _libraries['libpulse.so.0'].pa_stream_readable_size
pa_stream_readable_size.restype = size_t
pa_stream_readable_size.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_drain = _libraries['libpulse.so.0'].pa_stream_drain
pa_stream_drain.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_drain.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_update_timing_info = _libraries['libpulse.so.0'].pa_stream_update_timing_info
pa_stream_update_timing_info.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_update_timing_info.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_set_state_callback = _libraries['libpulse.so.0'].pa_stream_set_state_callback
pa_stream_set_state_callback.restype = None
pa_stream_set_state_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_write_callback = _libraries['libpulse.so.0'].pa_stream_set_write_callback
pa_stream_set_write_callback.restype = None
pa_stream_set_write_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_request_cb_t, ctypes.POINTER(None)]
pa_stream_set_read_callback = _libraries['libpulse.so.0'].pa_stream_set_read_callback
pa_stream_set_read_callback.restype = None
pa_stream_set_read_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_request_cb_t, ctypes.POINTER(None)]
pa_stream_set_overflow_callback = _libraries['libpulse.so.0'].pa_stream_set_overflow_callback
pa_stream_set_overflow_callback.restype = None
pa_stream_set_overflow_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_get_underflow_index = _libraries['libpulse.so.0'].pa_stream_get_underflow_index
pa_stream_get_underflow_index.restype = int64_t
pa_stream_get_underflow_index.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_set_underflow_callback = _libraries['libpulse.so.0'].pa_stream_set_underflow_callback
pa_stream_set_underflow_callback.restype = None
pa_stream_set_underflow_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_started_callback = _libraries['libpulse.so.0'].pa_stream_set_started_callback
pa_stream_set_started_callback.restype = None
pa_stream_set_started_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_latency_update_callback = _libraries['libpulse.so.0'].pa_stream_set_latency_update_callback
pa_stream_set_latency_update_callback.restype = None
pa_stream_set_latency_update_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_moved_callback = _libraries['libpulse.so.0'].pa_stream_set_moved_callback
pa_stream_set_moved_callback.restype = None
pa_stream_set_moved_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_suspended_callback = _libraries['libpulse.so.0'].pa_stream_set_suspended_callback
pa_stream_set_suspended_callback.restype = None
pa_stream_set_suspended_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_set_event_callback = _libraries['libpulse.so.0'].pa_stream_set_event_callback
pa_stream_set_event_callback.restype = None
pa_stream_set_event_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_event_cb_t, ctypes.POINTER(None)]
pa_stream_set_buffer_attr_callback = _libraries['libpulse.so.0'].pa_stream_set_buffer_attr_callback
pa_stream_set_buffer_attr_callback.restype = None
pa_stream_set_buffer_attr_callback.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_notify_cb_t, ctypes.POINTER(None)]
pa_stream_cork = _libraries['libpulse.so.0'].pa_stream_cork
pa_stream_cork.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_cork.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.c_int32, pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_flush = _libraries['libpulse.so.0'].pa_stream_flush
pa_stream_flush.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_flush.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_prebuf = _libraries['libpulse.so.0'].pa_stream_prebuf
pa_stream_prebuf.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_prebuf.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_trigger = _libraries['libpulse.so.0'].pa_stream_trigger
pa_stream_trigger.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_trigger.argtypes = [ctypes.POINTER(struct_pa_stream), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_set_name = _libraries['libpulse.so.0'].pa_stream_set_name
pa_stream_set_name.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_set_name.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_char), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_get_time = _libraries['libpulse.so.0'].pa_stream_get_time
pa_stream_get_time.restype = ctypes.c_int32
pa_stream_get_time.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_uint64)]
pa_stream_get_latency = _libraries['libpulse.so.0'].pa_stream_get_latency
pa_stream_get_latency.restype = ctypes.c_int32
pa_stream_get_latency.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_int32)]
pa_stream_get_timing_info = _libraries['libpulse.so.0'].pa_stream_get_timing_info
pa_stream_get_timing_info.restype = ctypes.POINTER(struct_pa_timing_info)
pa_stream_get_timing_info.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_sample_spec = _libraries['libpulse.so.0'].pa_stream_get_sample_spec
pa_stream_get_sample_spec.restype = ctypes.POINTER(struct_pa_sample_spec)
pa_stream_get_sample_spec.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_channel_map = _libraries['libpulse.so.0'].pa_stream_get_channel_map
pa_stream_get_channel_map.restype = ctypes.POINTER(struct_pa_channel_map)
pa_stream_get_channel_map.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_format_info = _libraries['libpulse.so.0'].pa_stream_get_format_info
pa_stream_get_format_info.restype = ctypes.POINTER(struct_pa_format_info)
pa_stream_get_format_info.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_get_buffer_attr = _libraries['libpulse.so.0'].pa_stream_get_buffer_attr
pa_stream_get_buffer_attr.restype = ctypes.POINTER(struct_pa_buffer_attr)
pa_stream_get_buffer_attr.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_stream_set_buffer_attr = _libraries['libpulse.so.0'].pa_stream_set_buffer_attr
pa_stream_set_buffer_attr.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_set_buffer_attr.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(struct_pa_buffer_attr), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_update_sample_rate = _libraries['libpulse.so.0'].pa_stream_update_sample_rate
pa_stream_update_sample_rate.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_update_sample_rate.argtypes = [ctypes.POINTER(struct_pa_stream), uint32_t, pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_proplist_update = _libraries['libpulse.so.0'].pa_stream_proplist_update
pa_stream_proplist_update.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_proplist_update.argtypes = [ctypes.POINTER(struct_pa_stream), pa_update_mode_t, ctypes.POINTER(struct_pa_proplist), pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_proplist_remove = _libraries['libpulse.so.0'].pa_stream_proplist_remove
pa_stream_proplist_remove.restype = ctypes.POINTER(struct_pa_operation)
pa_stream_proplist_remove.argtypes = [ctypes.POINTER(struct_pa_stream), ctypes.POINTER(ctypes.c_char) * 0, pa_stream_success_cb_t, ctypes.POINTER(None)]
pa_stream_set_monitor_stream = _libraries['libpulse.so.0'].pa_stream_set_monitor_stream
pa_stream_set_monitor_stream.restype = ctypes.c_int32
pa_stream_set_monitor_stream.argtypes = [ctypes.POINTER(struct_pa_stream), uint32_t]
pa_stream_get_monitor_stream = _libraries['libpulse.so.0'].pa_stream_get_monitor_stream
pa_stream_get_monitor_stream.restype = uint32_t
pa_stream_get_monitor_stream.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_context_subscribe_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), pa_subscription_event_type, ctypes.c_uint32, ctypes.POINTER(None))
pa_context_subscribe = _libraries['libpulse.so.0'].pa_context_subscribe
pa_context_subscribe.restype = ctypes.POINTER(struct_pa_operation)
pa_context_subscribe.argtypes = [ctypes.POINTER(struct_pa_context), pa_subscription_mask_t, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_set_subscribe_callback = _libraries['libpulse.so.0'].pa_context_set_subscribe_callback
pa_context_set_subscribe_callback.restype = None
pa_context_set_subscribe_callback.argtypes = [ctypes.POINTER(struct_pa_context), pa_context_subscribe_cb_t, ctypes.POINTER(None)]
pa_context_play_sample_cb_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_context), ctypes.c_uint32, ctypes.POINTER(None))
pa_stream_connect_upload = _libraries['libpulse.so.0'].pa_stream_connect_upload
pa_stream_connect_upload.restype = ctypes.c_int32
pa_stream_connect_upload.argtypes = [ctypes.POINTER(struct_pa_stream), size_t]
pa_stream_finish_upload = _libraries['libpulse.so.0'].pa_stream_finish_upload
pa_stream_finish_upload.restype = ctypes.c_int32
pa_stream_finish_upload.argtypes = [ctypes.POINTER(struct_pa_stream)]
pa_context_remove_sample = _libraries['libpulse.so.0'].pa_context_remove_sample
pa_context_remove_sample.restype = ctypes.POINTER(struct_pa_operation)
pa_context_remove_sample.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_play_sample = _libraries['libpulse.so.0'].pa_context_play_sample
pa_context_play_sample.restype = ctypes.POINTER(struct_pa_operation)
pa_context_play_sample.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_volume_t, pa_context_success_cb_t, ctypes.POINTER(None)]
pa_context_play_sample_with_proplist = _libraries['libpulse.so.0'].pa_context_play_sample_with_proplist
pa_context_play_sample_with_proplist.restype = ctypes.POINTER(struct_pa_operation)
pa_context_play_sample_with_proplist.argtypes = [ctypes.POINTER(struct_pa_context), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_volume_t, ctypes.POINTER(struct_pa_proplist), pa_context_play_sample_cb_t, ctypes.POINTER(None)]
pa_xmalloc = _libraries['libpulse.so.0'].pa_xmalloc
pa_xmalloc.restype = ctypes.POINTER(None)
pa_xmalloc.argtypes = [size_t]
pa_xmalloc0 = _libraries['libpulse.so.0'].pa_xmalloc0
pa_xmalloc0.restype = ctypes.POINTER(None)
pa_xmalloc0.argtypes = [size_t]
pa_xrealloc = _libraries['libpulse.so.0'].pa_xrealloc
pa_xrealloc.restype = ctypes.POINTER(None)
pa_xrealloc.argtypes = [ctypes.POINTER(None), size_t]
pa_xfree = _libraries['libpulse.so.0'].pa_xfree
pa_xfree.restype = None
pa_xfree.argtypes = [ctypes.POINTER(None)]
pa_xstrdup = _libraries['libpulse.so.0'].pa_xstrdup
pa_xstrdup.restype = ctypes.POINTER(ctypes.c_char)
pa_xstrdup.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_xstrndup = _libraries['libpulse.so.0'].pa_xstrndup
pa_xstrndup.restype = ctypes.POINTER(ctypes.c_char)
pa_xstrndup.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_xmemdup = _libraries['libpulse.so.0'].pa_xmemdup
pa_xmemdup.restype = ctypes.POINTER(None)
pa_xmemdup.argtypes = [ctypes.POINTER(None), size_t]
pa_utf8_valid = _libraries['libpulse.so.0'].pa_utf8_valid
pa_utf8_valid.restype = ctypes.POINTER(ctypes.c_char)
pa_utf8_valid.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_ascii_valid = _libraries['libpulse.so.0'].pa_ascii_valid
pa_ascii_valid.restype = ctypes.POINTER(ctypes.c_char)
pa_ascii_valid.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_utf8_filter = _libraries['libpulse.so.0'].pa_utf8_filter
pa_utf8_filter.restype = ctypes.POINTER(ctypes.c_char)
pa_utf8_filter.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_ascii_filter = _libraries['libpulse.so.0'].pa_ascii_filter
pa_ascii_filter.restype = ctypes.POINTER(ctypes.c_char)
pa_ascii_filter.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_utf8_to_locale = _libraries['libpulse.so.0'].pa_utf8_to_locale
pa_utf8_to_locale.restype = ctypes.POINTER(ctypes.c_char)
pa_utf8_to_locale.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_locale_to_utf8 = _libraries['libpulse.so.0'].pa_locale_to_utf8
pa_locale_to_utf8.restype = ctypes.POINTER(ctypes.c_char)
pa_locale_to_utf8.argtypes = [ctypes.POINTER(ctypes.c_char)]
class struct_pa_threaded_mainloop(Structure):
    pass

pa_threaded_mainloop = struct_pa_threaded_mainloop
pa_threaded_mainloop_new = _libraries['libpulse.so.0'].pa_threaded_mainloop_new
pa_threaded_mainloop_new.restype = ctypes.POINTER(struct_pa_threaded_mainloop)
pa_threaded_mainloop_new.argtypes = []
pa_threaded_mainloop_free = _libraries['libpulse.so.0'].pa_threaded_mainloop_free
pa_threaded_mainloop_free.restype = None
pa_threaded_mainloop_free.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_start = _libraries['libpulse.so.0'].pa_threaded_mainloop_start
pa_threaded_mainloop_start.restype = ctypes.c_int32
pa_threaded_mainloop_start.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_stop = _libraries['libpulse.so.0'].pa_threaded_mainloop_stop
pa_threaded_mainloop_stop.restype = None
pa_threaded_mainloop_stop.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_lock = _libraries['libpulse.so.0'].pa_threaded_mainloop_lock
pa_threaded_mainloop_lock.restype = None
pa_threaded_mainloop_lock.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_unlock = _libraries['libpulse.so.0'].pa_threaded_mainloop_unlock
pa_threaded_mainloop_unlock.restype = None
pa_threaded_mainloop_unlock.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_wait = _libraries['libpulse.so.0'].pa_threaded_mainloop_wait
pa_threaded_mainloop_wait.restype = None
pa_threaded_mainloop_wait.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_signal = _libraries['libpulse.so.0'].pa_threaded_mainloop_signal
pa_threaded_mainloop_signal.restype = None
pa_threaded_mainloop_signal.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop), ctypes.c_int32]
pa_threaded_mainloop_accept = _libraries['libpulse.so.0'].pa_threaded_mainloop_accept
pa_threaded_mainloop_accept.restype = None
pa_threaded_mainloop_accept.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_get_retval = _libraries['libpulse.so.0'].pa_threaded_mainloop_get_retval
pa_threaded_mainloop_get_retval.restype = ctypes.c_int32
pa_threaded_mainloop_get_retval.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_get_api = _libraries['libpulse.so.0'].pa_threaded_mainloop_get_api
pa_threaded_mainloop_get_api.restype = ctypes.POINTER(struct_pa_mainloop_api)
pa_threaded_mainloop_get_api.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_in_thread = _libraries['libpulse.so.0'].pa_threaded_mainloop_in_thread
pa_threaded_mainloop_in_thread.restype = ctypes.c_int32
pa_threaded_mainloop_in_thread.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop)]
pa_threaded_mainloop_set_name = _libraries['libpulse.so.0'].pa_threaded_mainloop_set_name
pa_threaded_mainloop_set_name.restype = None
pa_threaded_mainloop_set_name.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop), ctypes.POINTER(ctypes.c_char)]
pa_threaded_mainloop_once_unlocked = _libraries['libpulse.so.0'].pa_threaded_mainloop_once_unlocked
pa_threaded_mainloop_once_unlocked.restype = None
pa_threaded_mainloop_once_unlocked.argtypes = [ctypes.POINTER(struct_pa_threaded_mainloop), ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_pa_threaded_mainloop), ctypes.POINTER(None)), ctypes.POINTER(None)]
pa_get_user_name = _libraries['libpulse.so.0'].pa_get_user_name
pa_get_user_name.restype = ctypes.POINTER(ctypes.c_char)
pa_get_user_name.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_get_host_name = _libraries['libpulse.so.0'].pa_get_host_name
pa_get_host_name.restype = ctypes.POINTER(ctypes.c_char)
pa_get_host_name.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_get_fqdn = _libraries['libpulse.so.0'].pa_get_fqdn
pa_get_fqdn.restype = ctypes.POINTER(ctypes.c_char)
pa_get_fqdn.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_get_home_dir = _libraries['libpulse.so.0'].pa_get_home_dir
pa_get_home_dir.restype = ctypes.POINTER(ctypes.c_char)
pa_get_home_dir.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_get_binary_name = _libraries['libpulse.so.0'].pa_get_binary_name
pa_get_binary_name.restype = ctypes.POINTER(ctypes.c_char)
pa_get_binary_name.argtypes = [ctypes.POINTER(ctypes.c_char), size_t]
pa_path_get_filename = _libraries['libpulse.so.0'].pa_path_get_filename
pa_path_get_filename.restype = ctypes.POINTER(ctypes.c_char)
pa_path_get_filename.argtypes = [ctypes.POINTER(ctypes.c_char)]
pa_msleep = _libraries['libpulse.so.0'].pa_msleep
pa_msleep.restype = ctypes.c_int32
pa_msleep.argtypes = [ctypes.c_uint64]
pa_thread_make_realtime = _libraries['libpulse.so.0'].pa_thread_make_realtime
pa_thread_make_realtime.restype = ctypes.c_int32
pa_thread_make_realtime.argtypes = [ctypes.c_int32]
pa_gettimeofday = _libraries['libpulse.so.0'].pa_gettimeofday
pa_gettimeofday.restype = ctypes.POINTER(struct_timeval)
pa_gettimeofday.argtypes = [ctypes.POINTER(struct_timeval)]
pa_timeval_diff = _libraries['libpulse.so.0'].pa_timeval_diff
pa_timeval_diff.restype = pa_usec_t
pa_timeval_diff.argtypes = [ctypes.POINTER(struct_timeval), ctypes.POINTER(struct_timeval)]
pa_timeval_cmp = _libraries['libpulse.so.0'].pa_timeval_cmp
pa_timeval_cmp.restype = ctypes.c_int32
pa_timeval_cmp.argtypes = [ctypes.POINTER(struct_timeval), ctypes.POINTER(struct_timeval)]
pa_timeval_age = _libraries['libpulse.so.0'].pa_timeval_age
pa_timeval_age.restype = pa_usec_t
pa_timeval_age.argtypes = [ctypes.POINTER(struct_timeval)]
pa_timeval_add = _libraries['libpulse.so.0'].pa_timeval_add
pa_timeval_add.restype = ctypes.POINTER(struct_timeval)
pa_timeval_add.argtypes = [ctypes.POINTER(struct_timeval), pa_usec_t]
pa_timeval_sub = _libraries['libpulse.so.0'].pa_timeval_sub
pa_timeval_sub.restype = ctypes.POINTER(struct_timeval)
pa_timeval_sub.argtypes = [ctypes.POINTER(struct_timeval), pa_usec_t]
pa_timeval_store = _libraries['libpulse.so.0'].pa_timeval_store
pa_timeval_store.restype = ctypes.POINTER(struct_timeval)
pa_timeval_store.argtypes = [ctypes.POINTER(struct_timeval), pa_usec_t]
pa_timeval_load = _libraries['libpulse.so.0'].pa_timeval_load
pa_timeval_load.restype = pa_usec_t
pa_timeval_load.argtypes = [ctypes.POINTER(struct_timeval)]
pa_rtclock_now = _libraries['libpulse.so.0'].pa_rtclock_now
pa_rtclock_now.restype = pa_usec_t
pa_rtclock_now.argtypes = []
class struct_pa_simple(Structure):
    pass

pa_simple = struct_pa_simple
pa_simple_new = _libraries['libpulse-simple.so.0'].pa_simple_new
pa_simple_new.restype = ctypes.POINTER(struct_pa_simple)
pa_simple_new.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), pa_stream_direction_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_pa_sample_spec), ctypes.POINTER(struct_pa_channel_map), ctypes.POINTER(struct_pa_buffer_attr), ctypes.POINTER(ctypes.c_int32)]
pa_simple_free = _libraries['libpulse-simple.so.0'].pa_simple_free
pa_simple_free.restype = None
pa_simple_free.argtypes = [ctypes.POINTER(struct_pa_simple)]
pa_simple_write = _libraries['libpulse-simple.so.0'].pa_simple_write
pa_simple_write.restype = ctypes.c_int32
pa_simple_write.argtypes = [ctypes.POINTER(struct_pa_simple), ctypes.POINTER(None), size_t, ctypes.POINTER(ctypes.c_int32)]
pa_simple_drain = _libraries['libpulse-simple.so.0'].pa_simple_drain
pa_simple_drain.restype = ctypes.c_int32
pa_simple_drain.argtypes = [ctypes.POINTER(struct_pa_simple), ctypes.POINTER(ctypes.c_int32)]
pa_simple_read = _libraries['libpulse-simple.so.0'].pa_simple_read
pa_simple_read.restype = ctypes.c_int32
pa_simple_read.argtypes = [ctypes.POINTER(struct_pa_simple), ctypes.POINTER(None), size_t, ctypes.POINTER(ctypes.c_int32)]
pa_simple_get_latency = _libraries['libpulse-simple.so.0'].pa_simple_get_latency
pa_simple_get_latency.restype = pa_usec_t
pa_simple_get_latency.argtypes = [ctypes.POINTER(struct_pa_simple), ctypes.POINTER(ctypes.c_int32)]
pa_simple_flush = _libraries['libpulse-simple.so.0'].pa_simple_flush
pa_simple_flush.restype = ctypes.c_int32
pa_simple_flush.argtypes = [ctypes.POINTER(struct_pa_simple), ctypes.POINTER(ctypes.c_int32)]
__all__ = \
    ['PA_AUTOLOAD_SINK', 'PA_AUTOLOAD_SOURCE', 'PA_CHANNEL_MAP_AIFF',
    'PA_CHANNEL_MAP_ALSA', 'PA_CHANNEL_MAP_AUX',
    'PA_CHANNEL_MAP_DEFAULT', 'PA_CHANNEL_MAP_DEF_MAX',
    'PA_CHANNEL_MAP_OSS', 'PA_CHANNEL_MAP_WAVEEX',
    'PA_CHANNEL_POSITION_AUX0', 'PA_CHANNEL_POSITION_AUX1',
    'PA_CHANNEL_POSITION_AUX10', 'PA_CHANNEL_POSITION_AUX11',
    'PA_CHANNEL_POSITION_AUX12', 'PA_CHANNEL_POSITION_AUX13',
    'PA_CHANNEL_POSITION_AUX14', 'PA_CHANNEL_POSITION_AUX15',
    'PA_CHANNEL_POSITION_AUX16', 'PA_CHANNEL_POSITION_AUX17',
    'PA_CHANNEL_POSITION_AUX18', 'PA_CHANNEL_POSITION_AUX19',
    'PA_CHANNEL_POSITION_AUX2', 'PA_CHANNEL_POSITION_AUX20',
    'PA_CHANNEL_POSITION_AUX21', 'PA_CHANNEL_POSITION_AUX22',
    'PA_CHANNEL_POSITION_AUX23', 'PA_CHANNEL_POSITION_AUX24',
    'PA_CHANNEL_POSITION_AUX25', 'PA_CHANNEL_POSITION_AUX26',
    'PA_CHANNEL_POSITION_AUX27', 'PA_CHANNEL_POSITION_AUX28',
    'PA_CHANNEL_POSITION_AUX29', 'PA_CHANNEL_POSITION_AUX3',
    'PA_CHANNEL_POSITION_AUX30', 'PA_CHANNEL_POSITION_AUX31',
    'PA_CHANNEL_POSITION_AUX4', 'PA_CHANNEL_POSITION_AUX5',
    'PA_CHANNEL_POSITION_AUX6', 'PA_CHANNEL_POSITION_AUX7',
    'PA_CHANNEL_POSITION_AUX8', 'PA_CHANNEL_POSITION_AUX9',
    'PA_CHANNEL_POSITION_CENTER', 'PA_CHANNEL_POSITION_FRONT_CENTER',
    'PA_CHANNEL_POSITION_FRONT_LEFT',
    'PA_CHANNEL_POSITION_FRONT_LEFT_OF_CENTER',
    'PA_CHANNEL_POSITION_FRONT_RIGHT',
    'PA_CHANNEL_POSITION_FRONT_RIGHT_OF_CENTER',
    'PA_CHANNEL_POSITION_INVALID', 'PA_CHANNEL_POSITION_LEFT',
    'PA_CHANNEL_POSITION_LFE', 'PA_CHANNEL_POSITION_MAX',
    'PA_CHANNEL_POSITION_MONO', 'PA_CHANNEL_POSITION_REAR_CENTER',
    'PA_CHANNEL_POSITION_REAR_LEFT', 'PA_CHANNEL_POSITION_REAR_RIGHT',
    'PA_CHANNEL_POSITION_RIGHT', 'PA_CHANNEL_POSITION_SIDE_LEFT',
    'PA_CHANNEL_POSITION_SIDE_RIGHT', 'PA_CHANNEL_POSITION_SUBWOOFER',
    'PA_CHANNEL_POSITION_TOP_CENTER',
    'PA_CHANNEL_POSITION_TOP_FRONT_CENTER',
    'PA_CHANNEL_POSITION_TOP_FRONT_LEFT',
    'PA_CHANNEL_POSITION_TOP_FRONT_RIGHT',
    'PA_CHANNEL_POSITION_TOP_REAR_CENTER',
    'PA_CHANNEL_POSITION_TOP_REAR_LEFT',
    'PA_CHANNEL_POSITION_TOP_REAR_RIGHT', 'PA_CONTEXT_AUTHORIZING',
    'PA_CONTEXT_CONNECTING', 'PA_CONTEXT_FAILED',
    'PA_CONTEXT_NOAUTOSPAWN',
    'PA_CONTEXT_NOFAIL', 'PA_CONTEXT_NOFLAGS', 'PA_CONTEXT_READY',
    'PA_CONTEXT_SETTING_NAME', 'PA_CONTEXT_TERMINATED',
    'PA_CONTEXT_UNCONNECTED', 'PA_DEVICE_TYPE_SINK',
    'PA_DEVICE_TYPE_SOURCE', 'PA_DIRECTION_INPUT',
    'PA_DIRECTION_OUTPUT', 'PA_ENCODING_AC3_IEC61937',
    'PA_ENCODING_ANY', 'PA_ENCODING_DTSHD_IEC61937',
    'PA_ENCODING_DTS_IEC61937', 'PA_ENCODING_EAC3_IEC61937',
    'PA_ENCODING_INVALID', 'PA_ENCODING_MAX',
    'PA_ENCODING_MPEG2_AAC_IEC61937', 'PA_ENCODING_MPEG_IEC61937',
    'PA_ENCODING_PCM', 'PA_ENCODING_TRUEHD_IEC61937', 'PA_ERR_ACCESS',
    'PA_ERR_AUTHKEY', 'PA_ERR_BADSTATE', 'PA_ERR_BUSY',
    'PA_ERR_COMMAND', 'PA_ERR_CONNECTIONREFUSED',
    'PA_ERR_CONNECTIONTERMINATED', 'PA_ERR_EXIST', 'PA_ERR_FORKED',
    'PA_ERR_INTERNAL', 'PA_ERR_INVALID', 'PA_ERR_INVALIDSERVER',
    'PA_ERR_IO', 'PA_ERR_KILLED', 'PA_ERR_MAX',
    'PA_ERR_MODINITFAILED', 'PA_ERR_NODATA', 'PA_ERR_NOENTITY',
    'PA_ERR_NOEXTENSION', 'PA_ERR_NOTIMPLEMENTED',
    'PA_ERR_NOTSUPPORTED', 'PA_ERR_OBSOLETE', 'PA_ERR_PROTOCOL',
    'PA_ERR_TIMEOUT', 'PA_ERR_TOOLARGE', 'PA_ERR_UNKNOWN',
    'PA_ERR_VERSION', 'PA_IO_EVENT_ERROR', 'PA_IO_EVENT_HANGUP',
    'PA_IO_EVENT_INPUT', 'PA_IO_EVENT_NULL', 'PA_IO_EVENT_OUTPUT',
    'PA_OK', 'PA_OPERATION_CANCELLED', 'PA_OPERATION_DONE',
    'PA_OPERATION_RUNNING', 'PA_PORT_AVAILABLE_NO',
    'PA_PORT_AVAILABLE_UNKNOWN', 'PA_PORT_AVAILABLE_YES',
    'PA_PROP_TYPE_INT', 'PA_PROP_TYPE_INT_ARRAY',
    'PA_PROP_TYPE_INT_RANGE', 'PA_PROP_TYPE_INVALID',
    'PA_PROP_TYPE_STRING', 'PA_PROP_TYPE_STRING_ARRAY',
    'PA_SAMPLE_ALAW', 'PA_SAMPLE_FLOAT32BE', 'PA_SAMPLE_FLOAT32LE',
    'PA_SAMPLE_INVALID', 'PA_SAMPLE_MAX', 'PA_SAMPLE_S16BE',
    'PA_SAMPLE_S16LE', 'PA_SAMPLE_S24BE', 'PA_SAMPLE_S24LE',
    'PA_SAMPLE_S24_32BE', 'PA_SAMPLE_S24_32LE', 'PA_SAMPLE_S32BE',
    'PA_SAMPLE_S32LE', 'PA_SAMPLE_U8', 'PA_SAMPLE_ULAW',
    'PA_SEEK_ABSOLUTE', 'PA_SEEK_RELATIVE', 'PA_SEEK_RELATIVE_END',
    'PA_SEEK_RELATIVE_ON_READ', 'PA_SINK_DECIBEL_VOLUME',
    'PA_SINK_DYNAMIC_LATENCY', 'PA_SINK_FLAT_VOLUME',
    'PA_SINK_HARDWARE', 'PA_SINK_HW_MUTE_CTRL',
    'PA_SINK_HW_VOLUME_CTRL', 'PA_SINK_IDLE', 'PA_SINK_INIT',
    'PA_SINK_INVALID_STATE', 'PA_SINK_LATENCY', 'PA_SINK_NETWORK',
    'PA_SINK_NOFLAGS', 'PA_SINK_RUNNING', 'PA_SINK_SET_FORMATS',
    'PA_SINK_SUSPENDED', 'PA_SINK_UNLINKED',
    'PA_SOURCE_DECIBEL_VOLUME', 'PA_SOURCE_DYNAMIC_LATENCY',
    'PA_SOURCE_FLAT_VOLUME', 'PA_SOURCE_HARDWARE',
    'PA_SOURCE_HW_MUTE_CTRL', 'PA_SOURCE_HW_VOLUME_CTRL',
    'PA_SOURCE_IDLE', 'PA_SOURCE_INIT', 'PA_SOURCE_INVALID_STATE',
    'PA_SOURCE_LATENCY', 'PA_SOURCE_NETWORK', 'PA_SOURCE_NOFLAGS',
    'PA_SOURCE_RUNNING', 'PA_SOURCE_SUSPENDED', 'PA_SOURCE_UNLINKED',
    'PA_STREAM_ADJUST_LATENCY', 'PA_STREAM_AUTO_TIMING_UPDATE',
    'PA_STREAM_CREATING', 'PA_STREAM_DONT_INHIBIT_AUTO_SUSPEND',
    'PA_STREAM_DONT_MOVE', 'PA_STREAM_EARLY_REQUESTS',
    'PA_STREAM_FAILED', 'PA_STREAM_FAIL_ON_SUSPEND',
    'PA_STREAM_FIX_CHANNELS', 'PA_STREAM_FIX_FORMAT',
    'PA_STREAM_FIX_RATE', 'PA_STREAM_INTERPOLATE_TIMING',
    'PA_STREAM_NODIRECTION', 'PA_STREAM_NOFLAGS',
    'PA_STREAM_NOT_MONOTONIC', 'PA_STREAM_NO_REMAP_CHANNELS',
    'PA_STREAM_NO_REMIX_CHANNELS', 'PA_STREAM_PASSTHROUGH',
    'PA_STREAM_PEAK_DETECT', 'PA_STREAM_PLAYBACK', 'PA_STREAM_READY',
    'PA_STREAM_RECORD', 'PA_STREAM_RELATIVE_VOLUME',
    'PA_STREAM_START_CORKED', 'PA_STREAM_START_MUTED',
    'PA_STREAM_START_UNMUTED', 'PA_STREAM_TERMINATED',
    'PA_STREAM_UNCONNECTED', 'PA_STREAM_UPLOAD',
    'PA_STREAM_VARIABLE_RATE', 'PA_SUBSCRIPTION_EVENT_AUTOLOAD',
    'PA_SUBSCRIPTION_EVENT_CARD', 'PA_SUBSCRIPTION_EVENT_CHANGE',
    'PA_SUBSCRIPTION_EVENT_CLIENT',
    'PA_SUBSCRIPTION_EVENT_FACILITY_MASK',
    'PA_SUBSCRIPTION_EVENT_MODULE', 'PA_SUBSCRIPTION_EVENT_NEW',
    'PA_SUBSCRIPTION_EVENT_REMOVE',
    'PA_SUBSCRIPTION_EVENT_SAMPLE_CACHE',
    'PA_SUBSCRIPTION_EVENT_SERVER', 'PA_SUBSCRIPTION_EVENT_SINK',
    'PA_SUBSCRIPTION_EVENT_SINK_INPUT',
    'PA_SUBSCRIPTION_EVENT_SOURCE',
    'PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT',
    'PA_SUBSCRIPTION_EVENT_TYPE_MASK', 'PA_SUBSCRIPTION_MASK_ALL',
    'PA_SUBSCRIPTION_MASK_AUTOLOAD', 'PA_SUBSCRIPTION_MASK_CARD',
    'PA_SUBSCRIPTION_MASK_CLIENT', 'PA_SUBSCRIPTION_MASK_MODULE',
    'PA_SUBSCRIPTION_MASK_NULL', 'PA_SUBSCRIPTION_MASK_SAMPLE_CACHE',
    'PA_SUBSCRIPTION_MASK_SERVER', 'PA_SUBSCRIPTION_MASK_SINK',
    'PA_SUBSCRIPTION_MASK_SINK_INPUT', 'PA_SUBSCRIPTION_MASK_SOURCE',
    'PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT', 'PA_UPDATE_MERGE',
    'PA_UPDATE_REPLACE', 'PA_UPDATE_SET', 'int64_t', 'pa_ascii_filter',
    'pa_ascii_valid', 'pa_autoload_info', 'pa_autoload_info_cb_t',
    'pa_autoload_type', 'pa_autoload_type_t',
    'pa_autoload_type_t__enumvalues', 'pa_buffer_attr',
    'pa_bytes_per_second', 'pa_bytes_snprint', 'pa_bytes_to_usec',
    'pa_card_info', 'pa_card_info_cb_t', 'pa_card_port_info',
    'pa_card_profile_info', 'pa_card_profile_info2', 'pa_channel_map',
    'pa_channel_map_can_balance', 'pa_channel_map_can_fade',
    'pa_channel_map_can_lfe_balance', 'pa_channel_map_compatible',
    'pa_channel_map_def', 'pa_channel_map_def_t',
    'pa_channel_map_def_t__enumvalues', 'pa_channel_map_equal',
    'pa_channel_map_has_position', 'pa_channel_map_init',
    'pa_channel_map_init_auto', 'pa_channel_map_init_extend',
    'pa_channel_map_init_mono', 'pa_channel_map_init_stereo',
    'pa_channel_map_mask', 'pa_channel_map_parse',
    'pa_channel_map_snprint', 'pa_channel_map_superset',
    'pa_channel_map_to_name', 'pa_channel_map_to_pretty_name',
    'pa_channel_map_valid', 'pa_channel_position',
    'pa_channel_position_from_string', 'pa_channel_position_mask_t',
    'pa_channel_position_t', 'pa_channel_position_t__enumvalues',
    'pa_channel_position_to_pretty_string',
    'pa_channel_position_to_string', 'pa_channels_valid',
    'pa_client_info', 'pa_client_info_cb_t', 'pa_context',
    'pa_context_add_autoload', 'pa_context_connect',
    'pa_context_disconnect', 'pa_context_drain', 'pa_context_errno',
    'pa_context_event_cb_t', 'pa_context_exit_daemon',
    'pa_context_flags', 'pa_context_flags_t',
    'pa_context_flags_t__enumvalues',
    'pa_context_get_autoload_info_by_index',
    'pa_context_get_autoload_info_by_name',
    'pa_context_get_autoload_info_list',
    'pa_context_get_card_info_by_index',
    'pa_context_get_card_info_by_name',
    'pa_context_get_card_info_list', 'pa_context_get_client_info',
    'pa_context_get_client_info_list', 'pa_context_get_index',
    'pa_context_get_module_info', 'pa_context_get_module_info_list',
    'pa_context_get_protocol_version',
    'pa_context_get_sample_info_by_index',
    'pa_context_get_sample_info_by_name',
    'pa_context_get_sample_info_list', 'pa_context_get_server',
    'pa_context_get_server_info',
    'pa_context_get_server_protocol_version',
    'pa_context_get_sink_info_by_index',
    'pa_context_get_sink_info_by_name',
    'pa_context_get_sink_info_list', 'pa_context_get_sink_input_info',
    'pa_context_get_sink_input_info_list',
    'pa_context_get_source_info_by_index',
    'pa_context_get_source_info_by_name',
    'pa_context_get_source_info_list',
    'pa_context_get_source_output_info',
    'pa_context_get_source_output_info_list', 'pa_context_get_state',
    'pa_context_get_tile_size', 'pa_context_index_cb_t',
    'pa_context_is_local', 'pa_context_is_pending',
    'pa_context_kill_client', 'pa_context_kill_sink_input',
    'pa_context_kill_source_output',
    'pa_context_load_cookie_from_file', 'pa_context_load_module',
    'pa_context_move_sink_input_by_index',
    'pa_context_move_sink_input_by_name',
    'pa_context_move_source_output_by_index',
    'pa_context_move_source_output_by_name', 'pa_context_new',
    'pa_context_new_with_proplist', 'pa_context_notify_cb_t',
    'pa_context_play_sample', 'pa_context_play_sample_cb_t',
    'pa_context_play_sample_with_proplist',
    'pa_context_proplist_remove', 'pa_context_proplist_update',
    'pa_context_ref', 'pa_context_remove_autoload_by_index',
    'pa_context_remove_autoload_by_name', 'pa_context_remove_sample',
    'pa_context_rttime_new', 'pa_context_rttime_restart',
    'pa_context_set_card_profile_by_index',
    'pa_context_set_card_profile_by_name',
    'pa_context_set_default_sink', 'pa_context_set_default_source',
    'pa_context_set_event_callback', 'pa_context_set_name',
    'pa_context_set_port_latency_offset',
    'pa_context_set_sink_input_mute',
    'pa_context_set_sink_input_volume',
    'pa_context_set_sink_mute_by_index',
    'pa_context_set_sink_mute_by_name',
    'pa_context_set_sink_port_by_index',
    'pa_context_set_sink_port_by_name',
    'pa_context_set_sink_volume_by_index',
    'pa_context_set_sink_volume_by_name',
    'pa_context_set_source_mute_by_index',
    'pa_context_set_source_mute_by_name',
    'pa_context_set_source_output_mute',
    'pa_context_set_source_output_volume',
    'pa_context_set_source_port_by_index',
    'pa_context_set_source_port_by_name',
    'pa_context_set_source_volume_by_index',
    'pa_context_set_source_volume_by_name',
    'pa_context_set_state_callback',
    'pa_context_set_subscribe_callback', 'pa_context_stat',
    'pa_context_state', 'pa_context_state_t',
    'pa_context_state_t__enumvalues', 'pa_context_subscribe',
    'pa_context_subscribe_cb_t', 'pa_context_success_cb_t',
    'pa_context_suspend_sink_by_index',
    'pa_context_suspend_sink_by_name',
    'pa_context_suspend_source_by_index',
    'pa_context_suspend_source_by_name', 'pa_context_unload_module',
    'pa_context_unref', 'pa_cvolume', 'pa_cvolume_avg',
    'pa_cvolume_avg_mask', 'pa_cvolume_channels_equal_to',
    'pa_cvolume_compatible', 'pa_cvolume_compatible_with_channel_map',
    'pa_cvolume_dec', 'pa_cvolume_equal', 'pa_cvolume_get_balance',
    'pa_cvolume_get_fade', 'pa_cvolume_get_lfe_balance',
    'pa_cvolume_get_position', 'pa_cvolume_inc',
    'pa_cvolume_inc_clamp', 'pa_cvolume_init', 'pa_cvolume_max',
    'pa_cvolume_max_mask', 'pa_cvolume_merge', 'pa_cvolume_min',
    'pa_cvolume_min_mask', 'pa_cvolume_remap', 'pa_cvolume_scale',
    'pa_cvolume_scale_mask', 'pa_cvolume_set',
    'pa_cvolume_set_balance', 'pa_cvolume_set_fade',
    'pa_cvolume_set_lfe_balance', 'pa_cvolume_set_position',
    'pa_cvolume_snprint', 'pa_cvolume_snprint_verbose',
    'pa_cvolume_valid', 'pa_defer_event', 'pa_defer_event_cb_t',
    'pa_defer_event_destroy_cb_t', 'pa_device_type',
    'pa_device_type_t', 'pa_device_type_t__enumvalues',
    'pa_direction', 'pa_direction_t', 'pa_direction_t__enumvalues',
    'pa_direction_to_string', 'pa_direction_valid', 'pa_encoding',
    'pa_encoding_from_string', 'pa_encoding_t',
    'pa_encoding_t__enumvalues', 'pa_encoding_to_string',
    'pa_error_code', 'pa_error_code_t', 'pa_error_code_t__enumvalues',
    'pa_ext_device_manager_delete',
    'pa_ext_device_manager_enable_role_device_priority_routing',
    'pa_ext_device_manager_info', 'pa_ext_device_manager_read',
    'pa_ext_device_manager_read_cb_t',
    'pa_ext_device_manager_reorder_devices_for_role',
    'pa_ext_device_manager_role_priority_info',
    'pa_ext_device_manager_set_device_description',
    'pa_ext_device_manager_set_subscribe_cb',
    'pa_ext_device_manager_subscribe',
    'pa_ext_device_manager_subscribe_cb_t',
    'pa_ext_device_manager_test', 'pa_ext_device_manager_test_cb_t',
    'pa_ext_device_restore_info',
    'pa_ext_device_restore_read_device_formats_cb_t',
    'pa_ext_device_restore_read_formats',
    'pa_ext_device_restore_read_formats_all',
    'pa_ext_device_restore_save_formats',
    'pa_ext_device_restore_set_subscribe_cb',
    'pa_ext_device_restore_subscribe',
    'pa_ext_device_restore_subscribe_cb_t',
    'pa_ext_device_restore_test', 'pa_ext_device_restore_test_cb_t',
    'pa_ext_stream_restore_delete', 'pa_ext_stream_restore_info',
    'pa_ext_stream_restore_read', 'pa_ext_stream_restore_read_cb_t',
    'pa_ext_stream_restore_set_subscribe_cb',
    'pa_ext_stream_restore_subscribe',
    'pa_ext_stream_restore_subscribe_cb_t',
    'pa_ext_stream_restore_test', 'pa_ext_stream_restore_test_cb_t',
    'pa_ext_stream_restore_write', 'pa_format_info',
    'pa_format_info_copy', 'pa_format_info_free',
    'pa_format_info_free_string_array',
    'pa_format_info_from_sample_spec', 'pa_format_info_from_string',
    'pa_format_info_get_channel_map', 'pa_format_info_get_channels',
    'pa_format_info_get_prop_int',
    'pa_format_info_get_prop_int_array',
    'pa_format_info_get_prop_int_range',
    'pa_format_info_get_prop_string',
    'pa_format_info_get_prop_string_array',
    'pa_format_info_get_prop_type', 'pa_format_info_get_rate',
    'pa_format_info_get_sample_format',
    'pa_format_info_is_compatible', 'pa_format_info_is_pcm',
    'pa_format_info_new', 'pa_format_info_set_channel_map',
    'pa_format_info_set_channels', 'pa_format_info_set_prop_int',
    'pa_format_info_set_prop_int_array',
    'pa_format_info_set_prop_int_range',
    'pa_format_info_set_prop_string',
    'pa_format_info_set_prop_string_array', 'pa_format_info_set_rate',
    'pa_format_info_set_sample_format', 'pa_format_info_snprint',
    'pa_format_info_to_sample_spec', 'pa_format_info_valid',
    'pa_frame_size', 'pa_free_cb_t', 'pa_get_binary_name',
    'pa_get_fqdn', 'pa_get_home_dir', 'pa_get_host_name',
    'pa_get_library_version', 'pa_get_user_name', 'pa_gettimeofday',
    'pa_glib_mainloop', 'pa_glib_mainloop_free',
    'pa_glib_mainloop_get_api', 'pa_glib_mainloop_new', 'pa_io_event',
    'pa_io_event_cb_t', 'pa_io_event_destroy_cb_t',
    'pa_io_event_flags', 'pa_io_event_flags_t',
    'pa_io_event_flags_t__enumvalues', 'pa_locale_to_utf8',
    'pa_mainloop', 'pa_mainloop_api', 'pa_mainloop_api_once',
    'pa_mainloop_dispatch', 'pa_mainloop_free', 'pa_mainloop_get_api',
    'pa_mainloop_get_retval', 'pa_mainloop_iterate',
    'pa_mainloop_new', 'pa_mainloop_poll', 'pa_mainloop_prepare',
    'pa_mainloop_quit', 'pa_mainloop_run',
    'pa_mainloop_set_poll_func', 'pa_mainloop_wakeup',
    'pa_module_info', 'pa_module_info_cb_t', 'pa_msleep',
    'pa_operation', 'pa_operation_cancel', 'pa_operation_get_state',
    'pa_operation_notify_cb_t', 'pa_operation_ref',
    'pa_operation_set_state_callback', 'pa_operation_state',
    'pa_operation_state_t', 'pa_operation_state_t__enumvalues',
    'pa_operation_unref', 'pa_parse_sample_format',
    'pa_path_get_filename', 'pa_poll_func', 'pa_port_available',
    'pa_port_available_t', 'pa_port_available_t__enumvalues',
    'pa_prop_type_t', 'pa_proplist', 'pa_proplist_clear',
    'pa_proplist_contains', 'pa_proplist_copy', 'pa_proplist_equal',
    'pa_proplist_free', 'pa_proplist_from_string', 'pa_proplist_get',
    'pa_proplist_gets', 'pa_proplist_isempty', 'pa_proplist_iterate',
    'pa_proplist_key_valid', 'pa_proplist_new', 'pa_proplist_set',
    'pa_proplist_setf', 'pa_proplist_setp', 'pa_proplist_sets',
    'pa_proplist_size', 'pa_proplist_to_string',
    'pa_proplist_to_string_sep', 'pa_proplist_unset',
    'pa_proplist_unset_many', 'pa_proplist_update', 'pa_rtclock_now',
    'pa_sample_format', 'pa_sample_format_is_be',
    'pa_sample_format_is_le', 'pa_sample_format_t',
    'pa_sample_format_t__enumvalues', 'pa_sample_format_to_string',
    'pa_sample_format_valid', 'pa_sample_info', 'pa_sample_info_cb_t',
    'pa_sample_rate_valid', 'pa_sample_size',
    'pa_sample_size_of_format', 'pa_sample_spec',
    'pa_sample_spec_equal', 'pa_sample_spec_init',
    'pa_sample_spec_snprint', 'pa_sample_spec_valid', 'pa_seek_mode',
    'pa_seek_mode_t', 'pa_seek_mode_t__enumvalues', 'pa_server_info',
    'pa_server_info_cb_t', 'pa_signal_cb_t', 'pa_signal_destroy_cb_t',
    'pa_signal_done', 'pa_signal_event', 'pa_signal_free',
    'pa_signal_init', 'pa_signal_new', 'pa_signal_set_destroy',
    'pa_simple', 'pa_simple_drain', 'pa_simple_flush',
    'pa_simple_free', 'pa_simple_get_latency', 'pa_simple_new',
    'pa_simple_read', 'pa_simple_write', 'pa_sink_flags',
    'pa_sink_flags_t', 'pa_sink_flags_t__enumvalues', 'pa_sink_info',
    'pa_sink_info_cb_t', 'pa_sink_input_info',
    'pa_sink_input_info_cb_t', 'pa_sink_port_info', 'pa_sink_state',
    'pa_sink_state_t', 'pa_sink_state_t__enumvalues',
    'pa_source_flags', 'pa_source_flags_t',
    'pa_source_flags_t__enumvalues', 'pa_source_info',
    'pa_source_info_cb_t', 'pa_source_output_info',
    'pa_source_output_info_cb_t', 'pa_source_port_info',
    'pa_source_state', 'pa_source_state_t',
    'pa_source_state_t__enumvalues', 'pa_spawn_api', 'pa_stat_info',
    'pa_stat_info_cb_t', 'pa_stream', 'pa_stream_begin_write',
    'pa_stream_cancel_write', 'pa_stream_connect_playback',
    'pa_stream_connect_record', 'pa_stream_connect_upload',
    'pa_stream_cork', 'pa_stream_direction', 'pa_stream_direction_t',
    'pa_stream_direction_t__enumvalues', 'pa_stream_disconnect',
    'pa_stream_drain', 'pa_stream_drop', 'pa_stream_event_cb_t',
    'pa_stream_finish_upload', 'pa_stream_flags', 'pa_stream_flags_t',
    'pa_stream_flags_t__enumvalues', 'pa_stream_flush',
    'pa_stream_get_buffer_attr', 'pa_stream_get_channel_map',
    'pa_stream_get_context', 'pa_stream_get_device_index',
    'pa_stream_get_device_name', 'pa_stream_get_format_info',
    'pa_stream_get_index', 'pa_stream_get_latency',
    'pa_stream_get_monitor_stream', 'pa_stream_get_sample_spec',
    'pa_stream_get_state', 'pa_stream_get_time',
    'pa_stream_get_timing_info', 'pa_stream_get_underflow_index',
    'pa_stream_is_corked', 'pa_stream_is_suspended', 'pa_stream_new',
    'pa_stream_new_extended', 'pa_stream_new_with_proplist',
    'pa_stream_notify_cb_t', 'pa_stream_peek', 'pa_stream_prebuf',
    'pa_stream_proplist_remove', 'pa_stream_proplist_update',
    'pa_stream_readable_size', 'pa_stream_ref',
    'pa_stream_request_cb_t', 'pa_stream_set_buffer_attr',
    'pa_stream_set_buffer_attr_callback',
    'pa_stream_set_event_callback',
    'pa_stream_set_latency_update_callback',
    'pa_stream_set_monitor_stream', 'pa_stream_set_moved_callback',
    'pa_stream_set_name', 'pa_stream_set_overflow_callback',
    'pa_stream_set_read_callback', 'pa_stream_set_started_callback',
    'pa_stream_set_state_callback',
    'pa_stream_set_suspended_callback',
    'pa_stream_set_underflow_callback',
    'pa_stream_set_write_callback', 'pa_stream_state',
    'pa_stream_state_t', 'pa_stream_state_t__enumvalues',
    'pa_stream_success_cb_t', 'pa_stream_trigger', 'pa_stream_unref',
    'pa_stream_update_sample_rate', 'pa_stream_update_timing_info',
    'pa_stream_writable_size', 'pa_stream_write',
    'pa_stream_write_ext_free', 'pa_strerror',
    'pa_subscription_event_type', 'pa_subscription_event_type_t',
    'pa_subscription_event_type_t__enumvalues',
    'pa_subscription_mask', 'pa_subscription_mask_t',
    'pa_subscription_mask_t__enumvalues', 'pa_sw_cvolume_divide',
    'pa_sw_cvolume_divide_scalar', 'pa_sw_cvolume_multiply',
    'pa_sw_cvolume_multiply_scalar', 'pa_sw_cvolume_snprint_dB',
    'pa_sw_volume_divide', 'pa_sw_volume_from_dB',
    'pa_sw_volume_from_linear', 'pa_sw_volume_multiply',
    'pa_sw_volume_snprint_dB', 'pa_sw_volume_to_dB',
    'pa_sw_volume_to_linear', 'pa_thread_make_realtime',
    'pa_threaded_mainloop', 'pa_threaded_mainloop_accept',
    'pa_threaded_mainloop_free', 'pa_threaded_mainloop_get_api',
    'pa_threaded_mainloop_get_retval',
    'pa_threaded_mainloop_in_thread', 'pa_threaded_mainloop_lock',
    'pa_threaded_mainloop_new', 'pa_threaded_mainloop_once_unlocked',
    'pa_threaded_mainloop_set_name', 'pa_threaded_mainloop_signal',
    'pa_threaded_mainloop_start', 'pa_threaded_mainloop_stop',
    'pa_threaded_mainloop_unlock', 'pa_threaded_mainloop_wait',
    'pa_time_event', 'pa_time_event_cb_t',
    'pa_time_event_destroy_cb_t', 'pa_timeval_add', 'pa_timeval_age',
    'pa_timeval_cmp', 'pa_timeval_diff', 'pa_timeval_load',
    'pa_timeval_store', 'pa_timeval_sub', 'pa_timing_info',
    'pa_update_mode', 'pa_update_mode_t',
    'pa_update_mode_t__enumvalues', 'pa_usec_t', 'pa_usec_to_bytes',
    'pa_utf8_filter', 'pa_utf8_to_locale', 'pa_utf8_valid',
    'pa_volume_snprint', 'pa_volume_snprint_verbose', 'pa_volume_t',
    'pa_xfree', 'pa_xmalloc', 'pa_xmalloc0', 'pa_xmemdup',
    'pa_xrealloc', 'pa_xstrdup', 'pa_xstrndup', 'size_t',
    'struct__GMainContext', 'struct_pa_autoload_info',
    'struct_pa_buffer_attr', 'struct_pa_card_info',
    'struct_pa_card_port_info', 'struct_pa_card_profile_info',
    'struct_pa_card_profile_info2', 'struct_pa_channel_map',
    'struct_pa_client_info', 'struct_pa_context', 'struct_pa_cvolume',
    'struct_pa_defer_event', 'struct_pa_ext_device_manager_info',
    'struct_pa_ext_device_manager_role_priority_info',
    'struct_pa_ext_device_restore_info',
    'struct_pa_ext_stream_restore_info', 'struct_pa_format_info',
    'struct_pa_glib_mainloop', 'struct_pa_io_event',
    'struct_pa_mainloop', 'struct_pa_mainloop_api',
    'struct_pa_module_info', 'struct_pa_operation',
    'struct_pa_proplist', 'struct_pa_sample_info',
    'struct_pa_sample_spec', 'struct_pa_server_info',
    'struct_pa_signal_event', 'struct_pa_simple',
    'struct_pa_sink_info', 'struct_pa_sink_input_info',
    'struct_pa_sink_port_info', 'struct_pa_source_info',
    'struct_pa_source_output_info', 'struct_pa_source_port_info',
    'struct_pa_spawn_api', 'struct_pa_stat_info', 'struct_pa_stream',
    'struct_pa_threaded_mainloop', 'struct_pa_time_event',
    'struct_pa_timing_info', 'struct_pollfd', 'struct_timeval',
    'uint32_t', 'uint64_t', 'uint8_t']
