from django.shortcuts import render, redirect
from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class LoginException(Exception):
    def __init__(self, response):
        self.response = response


def login_page(request, error=None):
    params = {}

    if isinstance(error, str):
        params['error'] = error

    return render(request, "login/login.html", params)


def do_login(request):
    if request.method != 'POST':
        return login_page(request)

    form = LoginForm(request.POST)

    if not form.is_valid():
        return login_page(request, "Please enter a username and password.")

    user = auth.authenticate(username=form.cleaned_data.get('username'),
                             password=form.cleaned_data.get('password'))

    if user is None:
        return login_page(request, "Incorrect username or password.")

    return redirect('/home/')


def show_user(request):
    if not request.user.is_authenticated():
        raise LoginException(login_page(request))

    #request.user.
