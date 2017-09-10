from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.conf import settings
from mcp.ldap import HackspaceIPA, LDAPMergeBackend

# THIS IS SHAMEFUL DO NOT LOOK
@receiver(post_save, sender=User, weak=False)
def save_user(sender, **kwargs):
    user_from_save = kwargs['instance']
    user_from_ldap = HackspaceIPA().GetIPAUser(user_from_save.username)

    if user_from_ldap:
        attrs = {}
        if user_from_save.email != user_from_ldap['mail'][0]:
            print ("We need to save the email address! Old: %s,  New: %s" % (user_from_ldap['mail'][0], user_from_save.email))
            attrs['mail']=user_from_save.email
        if user_from_save.first_name != user_from_ldap['givenname'][0]:
            print ("We need to save the first name!  Old: %s,  New: %s" % (user_from_ldap['givenname'][0], user_from_save.first_name))
            attrs['givenname']=user_from_save.first_name
        if user_from_save.last_name != user_from_ldap['sn'][0]:
            print ("We need to save the last name!  Old: %s,  New: %s" % (user_from_ldap['sn'][0], user_from_save.last_name))
            attrs['sn']=user_from_save.last_name

        # If the user is changing their first name or surname update their full name.
        # This is really gross and absolutely one of the 'things programmers believe
        # about names' fallacies but right now i just want this shit to work.
        if 'sn' in attrs or 'givenname' in attrs:
            attrs['cn'] = "{} {}".format('givenname' in attrs and attrs['givenname'] or user_from_ldap['givenname'][0], 'sn' in attrs and attrs['sn'] or user_from_ldap['sn'][0])
            attrs['displayname'] = attrs['cn']
            attrs['gecos'] = attrs['cn']
            attrs['initials'] = "".join(item[0].upper() for item in attrs['cn'].split())

        if kwargs:
            return HackspaceIPA().ModifyIPAUser(user_from_save.username, **attrs)
    return False
