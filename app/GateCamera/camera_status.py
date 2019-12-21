from .operateCamera import Camera
from .. import redis_db, logger, hSDK_handle
from ..models import CONNECT_RETRY_TIMES


def connect(ip):
    tmp = Camera(ip)
    tmp.connect_camera()
    if str(tmp.device_status) == '1':
        hSDK_handle[ip] = tmp
        return True
    else:
        return False


def status(ip):
    if ip in hSDK_handle.keys() and str(hSDK_handle[ip].status) == "1":
        return True
    else:
        for _ in range(0, CONNECT_RETRY_TIMES):
            if connect(ip):
                return True
        return False