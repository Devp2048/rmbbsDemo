from exts import db
from datetime import datetime


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    check_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    board = db.relationship("Board", backref="posts")
    author = db.relationship("FrontUser", backref="posts")


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    post = db.relationship("Post", backref="comments")
    user = db.relationship("FrontUser", backref="comments")
