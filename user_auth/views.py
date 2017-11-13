from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

from .forms import SignupForm
from .models import Member, MemberEmergencyContacts
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from mcp.ldap import HackspaceIPA, LDAPMergeBackend

from datetime import datetime


def index(request):
    # TODO: if loogged out render this
    return render(request, 'user_auth/index.htm')
    # TODO: if logged in render dashboard


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("Creating user {username} {name} {email} {password}".format(**form.cleaned_data))
            ipa = HackspaceIPA()
            result = ipa.create_ipa_user(form.cleaned_data['username'], form.cleaned_data['name'],
                                         form.cleaned_data['email'])

            if not result['error']:
                pwc_result = ipa.change_ipa_user_password(form.cleaned_data['username'],
                                                          new_password=form.cleaned_data['password'])

                new_user = LDAPMergeBackend().populate_user(form.cleaned_data['username'])
                new_user.save()

                new_member = Member(
                    user=new_user,
                    address=form.cleaned_data['address'],
                    address1=form.cleaned_data['address1'],
                    city=form.cleaned_data['city'],
                    postcode=form.cleaned_data['postcode'],
                    phone=form.cleaned_data['phone'],
                    membership_expiry=datetime.now(),
                    emergency_information=form.cleaned_data['anything_else']
                )
                new_member.save()

                new_emergency_contact = MemberEmergencyContacts(
                    member=new_member,
                    name=form.cleaned_data['emergency_contact_name'],
                    phone=form.cleaned_data['emergency_contact_num']
                )
                new_emergency_contact.save()

                new_request = HttpRequest()
                if request.session:
                    new_request.session = request.session
                else:
                    new_request.session = engine.SessionStore()

                print("Getting authenticated user object from ldap")
                new_auth_user = authenticate(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             backend=LDAPMergeBackend)
                print("Logging in with our new object")
                login(new_request, new_auth_user)
                print("We are now logged in maybe?")

                return HttpResponseRedirect('/payments/')
            else:
                print('{name} Error Creating user! {message}'.format(**result['error']))
                pass
            return HttpResponseRedirect('/thanks/')
    else:
        form = SignupForm(label_suffix='')

    return render(request, 'user_auth/register.htm', {'form': form})


def thanks(request):
    return


@login_required
def test(request):
    return HttpResponse("Testy Test.  Test! (%s)" % request.user)
