# server
# coding=utf8
import binascii
import sys
from gevent import socket, select
import queue
import threading
import logging
import json
from app.PTZ.onvif_ptz import Move
from app import global_ptz


def log_init():
    # logging 配置
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger()
    hdlr = logging.FileHandler("log.txt")
    formatter = logging.Formatter(fmt='%(asctime)s - %(module)s-%(funcName)s - %(levelname)s - %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger


# logging 配置
logger = log_init()


# 目标java udp socket
def callback(status, content):
    address = ('10.190.0.249', 1221)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(address)
    s.send(json.dumps({"status": status, "content": content}).encode())
    s.close()


def ptz_control(host, data):
    logger.debug(f'ptz command from {host}')
    try:
        command = json.loads(data.decode())
        if host in global_ptz.keys():
            ptz_obj = global_ptz.get(host)
        else:
            ptz_obj = Move(**{'ip': command['ip'],
                              'port': int(command['port']),
                              'user': command['user'],
                              'passwd': command['passwd']})
            global_ptz[host] = ptz_obj
        getattr(ptz_obj, command['direction'])()
    except Exception as e:
        logger.error(f"{host} {data}")
        logger.error(f'frame_analyze error {e}')


class StartThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            data, addr = self.queue.get()
            if addr:
                try:
                    ptz_control(addr[0], data)
                except Exception as e:
                    logger.error('call frame analyze error {}'.format(e))

                self.queue.task_done()


def run():
    bufsize = 20480
    port = 8899
    thread_num = 20

    q = queue.Queue(maxsize=2000)

    for threads_pool in range(thread_num):
        t = StartThread(q)
        t.setDaemon(True)
        t.start()

    try:
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", port))
        sock.setblocking(False)
        input = [sock]

    except Exception as e:
        logger.error('PTZ ERROR: {}'.format(e))
        sys.exit(1)

    logger.info("----------------PTZ is started----------------\n")

    try:
        while 1:
            try:
                inputready, outputready, exceptready = select.select(input, [], [])

                for s in inputready:
                    if s == sock:
                        q.put(sock.recvfrom(bufsize))
                    else:
                        logger.warning("unknown socket: {}".format(s))

            except Exception as e:
                logger.error('PTZ running error: {}'.format(str(e)))
                sys.exit(1)

    except Exception as e:
        logger.error('PTZ running error: {}'.format(str(e)))
        sys.exit(1)


if __name__ == '__main__':
    run()
