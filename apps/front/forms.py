from apps.forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired
from utils import rmcache
from ..front.models import FrontUser

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请填写正确的手机号码!"),
                                        InputRequired(message='请输入手机号码!')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message="请填写正确的短信验证码!"),
                                          InputRequired(message='请输入短信验证码!')])
    username = StringField(validators=[Regexp(r'[a-zA-Z0-9_]{6,15}',message="用户名为6~15位字母数字下划线组成!"),
                                       InputRequired(message='请输入用户名!')])
    password1 = StringField(validators=[Regexp(r'[a-zA-Z0-9_@#$%&*]{6,20}',message="密码为6~20位字母数字下划线组成!"),
                                        InputRequired(message='请输入密码!')])
    password2 = StringField(validators=[EqualTo("password1", message="两次密码不一致!"),
                                        InputRequired(message='请输入确认密码!')])
    captcha = StringField(validators=[Regexp(r'\w{4}', message="图形验证码不正确!"),
                                      InputRequired(message='请输入图形验证码!')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = rmcache.get(telephone)
        if not sms_captcha_mem or sms_captcha.lower() != sms_captcha_mem.lower():
            raise ValidationError(message="短信验证码错误,试试重新获取!")

    def validate_captcha(self,field):
        captcha = field.data
        captcha_mem = rmcache.get(captcha.lower())
        if not captcha_mem:
            raise ValidationError(message="图形验证码错误,试试重新获取!")

    def validate_username(self, field):
        username = field.data
        frontuser = FrontUser.query.filter_by(username=username).first()
        if frontuser:
            raise ValidationError(message='此用户名已被注册!')

class SigninForm(BaseForm):
    account = StringField(validators=[Regexp(r'1[345789]\d{9}|[a-zA-Z0-9_]{6,15}'),
                                        InputRequired(message='请输入手机号码!')])
    password = StringField(validators=[Regexp(r'[a-zA-Z0-9_@#$%&*]{6,20}'),
                                        InputRequired(message='请输入密码!')])
    remember = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题!")])
    content = StringField(validators=[InputRequired(message="请输入内容!")])
    board_id = IntegerField(validators=[InputRequired(message="请输入板块ID!")])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message="请输入评论内容!")])
    post_id = IntegerField(validators=[InputRequired(message="请输入帖子ID!")])
