from .. import db, logger, socketio, redis_db
from ..GateCamera import openGate
from ..models import gate_dict


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')
    socketio.emit('test', 'connect test', namespace='/test')


@socketio.on('open gate', namespace='/test')
def open_gate(data):
    camera_ip = data.get('camera_ip') if 'camera_ip' in data.keys() else gate_dict[data.get('gate')]['camera_in']

    logger.info('open gate {}'.format(camera_ip))
    socketio.emit('open_result', {'content': openGate.open(camera_ip)}, namespace='/test')

    gate_name = [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == camera_ip][0]
    socketio.emit('wx test',
                  {'content':
                       {'gate': gate_name,
                        'camera_type': '',
                        'camera_ip': '',
                        'pic_path': '',
                        'gate_name': ''}},
                  namespace='/test')
    redis_db.delete(camera_ip)