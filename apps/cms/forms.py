from apps.forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from utils import rmcache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式不正确'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,12,message='密码格式不正确'),InputRequired(message='请输入密码')])
    remember = IntegerField()

class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,12,message='原密码格式不正确'),InputRequired(message='请输入原密码')])
    newpwd = StringField(validators=[Length(6,12,message='新密码格式不正确'),InputRequired(message='请输入新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message="密码不一致")])


class ResetEmailForm(BaseForm):
    newemail = StringField(validators=[Email(message='邮箱格式不正确'),InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(4,4,message='验证码格式不正确'),InputRequired(message='请输入验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.newemail.data
        captcha_cache = "".join(rmcache.get(email) or [])
        if not captcha_cache:
            raise ValidationError('验证码已过期，请重新获取!')
        elif captcha.lower() != captcha_cache.lower():
            raise ValidationError('验证码错误!')

    def validate_newemail(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('此邮箱已被注册!')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入图片名称')])
    image_url = StringField(validators=[InputRequired(message='请输入图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入权重')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField()

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入版块名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField()
