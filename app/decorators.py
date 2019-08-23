from functools import wraps
from flask import abort, request, jsonify
from .models import Permission
from . import logger
from .MyModule.ResultCallBack import call_back


def permission_ip(permission_ip_list):
    def decorator(f):
        @wraps(f)
        def decorated_fuction(*args, **kwargs):
            logger.info(
                'IP {} is getting insurance proposal'.format(
                    request.headers.get('X-Forwarded-For', request.remote_addr)))
            if request.headers.get('X-Forwarded-For', request.remote_addr) not in permission_ip_list:
                abort(jsonify({'code': 'fail', 'message': 'IP ' + request.remote_addr + ' not permitted', 'data': ''}))
            return f(*args, **kwargs)
        return decorated_fuction
    return decorator