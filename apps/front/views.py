from flask import (Blueprint,
                   views,
                   render_template,
                   request,
                   session,
                   url_for,
                   g,
                   abort
)
from .forms import SignupForm,SigninForm,AddPostForm,AddCommentForm
from .models import FrontUser
from ..models import Banner, Board, Post, Comment
from utils import restful, safeutils
from exts import db
import config
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint("front", __name__)

@bp.route('/')
def index():
    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st', type=int, default=1)
    banners = Banner.query.order_by(Banner.priority.desc()).all()
    boards = Board.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    # if sort == 1:
    #     query_obj = Post.query.order_by("-create_time")
    # elif sort == 2:
    #     query_obj = Post.query.order_by("-check_num")
    # else:
    #     query_obj = Post.query
    if board_id:
        query_obj = Post.query.filter(Post.board_id==board_id)
    else:
        query_obj = Post.query
    posts = query_obj.slice(start, end)
    posts_len = query_obj.count()
    posts_total_len = Post.query.count()
    pagination = Pagination(page=page, total=posts_len, bs_version=3, outer_window=0, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'current_board': board_id,
        'posts': posts,
        'posts_total_len': posts_total_len,
        'pagination': pagination,
        'current_sort': sort
    }
    return render_template("front/front_index.html", **context)

# 用户注册
class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url((return_to)):
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template("front/front_signup.html")

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message=form.get_error())
bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))

# 用户登录
class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url((return_to)) and return_to != url_for("front.signup"):
            return render_template("front/front_signin.html", return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            account = form.account.data
            password = form.password.data
            remember = form.remember.data
            telephone_user = FrontUser.query.filter_by(telephone=account).first()
            username_user = FrontUser.query.filter_by(username=account).first()
            if telephone_user and telephone_user.check_password(password):
                session[config.FRONT_USER_ID] = telephone_user.id
                if remember:
                    session.permanent = True
                return restful.success()
            elif username_user and username_user.check_password(password):
                session[config.FRONT_USER_ID] = username_user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.param_error(message="账号或密码错误!")
        else:
            return restful.param_error(message=form.get_error())
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))

# 发布帖子
class AddPostView(views.MethodView):
    decorators = [login_required]
    def get(self):
        boards = Board.query.all()
        context = {
            'boards': boards
        }
        return render_template("front/front_apost.html", **context)
    def post(self):
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = Board.query.get(board_id)
            if board:
                post = Post(title=title, content=content)
                post.board = board
                post.author = g.front_user
                db.session.add(post)
                db.session.commit()
                return restful.success()
            else:
                return restful.param_error(message="板块不存在!")
        else:
            return restful.param_error(message=form.get_error())
bp.add_url_rule('/apost/', view_func=AddPostView.as_view('apost'))

@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    post.check_num += 1
    db.session.commit()
    # post = Post.query.get(post_id)
    context = {
        'post': post
    }
    return render_template('front/front_post_detail.html', **context)

@bp.route('/acomment/', methods=['POST'])
@login_required
def acomment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = Post.query.get(post_id)
        if post:
            comment = Comment(content=content)
            comment.post = post
            comment.user = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message=form.get_error('没有这篇帖子'))
    else:
        return restful.param_error(message=form.get_error())