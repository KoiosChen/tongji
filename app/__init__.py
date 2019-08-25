from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_apscheduler import APScheduler
from flask_session import Session
import queue
from . import init_logging
import redis
from flask_pagedown import PageDown
from flask_socketio import SocketIO
from fdfs_client.client import *

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
redis_db = redis.Redis(host='localhost', port=6379, db=3)

logger = init_logging.init()

# fdfs_client = Fdfs_client('/etc/fdfs/client.conf')
fdfs_client = ''

hSDK_handle = {}

p_msg_cb_func = {}

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    sess.init_app(app)
    db.app = app
    db.init_app(app)
    db.create_scoped_session()
    pagedown.init_app(app)
    scheduler.init_app(app)
    scheduler.start()


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
