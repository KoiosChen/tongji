from app import socketio, redis_db, hSDK_handle, logger
from app.models import img_url, gate_dict
import json
import requests
import time


def run(camera_ip, pc_number):
    logger.info(f"camera {camera_ip} got pc_number {pc_number}")
    camera_json = \
        [{'gate': gk, 'camera_type': ck, 'camera_ip': cv} for gk, gv in gate_dict.items() for ck, cv in gv.items() if
         cv == camera_ip][0]
    try:
        ret = hSDK_handle[camera_ip].capture_pic()
    except Exception as e:
        logger.error(f"capture picture error -> {e}")
        ret = dict()
        ret['Remote file_id'] = 'group1/M00/00/0D/Cr4A-1104feAbD6fABAAAHPcgn8619.jpg'.encode()

    camera_json['pic_path'] = img_url + '/' + ret['Remote file_id'].decode()
    camera_json['gate_name'] = gate_dict[camera_json['gate']]['gate_name']

    # write to redis as a cache
    redis_db.set(camera_ip + '_camera', json.dumps(camera_json))
    redis_db.expire(camera_ip + '_camera', 600)

    # send websocket to web
    socketio.emit('ws_test', {'content': camera_json}, namespace='/test')
    socketio.emit('test', {'content': 'send msg'}, namespace='/test')

    # send restful api
    """
    camera_jason = {'gate': 'gate1', 
                    'camera_type': 'camera_in', 
                    'camera_ip': '10.170.0.234',
                    'pic_path': 'http://x.x.x.x/group1/xxxxx',
                    'gate_name': '西区大门'
                    }
    """
    api_url = "http://127.0.0.1:5555/gate_camera"
    headers = {'Content-Type': 'application/json', "encoding": "utf-8"}
    try:
        r = requests.post(api_url,
                          data=json.dumps(camera_json, ensure_ascii=False).encode('utf-8'),
                          headers=headers,
                          timeout=2)
        result = r.json()
        print(result)
    except Exception as e:
        print(e)
    return True
