from .. import db, logger, socketio, redis_db
from ..GateCamera import openGate
from ..models import gate_dict


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')
    socketio.emit('test', 'connect test', namespace='/test')


@socketio.on('open gate', namespace='/test')
def open_gate(data):
    logger.info('open gate {}'.format(data.get('camera_ip')))
    if 'camera_ip' in data.keys():
        open_result = openGate.open(data.get('camera_ip'))
    elif 'gate' in data.keys():
        open_result = openGate.open(gate_dict[data.get('gate')]['camera_in'])
    else:
        open_result = '开启哪个闸道？'
    socketio.emit('open_result', {'content': open_result}, namespace='/test')
    gate_name = [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == data.get('camera_ip')][0]
    socketio.emit('wx test', {'gate': gate_name, 'camera_type': '', 'camera_ip': '', 'pic_path': '', 'gate_name': ''},
                  namespace='/test')

    # socketio.emit('open_result', {'content': '{} open'.format(data.get('camera_ip'))}, namespace='/test')
