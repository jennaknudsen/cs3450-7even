from django import template

from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from dansbagels.models import *

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the dansbagels index.")


def test(request):
    return HttpResponse("You made it to the dansbagels test.")


def prototype2(request):
    # get database info here to pass in
    listOfUsers = []
    allPeople = Person.objects.all()

    context = {
        'all_users': allPeople
    }

    return render(request, 'dansbagels/prototype2.html', context)


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


def createAccount(request):
    context = {'purpose': "Account creation"}
    return render(request, 'dansbagels/createAccount.html', context)


def login(request):
    context = {'purpose': "Log in"}
    return render(request, 'dansbagels/login.html', context)


def home(request):
    context = {'purpose': "Home page"}
    return render(request, 'dansbagels/home.html', context)


def orderBagel(request):
    context = {'purpose': "Order Bagel"}
    return render(request, 'dansbagels/orderBagel.html', context)


def account(request):
    context = {'purpose': "View/Change account info"}
    return render(request, 'dansbagels/account.html', context)


def admin__add_rem(request):
    context = {'purpose': "View/add/remove accounts: admin only"}
    return render(request, 'dansbagels/admin__add_rem.html', context)



def changepassword(request):
    thisUsername = request.POST['user']
    newPassword = request.POST['new_password']
    
    thisUser = Person.objects.get(username_text=thisUsername)
    thisUser.password_text = newPassword
    thisUser.save()

    # return HttpResponseRedirect
    return HttpResponseRedirect(reverse('prototype1'))
