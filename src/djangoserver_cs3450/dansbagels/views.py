from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the dansbagels index.")


def test(request):
    return HttpResponse("You made it to the dansbagels test.")


def prototype2(request):
    # get database info here to pass in
    # here is a dummy version
    dummy = 'dummy string'
    # use the string in the first spot to reference the variable in the template file.
    context = {'dummy': dummy}

    return render(request, 'dansbagels/prototype2.html', context)
