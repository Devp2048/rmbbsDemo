from flask import (Blueprint,
                   views,
                   render_template,
                   request,
                   session,
                   redirect,
                   url_for,
                   g
)
from .forms import (
    LoginForm,
    ResetPwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm
)
from .models import CMSUser, CMSPermission
from ..models import Banner, Board, Post, Comment
from apps.front.models import FrontUser, GenderEnum
from .decorators import login_required, permission_required
import config
from exts import db,mail
from utils import restful, rmcache
from flask_mail import Message
import string
import random
from tasks import send_mail

bp = Blueprint("cms", __name__, url_prefix='/cms')


# 主页
@bp.route('/')
@login_required
def home():
    return render_template('cms/cms_home.html')


# 登录
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True #持久化，否则浏览器退出即删除session
                return redirect(url_for('cms.home'))
            else:
                return self.get(message="邮箱或密码错误")
        else:
            message = form.get_error()
            return self.get(message=message)
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 注销
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 修改密码
class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200, "message":""})
                return restful.success()
            else:
                # return jsonify({"code":400, "message":"原密码错误"})
                return restful.param_error("原密码错误")
        else:
            message = form.get_error()
            # return jsonify({"code":400, "message":message})
            return restful.param_error(message)
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))


# 邮箱修改验证码发送
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    email = request.args.get('newemail')
    if not email:
        return restful.param_error('请传入邮箱参数！')
    source = list(string.ascii_letters)
    source.extend(str(x) for x in range(0,10))
    captcha = random.sample(source, 4)
    captcha_str = "".join(captcha)
    # message = Message("论坛邮箱修改验证码", recipients=[email], body="您的验证码是：%s" % captcha_str)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    send_mail.delay("论坛邮箱修改验证码", [email], "您的验证码是：%s" % captcha_str)
    rmcache.set(email, captcha)
    return restful.success()


# 修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            newemail = form.newemail.data
            g.cms_user.email = newemail
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(form.get_error())
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


@bp.route('/banners/')
@login_required
#@permission_required(CMSPermission.POSTER)
def banners():
    banners = Banner.query.all()
    return render_template("cms/cms_banners.html", banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_id = form.banner_id.data
        banner = Banner.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message="无此轮播图")
    else:
        return restful.param_error(form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.param_error(message="请输入轮播图ID")
    banner = Banner.query.get(banner_id)
    if not banner:
        return restful.param_error(message="没有这个轮播图")
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    posts = Post.query.all()
    # comment_post_ids = Comment.query.with_entities(Comment.post_id).all()
    # post_comment_num = {}
    # for cpi in comment_post_ids:
    #     if cpi[0] in post_comment_num:
    #         post_comment_num[cpi[0]] += 1
    #     else:
    #         post_comment_num[cpi[0]] = 1
    context = {
        'posts': posts,
        # 'post_comment_num': post_comment_num
    }
    return render_template("cms/cms_posts.html", **context)


@bp.route('/dpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.param_error(message="请输入帖子ID")
    post = Post.query.get(post_id)
    if not post:
        return restful.param_error(message="没有这篇帖子")
    [db.session.delete(comment) for comment in post.comments]
    db.session.delete(post)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    comments = Comment.query.all()
    context = {
        'comments': comments
    }
    return render_template("cms/cms_comments.html", **context)


@bp.route('/dcomment/', methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def dcomment():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.param_error(message="请输入评论ID")
    comment = Comment.query.get(comment_id)
    if not comment:
        return restful.param_error(message="没有这条评论")
    db.session.delete(comment)
    db.session.commit()
    return restful.success()


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    boards = Board.query.all()
    comment_post_ids = Comment.query.with_entities(Comment.post_id).all()
    board_comment_num = {}
    for post_id in comment_post_ids:
        if Post.query.get(post_id[0]).board.id in board_comment_num:
            board_comment_num[Post.query.get(post_id[0]).board.id] += 1
        else:
            board_comment_num[Post.query.get(post_id[0]).board.id] = 1
    context = {
        'boards': boards,
        'board_comment_num': board_comment_num
    }
    return render_template("cms/cms_boards.html", **context)


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = Board(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board_id = form.board_id.data
        board = Board.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message="没有这个板块")
    else:
        restful.param_error(form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.param_error(message="请输入板块ID")
    board = Board.query.get(board_id)
    if not board:
        return restful.param_error(message="没有这个板块")
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    fusers = FrontUser.query.all()
    context = {
        'fusers': fusers,
        'GenderEnum': GenderEnum
    }
    return render_template("cms/cms_fusers.html", **context)


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def croles():
    return render_template("cms/cms_croles.html")