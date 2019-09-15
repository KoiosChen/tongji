from app import socketio, redis_db, hSDK_handle
from app.models import img_url, gate_dict
import json
import time


def run(camera_ip):
    camera_json = \
        [{'gate': gk, 'camera_type': ck, 'camera_ip': cv} for gk, gv in gate_dict.items() for ck, cv in gv.items() if
         cv == camera_ip][0]
    try:
        ret = hSDK_handle[camera_ip].capture_pic()
    except:
        ret = {}
        ret['Remote file_id'] = 'group1/M00/00/0D/Cr4A-1104feAbD6fABAAAHPcgn8619.jpg'.encode()
    camera_json['pic_path'] = img_url + '/' + ret['Remote file_id'].decode()
    camera_json['gate_name'] = gate_dict[camera_json['gate']]['gate_name']
    redis_db.set(camera_ip + '_camera', json.dumps(camera_json))
    socketio.emit('ws_test', {'content': camera_json}, namespace='/test')
    socketio.emit('test', {'content': 'send msg'}, namespace='/test')

    return True
