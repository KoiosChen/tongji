
from fdfs_client.client import Fdfs_client
import os
import datetime
import redis
import json


def processing(ip, startTime, stopTime, filename):
    def operate_redis(ip, start_time, stop_time, ret):
        redis_db = redis.Redis(host='localhost', port=6379, db=3)
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
        redis_db.close()


    def uploadToFdfs(ip, source_file_name):
        print('Start to upload file {}'.format(source_file_name))
        fc = Fdfs_client('/etc/fdfs/client.conf')
        ret = fc.upload_by_filename(source_file_name)
        os.remove(source_file_name)
        print(ret)
        return ret


    print('connecting camera {}'.format(ip))

    uploadResult = uploadToFdfs(ip, filename)
    operate_redis(ip, startTime, stopTime, uploadResult)

    return 1
