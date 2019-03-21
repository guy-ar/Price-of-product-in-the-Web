from functools import wraps

from flask import session, redirect, url_for, request
from src.app import config


# decorator for checking if the email exist = meaning user already logged in
# and if not, redirect to login page
def requires_login(func):
    @wraps(func)
    def decorated_fucntion(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            # after redirect to login page, flask will get parameter for next
            # so the next request after login will be the current that was extended
            return redirect(url_for('users.user_login', next=request.path))
        #if did not happen - return to original function
        return func(*args, **kwargs)
    return decorated_fucntion


# decorator for checking if the logged in user is admin and allowed tto do some activities
# and if not, redirect to login page
def requires_admin_priv(func):
    @wraps(func)
    def decorated_fucntion(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.user_login'))
        elif session['email'] not in config.ADMINS:
            return redirect(url_for('users.user_login'))
        #if did not happen - return to original function
        return func(*args, **kwargs)
    return decorated_fucntion
