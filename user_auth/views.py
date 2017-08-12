from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import SignupForm
from django.contrib.auth.decorators import login_required

from mcp.ldap import HackspaceIPA


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("Creating user {username} {name} {email} {password}".format(**form.cleaned_data))
            ipa = HackspaceIPA()
            result = ipa.CreateIPAUser(form.cleaned_data['username'], form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['password'])

            if not result['error']:
                pass
                #We have created the user!
                # Grab their user from LDAP auth
            else:
                print ('{name} Error Creating user! {message}'.format(**result['error']))
                pass
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = SignupForm(label_suffix='')

    return render(request, 'user_auth/register.htm', {'form': form})


def thanks(request):
    return

@login_required
def test(request):
    return HttpResponse("Testy Test.  Test! (%s)" % request.user)
