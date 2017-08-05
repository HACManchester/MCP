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
    ('Other', 'Other'),
)


class SignupForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True,
                           widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={"placeholder": "Your email address"}),
                             required=True)
    password = forms.CharField(label="Password", min_length=8,
                               widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password_check = forms.CharField(label="Re-enter Password", min_length=8,
                                     widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"}))
    username = forms.CharField(label="Username", max_length=100,
                               widget=forms.TextInput(attrs={"placeholder": "Username"}),
                               help_text="You can use this to login and will be used to refer to you in internal" 
                                         " systems")
    address = forms.CharField(label="Address", required=True,
                              widget=forms.TextInput(attrs={"placeholder": "Street Address"}))
    address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={"placeholder": "Street Address"}))
    city = forms.CharField(label="Town/City", widget=forms.TextInput(attrs={"placeholder": "Town/City"}))
    postcode = gb_forms.GBPostcodeField(label="Postcode",
                                        widget=forms.TextInput(attrs={"placeholder": "Postcode"}))
    phone = PhoneNumberField(label="Phone Number",
                             widget=forms.NumberInput(attrs={"placeholder": "Phone Number"}))
    emergency_contact_name = forms.CharField(label="Emergency Contact Name", max_length=100, required=True,
                                             widget=forms.TextInput(attrs={"placeholder": "Emergency Contact Name"}),
                                             help_text="Who should we contact if you chop your arm off?"
                                                       "<br><small>(Please note that we will, obviously, contact"
                                                       " emergency services, use this field to let us know who we"
                                                       " should inform about it)</small>")
    emergency_contact_num = PhoneNumberField(label="Emergency Contact Phone Number",
                                             widget=forms.NumberInput(attrs={
                                                 "placeholder": "Emergency Contact Number"}),
                                             help_text="How should we contact them?")
    anything_else = forms.CharField(label="Anything else we should know?",
                                    widget=forms.Textarea(attrs={"placeholder": "Anything else we should know?"}),
                                    help_text="Allergies, medical conditions etc.")
    how_find_us = forms.CharField(label="How did you find out about us?",
                                  widget=forms.Textarea(attrs={"placeholder": "How did you find out about us?"}),
                                  help_text="It would help our promotion team if you let us know how you found out "
                                            "about us")
    membership_amount = forms.CharField(label="Membership amount", widget=forms.Select(choices=MEMBERSHIP_AMOUNTS),
                                        initial='25',
                                        help_text="We run a 'Pay what you can' Membership system. The recommended"
                                                  " amount is &pound;25, but any amount above &pound;10 will be"
                                                  " accepted.")
    membership_amount_other = forms.CharField(label="Input membership amount",
                                              widget=forms.NumberInput(
                                                  attrs={"placeholder": "Input membership amount."}))
