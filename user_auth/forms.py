from django import forms

import localflavor.gb.forms as gb_forms

from django.utils.html import mark_safe
from django.forms.models import ModelFormOptions

from mcp import ldap

# adding fieldsets to forms

_old_init = ModelFormOptions.__init__


def _new_init(self, options=None):
    _old_init(self, options)
    self.fieldsets = getattr(options, 'fieldsets', None)

ModelFormOptions.__init__ = _new_init


class Fieldset(object):
    def __init__(self, form, title, fields, classes):
        self.form = form
        self.title = title
        self.fields = fields
        self.classes = classes

    def __iter__(self):
        for field in self.fields:
            yield field


def fieldsets(self):
    meta = getattr(self, '_meta', None)
    if not meta:
        meta = getattr(self, 'Meta', None)

    if not meta or not meta.fieldsets:
        return

    for name, data in meta.fieldsets:
        yield Fieldset(
            form=self,
            title=name,
            fields=(self[f] for f in data.get('fields')),
            classes=data.get('classes', ''),
        )

#  End fieldsets additions


class SignupForm(forms.Form):

    name = forms.CharField(label="Name", max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    email = forms.EmailField(label="E-Mail", widget=forms.EmailInput(attrs={"placeholder": "Your email address"}),
                             required=True)
    password = forms.CharField(label="Password", min_length=8,
                               widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password_check = forms.CharField(label="Re-enter Password", min_length=8,
                                     widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"}))
    username = ldap.LDAPUsernameField(label="Username", max_length=100,
                               widget=forms.TextInput(attrs={"placeholder": "Username"}),
                               help_text="You can use this to login and we will use it to refer to you in internal"
                                         " systems")
    address = forms.CharField(label="Address", required=True,
                              widget=forms.TextInput(attrs={"placeholder": "Street Address"}))
    address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={"placeholder": "Street Address"}))
    city = forms.CharField(label="Town/City", widget=forms.TextInput(attrs={"placeholder": "Town/City"}))
    postcode = gb_forms.GBPostcodeField(label="Postcode",
                                        widget=forms.TextInput(attrs={"placeholder": "Postcode"}))
    phone = forms.CharField(label="Phone Number",
                               widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))
    emergency_contact_name = forms.CharField(label="Emergency Contact Name", max_length=100, required=True,
                                             widget=forms.TextInput(attrs={"placeholder": "Emergency Contact Name"}),
                                             help_text=mark_safe("Please note that we will, obviously,"
                                                                 " contact emergency services, use this field to let us"
                                                                 " know who we should inform about it."))
    emergency_contact_num = forms.CharField(label="Emergency Contact Phone Number",
                                               widget=forms.TextInput(attrs={
                                                 "placeholder": "Emergency Contact Number"}),
                                               help_text="What number should we use to contact them?")
    anything_else = forms.CharField(label="Anything else we should know?",
                                    widget=forms.Textarea(attrs={"placeholder": "Anything else we should know?"}),
                                    help_text=mark_safe("Allergies, medical conditions etc.<br>If your contact knows"
                                                        " you by a different name to the one we commonly use for you"
                                                        " please list it here."))
    how_find_us = forms.CharField(label="How did you find out about us?",
                                  widget=forms.Textarea(attrs={"placeholder": "How did you find out about us?"}),
                                  help_text="It would help our promotion team if you let us know how you found out "
                                            "about us")

    class Meta:
        fieldsets = (
            ('member_data', {
                'fields': (
                    'name',
                    'email',
                    'password',
                    'password_check',
                    'username',
                    'address',
                    'address1',
                    'city',
                    'postcode',
                    'phone'),
                'classes': 'member_data'
            }),
            (mark_safe('Emergency Contact<br>Who should we contact if you chop your arm off?'), {
                'fields': ('emergency_contact_name', 'emergency_contact_num', 'anything_else'),
                'classes': 'emergency_contact'
            }),
            ('stats', {
                'fields': ('how_find_us',),
                'classes': 'stats'
            }),
        )

forms.BaseForm.fieldsets = fieldsets
