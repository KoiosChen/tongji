from flask import request, jsonify
from ..models import *
from .. import logger, work_q, redis_db
from . import main
from ..decorators import permission_ip


@main.route('/capturePicOpenGate', methods=['POST'])
@permission_ip(PermissionIP)
def capturePicOpenGate():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """

    try:
        assert True if redis_db.get('webrokerstools_status').decode() == '1' else False, 'service stopped'
        print(request.json)
        request_data = request.json['data']

        # 初始化尝试次数，最多尝试三次
        request_data['try_times'] = 0
        work_q.put(request_data)

        return jsonify({'code': 'success', 'message': 'Job has been successfully put into queue', 'data': ''})
    except Exception as e:
        logger.error(e)
        return jsonify({'code': 'fail', 'message': 'job put into queue fail for ' + str(e), 'data': ''})


@main.route('/service_control', methods=['POST'])
@permission_ip(PermissionIP)
def service_control():
    """
    只允许PermissionIP中涉及的服务器访问
    data中的键值对规则：
    1. code设置：{companyName + 'login': {username: {"password": password, "action": action}}, 其中action为add, modify, del
    2. service control: {companyName + 'workstatus': '1'} ‘1’表示允许请求， ‘0’表示拒绝请求，callback会提示服务停止
     全局禁止设置：{‘webrokerstools_status’: '1'} '1', '0'的含义相同
    举例：
    {"aia_login": {"A123": {"password": "123", "action": "add"}},
     "axa_login": {"aNov22": "123123"},
     "prudential_wordstatus": "0",
     "webrokerstools_status": "1"}
    :return:
    """
    company_list = ['aia', 'axa', 'prudential', 'manutouch', 'ftlife']
    suffix_list = ['_login', '_workstatus']

    permit_key_list = [company + suffix for company in company_list for suffix in suffix_list] + [
        'webrokerstools_status']
    try:
        request_data = request.json['data']
        for key, value in request_data.items():
            assert True \
                if key in permit_key_list else False, '主键不允许'

            assert True \
                if 'status' in key and value in ['0', '1'] else False, '服务状态value不被允许'

            assert True \
                if 'login' in key and isinstance(value, dict) else False, "用户名密码设置value不被允许"

            if redis_db.get(key):
                if 'status' in key:
                    redis_db.set(key, value)
                elif 'login' in key:
                    for username, passwd_action in value.items():
                        if passwd_action['action'] == 'add':
                            pass
            else:
                redis_db.set(key, value)

            redis_db.set(key, value)
        return jsonify({'code': 'success', 'message': 'service set successful', 'data': ''})
    except Exception as e:
        return jsonify({'code': 'fail', 'message': str(e), 'data': ''})
