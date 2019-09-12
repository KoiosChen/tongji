PATH_PREFIX = '/Users/Peter/python/WeBrokersTools/app/'
TMP_PROPOSAL = 'tmp_proposal/'
CONFIG_FILE_PATH = PATH_PREFIX + 'config_file/'
UPLOAD_FOLDER = PATH_PREFIX + 'UploadFile/'
CACTI_PIC_FOLDER = PATH_PREFIX + '/static/cacti_pic/'
WATERMARK_TEMPLATE = PATH_PREFIX + 'static/watermark_template/'

# CALLBACK_URL = "http://app.webrokers.hk:4000/advice/{}/notify"
CALLBACK_URL = {"version_0": "http://app.webrokers.hk:4000/advice/{}/notify",
                "lxj": "http://117.86.32.131:3010/api/notify"}

PermissionIP = ['112.64.53.150']

gate_dict = {'gate1': {'camera_in': '10.170.0.230',
                       'camera_out': '10.170.0.231',
                       'gate_name': '西区1'},
             }

lib_so = '/opt/tongji/app/static/ice_ipcsdk_lib/libice_ipcsdk.so'

img_url = 'http://221.181.89.66:811'