import threading
from .. import logger, work_q, redis_db, hSDK_handle, socketio
import json
from ..models import gate_dict
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
            capture_result = self.queue.get()
            # capture_result fomart:
            # {'code': 'camera',
            #  'camera_ip': pcIP.value,
            #  'url': 'http://221.181.89.66:811',
            #  'ret': ret}
            logger.debug(capture_result)
            redis_db.set(capture_result['camera_ip'], json.dumps(capture_result))
            camera_json = {}
            camera_json = [{'gate':gk, 'camera_type': ck, 'camera_ip': cv} for gk, gv in gate_dict.items() for ck, cv in gv.items() if
                             cv == capture_result['camera_ip']][0]
            capture_result['url'] = 'http://221.181.89.66:811'
            capture_result['ret'] = hSDK_handle[capture_result['camera_ip']].capture_pic()
            print(capture_result['ret'])
            camera_json['pic_path'] = capture_result['url'] + '/' + capture_result['ret']['ret']['Remote file_id'].decode()
            camera_json['gate_name'] = gate_dict[camera_json['gate']]['gate_name']
            t = {}
            t['content'] = camera_json
            socketio.emit('ws_test', t, namespace='/test')

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
