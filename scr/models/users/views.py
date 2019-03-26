from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from scr.models.alerts.alert import Alert
from scr.models.users.user import User
import scr.models.users.errors as UserErrors



user_buleprint = Blueprint('user', __name__)



@user_buleprint.route('/login', methods =['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # check login is valid
        email =request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email']=email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('/users/login.html')




@user_buleprint.route('/register')
def register_user():
    if request.method == 'POST':
        # check login is valid
        email =request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email']=email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('/users/register.html')



@user_buleprint.route('/alerts')
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alert()
    return render_template('users/alerts/jinja2', alerts = alerts)

@user_buleprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_buleprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
