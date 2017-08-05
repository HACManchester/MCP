# I had to subclass this because we want to be able to log in with usernames or
# email addresses, and django_auth_ldap gets like 90% of the way there but then
# fails at the last hurdle.
#https://bitbucket.org/illocution/django-auth-ldap/issues/63/authentication-against-different-ldap

from django_auth_ldap.backend import LDAPBackend

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
