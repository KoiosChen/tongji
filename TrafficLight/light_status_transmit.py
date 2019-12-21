# server
# coding=utf8
import binascii
import sys
from gevent import socket, select
import queue
import threading
import logging
import json


def log_init():
    # logging 配置
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger()
    hdlr = logging.FileHandler("log.txt")
    formatter = logging.Formatter(fmt='%(asctime)s - %(module)s-%(funcName)s - %(levelname)s - %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    return logger


# 帧结构
color = {'00': 'black', '01': 'green', '10': 'yellow', '11': 'red'}
flash = {'0': 'no', '1': 'yes'}
light_direction = {'00': 'east', '01': 'west', '10': 'south', '11': 'north'}
light_attribute = {'000': 'permit through', '001': 'turn left', '010': 'go straight', '011': 'turn right',
                   '100': 'pedestrian cross the street once', '101': 'pedestrian cross the street twice'}

# 目标java udp socket
address = ('192.168.42.10', 1221)


def frame_analyze(host, data):
    try:
        r = binascii.b2a_hex(data).decode()
        if r[:4] == '55aa':
            d = r[6:-2]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for x in range(0, 4 * (int(r[4:6])), 4):
                # 补全16位二进制
                cb = '{:016b}'.format(int(d[0 + x:4 + x], 16))
                send_content = {host: {'direction': light_direction[cb[0:2]],
                                       'attribute': light_attribute[cb[2:5]],
                                       'flash': flash[cb[5:6]],
                                       'color': color[cb[6:8]],
                                       'counter': int(cb[8:], 2)}}
                s.connect(address)
                s.send(json.dumps(send_content).encode())
            s.close()
        else:
            raise ValueError("Frame format error")
    except Exception as e:
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
                    frame_analyze(addr[0], data)
                except Exception as e:
                    logger.error('call frame analyze error {}'.format(e))

                self.queue.task_done()


def run():
    bufsize = 20480
    port = 8888
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
        logger.error('SYSLOG ERROR: {}'.format(e))
        sys.exit(1)

    logger.info("----------------traffic light transmit is started----------------\n")

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
                logger.error('traffic light transmit running error: {}'.format(str(e)))
                sys.exit(1)

    except Exception as e:
        logger.error('traffic light transmit running error: {}'.format(str(e)))
        sys.exit(1)


if __name__ == '__main__':
    # logging 配置
    logger = log_init()
    run()
