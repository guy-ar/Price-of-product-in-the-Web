from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

# 2 types of entries
# - first time to present the login page --> GET
# - second time to process the populated form

@user_blueprint.route('/login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # check if login is valid
        email = request.form['email']
        # decided not to save hashed password
        #password = request.form['hashed']
        password = request.form['password']
        # present the correct  exception message
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                #url_for return in a service the url of specific method - start with dot"." for current file
                #in this case the method in this file called user_alerts
                # so redurect to the new URL
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message


    # in case of GET - we need to present the login screen
    # in case of post - in case the user is invalid - TODO send an error to the users

    return render_template("users/login.html")

@user_blueprint.route('/register', methods = ['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        # check if login is valid
        email = request.form['email']
        # decided not to save hashed password
        # password = request.form['hasshed']
        password = request.form['password']
        name = request.form['name']

        # present the correct  exception message
        try:
            if User.register_user(name, email, password):
                session['email'] = email
                # url_for return in a service the url of specific method - start with dot"." for current file
                # in this case the method in this file called user_alerts
                # so redurect to the new URL
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message

    # in case of GET - we need to present the login screen
    # in case of post - in case the user is invalid - TODO send an error to the users

    return render_template("users/register.html")

@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.get_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)

@user_blueprint.route('/logout')
def user_logout():
    # remove the email session
    session['email'] = None

    return redirect(url_for('home'))

@user_blueprint.route('/check/alerts/<string_user_id>')
def check_user_alerts(user_id):
    pass

