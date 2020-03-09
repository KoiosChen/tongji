PATH_PREFIX = '/Users/Peter/python/WeBrokersTools/app/'
TMP_PROPOSAL = 'tmp_proposal/'
CONFIG_FILE_PATH = PATH_PREFIX + 'config_file/'
UPLOAD_FOLDER = PATH_PREFIX + 'UploadFile/'
CACTI_PIC_FOLDER = PATH_PREFIX + '/static/cacti_pic/'
WATERMARK_TEMPLATE = PATH_PREFIX + 'static/watermark_template/'

CALLBACK_URL = dict()

PermissionIP = ['112.64.53.150', '127.0.0.1', '192.168.42.10', '10.190.0.249']

gate_dict = {'gate1': {'camera_in': '10.170.0.230',
                       'camera_out': '10.170.0.231',
                       'gate_name': '教学楼门口'},
             'gate2': {'camera_in': '10.170.0.234',
                       'camera_out': '10.170.0.235',
                       'gate_name': '东区桥头道闸'},
             'gate3': {'camera_in': '10.170.0.236',
                       'camera_out': '10.170.0.237',
                       'gate_name': '东区东门道闸'},
             'gate4': {'camera_in': '10.170.0.238',
                       'camera_out': '10.170.0.239',
                       'gate_name': '东区西门道闸'}
             }

lib_so = '/opt/tongji/app/static/ice_ipcsdk_lib/libice_ipcsdk.so'

img_url = 'http://221.181.89.66:811'

CONNECT_RETRY_TIMES = 1
