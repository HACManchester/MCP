# I had to subclass the LDAPBackend because we want to be able to log in with usernames or
# email addresses, and django_auth_ldap gets like 90% of the way there but then
# fails at the last hurdle.
#https://bitbucket.org/illocution/django-auth-ldap/issues/63/authentication-against-different-ldap

from django_auth_ldap.backend import LDAPBackend
import ipahttp
import os
import random, string
import requests

from django.forms import CharField
from django.core import validators
from django.core.exceptions import ValidationError

def validate_ldap_username(value):
    user = LDAPMergeBackend().populate_user(value)
    if user is not None:
        raise ValidationError(
            'Sorry, username %(value)s is already in use.',
            params={'value': value},
        )

class LDAPUsernameField(CharField):
    default_validators = [validate_ldap_username]

class LDAPMergeBackend(LDAPBackend):
    def get_or_create_user(self, username, ldap_user):
        """
        This must return a (User, created) 2-tuple for the given LDAP user.
        username is the Django-friendly username of the user. ldap_user.dn is
        the user's DN and ldap_user.attrs contains all of their LDAP attributes.
        """
        model = self.get_user_model()
        username_field = getattr(model, 'USERNAME_FIELD', 'username')

        ldap_username_field = self.settings.USER_ATTR_MAP.get(username_field, None)
        if ldap_username_field:
            ldap_username = ldap_user.attrs.get(ldap_username_field, None)
            if ldap_username:        # Attribute not present/empty: fall back to user supplied name
                ldap_username = ldap_username[0]
            else:
                ldap_username = username
        else:            # No mapping defined, fall back to user supplied name
            ldap_username = username

        kwargs = {
            username_field + '__iexact': ldap_username,
            'defaults': {username_field: ldap_username.lower()}
        }

        return model.objects.get_or_create(**kwargs)

# Abstracts the raw ipa api calls to a standard interface which we can add extra nice things to
class HackspaceIPA():
    def __init__(self):
        self.ipa = ipahttp.ipa(os.environ.get('IPA_URL'), sslverify=True)
        self.ipa.login(os.environ.get('IPA_ADMIN_USER'), os.environ.get('IPA_ADMIN_PASSWORD'))

    def GetIPAUser(self, username):
        user = self.ipa.user_show(username)
        if user['error'] is None:
            return user['result']['result']

    def ModifyIPAUser(self, username, **kwargs):
        setattrs = []
        for arg in kwargs:
            setattrs.append("{0}={1}".format(arg, kwargs[arg]))
        print(setattrs)
        result = self.ipa.user_mod(username, setattrs=setattrs)
        return result['error'] is not None

    def CreateIPAUser(self, username, name, email):
        ename = name.split()
        tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20))
        return self.ipa.user_add(username, opts={'givenname':ename[0], 'sn':ename[-1], 'cn':name, 'displayname':username, 'mail':email, 'userpassword':tmp_pass})

    def ChangeIPAUserPassword(self, username, new_password, **kwargs):
        if 'old_password' not in kwargs:
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20))
            result = self.ipa.user_mod(username, setattrs=['userpassword='+tmp_pass])
            kwargs['old_password'] = tmp_pass

        headers = {
          'Accept': 'text/plain',
          'Content-Type': 'application/x-www-form-urlencoded',
          'Referer': os.environ.get('IPA_URL')
        }

        params = {
            'user': username,
            'old_password': kwargs['old_password'],
            'new_password': new_password
        }

        r = requests.post('https://'+os.environ.get('IPA_URL')+'/ipa/session/change_password', data=params, headers=headers)

        #       read the results back, if it wasn't 200 it failed, if it was 200 but the body has rejected in it, it failed
        if r.status_code == 200:
            if 'rejected' not in r.text:
                return True
        return False
