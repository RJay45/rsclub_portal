# from django.shortcuts import render
from django.http import HttpResponse
from rsapi import api
import string
import random


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        # user = authenticate()
        return HttpResponse("You are not authenticated")

    rsc = api.Api()
    """
    return HttpResponse(str(
        rsc.domain_register(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + ".com",
                            2,("ns1.onlyfordemo.net", "ns2.onlyfordemo.net"), 13665636, 47313197, 47313197, 47313197,
                            47313197,47313197, InvoiceMode.NoInvoice)))
    """
    return HttpResponse(str(
        rsc.domain_order_search(50, 1, status=api.DomainStatus.Active)
    ))
