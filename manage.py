from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from rmbbsDemo import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import Banner, Board, Post

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_models.FrontUser

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

###############################################后台操作相关###############################################
#命令行创建cms用户
@manager.option('-u', '--username',dest='username')
@manager.option('-p', '--password',dest='password')
@manager.option('-e', '--email',dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功!')

#命令行创建角色类型表
@manager.command
def create_role():
    #1. 用户（可以修改个人数据）
    visitor = CMSRole(name='用户', desc='只能浏览数据，不能修改数据')
    visitor.permissions = CMSPermission.VISITOR

    #2. 管理员（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='管理员', desc='管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER\
                           |CMSPermission.FRONTUSER

    #3. 超级管理员（拥有绝大部分权限）
    admin = CMSRole(name='超级管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER\
                        |CMSPermission.BOARDER|CMSPermission.FRONTUSER|CMSPermission.CMSUSER

    #4. 开发者（所有权限）
    developer = CMSRole(name='开发者', desc='开发人员专用权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

#命令行添加cms用户角色
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户角色添加成功！")
        else:
            print("没有这个角色：%s" % name)
    else:
        print("没有邮箱为%s的用户" % email)

#命令行查看cms用户权限
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def has_permission(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            if user.has_permission(role.permissions):
                print("邮箱为[%s]的用户有[%s]权限" % (email, name))
            else:
                print("邮箱为[%s]的用户没有[%s]权限" % (email, name))
        else:
            print("这个角色不存在[%s]" % name)
    else:
        print("没有邮箱为[%s]的用户" % email)


###############################################前台操作相关###############################################
#命令行创建前台用户
@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print("普通用户添加成功!")

#命令行批量创建测试帖子
@manager.command
def create_test_post():
    for i in range(1, 7):
        board_id = 9
        title = "板块%s——标题%s"%(board_id,i)
        content = "内容%s"%i
        board = Board.query.get(board_id)
        author = FrontUser.query.first()
        post = Post(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print("测试帖子添加成功!")

if __name__ == '__main__':
    manager.run()