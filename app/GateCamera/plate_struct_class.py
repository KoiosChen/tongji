from ctypes import Structure, c_uint
'''
包含SDK中定义的c语言结构体
'''


class LightParam(Structure):
    _fields_ = [
        ('u32Luminance', c_uint),
        ('u32Reserved', c_uint * 7),
    ]