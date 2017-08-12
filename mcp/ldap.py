# I had to subclass this because we want to be able to log in with usernames or
# email addresses, and django_auth_ldap gets like 90% of the way there but then
# fails at the last hurdle.
#https://bitbucket.org/illocution/django-auth-ldap/issues/63/authentication-against-different-ldap

from django_auth_ldap.backend import LDAPBackend
import ipahttp
import os

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

class HackspaceIPA():
    def __init__(self):
        self.ipa = ipahttp.ipa(os.environ.get('IPA_URL'), sslverify=True)
        self.ipa.login(os.environ.get('IPA_ADMIN_USER'), os.environ.get('IPA_ADMIN_PASSWORD'))

    def ModifyIPAUser(self, username, **kwargs):
        pass

    def CreateIPAUser(self, username, name, email, password):
        ename = name.split()
        return self.ipa.user_add(username, opts={'givenname':ename[0], 'sn':ename[-1], 'cn':name, 'displayname':username, 'mail':email, 'userpassword':password})
