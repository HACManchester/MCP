import json
from ldap3 import *
from string import Template

userDnTemplate = Template("CN=$username,CN=Users,DC=hackspace,DC=internal")
groupDnTemplate = Template("cn=$group_name,ou=Groups,dc=hackspace,dc=internal")

s = Server('ldaps://testserver.hackspace.internal:636', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema
c = Connection(s, user='CN=Administrator,CN=Users,DC=hackspace,DC=internal', password='Password4LDAP', auto_bind=True)

with open("users.json") as f:
    users = json.load(f)
    for user in users:
        print ("- Creating User %s (%s)" % (user['username'], user['display_name']))
        user['dn'] = userDnTemplate.substitute(user)

        createUser = {}
        createUser['objectClass'] = ['top','organizationalPerson','person','user']
        createUser['cn'] = user['username']
        createUser['samAccountName'] = user['username']
        createUser['description'] = user['display_name']
        createUser['displayName'] = user['display_name']

        c.add(user['dn'], attributes=createUser)

        for role in user['roles']:
            print ("  - Adding to group %s" % role)
            groupDn = groupDnTemplate.substitute({'group_name':role})
            c.modify(groupDn, {'member': [(MODIFY_ADD, [user['dn']])]})
