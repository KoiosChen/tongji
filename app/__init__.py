from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_apscheduler import APScheduler
from flask_session import Session
import queue
import redis
from flask_pagedown import PageDown
from flask_socketio import SocketIO
from fdfs_client.client import *
import logging

bootstrap = Bootstrap()
db = SQLAlchemy()
scheduler = APScheduler()
sess = Session()
pagedown = PageDown()
socketio = SocketIO()

# 用于处理订单建议书的队列
work_q = queue.Queue(maxsize=1000)

# 用于处理回调的队列
callback_q = queue.Queue(maxsize=1000)

# 用于存放建议书订单， 需要配置持久化
redis_db = redis.Redis(host='localhost', port=6379, db=3, decode_responses=True)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()
hdlr = logging.FileHandler("run.log")
formatter = logging.Formatter(fmt='%(asctime)s - %(module)s-%(funcName)s - %(levelname)s - %(message)s',
                              datefmt='%m/%d/%Y %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

if os.path.exists('/etc/fdfs/client.conf'):
    fdfs_client = Fdfs_client('/etc/fdfs/client.conf')
else:
    fdfs_client = ''

global_ptz = dict()
hSDK_handle = dict()
p_msg_cb_func = dict()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    sess.init_app(app)
    db.app = app
    db.init_app(app)
    db.create_scoped_session()
    socketio.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
