from django.shortcuts import render
from django.http import HttpResponse
from rsapi.api import Api


# Create your views here.
def index(request):
    j = Api()
    return HttpResponse("Testing 123...")