from django.shortcuts import render
from django.http import HttpResponse
from rsapi.api import Api


# Create your views here.
def index(request):
    rsc = Api()
    return HttpResponse(str(rsc.check_domain_availability("google", "com")))
