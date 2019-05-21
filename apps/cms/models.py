from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # flask提供的加密生成与解析密码


# CMS用户模型
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # self.password 等于调用self.password(password)
        self.email = email

    # 密码：对外的字段名是password
    # 密码：对内的字段名是_password
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def has_permission(self, permission):
        return permission == permission&self.permissions

    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)


# CMS用户权限类型
class CMSPermission(object):
    ALL_PERMISSION = 0b11111111  # 所有权限
    VISITOR =        0b00000001  # 访问者权限
    POSTER =         0b00000010  # 管理帖子权限
    COMMENTER =      0b00000100  # 管理评论权限
    BOARDER =        0b00001000  # 管理板块权限
    FRONTUSER =      0b00010000  # 管理前台用户权限
    CMSUSER =        0b00100000  # 管理后台用户权限


# CMS用户与CMS角色关联表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


# CMS角色模型
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)
    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')
