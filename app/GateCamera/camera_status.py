from .operateCamera import Camera
from .. import logger, hSDK_handle
from ..models import CONNECT_RETRY_TIMES


def connect(ip):
    tmp = Camera(ip)
    tmp.connect_camera()
    if str(tmp.device_status()) == '1':
        hSDK_handle[ip] = tmp
        return True
    else:
        return False


def status(ip):
    logger.debug(ip)
    if ip in hSDK_handle.keys() and str(hSDK_handle[ip].device_status()) == "1":
        logger.debug(f'>>> The camera {ip} is in the hSDK global dict, and the status is 1')
        return True
    else:
        logger.debug(f'>>> No connect with {ip}, try to connect the camera!')
        for t in range(0, CONNECT_RETRY_TIMES):
            logger.debug(f">>> The {t} time")
            if connect(ip):
                return True
        return False
