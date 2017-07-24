from django import forms
import localflavor.gb.forms as gb_forms
from phonenumber_field.formfields import PhoneNumberField

MEMBERSHIP_AMOUNTS = (
    ('10', 10),
    ('15', 15),
    ('20', 20),
    ('25', 25),
    ('30', 30),
    ('35', 35),
    ('40', 40),
    ('50', 50),
)


class SignupForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="Password", min_length=8, widget=forms.PasswordInput())
    password_check = forms.CharField(label="Re-enter Password", min_length=8, widget=forms.PasswordInput())
    nickname = forms.CharField(label="Nickname", max_length=100)
    address = forms.CharField(label="Address", required=True)
    address1 = forms.CharField(label="Address 1")
    city = forms.CharField(label="Town/City")
    postcode = gb_forms.GBPostcodeField(label="Postcode")
    phone = PhoneNumberField(label="Phone Number")
    emergency_contact_name = forms.CharField(label="Emergency Contact Name", max_length=100, required=True)
    emergency_contact_num = PhoneNumberField(label="Emergency Contact Phone Number")
    anything_else = forms.CharField(label="Anything else we should know?", widget=forms.Textarea)
    membership_amount = forms.CharField(label="Membership amount", widget=forms.Select(choices=MEMBERSHIP_AMOUNTS),
                                        initial='25')


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", min_length=8, widget=forms.PasswordInput(), required=True)
