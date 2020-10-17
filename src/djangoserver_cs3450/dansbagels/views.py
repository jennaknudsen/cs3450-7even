from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from dansbagels.models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the dansbagels index.")

def prototype1(request):
    # list will be of tuples (username, password)
    listOfUsers = []
    allPeople = Person.objects.all()
    for person in allPeople:
        listOfUsers.append((person.username_text, person.password_text))
    context = {
        'all_users' : listOfUsers
    }
    return render(request, 'dansbagels/prototype1.html', context)

def changepassword(request):
    thisUsername = request.POST['user']
    newPassword = request.POST['new_password']
    
    thisUser = Person.objects.get(username_text=thisUsername)
    thisUser.password_text = newPassword
    thisUser.save()

    # return HttpResponseRedirect
    return HttpResponseRedirect(reverse('prototype1'))
