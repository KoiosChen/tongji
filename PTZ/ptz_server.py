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
from app import logger
import pymysql


def register_camera_ptz(ip, port=80, user='admin', passwd='Admin123'):
    if ip not in global_ptz.keys():
        logger.info(f"Camera {ip} is not exist in global_ptz, create new one!")
        ptz_obj = Move(**{'ip': ip,
                          'port': port,
                          'user': user,
                          'passwd': passwd})
        global_ptz[ip] = ptz_obj
    else:
        logger.info(f"Camera {ip} is exist in global_ptz!")
    return global_ptz[ip]


# 目标java udp socket
def callback(status, content):
    address = ('10.190.0.249', 1221)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(address)
    send_content = {"status": status, "content": content}
    logger.info(send_content)
    s.send(json.dumps(send_content).encode())
    s.close()


def ptz_control(host, data):
    logger.info(f'Got ptz command from {host}')
    try:
        command = json.loads(data.decode())
        logger.info(f"The command from {host} is {command}")
        # 注册摄像头PTZ服务，如果在全局变量中未找到注册成功的对象，则重新注册该摄像头
        ptz_obj = register_camera_ptz(ip=command['ip'],
                                      port=int(command['port']),
                                      user=command['user'],
                                      passwd=command['passwd'])
        # 调用摄像头控制指令，目前是continuousMove，需要有stop指令才会停
        result = getattr(ptz_obj, command['direction'])()
        # 回调，告知指令操作结果
        callback(result.get("status"), result.get("content"))
    except Exception as e:
        logger.error(f"PTZ command from {host}, the data is {data}. Frame_analyze error {e}")


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

    db = pymysql.connect("10.190.0.249", "root", "root", "evaluation")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select ip from device where deviceType like  '%SXJ%' and deviceType not like '%QA%'")

    for camera in cursor:
        if camera[0]:
            r = threading.Thread(target=register_camera_ptz, args=(camera[0],))
            r.start()

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
