# Excute result call back
import requests
from .. import logger, callback_q
import threading
import time


class StartThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            try:
                cb = self.queue.get()
                cb_success = False
                logger.debug(cb)
                if 'retry' not in cb.keys():
                    cb['retry'] = 0
                else:
                    cb['retry'] += 1

                if cb['retry'] < 3:
                    for i in range(0, 3):
                        result = requests.post(cb['cb_url'], cb['cb_value'], cb['headers'])
                        r = result.json()
                        print(r)
                        if r.get('code') == 'success':
                            cb_success = True
                            break
                        else:
                            time.sleep(3)

                    if not cb_success:
                        callback_q.put(cb)

                self.queue.task_done()
            except Exception as e:
                logger.error("call back fail for {}".format(e))


# 在manager中启动回调线程池
def callback_worker(thread_num=5):
    """
    用来调度获取建议书任务，线程池默认共5个线程
    :return:
    """

    for threads_pool in range(thread_num):
        t = StartThread(callback_q)
        t.setDaemon(True)
        t.start()


# AllocateWorker调用call_back方法，把需要回调的数据put到队列里
def call_back(cb_url, cb_value):

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }

    # cb_value['url'] = cb_value['url'] + cb_value['id'] + '.pdf'

    callback_q.put({'headers': headers,
                    'cb_url': cb_url,
                    'cb_value': cb_value})

    logger.info('{} has been put in the call back queue'.format(cb_value))

    return True
