from flask_wtf import Form
from flask import session
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, IPAddress, Optional, NumberRange
from wtforms import StringField, SubmitField, PasswordField, SelectField, SelectMultipleField, DateTimeField, \
    RadioField, TextAreaField
from ..models import Role


class UserModal(Form):

    username = StringField('用户名', validators=[Regexp('^[\u4E00-\u9FA5]*$', 0,
                                                     '用户名只能为中文 ')])
    password = PasswordField('请输入密码')
    phone_number = StringField('电话', validators=[NumberRange(1, 9, '仅数字')])
    role = SelectField('请选择角色', default='0')

    def __init__(self):
        super(UserModal, self).__init__()
        role_c = [(str(k.id), k.name) for k in Role.query.all()]
        role_c.append(('0', None))
        self.role.choices = role_c
