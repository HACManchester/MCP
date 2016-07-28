from flask import Blueprint, flash, render_template
from flask_bcrypt import check_password_hash
from space_automation.mod_auth import forms
from space_automation.mod_auth import models

mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            # check that everything validates
            user = models.User.get(models.User.username == form.username.data)
            check_password_hash(user.password, form.password.data)

        except models.DoesNotExist:
            flash('Your username/password does not match', 'error')
    else:
        return render_template('auth/login.html')


@mod_auth.route('/join-us/', methods=['GET', 'POST'])
def join_us():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        # do some other things
        pass
