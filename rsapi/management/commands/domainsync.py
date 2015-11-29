from django.core.management.base import BaseCommand, CommandError
from rsapi.api import Api, OrderBy
from time import time
from math import ceil, floor
from datetime import datetime


class Command(BaseCommand):
    help = 'Get a list of domains about to expire'

    def add_arguments(self, parser):
        """parser.add_argument('poll_id', nargs='+', type=int)"""

    def handle(self, *args, **options):
        api = Api()
        page = 1
        per_page = 10
        num_pages = 1
        expire_time = int(time() + (60*60*24*30*1000))        #Remove the last 36..
        all_domains = []

        while page <= num_pages:
            domains = api.domain_order_search(per_page, page, expiry_date_end=expire_time, order_by=OrderBy.EndTime)
            page_items = int(domains.get("recsonpage"))

            if page_items == 0:
                break

            total_items = int(domains.get("recsindb"))
            num_pages = ceil(total_items / page_items)

            for i in range(1, page_items+1):
                end_timestamp = int(domains.get(str(i)).get("orders.endtime"))
                end_date = datetime.fromtimestamp(end_timestamp).strftime("%d %b %Y")
                days_left = floor((end_timestamp - time()) / 60 / 60 / 24)
                all_domains.append((domains.get(str(i)).get("entity.description"), end_date, days_left))

            page += 1

        print(all_domains)

"""
{'recsonpage': '3',
 '3': {'orders.privacyprotection': 'false', 'orders.creationtime': '1448833786', 'entity.description': '2dh0i1mkwtwoow8.com', 'orders.customerlock': 'true', 'entitytype.entitytypename': '.COM Domain Name', 'orders.orderid': '64246751', 'entity.entitytypeid': '3', 'orders.timestamp': '2015-11-29 21:49:58.18267+00', 'entity.entityid': '64246751', 'entity.customerid': '13665636', 'orders.endtime': '1511992186', 'orders.creationdt': '1448833797', 'orders.resellerlock': 'false', 'entity.currentstatus': 'Active', 'entitytype.entitytypekey': 'domcno', 'orders.autorenew': 'false', 'orders.transferlock': 'true'},
 'recsindb': '3',
 '1': {'orders.privacyprotection': 'false', 'orders.creationtime': '1448833761', 'entity.description': '2b07agnis5xtfj5.com', 'orders.customerlock': 'true', 'entitytype.entitytypename': '.COM Domain Name', 'orders.orderid': '64246743', 'entity.entitytypeid': '3', 'orders.timestamp': '2015-11-29 21:49:33.24664+00', 'entity.entityid': '64246743', 'entity.customerid': '13665636', 'orders.endtime': '1511992161', 'orders.creationdt': '1448833772', 'orders.resellerlock': 'false', 'entity.currentstatus': 'Active', 'entitytype.entitytypekey': 'domcno', 'orders.autorenew': 'false', 'orders.transferlock': 'true'},
 '2': {'orders.privacyprotection': 'false', 'orders.creationtime': '1448833778', 'entity.description': '8uba9uqpawn5yrl.com', 'orders.customerlock': 'true', 'entitytype.entitytypename': '.COM Domain Name', 'orders.orderid': '64246745', 'entity.entitytypeid': '3', 'orders.timestamp': '2015-11-29 21:49:50.435998+00', 'entity.entityid': '64246745', 'entity.customerid': '13665636', 'orders.endtime': '1511992178', 'orders.creationdt': '1448833789', 'orders.resellerlock': 'false', 'entity.currentstatus': 'Active', 'entitytype.entitytypekey': 'domcno', 'orders.autorenew': 'false', 'orders.transferlock': 'true'}}


[('u5mhr6d4bp7p0lt.com', '29 Nov 2016', 365),
('0nfvjzudr6vsoda.com', '29 Nov 2016', 365),
('6t73arqth8lpu6h.com', '29 Nov 2016', 365),
 ('2b07agnis5xtfj5.com', '29 Nov 2017', 730),
 ('8uba9uqpawn5yrl.com', '29 Nov 2017', 730),
 ('2dh0i1mkwtwoow8.com', '29 Nov 2017', 730),
 ('j4iwdg0xn7zennj.com', '29 Nov 2018', 1095),
 ('2z55gkoys3rhhov.com', '29 Nov 2018', 1095),
 ('0dngsiqlqe0gtap.com', '29 Nov 2019', 1460),
 ('3ibuw9z3rsb0mar.com', '29 Nov 2019', 1460),
 ('i4qzjneyvyizh2d.com', '29 Nov 2019', 1460),
 ('4a1tam4ly2x35ha.com', '29 Nov 2021', 2191),
 ('bv4xnrn51ncn308.com', '29 Nov 2022', 2556),
 ('hu8vwg3bahgpkba.com', '29 Nov 2023', 2921),
 ('4ijfwbff99k0cso.com', '29 Nov 2023', 2921),
 ('g324k38u4un08st.com', '29 Nov 2024', 3287),
 ('l73vflbtwsf0db8.com', '29 Nov 2025', 3652),
 ('p1zx01jxsamawii.com', '29 Nov 2025', 3652)]

 """