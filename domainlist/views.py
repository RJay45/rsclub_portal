from django.shortcuts import render
from rsapi.api import Api, ApiException, OrderBy
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    rsc = Api()
    template_variables = {}

    try:
        result = rsc.domain_order_search(100, 1, order_by=(OrderBy.EndTime,),
                                         expiry_date_start=(datetime.now() + timedelta(days=90)).timestamp())
        output_result = []
        num_items = int(result.get("recsonpage"))

        for i in range(1, num_items+1):
            entry = {
                'name': result.get(str(i)).get("entity.description"),
                'expire': datetime.fromtimestamp(int(result.get(str(i)).get("orders.endtime"))).strftime("%d %m %Y")
            }
            output_result.append(entry)

        template_variables['domains'] = output_result

    except ApiException as e:
        template_variables['error'] = e.message
        template_variables['error_req'] = e.request
        template_variables['error_res'] = e.response

    return render(request, 'domainlist/index.html', template_variables)

def pagetest(request):
    template_variables = {
        'domains': ({
                        'name': 'domain1.com',
                        'expire': '1 Jan 1970'
                    },
                    {
                        'name': 'domain2.com',
                        'expire': '2 Apr 2010'
                    }),
    }
    return render(request, 'domainlist/index.html', template_variables)
