#!/usr/bin/env python
import os
from app import create_app, db, logger, hSDK_handle
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import multiprocessing
from app.MyModule import ResultCallBack
from app.GateCamera import operateCamera

__author__ = 'Koios'

app = create_app(os.getenv('FLASK_CONFIG') or 'production')
manager = Manager(app)
migrate = Migrate(app, db)

# 启动调度程序

# 处理回调
ResultCallBack.callback_worker(thread_num=10)
logger.info('ResultCallBack.callback_worker started')

IP = ['10.170.0.230', '10.170.0.231']

for ip in IP:
    hSDK_handle[ip] = operateCamera.Camera(ip)
    hSDK_handle[ip].connect_camera()

def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
