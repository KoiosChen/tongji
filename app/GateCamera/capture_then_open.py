from ctypes import *


class LightParam(Structure):
    _fields_ = [
        ('u32Luminance', c_uint),
        ('u32Reserved', c_uint * 7),
    ]


r = cdll.LoadLibrary('../static/ice_ipcsdk_lib/libice_ipcsdk.so')

r.ICE_IPCSDK_Open.restype = POINTER(c_void_p)

r.ICE_IPCSDK_GetDevID.restype = c_int

r.ICE_IPCSDK_GetSDKVersion.restype = c_int

r.ICE_IPCSDK_Capture.restype = c_int

r.ICE_IPCSDK_GetCity.restype = c_int

r.ICE_IPCSDK_SetLightParam.restype = c_int

r.ICE_IPCSDK_GetExposureMode = c_int

v = (c_char * 48)()

pvPicData = (c_void_p * 1048576)()

nPicSize = c_long(1048576)

nPicLen = c_long(0)

luminance = 8

lightparam = LightParam((luminance - 1) * 20 + 10)

nMode = c_long()

r.ICE_IPCSDK_GetSDKVersion(byref(v))

print('SDK Version>> ', v.value)

hSDK = r.ICE_IPCSDK_Open(c_char_p(b'10.170.0.230'), 'NULL', 'NULL')

# set light param

light_resutl = r.ICE_IPCSDK_SetLightParam(hSDK, pointer(lightparam))

print(light_resutl)

print('capturing picture')

capture_result = r.ICE_IPCSDK_Capture(hSDK, pvPicData, nPicSize, pointer(nPicLen))

print('capture result>> ', capture_result, 'len>> ', nPicLen.value)

with open('./test_pic.jpg', 'wb') as f:
    f.write(pvPicData)

get_result = r.ICE_IPCSDK_GetExposureMode(hSDK, pointer(nMode))

print(get_result)

print("Exposure Mode>> ", nMode.value)
print('capturing picture')
