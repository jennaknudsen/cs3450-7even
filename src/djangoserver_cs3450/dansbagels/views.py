from django import template

from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from dansbagels.models import *
from .forms import *
from .dbfunctions import *
from datetime import datetime
from django.utils import timezone
import pytz

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
    context = {}
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
    if verifyLoginDB(username, password):
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
    context = {'purpose': "Order Bagel",
               'menuItems': MenuItem.objects.all(),
               'orderForm': OrderBagel(),
               'logged_in': True if 'logged_in' in request.session and request.session['logged_in'] is True else False
               }
    return render(request, 'dansbagels/orderBagel.html', context)


# URL: localhost:8000/dansbagels/account
def account(request):
    context = {'purpose': "View/Change account info"}
    if 'logged_in' in request.session and request.session['logged_in']:
        account = Person.objects.get(username_text=request.session['username'])
        if request.method == "GET":
            orderHistory = Order.objects.get(personOrdered=account)
            orderLineItemHistory = []
            for order in orderHistory:
                # only get orderLineItems from orders the account placed
                orderLineItemHistory.append(orderLineItemHistory.objects.get(order=order))
            context['userName'] = account.username_text
            context['password'] = account.password_text
            context['firstName'] = str(account.firstName_text)
            context['lastName'] = account.lastName_text
            context['email'] = account.email_email
            context['phoneNumber'] = account.phoneNumber_text
            context['accountBalance'] = str(account.accountBalance_decimal)
            context['accountType'] = request.session['accountType']
            context['updateAccountForm'] = UpdateAccount()
            context['orderHistory'] = orderHistory
            context['orderLineItemHistory'] = orderLineItemHistory

            return render(request, 'dansbagels/account.html', context)
        if request.method == "POST":
            form = UpdateAccount(request.POST)
            if form.is_valid():
                if updateAccountDB(
                    # series of ternary statements that check if the user inputed something into the field
                    # if the field is blank then it plugs in the users existing info
                    oldUsername=request.session['username'],
                    firstName=account.firstName_text if form.cleaned_data['firstName'] == '' else form.cleaned_data['firstName'],
                    lastName=account.lastName_text if form.cleaned_data['lastName'] == '' else form.cleaned_data['lastName'],
                    email=account.email_email if form.cleaned_data['email'] == '' else form.cleaned_data['email'],
                    phoneNumber=account.phoneNumber_text if form.cleaned_data['phone'] == '' else form.cleaned_data['phone'],
                    username=account.username_text if form.cleaned_data['username'] == '' else form.cleaned_data['username'],
                    password=account.password_text if form.cleaned_data['password'] == '' else form.cleaned_data['password'],
                    accountBalance=account.accountBalance_decimal if form.cleaned_data['accountBalance'] is None else form.cleaned_data['accountBalance']
                ):
                    if form.cleaned_data['username'] != "":
                        request.session['username'] = form.cleaned_data['username']
            return redirect(request.path)
    else:
        return redirect('login')


# URL: localhost:8000/dansbagels/admin/add_rem
def admin__add_rem(request):
    if request.method == "GET":
        context = {
            'purpose': "View/add/remove accounts: admin only",
            'form': ManagerAccountCreation(),
            'permitted': True if 'accountType' in request.session and request.session['accountType'] == 'Manager' else False,
            'people': Person.objects.all(),
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

# URL: localhost:8000/dansbagels/deleteAccount
# only intended to handle post requests from admin/add_rem
def deleteAccount(request):
    if request.method == "POST":
        deleteAccountDB(request.POST.get('DeleteButton'))
    return redirect('admin__add_rem')


def placeOrder(request):
    if request.method == "POST":
        form = OrderBagel(request.POST)
        if form.is_valid():
            orderDate = str(form.cleaned_data['pickUpDate'])
            orderTime = str(form.cleaned_data['pickUpTime']).split(":")
            order = createOrderDB(
                pickUpTime=datetime.datetime(year=int(orderDate[0:4]), month=int(orderDate[5:7]), day=int(orderDate[8:10]),
                                    hour=int(orderTime[0]), minute=int(orderTime[1]), second=0, tzinfo=pytz.UTC),
                personOrdered=Person.objects.get(username_text=request.session['username']),
                currentStatus=OrderStatus.objects.get(orderStatus_text="Ordered")
            )
            itemsOrdered = form.cleaned_data['itemsOrdered'].split(",")
            for i in range(0,len(itemsOrdered), 2):
                createOrderLineItemDB(
                    itemOrdered=MenuItem.objects.get(itemName_text=itemsOrdered[i+1]),
                    order=order,
                    orderQuantity=int(itemsOrdered[i])
                )
        return redirect("home")  # temp redirect, should redirect to order status page
