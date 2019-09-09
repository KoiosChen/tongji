import cv2
import multiprocessing
from fdfs_client.client import Fdfs_client
import os
import uuid
import datetime
import redis
import json

redis_db = redis.Redis(host='localhost', port=6379, db=3)


def recorder(ip, username='admin', password='Admin123', port='554'):
    def operate_redis(ip, start_time, stop_time, ret):
        print('write to redis')
        time_format = '%Y-%m-%d %H:%M:%S.%f'

        if not redis_db.exists(ip + '_lastrecord'):
            redis_db.set(ip + '_lastrecord', stop_time.strftime(time_format))

        if start_time >= datetime.datetime.strptime(redis_db.get(ip + '_lastrecord').decode(), time_format):
            key_name = ip + '_recorders'
            if redis_db.exists(key_name):
                exist_dict = json.loads(redis_db.get(key_name).decode())
                exist_dict[ret['Remote file_id'].decode()] = {'start_time': start_time.strftime(time_format),
                                                              'stop_time': stop_time.strftime(time_format)}
                redis_db.set(key_name, json.dumps(exist_dict))
            else:
                dict = {}
                dict[ret['Remote file_id'].decode()] = {'start_time': start_time.strftime(time_format),
                                                        'stop_time': stop_time.strftime(time_format)}
                redis_db.set(key_name, json.dumps(dict))
        else:
            print('time error for file {} from {} to {}'.format(ret['Remote file_id'].decode(),
                                                                start_time.strftime(time_format),
                                                                stop_time.strftime(time_format)))

    def convert_upload(source_file_name, ip, start_time, stop_time):
        print('Start to convert {}'.format(source_file_name))
        target_file_name = str(uuid.uuid1()) + '.mp4'
        os.system('ffmpeg -i {} -vcodec libx264 -f mp4 {}'.format(source_file_name, target_file_name))
        print('Start to upload file {}'.format(target_file_name))
        fc = Fdfs_client('/etc/fdfs/client.conf')
        ret = fc.upload_by_filename(target_file_name)
        os.remove(source_file_name)
        os.remove(target_file_name)
        operate_redis(ip, start_time, stop_time, ret)
        print(ret)
        return ret

    redis_db = redis.Redis(host='localhost', port=6379, db=3)
    print('connecting camera {}'.format(ip))
    cap = cv2.VideoCapture("rtsp://{}:{}@{}:{}//Streaming/Channels/1".format(username, password, ip, port))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    source_filename = str(uuid.uuid1()) + '.mp4'
    start_time = datetime.datetime.now()
    new_one = True
    videoWriter = cv2.VideoWriter(source_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    ret, frame = cap.read()
    while ret:
        if new_one == False:
            source_filename = str(uuid.uuid1()) + '.mp4'
            videoWriter = cv2.VideoWriter(source_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
            new_one = True
            start_time = datetime.datetime.now()
        ret, frame = cap.read()
        videoWriter.write(frame)
        stop_time = datetime.datetime.now()
        if stop_time - start_time > datetime.timedelta(seconds=900):
            print('cut', ip, ' at', stop_time)
            videoWriter.release()
            new_one = False
            convert = multiprocessing.Process(target=convert_upload,
                                              args=[source_filename, ip, start_time, stop_time, ])
            convert.daemon = True
            convert.start()


if __name__ == '__main__':

    Camera_IP_list = ['10.170.0.100', '10.170.0.101']
    for ip in Camera_IP_list:
        t = multiprocessing.Process(target=recorder, args=[ip,])
        t.daemon = True
        t.start()
