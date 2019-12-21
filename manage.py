#!/usr/bin/env python
import os
from app import create_app, db, logger, hSDK_handle
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import multiprocessing
from app.MyModule import ResultCallBack, AllocateQueueWork
from app.GateCamera import operateCamera, camera_status
from app.models import gate_dict
from PTZ import ptz_server

app = create_app(os.getenv('FLASK_CONFIG') or 'production')
manager = Manager(app)
migrate = Migrate(app, db)

# 启动调度程序

# 处理回调
ResultCallBack.callback_worker(thread_num=10)
logger.info('ResultCallBack.callback_worker started')

# 启动调度程序
AllocateQueueWork.allocate_worker(thread_num=10)

for value in gate_dict.values():
    for k, v in value.items():
        if k in ['camera_in', 'camera_out']:
            if camera_status.status(v):
                logger.info(f">>> {v} connected!")
            else:
                logger.error(f">>> {v} cannot be connected, check the cameras power supply or network connection!")

ptz_server.run()


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
