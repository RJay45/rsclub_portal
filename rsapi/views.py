# from django.shortcuts import render
from django.http import HttpResponse
from rsapi.api import Api, InvoiceMode, DomainStatus
import string
import random


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        # user = authenticate()
        return HttpResponse("You are not authenticated")

    rsc = Api()

    return HttpResponse(str(
        rsc.domain_register(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + ".com",
                            random.randint(1,10),("ns1.onlyfordemo.net", "ns2.onlyfordemo.net"), 13665636, 47313197, 47313197, 47313197,
                            47313197,47313197, InvoiceMode.NoInvoice)))
    """
    return HttpResponse(str(
        rsc.domain_order_search(50, 1, status=DomainStatus.Active)
    ))
    """

