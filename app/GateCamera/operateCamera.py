from ctypes import *
from .. import init_logging, fdfs_client, p_msg_cb_func, work_q
from .plate_struct_class import LightParam
from ..models import lib_so
from ..MyModule import send_socketio

logger = init_logging.init()


class Camera:
    @staticmethod
    def ice_ipcsdk_plate(pvParam, pcIP, pcNumber, pcColor, pvPicData, nPicLen, pvPlatePicData, nPlatePicLen,
                         nPlatePosLeft,
                         nPlatePosTop, nPlatePosRight, nPltePosBottom,
                         fPlateConfidence, nVehicleColor, nPlateType, nVehicleDir, nAlarmType, nSpeed, nCapTime,
                         nVehicleType, nResultHigh, nResultLow):
        logger.debug('It\'s now in ice_ipcsdk_plate callback function')
        logger.debug('There is a car waiting at the camera {}'.format(pcIP.decode()))
        # work_q.put(pcIP.decode())
        send_socketio.run(pcIP.decode())

    def __init__(self, ip):
        logger.debug(f'Initate {ip}')
        self.ip = ip
        self.r = cdll.LoadLibrary(lib_so)

        self.r.ICE_IPCSDK_Open.restype = c_void_p
        self.r.ICE_IPCSDK_GetStatus.restype = c_int
        self.r.ICE_IPCSDK_SetLightParam.restype = c_int
        self.r.ICE_IPCSDK_Capture.restype = c_int
        self.r.ICE_IPCSDK_OpenGate.restype = c_int

    def connect_camera(self):
        logger.debug('connecting camera {}'.format(self.ip))
        ICE_IPCSDK_Plate = CFUNCTYPE(c_void_p, c_void_p, c_char_p, c_char_p, c_char_p,
                                     c_void_p, c_long, c_void_p, c_long,
                                     c_long, c_long, c_long, c_long,
                                     c_float, c_long,
                                     c_long, c_long, c_long, c_long,
                                     c_long, c_long, c_long, c_long)

        p_msg_cb_func[self.ip] = ICE_IPCSDK_Plate(self.ice_ipcsdk_plate)

        self.hSDK = self.r.ICE_IPCSDK_Open(c_char_p(self.ip.encode('utf-8')), p_msg_cb_func[self.ip], 'NULL')

    def device_status(self):
        return self.r.ICE_IPCSDK_GetStatus(self.hSDK)

    def setLightParam(self, luminance):
        light_param = LightParam((luminance - 1) * 20 + 10)
        light_result = self.r.ICE_IPCSDK_SetLightParam(self.hSDK, pointer(light_param))
        logger.info(f'set light param result>> {light_result}')

    def capture_pic(self):
        pvPicData = (c_char * 1048576)()
        nPicSize = c_long(1048576)
        nPicLen = c_long(0)

        logger.debug('capturing picture')

        capture_result = self.r.ICE_IPCSDK_Capture(self.hSDK, pvPicData, nPicSize, pointer(nPicLen))

        logger.debug(f'capture result>> {capture_result} len>> {nPicLen.value}')

        ret = fdfs_client.upload_by_buffer(pvPicData, file_ext_name='jpg')
        logger.info(ret)
        return ret

    def open_gate(self):
        logger.info('Open gate {}'.format(self.ip))
        self.r.ICE_IPCSDK_OpenGate(self.hSDK)

    def close_gate(self):
        logger.info("Close gate {}".format(self.ip))
        close_result = self.r.ICE_IPCSDK_ControlAlarmOut(self.hSDK, 1)
        print(close_result)

    def close_connect(self):
        logger.info(f'close connection to the camera {self.ip}')
        self.r.ICE_IPCSDK_Close(self.hSDK)


if __name__ == '__main__':
    IP = ['10.170.0.230', '10.170.0.231']
    obj = []

    for index, ip in enumerate(IP):
        obj[index] = Camera(ip)
        obj[index].connect_camera()
