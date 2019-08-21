#!/usr/bin/env python
import os
from app import create_app, db, redis_db
from app.models import User, Role
from app.MyModule import SendMail, ResultCallBack
from TrafficLight import AllocateWorker, axa, prudential, watermark
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

__author__ = 'Koios'

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# 启动调度程序
AllocateWorker.allocate_worker(thread_num=10)

# 处理回调
ResultCallBack.callback_worker(thread_num=10)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, sendmail=SendMail, axa=axa, prudential=prudential,
                redis_db=redis_db, watermark=watermark)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
