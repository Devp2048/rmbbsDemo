from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp,InputRequired,ValidationError
import hashlib
from ..front.models import FrontUser

class SMSCaptchaForm(BaseForm):
    salt = '87vd84h23u37ff4h4d8934b`#$%'
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()
        if sign == sign2:
            return True
        else:
            return False

    def validate_telephone(self, field):
        telephone = field.data
        frontuser = FrontUser.query.filter_by(telephone=telephone).first()
        if frontuser:
            raise ValidationError(message='此手机号已被注册!')