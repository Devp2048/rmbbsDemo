from flask import session, redirect, url_for
from functools import wraps
import config

def login_required(func_view):
    @wraps(func_view)
    def inner(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func_view(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner