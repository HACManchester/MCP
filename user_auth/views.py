from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import SignupForm
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

@login_required
def test(request):
    return HttpResponse("Testy Test.  Test! (%s)" % request.user)
