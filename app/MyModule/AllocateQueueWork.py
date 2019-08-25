import threading
from .. import logger, work_q, redis_db, p_msg_cb_func
import json
import uuid
from ..MyModule.HashContent import md5_content
import os


class StartThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            camera_ip = self.queue.get()
            print(camera_ip)
            p_msg_cb_func[camera_ip].capture_pic()
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
