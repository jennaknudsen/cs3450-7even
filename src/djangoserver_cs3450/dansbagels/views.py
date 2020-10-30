from django import template

from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from dansbagels.models import *
from .forms import *
from .dbfunctions import *

# import helper functions from dbfunctions.py
from dansbagels.dbfunctions import *


# URL: localhost:8000/dansbagels/
def index(request):
    return HttpResponse("Hello, world. You're at the dansbagels index.")


# URL: localhost:8000/dansbagels/test
def test(request):
    return HttpResponse("You made it to the dansbagels test.")


# URL: localhost:8000/dansbagels/prototype1
def prototype1(request):
    # list will be of tuples (username, password)
    listOfUsers = []
    allPeople = Person.objects.all()
    for person in allPeople:
        listOfUsers.append((person.username_text, person.password_text))
    context = {
        'all_users': listOfUsers
    }
    return render(request, 'dansbagels/prototype1.html', context)


# URL: localhost:8000/dansbagels/prototype1/changepassword
def changepassword(request):
    thisUsername = request.POST['user']
    newPassword = request.POST['new_password']
    
    thisUser = Person.objects.get(username_text=thisUsername)
    thisUser.password_text = newPassword
    thisUser.save()

    # return HttpResponseRedirect
    return HttpResponseRedirect(reverse('prototype1'))


# URL: localhost:8000/dansbagels/prototype2
def prototype2(request):
    # get database info here to pass in
    listOfUsers = []
    allPeople = Person.objects.all()

    context = {
        'all_users': allPeople
    }

    return render(request, 'dansbagels/prototype2.html', context)


# URL: localhost:8000/dansbagels/createAccount
def createAccount(request):
    if request.method == 'GET':
        form = AccountCreation()
        context = {
            'purpose': "Account creation",
            'form': form
        }
        return render(request, 'dansbagels/createAccount.html', context)
    if request.method == 'POST':
        form = AccountCreation(request.POST)
        if form.is_valid():
            createAccountDB(
                firstName=form.cleaned_data['firstName'],
                lastName=form.cleaned_data['lastName'],
                email=form.cleaned_data['email'],
                phoneNumber=form.cleaned_data['phone'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                accountType=AccountType(AccountType.CUSTOMER)
            )
        return redirect('login')


# URL: localhost:8000/dansbagels/login
def login(request):
    context = {'purpose': "Log in"}
    # if logged in, set the proper context flags to show user that's logged in
    if 'logged_in' in request.session and request.session['logged_in']:
        username = request.session['username']
        context['username'] = username
        context['user_is_logged_in'] = True
    # otherwise, if there was a failed login then show a message
    elif 'failed_login' in request.session and request.session['failed_login']:
        context['failed_login'] = True
    # no matter what the state of the login is, we can still render the exact
    # same HTML page!
    return render(request, 'dansbagels/login.html', context)


# POST request from login.html
# URL: localhost:8000/dansbagels/login/prototypelogin
def prototype_login(request):
    username = request.POST['username']
    password = request.POST['password']
    # use internal function to verify the login
    if verifyLogin(username, password):
        # set correct flags upon successful login
        request.session['logged_in'] = True
        request.session['username'] = username
        request.session['password'] = password
        request.session['accountType'] = Person.objects.get(username_text=username).accountType.accountType_text
        # remove "failed login" flag upon successful login
        try:
            del request.session['failed_login']
        except KeyError:
            pass
    else:
        request.session['failed_login'] = True
    return HttpResponseRedirect(reverse('login'))


# another POST request from login.html
# URL: localhost:8000/dansbagels/login/prototypelogout
def prototype_logout(request):
    request.session['logged_in'] = False
    try:
        del request.session['username']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('login'))


# URL: localhost:8000/dansbagels/home
def home(request):
    context = {'purpose': "Home page"}
    return render(request, 'dansbagels/home.html', context)


# URL: localhost:8000/dansbagels/orderBagel
def orderBagel(request):
    context = {'purpose': "Order Bagel"}
    return render(request, 'dansbagels/orderBagel.html', context)


# URL: localhost:8000/dansbagels/account
def account(request):
    context = {'purpose': "View/Change account info"}
    try:
        account = Person.objects.get(username_text=request.session['username'])
        context['userName'] = request.session['username']
        context['password'] = request.session['password']
        context['firstName'] = str(account.firstName_text)
        context['lastName'] = account.lastName_text
        context['email'] = account.email_email
        context['phoneNumber'] = account.phoneNumber_text
        context['accountBalance'] = str(account.accountBalance_decimal)
        context['accountType'] = request.session['accountType']
        return render(request, 'dansbagels/account.html', context)
    except Exception:
        return redirect('login')


# URL: localhost:8000/dansbagels/admin/add_rem
def admin__add_rem(request):
    if request.method == "GET":
        form = ManagerAccountCreation()
        context = {
            'purpose': "View/add/remove accounts: admin only",
            'form': form,
            'permitted': True if request.session['accountType'] == 'Manager' else False,
            'people': Person.objects.all()
        }
        return render(request, 'dansbagels/admin__add_rem.html', context)
    if request.method == "POST":
        form = ManagerAccountCreation(request.POST)
        if form.is_valid():
            createAccountDB(
                firstName=form.cleaned_data['firstName'],
                lastName=form.cleaned_data['lastName'],
                email=form.cleaned_data['email'],
                phoneNumber=form.cleaned_data['phone'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                accountType=AccountType(form.cleaned_data['accountType'])
            )
        return redirect(request.path)



