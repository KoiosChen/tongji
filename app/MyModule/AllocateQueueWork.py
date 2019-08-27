import threading
from .. import logger, work_q, redis_db, hSDK_handle, socketio
import json
from ..models import gate_dict, img_url
import uuid
from ..MyModule.HashContent import md5_content
import os
from ..GateCamera import operateCamera

class StartThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            camera_ip = self.queue.get()
            # capture_result fomart:
            # {'code': 'camera',
            #  'camera_ip': pcIP.value,
            #  'url': 'http://221.181.89.66:811',
            #  'ret': ret}
            logger.debug(camera_ip)

            camera_json = [{'gate':gk, 'camera_type': ck, 'camera_ip': cv} for gk, gv in gate_dict.items() for ck, cv in gv.items() if
                             cv == camera_ip['camera_ip']][0]

            ret = hSDK_handle[camera_ip['camera_ip']].capture_pic()
            camera_json['pic_path'] = img_url + '/' + ret['Remote file_id'].decode()
            camera_json['gate_name'] = gate_dict[camera_json['gate']]['gate_name']
            redis_db.set(camera_ip, json.dumps(camera_json))
            socketio.emit('ws_test', {'content': camera_json}, namespace='/test')

            self.queue.task_done()


def allocate_worker(thread_num=10):
    """
    用来处理摄像头获取的信息，线程池默认共10个线程
    :return:
    """

    for threads_pool in range(thread_num):
        t = StartThread(work_q)
        t.setDaemon(True)
        t.start()
