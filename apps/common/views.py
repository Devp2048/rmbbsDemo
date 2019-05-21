from flask import Blueprint,request,make_response,jsonify
# from exts import alidayuSMS
from utils import restful,rmcache
from utils.captcha import Captcha
from io import BytesIO
from .forms import SMSCaptchaForm
import qiniu
from tasks import send_sms_captcha

bp = Blueprint("common", __name__, url_prefix='/c')

@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        # result = alidayuSMS.sendSMS(telephone, code=captcha)
        result = send_sms_captcha.delay(telephone=telephone, code=captcha)
        if result:
            print("短信验证码："+captcha)
            rmcache.set(telephone, captcha, timeout=600)#手机号作为key
            return restful.success()
        else:
            return restful.param_error(message="验证码发送失败!")
    else:
        return restful.param_error(message=form.get_error())


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    rmcache.set(text.lower(), text.lower(), timeout=600)
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = 'rw9PsY0AB0TbdTpWV6YN03ovz50xLruaR6VPSJiC'
    secret_key = '5b4jiUdDR7IVwjYisNcnsJA9324WA4dkv9kFuUxR'
    q = qiniu.Auth(access_key, secret_key)
    bucket = 'rma_qny'
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})