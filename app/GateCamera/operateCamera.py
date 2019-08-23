from ctypes import *
from .. import init_logging, fdfs_client
from .plate_struct_class import LightParam
from ..MyModule.ResultCallBack import call_back

logger = init_logging.init()


class Camera:
    @staticmethod
    def ice_ipcsdk_plate(pvParam, pcIP, pcNumber, pcColor, pvPicData, nPicLen, pvPlatePicData, nPlatePicLen,
                         nPlatePosLeft,
                         nPlatePosTop, nPlatePosRight, nPltePosBottom,
                         fPlateConfidence, nVehicleColor, nPlateType, nVehicleDir, nAlarmType, nSpeed, nCapTime,
                         nVehicleType, nResultigh, nResultLow):
        """
        作为ICE_IPCSDK_Open的回调函数
        :pvParam = c_void_p()
        :pcIP = (c_char * 48)()
        :pcNumber = (c_char * 48)()
        :pcColor = (c_char * 48)()
        :pvPicData = (c_void_p * 1048576)()
        :nPicLen = c_long()
        :pvPlatePicData = (c_void_p * 1048576)()
        :nPlatePicLen = c_long()
        :nPlatePosLeft = c_long()
        :nPlatePosTop = c_long()
        :nPlatePosRight = c_long()
        :nPlatePosBottom = c_long()
        :fPlateConfidence = c_float()
        :nVehicleColor = c_long()
        :nPlateType = c_long()
        :nVehicleDir = c_long()
        :nAlarmType = c_long()
        :nSpeed = c_long()
        :nCapTime = c_long()
        :nVehicleType = c_long()
        :nResultHigh = c_long()
        :nResultLow = c_long()
        :return:
        """
        logger.debug('ip address>> {}'.format(pcIP.value))
        if pcNumber:
            logger.debug('plate number>> {}'.format(pcNumber.value))

        logger.debug('pic len>> ', nPicLen.value)

        # with open('./test_pic.jpg', 'wb') as f:
        #     f.write(pvPicData)
        """
        @return dict {
        'Group name' : group_name,
        'Remote file_id' : remote_file_id,
        'Status' : 'Upload successed.',
        'Local file name' : '',
        'Uploaded size' : upload_size,
        'Storage IP' : storage_ip
        }
        """
        ret = fdfs_client.upload_by_buffer(pvPicData)
        logger.info(ret)
        call_back(cb_url='http://127.0.0.1/camera',
                  cb_value={'code': 'camera',
                            'camera_ip': pcIP.value,
                            'url': 'http://221.181.89.66:811',
                            'ret': ret})


    def __init__(self, ip):
        self.ip = ip
        self.r = cdll.LoadLibrary('../static/ice_ipcsdk_lib/libice_ipcsdk.so')

    def connect_camera(self):
        self.r.ICE_IPCSDK_Open.restype = POINTER(c_void_p)

        ICE_IPCSDK_Plate = CFUNCTYPE(c_void_p,
                                     c_void_p, POINTER(c_char * 48), POINTER(c_char * 48), POINTER(c_char * 48),
                                     c_void_p, c_long, c_void_p, c_long,
                                     c_long, c_long, c_long, c_long,
                                     c_float, c_long,
                                     c_long, c_long, c_long, c_long,
                                     c_long, c_long, c_long, c_long)

        plate_func = ICE_IPCSDK_Plate(self.ice_ipcsdk_plate)

        self.hSDK = self.r.ICE_IPCSDK_Open(c_char_p(ip.encode('utf-8')), plate_func, 'NULL')

    def device_status(self):
        self.r.ICE_IPCSDK_GetStatus.restype = c_int
        return self.r.ICE_IPCSDK_GetStatus(self.hSDK)

    def setLightParam(self, luminance):
        lightparam = LightParam((luminance - 1) * 20 + 10)
        self.r.ICE_IPCSDK_SetLightParam.restype = c_int
        light_resutl = self.r.ICE_IPCSDK_SetLightParam(self.hSDK, pointer(lightparam))
        print(light_resutl)

    def capture_pic(self):
        self.r.ICE_IPCSDK_Capture.restype = c_int

        pvPicData = (c_void_p * 1048576)()
        nPicSize = c_long(1048576)
        nPicLen = c_long(0)

        logger.debug('capturing picture')

        capture_result = self.r.ICE_IPCSDK_Capture(self.hSDK, pvPicData, nPicSize, pointer(nPicLen))

        logger.debug('capture result>> {} len>> {}'.format(capture_result, nPicLen.value))

        with open('./test_pic.jpg', 'wb') as f:
            f.write(pvPicData)

    def open_gate(self):
        logger.info('Open gate {}'.format(self.ip))
        self.r.ICE_IPCSDK_OpenGate.restype = c_int

        self.r.ICE_IPCSDK_OpenGate(self.hSDK)


if __name__ == '__main__':
    ip = '10.170.0.230'

    camera = Camera(ip)
    camera.connect_camera()
