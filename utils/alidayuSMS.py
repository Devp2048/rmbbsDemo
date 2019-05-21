from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

class AlidayuSMS(object):
    APP_KEY_FIELD = 'ALIDAYU_APP_KEY'
    APP_SECRET_FIELD = 'ALIDAYU_APP_SECRET'
    SMS_SIGN_NAME_FIELD = 'ALIDAYU_SIGN_NAME'
    SMS_TEMPLATE_CODE_FIELD = 'ALIDAYU_TEMPLATE_CODE'

    def __init__(self, app=None):
        self.client = None
        self.request = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        config = app.config
        self.client = AcsClient(config[self.APP_KEY_FIELD], config[self.APP_SECRET_FIELD], 'default')
        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('dysmsapi.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_protocol_type('https') # https | http
        self.request.set_version('2017-05-25')
        self.request.set_action_name('SendSms')
        self.request.add_query_param('SignName', config[self.SMS_SIGN_NAME_FIELD])
        self.request.add_query_param('TemplateCode', config[self.SMS_TEMPLATE_CODE_FIELD])

    def sendSMS(self, phone, code):
        self.request.add_query_param('PhoneNumbers', phone)
        json_code = json.dumps({'code':code})
        self.request.add_query_param('TemplateParam', json_code)
        response = self.client.do_action_with_exception(self.request)
        return response