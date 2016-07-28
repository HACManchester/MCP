from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, email, equal_to, length

import config

class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired(message="Please enter your username.")]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Sorry, your password is a requirement.")]
    )


class SignUpForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), email]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), length(min=10)]
    )
    password1 = PasswordField(
        'Repeat your password',
        validators=[DataRequired(), equal_to(password)]
    )
    display_name = StringField('Display name')
    first_name = StringField(
        'First name',
        validators=[DataRequired(message="We need your first initial at a minimum, sorry")]
    )
    last_name = StringField(
        'last_name',
        validators=[DataRequired(message="We need your full last name, sorry"), length(min=2)]
    )
    address1 = StringField(
        'Address Line 1',
        validators=[DataRequired()]
    )
    address2 = StringField('Address Line 2 (optional)')
    address3 = StringField('Address Line 3 (optional)')
    postcode = StringField('Postcode', validators=[DataRequired(), length(min=5)])
    phone = IntegerField('Phone number', length(11), validators=[DataRequired()])
    emergency_contact_name = StringField(
        'Who should we contact if you cut your arm off',
        validators=[DataRequired()]
    )
    emergency_contact_deets = TextAreaField(
        'How should we contact them? (Please give phone number, and any other details required.)',
        validators=[DataRequired()]
    )
    anything_else = TextAreaField(
        'Is there anything else we should know about? Allergies, medical conditions, etc.'
    )
    membership_amount = IntegerField(
        'We run a "pay what you can" membership system, the recommended amount is £25, the minimum '
        '£10'
    )
    captcha = RecaptchaField(
        public_key=config.RECAPTCHA_PUBLIC_KEY,
        private_key=config.RECAPTCHA_PRIVATE_KEY,
        secure=True
    )
