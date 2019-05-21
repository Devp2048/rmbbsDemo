from flask import session, redirect, url_for, g
from functools import wraps
import config

def login_required(func_view):
    @wraps(func_view)
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func_view(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner

def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.home'))
        return inner
    return outter