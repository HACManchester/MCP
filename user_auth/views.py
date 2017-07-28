from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = SignupForm()

    return render(request, 'user_auth/index.htm', {'form': form})

def thanks(request):
    return

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/profile/')
    else:
        form = LoginForm()

    return render(request, 'user_auth/login.htm', {'form': form})

@login_required
def test(request):
    return HttpResponse("Testy Test.  Test! (%s)" % request.user)
