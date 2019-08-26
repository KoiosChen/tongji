import threading
from .. import logger, work_q, redis_db, p_msg_cb_func, socketio
import json
from ..models import gate_dict
import uuid
from ..MyModule.HashContent import md5_content
import os


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

            camera_json = [{'gate':gk, 'camera_type': ck, 'camera_ip': cv} for gk, gv in gate_dict.items() for ck, cv in gv.items() if
                             cv == capture_result['camera_ip']][0]
            camera_json['pic_path'] = capture_result['url'] + '/' + capture_result['ret']['Remote file_id'].decode()
            camera_json['gate_name'] = gate_dict[camera_json['gate']]['gate_name']

            socketio.emit('ws_test', camera_json, namespace='/test')

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
