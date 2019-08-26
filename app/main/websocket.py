from .. import db, logger, socketio, redis_db
from ..GateCamera import openGate
from ..models import gate_dict


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')


@socketio.on('open gate', namespace='/test')
def open_gate(data):
    logger.info('open gate {}'.format(data.get('camera_ip')))
    socketio.emit('open result', {'result': openGate.open(data.get('camera_ip'))}, namespace='/test')
    gate_name = [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == data.get('camera_ip')][0]
    socketio.emit('wx test', {'gate': gate_name, 'camera_type': '', 'camera_ip': '', 'pic_path': '', 'gate_name': ''},
                  namespace='/test')

    socketio.emit('open_result', {'content': '{} open'.format(data.get('camera_ip'))}, namespace='/test')
