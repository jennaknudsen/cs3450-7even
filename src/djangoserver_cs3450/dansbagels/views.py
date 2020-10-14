from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the dansbagels index.")

def test(request):
    return HttpResponse("You made it to the dansbagels test.")
